"""
MinGW Environment Setup

This module provides comprehensive MSYS2 environment setup for MinGW compiler execution,
including environment variable management, path configuration, and validation.
"""

import logging
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from .terminal_invoker import TerminalInvoker, CommandResult


class MSYS2Environment(Enum):
    """MSYS2 environment types
    
    Attributes:
        UCRT64: UCRT64 environment (recommended for C++23)
        MINGW64: MINGW64 environment (64-bit, MSVCRT)
        MINGW32: MINGW32 environment (32-bit, MSVCRT)
        MSYS: MSYS environment (POSIX compatibility)
        CLANG64: CLANG64 environment (Clang-based)
    """
    UCRT64 = "UCRT64"
    MINGW64 = "MINGW64"
    MINGW32 = "MINGW32"
    MSYS = "MSYS"
    CLANG64 = "CLANG64"


@dataclass
class MinGWEnvironmentConfig:
    """Configuration for MinGW environment setup
    
    Attributes:
        environment: MSYS2 environment type
        msys2_path: Path to MSYS2 installation
        architecture: Target architecture (x64, x86)
        set_pkg_config: Set PKG_CONFIG_PATH environment variable
        set_aclocal: Set ACLOCAL_PATH environment variable
    """
    environment: MSYS2Environment = MSYS2Environment.UCRT64
    msys2_path: Optional[str] = None
    architecture: str = "x64"
    set_pkg_config: bool = True
    set_aclocal: bool = True


@dataclass
class EnvironmentValidationResult:
    """Result of environment validation
    
    Attributes:
        is_valid: Whether environment is valid
        errors: List of error messages
        warnings: List of warning messages
        missing_variables: List of missing environment variables
        invalid_paths: List of invalid paths
    """
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    missing_variables: List[str] = field(default_factory=list)
    invalid_paths: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "missing_variables": self.missing_variables,
            "invalid_paths": self.invalid_paths
        }


