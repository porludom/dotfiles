# Expand aliases in the command following sudo.
alias sudo='sudo '

# Command replacements
if _exists trash; then
  alias rm='trash'
fi

if _exists tldr; then
  alias help='tldr'
fi

if _exists eza; then
  alias ls='eza -a --icons=auto'
  alias ll='eza -lah'
  alias tree='eza -T'
fi

if _exists bat; then
  export BAT_THEME='ansi'
  alias cat='bat -p'
fi

alias open='open_command'

# Shell shortcuts
alias c='clear'
alias q="cd ~ && clear"
alias e="$EDITOR"
alias -g G="| rg"
alias -- +x='chmod +x'
alias x+='chmod +x'
alias reload="source $HOME/.zshrc"
alias path='echo -e ${PATH//:/\\n}'

# Open files and terminals
alias o='open'
alias oo='open .'
alias term='open -a iterm.app'

# Navigation
[ -d ~/Downloads ] && alias dl='cd ~/Downloads'
[ -d ~/Desktop ] && alias dt='cd ~/Desktop'
[ -d ~/dev ] && alias dev='cd ~/dev'
function mkcd {
  command mkdir -p $1 && cd $1
}

# Files and networking
alias sizes='du -sh * | sort -h'
alias get="curl -O -L"
alias myip='ifconfig | sed -En "s/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p"'
alias ports='lsof -i -P -n | grep LISTEN'
function killport() { lsof -tiTCP:"${1:?Usage: killport <port>}" -sTCP:LISTEN | xargs kill -9 ; }

# Git
function gud {
  branch=$(git branch --show-current)
  main_branch=$(git remote show origin | grep 'HEAD branch' | awk '{print $NF}')

  git switch $main_branch
  git pull --rebase
  git fetch --all --tags --prune --jobs=10
  git branch --delete --force $branch
}
