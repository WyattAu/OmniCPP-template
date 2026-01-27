"""
Unit tests for CompilerFactory

Tests compiler factory functionality including:
- Detector registration
- Compiler creation
- Compiler selection
- Caching
- Error handling
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import sys
import os

# Add scripts/python to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "python"))

from compilers.compiler_factory import (
    CompilerFactory,
    CompilerRequirements
)
from compilers.msvc_detector import (
    CompilerType,
    Architecture,
    CompilerInfo,
    VersionInfo,
    CapabilityInfo,
    EnvironmentInfo,
    ICompilerDetector,
    ValidationResult
)


class MockCompilerDetector(ICompilerDetector):
    """Mock compiler detector for testing"""
    
    def __init__(self, compilers: list[CompilerInfo] | None = None):
        self._compilers = compilers or []
        self.detect_called = False
        self.detect_version_called = False
        self.detect_capabilities_called = False
        self.validate_called = False
    
    def detect(self) -> list[CompilerInfo]:
        """Detect compilers (mock)"""
        self.detect_called = True
        return self._compilers
    
    def detect_version(self, compiler_path: str) -> VersionInfo | None:
        """Detect version (mock)"""
        self.detect_version_called = True
        return VersionInfo(major=19, minor=40, patch=0)
    
    def detect_capabilities(self, compiler_path: str) -> CapabilityInfo:
        """Detect capabilities (mock)"""
        self.detect_capabilities_called = True
        return CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            modules=True,
            coroutines=True,
            concepts=True,
            ranges=True,
            std_format=True
        )
    
    def validate(self, compiler_info: CompilerInfo) -> ValidationResult:
        """Validate compiler (mock)"""
        self.validate_called = True
        return ValidationResult(
            is_valid=True,
            errors=[],
            warnings=[]
        )


class TestCompilerFactory(unittest.TestCase):
    """Test cases for CompilerFactory"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.factory = CompilerFactory()
        self.mock_detector = MockCompilerDetector()
    
    def test_register_detector_success(self):
        """Test successful detector registration"""
        # Act
        self.factory.register_detector("test_compiler", self.mock_detector)
        
        # Assert
        self.assertIn("test_compiler", self.factory._detectors)
        self.assertEqual(
            self.factory._detectors["test_compiler"],
            self.mock_detector
        )
    
    def test_register_detector_empty_type(self):
        """Test detector registration with empty type"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.factory.register_detector("", self.mock_detector)
        
        self.assertIn("Compiler type cannot be empty", str(context.exception))
    
    def test_register_detector_none_detector(self):
        """Test detector registration with None detector"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.factory.register_detector("test_compiler", None)
        
        self.assertIn("Detector cannot be None", str(context.exception))
    
    def test_create_compiler_success(self):
        """Test successful compiler creation"""
        # Arrange
        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MSVC,
            version=VersionInfo(major=19, minor=40, patch=0),
            path="C:\\Program Files\\Microsoft Visual Studio\\2022\\VC\\Tools\\MSVC\\14.40.33811\\bin\\Hostx64\\x64\\cl.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="C:\\Program Files\\Microsoft Visual Studio\\2022")
        )
        detector = MockCompilerDetector([compiler_info])
        self.factory.register_detector("msvc", detector)
        
        # Act
        result = self.factory.create_compiler("msvc", "x64")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.compiler_type, CompilerType.MSVC)
        self.assertEqual(result.architecture, Architecture.X64)
        self.assertEqual(result.version.major, 19)
        self.assertTrue(detector.detect_called)
    
    def test_create_compiler_cache_hit(self):
        """Test compiler creation with cache hit"""
        # Arrange
        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MSVC,
            version=VersionInfo(major=19, minor=40, patch=0),
            path="C:\\cl.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="C:\\")
        )
        detector = MockCompilerDetector([compiler_info])
        self.factory.register_detector("msvc", detector)
        
        # Pre-populate cache
        self.factory._cache["msvc_x64"] = compiler_info
        
        # Act
        result = self.factory.create_compiler("msvc", "x64")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result, compiler_info)
        self.assertFalse(detector.detect_called)  # Should not call detect due to cache
    
    def test_create_compiler_no_detector(self):
        """Test compiler creation with no detector registered"""
        # Act
        result = self.factory.create_compiler("unknown", "x64")
        
        # Assert
        self.assertIsNone(result)
    
    def test_create_compiler_no_compilers_detected(self):
        """Test compiler creation when no compilers are detected"""
        # Arrange
        detector = MockCompilerDetector([])
        self.factory.register_detector("msvc", detector)
        
        # Act
        result = self.factory.create_compiler("msvc", "x64")
        
        # Assert
        self.assertIsNone(result)
    
    def test_create_compiler_no_matching_architecture(self):
        """Test compiler creation when no matching architecture found"""
        # Arrange
        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MSVC,
            version=VersionInfo(major=19, minor=40, patch=0),
            path="C:\\cl.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="C:\\")
        )
        detector = MockCompilerDetector([compiler_info])
        self.factory.register_detector("msvc", detector)
        
        # Act
        result = self.factory.create_compiler("msvc", "x86")
        
        # Assert
        self.assertIsNone(result)
    
    def test_create_compiler_invalid_architecture(self):
        """Test compiler creation with invalid architecture"""
        # Arrange
        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MSVC,
            version=VersionInfo(major=19, minor=40, patch=0),
            path="C:\\cl.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="C:\\")
        )
        detector = MockCompilerDetector([compiler_info])
        self.factory.register_detector("msvc", detector)
        
        # Act
        result = self.factory.create_compiler("msvc", "invalid_arch")
        
        # Assert
        self.assertIsNone(result)
    
    def test_create_compiler_selects_best_version(self):
        """Test that create_compiler selects highest version"""
        # Arrange
        compilers = [
            CompilerInfo(
                compiler_type=CompilerType.MSVC,
                version=VersionInfo(major=19, minor=28, patch=0),
                path="C:\\cl_old.exe",
                architecture=Architecture.X64,
                capabilities=CapabilityInfo(),
                environment=EnvironmentInfo(path="C:\\")
            ),
            CompilerInfo(
                compiler_type=CompilerType.MSVC,
                version=VersionInfo(major=19, minor=40, patch=0),
                path="C:\\cl_new.exe",
                architecture=Architecture.X64,
                capabilities=CapabilityInfo(),
                environment=EnvironmentInfo(path="C:\\")
            )
        ]
        detector = MockCompilerDetector(compilers)
        self.factory.register_detector("msvc", detector)
        
        # Act
        result = self.factory.create_compiler("msvc", "x64")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.version.major, 19)
        self.assertEqual(result.version.minor, 40)
        self.assertEqual(result.path, "C:\\cl_new.exe")
    
    def test_get_available_compilers(self):
        """Test getting all available compilers"""
        # Arrange
        msvc_compiler = CompilerInfo(
            compiler_type=CompilerType.MSVC,
            version=VersionInfo(major=19, minor=40, patch=0),
            path="C:\\cl.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="C:\\")
        )
        msvc_detector = MockCompilerDetector([msvc_compiler])
        self.factory.register_detector("msvc", msvc_detector)
        
        mingw_compiler = CompilerInfo(
            compiler_type=CompilerType.MINGW_GCC,
            version=VersionInfo(major=13, minor=2, patch=0),
            path="C:\\mingw64\\bin\\g++.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="C:\\mingw64")
        )
        mingw_detector = MockCompilerDetector([mingw_compiler])
        self.factory.register_detector("mingw_gcc", mingw_detector)
        
        # Act
        result = self.factory.get_available_compilers()
        
        # Assert
        self.assertIn("msvc", result)
        self.assertIn("mingw_gcc", result)
        self.assertEqual(len(result["msvc"]), 1)
        self.assertEqual(len(result["mingw_gcc"]), 1)
        self.assertEqual(result["msvc"][0].compiler_type, CompilerType.MSVC)
        self.assertEqual(result["mingw_gcc"][0].compiler_type, CompilerType.MINGW_GCC)
    
    def test_select_best_compiler_with_type(self):
        """Test selecting best compiler with specific type"""
        # Arrange
        compilers = [
            CompilerInfo(
                compiler_type=CompilerType.MSVC,
                version=VersionInfo(major=19, minor=40, patch=0),
                path="C:\\cl.exe",
                architecture=Architecture.X64,
                capabilities=CapabilityInfo(),
                environment=EnvironmentInfo(path="C:\\")
            )
        ]
        detector = MockCompilerDetector(compilers)
        self.factory.register_detector("msvc", detector)
        
        requirements = CompilerRequirements(
            compiler_type=CompilerType.MSVC,
            architecture=Architecture.X64
        )
        
        # Act
        result = self.factory.select_best_compiler(requirements)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.compiler_type, CompilerType.MSVC)
        self.assertEqual(result.architecture, Architecture.X64)
    
    def test_select_best_compiler_with_capabilities(self):
        """Test selecting best compiler with capability requirements"""
        # Arrange
        compilers = [
            CompilerInfo(
                compiler_type=CompilerType.MSVC,
                version=VersionInfo(major=19, minor=40, patch=0),
                path="C:\\cl.exe",
                architecture=Architecture.X64,
                capabilities=CapabilityInfo(
                    cpp23=True,
                    cpp20=True,
                    cpp17=True,
                    modules=True
                ),
                environment=EnvironmentInfo(path="C:\\")
            ),
            CompilerInfo(
                compiler_type=CompilerType.MSVC,
                version=VersionInfo(major=19, minor=14, patch=0),
                path="C:\\cl_old.exe",
                architecture=Architecture.X64,
                capabilities=CapabilityInfo(
                    cpp17=True,
                    cpp14=True,
                    modules=False
                ),
                environment=EnvironmentInfo(path="C:\\")
            )
        ]
        detector = MockCompilerDetector(compilers)
        self.factory.register_detector("msvc", detector)
        
        requirements = CompilerRequirements(
            compiler_type=CompilerType.MSVC,
            architecture=Architecture.X64,
            required_capabilities=["cpp23", "modules"]
        )
        
        # Act
        result = self.factory.select_best_compiler(requirements)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.version.major, 19)
        self.assertEqual(result.version.minor, 40)
        self.assertTrue(result.capabilities.cpp23)
        self.assertTrue(result.capabilities.modules)
    
    def test_select_best_compiler_with_version(self):
        """Test selecting best compiler with version preference"""
        # Arrange
        compilers = [
            CompilerInfo(
                compiler_type=CompilerType.MSVC,
                version=VersionInfo(major=19, minor=40, patch=0),
                path="C:\\cl.exe",
                architecture=Architecture.X64,
                capabilities=CapabilityInfo(),
                environment=EnvironmentInfo(path="C:\\")
            ),
            CompilerInfo(
                compiler_type=CompilerType.MSVC,
                version=VersionInfo(major=19, minor=28, patch=0),
                path="C:\\cl_old.exe",
                architecture=Architecture.X64,
                capabilities=CapabilityInfo(),
                environment=EnvironmentInfo(path="C:\\")
            )
        ]
        detector = MockCompilerDetector(compilers)
        self.factory.register_detector("msvc", detector)
        
        requirements = CompilerRequirements(
            compiler_type=CompilerType.MSVC,
            architecture=Architecture.X64,
            preferred_version="19.28.0"
        )
        
        # Act
        result = self.factory.select_best_compiler(requirements)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.version.major, 19)
        self.assertEqual(result.version.minor, 28)
        self.assertEqual(result.path, "C:\\cl_old.exe")
    
    def test_select_best_compiler_no_match(self):
        """Test selecting best compiler when no match found"""
        # Arrange
        compilers = [
            CompilerInfo(
                compiler_type=CompilerType.MSVC,
                version=VersionInfo(major=19, minor=40, patch=0),
                path="C:\\cl.exe",
                architecture=Architecture.X64,
                capabilities=CapabilityInfo(),
                environment=EnvironmentInfo(path="C:\\")
            )
        ]
        detector = MockCompilerDetector(compilers)
        self.factory.register_detector("msvc", detector)
        
        requirements = CompilerRequirements(
            compiler_type=CompilerType.MSVC,
            architecture=Architecture.X86  # No x86 compiler available
        )
        
        # Act
        result = self.factory.select_best_compiler(requirements)
        
        # Assert
        self.assertIsNone(result)
    
    def test_select_best_compiler_all_types(self):
        """Test selecting best compiler from all types"""
        # Arrange
        msvc_compilers = [
            CompilerInfo(
                compiler_type=CompilerType.MSVC,
                version=VersionInfo(major=19, minor=40, patch=0),
                path="C:\\cl.exe",
                architecture=Architecture.X64,
                capabilities=CapabilityInfo(),
                environment=EnvironmentInfo(path="C:\\")
            )
        ]
        msvc_detector = MockCompilerDetector(msvc_compilers)
        self.factory.register_detector("msvc", msvc_detector)
        
        mingw_compilers = [
            CompilerInfo(
                compiler_type=CompilerType.MINGW_GCC,
                version=VersionInfo(major=13, minor=2, patch=0),
                path="C:\\g++.exe",
                architecture=Architecture.X64,
                capabilities=CapabilityInfo(),
                environment=EnvironmentInfo(path="C:\\mingw64")
            )
        ]
        mingw_detector = MockCompilerDetector(mingw_compilers)
        self.factory.register_detector("mingw_gcc", mingw_detector)
        
        requirements = CompilerRequirements(
            architecture=Architecture.X64
        )
        
        # Act
        result = self.factory.select_best_compiler(requirements)
        
        # Assert
        self.assertIsNotNone(result)
        # Should return highest version compiler
        self.assertIn(result.compiler_type, [CompilerType.MSVC, CompilerType.MINGW_GCC])
    
    def test_clear_cache(self):
        """Test clearing compiler cache"""
        # Arrange
        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MSVC,
            version=VersionInfo(major=19, minor=40, patch=0),
            path="C:\\cl.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="C:\\")
        )
        self.factory._cache["msvc_x64"] = compiler_info
        self.factory._cache["mingw_gcc_x64"] = compiler_info
        
        # Act
        self.factory.clear_cache()
        
        # Assert
        self.assertEqual(len(self.factory._cache), 0)
    
    def test_get_cache_info(self):
        """Test getting cache information"""
        # Arrange
        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MSVC,
            version=VersionInfo(major=19, minor=40, patch=0),
            path="C:\\cl.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="C:\\")
        )
        self.factory._cache["msvc_x64"] = compiler_info
        
        # Act
        cache_info = self.factory.get_cache_info()
        
        # Assert
        self.assertEqual(cache_info["size"], 1)
        self.assertIn("msvc_x64", cache_info["keys"])
        self.assertEqual(len(cache_info["compilers"]), 1)
        self.assertEqual(
            cache_info["compilers"][0]["type"],
            "msvc"
        )
        self.assertEqual(
            cache_info["compilers"][0]["architecture"],
            "x64"
        )
    
    def test_get_cache_info_empty(self):
        """Test getting cache information when empty"""
        # Act
        cache_info = self.factory.get_cache_info()
        
        # Assert
        self.assertEqual(cache_info["size"], 0)
        self.assertEqual(len(cache_info["keys"]), 0)
        self.assertEqual(len(cache_info["compilers"]), 0)
    
    def test_compiler_requirements_to_dict(self):
        """Test converting CompilerRequirements to dictionary"""
        # Arrange
        requirements = CompilerRequirements(
            compiler_type=CompilerType.MSVC,
            architecture=Architecture.X64,
            cpp_standard="cpp23",
            required_capabilities=["modules", "concepts"],
            preferred_version="19.40.0"
        )
        
        # Act
        result = requirements.to_dict()
        
        # Assert
        self.assertEqual(result["compiler_type"], "msvc")
        self.assertEqual(result["architecture"], "x64")
        self.assertEqual(result["cpp_standard"], "cpp23")
        self.assertEqual(result["required_capabilities"], ["modules", "concepts"])
        self.assertEqual(result["preferred_version"], "19.40.0")
    
    def test_compiler_requirements_to_dict_none_values(self):
        """Test converting CompilerRequirements with None values to dictionary"""
        # Arrange
        requirements = CompilerRequirements()
        
        # Act
        result = requirements.to_dict()
        
        # Assert
        self.assertIsNone(result["compiler_type"])
        self.assertIsNone(result["architecture"])
        self.assertIsNone(result["cpp_standard"])
        self.assertIsNone(result["required_capabilities"])
        self.assertIsNone(result["preferred_version"])
    
    def test_initialize_default_detectors(self):
        """Test initializing default compiler detectors"""
        # Act
        self.factory.initialize_default_detectors()
        
        # Assert
        self.assertIn("msvc", self.factory._detectors)
        self.assertIn("msvc_clang", self.factory._detectors)
        self.assertIn("mingw_gcc", self.factory._detectors)
        self.assertIn("mingw_clang", self.factory._detectors)
    
    def test_get_detector(self):
        """Test getting detector by type"""
        # Arrange
        self.factory.register_detector("test_compiler", self.mock_detector)
        
        # Act
        result = self.factory._get_detector("test_compiler")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result, self.mock_detector)
    
    def test_get_detector_not_found(self):
        """Test getting detector when not found"""
        # Act
        result = self.factory._get_detector("unknown_compiler")
        
        # Assert
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
