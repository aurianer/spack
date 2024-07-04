# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStanfordStk(Package):
    """A light-weight PyTorch library for block-sparse matrices and block-sparse matrix multiplication."""

    homepage = "https://github.com/stanford-futuredata/stk/tree/main"
    pypi = "stanford-stk/stanford-stk-0.0.0.tar.gz"

    version("0.7.0", sha256="756e3173619b60f9ddce3cc5580b3fa1e2717921ab3d431f197bd072f63f8133")

    maintainers("aurianer")

    license("Apache-2.0")

    with default_args(type="build"):
        depends_on("py-setuptools")
        depends_on("py-setuptools-rust")

    with default_args(type="build"):
        depends_on("py-triton@2.1.0:")
