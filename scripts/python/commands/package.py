"""
Package command - Distribution package creation

This module provides package command for creating distribution
packages including tarballs, installers, and package metadata.
"""

import argparse
import os
import json
from typing import Any, Dict, Optional

from core.logger import Logger
from core.exception_handler import BuildError
from core.terminal_invoker import TerminalInvoker
from core.terminal_detector import TerminalDetector
from cmake.cmake_wrapper import CMakeWrapper


class PackageCommand:
    """Create distribution packages.
    
    This command handles packaging including:
    - Multiple package formats (tarball, installer)
    - Package metadata generation
    - Package signing
    - Package integrity verification
    - Error handling
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize package command.
        
        Args:
            config: Configuration dictionary containing build settings
        """
        self.config = config
        self.logger = Logger("package", config.get("logging", {}))
        
        # Initialize terminal invoker
        terminal_detector = TerminalDetector()
        terminal = terminal_detector.get_default()
        if not terminal:
            raise BuildError("No terminal detected")
        
        self.terminal_invoker = TerminalInvoker(terminal)
        
        # Initialize CMake wrapper
        self.cmake_wrapper = CMakeWrapper(config)
    
    def execute(self, args: argparse.Namespace) -> int:
        """Execute package command.
        
        Args:
            args: Command-line arguments
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            self.logger.info("Starting package creation...")
            
            # Get configuration parameters
            build_dir = getattr(args, "build_dir", "build")
            package_type = getattr(args, "type", "zip")
            output_dir = getattr(args, "output", "packages")
            version = getattr(args, "version", None)
            sign = getattr(args, "sign", False)
            
            # Validate build directory exists
            if not os.path.exists(build_dir):
                raise BuildError(
                    f"Build directory does not exist: {build_dir}. "
                    "Run configure and compile commands first."
                )
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Build CMake package arguments
            cmake_args = self._build_cmake_args(
                build_dir=build_dir,
                package_type=package_type,
                output_dir=output_dir,
                version=version
            )
            
            # Execute CMake package
            self.logger.info(f"Creating {package_type} package...")
            self.logger.info(f"Output directory: {os.path.abspath(output_dir)}")
            
            result = self.cmake_wrapper.build(cmake_args)
            
            if result.return_code != 0:
                self.logger.error("Package creation failed")
                if result.stderr:
                    self.logger.error(f"Error output:\n{result.stderr}")
                raise BuildError(
                    "Package creation failed",
                    {
                        "return_code": result.return_code,
                        "stderr": result.stderr
                    }
                )
            
            # Generate package metadata
            metadata = self._generate_metadata(
                package_type=package_type,
                version=version
            )
            
            # Save package metadata
            metadata_file = os.path.join(output_dir, "package_metadata.json")
            self._save_metadata(metadata, metadata_file)
            
            # Sign package if requested
            if sign:
                self._sign_package(output_dir, package_type)
            
            # Verify package integrity
            self._verify_package(output_dir, package_type)
            
            self.logger.info("Package created successfully")
            return 0
            
        except BuildError as e:
            self.logger.error(f"Package creation failed: {e}")
            return 1
        except Exception as e:
            self.logger.error(f"Unexpected error during package creation: {e}")
            return 1
    
    def _build_cmake_args(
        self,
        build_dir: str,
        package_type: str,
        output_dir: str,
        version: Optional[str]
    ) -> list[str]:
        """Build CMake package arguments.
        
        Args:
            build_dir: Build directory
            package_type: Package type (zip, tar, installer)
            output_dir: Output directory
            version: Package version
            
        Returns:
            List of CMake arguments
        """
        args: list[str] = []
        
        # Add package command
        args.extend(["--build", build_dir, "--target", "package"])
        
        # Add package type
        args.extend(["--config", f"CPACK_GENERATOR={package_type}"])
        
        # Add output directory
        args.extend(["--config", f"CPACK_OUTPUT_DIRECTORY={output_dir}"])
        
        # Add version if specified
        if version:
            args.extend(["--config", f"CPACK_PACKAGE_VERSION={version}"])
        
        return args
    
    def _generate_metadata(
        self,
        package_type: str,
        version: Optional[str]
    ) -> Dict[str, Any]:
        """Generate package metadata.
        
        Args:
            package_type: Package type
            version: Package version
            
        Returns:
            Package metadata dictionary
        """
        # Get project configuration
        project_name = self.config.get("project_name", "OmniCppTemplate")
        project_version = version or self.config.get("project_version", "1.0.0")
        project_description = self.config.get("project_description", "")
        
        metadata: Dict[str, Any] = {
            "package_name": project_name,
            "package_version": project_version,
            "package_type": package_type,
            "package_description": project_description,
            "build_date": self._get_current_date(),
            "platform": self._detect_platform(),
            "architecture": self._detect_architecture()
        }
        
        return metadata
    
    def _save_metadata(
        self,
        metadata: Dict[str, Any],
        metadata_file: str
    ) -> None:
        """Save package metadata to file.
        
        Args:
            metadata: Package metadata
            metadata_file: Metadata file path
        """
        try:
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)
            
            self.logger.info(f"Package metadata saved to: {metadata_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save package metadata: {e}")
    
    def _sign_package(self, output_dir: str, package_type: str) -> None:
        """Sign package if configured.
        
        Args:
            output_dir: Output directory
            package_type: Package type
        """
        self.logger.info("Package signing not implemented")
        # TODO: Implement package signing
    
    def _verify_package(self, output_dir: str, package_type: str) -> None:
        """Verify package integrity.
        
        Args:
            output_dir: Output directory
            package_type: Package type
            
        Raises:
            BuildError: If verification fails
        """
        self.logger.info("Verifying package integrity...")
        
        # Look for package files
        package_files = self._find_package_files(output_dir, package_type)
        
        if not package_files:
            raise BuildError(
                f"No package files found in {output_dir}"
            )
        
        # Verify each package file
        for package_file in package_files:
            if not os.path.exists(package_file):
                raise BuildError(
                    f"Package file not found: {package_file}"
                )
            
            file_size = os.path.getsize(package_file)
            self.logger.info(f"Verified package: {package_file} ({file_size} bytes)")
    
    def _find_package_files(self, output_dir: str, package_type: str) -> list[str]:
        """Find package files in output directory.
        
        Args:
            output_dir: Output directory
            package_type: Package type
            
        Returns:
            List of package file paths
        """
        package_files: list[str] = []
        
        # Map package types to file extensions
        extensions = {
            "zip": [".zip"],
            "tar": [".tar.gz", ".tar.bz2", ".tar.xz"],
            "installer": [".exe", ".msi", ".dmg", ".deb", ".rpm"]
        }
        
        # Get expected extensions for package type
        expected_extensions = extensions.get(package_type, [])
        
        # Find matching files
        for filename in os.listdir(output_dir):
            for ext in expected_extensions:
                if filename.endswith(ext):
                    package_files.append(os.path.join(output_dir, filename))
                    break
        
        return package_files
    
    def _get_current_date(self) -> str:
        """Get current date in ISO format.
        
        Returns:
            Current date string
        """
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _detect_platform(self) -> str:
        """Detect current platform.
        
        Returns:
            Platform name
        """
        if os.name == "nt":
            return "windows"
        elif os.name == "posix":
            return "linux"
        else:
            return "unknown"
    
    def _detect_architecture(self) -> str:
        """Detect CPU architecture.
        
        Returns:
            Architecture name
        """
        import platform
        machine = platform.machine().lower()
        
        if "x86_64" in machine or "amd64" in machine:
            return "x64"
        elif "arm64" in machine or "aarch64" in machine:
            return "arm64"
        elif "i386" in machine or "i686" in machine:
            return "x86"
        else:
            return "unknown"
