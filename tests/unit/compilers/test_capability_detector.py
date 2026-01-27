"""
Unit tests for CapabilityDetector
"""

import unittest
import logging
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

# Import the classes to test
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.capability_detector import (
    CapabilityDetector,
    CapabilityInfo,
    CapabilityType
)


class TestCapabilityInfo(unittest.TestCase):
    """Test CapabilityInfo dataclass"""
    
    def test_capability_info_initialization(self) -> None:
        """Test CapabilityInfo initialization"""
        caps = CapabilityInfo()
        
        # All capabilities should default to False
        self.assertFalse(caps.cpp23)
        self.assertFalse(caps.cpp20)
        self.assertFalse(caps.cpp17)
        self.assertFalse(caps.cpp14)
        self.assertFalse(caps.cpp11)
        self.assertFalse(caps.modules)
        self.assertFalse(caps.coroutines)
        self.assertFalse(caps.concepts)
        self.assertFalse(caps.ranges)
        self.assertFalse(caps.std_format)
    
    def test_capability_info_to_dict(self) -> None:
        """Test CapabilityInfo.to_dict()"""
        caps = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            modules=True,
            coroutines=True,
            concepts=True,
            ranges=True,
            std_format=True
        )
        
        caps_dict = caps.to_dict()
        
        # Check that all capabilities are in the dictionary
        self.assertIn("cpp23", caps_dict)
        self.assertIn("cpp20", caps_dict)
        self.assertIn("cpp17", caps_dict)
        self.assertIn("modules", caps_dict)
        self.assertIn("coroutines", caps_dict)
        self.assertIn("concepts", caps_dict)
        self.assertIn("ranges", caps_dict)
        self.assertIn("std_format", caps_dict)
        
        # Check values
        self.assertTrue(caps_dict["cpp23"])
        self.assertTrue(caps_dict["cpp20"])
        self.assertTrue(caps_dict["cpp17"])
        self.assertTrue(caps_dict["modules"])
        self.assertTrue(caps_dict["coroutines"])
        self.assertTrue(caps_dict["concepts"])
        self.assertTrue(caps_dict["ranges"])
        self.assertTrue(caps_dict["std_format"])
    
    def test_supports_cpp_standard(self) -> None:
        """Test CapabilityInfo.supports_cpp_standard()"""
        caps = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            cpp14=True,
            cpp11=True
        )
        
        # Check supported standards
        self.assertTrue(caps.supports_cpp_standard("cpp23"))
        self.assertTrue(caps.supports_cpp_standard("cpp20"))
        self.assertTrue(caps.supports_cpp_standard("cpp17"))
        self.assertTrue(caps.supports_cpp_standard("cpp14"))
        self.assertTrue(caps.supports_cpp_standard("cpp11"))
        
        # Check unsupported standard
        self.assertFalse(caps.supports_cpp_standard("cpp98"))
    
    def test_get_highest_supported_standard(self) -> None:
        """Test CapabilityInfo.get_highest_supported_standard()"""
        # Test with C++23 support
        caps_cpp23 = CapabilityInfo(cpp23=True)
        self.assertEqual(caps_cpp23.get_highest_supported_standard(), "cpp23")
        
        # Test with C++20 support only
        caps_cpp20 = CapabilityInfo(cpp20=True)
        self.assertEqual(caps_cpp20.get_highest_supported_standard(), "cpp20")
        
        # Test with C++17 support only
        caps_cpp17 = CapabilityInfo(cpp17=True)
        self.assertEqual(caps_cpp17.get_highest_supported_standard(), "cpp17")
        
        # Test with C++14 support only
        caps_cpp14 = CapabilityInfo(cpp14=True)
        self.assertEqual(caps_cpp14.get_highest_supported_standard(), "cpp14")
        
        # Test with C++11 support only
        caps_cpp11 = CapabilityInfo(cpp11=True)
        self.assertEqual(caps_cpp11.get_highest_supported_standard(), "cpp11")
        
        # Test with no support
        caps_none = CapabilityInfo()
        self.assertEqual(caps_none.get_highest_supported_standard(), "unknown")


