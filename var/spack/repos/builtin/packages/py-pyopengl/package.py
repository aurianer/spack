# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyPyopengl(PythonPackage):
    """PyOpenGL is the most common cross platform Python binding to OpenGL and related APIs."""

    homepage = "http://pyopengl.sourceforge.net"
    pypi = "pyopengl/PyOpenGL-3.1.6.tar.gz"

    version("3.1.6", sha256="8ea6c8773927eda7405bffc6f5bb93be81569a7b05c8cac50cd94e969dce5e27")

    variant("glu", default=True, description="Enable OpenGL Utility (GLU) binding.")
    variant("glut", default=True, description="Enable OpenGL Utility Toolkit (GLUT) binding.")

    conflicts("osmesa", when="^glx")

    depends_on("py-setuptools", type="build")
    # actually installing PyOpenGL itself just requires python
    # but tests (and possibly dependent packages) need OpenGL libraries
    depends_on("gl", type="link")
    depends_on("glu", when="+glu", type="link")
    depends_on("freeglut+shared", when="+glut", type="link")

    def setup_run_environment(self, env):
        # PyOpenGL uses ctypes.cdll (or similar), which searches LD_LIBRARY_PATH
        lib_dirs = self.spec["gl"].libs.directories
        if self.spec.satisfies("^glx"):
            lib_dirs.extend(self.spec["glx"].libs.directories)
            env.set("PYOPENGL_PLATFORM", "glx")
        if self.spec.satisfies("^osmesa"):
            lib_dirs.extend(self.spec["osmesa"].libs.directories)
            env.set("PYOPENGL_PLATFORM", "osmesa")
        if self.spec.satisfies("+glu"):
            lib_dirs.extend(self.spec["glu"].libs.directories)
        if self.spec.satisfies("+glut"):
            lib_dirs.extend(self.spec["freeglut"].libs.directories)
        libs = ":".join(lib_dirs)
        if sys.platform == "darwin":
            env.prepend_path("DYLD_FALLBACK_LIBRARY_PATH", libs)
        else:
            env.prepend_path("LD_LIBRARY_PATH", libs)

    def setup_dependent_build_environment_(self, env, dependent_spec):
        self.setup_run_environment(env)

    # only test import available module
    @property
    def import_modules(self):
        modules = ["OpenGL", "OpenGL.GL"]
        if self.spec.satisfies("gl=glx"):
            modules.append("OpenGL.GLX")
        if self.spec.satisfies("gl=osmesa"):
            modules.append("OpenGL.osmesa")
        if self.spec.satisfies("+glu"):
            modules.append("OpenGL.GLU")
        if self.spec.satisfies("+glut"):
            modules.append("OpenGL.GLUT")
        if self.spec.satisfies("^python+tkinter"):
            modules.append("OpenGL.Tk")

        return modules
