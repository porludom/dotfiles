export FZF_CTRL_T_OPTS="--walker-skip .git,node_modules,.venv"
if _exists bat && _exists eza; then
  export FZF_CTRL_T_OPTS="$FZF_CTRL_T_OPTS \
    --preview 'if [ -d {} ]; then eza -a --color=always -- {}; else bat --color=always --style=numbers --line-range=:200 -- {}; fi' \
    --preview-window right:60% --bind 'ctrl-/:toggle-preview'"
fi

export FZF_CTRL_R_OPTS="--with-nth=2.. --no-sort --bind 'alt-w:toggle-wrap'"
if _exists pbcopy; then
  export FZF_CTRL_R_OPTS="$FZF_CTRL_R_OPTS \
    --bind 'ctrl-y:execute-silent(printf %s {2..} | pbcopy)+abort'"
fi
