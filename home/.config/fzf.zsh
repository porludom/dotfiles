zstyle ':completion:*' menu no
zstyle ':completion:*:descriptions' format '[%d]'
zstyle ':completion:*:git-checkout:*' sort false
zstyle ':fzf-tab:*' switch-group '<' '>'
if _exists eza; then
  zstyle ':fzf-tab:complete:*cd*:*' fzf-preview 'eza -a --color=always -- "$realpath"'
fi

if _exists fd; then
  export FZF_CTRL_T_COMMAND="fd --type f --type d --hidden \
    --exclude .git --exclude node_modules --exclude .venv --exclude __pycache__ \
    --exclude .pytest_cache --exclude .mypy_cache --exclude .ruff_cache"
fi
export FZF_CTRL_T_OPTS="--height=70% --layout=reverse --border=rounded --info=inline \
  --border-label='Files & directories' --prompt='files> ' --highlight-line \
  --walker-skip .git,node_modules,.venv,__pycache__,.pytest_cache,.mypy_cache,.ruff_cache \
  --header='Tab: select | Ctrl-/: preview | Ctrl-Y: copy paths'"
if _exists bat && _exists eza; then
  export FZF_CTRL_T_OPTS="$FZF_CTRL_T_OPTS \
    --preview 'if [ -d {} ]; then eza -a --color=always -- {}; else bat --color=always --style=numbers --line-range=:200 -- {}; fi' \
    --preview-window 'right,60%,<100(down,45%)' --bind 'ctrl-/:toggle-preview'"
fi
if _exists pbcopy; then
  export FZF_CTRL_T_OPTS="$FZF_CTRL_T_OPTS \
    --bind \"ctrl-y:execute-silent(printf '%s\\n' {+} | pbcopy)+abort\""
fi

# History selections are inserted for editing, never executed by the picker.
export FZF_CTRL_R_OPTS="--height=70% --layout=reverse --border=rounded --info=inline \
  --border-label='Command history' --prompt='history> ' --with-nth=2.. --no-sort \
  --header='Ctrl-R: sort | Ctrl-/: preview | Alt-W: wrap | Ctrl-Y: copy' \
  --bind 'alt-w:toggle-wrap'"
if _exists bat; then
  export FZF_CTRL_R_OPTS="$FZF_CTRL_R_OPTS \
    --preview 'printf %s {2..} | bat --language=zsh --color=always --style=plain --paging=never' \
    --preview-window 'down,6,hidden,wrap' --bind 'ctrl-/:toggle-preview'"
fi
if _exists pbcopy; then
  export FZF_CTRL_R_OPTS="$FZF_CTRL_R_OPTS \
    --bind 'ctrl-y:execute-silent(printf %s {2..} | pbcopy)+abort'"
fi
