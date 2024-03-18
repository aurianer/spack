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
    variant("dist_adam", default=True, description="Build with distributed Adam optimizer")
    variant("dist_lamb", default=True, description="Build with distributed Lamb optimizer")
    variant("perm_search", default=True, description="Build with permutation search")
    variant("bnp", default=True, description="Build with batch norm")
    variant("xentropy", default=True, description="Build with cross entropy")
    variant("focal_loss", default=True, description="Build with focal loss")
    variant("group_norm", default=True, description="Build with group norm")
    variant("index_mul_2d", default=True, description="Build with index_mul_2d")
    variant("fast_layer_norm", default=True, description="Build with fast layer norm")
    variant("fmha", default=True, description="Build with fmha")
    variant("fast_multihead_attn", default=True, description="Build with fast multihead attn")
    variant("transducer", default=True, description="Build with transducer")
    variant("cudnn_gbn", default=True, description="Build with fast cudnn gbn")
    variant("peer_memory", default=True, description="Build with peer memory")
    variant("nccl_p2p", default=True, description="Build with nccl p2p")
    variant("fast_bottleneck", default=True, description="Build with fast_bottleneck")
    variant("fused_conv_bias_relu", default=True, description="Build with fused_conv_bias_relu")
    variant("gpu_direct_storage", default=True, description="Build with gpu_direct_storage")

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
        if "+dist_adam" in spec:
            args.append("--distributed_adam")
        if "+dist_lamb" in spec:
            args.append("--distributed_lamb")
        if "+perm_search" in spec:
            args.append("--permutation_search")
        if "+bnp" in spec:
            args.append("--bnp")
        if "+xentropy" in spec:
            args.append("--xentropy")
        if "+focal_loss" in spec:
            args.append("--focal_loss")
        if "+group_norm" in spec:
            args.append("--group_norm")
        if "+index_mul_2d" in spec:
            args.append("--index_mul_2d")
        if "+fast_layer_norm" in spec:
            args.append("--fast_layer_norm")
        if "+fmha" in spec:
            args.append("--fmha")
        if "+fast_multihead_attn" in spec:
            args.append("--fast_multihead_attn")
        if "+transducer" in spec:
            args.append("--transducer")
        if "+cudnn_gbn" in spec:
            args.append("--cudnn_gbn")
        if "+peer_memory" in spec:
            args.append("--peer_memory")
        if "+nccl_p2p" in spec:
            args.append("--nccl_p2p")
        if "+fast_bottleneck" in spec:
            args.append("--fast_bottleneck")
        if "+fused_conv_bias_relu" in spec:
            args.append("--fused_conv_bias_relu")
        if "+gpu_direct_storage" in spec:
            args.append("--gpu_direct_storage")
        return args

    @when("^python@3.11:")
    def config_settings(self, spec, prefix):
        return {
            "builddir": "build",
            "compile-args": f"-j{make_jobs}",
            "--global-option": "--cpp_ext --cuda_ext",
        }
