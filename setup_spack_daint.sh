#!/bin/bash -l

set -eux
#cp -r /apps/common/UES/jenkins/production/spack/daint $SPACK_ROOT/etc/spack/cray
#cp $SRC_DIR/production/spack/daint/* $SPACK_ROOT/etc/spack/cray

# soft link from eth-cscs/production repo config files
pushd $SPACK_ROOT_AURIANER/etc/spack/cray
    ln -s $PRODUCTION_ROOT/spack/daint/* .
popd
