# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDacite(PythonPackage):
    """This package simplifies creation of data classes from dictionaries"""

    git = "https://github.com/konradhalas/dacite"
    pypi = "dacite/dacite-1.8.1-py3-none-any.whl"

    maintainers("aurianer")

    license("MIT")

    version(
        "1.8.1",
        sha256="cc31ad6fdea1f49962ea42db9421772afe01ac5442380d9a99fcf3d188c61afe",
        url="https://files.pythonhosted.org/packages/21/0f/cf0943f4f55f0fbc7c6bd60caf1343061dff818b02af5a0d444e473bb78d/dacite-1.8.1-py3-none-any.whl",
        expand=False,
    )

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
