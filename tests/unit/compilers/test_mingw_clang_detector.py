"""
Unit tests for MinGW-Clang Compiler Detector
"""

import os
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from compilers.mingw_clang_detector import (
    MinGWClangDetector,
    CompilerType,
    Architecture,
    VersionInfo,
    CapabilityInfo,
    EnvironmentInfo,
    CompilerInfo,
    ValidationResult
)


class TestMinGWClangDetector(unittest.TestCase):
    """Test cases for MinGWClangDetector"""

    def setUp(self):
        """Set up test fixtures"""
        self.logger = Mock()
        self.detector = MinGWClangDetector(logger=self.logger)

    def test_detector_initialization(self):
        """Test detector initialization"""
        self.assertIsNotNone(self.detector)
        self.assertIsNotNone(self.detector._logger)
        self.assertIsInstance(self.detector._msys2_paths, list)
        self.assertIsInstance(self.detector._standalone_paths, list)
        self.assertIsInstance(self.detector._package_manager_paths, dict)

    def test_msys2_environments_config(self):
        """Test MSYS2 environment configurations"""
        self.assertIn("UCRT64", MinGWClangDetector.MSYS2_ENVIRONMENTS)
        self.assertIn("MINGW64", MinGWClangDetector.MSYS2_ENVIRONMENTS)
        self.assertIn("CLANG64", MinGWClangDetector.MSYS2_ENVIRONMENTS)

        # Check UCRT64 configuration
        ucrt64_config = MinGWClangDetector.MSYS2_ENVIRONMENTS["UCRT64"]
        self.assertEqual(ucrt64_config["bin_path"], "ucrt64/bin")
        self.assertEqual(ucrt64_config["msystem"], "UCRT64")
        self.assertEqual(ucrt64_config["mingw_prefix"], "/ucrt64")
        self.assertEqual(ucrt64_config["mingw_chost"], "x86_64-w64-mingw32")
        self.assertEqual(ucrt64_config["architecture"], Architecture.X64)
        self.assertTrue(ucrt64_config["recommended"])

        # Check MINGW64 configuration
        mingw64_config = MinGWClangDetector.MSYS2_ENVIRONMENTS["MINGW64"]
        self.assertEqual(mingw64_config["bin_path"], "mingw64/bin")
        self.assertEqual(mingw64_config["msystem"], "MINGW64")
        self.assertEqual(mingw64_config["mingw_prefix"], "/mingw64")
        self.assertEqual(mingw64_config["mingw_chost"], "x86_64-w64-mingw32")
        self.assertEqual(mingw64_config["architecture"], Architecture.X64)
        self.assertFalse(mingw64_config["recommended"])

        # Check CLANG64 configuration
        clang64_config = MinGWClangDetector.MSYS2_ENVIRONMENTS["CLANG64"]
        self.assertEqual(clang64_config["bin_path"], "clang64/bin")
        self.assertEqual(clang64_config["msystem"], "CLANG64")
        self.assertEqual(clang64_config["mingw_prefix"], "/clang64")
        self.assertEqual(clang64_config["mingw_chost"], "x86_64-w64-mingw32")
        self.assertEqual(clang64_config["architecture"], Architecture.X64)
        self.assertFalse(clang64_config["recommended"])

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_version_success(self, mock_run, mock_exists):
        """Test successful version detection"""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="clang version 18.1.3 (https://github.com/llvm/llvm-project.git)\n",
            stderr=""
        )

        version = self.detector.detect_version("C:\\LLVM\\bin\\clang++.exe")

        self.assertIsNotNone(version)
        self.assertEqual(version.major, 18)
        self.assertEqual(version.minor, 1)
        self.assertEqual(version.patch, 3)
        self.assertEqual(str(version), "18.1.3")

    @patch('os.path.exists')
    def test_detect_version_file_not_found(self, mock_exists):
        """Test version detection when file not found"""
        mock_exists.return_value = False

        version = self.detector.detect_version("C:\\LLVM\\bin\\clang++.exe")

        self.assertIsNone(version)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_version_command_fails(self, mock_run, mock_exists):
        """Test version detection when command fails"""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=1,
            stdout="",
            stderr="Error executing clang++.exe"
        )

        version = self.detector.detect_version("C:\\LLVM\\bin\\clang++.exe")

        self.assertIsNone(version)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_capabilities_clang18(self, mock_run, mock_exists):
        """Test capability detection for Clang 18"""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="clang version 18.1.3\n",
            stderr=""
        )

        capabilities = self.detector.detect_capabilities("C:\\LLVM\\bin\\clang++.exe")

        self.assertTrue(capabilities.cpp23)
        self.assertTrue(capabilities.cpp20)
        self.assertTrue(capabilities.cpp17)
        self.assertTrue(capabilities.cpp14)
        self.assertTrue(capabilities.modules)
        self.assertTrue(capabilities.coroutines)
        self.assertTrue(capabilities.concepts)
        self.assertTrue(capabilities.ranges)
        self.assertTrue(capabilities.std_format)
        self.assertTrue(capabilities.mingw_compatibility)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_capabilities_clang17(self, mock_run, mock_exists):
        """Test capability detection for Clang 17"""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="clang version 17.0.6\n",
            stderr=""
        )

        capabilities = self.detector.detect_capabilities("C:\\LLVM\\bin\\clang++.exe")

        self.assertFalse(capabilities.cpp23)
        self.assertTrue(capabilities.cpp20)
        self.assertTrue(capabilities.cpp17)
        self.assertTrue(capabilities.cpp14)
        self.assertTrue(capabilities.modules)
        self.assertTrue(capabilities.coroutines)
        self.assertTrue(capabilities.concepts)
        self.assertTrue(capabilities.ranges)
        self.assertTrue(capabilities.std_format)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_capabilities_clang16(self, mock_run, mock_exists):
        """Test capability detection for Clang 16"""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="clang version 16.0.6\n",
            stderr=""
        )

        capabilities = self.detector.detect_capabilities("C:\\LLVM\\bin\\clang++.exe")

        self.assertFalse(capabilities.cpp23)
        self.assertFalse(capabilities.cpp20)
        self.assertTrue(capabilities.cpp17)
        self.assertTrue(capabilities.cpp14)
        self.assertTrue(capabilities.modules)
        self.assertTrue(capabilities.coroutines)
        self.assertTrue(capabilities.concepts)
        self.assertTrue(capabilities.ranges)
        self.assertTrue(capabilities.std_format)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_validate_success(self, mock_run, mock_exists):
        """Test successful compiler validation"""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="clang version 18.1.3\n",
            stderr=""
        )

        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MINGW_CLANG,
            version=VersionInfo(major=18, minor=1, patch=3),
            path="C:\\LLVM\\bin\\clang++.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="C:\\LLVM"),
            metadata={"environment": "UCRT64"}
        )

        result = self.detector.validate(compiler_info)

        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    @patch('os.path.exists')
    def test_validate_file_not_found(self, mock_exists):
        """Test validation when file not found"""
        mock_exists.return_value = False

        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MINGW_CLANG,
            version=VersionInfo(major=18, minor=1, patch=3),
            path="C:\\LLVM\\bin\\clang++.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="C:\\LLVM"),
            metadata={}
        )

        result = self.detector.validate(compiler_info)

        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertIn("Compiler executable not found", result.errors[0])

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_validate_command_fails(self, mock_run, mock_exists):
        """Test validation when command fails"""
        mock_exists.return_value = True
        mock_run.return_value = Mock(
            returncode=1,
            stdout="",
            stderr="Error executing clang++.exe"
        )

        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MINGW_CLANG,
            version=VersionInfo(major=18, minor=1, patch=3),
            path="C:\\LLVM\\bin\\clang++.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="C:\\LLVM"),
            metadata={}
        )

        result = self.detector.validate(compiler_info)

        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertIn("Compiler executable is not functional", result.errors[0])

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_via_msys2_ucrt64(self, mock_run, mock_exists):
        """Test MSYS2 UCRT64 detection"""
        # Mock file existence
        def exists_side_effect(path):
            if "C:\\msys64" in path:
                return True
            if "clang++.exe" in path and "ucrt64" in path.lower():
                return True
            return False

        mock_exists.side_effect = exists_side_effect
        mock_run.return_value = Mock(
            returncode=0,
            stdout="clang version 18.1.3\n",
            stderr=""
        )

        compilers = self.detector._detect_via_msys2()

        self.assertGreater(len(compilers), 0)

        # Check UCRT64 compiler
        ucrt64_compilers = [c for c in compilers if c.metadata.get("environment") == "UCRT64"]
        self.assertGreater(len(ucrt64_compilers), 0)

        compiler = ucrt64_compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_CLANG)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "msys2")
        self.assertEqual(compiler.metadata["environment"], "UCRT64")
        self.assertEqual(compiler.metadata["msystem"], "UCRT64")
        self.assertEqual(compiler.metadata["mingw_prefix"], "/ucrt64")
        self.assertEqual(compiler.metadata["mingw_chost"], "x86_64-w64-mingw32")
        self.assertEqual(compiler.metadata["recommended"], "true")

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_via_msys2_mingw64(self, mock_run, mock_exists):
        """Test MSYS2 MINGW64 detection"""
        # Mock file existence
        def exists_side_effect(path):
            if "C:\\msys64" in path:
                return True
            if "clang++.exe" in path and "mingw64" in path.lower():
                return True
            return False

        mock_exists.side_effect = exists_side_effect
        mock_run.return_value = Mock(
            returncode=0,
            stdout="clang version 18.1.3\n",
            stderr=""
        )

        compilers = self.detector._detect_via_msys2()

        # Check MINGW64 compiler
        mingw64_compilers = [c for c in compilers if c.metadata.get("environment") == "MINGW64"]
        self.assertGreater(len(mingw64_compilers), 0)

        compiler = mingw64_compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_CLANG)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "msys2")
        self.assertEqual(compiler.metadata["environment"], "MINGW64")
        self.assertEqual(compiler.metadata["msystem"], "MINGW64")
        self.assertEqual(compiler.metadata["mingw_prefix"], "/mingw64")
        self.assertEqual(compiler.metadata["mingw_chost"], "x86_64-w64-mingw32")
        self.assertEqual(compiler.metadata["recommended"], "false")

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_via_msys2_clang64(self, mock_run, mock_exists):
        """Test MSYS2 CLANG64 detection"""
        # Mock file existence
        def exists_side_effect(path):
            if "C:\\msys64" in path:
                return True
            if "clang++.exe" in path and "clang64" in path.lower():
                return True
            return False

        mock_exists.side_effect = exists_side_effect
        mock_run.return_value = Mock(
            returncode=0,
            stdout="clang version 18.1.3\n",
            stderr=""
        )

        compilers = self.detector._detect_via_msys2()

        # Check CLANG64 compiler
        clang64_compilers = [c for c in compilers if c.metadata.get("environment") == "CLANG64"]
        self.assertGreater(len(clang64_compilers), 0)

        compiler = clang64_compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_CLANG)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "msys2")
        self.assertEqual(compiler.metadata["environment"], "CLANG64")
        self.assertEqual(compiler.metadata["msystem"], "CLANG64")
        self.assertEqual(compiler.metadata["mingw_prefix"], "/clang64")
        self.assertEqual(compiler.metadata["mingw_chost"], "x86_64-w64-mingw32")
        self.assertEqual(compiler.metadata["recommended"], "false")

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_standalone(self, mock_run, mock_exists):
        """Test standalone LLVM detection"""
        # Mock file existence
        def exists_side_effect(path):
            if "C:\\LLVM" in path:
                return True
            if "clang++.exe" in path:
                return True
            return False

        mock_exists.side_effect = exists_side_effect
        mock_run.return_value = Mock(
            returncode=0,
            stdout="clang version 18.1.3\n",
            stderr=""
        )

        compilers = self.detector._detect_standalone()

        self.assertGreater(len(compilers), 0)

        compiler = compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_CLANG)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "standalone")
        self.assertEqual(compiler.metadata["detection_method"], "standard_paths")

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_chocolatey_llvm(self, mock_run, mock_exists):
        """Test Chocolatey LLVM detection"""
        # Mock file existence
        def exists_side_effect(path):
            if "chocolatey" in path.lower() and "llvm" in path.lower():
                return True
            if "clang++.exe" in path:
                return True
            return False

        mock_exists.side_effect = exists_side_effect
        mock_run.return_value = Mock(
            returncode=0,
            stdout="clang version 18.1.3\n",
            stderr=""
        )

        compilers = self.detector._detect_chocolatey_llvm()

        self.assertGreater(len(compilers), 0)

        compiler = compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_CLANG)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "package_manager")
        self.assertEqual(compiler.metadata["package_manager"], "chocolatey")
        self.assertEqual(compiler.metadata["detection_method"], "package_manager")

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_scoop_llvm(self, mock_run, mock_exists):
        """Test Scoop LLVM detection"""
        # Mock file existence
        def exists_side_effect(path):
            if "scoop" in path.lower() and "llvm" in path.lower():
                return True
            if "clang++.exe" in path:
                return True
            return False

        mock_exists.side_effect = exists_side_effect
        mock_run.return_value = Mock(
            returncode=0,
            stdout="clang version 18.1.3\n",
            stderr=""
        )

        compilers = self.detector._detect_scoop_llvm()

        self.assertGreater(len(compilers), 0)

        compiler = compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_CLANG)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "package_manager")
        self.assertEqual(compiler.metadata["package_manager"], "scoop")
        self.assertEqual(compiler.metadata["detection_method"], "package_manager")

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_winget_llvm(self, mock_run, mock_exists):
        """Test winget LLVM detection"""
        # Mock file existence
        def exists_side_effect(path):
            if "Program Files" in path and "LLVM" in path:
                return True
            if "clang++.exe" in path:
                return True
            return False

        mock_exists.side_effect = exists_side_effect
        mock_run.return_value = Mock(
            returncode=0,
            stdout="clang version 18.1.3\n",
            stderr=""
        )

        compilers = self.detector._detect_winget_llvm()

        self.assertGreater(len(compilers), 0)

        compiler = compilers[0]
        self.assertEqual(compiler.compiler_type, CompilerType.MINGW_CLANG)
        self.assertEqual(compiler.architecture, Architecture.X64)
        self.assertEqual(compiler.metadata["installation_type"], "package_manager")
        self.assertEqual(compiler.metadata["package_manager"], "winget")
        self.assertEqual(compiler.metadata["detection_method"], "package_manager")

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_via_package_managers(self, mock_run, mock_exists):
        """Test package manager detection"""
        # Mock file existence
        def exists_side_effect(path):
            if "chocolatey" in path.lower() or "scoop" in path.lower() or "LLVM" in path:
                return True
            if "clang++.exe" in path:
                return True
            return False

        mock_exists.side_effect = exists_side_effect
        mock_run.return_value = Mock(
            returncode=0,
            stdout="clang version 18.1.3\n",
            stderr=""
        )

        compilers = self.detector._detect_via_package_managers()

        # Should find compilers from all package managers
        self.assertGreater(len(compilers), 0)

        # Check that we have different package managers
        package_managers = set(c.metadata.get("package_manager") for c in compilers)
        self.assertTrue(len(package_managers) > 0)

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_detect_all(self, mock_run, mock_exists):
        """Test full detection process"""
        # Mock file existence
        def exists_side_effect(path):
            if "msys64" in path or "LLVM" in path or "chocolatey" in path.lower():
                return True
            if "clang++.exe" in path:
                return True
            return False

        mock_exists.side_effect = exists_side_effect
        mock_run.return_value = Mock(
            returncode=0,
            stdout="clang version 18.1.3\n",
            stderr=""
        )

        compilers = self.detector.detect()

        self.assertGreater(len(compilers), 0)

        # Check that first compiler is marked as recommended
        self.assertEqual(compilers[0].metadata.get("recommended"), "true")

        # Check that compilers are sorted by version
        if len(compilers) > 1:
            for i in range(len(compilers) - 1):
                self.assertGreaterEqual(
                    compilers[i].version.major,
                    compilers[i + 1].version.major
                )

    def test_version_info_comparison(self):
        """Test VersionInfo comparison"""
        v1 = VersionInfo(major=18, minor=1, patch=3)
        v2 = VersionInfo(major=17, minor=0, patch=0)
        v3 = VersionInfo(major=18, minor=1, patch=3)

        self.assertTrue(v2 < v1)
        self.assertFalse(v1 < v3)
        self.assertFalse(v3 < v1)

    def test_version_info_string_representation(self):
        """Test VersionInfo string representation"""
        v1 = VersionInfo(major=18, minor=1, patch=3)
        self.assertEqual(str(v1), "18.1.3")

        v2 = VersionInfo(major=18, minor=1, patch=3, build="12345")
        self.assertEqual(str(v2), "18.1.3.12345")

    def test_capability_info_to_dict(self):
        """Test CapabilityInfo to_dict method"""
        capabilities = CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            modules=True,
            mingw_compatibility=True
        )

        caps_dict = capabilities.to_dict()

        self.assertTrue(caps_dict["cpp23"])
        self.assertTrue(caps_dict["cpp20"])
        self.assertTrue(caps_dict["cpp17"])
        self.assertTrue(caps_dict["modules"])
        self.assertTrue(caps_dict["mingw_compatibility"])

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
        env_info = EnvironmentInfo(
            path="C:\\LLVM",
            include_paths=["C:\\LLVM\\include"],
            library_paths=["C:\\LLVM\\lib"],
            environment_variables={"MSYSTEM": "UCRT64"}
        )

        env_dict = env_info.to_dict()

        self.assertEqual(env_dict["path"], "C:\\LLVM")
        self.assertEqual(env_dict["include_paths"], ["C:\\LLVM\\include"])
        self.assertEqual(env_dict["library_paths"], ["C:\\LLVM\\lib"])
        self.assertEqual(env_dict["environment_variables"], {"MSYSTEM": "UCRT64"})

    def test_compiler_info_to_dict(self):
        """Test CompilerInfo to_dict method"""
        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MINGW_CLANG,
            version=VersionInfo(major=18, minor=1, patch=3),
            path="C:\\LLVM\\bin\\clang++.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="C:\\LLVM"),
            metadata={"installation_type": "standalone"}
        )

        info_dict = compiler_info.to_dict()

        self.assertEqual(info_dict["compiler_type"], "mingw_clang")
        self.assertEqual(info_dict["version"], "18.1.3")
        self.assertEqual(info_dict["path"], "C:\\LLVM\\bin\\clang++.exe")
        self.assertEqual(info_dict["architecture"], "x64")
        self.assertEqual(info_dict["metadata"]["installation_type"], "standalone")

    def test_compiler_info_is_valid(self):
        """Test CompilerInfo is_valid method"""
        compiler_info = CompilerInfo(
            compiler_type=CompilerType.MINGW_CLANG,
            version=VersionInfo(major=18, minor=1, patch=3),
            path="C:\\LLVM\\bin\\clang++.exe",
            architecture=Architecture.X64,
            capabilities=CapabilityInfo(),
            environment=EnvironmentInfo(path="C:\\LLVM"),
            metadata={}
        )

        # Mock os.path.exists
        with patch('os.path.exists', return_value=True):
            self.assertTrue(compiler_info.is_valid())

        with patch('os.path.exists', return_value=False):
            self.assertFalse(compiler_info.is_valid())

    def test_validation_result_to_dict(self):
        """Test ValidationResult to_dict method"""
        result = ValidationResult(
            is_valid=True,
            errors=[],
            warnings=["MSYSTEM environment variable not set"]
        )

        result_dict = result.to_dict()

        self.assertTrue(result_dict["is_valid"])
        self.assertEqual(result_dict["errors"], [])
        self.assertEqual(result_dict["warnings"], ["MSYSTEM environment variable not set"])

    def test_get_msys2_paths(self):
        """Test MSYS2 path generation"""
        paths = self.detector._get_msys2_paths()

        self.assertIsInstance(paths, list)
        self.assertGreater(len(paths), 0)
        self.assertIn(r"C:\msys64", paths)
        self.assertIn(r"C:\msys32", paths)

    def test_get_standalone_paths(self):
        """Test standalone LLVM path generation"""
        paths = self.detector._get_standalone_paths()

        self.assertIsInstance(paths, list)
        self.assertGreater(len(paths), 0)
        self.assertIn(r"C:\LLVM", paths)

    def test_get_package_manager_paths(self):
        """Test package manager path generation"""
        paths = self.detector._get_package_manager_paths()

        self.assertIsInstance(paths, dict)
        self.assertIn("chocolatey", paths)
        self.assertIn("scoop", paths)
        self.assertIn("winget", paths)

        # Check that each package manager has a list of paths
        for pkg_manager, pkg_paths in paths.items():
            self.assertIsInstance(pkg_paths, list)
            self.assertGreater(len(pkg_paths), 0)


if __name__ == '__main__':
    unittest.main()