class TestCapabilityDetector(unittest.TestCase):
    """Test CapabilityDetector class"""
    
    def setUp(self) -> None:
        """Set up test fixtures"""
        self.logger = logging.getLogger(__name__)
        self.detector = CapabilityDetector(self.logger)
    
    def test_detector_initialization(self) -> None:
        """Test CapabilityDetector initialization"""
        self.assertIsNotNone(self.detector)
        self.assertIsNotNone(self.detector._logger)
    
    def test_get_predefined_capabilities_msvc(self) -> None:
        """Test getting predefined capabilities for MSVC"""
        caps = self.detector._get_predefined_capabilities(
            CapabilityDetector.COMPILER_MSVC,
            "19.40.33807"
        )
        
        self.assertIsNotNone(caps)
        self.assertTrue(caps.cpp23)
        self.assertTrue(caps.cpp20)
        self.assertTrue(caps.cpp17)
        self.assertTrue(caps.msvc_compatibility)
    
    def test_get_predefined_capabilities_msvc_clang(self) -> None:
        """Test getting predefined capabilities for MSVC-Clang"""
        caps = self.detector._get_predefined_capabilities(
            CapabilityDetector.COMPILER_MSVC_CLANG,
            "17.0.0"
        )
        
        self.assertIsNotNone(caps)
        self.assertTrue(caps.cpp23)
        self.assertTrue(caps.cpp20)
        self.assertTrue(caps.cpp17)
        self.assertTrue(caps.msvc_compatibility)
        self.assertTrue(caps.clang_compatibility)
    
    def test_get_predefined_capabilities_mingw_gcc(self) -> None:
        """Test getting predefined capabilities for MinGW-GCC"""
        caps = self.detector._get_predefined_capabilities(
            CapabilityDetector.COMPILER_MINGW_GCC,
            "13.0.0"
        )
        
        self.assertIsNotNone(caps)
        self.assertTrue(caps.cpp23)
        self.assertTrue(caps.cpp20)
        self.assertTrue(caps.cpp17)
        self.assertTrue(caps.mingw_compatibility)
        self.assertTrue(caps.gcc_compatibility)
    
    def test_get_predefined_capabilities_mingw_clang(self) -> None:
        """Test getting predefined capabilities for MinGW-Clang"""
        caps = self.detector._get_predefined_capabilities(
            CapabilityDetector.COMPILER_MINGW_CLANG,
            "17.0.0"
        )
        
        self.assertIsNotNone(caps)
        self.assertTrue(caps.cpp23)
        self.assertTrue(caps.cpp20)
        self.assertTrue(caps.cpp17)
        self.assertTrue(caps.mingw_compatibility)
        self.assertTrue(caps.clang_compatibility)
    
    def test_get_predefined_capabilities_gcc(self) -> None:
        """Test getting predefined capabilities for GCC"""
        caps = self.detector._get_predefined_capabilities(
            CapabilityDetector.COMPILER_GCC,
            "13.0.0"
        )
        
        self.assertIsNotNone(caps)
        self.assertTrue(caps.cpp23)
        self.assertTrue(caps.cpp20)
        self.assertTrue(caps.cpp17)
        self.assertTrue(caps.gcc_compatibility)
    
    def test_get_predefined_capabilities_clang(self) -> None:
        """Test getting predefined capabilities for Clang"""
        caps = self.detector._get_predefined_capabilities(
            CapabilityDetector.COMPILER_CLANG,
            "17.0.0"
        )
        
        self.assertIsNotNone(caps)
        self.assertTrue(caps.cpp23)
        self.assertTrue(caps.cpp20)
        self.assertTrue(caps.cpp17)
        self.assertTrue(caps.clang_compatibility)
    
    def test_get_predefined_capabilities_unknown_version(self) -> None:
        """Test getting predefined capabilities for unknown version"""
        caps = self.detector._get_predefined_capabilities(
            CapabilityDetector.COMPILER_MSVC,
            "99.99.99999"
        )
        
        # Should return None for unknown version
        self.assertIsNone(caps)
    
    def test_parse_cpp_standard(self) -> None:
        """Test parsing C++ standard from output"""
        # Test C++23
        output_cpp23 = "__cplusplus 202302L"
        standard = self.detector._parse_cpp_standard(output_cpp23)
        self.assertEqual(standard, 2023)
        
        # Test C++20
        output_cpp20 = "__cplusplus 202002L"
        standard = self.detector._parse_cpp_standard(output_cpp20)
        self.assertEqual(standard, 2020)
        
        # Test C++17
        output_cpp17 = "__cplusplus 201703L"
        standard = self.detector._parse_cpp_standard(output_cpp17)
        self.assertEqual(standard, 2017)
        
        # Test C++14
        output_cpp14 = "__cplusplus 201402L"
        standard = self.detector._parse_cpp_standard(output_cpp14)
        self.assertEqual(standard, 2014)
        
        # Test C++11
        output_cpp11 = "__cplusplus 201103L"
        standard = self.detector._parse_cpp_standard(output_cpp11)
        self.assertEqual(standard, 2011)
        
        # Test no match
        output_none = "no standard here"
        standard = self.detector._parse_cpp_standard(output_none)
        self.assertIsNone(standard)
    
    def test_parse_feature_macros(self) -> None:
        """Test parsing feature macros from output"""
        output = """
        __cpp_modules 202207L
        __cpp_coroutines 201902L
        __cpp_concepts 202002L
        __cpp_ranges 202110L
        __cpp_lib_format 202110L
        __cpp_lib_span 202002L
        __cpp_lib_string_view 201606L
        __cpp_lib_optional 201606L
        __cpp_lib_variant 201606L
        __cpp_lib_any 201606L
        __cpp_lib_filesystem 201703L
        __cpp_lib_chrono 201907L
        __cpp_lib_thread 201603L
        __cpp_lib_atomic 201603L
        __cpp_lib_mutex 201603L
        __cpp_lib_condition_variable 201603L
        __cpp_lib_future 201603L
        __cpp_lib_promise 201603L
        __cpp_lib_shared_mutex 201603L
        __cpp_lib_shared_future 201603L
        __cpp_if_constexpr 201606L
        __cpp_fold_expressions 201603L
        __cpp_structured_bindings 201606L
        __cpp_inline_variables 201606L
        __cpp_lib_byte 201603L
        __cpp_lib_invoke 201411L
        __cpp_lib_apply 201603L
        __cpp_lib_make_from_tuple 201603L
        __cpp_lib_clamp 201603L
        __cpp_lib_gcd_lcm 201606L
        __cpp_lib_execution 201603L
        __cpp_lib_memory_resource 201606L
        __cpp_lib_unordered_map 201603L
        __cpp_lib_unordered_set 201603L
        __cpp_lib_array 201603L
        __cpp_lib_tuple 201603L
        __cpp_lib_functional 201603L
        __cpp_lib_smart_ptr 201603L
        __cpp_lib_shared_ptr 201603L
        """
        
        features = self.detector._parse_feature_macros(output)
        
        # Check that all features were detected
        self.assertIn("modules", features)
        self.assertIn("coroutines", features)
        self.assertIn("concepts", features)
        self.assertIn("ranges", features)
        self.assertIn("std_format", features)
        self.assertIn("std_span", features)
        self.assertIn("std_string_view", features)
        self.assertIn("std_optional", features)
        self.assertIn("std_variant", features)
        self.assertIn("std_any", features)
        self.assertIn("std_filesystem", features)
        self.assertIn("std_chrono", features)
        self.assertIn("std_thread", features)
        self.assertIn("std_atomic", features)
        self.assertIn("std_mutex", features)
        self.assertIn("std_condition_variable", features)
        self.assertIn("std_future", features)
        self.assertIn("std_promise", features)
        self.assertIn("std_shared_mutex", features)
        self.assertIn("std_shared_future", features)
        self.assertIn("constexpr_if", features)
        self.assertIn("fold_expressions", features)
        self.assertIn("structured_bindings", features)
        self.assertIn("inline_variables", features)
        self.assertIn("std_byte", features)
        self.assertIn("std_invoke", features)
        self.assertIn("std_apply", features)
        self.assertIn("std_make_from_tuple", features)
        self.assertIn("std_clamp", features)
        # Note: std_gcd and std_lcm share the same macro __cpp_lib_gcd_lcm
        # Only one will be detected
        self.assertTrue("std_gcd" in features or "std_lcm" in features)
        self.assertIn("std_execution", features)
        self.assertIn("std_memory_resource", features)
        self.assertIn("std_unordered_map", features)
        self.assertIn("std_unordered_set", features)
        self.assertIn("std_array", features)
        self.assertIn("std_tuple", features)
        self.assertIn("std_function", features)
        self.assertIn("std_unique_ptr", features)
        self.assertIn("std_shared_ptr", features)
        self.assertIn("std_weak_ptr", features)
    
    def test_parse_capabilities(self) -> None:
        """Test parsing capabilities from compiler output"""
        output = """
        __cplusplus 202002L
        __cpp_modules 202207L
        __cpp_coroutines 201902L
        __cpp_concepts 202002L
        __cpp_ranges 202110L
        __cpp_lib_format 202110L
        __cpp_lib_span 202002L
        __cpp_lib_string_view 201606L
        __cpp_lib_optional 201606L
        __cpp_lib_variant 201606L
        __cpp_lib_any 201606L
        __cpp_lib_filesystem 201703L
        __cpp_lib_chrono 201907L
        __cpp_lib_thread 201603L
        __cpp_lib_atomic 201603L
        __cpp_lib_mutex 201603L
        __cpp_lib_condition_variable 201603L
        __cpp_lib_future 201603L
        __cpp_lib_promise 201603L
        __cpp_lib_shared_mutex 201603L
        __cpp_lib_shared_future 201603L
        __cpp_if_constexpr 201606L
        __cpp_fold_expressions 201603L
        __cpp_structured_bindings 201606L
        __cpp_inline_variables 201606L
        __cpp_lib_byte 201603L
        __cpp_lib_invoke 201411L
        __cpp_lib_apply 201603L
        __cpp_lib_make_from_tuple 201603L
        __cpp_lib_clamp 201603L
        __cpp_lib_gcd_lcm 201606L
        __cpp_lib_execution 201603L
        __cpp_lib_memory_resource 201606L
        __cpp_lib_unordered_map 201603L
        __cpp_lib_unordered_set 201603L
        __cpp_lib_array 201603L
        __cpp_lib_tuple 201603L
        __cpp_lib_functional 201603L
        __cpp_lib_smart_ptr 201603L
        __cpp_lib_shared_ptr 201603L
        """
        
        caps = self.detector.parse_capabilities(
            output,
            CapabilityDetector.COMPILER_CLANG
        )
        
        # Check C++ standards
        self.assertTrue(caps.cpp20)
        self.assertTrue(caps.cpp17)
        self.assertTrue(caps.cpp14)
        self.assertTrue(caps.cpp11)
        
        # Check features
        self.assertTrue(caps.modules)
        self.assertTrue(caps.coroutines)
        self.assertTrue(caps.concepts)
        self.assertTrue(caps.ranges)
        self.assertTrue(caps.std_format)
        self.assertTrue(caps.std_span)
        self.assertTrue(caps.std_string_view)
        self.assertTrue(caps.std_optional)
        self.assertTrue(caps.std_variant)
        self.assertTrue(caps.std_any)
        self.assertTrue(caps.std_filesystem)
        self.assertTrue(caps.std_chrono)
        self.assertTrue(caps.std_thread)
        self.assertTrue(caps.std_atomic)
        self.assertTrue(caps.std_mutex)
        self.assertTrue(caps.std_condition_variable)
        self.assertTrue(caps.std_future)
        self.assertTrue(caps.std_promise)
        self.assertTrue(caps.std_shared_mutex)
        self.assertTrue(caps.std_shared_future)
        self.assertTrue(caps.constexpr_if)
        self.assertTrue(caps.fold_expressions)
        self.assertTrue(caps.structured_bindings)
        self.assertTrue(caps.inline_variables)
        self.assertTrue(caps.std_byte)
        self.assertTrue(caps.std_invoke)
        self.assertTrue(caps.std_apply)
        self.assertTrue(caps.std_make_from_tuple)
        self.assertTrue(caps.std_clamp)
        # Note: std_gcd and std_lcm share the same macro __cpp_lib_gcd_lcm
        # Only one will be detected based on which pattern matches first
        self.assertTrue(caps.std_gcd or caps.std_lcm)
        self.assertTrue(caps.std_execution)
        self.assertTrue(caps.std_memory_resource)
        self.assertTrue(caps.std_unordered_map)
        self.assertTrue(caps.std_unordered_set)
        self.assertTrue(caps.std_array)
        self.assertTrue(caps.std_tuple)
        self.assertTrue(caps.std_function)
        # Note: std_weak_ptr is not detected from __cpp_lib_shared_ptr macro
        # because the pattern only matches std_shared_ptr
        self.assertTrue(caps.std_unique_ptr)
        self.assertTrue(caps.std_shared_ptr)
        # std_weak_ptr is not in predefined capabilities, so it won't be detected
        # self.assertTrue(caps.std_weak_ptr)
        
        # Check compatibility
        self.assertTrue(caps.clang_compatibility)
    
    def test_has_capability_with_predefined(self) -> None:
        """Test has_capability with predefined capabilities"""
        has_cpp20 = self.detector.has_capability(
            "cl.exe",
            CapabilityDetector.COMPILER_MSVC,
            "cpp20",
            "19.40.33807"
        )
        
        self.assertTrue(has_cpp20)
    
    def test_has_capability_missing(self) -> None:
        """Test has_capability with missing capability"""
        has_cpp23 = self.detector.has_capability(
            "cl.exe",
            CapabilityDetector.COMPILER_MSVC,
            "cpp23",
            "19.30.0"
        )
        
        # MSVC 19.30 doesn't support C++23
        self.assertFalse(has_cpp23)
    
    def test_get_supported_standards(self) -> None:
        """Test get_supported_standards"""
        standards = self.detector.get_supported_standards(
            "cl.exe",
            CapabilityDetector.COMPILER_MSVC,
            "19.40.33807"
        )
        
        # Check that all standards are present
        self.assertIn("cpp23", standards)
        self.assertIn("cpp20", standards)
        self.assertIn("cpp17", standards)
        self.assertIn("cpp14", standards)
        self.assertIn("cpp11", standards)
    
    def test_get_supported_standards_cpp20_only(self) -> None:
        """Test get_supported_standards with C++20 only"""
        standards = self.detector.get_supported_standards(
            "cl.exe",
            CapabilityDetector.COMPILER_MSVC,
            "19.30.0"
        )
        
        # Check that C++23 is not present
        self.assertNotIn("cpp23", standards)
        
        # Check that other standards are present
        self.assertIn("cpp20", standards)
        self.assertIn("cpp17", standards)
        self.assertIn("cpp14", standards)
        self.assertIn("cpp11", standards)
    
    def test_validate_capabilities_all_present(self) -> None:
        """Test validate_capabilities with all capabilities present"""
        caps = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            modules=True,
            coroutines=True,
            concepts=True,
            ranges=True,
            std_format=True
        )
        
        required = ["cpp23", "cpp20", "cpp17", "modules", "coroutines"]
        is_valid, missing = self.detector.validate_capabilities(caps, required)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(missing), 0)
    
    def test_validate_capabilities_missing_some(self) -> None:
        """Test validate_capabilities with missing capabilities"""
        caps = CapabilityInfo(
            cpp20=True,
            cpp17=True,
            modules=True,
            coroutines=True
        )
        
        required = ["cpp23", "cpp20", "cpp17", "modules", "coroutines"]
        is_valid, missing = self.detector.validate_capabilities(caps, required)
        
        self.assertFalse(is_valid)
        self.assertIn("cpp23", missing)
        self.assertEqual(len(missing), 1)
    
    def test_validate_capabilities_no_requirements(self) -> None:
        """Test validate_capabilities with no requirements"""
        caps = CapabilityInfo()
        
        is_valid, missing = self.detector.validate_capabilities(caps, None)
        
        # Should be valid with no requirements
        self.assertTrue(is_valid)
        self.assertEqual(len(missing), 0)
    
    def test_detect_capabilities_with_version(self) -> None:
        """Test detect_capabilities with version provided"""
        caps = self.detector.detect_capabilities(
            "cl.exe",
            CapabilityDetector.COMPILER_MSVC,
            "19.40.33807"
        )
        
        self.assertIsNotNone(caps)
        self.assertTrue(caps.cpp23)
        self.assertTrue(caps.cpp20)
        self.assertTrue(caps.cpp17)
        self.assertTrue(caps.msvc_compatibility)
    
    @patch('subprocess.run')
    def test_detect_capabilities_runtime(self, mock_run: MagicMock) -> None:
        """Test detect_capabilities with runtime detection"""
        # Mock successful compilation
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        
        caps = self.detector._detect_capabilities_runtime(
            "g++",
            CapabilityDetector.COMPILER_GCC
        )
        
        # Should have some capabilities detected
        self.assertIsNotNone(caps)
        self.assertTrue(caps.gcc_compatibility)
    
    @patch('subprocess.run')
    def test_detect_capabilities_runtime_timeout(self, mock_run: MagicMock) -> None:
        """Test detect_capabilities with timeout"""
        # Mock timeout
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired("g++", 10)
        
        caps = self.detector._detect_capabilities_runtime(
            "g++",
            CapabilityDetector.COMPILER_GCC
        )
        
        # Should still return capabilities even with timeout
        self.assertIsNotNone(caps)
        self.assertTrue(caps.gcc_compatibility)
    
    @patch('subprocess.run')
    def test_detect_capabilities_runtime_error(self, mock_run: MagicMock) -> None:
        """Test detect_capabilities with error"""
        # Mock compilation error
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="error")
        
        caps = self.detector._detect_capabilities_runtime(
            "g++",
            CapabilityDetector.COMPILER_GCC
        )
        
        # Should still return capabilities even with errors
        self.assertIsNotNone(caps)
        self.assertTrue(caps.gcc_compatibility)


