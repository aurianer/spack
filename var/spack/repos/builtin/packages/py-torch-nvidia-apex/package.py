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

    license("BSD-3-Clause")

    version("master", branch="master")
    version("2020-10-19", commit="8a1ed9e8d35dfad26fb973996319965e4224dcdd")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-packaging", type="build")
    depends_on("py-torch@0.4:", type=("build", "run"))
    depends_on("cuda@9:", when="+cuda")
    depends_on("py-pybind11", type=("build", "link", "run"))

    variant("cuda", default=True, description="Build with CUDA")

    variant("bnp", default=True)
    variant("cudnn_gbn_lib", default=True)
    variant("fast_layer_norm", default=True)
    variant("fast_multihead_attn", default=True)
    variant("fmhalib", default=True)
    variant("focal_loss_cuda", default=True)
    variant("fused_conv_bias_relu", default=True)
    variant("fused_index_mul_2d", default=True)
    variant("index_mul_2d", default=True)
    variant("permutation_search_cuda", default=True)
    variant("peer_memory", default=True)
    variant("permutation_search_cuda", default=True)
    variant("nccl_p2p", default=True)
    variant("transducer", default=True)
    variant("xentropy", default=True)

    requires("nccl@2.10:", when="+nccl_p2p")
    requires("cudnn@8.5:", when="+cudnn_gbn_lib")
    requires("cudnn@8.4:", when="+fused_conv_bias_relu")
    depends_on("cuda@11", when="+cuda")

    # https://github.com/NVIDIA/apex/issues/1498
    # https://github.com/NVIDIA/apex/pull/1499
    patch("1499.patch", when="@2020-10-19")

    def setup_build_environment(self, env):
        if "+cuda" in self.spec:
            env.set("CUDA_HOME", self.spec["cuda"].prefix)
        else:
            env.unset("CUDA_HOME")

    @when("^python@:3.10")
    def global_options(self, spec, prefix):
        args = []
        if spec.satisfies("^py-torch@1.0:"):
            args.append("--cpp_ext")
            if spec.satisfies("+cuda"):
                args.append("--cuda_ext")

            if spec.satisfies("+bnp"):
                args.append("--bnp")
            if spec.satisfies("+cudnn_gbn_lib"):
                args.append("--cudnn_gbn")
            if spec.satisfies("+fast_layer_norm"):
                args.append("--fast_layer_norm")
            if spec.satisfies("+fmhalib"):
                args.append("--fmha")
            if spec.satisfies("+fast_multihead_attn"):
                args.append("--fast_multihead_attn")
            if spec.satisfies("+permutation_search_cuda"):
                args.append("--permutation_search")
            if spec.satisfies("+focal_loss_cuda"):
                args.append("--focal_loss")
            if spec.satisfies("+xentropy"):
                args.append("--xentropy")
            if spec.satisfies("+fused_index_mul_2d"):
                args.append("--index_mul_2d")
            if spec.satisfies("+transducer"):
                args.append("--transducer")
            if spec.satisfies("+peer_memory"):
                args.append("--peer_memory")
            if spec.satisfies("+fused_conv_bias_relu"):
                args.append("--fused_conv_bias_relu")
        return args

    @when("^python@3.11:")
    def config_settings(self, spec, prefix):
        return {
            "builddir": "build",
            "compile-args": f"-j{make_jobs}",
            "--global-option": "--cpp_ext --cuda_ext",
        }
