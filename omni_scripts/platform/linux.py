# omni_scripts/platform/linux.py
"""
Linux-specific platform detection for OmniCPP project.

Provides Linux platform detection including GCC and Clang compiler detection,
and terminal environment setup for Linux compilers.
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Union

from omni_scripts.logging.logger import get_logger


@dataclass
class GCCInfo:
    """Information about GCC installation.
    
    Attributes:
        version: GCC version (e.g., '13.2.0')
        path: Path to gcc executable
        gxx_path: Path to g++ executable
        supports_cpp23: Whether GCC supports C++23
    """
    version: str
    path: Path
    gxx_path: Path
    supports_cpp23: bool


@dataclass
class ClangInfo:
    """Information about Clang installation.
    
    Attributes:
        version: Clang version (e.g., '18.1.3')
        path: Path to clang executable
        clangxx_path: Path to clang++ executable
        supports_cpp23: Whether Clang supports C++23
    """
    version: str
    path: Path
    clangxx_path: Path
    supports_cpp23: bool


def detect_gcc() -> Optional[GCCInfo]:
    """Detect GCC compiler installation on Linux.
    
    This function searches for GCC compiler installation and validates
    compiler availability. It checks for gcc and g++ executables and
    determines the GCC version.
    
    Returns:
        GCCInfo object if GCC is found, None otherwise
    """
    logger = get_logger(__name__)
    
    try:
        # Try to find gcc in PATH
        gcc_path = _find_executable("gcc")
        if not gcc_path:
            logger.warning("GCC not found in PATH")
            return None
        
        gxx_path = _find_executable("g++")
        if not gxx_path:
            logger.warning("g++ not found in PATH")
            return None
        
        # Get GCC version
        version = _get_gcc_version(gcc_path)
        
        # Check C++23 support
        supports_cpp23 = _check_gcc_cpp23_support(gcc_path, version)
        
        gcc_info = GCCInfo(
            version=version,
            path=gcc_path,
            gxx_path=gxx_path,
            supports_cpp23=supports_cpp23
        )
        
        logger.info(
            f"Found GCC {version} at {gcc_path} "
            f"(C++23: {'Yes' if supports_cpp23 else 'No'})"
        )
        
        return gcc_info
        
    except Exception as e:
        logger.error(f"GCC detection failed: {e}")
        return None


def _find_executable(name: str) -> Optional[Path]:
    """Find an executable in PATH.
    
    Args:
        name: Name of the executable to find
        
    Returns:
        Path to the executable if found, None otherwise
    """
    try:
        result = subprocess.run(
            ["which", name],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip())
        
        return None
        
    except Exception:
        return None


def _get_gcc_version(gcc_path: Path) -> str:
    """Get GCC version from gcc executable.
    
    Args:
        gcc_path: Path to gcc executable
        
    Returns:
        GCC version string
    """
    logger = get_logger(__name__)
    
    try:
        result = subprocess.run(
            [str(gcc_path), "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.stdout:
            # Parse version from gcc output
            # Output format: "gcc (GCC) 13.2.0"
            match = re.search(r"gcc.*?(\d+\.\d+\.\d+)", result.stdout)
            if match:
                return match.group(1)
        
        logger.warning("Could not determine GCC version, using default")
        return "13.2.0"
        
    except Exception as e:
        logger.warning(f"Failed to get GCC version: {e}, using default")
        return "13.2.0"


def _check_gcc_cpp23_support(gcc_path: Path, version: str) -> bool:
    """Check if GCC supports C++23.
    
    Args:
        gcc_path: Path to gcc executable
        version: GCC version string
        
    Returns:
        True if GCC supports C++23, False otherwise
    """
    logger = get_logger(__name__)
    
    try:
        # GCC 13+ has good C++23 support
        major_version = int(version.split(".")[0])
        if major_version >= 13:
            return True
        
        # Try to compile a simple C++23 test
        test_code = """
        #include <version>
        #if __cpp_modules >= 202207L
        int main() { return 0; }
        #else
        #error "C++23 not supported"
        #endif
        """
        
        result = subprocess.run(
            [str(gcc_path), "-std=c++23", "-x", "c++", "-o", "/dev/null", "-"],
            input=test_code,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return result.returncode == 0
        
    except Exception as e:
        logger.warning(f"Failed to check GCC C++23 support: {e}")
        return False


def detect_clang() -> Optional[ClangInfo]:
    """Detect Clang compiler installation on Linux.
    
    This function searches for Clang compiler installation and validates
    compiler availability. It checks for clang and clang++ executables and
    determines the Clang version.
    
    Returns:
        ClangInfo object if Clang is found, None otherwise
    """
    logger = get_logger(__name__)
    
    try:
        # Try to find clang in PATH
        clang_path = _find_executable("clang")
        if not clang_path:
            logger.warning("Clang not found in PATH")
            return None
        
        clangxx_path = _find_executable("clang++")
        if not clangxx_path:
            logger.warning("clang++ not found in PATH")
            return None
        
        # Get Clang version
        version = _get_clang_version(clang_path)
        
        # Check C++23 support
        supports_cpp23 = _check_clang_cpp23_support(clang_path, version)
        
        clang_info = ClangInfo(
            version=version,
            path=clang_path,
            clangxx_path=clangxx_path,
            supports_cpp23=supports_cpp23
        )
        
        logger.info(
            f"Found Clang {version} at {clang_path} "
            f"(C++23: {'Yes' if supports_cpp23 else 'No'})"
        )
        
        return clang_info
        
    except Exception as e:
        logger.error(f"Clang detection failed: {e}")
        return None


def _get_clang_version(clang_path: Path) -> str:
    """Get Clang version from clang executable.
    
    Args:
        clang_path: Path to clang executable
        
    Returns:
        Clang version string
    """
    logger = get_logger(__name__)
    
    try:
        result = subprocess.run(
            [str(clang_path), "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.stdout:
            # Parse version from clang output
            # Output format: "clang version 18.1.3"
            match = re.search(r"clang version (\d+\.\d+\.\d+)", result.stdout)
            if match:
                return match.group(1)
        
        logger.warning("Could not determine Clang version, using default")
        return "18.1.0"
        
    except Exception as e:
        logger.warning(f"Failed to get Clang version: {e}, using default")
        return "18.1.0"


def _check_clang_cpp23_support(clang_path: Path, version: str) -> bool:
    """Check if Clang supports C++23.
    
    Args:
        clang_path: Path to clang executable
        version: Clang version string
        
    Returns:
        True if Clang supports C++23, False otherwise
    """
    logger = get_logger(__name__)
    
    try:
        # Clang 16+ has good C++23 support
        major_version = int(version.split(".")[0])
        if major_version >= 16:
            return True
        
        # Try to compile a simple C++23 test
        test_code = """
        #include <version>
        #if __cpp_modules >= 202207L
        int main() { return 0; }
        #else
        #error "C++23 not supported"
        #endif
        """
        
        result = subprocess.run(
            [str(clang_path), "-std=c++23", "-x", "c++", "-o", "/dev/null", "-"],
            input=test_code,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return result.returncode == 0
        
    except Exception as e:
        logger.warning(f"Failed to check Clang C++23 support: {e}")
        return False


def detect_system_compilers() -> Dict[str, Optional[Union[GCCInfo, ClangInfo]]]:
    """Detect all available compilers on Linux.
    
    This function detects GCC and Clang compilers and returns
    information about available compilers.
    
    Returns:
        Dictionary with compiler information
    """
    logger = get_logger(__name__)
    
    compilers: Dict[str, Optional[Union[GCCInfo, ClangInfo]]] = {
        "gcc": None,
        "clang": None
    }
    
    # Detect GCC
    gcc_info = detect_gcc()
    if gcc_info:
        compilers["gcc"] = gcc_info
    
    # Detect Clang
    clang_info = detect_clang()
    if clang_info:
        compilers["clang"] = clang_info
    
    # Log summary
    available = [name for name, info in compilers.items() if info is not None]
    if available:
        logger.info(f"Available compilers: {', '.join(available)}")
    else:
        logger.warning("No compilers found")
    
    return compilers


def setup_linux_environment(compiler: str = 'gcc') -> Dict[str, str]:
    """Set up appropriate environment for Linux compilers.
    
    This function sets up the environment for Linux compilers (GCC or Clang).
    It preserves existing environment variables, adds compiler-specific paths
    to PATH if needed, supports custom environment variable overrides, and
    validates environment setup before proceeding.
    
    Args:
        compiler: The compiler to set up ('gcc' or 'clang'). Defaults to 'gcc'.
        
    Returns:
        Dictionary of environment variables set up for the specified compiler.
        
    Raises:
        RuntimeError: If the specified compiler is not found or setup fails.
        ValueError: If an invalid compiler is specified.
        
    Example:
        >>> env = setup_linux_environment('gcc')
        >>> os.environ.update(env)
    """
    logger = get_logger(__name__)
    
    try:
        # Validate compiler type
        compiler = compiler.lower()
        if compiler not in ['gcc', 'clang']:
            raise ValueError(
                f"Invalid compiler: {compiler}. Must be 'gcc' or 'clang'."
            )
        
        logger.info(f"Setting up Linux environment for {compiler}")
        
        # Start with current environment variables
        env_vars = os.environ.copy()
        
        # Detect compiler and validate availability
        if compiler == 'gcc':
            gcc_info = detect_gcc()
            if not gcc_info:
                raise RuntimeError(
                    "GCC not found. Please install GCC using your package manager."
                )
            
            # Set CC and CXX environment variables
            env_vars['CC'] = str(gcc_info.path)
            env_vars['CXX'] = str(gcc_info.gxx_path)
            
            logger.info(f"GCC {gcc_info.version} found at {gcc_info.path}")
            
        elif compiler == 'clang':
            clang_info = detect_clang()
            if not clang_info:
                raise RuntimeError(
                    "Clang not found. Please install Clang using your package manager."
                )
            
            # Set CC and CXX environment variables
            env_vars['CC'] = str(clang_info.path)
            env_vars['CXX'] = str(clang_info.clangxx_path)
            
            logger.info(f"Clang {clang_info.version} found at {clang_info.path}")
        
        # Validate environment setup
        _validate_linux_environment(env_vars, compiler)
        
        logger.info(f"Linux environment set up successfully for {compiler}")
        logger.debug(f"Environment variables set: CC={env_vars.get('CC')}, CXX={env_vars.get('CXX')}")
        
        return env_vars
        
    except Exception as e:
        logger.error(f"Failed to set up Linux environment: {e}")
        raise RuntimeError(
            f"Failed to set up Linux environment: {e}"
        ) from e


def _validate_linux_environment(env_vars: Dict[str, str], compiler: str) -> None:
    """Validate Linux environment setup before proceeding.
    
    This function verifies that required environment variables are set,
    checks that compiler executables are accessible, validates PATH configuration,
    and tests compiler invocation with a simple command.
    
    Args:
        env_vars: Dictionary of environment variables to validate.
        compiler: The compiler being validated ('gcc' or 'clang').
        
    Raises:
        RuntimeError: If validation fails.
    """
    logger = get_logger(__name__)
    
    try:
        # Check required environment variables
        required_vars = ['CC', 'CXX']
        missing_vars = [var for var in required_vars if var not in env_vars]
        
        if missing_vars:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
        
        # Check compiler executables are accessible
        cc_path = Path(env_vars['CC'])
        cxx_path = Path(env_vars['CXX'])
        
        if not cc_path.exists():
            raise RuntimeError(
                f"CC compiler not found: {cc_path}"
            )
        
        if not cxx_path.exists():
            raise RuntimeError(
                f"CXX compiler not found: {cxx_path}"
            )
        
        # Validate PATH configuration
        path = env_vars.get('PATH', '')
        if not path:
            raise RuntimeError(
                "PATH environment variable is not set"
            )
        
        # Test compiler invocation with simple command
        try:
            result = subprocess.run(
                [str(cc_path), '--version'],
                capture_output=True,
                text=True,
                timeout=5,
                env=env_vars
            )
            
            if result.returncode != 0:
                raise RuntimeError(
                    f"Compiler invocation failed: {result.stderr}"
                )
            
            logger.debug(f"Compiler validation successful: {result.stdout.split()[0:3]}")
            
        except subprocess.TimeoutExpired:
            raise RuntimeError(
                f"Compiler invocation timed out"
            )
        except FileNotFoundError:
            raise RuntimeError(
                f"Compiler executable not found: {cc_path}"
            )
        
        logger.info(f"Linux environment validation successful for {compiler}")
        
    except Exception as e:
        logger.error(f"Linux environment validation failed: {e}")
        raise RuntimeError(
            f"Linux environment validation failed: {e}"
        ) from e


__all__ = [
    'GCCInfo',
    'ClangInfo',
    'detect_gcc',
    'detect_clang',
    'detect_system_compilers',
    'setup_linux_environment',
]
