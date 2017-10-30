[ -n "$PYENV_DEBUG" ] && set -x
export PYENV_ROOT="/Users/lizhiwei/.pyenv"
program="$("/usr/local/Cellar/pyenv/1.1.5/libexec/pyenv" which "${BASH_SOURCE##*/}")"
if [ -e "${program}" ]; then
  . "${program}" "$@"
fi
