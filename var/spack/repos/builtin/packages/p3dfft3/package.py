# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class P3dfft3(AutotoolsPackage):
    """P3DFFT++ (a.k.a. P3DFFT v. 3) is a new generation of P3DFFT library
    that aims to provide a comprehensive framework for simulating multiscale
    phenomena. It takes the essence of P3DFFT further by creating an
    extensible, modular structure uniquely adaptable to a greater range
    of use cases."""

    homepage = "https://www.p3dfft.net"
    url = "https://github.com/sdsc/p3dfft.3/archive/v3.0.0.tar.gz"
    git = "https://github.com/sdsc/p3dfft.3.git"

    version("develop", branch="master")
    version("3.0.0", sha256="1c549e78097d1545d18552b039be0d11cdb96be46efe99a16b65fd5d546dbfa7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("fftw", default=True, description="Builds with FFTW library")
    variant("essl", default=False, description="Builds with ESSL library")
    variant("mpi", default=True, description="Enable MPI support.")
    variant(
        "measure",
        default=False,
        description="Define if you want to use" "the measure fftw planner flag",
    )
    variant(
        "estimate",
        default=False,
        description="Define if you want to" "use the estimate fftw planner flag",
    )
    variant(
        "patient",
        default=False,
        description="Define if you want to" "use the patient fftw planner flag",
    )

    # TODO: Add more configure options!

    depends_on("mpi", when="+mpi")
    depends_on("fftw", when="+fftw")
    depends_on("essl", when="+essl")

    def configure_args(self):
        args = []

        if self.spec.satisfies("%gcc"):
            args.append("--enable-gnu")

        if self.spec.satisfies("%intel"):
            args.append("--enable-intel")

        if self.spec.satisfies("%xl"):
            args.append("--enable-ibm")

        if self.spec.satisfies("%cce"):
            args.append("--enable-cray")

        if self.spec.satisfies("%pgi"):
            args.append("--enable-pgi")

        if self.spec.satisfies("+mpi"):
            args.append("CC=%s" % self.spec["mpi"].mpicc)
            args.append("CXX=%s" % self.spec["mpi"].mpicxx)
            args.append("FC=%s" % self.spec["mpi"].mpifc)

        if self.spec.satisfies("+openmpi"):
            args.append("--enable-openmpi")

        if self.spec.satisfies("+fftw"):
            args.append("--enable-fftw")

            if self.spec.satisfies("@:3.0.0"):
                args.append("--with-fftw-lib=%s" % self.spec["fftw"].prefix.lib)
                args.append("--with-fftw-inc=%s" % self.spec["fftw"].prefix.include)
            else:
                args.append("--with-fftw=%s" % self.spec["fftw"].prefix)

            if self.spec.satisfies("fftw+measure"):
                args.append("--enable-fftwmeasure")
            if self.spec.satisfies("fftw+estimate"):
                args.append("--enable-fftwestimate")
            if self.spec.satisfies("fftw+patient"):
                args.append("--enable-fftwpatient")

        if self.spec.satisfies("+essl"):
            args.append("--enable-essl")
            args.append("--with-essl-lib=%s" % self.spec["essl"].prefix.lib)
            args.append("--with-essl-inc=%s" % self.spec["essl"].prefix.include)

        if self.spec.satisfies("+mkl"):
            args.append("--enable-mkl")
            args.append("--with-mkl-lib=%s" % self.spec["mkl"].prefix.lib)
            args.append("--with-mkl-inc=%s" % self.spec["mkl"].prefix.include)

        return args
