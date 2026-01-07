"""
CMake presets management

This module provides comprehensive CMake presets file generation and management
including CMakePresets.json and CMakeUserPresets.json with proper
validation and error handling.
"""

import json
from pathlib import Path
from typing import Any, Optional

from core.exception_handler import ConfigurationError
from core.logger import Logger


from dataclasses import dataclass


@dataclass
class PresetInfo:
    """CMake preset information data class."""
    
    name: str
    generator: str
    toolchain: str
    build_type: str
    cache_vars: dict[str, str]
    environment: dict[str, str]
    description: Optional[str] = None


class PresetsManager:
    """Manage CMake presets files.
    
    This class provides methods for generating, reading, and manipulating
    CMake presets files (CMakePresets.json and CMakeUserPresets.json)
    with proper validation and error handling.
    """
    
    def __init__(self, source_dir: str, logger: Optional[Logger] = None) -> None:
        """Initialize presets manager.
        
        Args:
            source_dir: Source directory for presets files
            logger: Logger instance for logging operations
            
        Raises:
            ConfigurationError: If source directory is invalid
        """
        self.source_dir = Path(source_dir).resolve()
        self.presets_file = self.source_dir / "CMakePresets.json"
        self.user_presets_file = self.source_dir / "CMakeUserPresets.json"
        self.logger = logger or Logger("PresetsManager", {
            "level": "INFO",
            "console_handler_enabled": True,
            "file_handler_enabled": False
        })
        
        # Validate source directory
        if not self.source_dir.exists():
            self.logger.warning(f"Source directory does not exist: {self.source_dir}")
        
        self.logger.info(f"Presets manager initialized for: {self.source_dir}")
    
    def generate(
        self,
        configs: list[dict[str, Any]],
        user_presets: Optional[list[dict[str, Any]]] = None
    ) -> None:
        """Generate CMake presets file.
        
        Args:
            configs: List of build configuration dictionaries
            user_presets: Optional list of user preset dictionaries
            
        Raises:
            ConfigurationError: If generation fails
        """
        self.logger.info(f"Generating CMake presets with {len(configs)} configurations")
        
        try:
            # Build presets structure
            presets_data = {
                "version": 3,
                "cmakeMinimumRequired": "3.15",
                "include": [],
                "configurePresets": [],
                "buildPresets": [],
                "testPresets": [],
                "packagePresets": []
            }
            
            # Add configure presets
            for config in configs:
                preset = self._build_configure_preset(config)
                presets_data["configurePresets"].append(preset)
                
                # Add corresponding build preset
                build_preset = self._build_build_preset(config)
                presets_data["buildPresets"].append(build_preset)
                
                # Add corresponding test preset
                test_preset = self._build_test_preset(config)
                presets_data["testPresets"].append(test_preset)
            
            # Write presets file
            self._write_presets_file(self.presets_file, presets_data)
            
            # Write user presets if provided
            if user_presets:
                user_presets_data = {
                    "version": 3,
                    "cmakeMinimumRequired": "3.15",
                    "include": [],
                    "configurePresets": []
                }
                
                for user_config in user_presets:
                    user_preset = self._build_configure_preset(user_config)
                    user_presets_data["configurePresets"].append(user_preset)
                
                self._write_presets_file(self.user_presets_file, user_presets_data)
            
            self.logger.info("CMake presets generated successfully")
        except Exception as e:
            self.logger.error(f"Failed to generate presets: {e}")
            raise ConfigurationError(
                f"Failed to generate CMake presets: {e}",
                {"source_dir": str(self.source_dir)}
            )
    
    def _build_configure_preset(self, config: dict[str, Any]) -> dict[str, Any]:
        """Build configure preset from configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Configure preset dictionary
        """
        preset = {
            "name": config.get("name", "default"),
            "displayName": config.get("display_name", config.get("name", "Default")),
            "description": config.get("description", ""),
            "generator": config.get("generator", "Ninja"),
            "binaryDir": config.get("binary_dir", "${sourceDir}/build/${presetName}")
        }
        
        # Add toolchain file if specified
        if "toolchain_file" in config:
            preset["toolchainFile"] = config["toolchain_file"]
        
        # Add cache variables
        if "cache_vars" in config:
            preset["cacheVariables"] = config["cache_vars"]
        
        # Add environment variables
        if "environment" in config:
            preset["environment"] = config["environment"]
        
        # Add inherit from if specified
        if "inherits" in config:
            preset["inherits"] = config["inherits"]
        
        return preset
    
    def _build_build_preset(self, config: dict[str, Any]) -> dict[str, Any]:
        """Build build preset from configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Build preset dictionary
        """
        preset = {
            "name": config.get("name", "default"),
            "displayName": config.get("display_name", config.get("name", "Default")),
            "description": config.get("description", ""),
            "configurePreset": config.get("name", "default")
        }
        
        # Add build targets if specified
        if "targets" in config:
            preset["targets"] = config["targets"]
        
        # Add configuration if specified
        if "build_type" in config:
            preset["configuration"] = config["build_type"]
        
        # Add inherit from if specified
        if "inherits" in config:
            preset["inherits"] = config["inherits"]
        
        return preset
    
    def _build_test_preset(self, config: dict[str, Any]) -> dict[str, Any]:
        """Build test preset from configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Test preset dictionary
        """
        preset = {
            "name": config.get("name", "default"),
            "displayName": config.get("display_name", config.get("name", "Default")),
            "description": config.get("description", ""),
            "configurePreset": config.get("name", "default")
        }
        
        # Add configuration if specified
        if "build_type" in config:
            preset["configuration"] = config["build_type"]
        
        # Add inherit from if specified
        if "inherits" in config:
            preset["inherits"] = config["inherits"]
        
        return preset
    
    def _write_presets_file(self, file_path: Path, data: dict[str, Any]) -> None:
        """Write presets file with proper formatting.
        
        Args:
            file_path: Path to presets file
            data: Presets data to write
        """
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write with proper formatting
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, sort_keys=False)
            f.write('\n')  # Add trailing newline
        
        self.logger.debug(f"Wrote presets file: {file_path}")
    
    def get_preset(self, name: str) -> Optional[PresetInfo]:
        """Get preset by name.
        
        Args:
            name: Preset name
            
        Returns:
            PresetInfo object or None if not found
        """
        presets_data = self._load_presets_file(self.presets_file)
        if not presets_data:
            return None
        
        for preset in presets_data.get("configurePresets", []):
            if preset.get("name") == name:
                return self._preset_to_info(preset)
        
        return None
    
    def list_presets(self) -> list[PresetInfo]:
        """List all configure presets.
        
        Returns:
            List of PresetInfo objects
        """
        presets: list[PresetInfo] = []
        
        presets_data = self._load_presets_file(self.presets_file)
        if not presets_data:
            return presets
        
        for preset in presets_data.get("configurePresets", []):
            presets.append(self._preset_to_info(preset))
        
        self.logger.debug(f"Found {len(presets)} presets")
        return presets
    
    def _preset_to_info(self, preset: dict[str, Any]) -> PresetInfo:
        """Convert preset dictionary to PresetInfo.
        
        Args:
            preset: Preset dictionary
            
        Returns:
            PresetInfo object
        """
        return PresetInfo(
            name=preset.get("name", ""),
            generator=preset.get("generator", ""),
            toolchain=preset.get("toolchainFile", ""),
            build_type=preset.get("cacheVariables", {}).get("CMAKE_BUILD_TYPE", "Release"),
            cache_vars=preset.get("cacheVariables", {}),
            environment=preset.get("environment", {}),
            description=preset.get("description")
        )
    
    def _load_presets_file(self, file_path: Path) -> Optional[dict[str, Any]]:
        """Load presets file.
        
        Args:
            file_path: Path to presets file
            
        Returns:
            Presets data dictionary or None if file doesn't exist
        """
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load presets file {file_path}: {e}")
            return None
    
    def create_preset(self, preset: PresetInfo) -> None:
        """Create new preset.
        
        Args:
            preset: PresetInfo object
            
        Raises:
            ConfigurationError: If preset creation fails
        """
        self.logger.info(f"Creating preset: {preset.name}")
        
        # Load existing presets
        presets_data = self._load_presets_file(self.presets_file)
        if not presets_data:
            presets_data = {
                "version": 3,
                "cmakeMinimumRequired": "3.15",
                "include": [],
                "configurePresets": [],
                "buildPresets": [],
                "testPresets": []
            }
        
        # Build preset dictionary
        preset_dict = {
            "name": preset.name,
            "displayName": preset.name,
            "description": preset.description or "",
            "generator": preset.generator,
            "binaryDir": "${sourceDir}/build/${presetName}"
        }
        
        # Add toolchain file if specified
        if preset.toolchain:
            preset_dict["toolchainFile"] = preset.toolchain
        
        # Add cache variables
        if preset.cache_vars:
            preset_dict["cacheVariables"] = preset.cache_vars
        
        # Add environment variables
        if preset.environment:
            preset_dict["environment"] = preset.environment
        
        # Check if preset already exists
        existing_index = None
        for i, existing_preset in enumerate(presets_data.get("configurePresets", [])):
            if existing_preset.get("name") == preset.name:
                existing_index = i
                break
        
        # Update or add preset
        if existing_index is not None:
            presets_data["configurePresets"][existing_index] = preset_dict
            self.logger.debug(f"Updated existing preset: {preset.name}")
        else:
            presets_data["configurePresets"].append(preset_dict)
            self.logger.debug(f"Added new preset: {preset.name}")
        
        # Write presets file
        self._write_presets_file(self.presets_file, presets_data)
    
    def remove_preset(self, name: str) -> bool:
        """Remove preset by name.
        
        Args:
            name: Preset name to remove
            
        Returns:
            True if preset was removed, False if not found
        """
        self.logger.info(f"Removing preset: {name}")
        
        presets_data = self._load_presets_file(self.presets_file)
        if not presets_data:
            return False
        
        # Find and remove preset
        configure_presets = presets_data.get("configurePresets", [])
        original_count = len(configure_presets)
        
        presets_data["configurePresets"] = [
            p for p in configure_presets if p.get("name") != name
        ]
        
        if len(presets_data["configurePresets"]) < original_count:
            # Also remove corresponding build and test presets
            presets_data["buildPresets"] = [
                p for p in presets_data.get("buildPresets", [])
                if p.get("name") != name
            ]
            presets_data["testPresets"] = [
                p for p in presets_data.get("testPresets", [])
                if p.get("name") != name
            ]
            
            # Write presets file
            self._write_presets_file(self.presets_file, presets_data)
            self.logger.info(f"Removed preset: {name}")
            return True
        
        return False
    
    def validate_presets(self) -> list[str]:
        """Validate presets file and return list of issues.
        
        Returns:
            List of validation issue messages
        """
        issues: list[str] = []
        
        presets_data = self._load_presets_file(self.presets_file)
        if not presets_data:
            issues.append("CMakePresets.json does not exist or is invalid")
            return issues
        
        # Validate version
        version = presets_data.get("version")
        if version not in [1, 2, 3]:
            issues.append(f"Invalid presets version: {version}")
        
        # Validate configure presets
        preset_names = set()
        for preset in presets_data.get("configurePresets", []):
            name = preset.get("name")
            if not name:
                issues.append("Found preset without name")
                continue
            
            # Check for duplicate names
            if name in preset_names:
                issues.append(f"Duplicate preset name: {name}")
            preset_names.add(name)
            
            # Validate required fields
            if "generator" not in preset:
                issues.append(f"Preset '{name}' missing generator")
            
            # Validate inherits references
            if "inherits" in preset:
                inherits = preset["inherits"]
                if isinstance(inherits, str) and inherits not in preset_names:
                    issues.append(f"Preset '{name}' inherits from non-existent preset: {inherits}")
        
        # Validate build presets
        for preset in presets_data.get("buildPresets", []):
            name = preset.get("name")
            if not name:
                issues.append("Found build preset without name")
                continue
            
            # Validate configurePreset reference
            if "configurePreset" in preset:
                configure_preset = preset["configurePreset"]
                if configure_preset not in preset_names:
                    issues.append(f"Build preset '{name}' references non-existent configure preset: {configure_preset}")
        
        # Validate test presets
        for preset in presets_data.get("testPresets", []):
            name = preset.get("name")
            if not name:
                issues.append("Found test preset without name")
                continue
            
            # Validate configurePreset reference
            if "configurePreset" in preset:
                configure_preset = preset["configurePreset"]
                if configure_preset not in preset_names:
                    issues.append(f"Test preset '{name}' references non-existent configure preset: {configure_preset}")
        
        if not issues:
            self.logger.info("Presets validation passed")
        else:
            self.logger.warning(f"Presets validation found {len(issues)} issues")
        
        return issues
    
    def get_default_preset(self) -> Optional[str]:
        """Get default preset name.
        
        Returns:
            Default preset name or None if not found
        """
        presets_data = self._load_presets_file(self.presets_file)
        if not presets_data:
            return None
        
        # Look for preset with "hidden": false and no inherits
        for preset in presets_data.get("configurePresets", []):
            if not preset.get("hidden", False) and "inherits" not in preset:
                return preset.get("name")
        
        # Return first preset if no default found
        configure_presets = presets_data.get("configurePresets", [])
        if configure_presets:
            return configure_presets[0].get("name")
        
        return None