class MinGWEnvironment:
    """MinGW/MSYS2 environment setup and management
    
    This class provides comprehensive MinGW environment setup including:
    - MSYS2 environment variable configuration (MSYSTEM, MINGW_PREFIX, MINGW_CHOST)
    - Path configuration for all MSYS2 environments (UCRT64, MINGW64, MINGW32, MSYS, CLANG64)
    - Environment variable capture and restoration
    - Package configuration (PKG_CONFIG_PATH, ACLOCAL_PATH)
    - Environment validation
    """

    # Required environment variables for MinGW
    REQUIRED_ENV_VARS = [
        "PATH",
        "MSYSTEM",
        "MINGW_PREFIX"
    ]

    # Optional but important environment variables
    OPTIONAL_ENV_VARS = [
        "MINGW_CHOST",
        "MINGW_HOME",
        "PKG_CONFIG_PATH",
        "ACLOCAL_PATH",
        "MSYS2_PATH"
    ]

    # MSYS2 environment to prefix mapping
    ENVIRONMENT_PREFIX_MAP = {
        MSYS2Environment.UCRT64: "/ucrt64",
        MSYS2Environment.MINGW64: "/mingw64",
        MSYS2Environment.MINGW32: "/mingw32",
        MSYS2Environment.MSYS: "/usr",
        MSYS2Environment.CLANG64: "/clang64"
    }

    # MSYS2 environment to CHOST mapping
    ENVIRONMENT_CHOST_MAP = {
        MSYS2Environment.UCRT64: "x86_64-w64-mingw32",
        MSYS2Environment.MINGW64: "x86_64-w64-mingw32",
        MSYS2Environment.MINGW32: "i686-w64-mingw32",
        MSYS2Environment.MSYS: "x86_64-pc-msys",
        MSYS2Environment.CLANG64: "x86_64-w64-mingw32"
    }

    # MSYS2 environment to architecture mapping
    ENVIRONMENT_ARCH_MAP = {
        MSYS2Environment.UCRT64: "x64",
        MSYS2Environment.MINGW64: "x64",
        MSYS2Environment.MINGW32: "x86",
        MSYS2Environment.MSYS: "x64",
        MSYS2Environment.CLANG64: "x64"
    }

    def __init__(
        self,
        terminal_invoker: Optional[TerminalInvoker] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize MinGW environment manager
        
        Args:
            terminal_invoker: Terminal invoker for executing commands
            logger: Logger instance for logging operations
        """
        self._logger = logger or logging.getLogger(__name__)
        self._terminal_invoker = terminal_invoker or TerminalInvoker(logger=self._logger)
        
        # Environment state
        self._original_environment: Dict[str, str] = {}
        self._current_environment: Dict[str, str] = {}
        self._is_setup: bool = False
        self._msys2_path: Optional[str] = None
        self._current_environment_type: Optional[MSYS2Environment] = None

    def setup(
        self,
        config: MinGWEnvironmentConfig
    ) -> Dict[str, str]:
        """
        Setup MinGW environment with specified configuration
        
        Args:
            config: MinGW environment configuration
            
        Returns:
            Environment variables after setup
            
        Raises:
            RuntimeError: If MSYS2 path not found or setup fails
            ValueError: If configuration is invalid
        """
        self._logger.info(
            f"Setting up MinGW environment for {config.environment.value}"
        )

        # Validate configuration
        self._validate_config(config)

        # Save original environment
        self._original_environment = self._terminal_invoker.capture_environment()
        self._logger.debug("Saved original environment")

        # Find MSYS2 path
        self._msys2_path = self._find_msys2_path(config.msys2_path)
        
        if not self._msys2_path:
            error_msg = (
                "MSYS2 installation not found. "
                "Please install MSYS2 or provide the installation path."
            )
            self._logger.error(error_msg)
            raise RuntimeError(error_msg)

        self._logger.info(f"Found MSYS2 installation: {self._msys2_path}")

        # Setup MSYS2 environment
        self._current_environment_type = config.environment
        self._setup_msys2(config)

        # Capture environment after setup
        self._current_environment = self._terminal_invoker.capture_environment()
        self._is_setup = True

        self._logger.info("MinGW environment setup complete")
        return self._current_environment

    def setup_msys2(
        self,
        environment: MSYS2Environment = MSYS2Environment.UCRT64,
        msys2_path: Optional[str] = None,
        architecture: str = "x64",
        set_pkg_config: bool = True,
        set_aclocal: bool = True
    ) -> Dict[str, str]:
        """
        Setup MSYS2 environment by configuring environment variables
        
        Args:
            environment: MSYS2 environment type
            msys2_path: Path to MSYS2 installation (auto-detect if None)
            architecture: Target architecture (x64, x86)
            set_pkg_config: Set PKG_CONFIG_PATH environment variable
            set_aclocal: Set ACLOCAL_PATH environment variable
            
        Returns:
            Environment variables after setup
            
        Raises:
            RuntimeError: If MSYS2 path not found or setup fails
            ValueError: If environment type is invalid
        """
        self._logger.info(
            f"Setting up MSYS2 {environment.value} environment"
        )

        # Validate environment type
        if not isinstance(environment, MSYS2Environment):
            raise ValueError(
                f"Invalid environment type: {type(environment)}. "
                f"Expected MSYS2Environment enum."
            )

        # Save original environment if not already saved
        if not self._original_environment:
            self._original_environment = self._terminal_invoker.capture_environment()
            self._logger.debug("Saved original environment")

        # Find MSYS2 path
        self._msys2_path = self._find_msys2_path(msys2_path)
        
        if not self._msys2_path:
            error_msg = (
                "MSYS2 installation not found. "
                "Please install MSYS2 or provide the installation path."
            )
            self._logger.error(error_msg)
            raise RuntimeError(error_msg)

        self._logger.info(f"Found MSYS2 installation: {self._msys2_path}")

        # Store current environment type
        self._current_environment_type = environment

        # Set MSYSTEM environment variable
        os.environ["MSYSTEM"] = environment.value
        self._logger.debug(f"Set MSYSTEM={environment.value}")

        # Set MINGW_PREFIX environment variable
        mingw_prefix = self.ENVIRONMENT_PREFIX_MAP.get(environment, "/usr")
        os.environ["MINGW_PREFIX"] = mingw_prefix
        self._logger.debug(f"Set MINGW_PREFIX={mingw_prefix}")

        # Set MINGW_CHOST environment variable
        mingw_chost = self.ENVIRONMENT_CHOST_MAP.get(environment, "")
        if mingw_chost:
            os.environ["MINGW_CHOST"] = mingw_chost
            self._logger.debug(f"Set MINGW_CHOST={mingw_chost}")

        # Set MSYS2_PATH environment variable
        os.environ["MSYS2_PATH"] = self._msys2_path
        self._logger.debug(f"Set MSYS2_PATH={self._msys2_path}")

        # Set MINGW_HOME environment variable
        os.environ["MINGW_HOME"] = self._msys2_path
        self._logger.debug(f"Set MINGW_HOME={self._msys2_path}")

        # Add environment-specific bin directory to PATH
        env_bin_path = os.path.join(
            self._msys2_path,
            environment.value.lower(),
            "bin"
        )
        usr_bin_path = os.path.join(self._msys2_path, "usr", "bin")

        if os.path.exists(env_bin_path):
            current_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{env_bin_path};{usr_bin_path};{current_path}"
            self._logger.debug(f"Added {environment.value} bin to PATH: {env_bin_path}")
        else:
            self._logger.warning(
                f"Environment bin path not found: {env_bin_path}"
            )

        # Set PKG_CONFIG_PATH if requested
        if set_pkg_config:
            self._set_pkg_config_path(environment)

        # Set ACLOCAL_PATH if requested
        if set_aclocal:
            self._set_aclocal_path(environment)

        # Capture environment after setup
        self._current_environment = self._terminal_invoker.capture_environment()
        self._is_setup = True

        self._logger.info(f"MSYS2 {environment.value} environment setup complete")
        return self._current_environment

    def get_environment_variables(self) -> Dict[str, str]:
        """
        Get current MinGW environment variables
        
        Returns:
            Dictionary of environment variables
            
        Raises:
            RuntimeError: If environment has not been setup
        """
        if not self._is_setup:
            error_msg = "Environment has not been setup. Call setup() first."
            self._logger.error(error_msg)
            raise RuntimeError(error_msg)

        self._logger.debug("Getting current environment variables")
        return self._current_environment.copy()

    def restore_environment(self) -> None:
        """
        Restore environment to original state
        
        Raises:
            RuntimeError: If environment has not been setup
        """
        if not self._is_setup:
            error_msg = "Environment has not been setup. Nothing to restore."
            self._logger.warning(error_msg)
            return

        self._logger.info("Restoring original environment")
        self._terminal_invoker.restore_environment(self._original_environment)
        self._current_environment = self._original_environment.copy()
        self._is_setup = False

        self._logger.info("Environment restored successfully")

    def validate_environment(self) -> EnvironmentValidationResult:
        """
        Validate current MinGW environment
        
        Returns:
            Environment validation result
        """
        self._logger.info("Validating MinGW environment")

        result = EnvironmentValidationResult(is_valid=True)
        current_env = self._terminal_invoker.capture_environment()

        # Check required environment variables
        for var in self.REQUIRED_ENV_VARS:
            if var not in current_env or not current_env[var]:
                result.missing_variables.append(var)
                result.is_valid = False
                self._logger.warning(f"Missing required environment variable: {var}")

        # Check optional environment variables
        for var in self.OPTIONAL_ENV_VARS:
            if var not in current_env:
                result.warnings.append(f"Missing optional variable: {var}")
                self._logger.debug(f"Missing optional environment variable: {var}")

        # Validate paths in environment variables
        self._validate_environment_paths(current_env, result)

        # Check for g++.exe in PATH
        self._validate_gcc_in_path(current_env, result)

        # Check MSYS2 installation
        if self._msys2_path:
            self._validate_msys2_installation(result)

        # Log validation result
        if result.is_valid:
            self._logger.info("MinGW environment validation passed")
        else:
            self._logger.error(
                f"MinGW environment validation failed: {len(result.errors)} errors, "
                f"{len(result.warnings)} warnings"
            )

        return result

    def _validate_config(self, config: MinGWEnvironmentConfig) -> None:
        """
        Validate MinGW environment configuration
        
        Args:
            config: Configuration to validate
            
        Raises:
            ValueError: If configuration is invalid
        """
        self._logger.debug("Validating MinGW environment configuration")

        # Validate environment type
        if not isinstance(config.environment, MSYS2Environment):
            raise ValueError(
                f"Invalid environment type: {type(config.environment)}. "
                f"Expected MSYS2Environment enum."
            )

        # Validate architecture
        valid_architectures = ["x64", "x86", "arm", "arm64"]
        if config.architecture not in valid_architectures:
            raise ValueError(
                f"Invalid architecture: {config.architecture}. "
                f"Valid architectures are: {', '.join(valid_architectures)}"
            )

        self._logger.debug("Configuration validation passed")

    def _find_msys2_path(self, provided_path: Optional[str] = None) -> Optional[str]:
        """
        Find MSYS2 installation path
        
        Args:
            provided_path: User-provided MSYS2 path
            
        Returns:
            Path to MSYS2 installation or None if not found
        """
        self._logger.debug("Searching for MSYS2 installation")

        # If path is provided, use it
        if provided_path:
            if os.path.exists(provided_path):
                self._logger.debug(f"Using provided MSYS2 path: {provided_path}")
                return provided_path
            else:
                self._logger.warning(
                    f"Provided MSYS2 path does not exist: {provided_path}"
                )
                return None

        # Try common installation paths
        common_paths = [
            r"C:\msys64",
            r"C:\msys32",
            r"C:\mingw64",
            r"C:\mingw",
            r"C:\mingw-w64",
            os.path.join(
                os.environ.get("ProgramFiles", r"C:\Program Files"),
                "msys64"
            ),
            os.path.join(
                os.environ.get("ProgramFiles", r"C:\Program Files"),
                "mingw64"
            ),
        ]

        for path in common_paths:
            if os.path.exists(path):
                # Check if it's a valid MSYS2 installation
                if os.path.exists(os.path.join(path, "usr", "bin")):
                    self._logger.debug(f"Found MSYS2 installation at: {path}")
                    return path

        self._logger.warning("MSYS2 installation not found in common paths")
        return None

    def _setup_msys2(self, config: MinGWEnvironmentConfig) -> None:
        """
        Setup MSYS2 environment with configuration
        
        Args:
            config: MinGW environment configuration
        """
        self._logger.debug("Setting up MSYS2 environment")

        # Set MSYSTEM
        os.environ["MSYSTEM"] = config.environment.value
        self._logger.debug(f"Set MSYSTEM={config.environment.value}")

        # Set MINGW_PREFIX
        mingw_prefix = self.ENVIRONMENT_PREFIX_MAP.get(
            config.environment,
            "/usr"
        )
        os.environ["MINGW_PREFIX"] = mingw_prefix
        self._logger.debug(f"Set MINGW_PREFIX={mingw_prefix}")

        # Set MINGW_CHOST
        mingw_chost = self.ENVIRONMENT_CHOST_MAP.get(config.environment, "")
        if mingw_chost:
            os.environ["MINGW_CHOST"] = mingw_chost
            self._logger.debug(f"Set MINGW_CHOST={mingw_chost}")

        # Set MSYS2_PATH
        os.environ["MSYS2_PATH"] = self._msys2_path
        self._logger.debug(f"Set MSYS2_PATH={self._msys2_path}")

        # Set MINGW_HOME
        os.environ["MINGW_HOME"] = self._msys2_path
        self._logger.debug(f"Set MINGW_HOME={self._msys2_path}")

        # Add environment-specific bin directory to PATH
        env_bin_path = os.path.join(
            self._msys2_path,
            config.environment.value.lower(),
            "bin"
        )
        usr_bin_path = os.path.join(self._msys2_path, "usr", "bin")

        if os.path.exists(env_bin_path):
            current_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{env_bin_path};{usr_bin_path};{current_path}"
            self._logger.debug(f"Added {config.environment.value} bin to PATH: {env_bin_path}")
        else:
            self._logger.warning(
                f"Environment bin path not found: {env_bin_path}"
            )

        # Set PKG_CONFIG_PATH if requested
        if config.set_pkg_config:
            self._set_pkg_config_path(config.environment)

        # Set ACLOCAL_PATH if requested
        if config.set_aclocal:
            self._set_aclocal_path(config.environment)

        self._logger.debug("MSYS2 environment setup complete")

    def _set_pkg_config_path(self, environment: MSYS2Environment) -> None:
        """
        Set PKG_CONFIG_PATH environment variable
        
        Args:
            environment: MSYS2 environment type
        """
        self._logger.debug("Setting PKG_CONFIG_PATH")

        mingw_prefix = self.ENVIRONMENT_PREFIX_MAP.get(environment, "/usr")
        pkg_config_paths = [
            os.path.join(self._msys2_path, mingw_prefix.lstrip("/"), "lib", "pkgconfig"),
            os.path.join(self._msys2_path, mingw_prefix.lstrip("/"), "share", "pkgconfig"),
            os.path.join(self._msys2_path, "usr", "lib", "pkgconfig"),
            os.path.join(self._msys2_path, "usr", "share", "pkgconfig"),
        ]

        # Filter existing paths
        existing_paths = [p for p in pkg_config_paths if os.path.exists(p)]

        if existing_paths:
            pkg_config_path = os.pathsep.join(existing_paths)
            os.environ["PKG_CONFIG_PATH"] = pkg_config_path
            self._logger.debug(f"Set PKG_CONFIG_PATH={pkg_config_path}")
        else:
            self._logger.warning("No valid PKG_CONFIG_PATH found")

    def _set_aclocal_path(self, environment: MSYS2Environment) -> None:
        """
        Set ACLOCAL_PATH environment variable
        
        Args:
            environment: MSYS2 environment type
        """
        self._logger.debug("Setting ACLOCAL_PATH")

        mingw_prefix = self.ENVIRONMENT_PREFIX_MAP.get(environment, "/usr")
        aclocal_paths = [
            os.path.join(self._msys2_path, mingw_prefix.lstrip("/"), "share", "aclocal"),
            os.path.join(self._msys2_path, "usr", "share", "aclocal"),
        ]

        # Filter existing paths
        existing_paths = [p for p in aclocal_paths if os.path.exists(p)]

        if existing_paths:
            aclocal_path = os.pathsep.join(existing_paths)
            os.environ["ACLOCAL_PATH"] = aclocal_path
            self._logger.debug(f"Set ACLOCAL_PATH={aclocal_path}")
        else:
            self._logger.warning("No valid ACLOCAL_PATH found")

    def _validate_environment_paths(
        self,
        env: Dict[str, str],
        result: EnvironmentValidationResult
    ) -> None:
        """
        Validate paths in environment variables
        
        Args:
            env: Environment variables
            result: Validation result to update
        """
        self._logger.debug("Validating environment paths")

        # Check PATH
        if "PATH" in env:
            path_dirs = env["PATH"].split(os.pathsep)
            for path_dir in path_dirs:
                if path_dir and not os.path.exists(path_dir):
                    result.invalid_paths.append(f"PATH: {path_dir}")
                    result.warnings.append(f"Invalid PATH directory: {path_dir}")
                    self._logger.warning(f"Invalid PATH directory: {path_dir}")

        # Check PKG_CONFIG_PATH
        if "PKG_CONFIG_PATH" in env:
            pkg_paths = env["PKG_CONFIG_PATH"].split(os.pathsep)
            for path_dir in pkg_paths:
                if path_dir and not os.path.exists(path_dir):
                    result.invalid_paths.append(f"PKG_CONFIG_PATH: {path_dir}")
                    result.warnings.append(f"Invalid PKG_CONFIG_PATH: {path_dir}")
                    self._logger.warning(f"Invalid PKG_CONFIG_PATH: {path_dir}")

        # Check ACLOCAL_PATH
        if "ACLOCAL_PATH" in env:
            aclocal_paths = env["ACLOCAL_PATH"].split(os.pathsep)
            for path_dir in aclocal_paths:
                if path_dir and not os.path.exists(path_dir):
                    result.invalid_paths.append(f"ACLOCAL_PATH: {path_dir}")
                    result.warnings.append(f"Invalid ACLOCAL_PATH: {path_dir}")
                    self._logger.warning(f"Invalid ACLOCAL_PATH: {path_dir}")

    def _validate_gcc_in_path(
        self,
        env: Dict[str, str],
        result: EnvironmentValidationResult
    ) -> None:
        """
        Validate that g++.exe is in PATH
        
        Args:
            env: Environment variables
            result: Validation result to update
        """
        self._logger.debug("Validating g++.exe in PATH")

        if "PATH" not in env:
            result.errors.append("PATH environment variable not set")
            result.is_valid = False
            return

        path_dirs = env["PATH"].split(os.pathsep)
        gcc_found = False

        for path_dir in path_dirs:
            gcc_path = os.path.join(path_dir, "g++.exe")
            if os.path.exists(gcc_path):
                gcc_found = True
                self._logger.debug(f"Found g++.exe at: {gcc_path}")
                break

        if not gcc_found:
            result.errors.append("g++.exe not found in PATH")
            result.is_valid = False
            self._logger.error("g++.exe not found in PATH")

    def _validate_msys2_installation(self, result: EnvironmentValidationResult) -> None:
        """
        Validate MSYS2 installation
        
        Args:
            result: Validation result to update
        """
        self._logger.debug("Validating MSYS2 installation")

        if not self._msys2_path:
            result.errors.append("MSYS2 path not set")
            result.is_valid = False
            return

        # Check for required directories
        required_dirs = ["usr", "usr/bin"]
        for dir_name in required_dirs:
            dir_path = os.path.join(self._msys2_path, dir_name)
            if not os.path.exists(dir_path):
                result.errors.append(f"MSYS2 directory not found: {dir_path}")
                result.is_valid = False
                self._logger.error(f"MSYS2 directory not found: {dir_path}")

        # Check for environment-specific directory
        if self._current_environment_type:
            env_dir = os.path.join(
                self._msys2_path,
                self._current_environment_type.value.lower()
            )
            if not os.path.exists(env_dir):
                result.errors.append(f"MSYS2 environment directory not found: {env_dir}")
                result.is_valid = False
                self._logger.error(f"MSYS2 environment directory not found: {env_dir}")
