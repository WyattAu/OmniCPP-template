"""
Install command - Install build artifacts

This module provides install command for installing build artifacts
to target directories, including component selection and verification.
"""

import argparse
import os
import shutil
from typing import Any, Dict, Optional

from core.logger import Logger
from core.exception_handler import BuildError, PermissionError
from core.terminal_invoker import TerminalInvoker
from core.terminal_detector import TerminalDetector
from cmake.cmake_wrapper import CMakeWrapper


class InstallCommand:
    """Install build artifacts.
    
    This command handles installation including:
    - Installation prefix configuration
    - Component selection
    - Installation verification
    - Uninstallation support
    - Permission handling
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize install command.
        
        Args:
            config: Configuration dictionary containing build settings
        """
        self.config = config
        self.logger = Logger("install", config.get("logging", {}))
        
        # Initialize terminal invoker
        terminal_detector = TerminalDetector()
        terminal = terminal_detector.get_default()
        if not terminal:
            raise BuildError("No terminal detected")
        
        self.terminal_invoker = TerminalInvoker(terminal)
        
        # Initialize CMake wrapper
        self.cmake_wrapper = CMakeWrapper(config)
    
    def execute(self, args: argparse.Namespace) -> int:
        """Execute install command.
        
        Args:
            args: Command-line arguments
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            self.logger.info("Starting installation...")
            
            # Get configuration parameters
            build_dir = getattr(args, "build_dir", "build")
            prefix = getattr(args, "prefix", None)
            component = getattr(args, "component", None)
            strip = getattr(args, "strip", False)
            uninstall = getattr(args, "uninstall", False)
            
            # Validate build directory exists
            if not os.path.exists(build_dir):
                raise BuildError(
                    f"Build directory does not exist: {build_dir}. "
                    "Run configure and compile commands first."
                )
            
            # Handle uninstallation
            if uninstall:
                return self._uninstall(build_dir, prefix)
            
            # Build CMake install arguments
            cmake_args = self._build_cmake_args(
                build_dir=build_dir,
                prefix=prefix,
                component=component,
                strip=strip
            )
            
            # Execute CMake install
            install_prefix = prefix or self._get_default_prefix()
            self.logger.info(f"Installing to: {install_prefix}")
            if component:
                self.logger.info(f"Installing component: {component}")
            
            result = self.cmake_wrapper.install(cmake_args)
            
            if result.return_code != 0:
                self.logger.error("Installation failed")
                if result.stderr:
                    self.logger.error(f"Error output:\n{result.stderr}")
                raise BuildError(
                    "Installation failed",
                    {
                        "return_code": result.return_code,
                        "stderr": result.stderr
                    }
                )
            
            # Verify installation
            self._verify_installation(install_prefix, component)
            
            self.logger.info("Installation completed successfully")
            return 0
            
        except (BuildError, PermissionError) as e:
            self.logger.error(f"Installation failed: {e}")
            return 1
        except Exception as e:
            self.logger.error(f"Unexpected error during installation: {e}")
            return 1
    
    def _get_default_prefix(self) -> str:
        """Get default installation prefix.
        
        Returns:
            Default installation prefix path
        """
        # Check config for default prefix
        config_prefix = self.config.get("install_prefix")
        if config_prefix:
            return config_prefix
        
        # Use platform-specific default
        if os.name == "nt":
            return os.path.join(os.environ.get("LOCALAPPDATA", ""), "OmniCpp")
        else:
            return "/usr/local"
    
    def _build_cmake_args(
        self,
        build_dir: str,
        prefix: Optional[str],
        component: Optional[str],
        strip: bool
    ) -> list[str]:
        """Build CMake install arguments.
        
        Args:
            build_dir: Build directory
            prefix: Installation prefix
            component: Component to install
            strip: Whether to strip binaries
            
        Returns:
            List of CMake arguments
        """
        args: list[str] = []
        
        # Add install prefix if specified
        if prefix:
            args.extend(["--prefix", prefix])
        
        # Add component if specified
        if component:
            args.extend(["--component", component])
        
        # Add strip flag if requested
        if strip:
            args.append("--strip")
        
        # Add build directory
        args.extend(["--build", build_dir])
        
        return args
    
    def _verify_installation(
        self,
        prefix: str,
        component: Optional[str]
    ) -> None:
        """Verify installation was successful.
        
        Args:
            prefix: Installation prefix
            component: Installed component
            
        Raises:
            BuildError: If verification fails
        """
        self.logger.info("Verifying installation...")
        
        # Check if prefix exists
        if not os.path.exists(prefix):
            raise BuildError(
                f"Installation prefix does not exist: {prefix}"
            )
        
        # Check for common installation directories
        expected_dirs = ["bin", "lib", "include"]
        found_dirs = []
        
        for dir_name in expected_dirs:
            dir_path = os.path.join(prefix, dir_name)
            if os.path.exists(dir_path):
                found_dirs.append(dir_name)  # type: ignore
                self.logger.debug(f"Found installation directory: {dir_path}")
        
        if not found_dirs:
            self.logger.warning(
                "No standard installation directories found. "
                "Installation may be incomplete."
            )
        else:
            self.logger.info(f"Verified installation directories: {', '.join(found_dirs)}")  # type: ignore
    
    def _uninstall(self, build_dir: str, prefix: Optional[str]) -> int:
        """Uninstall previously installed artifacts.
        
        Args:
            build_dir: Build directory
            prefix: Installation prefix
            
        Returns:
            Exit code
        """
        try:
            self.logger.info("Uninstalling...")
            
            install_prefix = prefix or self._get_default_prefix()
            
            # Check if prefix exists
            if not os.path.exists(install_prefix):
                self.logger.warning(
                    f"Installation prefix does not exist: {install_prefix}"
                )
                return 0
            
            # Remove installation directories
            dirs_to_remove = ["bin", "lib", "include", "share"]
            removed_count = 0
            
            for dir_name in dirs_to_remove:
                dir_path = os.path.join(install_prefix, dir_name)
                if os.path.exists(dir_path):
                    try:
                        shutil.rmtree(dir_path)
                        self.logger.info(f"Removed: {dir_path}")
                        removed_count += 1
                    except PermissionError as e:
                        raise PermissionError(
                            f"Permission denied removing {dir_path}",
                            {"path": dir_path, "error": str(e)}
                        )
            
            if removed_count == 0:
                self.logger.warning("No installation directories found to remove")
            else:
                self.logger.info(f"Uninstalled {removed_count} directories")
            
            return 0
            
        except PermissionError as e:
            self.logger.error(f"Uninstall failed: {e}")
            return 1
        except Exception as e:
            self.logger.error(f"Unexpected error during uninstall: {e}")
            return 1
