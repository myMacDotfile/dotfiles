

set -ex



python -c "from __future__ import print_function; import conda; print(conda.__version__)"
which conda
which conda-env
conda --version
conda info
conda env --help
exit 0
