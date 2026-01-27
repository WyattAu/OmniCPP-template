"""
Unit tests for OmniCpp build system modules.

This module contains comprehensive unit tests for all build system components
including OmniCppController, build module, cmake module, conan module, and utils.
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from omni_scripts.build import BuildContext, BuildManager, BuildError
from omni_scripts.cmake import CMakeManager, CMakeError
from omni_scripts.conan import ConanManager, ConanError
from omni_scripts.utils import (
    run_command,
    validate_compiler,
    detect_platform,
    get_compiler_path,
    format_duration,
    sanitize_filename
)


class TestBuildContext(unittest.TestCase):
    """Test cases for BuildContext class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.context = BuildContext(
            target="standalone",
            build_type="debug",
            compiler="msvc",
            preset="default"
        )
    
    def test_build_context_initialization(self):
        """Test that BuildContext initializes correctly."""
        self.assertEqual(self.context.target, "standalone")
        self.assertEqual(self.context.build_type, "debug")
        self.assertEqual(self.context.compiler, "msvc")
        self.assertEqual(self.context.preset, "default")
    
    def test_build_context_to_dict(self):
        """Test conversion of BuildContext to dictionary."""
        result = self.context.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["target"], "standalone")
        self.assertEqual(result["build_type"], "debug")
    
    def test_build_context_from_dict(self):
        """Test creation of BuildContext from dictionary."""
        data = {
            "target": "standalone",
            "build_type": "release",
            "compiler": "mingw-gcc",
            "preset": "default"
        }
        context = BuildContext.from_dict(data)
        self.assertEqual(context.target, "standalone")
        self.assertEqual(context.build_type, "release")
        self.assertEqual(context.compiler, "mingw-gcc")


class TestBuildManager(unittest.TestCase):
    """Test cases for BuildManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = BuildManager()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_build_manager_initialization(self):
        """Test that BuildManager initializes correctly."""
        self.assertIsNotNone(self.manager)
    
    @patch('omni_scripts.build.run_command')
    def test_configure_build(self, mock_run):
        """Test build configuration."""
        mock_run.return_value = (0, "", "")
        context = BuildContext(
            target="standalone",
            build_type="debug",
            compiler="msvc",
            preset="default"
        )
        
        result = self.manager.configure(context)
        self.assertTrue(result)
    
    @patch('omni_scripts.build.run_command')
    def test_build_project(self, mock_run):
        """Test project building."""
        mock_run.return_value = (0, "", "")
        context = BuildContext(
            target="standalone",
            build_type="debug",
            compiler="msvc",
            preset="default"
        )
        
        result = self.manager.build(context)
        self.assertTrue(result)
    
    @patch('omni_scripts.build.run_command')
    def test_clean_build(self, mock_run):
        """Test clean build."""
        mock_run.return_value = (0, "", "")
        context = BuildContext(
            target="standalone",
            build_type="debug",
            compiler="msvc",
            preset="default"
        )
        
        result = self.manager.clean(context)
        self.assertTrue(result)


class TestCMakeManager(unittest.TestCase):
    """Test cases for CMakeManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = CMakeManager()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_cmake_manager_initialization(self):
        """Test that CMakeManager initializes correctly."""
        self.assertIsNotNone(self.manager)
    
    @patch('omni_scripts.cmake.run_command')
    def test_generate(self, mock_run):
        """Test CMake generation."""
        mock_run.return_value = (0, "", "")
        
        result = self.manager.generate(
            source_dir=".",
            build_dir=self.temp_dir,
            preset="default",
            toolchain=None
        )
        self.assertTrue(result)
    
    @patch('omni_scripts.cmake.run_command')
    def test_build(self, mock_run):
        """Test CMake build."""
        mock_run.return_value = (0, "", "")
        
        result = self.manager.build(
            build_dir=self.temp_dir,
            target="all",
            config="debug"
        )
        self.assertTrue(result)
    
    @patch('omni_scripts.cmake.run_command')
    def test_install(self, mock_run):
        """Test CMake install."""
        mock_run.return_value = (0, "", "")
        
        result = self.manager.install(
            build_dir=self.temp_dir,
            config="debug"
        )
        self.assertTrue(result)


