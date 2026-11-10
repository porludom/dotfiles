"""Protect saved layouts until native restoration is explicitly acknowledged."""

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.apps.vscode import VSCode


class VSCodeSyncTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.shared = self.root / "shared"
        self.shared.mkdir()
        for name in ("settings.jsonc", "extras.jsonc"):
            (self.shared / name).write_text("{}\n")
        (self.shared / "keybindings.json").write_text("[]\n")
        (self.shared / "extensions.txt").write_text("# No fixture extensions.\n")
        self.profile = self.shared / "ui-state.code-profile"
        self.profile.write_text(
            json.dumps(
                {
                    "name": "Dotfiles UI",
                    "globalState": json.dumps({"storage": {"workbench.panel.alignment": "right"}}),
                }
            )
        )
        settings = {
            "shared": str(self.shared),
            "private": str(self.root / "private.jsonc"),
            "user": str(self.root / "user"),
            "extensions": str(self.root / "extensions.json"),
            "baseline": "vscode/extensions.json",
            "backups": str(self.root / "backups"),
            "layout_keys": ["workbench.panel.alignment"],
            "cli": "unused-fixture-code",
            "extension_timeout_seconds": 1,
        }
        with (
            patch("src.apps.base.load", return_value=settings),
            patch("src.apps.vscode.STATE", self.root / "state"),
        ):
            self.adapter = VSCode()
        self.database = self.adapter.USER / "globalStorage/state.vscdb"

    def write_fixture_state(self, alignment):
        self.database.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.database) as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS ItemTable (key TEXT PRIMARY KEY, value TEXT)"
            )
            connection.executemany(
                "INSERT OR REPLACE INTO ItemTable VALUES (?, ?)",
                [
                    ("__$__targetStorageMarker", json.dumps({"workbench.panel.alignment": 0})),
                    ("workbench.panel.alignment", alignment),
                ],
            )

    def snapshot(self):
        return {
            p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()
        }

    def test_fresh_sync_keeps_saved_layout_and_all_files_untouched_on_rerun(self):
        for has_database in (False, True):
            with self.subTest(has_database=has_database):
                if has_database:
                    self.write_fixture_state("center")
                before = self.snapshot()
                for _ in range(2):
                    with self.assertRaisesRegex(RuntimeError, "--vscode-ui-restored"):
                        self.adapter.sync()
                    self.assertEqual(self.snapshot(), before)

    def test_acknowledged_restore_enables_normal_later_exports(self):
        self.write_fixture_state("right")
        self.adapter.sync(ui_restored=True)
        self.assertTrue(self.adapter.EXTENSION_BASELINE.exists())
        self.assertTrue((self.adapter.USER / "settings.json").exists())
        self.adapter.EXTENSIONS.write_text("[]")
        self.write_fixture_state("left")
        self.adapter.sync()
        exported = json.loads(self.profile.read_text())
        self.assertEqual(
            json.loads(exported["globalState"])["storage"], {"workbench.panel.alignment": "left"}
        )

    def test_existing_machine_continues_exporting_without_acknowledgement(self):
        self.adapter.EXTENSION_BASELINE.parent.mkdir(parents=True)
        self.adapter.EXTENSION_BASELINE.write_text("[]")
        self.adapter.EXTENSIONS.write_text("[]")
        self.write_fixture_state("left")
        self.adapter.sync()
        exported = json.loads(self.profile.read_text())
        self.assertEqual(
            json.loads(exported["globalState"])["storage"]["workbench.panel.alignment"], "left"
        )

    def test_acknowledgement_without_native_state_does_not_initialize_sync(self):
        before = self.snapshot()
        with self.assertRaisesRegex(RuntimeError, "Finish importing"):
            self.adapter.sync(ui_restored=True)
        self.assertEqual(self.snapshot(), before)

    def test_no_saved_layout_needs_no_restoration(self):
        self.profile.unlink()
        self.adapter.sync()
        self.assertTrue(self.adapter.EXTENSION_BASELINE.exists())
        self.assertFalse(self.profile.exists())
