from hatchling.builders.hooks.plugin.interface import BuildHookInterface

from typing import Any

import subprocess
import shutil


class SpecialBuildHook(BuildHookInterface):
    def initialize(self, version: str, build_data: dict[str, Any]):
        cmake = shutil.which("cmake")
        if cmake is None:
            raise RuntimeError("CMake has not been found")

        build_dir = f"{self.root}/native/build"

        subprocess.check_call(
            [
                cmake,
                "-DCMAKE_BUILD_TYPE=Release",
                "-S",
                f"{self.root}/native",
                "-B",
                build_dir,
            ]
        )
        subprocess.check_call([cmake, "--build", build_dir])
        subprocess.check_call(
            [
                cmake,
                "--install",
                build_dir,
                "--prefix",
                f"{self.root}/tacoeditor/resources",
            ]
        )