class TestConanManager(unittest.TestCase):
    """Test cases for ConanManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = ConanManager()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_conan_manager_initialization(self):
        """Test that ConanManager initializes correctly."""
        self.assertIsNotNone(self.manager)
    
    @patch('omni_scripts.conan.run_command')
    def test_install(self, mock_run):
        """Test Conan install."""
        mock_run.return_value = (0, "", "")
        
        result = self.manager.install(
            profile="default",
            build_type="debug",
            settings=None
        )
        self.assertTrue(result)
    
    @patch('omni_scripts.conan.run_command')
    def test_create_profile(self, mock_run):
        """Test Conan profile creation."""
        mock_run.return_value = (0, "", "")
        
        result = self.manager.create_profile(
            name="test_profile",
            settings={"compiler": "msvc", "build_type": "Debug"}
        )
        self.assertTrue(result)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    @patch('omni_scripts.utils.subprocess.run')
    def test_run_command_success(self, mock_run):
        """Test successful command execution."""
        mock_process = Mock()
        mock_process.returncode = 0
        mock_process.stdout = "output"
        mock_process.stderr = ""
        mock_run.return_value = mock_process
        
        returncode, stdout, stderr = run_command("echo test")
        self.assertEqual(returncode, 0)
        self.assertEqual(stdout, "output")
    
    @patch('omni_scripts.utils.subprocess.run')
    def test_run_command_failure(self, mock_run):
        """Test failed command execution."""
        mock_process = Mock()
        mock_process.returncode = 1
        mock_process.stdout = ""
        mock_process.stderr = "error"
        mock_run.return_value = mock_process
        
        returncode, stdout, stderr = run_command("false")
        self.assertEqual(returncode, 1)
        self.assertEqual(stderr, "error")
    
    def test_detect_platform(self):
        """Test platform detection."""
        platform = detect_platform()
        self.assertIn(platform, ["windows", "linux", "macos"])
    
    def test_format_duration(self):
        """Test duration formatting."""
        self.assertEqual(format_duration(0), "0s")
        self.assertEqual(format_duration(60), "1m 0s")
        self.assertEqual(format_duration(3661), "1h 1m 1s")
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        self.assertEqual(sanitize_filename("test/file"), "test_file")
        self.assertEqual(sanitize_filename("test:file"), "test_file")
        self.assertEqual(sanitize_filename("test file"), "test_file")


class TestBuildError(unittest.TestCase):
    """Test cases for BuildError exception."""
    
    def test_build_error_creation(self):
        """Test BuildError creation."""
        error = BuildError("Test error message")
        self.assertEqual(str(error), "Test error message")
    
    def test_build_error_inheritance(self):
        """Test that BuildError inherits from Exception."""
        error = BuildError("Test")
        self.assertIsInstance(error, Exception)


class TestCMakeError(unittest.TestCase):
    """Test cases for CMakeError exception."""
    
    def test_cmake_error_creation(self):
        """Test CMakeError creation."""
        error = CMakeError("CMake error")
        self.assertEqual(str(error), "CMake error")
    
    def test_cmake_error_inheritance(self):
        """Test that CMakeError inherits from Exception."""
        error = CMakeError("Test")
        self.assertIsInstance(error, Exception)


class TestConanError(unittest.TestCase):
    """Test cases for ConanError exception."""
    
    def test_conan_error_creation(self):
        """Test ConanError creation."""
        error = ConanError("Conan error")
        self.assertEqual(str(error), "Conan error")
    
    def test_conan_error_inheritance(self):
        """Test that ConanError inherits from Exception."""
        error = ConanError("Test")
        self.assertIsInstance(error, Exception)


if __name__ == '__main__':
    unittest.main()
