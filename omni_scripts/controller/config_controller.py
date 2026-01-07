"""
Configuration controller for OmniCppController.

This module provides the configuration controller that handles
configuration-related commands such as setting up build configurations,
managing presets, and configuring toolchains.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Optional

from omni_scripts.controller.base import BaseController
from omni_scripts.exceptions import ControllerError


class ConfigController(BaseController):
    """Controller for configuration-related commands.

    This controller handles:
    - Configuring build systems (CMake, Conan, etc.)
    - Managing build presets
    - Setting up toolchains
    - Managing configuration files

    Attributes:
        logger: Logger instance for the controller.
        args: Parsed command-line arguments.
    """

    def __init__(self, args: argparse.Namespace) -> None:
        """Initialize the configuration controller.

        Args:
            args: Parsed command-line arguments.
        """
        super().__init__(args)
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute(self) -> int:
        """Execute the configuration command.

        Returns:
            Exit code (0 for success, non-zero for failure).
        """
        self.log_command_start("configure")

        try:
            # Validate arguments
            self._validate_arguments()

            # Perform configuration
            result = self._configure()

            if result:
                self.log_command_success("configure")
                return 0
            else:
                self.logger.error("Configuration failed")
                return 1

        except ControllerError as e:
            self.log_command_error("configure", e)
            return e.exit_code
        except Exception as e:
            self.logger.exception(f"Unexpected error during configuration: {e}")
            return 1

    def _validate_arguments(self) -> None:
        """Validate command-line arguments.

        Raises:
            ControllerError: If arguments are invalid.
        """
        # Validate generator if specified
        if hasattr(self.args, "generator") and self.args.generator:
            valid_generators = ["Ninja", "Unix Makefiles", "Visual Studio 17 2022"]
            if self.args.generator not in valid_generators:
                raise ControllerError(
                    message=f"Invalid generator '{self.args.generator}'. Valid generators are: {', '.join(valid_generators)}",
                    command="configure",
                    context={"generator": self.args.generator, "valid_generators": valid_generators},
                    exit_code=2,
                )

        # Validate toolchain if specified
        if hasattr(self.args, "toolchain") and self.args.toolchain:
            toolchain_path = Path(self.args.toolchain)
            if not toolchain_path.exists():
                raise ControllerError(
                    message=f"Toolchain file not found: {self.args.toolchain}",
                    command="configure",
                    context={"toolchain": self.args.toolchain},
                    exit_code=3,
                )

        # Validate preset if specified
        if hasattr(self.args, "preset") and self.args.preset:
            preset_path = self.get_config_path(f"CMakePresets.json")
            if not preset_path.exists():
                raise ControllerError(
                    message=f"CMakePresets.json not found: {preset_path}",
                    command="configure",
                    context={"preset": self.args.preset, "preset_path": str(preset_path)},
                    exit_code=3,
                )

    def _configure(self) -> bool:
        """Perform the configuration.

        Returns:
            True if configuration succeeded, False otherwise.
        """
        # Check which configuration method to use
        if hasattr(self.args, "preset") and self.args.preset:
            return self._configure_with_preset()
        elif hasattr(self.args, "generator") and self.args.generator:
            return self._configure_with_generator()
        elif hasattr(self.args, "toolchain") and self.args.toolchain:
            return self._configure_with_toolchain()
        else:
            self.logger.error("No configuration method specified")
            return False

    def _configure_with_preset(self) -> bool:
        """Configure using a CMake preset.

        Returns:
            True if configuration succeeded, False otherwise.
        """
        preset = self.args.preset
        self.logger.info(f"Configuring with preset: {preset}")

        # Import CMake wrapper
        try:
            from omni_scripts.build_system.cmake import CMakeWrapper

            cmake = CMakeWrapper()
            result = cmake.configure(preset=preset)

            if result:
                self.logger.info(f"Successfully configured with preset: {preset}")
                return True
            else:
                self.logger.error(f"Failed to configure with preset: {preset}")
                return False

        except ImportError as e:
            self.logger.error(f"CMakeWrapper not available: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error configuring with preset: {e}")
            return False

    def _configure_with_generator(self) -> bool:
        """Configure using a specific generator.

        Returns:
            True if configuration succeeded, False otherwise.
        """
        generator = self.args.generator
        self.logger.info(f"Configuring with generator: {generator}")

        # Import CMake wrapper
        try:
            from omni_scripts.build_system.cmake import CMakeWrapper

            cmake = CMakeWrapper()
            result = cmake.configure(generator=generator)

            if result:
                self.logger.info(f"Successfully configured with generator: {generator}")
                return True
            else:
                self.logger.error(f"Failed to configure with generator: {generator}")
                return False

        except ImportError as e:
            self.logger.error(f"CMakeWrapper not available: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error configuring with generator: {e}")
            return False

    def _configure_with_toolchain(self) -> bool:
        """Configure using a specific toolchain.

        Returns:
            True if configuration succeeded, False otherwise.
        """
        toolchain = self.args.toolchain
        self.logger.info(f"Configuring with toolchain: {toolchain}")

        # Import CMake wrapper
        try:
            from omni_scripts.build_system.cmake import CMakeWrapper

            cmake = CMakeWrapper()
            result = cmake.configure(toolchain=toolchain)

            if result:
                self.logger.info(f"Successfully configured with toolchain: {toolchain}")
                return True
            else:
                self.logger.error(f"Failed to configure with toolchain: {toolchain}")
                return False

        except ImportError as e:
            self.logger.error(f"CMakeWrapper not available: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error configuring with toolchain: {e}")
            return False


__all__ = [
    "ConfigController",
]
