from hatchling.builders.hooks.plugin.interface import BuildHookInterface

import os
import sys
import shutil
import subprocess

from typing import Any

suffix = "dll" if sys.platform == "win32" else "so"

class SpecialBuildHook(BuildHookInterface):
    def initialize(self, version: str, build_data: dict[str, Any]):
        cmake = shutil.which("cmake")
        if cmake is None:
            raise RuntimeError("CMake has not been found")

        build_dir = f"{self.root}/gl_preview/build"

        subprocess.check_call([
            cmake,
            "-DCMAKE_BUILD_TYPE=Release",
            "-S",
            f"{self.root}/gl_preview",
            "-B",
            build_dir
        ])

        subprocess.check_call([
            cmake,
            "--build",
            build_dir
        ])

        shutil.copy(f"{build_dir}/libgl_preview.{suffix}", f"{self.root}/tacoeditor/resources")

        gircompiler = shutil.which("g-ir-compiler")
        if gircompiler is None:
            raise RuntimeError("g-ir-compiler has not been found")

        subprocess.check_call([
            gircompiler,
            f"--output={self.root}/tacoeditor/resources/TacoEditor-1.0.typelib",
            f"--shared-library=./resources/libgl_preview.{suffix}",
            f"{build_dir}/TacoEditor-1.0.gir"
        ])

    def clean(self, versions: list[str]):
        shutil.rmtree(f"{self.root}/gl_preview/build")
        os.remove(f"{self.root}/tacoeditor/resources/TacoEditor-1.0.typelib")
        os.remove(f"{self.root}/tacoeditor/resources/libtaco_gl_preview.{suffix}")
