import json
import os
import plistlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import yaml

from src import apps
from src import config as model
from src import install as installer

SOURCE = Path(__file__).resolve().parents[1]
main, prompt = installer.main, installer.prompt
vscode, iterm = apps.VSCode(), apps.ITerm()
configuration = repository = installer
preferences = apps


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo with spaces"
        self.root.mkdir(parents=True)
        shutil.copy2(SOURCE / "install.yaml", self.root / "install.yaml")
        shutil.copytree(SOURCE / "home", self.root / "home")
        shutil.copytree(
            SOURCE / "src", self.root / "src", ignore=shutil.ignore_patterns("__pycache__")
        )
        self.catalog = model.load_catalog(self.root / "install.yaml")
        for bundle in self.catalog:
            for config in bundle.configuration:
                source = self.root / config.source
                source.parent.mkdir(parents=True, exist_ok=True)
                if config.adapter or config.source.endswith(
                    ("sheldon", "atuin", "/git", "/ruff", "karabiner", "linearmouse", "dev-flow")
                ):
                    source.mkdir(exist_ok=True)
                    (source / "settings.json").write_text("{}\n")
                else:
                    source.write_text("original\n")
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.test")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        self.local_home = Path(self.temp.name) / "local-home"
        self.local_home.mkdir()
        home_patch = patch.object(configuration.Path, "home", return_value=self.local_home)
        home_patch.start()
        self.addCleanup(home_patch.stop)
        self.choices = {b.id: "k" for b in self.catalog}
        fork = patch("src.install.run_shell")
        fork.start()
        self.addCleanup(fork.stop)

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True)

    def plan(self):
        return model.resolve(self.catalog, self.choices)

    def test_setup_groups_match_the_requested_order(self):
        self.assertEqual(
            [stage.id for stage in self.catalog],
            [
                "setup-terminal",
                "setup-macos",
                "setup-development",
                "setup-codex",
                "setup-desktop",
                "setup-vscode",
                "setup-iterm",
            ],
        )
        document = yaml.safe_load((self.root / "install.yaml").read_text())
        for name in ("macos", "vscode", "iterm"):
            self.assertIn("settings", document["setup-" + name])
            self.assertNotIn(name, document["settings"])

    def test_stage_prompts_and_invalid_retry(self):
        with patch("builtins.input", side_effect=["invalid", *([""] * len(self.catalog))]) as ask:
            self.assertEqual(prompt(self.catalog), self.choices)
        self.assertEqual(ask.call_count, len(self.catalog) + 1)

    def test_selection_and_shared_dependency_are_resolved_once(self):
        self.choices["setup-desktop"] = "i"
        plan = self.plan()
        names = [p.name for p in plan.packages]
        self.assertEqual(names.count("mas"), 1)
        self.assertNotIn("visual-studio-code", names)
        self.assertNotIn("tldr", names)

    def test_catalog_rejects_overlapping_ownership(self):
        path = self.root / "install.yaml"
        settings = yaml.safe_load(path.read_text())
        settings["setup-vscode"]["link"] = [{"source": "iterm2", "adapter": "iterm"}]
        path.write_text(yaml.safe_dump(settings))
        with self.assertRaisesRegex(ValueError, "overlapping owners"):
            model.load_catalog(self.root / "install.yaml")

    def test_cli_installs_github_cli_alongside_git(self):
        self.choices["setup-terminal"] = "i"
        self.assertTrue({"gh", "git", "git-lfs"} <= {p.name for p in self.plan().packages})

    def test_macos_commands_and_vscode_associations_have_separate_settings(self):
        settings = model.load("macos")
        self.assertNotIn("editor", settings)
        self.assertEqual(len(model.load("vscode")["file_associations"]), 6)
        self.assertIn("destination", model.load("iterm"))
        with patch.object(configuration.subprocess, "run") as run:
            configuration.macos_preferences()
        commands = [call.args[0] for call in run.call_args_list if call.args[0][0] == "defaults"]
        self.assertEqual(len(commands), 17)
        self.assertIn(
            ["defaults", "-currentHost", "write", "com.apple.controlcenter", "Sound", "-int", "18"],
            commands,
        )
        self.assertNotIn("duti", {call.args[0][0] for call in run.call_args_list})
        settings["defaults"] = ['defaults write test greeting "hello world"']
        with (
            patch.object(configuration, "load", return_value=settings),
            patch.object(configuration.subprocess, "run") as run,
        ):
            configuration.macos_preferences()
        self.assertIn(
            ["defaults", "write", "test", "greeting", "hello world"],
            [call.args[0] for call in run.call_args_list],
        )

    def test_vscode_associations_do_not_require_the_macos_stage(self):
        self.choices["setup-vscode"] = "i"
        self.shell_command("duti", 'echo "$*" >> "$COMMAND_LOG"\n')
        log = Path(self.temp.name) / "associations.log"
        with (
            patch.object(apps, "sync_apps"),
            patch.dict(
                os.environ,
                {
                    "PATH": str(Path(self.temp.name) / "commands")
                    + os.pathsep
                    + os.environ["PATH"],
                    "COMMAND_LOG": str(log),
                },
            ),
        ):
            configuration.apply(self.root, self.plan(), command="install")
        self.assertEqual(len(log.read_text().splitlines()), 6)

    def test_unknown_stage_actions_are_rejected(self):
        path = self.root / "install.yaml"
        path.write_text("setup-test: {title: Test, description: Test, mystery: true}\n")
        with self.assertRaisesRegex(ValueError, "Unknown actions"):
            model.load_catalog(path)

    def test_scalar_package_action_is_rejected_before_installation(self):
        path = self.root / "install.yaml"
        data = yaml.safe_load(path.read_text())
        data["setup-terminal"]["brew"] = "git"
        path.write_text(yaml.safe_dump(data))
        with self.assertRaisesRegex(ValueError, "setup-terminal.brew"):
            model.load_catalog(path)

    def test_home_links_automatically_even_when_optional_bundles_are_kept(self):
        with patch.object(apps, "sync_apps") as sync:
            configuration.apply(self.root, self.plan())
        target = self.local_home / ".config/starship.toml"
        self.assertTrue(target.is_symlink())
        self.assertFalse(target.parent.is_symlink())
        self.assertEqual(target.resolve(), (self.root / "home/.config/starship.toml").resolve())
        extra = self.local_home / ".config/new-app.conf"
        extra.write_text("local only")
        self.assertFalse((self.root / "home/.config/new-app.conf").exists())
        sync.assert_called_once_with(self.root, ())

    def test_missing_home_source_stops_before_linking(self):
        shutil.rmtree(self.root / "home")
        with self.assertRaisesRegex(RuntimeError, "Restore the repository home/"):
            configuration.check_sources(self.root, self.plan())
        self.assertEqual(list(self.local_home.iterdir()), [])

    def test_home_directory_link_migration_preserves_existing_files(self):
        (self.local_home / ".config").symlink_to(self.root / "home/.config")
        source = self.root / "home/.config/personal.conf"
        source.write_text("personal")
        configuration.link_home(self.root / "home", self.local_home)
        self.assertFalse((self.local_home / ".config").is_symlink())
        self.assertEqual((self.local_home / ".config/personal.conf").read_text(), "personal")
        self.assertEqual(source.read_text(), "personal")
        configuration.link_home(self.root / "home", self.local_home)
        self.assertEqual(len(list(self.local_home.glob("dotfiles-backup-*"))), 1)

    def test_delete_removes_local_sources_without_touching_index(self):
        self.choices["setup-vscode"] = "d"
        (self.root / "vscode/settings.json").write_text("local edit")
        (self.root / "vscode/private").write_text("local data")
        repository.prune_local(self.root, self.plan())
        self.assertFalse((self.root / "vscode").exists())
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "")
        repository.prune_local(self.root, self.plan())

    def test_existing_parent_symlink_neither_moves_nor_prunes_source(self):
        home = Path(self.temp.name) / "home"
        home.mkdir()
        (home / ".config").symlink_to(self.root / "home/.config", target_is_directory=True)
        source = self.root / "home/.config/starship.toml"
        with patch.object(configuration.Path, "home", return_value=home):
            configuration.link(source, home / ".config/starship.toml")
            self.choices["setup-terminal"] = "d"
            repository.prune_local(self.root, self.plan())
        self.assertTrue(source.is_file())
        self.assertFalse(source.is_symlink())

    def test_install_leaves_existing_index_untouched(self):
        (self.root / "home/.zshrc").write_text("existing edit")
        self.git("add", "home/.zshrc")
        before = self.git("diff", "--cached")
        with (
            patch("src.install.sys.platform", "darwin"),
            patch("builtins.input", side_effect=[*(["k"] * len(self.catalog)), "n"]),
        ):
            main(["install"], self.root)
        self.assertEqual(self.git("diff", "--cached"), before)

    def test_real_entrypoint_keeps_stdin_for_stage_prompts(self):
        shutil.copy2(SOURCE / "install", self.root / "install")
        self.shell_command("xcode-select", "exit 0\n")
        result = subprocess.run(
            ["bash", str(self.root / "install")],
            input="\n" * len(self.catalog) + "n\n",
            text=True,
            capture_output=True,
            env={
                **os.environ,
                "HOME": str(self.local_home),
                "PATH": str(Path(self.temp.name) / "commands") + os.pathsep + os.environ["PATH"],
            },
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        choices = json.loads((self.root / ".install/choices.local.json").read_text())
        self.assertEqual(choices, self.choices)
        self.assertTrue((self.local_home / ".zshrc").is_symlink())

    def test_regrouped_saved_choices_require_explicit_review(self):
        previous = {
            "shell": "i",
            "cli": "k",
            "development": "k",
            "vscode": "k",
            "iterm": "k",
            "ai": "k",
            "desktop": "k",
            "macos": "k",
        }
        with self.assertRaisesRegex(ValueError, "--choose"):
            model.resolve(self.catalog, previous)

    def test_repeat_install_reuses_choices_without_reprompting(self):
        with (
            patch("src.install.sys.platform", "darwin"),
            patch("builtins.input", side_effect=[*(["k"] * len(self.catalog)), "n"]),
            patch("src.install.run_shell") as install,
        ):
            main(["install"], self.root)
            install.assert_called_once_with("fork", "n", cwd=self.root)
        state = self.root / ".install/choices.local.json"
        self.assertEqual(json.loads(state.read_text()), self.choices)
        self.git("reset", "-q")
        with (
            patch("src.install.sys.platform", "darwin"),
            patch("builtins.input") as ask,
            patch("src.install.run_shell"),
        ):
            main(["install"], self.root)
            ask.assert_not_called()

    def test_failed_install_can_retry_saved_choices_without_staging(self):
        with (
            patch("src.install.sys.platform", "darwin"),
            patch(
                "builtins.input",
                side_effect=["i" if key == "setup-desktop" else "k" for key in self.choices],
            ),
            patch("src.install.run_shell", side_effect=RuntimeError("package failed")),
            self.assertRaisesRegex(RuntimeError, "package failed"),
        ):
            main(["install"], self.root)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "")
        with (
            patch("src.install.sys.platform", "darwin"),
            patch("builtins.input") as ask,
            patch("src.install.run_shell"),
        ):
            main(["install"], self.root)
            ask.assert_not_called()

    def run_fork(self, answer="y\n", fail=False):
        commands = Path(self.temp.name) / "commands"
        commands.mkdir(exist_ok=True)
        gh = commands / "gh"
        gh.write_text(
            "#!/bin/bash\n"
            'printf "%s\\n" "$*" >> "$FORK_LOG"\n'
            'case "$1 $2" in\n'
            '  "api user") echo friend ;;\n'
            '  "repo fork") [[ "$FORK_FAIL" != 1 ]] ;;\n'
            '  "repo view") echo dotfiles ;;\n'
            "esac\n"
        )
        gh.chmod(0o755)
        return subprocess.run(
            ["bash", str(SOURCE / "src/system.sh"), "--fork"],
            cwd=self.root,
            input=answer,
            text=True,
            capture_output=True,
            env={
                **os.environ,
                "PATH": str(commands) + os.pathsep + os.environ["PATH"],
                "FORK_LOG": str(Path(self.temp.name) / "fork.log"),
                "FORK_FAIL": "1" if fail else "0",
            },
            check=False,
        )

    def test_fork_requires_consent_and_updates_remotes_only_after_creation(self):
        origin = "https://github.com/source/dotfiles.git"
        self.git("remote", "add", "origin", origin)
        result = self.run_fork("n\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git("remote").strip(), "origin")
        self.assertFalse((Path(self.temp.name) / "fork.log").exists())
        result = self.run_fork()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git("remote").strip(), "origin")
        self.assertEqual(
            self.git("remote", "get-url", "origin").strip(),
            "https://github.com/friend/dotfiles.git",
        )

    def test_sync_uses_only_requested_adapters_and_isolates_failures(self):
        first = SimpleNamespace(sync=Mock(side_effect=RuntimeError("invalid settings")))
        second = SimpleNamespace(sync=Mock())
        with (
            patch.object(apps, "STATE", Path(self.temp.name) / "state"),
            patch.dict(apps.APPLICATIONS, {"vscode": lambda: first, "iterm": lambda: second}),
            self.assertRaisesRegex(RuntimeError, "vscode: invalid settings"),
        ):
            apps.sync_apps(self.root, ("vscode", "iterm"))
        first.sync.assert_called_once()
        second.sync.assert_called_once()

    def shell_command(self, name, content):
        directory = Path(self.temp.name) / "commands"
        directory.mkdir(exist_ok=True)
        script = directory / name
        script.write_text("#!/bin/bash\nset -euo pipefail\n" + content)
        script.chmod(0o755)
        return script

    def run_shell(self, name, *args, fail=False):
        return subprocess.run(
            [
                "bash",
                str(SOURCE / "src/system.sh"),
                "--" + name.removesuffix(".sh"),
                *map(str, args),
            ],
            text=True,
            capture_output=True,
            env={
                **os.environ,
                "PATH": str(Path(self.temp.name) / "commands") + os.pathsep + os.environ["PATH"],
                "COMMAND_LOG": str(Path(self.temp.name) / "commands.log"),
                "COMMAND_FAIL": "1" if fail else "0",
            },
            check=False,
        )

    def test_package_update_is_limited_to_selection_and_dependencies(self):
        self.shell_command("mas", 'echo "mas $*" >> "$COMMAND_LOG"\n')
        self.shell_command(
            "brew", 'echo "$*" >> "$COMMAND_LOG"\n[[ "$*" != "list --formula missing" ]]\n'
        )
        result = self.run_shell(
            "packages.sh",
            "update",
            "selected.Brewfile",
            "brew",
            "git",
            "cask",
            "visual-studio-code",
            "brew",
            "missing",
            "mas",
            "409183694",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        commands = (Path(self.temp.name) / "commands.log").read_text().splitlines()
        self.assertEqual(
            commands,
            [
                "update",
                "list --formula git",
                "upgrade --formula git",
                "list --cask visual-studio-code",
                "upgrade --cask visual-studio-code",
                "list --formula missing",
                "bundle install --no-upgrade --file=selected.Brewfile",
                "mas upgrade 409183694",
            ],
        )

    def test_touch_id_preserves_enabled_entry_and_rejects_invalid_template(self):
        self.shell_command(
            "sudo", 'echo "$*" >> "$COMMAND_LOG"\n/usr/bin/install -m 0444 "${@: -2}"\n'
        )
        config = Path(self.temp.name) / "sudo_local"
        template = Path(self.temp.name) / "template"
        template.write_text("# PAM\n#auth sufficient pam_tid.so\naccount required pam_permit.so\n")
        result = self.run_shell("touch-id.sh", config, template)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            config.read_text(),
            "# PAM\nauth sufficient pam_tid.so\naccount required pam_permit.so\n",
        )
        self.assertEqual(config.stat().st_mode & 0o777, 0o444)
        log = Path(self.temp.name) / "commands.log"
        before = log.read_text()
        result = self.run_shell("touch-id.sh", config, template)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(log.read_text(), before)
        config.unlink()
        template.write_text("# no supported entry\n")
        result = self.run_shell("touch-id.sh", config, template)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(config.exists())
        self.assertEqual(log.read_text(), before)

    def test_fork_failure_never_changes_local_remotes(self):
        origin = "git@github.com:source/dotfiles.git"
        self.git("remote", "add", "origin", origin)
        result = self.run_fork(fail=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("remote").strip(), "origin")
        self.assertEqual(self.git("remote", "get-url", "origin").strip(), origin)

    def test_fork_leaves_existing_upstream_untouched_and_declines_eof(self):
        origin = "https://github.com/source/dotfiles.git"
        self.git("remote", "add", "origin", origin)
        self.git("remote", "add", "upstream", "https://github.com/other/dotfiles.git")
        result = self.run_fork()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.git("remote", "get-url", "upstream").strip(),
            "https://github.com/other/dotfiles.git",
        )
        before = self.git("remote", "-v")
        result = self.run_fork("")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("remote", "-v"), before)

    def test_existing_configuration_is_backed_up(self):
        home = Path(self.temp.name) / "home"
        home.mkdir()
        destination = home / ".zshrc"
        destination.write_text("personal settings")
        with patch.object(configuration.Path, "home", return_value=home):
            configuration.link(self.root / "home/.zshrc", destination)
        self.assertTrue(destination.is_symlink())
        (backup,) = home.glob("dotfiles-backup-*/.zshrc")
        self.assertEqual(backup.read_text(), "personal settings")

    def test_sync_agent_invokes_installer_directly_and_does_not_reload_unchanged(self):
        home = Path(self.temp.name) / "home"
        state = home / "state"
        state.mkdir(parents=True)
        adapter = SimpleNamespace(WATCH_PATHS=[self.root / "vscode"])
        with (
            patch.object(configuration.Path, "home", return_value=home),
            patch.object(apps, "STATE", state),
            patch.dict(apps.APPLICATIONS, {"vscode": lambda: adapter}),
            patch.object(apps.subprocess, "run") as run,
        ):
            run.return_value.returncode = 0
            apps.install_agent(self.root, ("vscode",))
            agent = home / "Library/LaunchAgents/com.dotfiles.sync.plist"
            data = plistlib.loads(agent.read_bytes())
            self.assertEqual(
                data["ProgramArguments"], [sys.executable, "-m", "src.install", "sync"]
            )
            self.assertEqual(data["WorkingDirectory"], str(self.root))
            self.assertIn(str(self.root / "install.yaml"), data["WatchPaths"])
            self.assertIn(str(self.root / "src/apps/vscode.py"), data["WatchPaths"])
            self.assertFalse(any("sync.py" in p for p in data["ProgramArguments"]))
            apps.install_agent(self.root, ("vscode",))
            self.assertEqual(run.call_count, 3)
            run.assert_called_with(
                ["launchctl", "print", f"gui/{os.getuid()}/com.dotfiles.sync"],
                capture_output=True,
                check=False,
            )
            run.side_effect = [
                SimpleNamespace(returncode=1),
                SimpleNamespace(returncode=0),
                subprocess.CalledProcessError(5, "launchctl"),
            ]
            with self.assertRaises(subprocess.CalledProcessError):
                apps.install_agent(self.root, ("vscode",))
            run.side_effect = [SimpleNamespace(returncode=1), run.return_value, run.return_value]
            apps.install_agent(self.root, ("vscode",))
            run.assert_called_with(
                ["launchctl", "bootstrap", f"gui/{os.getuid()}", str(agent)], check=True
            )

    def test_moved_vscode_adapter_still_reads_repository_data(self):
        user = Path(self.temp.name) / "code-user"
        with patch.object(vscode, "PRIVATE", Path(self.temp.name) / "absent-private.jsonc"):
            vscode.sync_settings(user)
        expected = vscode.read_jsonc(SOURCE / "vscode/settings.jsonc")
        expected.update(vscode.read_jsonc(SOURCE / "vscode/extras.jsonc"))
        actual = json.loads((user / "settings.json").read_text())
        self.assertTrue(
            all(
                actual.get(k) == v
                for k, v in expected.items()
                if k != "settingsSync.ignoredSettings"
            )
        )
        self.assertEqual(
            (user / "keybindings.json").read_text(),
            (SOURCE / "vscode/keybindings.json")
            .read_text()
            .replace("${vscodeDir}", (SOURCE / "vscode").as_uri()),
        )

    def test_moved_iterm_adapter_preserves_profile_identity_and_local_keys(self):
        original = {
            "New Bookmarks": [
                {
                    "Guid": "local-guid",
                    "Name": "Personal",
                    "Keyboard Map": {"personal": {"Action": 1}},
                }
            ],
            "Default Bookmark Guid": "local-guid",
        }
        with patch.object(iterm, "load_theme", return_value={}):
            result, profiles = iterm.build_preferences(original)
        self.assertEqual(result["New Bookmarks"][0]["Guid"], "local-guid")
        self.assertEqual(result["New Bookmarks"][0]["Keyboard Map"]["personal"], {"Action": 1})
        self.assertEqual(profiles["Profiles"][0]["Dynamic Profile Parent GUID"], "local-guid")
        self.assertEqual(original["New Bookmarks"][0]["Keyboard Map"], {"personal": {"Action": 1}})

    def test_shared_preference_writer_keeps_private_permissions_and_content(self):
        path = Path(self.temp.name) / "preferences/settings.json"
        preferences.write_if_changed(path, "settings\n")
        self.assertEqual(path.read_text(), "settings\n")
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        preferences.write_if_changed(path, "updated\n")
        self.assertEqual(path.read_text(), "updated\n")

    def test_unsupported_platform_stops_before_any_operation(self):
        with (
            patch("src.install.sys.platform", "linux"),
            patch("src.install.run_shell") as cleanup,
            self.assertRaises(SystemExit),
        ):
            main(["cleanup"], self.root)
        cleanup.assert_not_called()

    def test_saved_apply_and_sync_reuse_choices_without_installing(self):
        state = self.root / ".install/choices.local.json"
        state.parent.mkdir()
        state.write_text(json.dumps(self.choices))
        with (
            patch("src.install.sys.platform", "darwin"),
            patch("builtins.input") as ask,
            patch("src.install.run_shell") as install,
            patch.object(configuration, "apply") as apply,
        ):
            main(["apply"], self.root)
            apply.assert_called_once()
            install.assert_not_called()
            ask.assert_not_called()
        with (
            patch("src.install.sys.platform", "darwin"),
            patch.object(apps, "sync_apps") as sync,
        ):
            main(["sync"], self.root)
            sync.assert_called_once_with(self.root, (), register_agent=False)

    def test_saved_update_only_updates_selected_packages_and_configuration(self):
        self.choices["setup-vscode"] = "i"
        state = self.root / ".install/choices.local.json"
        state.parent.mkdir()
        state.write_text(json.dumps(self.choices))
        with (
            patch("src.install.sys.platform", "darwin"),
            patch.dict("os.environ", {"DOTFILES_AFTER_PULL": "1"}),
            patch("builtins.input") as ask,
            patch("src.install.run_shell") as install,
            patch.object(apps, "sync_apps"),
        ):
            main(["update"], self.root)
        install.assert_called_once()
        self.assertEqual(install.call_args.args[0:2], ("packages", "update"))
        self.assertEqual(install.call_args.args[3:], ("cask", "visual-studio-code", "brew", "duti"))

        ask.assert_not_called()

    def test_update_refresh_preserves_safe_pull_and_reexecutes_updated_installer(self):
        self.shell_command("git", 'echo "$*" >> "$COMMAND_LOG"\n[[ "$COMMAND_FAIL" != 1 ]]\n')
        entrypoint = self.root / "install"
        entrypoint.write_text('#!/bin/bash\necho "$DOTFILES_AFTER_PULL $*" >> "$COMMAND_LOG"\n')
        result = self.run_shell("update.sh", self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        log = Path(self.temp.name) / "commands.log"
        self.assertEqual(
            log.read_text().splitlines(),
            ["-c merge.autoStash=false pull --ff-only --no-rebase", "1 update"],
        )
        log.unlink()
        result = self.run_shell("update.sh", self.root, fail=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(log.read_text().splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
