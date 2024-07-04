# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMegablocks(Package):
    """MegaBlocks is a light-weight library for mixture-of-experts (MoE) training."""

    homepage = "https://github.com/databricks/megablocks"
    pypi = "megablocks/megablocks-0.0.0.tar.gz"

    version("0.5.1", sha256="4e3346f2987761e67055a8947e9ee97f9673c672056d61c89f060546f448277c")

    maintainers("aurianer")

    license("Apache-2.0")

    with default_args(type="build"):
        depends_on("py-setuptools")
        depends_on("py-setuptools-rust")

    with default_args(type="build"):
        depends_on("py-triton@2.1.0:")
