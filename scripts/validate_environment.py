#!/usr/bin/env python3
"""
OmniCpp Environment Validation Script

This script validates the development environment for OmniCpp builds,
checking for required tools, compilers, and dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class ToolchainValidator:
    """Validates and installs cross-compilation toolchains."""

    def __init__(self, arch: str):
        self.arch = arch
        self.system = platform.system().lower()
        self.is_linux = self.system == "linux"
        self.required_tools = self._get_required_tools()

    def _get_required_tools(self) -> List[str]:
        """Get required tools for the target architecture."""
        toolchains = {
            "arm64-linux-gnu": ["aarch64-linux-gnu-gcc", "aarch64-linux-gnu-g++"],
            "x86-linux-gnu": ["x86_64-linux-gnu-gcc", "x86_64-linux-gnu-g++"]
        }
        return toolchains.get(self.arch, [])

    def install_missing_tools(self) -> bool:
        """Attempt to install missing tools automatically."""
        if self.is_linux:
            return self._install_linux_tools()
        return False

    def _install_linux_tools(self) -> bool:
        """Install Linux cross-compilation tools."""
        if not self.required_tools:
            return True

        # Try different package managers
        for pm in ["apt", "dnf", "pacman"]:
            if self._has_package_manager(pm):
                return self._install_with_pm(pm, self.required_tools)
        return False

    def _has_package_manager(self, pm: str) -> bool:
        """Check if package manager is available."""
        try:
            subprocess.run([pm, "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _install_with_pm(self, pm: str, tools: List[str]) -> bool:
        """Install tools using the specified package manager."""
        package_map = {
            "apt": {
                "aarch64-linux-gnu-gcc": "gcc-aarch64-linux-gnu",
                "aarch64-linux-gnu-g++": "g++-aarch64-linux-gnu",
                "x86_64-linux-gnu-gcc": "gcc-x86-64-linux-gnu",
                "x86_64-linux-gnu-g++": "g++-x86-64-linux-gnu"
            },
            "dnf": {
                "aarch64-linux-gnu-gcc": "gcc-aarch64-linux-gnu",
                "aarch64-linux-gnu-g++": "gcc-c++-aarch64-linux-gnu",
                "x86_64-linux-gnu-gcc": "gcc-x86_64-linux-gnu",
                "x86_64-linux-gnu-g++": "gcc-c++-x86_64-linux-gnu"
            },
            "pacman": {
                "aarch64-linux-gnu-gcc": "aarch64-linux-gnu-gcc",
                "aarch64-linux-gnu-g++": "aarch64-linux-gnu-gcc",  # pacman often bundles
                "x86_64-linux-gnu-gcc": "x86_64-linux-gnu-gcc",
                "x86_64-linux-gnu-g++": "x86_64-linux-gnu-gcc"
            }
        }

        packages = []
        for tool in tools:
            pkg = package_map.get(pm, {}).get(tool)
            if pkg:
                packages.append(pkg)

        if not packages:
            return False

        try:
            cmd = [pm, "-y", "install"] + packages if pm == "dnf" else [pm, "install", "-y"] + packages if pm == "apt" else [pm, "-S", "--noconfirm"] + packages
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def _get_installation_commands(self, arch: str, missing_tools: List[str]) -> str:
        """Get installation commands for missing tools."""
        if not self.is_linux:
            return ""

        commands = []
        for pm in ["apt", "dnf", "pacman"]:
            if self._has_package_manager(pm):
                package_map = {
                    "apt": {
                        "aarch64-linux-gnu-gcc": "gcc-aarch64-linux-gnu",
                        "aarch64-linux-gnu-g++": "g++-aarch64-linux-gnu",
                        "x86_64-linux-gnu-gcc": "gcc-x86-64-linux-gnu",
                        "x86_64-linux-gnu-g++": "g++-x86-64-linux-gnu"
                    },
                    "dnf": {
                        "aarch64-linux-gnu-gcc": "gcc-aarch64-linux-gnu",
                        "aarch64-linux-gnu-g++": "gcc-c++-aarch64-linux-gnu",
                        "x86_64-linux-gnu-gcc": "gcc-x86_64-linux-gnu",
                        "x86_64-linux-gnu-g++": "gcc-c++-x86_64-linux-gnu"
                    },
                    "pacman": {
                        "aarch64-linux-gnu-gcc": "aarch64-linux-gnu-gcc",
                        "aarch64-linux-gnu-g++": "aarch64-linux-gnu-gcc",
                        "x86_64-linux-gnu-gcc": "x86_64-linux-gnu-gcc",
                        "x86_64-linux-gnu-g++": "x86_64-linux-gnu-gcc"
                    }
                }
                packages = [pkg for tool in missing_tools if (pkg := package_map[pm].get(tool))]
                if packages:
                    cmd = f"{pm} install {' '.join(packages)}"
                    commands.append(cmd)

        return " | ".join(commands) if commands else ""


class EnvironmentValidator:
    """Validates the OmniCpp development environment."""

    def __init__(self):
        self.system = platform.system().lower()
        self.is_windows = self.system == "windows"
        self.is_linux = self.system == "linux"
        self.is_macos = self.system == "darwin"

        self.results = {
            "passed": [],
            "failed": [],
            "warnings": []
        }

    def run_command(self, cmd: str, shell: bool = False) -> Tuple[bool, str]:
        """Run a command and return success status and output."""
        try:
            result = subprocess.run(
                cmd if shell else cmd.split(),
                shell=shell,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False, ""

    def check_command(self, command: str, description: str) -> bool:
        """Check if a command is available."""
        success, _ = self.run_command(f"which {command}" if not self.is_windows else f"where {command}")
        if success:
            self.results["passed"].append(f"✅ {description}: {command}")
            return True
        else:
            self.results["failed"].append(f"❌ {description}: {command} not found")
            return False

    def check_version(self, command: str, description: str, min_version: Optional[str] = None) -> bool:
        """Check command version."""
        success, output = self.run_command(f"{command} --version")
        if success:
            version = output.split()[0] if output else "unknown"
            if min_version and version < min_version:
                self.results["warnings"].append(f"⚠️  {description}: {command} version {version} < {min_version}")
                return False
            else:
                self.results["passed"].append(f"✅ {description}: {command} {version}")
                return True
        else:
            self.results["failed"].append(f"❌ {description}: {command} not found")
            return False

    def check_file(self, path: str, description: str) -> bool:
        """Check if a file exists."""
        if os.path.exists(path):
            self.results["passed"].append(f"✅ {description}: {path}")
            return True
        else:
            self.results["failed"].append(f"❌ {description}: {path} not found")
            return False

    def check_directory(self, path: str, description: str) -> bool:
        """Check if a directory exists."""
        if os.path.isdir(path):
            self.results["passed"].append(f"✅ {description}: {path}")
            return True
        else:
            self.results["failed"].append(f"❌ {description}: {path} not found")
            return False

    def validate_essential_tools(self) -> None:
        """Validate essential development tools."""
        print("🔧 Checking Essential Tools...")

        # Git
        self.check_version("git", "Git version control", "2.25")

        # CMake
        self.check_version("cmake", "CMake build system", "3.31")

        # Python
        self.check_version("python", "Python runtime", "3.8")

        # Ninja
        self.check_command("ninja", "Ninja build tool")

    def validate_compilers(self) -> None:
        """Validate compiler installations."""
        print("🔨 Checking Compilers...")

        compilers = []

        if self.is_windows:
            compilers.extend([
                ("cl", "MSVC compiler"),
                ("clang-cl", "Clang-MSVC compiler"),
                ("gcc", "MinGW GCC compiler")
            ])
        else:
            compilers.extend([
                ("gcc", "GCC compiler"),
                ("g++", "G++ compiler"),
                ("clang", "Clang compiler"),
                ("clang++", "Clang++ compiler")
            ])

        for cmd, desc in compilers:
            self.check_command(cmd, desc)

    def validate_package_managers(self) -> None:
        """Validate package managers."""
        print("📦 Checking Package Managers...")

        # Conan
        self.check_version("conan", "Conan package manager", "2.0")

        # vcpkg (check if directory exists)
        vcpkg_paths = [
            "/usr/local/vcpkg",
            "~/vcpkg",
            "C:\\vcpkg",
            "C:\\Program Files\\vcpkg"
        ]

        vcpkg_found = False
        for path in vcpkg_paths:
            expanded_path = os.path.expanduser(path)
            if self.check_directory(expanded_path, "vcpkg installation"):
                vcpkg_found = True
                break

        if not vcpkg_found:
            self.results["warnings"].append("⚠️  vcpkg not found in common locations")

    def validate_qt_vulkan(self) -> None:
        """Validate Qt and Vulkan development setup."""
        print("🎨 Checking Qt/Vulkan Development...")

        # Vulkan SDK
        vulkan_paths = [
            "C:\\VulkanSDK",
            "/usr/local/VulkanSDK",
            "~/VulkanSDK"
        ]

        vulkan_found = False
        for path in vulkan_paths:
            expanded_path = os.path.expanduser(path)
            if self.check_directory(expanded_path, "Vulkan SDK"):
                vulkan_found = True
                break

        if not vulkan_found:
            self.results["warnings"].append("⚠️  Vulkan SDK not found - required for Qt/Vulkan builds")

    def validate_cross_compilation(self) -> None:
        """Validate cross-compilation toolchains."""
        print("🔄 Checking Cross-Compilation Toolchains...")

        toolchains = {
            "arm64-linux-gnu": ["aarch64-linux-gnu-gcc", "aarch64-linux-gnu-g++"],
            "x86-linux-gnu": ["x86_64-linux-gnu-gcc", "x86_64-linux-gnu-g++"],
            "emscripten": ["emcc", "em++"]
        }

        for arch, tools in toolchains.items():
            toolchain_ok = True
            missing_tools = []
            for tool in tools:
                if not self.check_command(tool, f"{arch} toolchain"):
                    toolchain_ok = False
                    missing_tools.append(tool)

            if not toolchain_ok:
                # Try to install missing tools
                if arch in ["arm64-linux-gnu", "x86-linux-gnu"] and self.is_linux:
                    validator = ToolchainValidator(arch)
                    if validator.install_missing_tools():
                        # Re-check after installation
                        toolchain_ok = True
                        missing_tools = []
                        for tool in tools:
                            if not self.check_command(tool, f"{arch} toolchain"):
                                missing_tools.append(tool)
                        if missing_tools:
                            toolchain_ok = False

                if not toolchain_ok:
                    # Provide installation commands in error messages
                    install_cmds = self._get_installation_commands(arch, missing_tools)
                    error_msg = f"⚠️  {arch} toolchain incomplete - missing: {', '.join(missing_tools)}"
                    if install_cmds:
                        error_msg += f". Install with: {install_cmds}"
                    self.results["warnings"].append(error_msg)

    def validate_development_tools(self) -> None:
        """Validate additional development tools."""
        print("🛠️  Checking Development Tools...")

        tools = [
            ("clang-format", "Code formatter"),
            ("clang-tidy", "Static analyzer"),
            ("doxygen", "Documentation generator"),
            ("ccache", "Compilation cache")
        ]

        for cmd, desc in tools:
            self.check_command(cmd, desc)

    def print_summary(self) -> None:
        """Print validation summary."""
        print("\n" + "="*60)
        print("ENVIRONMENT VALIDATION SUMMARY")
        print("="*60)

        if self.results["passed"]:
            print(f"\n✅ PASSED ({len(self.results['passed'])}):")
            for item in self.results["passed"]:
                print(f"  {item}")

        if self.results["warnings"]:
            print(f"\n⚠️  WARNINGS ({len(self.results['warnings'])}):")
            for item in self.results["warnings"]:
                print(f"  {item}")

        if self.results["failed"]:
            print(f"\n❌ FAILED ({len(self.results['failed'])}):")
            for item in self.results["failed"]:
                print(f"  {item}")

        print(f"\nTotal checks: {len(self.results['passed']) + len(self.results['failed']) + len(self.results['warnings'])}")
        print(f"Passed: {len(self.results['passed'])}, Warnings: {len(self.results['warnings'])}, Failed: {len(self.results['failed'])}")

        if self.results["failed"]:
            print("\n❌ Some essential tools are missing. Please install them before building.")
            print("See docs/troubleshooting.md for installation instructions.")
            return False
        elif self.results["warnings"]:
            print("\n⚠️  Environment is functional but some optional tools are missing.")
            print("Qt/Vulkan builds may require additional setup.")
            return True
        else:
            print("\n✅ Environment validation passed! Ready for OmniCpp development.")
            return True

def main():
    """Main validation function."""
    print("🚀 OmniCpp Environment Validator")
    print("="*40)

    validator = EnvironmentValidator()

    # Run all validation checks
    validator.validate_essential_tools()
    validator.validate_compilers()
    validator.validate_package_managers()
    validator.validate_qt_vulkan()
    validator.validate_cross_compilation()
    validator.validate_development_tools()

    # Print summary and return exit code
    success = validator.print_summary()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()</content>
</xai:function_call">The file scripts/validate_environment.py has been created successfully.