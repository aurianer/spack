# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTorchNvidiaApex(PythonPackage, CudaPackage):
    """A PyTorch Extension: Tools for easy mixed precision and
    distributed training in Pytorch"""

    homepage = "https://github.com/nvidia/apex/"
    git = "https://github.com/nvidia/apex/"
    url = "https://github.com/NVIDIA/apex/archive/refs/tags/0.0.tar.gz"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("23.08", sha256="a6ab2d10b681b621a96c028d6727d133fdaea6dd4c30f0546f70cf6904de522e")
    version("23.07", sha256="1bdfdd04db1fcc74d34d81a3b8815f7823b1f4d5850dc174e19e7fd91c8be25a")
    version("23.06", sha256="261af099a608262543a091d1da223545c15933255fac1ec5223f19137510d9a3")
    version("23.05", sha256="c770795fe710fc9d76388952ff073808d66a8f33593f46961351ab549ec73d47")
    version("22.03", sha256="694f1ac1aaed6435b2f0c2ebc1af56b8a215a5eaa96c2565a578e8734378ff66")
    version("2020-10-19", commit="8a1ed9e8d35dfad26fb973996319965e4224dcdd")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pip", type="build")
    depends_on("py-packaging", type="build")
    depends_on("py-torch@0.4:", type=("build", "run"))
    depends_on("cuda@9:", when="+cuda")
    depends_on("py-pybind11", type=("build", "link", "run"))

    variant("cuda", default=True, description="Build with CUDA")

    # https://github.com/NVIDIA/apex/issues/1498
    # https://github.com/NVIDIA/apex/pull/1499
    patch("1499.patch", when="@2020-10-19")

    def setup_build_environment(self, env):
        if "+cuda" in self.spec:
            env.set("CUDA_HOME", self.spec["cuda"].prefix)
            if self.spec.variants["cuda_arch"].value[0] != "none":
                torch_cuda_arch = ";".join(
                    "{0:.1f}".format(float(i) / 10.0)
                    for i in self.spec.variants["cuda_arch"].value
                )
                env.set("TORCH_CUDA_ARCH_LIST", torch_cuda_arch)
        else:
            env.unset("CUDA_HOME")

    @when("^python@:3.10")
    def global_options(self, spec, prefix):
        args = []
        if spec.satisfies("^py-torch@1.0:"):
            args.append("--cpp_ext")
            if "+cuda" in spec:
                args.append("--cuda_ext")
        return args

    @when("^python@3.11:")
    def config_settings(self, spec, prefix):
        return {
            "builddir": "build",
            "compile-args": f"-j{make_jobs}",
            "--global-option": "--cpp_ext --cuda_ext",
        }
