"""
CMake toolchain management

This module provides comprehensive CMake toolchain file generation and management
including cross-compilation toolchains, compiler detection, and toolchain
validation with proper error handling.
"""

from pathlib import Path
from typing import Optional

from core.exception_handler import ConfigurationError, CompilerError
from core.logger import Logger


class ToolchainManager:
    """Manage CMake toolchain files.
    
    This class provides methods for generating, reading, and manipulating
    CMake toolchain files for cross-compilation and custom compiler
    configurations with proper validation and error handling.
    """
    
    # Supported toolchain types
    TOOLCHAIN_TYPES = {
        "msvc": "MSVC",
        "msvc-clang": "MSVC-Clang",
        "mingw-gcc": "MinGW-GCC",
        "mingw-clang": "MinGW-Clang",
        "gcc": "GCC",
        "clang": "Clang",
        "emscripten": "Emscripten"
    }
    
    # Supported architectures
    ARCHITECTURES = {
        "x64": "x86_64",
        "x86": "i686",
        "arm64": "aarch64",
        "arm": "arm"
    }
    
    def __init__(
        self,
        toolchain_dir: str,
        logger: Optional[Logger] = None
    ) -> None:
        """Initialize toolchain manager.
        
        Args:
            toolchain_dir: Directory for toolchain files
            logger: Logger instance for logging operations
            
        Raises:
            ConfigurationError: If toolchain directory is invalid
        """
        self.toolchain_dir = Path(toolchain_dir).resolve()
        self.logger = logger or Logger("ToolchainManager", {
            "level": "INFO",
            "console_handler_enabled": True,
            "file_handler_enabled": False
        })
        
        # Ensure toolchain directory exists
        self.toolchain_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Toolchain manager initialized for: {self.toolchain_dir}")
    
    def generate_toolchain(
        self,
        toolchain_type: str,
        architecture: str = "x64",
        compiler_path: Optional[str] = None,
        sysroot: Optional[str] = None,
        extra_flags: Optional[list[str]] = None
    ) -> str:
        """Generate CMake toolchain file.
        
        Args:
            toolchain_type: Type of toolchain (msvc, gcc, clang, etc.)
            architecture: Target architecture (x64, x86, arm64, arm)
            compiler_path: Optional path to compiler executable
            sysroot: Optional sysroot path for cross-compilation
            extra_flags: Optional list of extra compiler flags
            
        Returns:
            Path to generated toolchain file
            
        Raises:
            ConfigurationError: If toolchain type is invalid
            CompilerError: If compiler cannot be found
        """
        # Validate toolchain type
        if toolchain_type not in self.TOOLCHAIN_TYPES:
            raise ConfigurationError(
                f"Invalid toolchain type: {toolchain_type}",
                {"valid_types": list(self.TOOLCHAIN_TYPES.keys()), "provided": toolchain_type}
            )
        
        # Validate architecture
        if architecture not in self.ARCHITECTURES:
            raise ConfigurationError(
                f"Invalid architecture: {architecture}",
                {"valid_architectures": list(self.ARCHITECTURES.keys()), "provided": architecture}
            )
        
        # Generate toolchain file name
        toolchain_name = f"{toolchain_type}-{architecture}.cmake"
        toolchain_path = self.toolchain_dir / toolchain_name
        
        self.logger.info(f"Generating toolchain file: {toolchain_path}")
        
        # Generate toolchain content based on type
        if toolchain_type == "msvc":
            content = self._generate_msvc_toolchain(architecture, compiler_path, extra_flags)
        elif toolchain_type == "msvc-clang":
            content = self._generate_msvc_clang_toolchain(architecture, compiler_path, extra_flags)
        elif toolchain_type == "mingw-gcc":
            content = self._generate_mingw_gcc_toolchain(architecture, compiler_path, sysroot, extra_flags)
        elif toolchain_type == "mingw-clang":
            content = self._generate_mingw_clang_toolchain(architecture, compiler_path, sysroot, extra_flags)
        elif toolchain_type == "gcc":
            content = self._generate_gcc_toolchain(architecture, compiler_path, sysroot, extra_flags)
        elif toolchain_type == "clang":
            content = self._generate_clang_toolchain(architecture, compiler_path, sysroot, extra_flags)
        elif toolchain_type == "emscripten":
            content = self._generate_emscripten_toolchain(architecture, compiler_path, extra_flags)
        else:
            raise ConfigurationError(f"Unsupported toolchain type: {toolchain_type}")
        
        # Write toolchain file
        try:
            with open(toolchain_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Toolchain file generated: {toolchain_path}")
            return str(toolchain_path)
        except Exception as e:
            self.logger.error(f"Failed to write toolchain file: {e}")
            raise CompilerError(
                f"Failed to write toolchain file: {e}",
                {"toolchain_path": str(toolchain_path)}
            )
    
    def _generate_msvc_toolchain(
        self,
        architecture: str,
        compiler_path: Optional[str],
        extra_flags: Optional[list[str]]
    ) -> str:
        """Generate MSVC toolchain file.
        
        Args:
            architecture: Target architecture
            compiler_path: Optional compiler path
            extra_flags: Optional extra compiler flags
            
        Returns:
            Toolchain file content
        """
        content = [
            "# CMake toolchain file for MSVC",
            "# Generated by OmniCPP ToolchainManager",
            ""
        ]
        
        # Set architecture
        if architecture == "x64":
            content.append("set(CMAKE_GENERATOR_PLATFORM x64)")
        elif architecture == "x86":
            content.append("set(CMAKE_GENERATOR_PLATFORM Win32)")
        
        # Add extra flags if provided
        if extra_flags:
            flags = " ".join(extra_flags)
            content.append(f"set(CMAKE_C_FLAGS_INIT \"{flags}\")")
            content.append(f"set(CMAKE_CXX_FLAGS_INIT \"{flags}\")")
        
        content.append("")
        return "\n".join(content)
    
    def _generate_msvc_clang_toolchain(
        self,
        architecture: str,
        compiler_path: Optional[str],
        extra_flags: Optional[list[str]]
    ) -> str:
        """Generate MSVC-Clang toolchain file.
        
        Args:
            architecture: Target architecture
            compiler_path: Optional compiler path
            extra_flags: Optional extra compiler flags
            
        Returns:
            Toolchain file content
        """
        content = [
            "# CMake toolchain file for MSVC-Clang",
            "# Generated by OmniCPP ToolchainManager",
            ""
        ]
        
        # Set compiler
        if compiler_path:
            clang_path = Path(compiler_path)
            content.append(f"set(CMAKE_C_COMPILER \"{clang_path}\")")
            content.append(f"set(CMAKE_CXX_COMPILER \"{clang_path.parent / 'clang++.exe'}\")")
        else:
            content.append("set(CMAKE_C_COMPILER clang)")
            content.append("set(CMAKE_CXX_COMPILER clang++)")
        
        # Set architecture
        if architecture == "x64":
            content.append("set(CMAKE_GENERATOR_PLATFORM x64)")
        elif architecture == "x86":
            content.append("set(CMAKE_GENERATOR_PLATFORM Win32)")
        
        # Add extra flags if provided
        if extra_flags:
            flags = " ".join(extra_flags)
            content.append(f"set(CMAKE_C_FLAGS_INIT \"{flags}\")")
            content.append(f"set(CMAKE_CXX_FLAGS_INIT \"{flags}\")")
        
        content.append("")
        return "\n".join(content)
    
    def _generate_mingw_gcc_toolchain(
        self,
        architecture: str,
        compiler_path: Optional[str],
        sysroot: Optional[str],
        extra_flags: Optional[list[str]]
    ) -> str:
        """Generate MinGW-GCC toolchain file.
        
        Args:
            architecture: Target architecture
            compiler_path: Optional compiler path
            sysroot: Optional sysroot path
            extra_flags: Optional extra compiler flags
            
        Returns:
            Toolchain file content
        """
        content = [
            "# CMake toolchain file for MinGW-GCC",
            "# Generated by OmniCPP ToolchainManager",
            ""
        ]
        
        # Set compiler
        if compiler_path:
            gcc_path = Path(compiler_path)
            content.append(f"set(CMAKE_C_COMPILER \"{gcc_path}\")")
            content.append(f"set(CMAKE_CXX_COMPILER \"{gcc_path.parent / 'g++.exe'}\")")
        else:
            content.append("set(CMAKE_C_COMPILER gcc)")
            content.append("set(CMAKE_CXX_COMPILER g++)")
        
        # Set architecture
        if architecture == "x64":
            content.append("set(CMAKE_SYSTEM_PROCESSOR x86_64)")
        elif architecture == "x86":
            content.append("set(CMAKE_SYSTEM_PROCESSOR i686)")
        elif architecture == "arm64":
            content.append("set(CMAKE_SYSTEM_PROCESSOR aarch64)")
        elif architecture == "arm":
            content.append("set(CMAKE_SYSTEM_PROCESSOR arm)")
        
        # Set sysroot if provided
        if sysroot:
            content.append(f"set(CMAKE_SYSROOT \"{sysroot}\")")
            content.append(f"set(CMAKE_FIND_ROOT_PATH \"{sysroot}\")")
        
        # Add extra flags if provided
        if extra_flags:
            flags = " ".join(extra_flags)
            content.append(f"set(CMAKE_C_FLAGS_INIT \"{flags}\")")
            content.append(f"set(CMAKE_CXX_FLAGS_INIT \"{flags}\")")
        
        content.append("")
        return "\n".join(content)
    
    def _generate_mingw_clang_toolchain(
        self,
        architecture: str,
        compiler_path: Optional[str],
        sysroot: Optional[str],
        extra_flags: Optional[list[str]]
    ) -> str:
        """Generate MinGW-Clang toolchain file.
        
        Args:
            architecture: Target architecture
            compiler_path: Optional compiler path
            sysroot: Optional sysroot path
            extra_flags: Optional extra compiler flags
            
        Returns:
            Toolchain file content
        """
        content = [
            "# CMake toolchain file for MinGW-Clang",
            "# Generated by OmniCPP ToolchainManager",
            ""
        ]
        
        # Set compiler
        if compiler_path:
            clang_path = Path(compiler_path)
            content.append(f"set(CMAKE_C_COMPILER \"{clang_path}\")")
            content.append(f"set(CMAKE_CXX_COMPILER \"{clang_path.parent / 'clang++.exe'}\")")
        else:
            content.append("set(CMAKE_C_COMPILER clang)")
            content.append("set(CMAKE_CXX_COMPILER clang++)")
        
        # Set architecture
        if architecture == "x64":
            content.append("set(CMAKE_SYSTEM_PROCESSOR x86_64)")
        elif architecture == "x86":
            content.append("set(CMAKE_SYSTEM_PROCESSOR i686)")
        elif architecture == "arm64":
            content.append("set(CMAKE_SYSTEM_PROCESSOR aarch64)")
        elif architecture == "arm":
            content.append("set(CMAKE_SYSTEM_PROCESSOR arm)")
        
        # Set sysroot if provided
        if sysroot:
            content.append(f"set(CMAKE_SYSROOT \"{sysroot}\")")
            content.append(f"set(CMAKE_FIND_ROOT_PATH \"{sysroot}\")")
        
        # Add extra flags if provided
        if extra_flags:
            flags = " ".join(extra_flags)
            content.append(f"set(CMAKE_C_FLAGS_INIT \"{flags}\")")
            content.append(f"set(CMAKE_CXX_FLAGS_INIT \"{flags}\")")
        
        content.append("")
        return "\n".join(content)
    
    def _generate_gcc_toolchain(
        self,
        architecture: str,
        compiler_path: Optional[str],
        sysroot: Optional[str],
        extra_flags: Optional[list[str]]
    ) -> str:
        """Generate GCC toolchain file.
        
        Args:
            architecture: Target architecture
            compiler_path: Optional compiler path
            sysroot: Optional sysroot path
            extra_flags: Optional extra compiler flags
            
        Returns:
            Toolchain file content
        """
        content = [
            "# CMake toolchain file for GCC",
            "# Generated by OmniCPP ToolchainManager",
            ""
        ]
        
        # Set compiler
        if compiler_path:
            gcc_path = Path(compiler_path)
            content.append(f"set(CMAKE_C_COMPILER \"{gcc_path}\")")
            content.append(f"set(CMAKE_CXX_COMPILER \"{gcc_path.parent / 'g++'}\")")
        else:
            content.append("set(CMAKE_C_COMPILER gcc)")
            content.append("set(CMAKE_CXX_COMPILER g++)")
        
        # Set architecture
        if architecture == "x64":
            content.append("set(CMAKE_SYSTEM_PROCESSOR x86_64)")
        elif architecture == "x86":
            content.append("set(CMAKE_SYSTEM_PROCESSOR i686)")
        elif architecture == "arm64":
            content.append("set(CMAKE_SYSTEM_PROCESSOR aarch64)")
        elif architecture == "arm":
            content.append("set(CMAKE_SYSTEM_PROCESSOR arm)")
        
        # Set sysroot if provided
        if sysroot:
            content.append(f"set(CMAKE_SYSROOT \"{sysroot}\")")
            content.append(f"set(CMAKE_FIND_ROOT_PATH \"{sysroot}\")")
        
        # Add extra flags if provided
        if extra_flags:
            flags = " ".join(extra_flags)
            content.append(f"set(CMAKE_C_FLAGS_INIT \"{flags}\")")
            content.append(f"set(CMAKE_CXX_FLAGS_INIT \"{flags}\")")
        
        content.append("")
        return "\n".join(content)
    
    def _generate_clang_toolchain(
        self,
        architecture: str,
        compiler_path: Optional[str],
        sysroot: Optional[str],
        extra_flags: Optional[list[str]]
    ) -> str:
        """Generate Clang toolchain file.
        
        Args:
            architecture: Target architecture
            compiler_path: Optional compiler path
            sysroot: Optional sysroot path
            extra_flags: Optional extra compiler flags
            
        Returns:
            Toolchain file content
        """
        content = [
            "# CMake toolchain file for Clang",
            "# Generated by OmniCPP ToolchainManager",
            ""
        ]
        
        # Set compiler
        if compiler_path:
            clang_path = Path(compiler_path)
            content.append(f"set(CMAKE_C_COMPILER \"{clang_path}\")")
            content.append(f"set(CMAKE_CXX_COMPILER \"{clang_path.parent / 'clang++'}\")")
        else:
            content.append("set(CMAKE_C_COMPILER clang)")
            content.append("set(CMAKE_CXX_COMPILER clang++)")
        
        # Set architecture
        if architecture == "x64":
            content.append("set(CMAKE_SYSTEM_PROCESSOR x86_64)")
        elif architecture == "x86":
            content.append("set(CMAKE_SYSTEM_PROCESSOR i686)")
        elif architecture == "arm64":
            content.append("set(CMAKE_SYSTEM_PROCESSOR aarch64)")
        elif architecture == "arm":
            content.append("set(CMAKE_SYSTEM_PROCESSOR arm)")
        
        # Set sysroot if provided
        if sysroot:
            content.append(f"set(CMAKE_SYSROOT \"{sysroot}\")")
            content.append(f"set(CMAKE_FIND_ROOT_PATH \"{sysroot}\")")
        
        # Add extra flags if provided
        if extra_flags:
            flags = " ".join(extra_flags)
            content.append(f"set(CMAKE_C_FLAGS_INIT \"{flags}\")")
            content.append(f"set(CMAKE_CXX_FLAGS_INIT \"{flags}\")")
        
        content.append("")
        return "\n".join(content)
    
    def _generate_emscripten_toolchain(
        self,
        architecture: str,
        compiler_path: Optional[str],
        extra_flags: Optional[list[str]]
    ) -> str:
        """Generate Emscripten toolchain file.
        
        Args:
            architecture: Target architecture (should be wasm32 or wasm64)
            compiler_path: Optional compiler path
            extra_flags: Optional extra compiler flags
            
        Returns:
            Toolchain file content
        """
        content = [
            "# CMake toolchain file for Emscripten",
            "# Generated by OmniCPP ToolchainManager",
            ""
        ]
        
        # Set compiler
        if compiler_path:
            emcc_path = Path(compiler_path)
            content.append(f"set(CMAKE_C_COMPILER \"{emcc_path}\")")
            content.append(f"set(CMAKE_CXX_COMPILER \"{emcc_path.parent / 'em++'}\")")
        else:
            content.append("set(CMAKE_C_COMPILER emcc)")
            content.append("set(CMAKE_CXX_COMPILER em++)")
        
        # Set system name
        content.append("set(CMAKE_SYSTEM_NAME Emscripten)")
        content.append("set(CMAKE_SYSTEM_PROCESSOR wasm)")
        
        # Add extra flags if provided
        if extra_flags:
            flags = " ".join(extra_flags)
            content.append(f"set(CMAKE_C_FLAGS_INIT \"{flags}\")")
            content.append(f"set(CMAKE_CXX_FLAGS_INIT \"{flags}\")")
        
        content.append("")
        return "\n".join(content)
    
    def list_toolchains(self) -> list[str]:
        """List all available toolchain files.
        
        Returns:
            List of toolchain file paths
        """
        toolchains: list[str] = []
        
        if not self.toolchain_dir.exists():
            return toolchains
        
        for file_path in self.toolchain_dir.glob("*.cmake"):
            toolchains.append(str(file_path))
        
        self.logger.debug(f"Found {len(toolchains)} toolchain files")
        return toolchains
    
    def get_toolchain(self, toolchain_type: str, architecture: str = "x64") -> Optional[str]:
        """Get toolchain file path for type and architecture.
        
        Args:
            toolchain_type: Type of toolchain
            architecture: Target architecture
            
        Returns:
            Toolchain file path or None if not found
        """
        toolchain_name = f"{toolchain_type}-{architecture}.cmake"
        toolchain_path = self.toolchain_dir / toolchain_name
        
        if toolchain_path.exists():
            return str(toolchain_path)
        
        return None
    
    def remove_toolchain(self, toolchain_type: str, architecture: str = "x64") -> bool:
        """Remove toolchain file.
        
        Args:
            toolchain_type: Type of toolchain
            architecture: Target architecture
            
        Returns:
            True if toolchain was removed, False if not found
        """
        toolchain_name = f"{toolchain_type}-{architecture}.cmake"
        toolchain_path = self.toolchain_dir / toolchain_name
        
        if toolchain_path.exists():
            try:
                toolchain_path.unlink()
                self.logger.info(f"Removed toolchain file: {toolchain_path}")
                return True
            except Exception as e:
                self.logger.error(f"Failed to remove toolchain file: {e}")
                return False
        
        return False
    
    def validate_toolchain(self, toolchain_path: str) -> list[str]:
        """Validate toolchain file and return list of issues.
        
        Args:
            toolchain_path: Path to toolchain file
            
        Returns:
            List of validation issue messages
        """
        issues: list[str] = []
        
        path = Path(toolchain_path)
        
        # Check if file exists
        if not path.exists():
            issues.append(f"Toolchain file does not exist: {toolchain_path}")
            return issues
        
        # Check file extension
        if path.suffix != ".cmake":
            issues.append(f"Toolchain file must have .cmake extension: {toolchain_path}")
        
        # Check file content
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for required CMake variables
                required_vars = ["CMAKE_C_COMPILER", "CMAKE_CXX_COMPILER"]
                for var in required_vars:
                    if var not in content:
                        issues.append(f"Toolchain file missing required variable: {var}")
                
                # Check for common errors
                if "set(" not in content:
                    issues.append("Toolchain file does not contain any set() commands")
                
        except Exception as e:
            issues.append(f"Failed to read toolchain file: {e}")
        
        if not issues:
            self.logger.info(f"Toolchain validation passed: {toolchain_path}")
        else:
            self.logger.warning(f"Toolchain validation found {len(issues)} issues: {toolchain_path}")
        
        return issues
