# riZZZhik's dotfiles

```sh
git clone https://github.com/riZZZhik/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
make install
```

Choose **Install**, **Delete from local**, or **Keep local** for each setup stage.
Finish Command Line Tools setup if prompted, then rerun. Apps are never uninstalled.

`install` bootstraps the installer. Source code lives in `src/`.
`install.yaml` lists setup stages in order.
Actions: `brew`, `cask`, `mas`, `link`, and named `extras` for apps and macOS settings.
`home/` always maps onto `~/` using real directories and linked files, with backups.

Delete removes repository sources, including local edits; committed versions remain in Git.
The final prompt can create a GitHub fork and switch `origin` to it.
Review local changes, then stage, commit and push them yourself.

`make apply` reapplies saved choices; `make update` updates selected components;
`make cleanup` clears package caches.
