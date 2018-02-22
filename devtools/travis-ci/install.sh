# Temporarily change directory to $HOME to install software
pushd .
cd $HOME

# Install Miniconda
MINICONDA=Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh
MINICONDA_HOME=$HOME/miniconda3
MINICONDA_MD5=$(curl -s https://repo.continuum.io/miniconda/ | grep -A3 $MINICONDA | sed -n '4p' | sed -n 's/ *<td>\(.*\)<\/td> */\1/p')
wget -q https://repo.continuum.io/miniconda/$MINICONDA
# Parse version out of file as fall back
# Sed cuts out everything before the first digit, then traps the first digit and everything after
MINICONDA_DL_VER=$(head $MINICONDA | grep VER | sed -n 's/[^0-9]*\([0-9.]*\)/\1/p')
MINICONDA_FILE_VER="Miniconda3-$MINICONDA_DL_VER-Linux-x86_64.sh"
MINICONDA_MD5_VER=$(curl -s https://repo.continuum.io/miniconda/ | grep -A3 $MINICONDA_FILE_VER | sed -n '4p' | sed -n 's/ *<td>\(.*\)<\/td> */\1/p')
if [[ $MINICONDA_MD5 != $(md5sum $MINICONDA | cut -d ' ' -f 1) ]]; then
    if [[ $MINICONDA_MD5_VER != $(md5sum $MINICONDA | cut -d ' ' -f 1) ]]; then
        echo "Miniconda MD5 mismatch"
        exit 1
    fi
fi
bash $MINICONDA -b -p $MINICONDA_HOME

# Configure miniconda
export PIP_ARGS="-U"
export PATH=$MINICONDA_HOME/bin:$PATH
# Use the latest miniconda starting from MINICONDA_VERSION
conda update --yes conda

# Restore original directory
popd
