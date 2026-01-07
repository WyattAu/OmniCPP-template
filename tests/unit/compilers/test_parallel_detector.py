"""
Unit tests for Parallel Compiler Detector

Tests parallel detection of compiler installations,
including error handling, logging, and performance metrics.
"""

import unittest
import time
from typing import List
from unittest.mock import patch

from scripts.python.compilers.parallel_detector import (
    ParallelDetector,
    ParallelDetectionResult,
    ParallelDetectionSummary,
    CompilerType,
    Architecture,
    VersionInfo,
    CapabilityInfo,
    EnvironmentInfo,
    CompilerInfo
)


class TestParallelDetector(unittest.TestCase):
    """Test cases for ParallelDetector class"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ParallelDetector(max_workers=2)

    def tearDown(self):
        """Clean up after tests"""
        self.detector.clear_results()

    def test_initialization(self):
        """Test ParallelDetector initialization"""
        self.assertIsNotNone(self.detector)

    def test_initialization_with_custom_workers(self):
        """Test ParallelDetector initialization with custom workers"""
        detector = ParallelDetector(max_workers=8)
        self.assertIsNotNone(detector)

    def test_register_detector(self):
        """Test registering a compiler detector"""
        def mock_detector() -> List[CompilerInfo]:
            return []

        self.detector.register_detector("msvc", mock_detector)
        # Verify detector was registered by checking it works
        result = self.detector.detect_compiler_parallel("msvc")
        self.assertIsNotNone(result)

    def test_register_multiple_detectors(self):
        """Test registering multiple compiler detectors"""
        def msvc_detector() -> List[CompilerInfo]:
            return []

        def mingw_detector() -> List[CompilerInfo]:
            return []

        self.detector.register_detector("msvc", msvc_detector)
        self.detector.register_detector("mingw_gcc", mingw_detector)

        # Verify both detectors work
        result1 = self.detector.detect_compiler_parallel("msvc")
        result2 = self.detector.detect_compiler_parallel("mingw_gcc")
        self.assertIsNotNone(result1)
        self.assertIsNotNone(result2)

    @patch('os.path.exists', return_value=True)
    def test_detect_all_parallel_no_detectors(self, mock_exists):
        """Test parallel detection with no registered detectors"""
        summary = self.detector.detect_all_parallel()

        self.assertIsInstance(summary, ParallelDetectionSummary)
        self.assertEqual(summary.total_compilers, 0)
        self.assertEqual(summary.successful_detections, 0)
        self.assertEqual(summary.failed_detections, 0)
        self.assertEqual(len(summary.results), 0)

    @patch('os.path.exists', return_value=True)
    def test_detect_all_parallel_single_detector(self, mock_exists):
        """Test parallel detection with single detector"""
        def mock_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MSVC,
                    version=VersionInfo(major=19, minor=40, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ]

        self.detector.register_detector("msvc", mock_detector)
        summary = self.detector.detect_all_parallel()

        self.assertEqual(summary.total_compilers, 1)
        self.assertEqual(summary.successful_detections, 1)
        self.assertEqual(summary.failed_detections, 0)
        self.assertIn("msvc", summary.results)
        self.assertTrue(summary.results["msvc"].success)
        self.assertEqual(len(summary.results["msvc"].compilers), 1)

    @patch('os.path.exists', return_value=True)
    def test_detect_all_parallel_multiple_detectors(self, mock_exists):
        """Test parallel detection with multiple detectors"""
        def msvc_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MSVC,
                    version=VersionInfo(major=19, minor=40, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ]

        def mingw_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MINGW_GCC,
                    version=VersionInfo(major=13, minor=2, patch=0),
                    path=r"C:\msys64\ucrt64\bin\g++.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\msys64")
                )
            ]

        self.detector.register_detector("msvc", msvc_detector)
        self.detector.register_detector("mingw_gcc", mingw_detector)
        summary = self.detector.detect_all_parallel()

        self.assertEqual(summary.total_compilers, 2)
        self.assertEqual(summary.successful_detections, 2)
        self.assertEqual(summary.failed_detections, 0)
        self.assertIn("msvc", summary.results)
        self.assertIn("mingw_gcc", summary.results)

    @patch('os.path.exists', return_value=True)
    def test_detect_all_parallel_with_filter(self, mock_exists):
        """Test parallel detection with compiler type filter"""
        def msvc_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MSVC,
                    version=VersionInfo(major=19, minor=40, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ]

        def mingw_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MINGW_GCC,
                    version=VersionInfo(major=13, minor=2, patch=0),
                    path=r"C:\msys64\ucrt64\bin\g++.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\msys64")
                )
            ]

        self.detector.register_detector("msvc", msvc_detector)
        self.detector.register_detector("mingw_gcc", mingw_detector)
        summary = self.detector.detect_all_parallel(compiler_types=["msvc"])

        self.assertEqual(summary.total_compilers, 1)
        self.assertEqual(summary.successful_detections, 1)
        self.assertIn("msvc", summary.results)
        self.assertNotIn("mingw_gcc", summary.results)

    @patch('os.path.exists', return_value=True)
    def test_detect_compiler_parallel_success(self, mock_exists):
        """Test parallel detection of single compiler type"""
        def mock_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MSVC,
                    version=VersionInfo(major=19, minor=40, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ]

        self.detector.register_detector("msvc", mock_detector)
        result = self.detector.detect_compiler_parallel("msvc")

        self.assertIsInstance(result, ParallelDetectionResult)
        self.assertTrue(result.success)
        self.assertEqual(result.compiler_type, "msvc")
        self.assertEqual(len(result.compilers), 1)
        self.assertIsNone(result.error)

    def test_detect_compiler_parallel_not_registered(self):
        """Test parallel detection of unregistered compiler type"""
        result = self.detector.detect_compiler_parallel("msvc")

        self.assertIsInstance(result, ParallelDetectionResult)
        self.assertFalse(result.success)
        self.assertEqual(result.compiler_type, "msvc")
        self.assertEqual(len(result.compilers), 0)
        self.assertIsNotNone(result.error)
        self.assertIsNotNone(result.error)

    def test_detect_compiler_parallel_exception(self):
        """Test parallel detection with detector exception"""
        def failing_detector() -> List[CompilerInfo]:
            raise RuntimeError("Detection failed")

        self.detector.register_detector("msvc", failing_detector)
        result = self.detector.detect_compiler_parallel("msvc")

        self.assertIsInstance(result, ParallelDetectionResult)
        self.assertFalse(result.success)
        self.assertEqual(result.compiler_type, "msvc")
        self.assertEqual(len(result.compilers), 0)
        self.assertIsNotNone(result.error)
        self.assertIsNotNone(result.error)

    @patch('os.path.exists', return_value=True)
    def test_get_parallel_results(self, mock_exists):
        """Test getting parallel detection results"""
        def mock_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MSVC,
                    version=VersionInfo(major=19, minor=40, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ]

        self.detector.register_detector("msvc", mock_detector)
        self.detector.detect_all_parallel()
        results = self.detector.get_parallel_results()

        self.assertIsInstance(results, dict)
        self.assertIn("msvc", results)
        self.assertEqual(len(results["msvc"].compilers), 1)

    def test_get_parallel_results_empty(self):
        """Test getting parallel results when no detection performed"""
        results = self.detector.get_parallel_results()

        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 0)

    @patch('os.path.exists', return_value=True)
    def test_get_parallel_summary(self, mock_exists):
        """Test getting parallel detection summary"""
        def mock_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MSVC,
                    version=VersionInfo(major=19, minor=40, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ]

        self.detector.register_detector("msvc", mock_detector)
        self.detector.detect_all_parallel()
        summary = self.detector.get_parallel_summary()

        self.assertIsInstance(summary, ParallelDetectionSummary)
        self.assertEqual(summary.total_compilers, 1)
        self.assertEqual(summary.successful_detections, 1)
        self.assertEqual(summary.failed_detections, 0)

    def test_get_parallel_summary_none(self):
        """Test getting parallel summary when no detection performed"""
        summary = self.detector.get_parallel_summary()

        self.assertIsNone(summary)

    @patch('os.path.exists', return_value=True)
    def test_get_compilers_by_type(self, mock_exists):
        """Test getting compilers by type"""
        def mock_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MSVC,
                    version=VersionInfo(major=19, minor=40, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ]

        self.detector.register_detector("msvc", mock_detector)
        self.detector.detect_all_parallel()
        compilers = self.detector.get_compilers_by_type("msvc")

        self.assertIsInstance(compilers, list)
        self.assertEqual(len(compilers), 1)
        self.assertEqual(compilers[0].compiler_type, CompilerType.MSVC)

    @patch('os.path.exists', return_value=True)
    def test_get_compilers_by_type_not_found(self, mock_exists):
        """Test getting compilers for non-existent type"""
        def mock_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MSVC,
                    version=VersionInfo(major=19, minor=40, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ]

        self.detector.register_detector("msvc", mock_detector)
        self.detector.detect_all_parallel()
        compilers = self.detector.get_compilers_by_type("mingw_gcc")

        self.assertIsInstance(compilers, list)
        self.assertEqual(len(compilers), 0)

    @patch('os.path.exists', return_value=True)
    def test_get_all_compilers(self, mock_exists):
        """Test getting all detected compilers"""
        def msvc_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MSVC,
                    version=VersionInfo(major=19, minor=40, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ]

        def mingw_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MINGW_GCC,
                    version=VersionInfo(major=13, minor=2, patch=0),
                    path=r"C:\msys64\ucrt64\bin\g++.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\msys64")
                )
            ]

        self.detector.register_detector("msvc", msvc_detector)
        self.detector.register_detector("mingw_gcc", mingw_detector)
        self.detector.detect_all_parallel()
        all_compilers = self.detector.get_all_compilers()

        self.assertIsInstance(all_compilers, list)
        self.assertEqual(len(all_compilers), 2)

    @patch('os.path.exists', return_value=True)
    def test_clear_results(self, mock_exists):
        """Test clearing detection results"""
        def mock_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MSVC,
                    version=VersionInfo(major=19, minor=40, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ]

        self.detector.register_detector("msvc", mock_detector)
        self.detector.detect_all_parallel()

        # Verify results exist
        results = self.detector.get_parallel_results()
        self.assertEqual(len(results), 1)

        self.detector.clear_results()

        # Verify results are cleared
        results = self.detector.get_parallel_results()
        self.assertEqual(len(results), 0)

    @patch('os.path.exists', return_value=True)
    def test_parallel_detection_performance(self, mock_exists):
        """Test parallel detection performance improvement"""
        def slow_detector() -> List[CompilerInfo]:
            time.sleep(0.1)
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MSVC,
                    version=VersionInfo(major=19, minor=40, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ]

        self.detector.register_detector("msvc", slow_detector)
        self.detector.register_detector("mingw_gcc", slow_detector)
        self.detector.register_detector("msvc_clang", slow_detector)
        self.detector.register_detector("mingw_clang", slow_detector)

        start_time = time.time()
        summary = self.detector.detect_all_parallel()
        total_time = time.time() - start_time

        # With 4 workers and 4 detectors each taking 0.1s,
        # parallel execution should complete in ~0.1-0.2s
        # (not 0.4s which would be sequential)
        self.assertLess(total_time, 0.3)
        self.assertEqual(summary.total_compilers, 4)

    @patch('os.path.exists', return_value=True)
    def test_get_detection_statistics(self, mock_exists):
        """Test getting detection statistics"""
        def msvc_detector() -> List[CompilerInfo]:
            time.sleep(0.05)
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MSVC,
                    version=VersionInfo(major=19, minor=40, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ]

        def mingw_detector() -> List[CompilerInfo]:
            time.sleep(0.1)
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MINGW_GCC,
                    version=VersionInfo(major=13, minor=2, patch=0),
                    path=r"C:\msys64\ucrt64\bin\g++.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\msys64")
                )
            ]

        self.detector.register_detector("msvc", msvc_detector)
        self.detector.register_detector("mingw_gcc", mingw_detector)
        self.detector.detect_all_parallel()
        stats = self.detector.get_detection_statistics()

        self.assertIsInstance(stats, dict)
        self.assertIn("total_time", stats)
        self.assertIn("total_compilers", stats)
        self.assertIn("successful_detections", stats)
        self.assertIn("failed_detections", stats)
        self.assertIn("average_detection_time", stats)
        self.assertIn("fastest_detection", stats)
        self.assertIn("slowest_detection", stats)
        self.assertIn("compilers_by_type", stats)

        self.assertEqual(stats["total_compilers"], 2)
        self.assertEqual(stats["successful_detections"], 2)
        self.assertEqual(stats["failed_detections"], 0)

    def test_get_detection_statistics_empty(self):
        """Test getting detection statistics when no detection performed"""
        stats = self.detector.get_detection_statistics()

        self.assertIsInstance(stats, dict)
        self.assertEqual(len(stats), 0)

    def test_parallel_detection_result_to_dict(self):
        """Test ParallelDetectionResult to_dict method"""
        result = ParallelDetectionResult(
            compiler_type="msvc",
            compilers=[
                CompilerInfo(
                    compiler_type=CompilerType.MSVC,
                    version=VersionInfo(major=19, minor=40, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ],
            success=True,
            detection_time=0.5
        )

        result_dict = result.to_dict()

        self.assertIsInstance(result_dict, dict)
        self.assertEqual(result_dict["compiler_type"], "msvc")
        self.assertEqual(result_dict["success"], True)
        self.assertEqual(result_dict["detection_time"], 0.5)
        self.assertEqual(len(result_dict["compilers"]), 1)
        self.assertIsNone(result_dict["error"])

    def test_parallel_detection_summary_to_dict(self):
        """Test ParallelDetectionSummary to_dict method"""
        summary = ParallelDetectionSummary(
            total_compilers=2,
            successful_detections=2,
            failed_detections=0,
            total_time=1.0,
            results={
                "msvc": ParallelDetectionResult(
                    compiler_type="msvc",
                    compilers=[],
                    success=True,
                    detection_time=0.5
                ),
                "mingw_gcc": ParallelDetectionResult(
                    compiler_type="mingw_gcc",
                    compilers=[],
                    success=True,
                    detection_time=0.5
                )
            }
        )

        summary_dict = summary.to_dict()

        self.assertIsInstance(summary_dict, dict)
        self.assertEqual(summary_dict["total_compilers"], 2)
        self.assertEqual(summary_dict["successful_detections"], 2)
        self.assertEqual(summary_dict["failed_detections"], 0)
        self.assertEqual(summary_dict["total_time"], 1.0)
        self.assertIn("results", summary_dict)
        self.assertIn("errors", summary_dict)

    def test_compiler_info_to_dict(self):
        """Test CompilerInfo to_dict method"""
        compiler = CompilerInfo(
            compiler_type=CompilerType.MSVC,
            version=VersionInfo(major=19, minor=40, patch=0),
            path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022"),
            metadata={"test": "value"}
        )

        compiler_dict = compiler.to_dict()

        self.assertIsInstance(compiler_dict, dict)
        self.assertEqual(compiler_dict["compiler_type"], "msvc")
        self.assertEqual(compiler_dict["version"], "19.40.0")
        self.assertEqual(compiler_dict["architecture"], "x64")
        self.assertIn("capabilities", compiler_dict)
        self.assertIn("environment", compiler_dict)
        self.assertIn("metadata", compiler_dict)

    def test_version_info_str(self):
        """Test VersionInfo __str__ method"""
        version = VersionInfo(major=19, minor=40, patch=0)
        self.assertEqual(str(version), "19.40.0")

        version_with_build = VersionInfo(major=19, minor=40, patch=0, build="33811")
        self.assertEqual(str(version_with_build), "19.40.0.33811")

    def test_version_info_comparison(self):
        """Test VersionInfo comparison"""
        v1 = VersionInfo(major=19, minor=40, patch=0)
        v2 = VersionInfo(major=19, minor=41, patch=0)
        v3 = VersionInfo(major=20, minor=0, patch=0)

        self.assertTrue(v1 < v2)
        self.assertTrue(v1 < v3)
        self.assertTrue(v2 < v3)
        self.assertFalse(v2 < v1)

    def test_capability_info_to_dict(self):
        """Test CapabilityInfo to_dict method"""
        capabilities = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            modules=True
        )

        caps_dict = capabilities.to_dict()

        self.assertIsInstance(caps_dict, dict)
        self.assertTrue(caps_dict["cpp23"])
        self.assertTrue(caps_dict["cpp20"])
        self.assertTrue(caps_dict["cpp17"])
        self.assertTrue(caps_dict["modules"])

    def test_capability_info_supports_cpp_standard(self):
        """Test CapabilityInfo supports_cpp_standard method"""
        capabilities = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True
        )

        self.assertTrue(capabilities.supports_cpp_standard("cpp23"))
        self.assertTrue(capabilities.supports_cpp_standard("cpp20"))
        self.assertTrue(capabilities.supports_cpp_standard("cpp17"))
        self.assertFalse(capabilities.supports_cpp_standard("cpp14"))

    def test_environment_info_to_dict(self):
        """Test EnvironmentInfo to_dict method"""
        env = EnvironmentInfo(
            path=r"C:\Program Files\Microsoft Visual Studio\2022",
            include_paths=[r"C:\Program Files\Microsoft Visual Studio\2022\VC\include"],
            library_paths=[r"C:\Program Files\Microsoft Visual Studio\2022\VC\lib"],
            environment_variables={"PATH": "test"}
        )

        env_dict = env.to_dict()

        self.assertIsInstance(env_dict, dict)
        self.assertEqual(env_dict["path"], r"C:\Program Files\Microsoft Visual Studio\2022")
        self.assertEqual(len(env_dict["include_paths"]), 1)
        self.assertEqual(len(env_dict["library_paths"]), 1)
        self.assertEqual(env_dict["environment_variables"]["PATH"], "test")


class TestParallelDetectorIntegration(unittest.TestCase):
    """Integration tests for ParallelDetector with real detector mocks"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ParallelDetector(max_workers=4)

    def tearDown(self):
        """Clean up after tests"""
        self.detector.clear_results()

    @patch('os.path.exists', return_value=True)
    def test_full_parallel_detection_workflow(self, mock_exists):
        """Test complete parallel detection workflow"""
        # Register all compiler type detectors
        def msvc_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MSVC,
                    version=VersionInfo(major=19, minor=40, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(cpp23=True, cpp20=True, cpp17=True),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ]

        def msvc_clang_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MSVC_CLANG,
                    version=VersionInfo(major=17, minor=0, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\Llvm\x64\bin\clang++.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(cpp23=True, cpp20=True, cpp17=True),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ]

        def mingw_gcc_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MINGW_GCC,
                    version=VersionInfo(major=13, minor=2, patch=0),
                    path=r"C:\msys64\ucrt64\bin\g++.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(cpp23=True, cpp20=True, cpp17=True),
                    environment=EnvironmentInfo(path=r"C:\msys64")
                )
            ]

        def mingw_clang_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MINGW_CLANG,
                    version=VersionInfo(major=17, minor=0, patch=0),
                    path=r"C:\msys64\clang64\bin\clang++.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(cpp23=True, cpp20=True, cpp17=True),
                    environment=EnvironmentInfo(path=r"C:\msys64")
                )
            ]

        # Register detectors
        self.detector.register_detector("msvc", msvc_detector)
        self.detector.register_detector("msvc_clang", msvc_clang_detector)
        self.detector.register_detector("mingw_gcc", mingw_gcc_detector)
        self.detector.register_detector("mingw_clang", mingw_clang_detector)

        # Detect all compilers in parallel
        summary = self.detector.detect_all_parallel()

        # Verify results
        self.assertEqual(summary.total_compilers, 4)
        self.assertEqual(summary.successful_detections, 4)
        self.assertEqual(summary.failed_detections, 0)
        self.assertEqual(len(summary.results), 4)

        # Verify each compiler type was detected
        self.assertIn("msvc", summary.results)
        self.assertIn("msvc_clang", summary.results)
        self.assertIn("mingw_gcc", summary.results)
        self.assertIn("mingw_clang", summary.results)

        # Verify all detections were successful
        for result in summary.results.values():
            self.assertTrue(result.success)
            self.assertIsNone(result.error)

        # Get statistics
        stats = self.detector.get_detection_statistics()
        self.assertEqual(stats["total_compilers"], 4)
        self.assertEqual(stats["successful_detections"], 4)
        self.assertEqual(stats["failed_detections"], 0)
        self.assertIn("compilers_by_type", stats)

    @patch('os.path.exists', return_value=True)
    def test_parallel_detection_with_mixed_success_failure(self, mock_exists):
        """Test parallel detection with some detectors failing"""
        def successful_detector() -> List[CompilerInfo]:
            return [
                CompilerInfo(
                    compiler_type=CompilerType.MSVC,
                    version=VersionInfo(major=19, minor=40, patch=0),
                    path=r"C:\Program Files\Microsoft Visual Studio\2022\VC\Tools\MSVC\Hostx64\x64\cl.exe",
                    architecture=Architecture.X64,
                    capabilities=CapabilityInfo(),
                    environment=EnvironmentInfo(path=r"C:\Program Files\Microsoft Visual Studio\2022")
                )
            ]

        def failing_detector() -> List[CompilerInfo]:
            raise RuntimeError("Detection failed")

        self.detector.register_detector("msvc", successful_detector)
        self.detector.register_detector("mingw_gcc", failing_detector)

        summary = self.detector.detect_all_parallel()

        self.assertEqual(summary.total_compilers, 1)
        self.assertEqual(summary.successful_detections, 1)
        self.assertEqual(summary.failed_detections, 1)
        self.assertEqual(len(summary.errors), 1)
        self.assertIsNotNone(summary.errors[0])

    def test_parallel_detection_error_handling(self):
        """Test parallel detection error handling"""
        def exception_detector() -> List[CompilerInfo]:
            raise ValueError("Invalid configuration")

        self.detector.register_detector("msvc", exception_detector)

        result = self.detector.detect_compiler_parallel("msvc")

        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)
        self.assertIsNotNone(result.error)


if __name__ == "__main__":
    unittest.main()
