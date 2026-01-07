"""
MSVC Environment Setup

This module provides comprehensive MSVC environment setup for compiler execution,
including vcvarsall.bat invocation, environment variable management, and validation.
"""

import logging
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from .msvc_architecture import MSVCArchitecture, MSVCArchitectureMapper
from .terminal_invoker import TerminalInvoker, CommandResult


@dataclass
class MSVCEnvironmentConfig:
    """Configuration for MSVC environment setup
    
    Attributes:
        architecture: Target architecture for MSVC environment
        platform_type: Platform type (desktop, uwp, store)
        spectre_mitigation: Enable Spectre mitigation
        windows_sdk_version: Specific Windows SDK version to use
        vc_install_path: Visual Studio installation path
    """
    architecture: MSVCArchitecture = MSVCArchitecture.X64
    platform_type: str = "desktop"
    spectre_mitigation: bool = False
    windows_sdk_version: Optional[str] = None
    vc_install_path: Optional[str] = None


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


class MSVCEnvironment:
    """MSVC environment setup and management
    
    This class provides comprehensive MSVC environment setup including:
    - vcvarsall.bat invocation with architecture and platform arguments
    - Environment variable capture and restoration
    - Spectre mitigation support
    - UWP and Store app platform support
    - Windows SDK version selection
    - Environment validation
    """

    # Required environment variables for MSVC
    REQUIRED_ENV_VARS = [
        "PATH",
        "INCLUDE",
        "LIB",
        "LIBPATH",
        "WindowsSDKVersion"
    ]

    # Optional but important environment variables
    OPTIONAL_ENV_VARS = [
        "VCINSTALLDIR",
        "VSINSTALLDIR",
        "DevEnvDir",
        "VCToolsInstallDir",
        "VCToolsVersion",
        "VSCMD_ARG_app_plat",
        "VSCMD_ARG_HOST_ARCH",
        "VSCMD_ARG_TGT_ARCH"
    ]

    def __init__(
        self,
        terminal_invoker: Optional[TerminalInvoker] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize MSVC environment manager
        
        Args:
            terminal_invoker: Terminal invoker for executing commands
            logger: Logger instance for logging operations
        """
        self._logger = logger or logging.getLogger(__name__)
        self._terminal_invoker = terminal_invoker or TerminalInvoker(logger=self._logger)
        self._arch_mapper = MSVCArchitectureMapper(logger=self._logger)
        
        # Environment state
        self._original_environment: Dict[str, str] = {}
        self._current_environment: Dict[str, str] = {}
        self._is_setup: bool = False
        self._vcvarsall_path: Optional[str] = None

    def setup(
        self,
        config: MSVCEnvironmentConfig
    ) -> Dict[str, str]:
        """
        Setup MSVC environment with specified configuration
        
        Args:
            config: MSVC environment configuration
            
        Returns:
            Environment variables after setup
            
        Raises:
            RuntimeError: If vcvarsall.bat not found or setup fails
            ValueError: If configuration is invalid
        """
        self._logger.info(
            f"Setting up MSVC environment for architecture: {config.architecture.value}"
        )

        # Validate configuration
        self._validate_config(config)

        # Save original environment
        self._original_environment = self._terminal_invoker.capture_environment()
        self._logger.debug("Saved original environment")

        # Find vcvarsall.bat
        self._vcvarsall_path = self._find_vcvarsall(config.vc_install_path)
        
        if not self._vcvarsall_path:
            error_msg = "vcvarsall.bat not found. Cannot setup MSVC environment."
            self._logger.error(error_msg)
            raise RuntimeError(error_msg)

        self._logger.info(f"Found vcvarsall.bat: {self._vcvarsall_path}")

        # Setup vcvarsall.bat
        self._setup_vcvarsall(config)

        # Capture environment after setup
        self._current_environment = self._terminal_invoker.capture_environment()
        self._is_setup = True

        self._logger.info("MSVC environment setup complete")
        return self._current_environment

    def setup_vcvarsall(
        self,
        architecture: MSVCArchitecture,
        platform_type: str = "desktop",
        spectre_mitigation: bool = False,
        windows_sdk_version: Optional[str] = None,
        vc_install_path: Optional[str] = None
    ) -> CommandResult:
        """
        Setup MSVC environment by invoking vcvarsall.bat
        
        Args:
            architecture: Target architecture
            platform_type: Platform type (desktop, uwp, store)
            spectre_mitigation: Enable Spectre mitigation
            windows_sdk_version: Specific Windows SDK version
            vc_install_path: Visual Studio installation path
            
        Returns:
            Command execution result
            
        Raises:
            FileNotFoundError: If vcvarsall.bat not found
            RuntimeError: If vcvarsall.bat execution fails
        """
        self._logger.info(
            f"Invoking vcvarsall.bat with architecture: {architecture.value}, "
            f"platform: {platform_type}, spectre: {spectre_mitigation}"
        )

        # Find vcvarsall.bat
        if not self._vcvarsall_path:
            self._vcvarsall_path = self._find_vcvarsall(vc_install_path)

        if not self._vcvarsall_path:
            error_msg = "vcvarsall.bat not found"
            self._logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        # Build arguments for vcvarsall.bat
        args = self._build_vcvarsall_args(
            architecture,
            platform_type,
            spectre_mitigation,
            windows_sdk_version
        )

        self._logger.debug(f"vcvarsall.bat arguments: {' '.join(args)}")

        # Execute vcvarsall.bat
        result = self._terminal_invoker.execute_batch_file(
            self._vcvarsall_path,
            args
        )

        # Check result
        if not result.success:
            error_msg = f"vcvarsall.bat execution failed: {result.stderr}"
            self._logger.error(error_msg)
            self._logger.error(f"Exit code: {result.exit_code}")
            raise RuntimeError(error_msg)

        # Set additional environment variables
        self._set_additional_environment_variables(
            architecture,
            platform_type,
            spectre_mitigation,
            windows_sdk_version
        )

        self._logger.info("vcvarsall.bat execution successful")
        return result

    def get_environment_variables(self) -> Dict[str, str]:
        """
        Get current MSVC environment variables
        
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
        Validate current MSVC environment
        
        Returns:
            Environment validation result
        """
        self._logger.info("Validating MSVC environment")

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

        # Check for cl.exe in PATH
        self._validate_cl_in_path(current_env, result)

        # Log validation result
        if result.is_valid:
            self._logger.info("MSVC environment validation passed")
        else:
            self._logger.error(
                f"MSVC environment validation failed: {len(result.errors)} errors, "
                f"{len(result.warnings)} warnings"
            )

        return result

    def _validate_config(self, config: MSVCEnvironmentConfig) -> None:
        """
        Validate MSVC environment configuration
        
        Args:
            config: Configuration to validate
            
        Raises:
            ValueError: If configuration is invalid
        """
        self._logger.debug("Validating MSVC environment configuration")

        # Validate architecture
        if config.architecture not in MSVCArchitecture:
            raise ValueError(
                f"Invalid architecture type: {type(config.architecture)}"
            )

        # Validate platform type
        valid_platforms = ["desktop", "uwp", "store"]
        if config.platform_type not in valid_platforms:
            raise ValueError(
                f"Invalid platform type: {config.platform_type}. "
                f"Valid types are: {', '.join(valid_platforms)}"
            )

        # Validate Windows SDK version format
        if config.windows_sdk_version:
            sdk_version = config.windows_sdk_version.strip()
            if not sdk_version.startswith("10.0."):
                raise ValueError(
                    f"Invalid Windows SDK version format: {config.windows_sdk_version}. "
                    "Expected format: 10.0.xxxxx"
                )

        self._logger.debug("Configuration validation passed")

    def _find_vcvarsall(self, vc_install_path: Optional[str] = None) -> Optional[str]:
        """
        Find vcvarsall.bat path
        
        Args:
            vc_install_path: Visual Studio installation path
            
        Returns:
            Path to vcvarsall.bat or None if not found
        """
        self._logger.debug("Searching for vcvarsall.bat")

        # If installation path is provided, use it
        if vc_install_path:
            vcvarsall_path = self._arch_mapper.get_vcvarsall_path(vc_install_path)
            if os.path.exists(vcvarsall_path):
                self._logger.debug(f"Found vcvarsall.bat at: {vcvarsall_path}")
                return vcvarsall_path

        # Try common installation paths
        common_paths = [
            # VS 2022
            os.path.join(
                os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                "Microsoft Visual Studio",
                "2022",
                "BuildTools",
                "VC",
                "Auxiliary",
                "Build",
                "vcvarsall.bat"
            ),
            os.path.join(
                os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                "Microsoft Visual Studio",
                "2022",
                "Community",
                "VC",
                "Auxiliary",
                "Build",
                "vcvarsall.bat"
            ),
            os.path.join(
                os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                "Microsoft Visual Studio",
                "2022",
                "Professional",
                "VC",
                "Auxiliary",
                "Build",
                "vcvarsall.bat"
            ),
            os.path.join(
                os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                "Microsoft Visual Studio",
                "2022",
                "Enterprise",
                "VC",
                "Auxiliary",
                "Build",
                "vcvarsall.bat"
            ),
            # VS 2019
            os.path.join(
                os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                "Microsoft Visual Studio",
                "2019",
                "BuildTools",
                "VC",
                "Auxiliary",
                "Build",
                "vcvarsall.bat"
            ),
            os.path.join(
                os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                "Microsoft Visual Studio",
                "2019",
                "Community",
                "VC",
                "Auxiliary",
                "Build",
                "vcvarsall.bat"
            ),
        ]

        for path in common_paths:
            if os.path.exists(path):
                self._logger.debug(f"Found vcvarsall.bat at: {path}")
                return path

        self._logger.warning("vcvarsall.bat not found in common paths")
        return None

    def _build_vcvarsall_args(
        self,
        architecture: MSVCArchitecture,
        platform_type: str,
        spectre_mitigation: bool,
        windows_sdk_version: Optional[str]
    ) -> List[str]:
        """
        Build arguments for vcvarsall.bat
        
        Args:
            architecture: Target architecture
            platform_type: Platform type
            spectre_mitigation: Enable Spectre mitigation
            windows_sdk_version: Windows SDK version
            
        Returns:
            List of arguments for vcvarsall.bat
        """
        args = []

        # Add architecture argument
        arch_arg = self._arch_mapper.get_vcvarsall_argument(architecture)
        args.append(arch_arg)

        # Add platform type argument
        if platform_type == "uwp":
            args.append("uwp")
        elif platform_type == "store":
            args.append("store")

        # Add Spectre mitigation argument
        if spectre_mitigation:
            args.append("spectre")

        # Add Windows SDK version argument
        if windows_sdk_version:
            args.append(f"-vcvars_ver={windows_sdk_version}")

        return args

    def _set_additional_environment_variables(
        self,
        architecture: MSVCArchitecture,
        platform_type: str,
        spectre_mitigation: bool,
        windows_sdk_version: Optional[str]
    ) -> None:
        """
        Set additional environment variables after vcvarsall.bat execution
        
        Args:
            architecture: Target architecture
            platform_type: Platform type
            spectre_mitigation: Spectre mitigation enabled
            windows_sdk_version: Windows SDK version
        """
        self._logger.debug("Setting additional environment variables")

        # Set Spectre mitigation variable
        if spectre_mitigation:
            os.environ["SPECTRE_MITIGATION"] = "1"
            self._logger.debug("Set SPECTRE_MITIGATION=1")

        # Set Windows SDK version if specified
        if windows_sdk_version:
            os.environ["WindowsSDKVersion"] = windows_sdk_version
            self._logger.debug(f"Set WindowsSDKVersion={windows_sdk_version}")

        # Set platform type variable
        os.environ["VSCMD_ARG_app_plat"] = platform_type
        self._logger.debug(f"Set VSCMD_ARG_app_plat={platform_type}")

        # Set host architecture variable
        os.environ["VSCMD_ARG_HOST_ARCH"] = architecture.host_architecture
        self._logger.debug(f"Set VSCMD_ARG_HOST_ARCH={architecture.host_architecture}")

        # Set target architecture variable
        os.environ["VSCMD_ARG_TGT_ARCH"] = architecture.target_architecture
        self._logger.debug(f"Set VSCMD_ARG_TGT_ARCH={architecture.target_architecture}")

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

        # Check INCLUDE paths
        if "INCLUDE" in env:
            include_paths = env["INCLUDE"].split(os.pathsep)
            for path in include_paths:
                if path and not os.path.exists(path):
                    result.invalid_paths.append(f"INCLUDE: {path}")
                    result.warnings.append(f"Invalid INCLUDE path: {path}")
                    self._logger.warning(f"Invalid INCLUDE path: {path}")

        # Check LIB paths
        if "LIB" in env:
            lib_paths = env["LIB"].split(os.pathsep)
            for path in lib_paths:
                if path and not os.path.exists(path):
                    result.invalid_paths.append(f"LIB: {path}")
                    result.warnings.append(f"Invalid LIB path: {path}")
                    self._logger.warning(f"Invalid LIB path: {path}")

        # Check LIBPATH paths
        if "LIBPATH" in env:
            libpath_paths = env["LIBPATH"].split(os.pathsep)
            for path in libpath_paths:
                if path and not os.path.exists(path):
                    result.invalid_paths.append(f"LIBPATH: {path}")
                    result.warnings.append(f"Invalid LIBPATH path: {path}")
                    self._logger.warning(f"Invalid LIBPATH path: {path}")

    def _validate_cl_in_path(
        self,
        env: Dict[str, str],
        result: EnvironmentValidationResult
    ) -> None:
        """
        Validate that cl.exe is in PATH
        
        Args:
            env: Environment variables
            result: Validation result to update
        """
        self._logger.debug("Validating cl.exe in PATH")

        if "PATH" not in env:
            result.errors.append("PATH environment variable not set")
            result.is_valid = False
            return

        path_dirs = env["PATH"].split(os.pathsep)
        cl_found = False

        for path_dir in path_dirs:
            cl_path = os.path.join(path_dir, "cl.exe")
            if os.path.exists(cl_path):
                cl_found = True
                self._logger.debug(f"Found cl.exe at: {cl_path}")
                break

        if not cl_found:
            result.errors.append("cl.exe not found in PATH")
            result.is_valid = False
            self._logger.error("cl.exe not found in PATH")

    def _setup_vcvarsall(self, config: MSVCEnvironmentConfig) -> None:
        """
        Setup vcvarsall.bat with configuration
        
        Args:
            config: MSVC environment configuration
        """
        self._logger.debug("Setting up vcvarsall.bat")

        # Build arguments
        args = self._build_vcvarsall_args(
            config.architecture,
            config.platform_type,
            config.spectre_mitigation,
            config.windows_sdk_version
        )

        # Execute vcvarsall.bat
        if not self._vcvarsall_path:
            raise RuntimeError("vcvarsall.bat path is not set")
            
        result = self._terminal_invoker.execute_batch_file(
            self._vcvarsall_path,
            args
        )

        # Check result
        if not result.success:
            error_msg = (
                f"vcvarsall.bat execution failed with exit code {result.exit_code}. "
                f"Error: {result.stderr}"
            )
            self._logger.error(error_msg)
            raise RuntimeError(error_msg)

        # Set additional environment variables
        self._set_additional_environment_variables(
            config.architecture,
            config.platform_type,
            config.spectre_mitigation,
            config.windows_sdk_version
        )

        self._logger.debug("vcvarsall.bat setup complete")