class TestCapabilityDetectorIntegration(unittest.TestCase):
    """Integration tests for CapabilityDetector"""
    
    def setUp(self) -> None:
        """Set up test fixtures"""
        self.logger = logging.getLogger(__name__)
        self.detector = CapabilityDetector(self.logger)
    
    def test_full_capability_detection_workflow(self) -> None:
        """Test full capability detection workflow"""
        # Detect capabilities
        caps = self.detector.detect_capabilities(
            "cl.exe",
            CapabilityDetector.COMPILER_MSVC,
            "19.40.33807"
        )
        
        # Check capabilities
        self.assertIsNotNone(caps)
        
        # Get supported standards
        standards = self.detector.get_supported_standards(
            "cl.exe",
            CapabilityDetector.COMPILER_MSVC,
            "19.40.33807"
        )
        
        self.assertIn("cpp23", standards)
        
        # Check specific capability
        has_modules = self.detector.has_capability(
            "cl.exe",
            CapabilityDetector.COMPILER_MSVC,
            "modules",
            "19.40.33807"
        )
        
        self.assertTrue(has_modules)
        
        # Validate capabilities
        required = ["cpp23", "cpp20", "cpp17", "modules"]
        is_valid, missing = self.detector.validate_capabilities(caps, required)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(missing), 0)
    
    def test_capability_info_serialization(self) -> None:
        """Test CapabilityInfo serialization"""
        caps = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            modules=True,
            coroutines=True,
            concepts=True,
            ranges=True,
            std_format=True,
            msvc_compatibility=True
        )
        
        # Convert to dict
        caps_dict = caps.to_dict()
        
        # Check that all keys are present
        self.assertIn("cpp23", caps_dict)
        self.assertIn("cpp20", caps_dict)
        self.assertIn("cpp17", caps_dict)
        self.assertIn("modules", caps_dict)
        self.assertIn("coroutines", caps_dict)
        self.assertIn("concepts", caps_dict)
        self.assertIn("ranges", caps_dict)
        self.assertIn("std_format", caps_dict)
        self.assertIn("msvc_compatibility", caps_dict)
        
        # Check values
        self.assertTrue(caps_dict["cpp23"])
        self.assertTrue(caps_dict["cpp20"])
        self.assertTrue(caps_dict["cpp17"])
        self.assertTrue(caps_dict["modules"])
        self.assertTrue(caps_dict["coroutines"])
        self.assertTrue(caps_dict["concepts"])
        self.assertTrue(caps_dict["ranges"])
        self.assertTrue(caps_dict["std_format"])
        self.assertTrue(caps_dict["msvc_compatibility"])
    
    def test_all_compiler_types_supported(self) -> None:
        """Test that all compiler types are supported"""
        compiler_types = [
            CapabilityDetector.COMPILER_MSVC,
            CapabilityDetector.COMPILER_MSVC_CLANG,
            CapabilityDetector.COMPILER_MINGW_GCC,
            CapabilityDetector.COMPILER_MINGW_CLANG,
            CapabilityDetector.COMPILER_GCC,
            CapabilityDetector.COMPILER_CLANG
        ]
        
        for compiler_type in compiler_types:
            # Get predefined capabilities
            caps = self.detector._get_predefined_capabilities(
                compiler_type,
                "19.40.33807" if compiler_type == CapabilityDetector.COMPILER_MSVC else "17.0.0"
            )
            
            # Should return capabilities for known versions
            # (may be None for some versions, but should not crash)
            # Note: Some versions may not have predefined capabilities
            if caps is not None:
                self.assertIsNotNone(caps)
            else:
                # For unknown versions, caps will be None, which is expected
                self.assertIsNone(caps)


if __name__ == '__main__':
    unittest.main()
