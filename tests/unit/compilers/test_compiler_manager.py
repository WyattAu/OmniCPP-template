"""
Unit tests for CompilerManager

Tests compiler detection, validation, and selection operations.
"""

import pytest
from unittest.mock import Mock
import logging

from scripts.python.compilers.compiler_manager import CompilerManager
from scripts.python.compilers.compiler_factory import CompilerFactory, CompilerRequirements
from scripts.python.compilers.msvc_detector import (
    CompilerInfo,
    CompilerType,
    Architecture,
    VersionInfo,
    CapabilityInfo,
    EnvironmentInfo
)


@pytest.fixture
def mock_logger() -> Mock:
    """Create a mock logger"""
    return Mock(spec=logging.Logger)


@pytest.fixture
def mock_factory() -> Mock:
    """Create a mock CompilerFactory"""
    factory = Mock(spec=CompilerFactory)
    factory._detectors = {}
    factory._cache = {}
    return factory


@pytest.fixture
def sample_compiler_info() -> CompilerInfo:
    """Create sample CompilerInfo for testing"""
    return CompilerInfo(
        compiler_type=CompilerType.MSVC,
        version=VersionInfo(major=19, minor=40, patch=0),
        path=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.40.33807\bin\Hostx64\x64\cl.exe",
        architecture=Architecture.X64,
        capabilities=CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            modules=True,
            coroutines=True,
            concepts=True,
            ranges=True,
            std_format=True
        ),
        environment=EnvironmentInfo(
            path=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.40.33807\bin\Hostx64\x64",
            include_paths=[],
            library_paths=[],
            environment_variables={}
        ),
        metadata={"installation_path": r"C:\Program Files\Microsoft Visual Studio\2022\Community"}
    )


@pytest.fixture
def sample_compiler_info_mingw() -> CompilerInfo:
    """Create sample MinGW CompilerInfo for testing"""
    return CompilerInfo(
        compiler_type=CompilerType.MINGW_GCC,
        version=VersionInfo(major=13, minor=2, patch=0),
        path=r"C:\msys64\ucrt64\bin\gcc.exe",
        architecture=Architecture.X64,
        capabilities=CapabilityInfo(
            cpp23=True,
            cpp20=True,
            cpp17=True,
            modules=True,
            coroutines=True,
            concepts=True,
            ranges=True,
            std_format=True
        ),
        environment=EnvironmentInfo(
            path=r"C:\msys64\ucrt64\bin",
            include_paths=[],
            library_paths=[],
            environment_variables={}
        ),
        metadata={"msys2_path": r"C:\msys64", "environment": "UCRT64"}
    )


@pytest.fixture
def compiler_manager(mock_factory: Mock, mock_logger: Mock) -> CompilerManager:
    """Create CompilerManager instance for testing"""
    return CompilerManager(factory=mock_factory, logger=mock_logger)


class TestCompilerManagerInitialization:
    """Test CompilerManager initialization"""

    def test_initialization(self, mock_factory: Mock, mock_logger: Mock):
        """Test that CompilerManager initializes correctly"""
        manager = CompilerManager(factory=mock_factory, logger=mock_logger)
        
        assert manager._factory == mock_factory
        assert manager._logger == mock_logger
        mock_logger.debug.assert_called_with("CompilerManager initialized")

    def test_initialization_without_logger(self, mock_factory: Mock):
        """Test that CompilerManager creates default logger if none provided"""
        manager = CompilerManager(factory=mock_factory)
        
        assert manager._factory == mock_factory
        assert manager._logger is not None
        assert isinstance(manager._logger, logging.Logger)


class TestDetectAll:
    """Test detect_all method"""

    def test_detect_all_success(
        self,
        compiler_manager: CompilerManager,
        mock_factory: Mock,
        sample_compiler_info: CompilerInfo
    ):
        """Test successful detection of all compilers"""
        # Setup mock
        mock_factory.get_available_compilers.return_value = {
            "msvc": [sample_compiler_info],
            "mingw_gcc": []
        }
        
        # Execute
        result = compiler_manager.detect_all()
        
        # Verify
        assert "msvc" in result
        assert "mingw_gcc" in result
        assert len(result["msvc"]) == 1
        assert result["msvc"][0] == sample_compiler_info
        mock_factory.get_available_compilers.assert_called_once()
        mock_logger = compiler_manager._logger
        assert mock_logger.info.called
        assert "Detection complete" in str(mock_logger.info.call_args)

    def test_detect_all_empty(self, compiler_manager: CompilerManager, mock_factory: Mock):
        """Test detection when no compilers found"""
        # Setup mock
        mock_factory.get_available_compilers.return_value = {}
        
        # Execute
        result = compiler_manager.detect_all()
        
        # Verify
        assert result == {}
        mock_factory.get_available_compilers.assert_called_once()

    def test_detect_all_exception(self, compiler_manager: CompilerManager, mock_factory: Mock):
        """Test detection when factory raises exception"""
        # Setup mock
        mock_factory.get_available_compilers.side_effect = Exception("Detection failed")
        
        # Execute and verify exception
        with pytest.raises(Exception, match="Detection failed"):
            compiler_manager.detect_all()
        
        mock_logger = compiler_manager._logger
        mock_logger.error.assert_called()


class TestDetectCompiler:
    """Test detect_compiler method"""

    def test_detect_compiler_success(
        self,
        compiler_manager: CompilerManager,
        mock_factory: Mock,
        sample_compiler_info: CompilerInfo
    ):
        """Test successful detection of specific compiler type"""
        # Setup mock
        mock_factory.get_available_compilers.return_value = {
            "msvc": [sample_compiler_info]
        }
        
        # Execute
        result = compiler_manager.detect_compiler("msvc")
        
        # Verify
        assert len(result) == 1
        assert result[0] == sample_compiler_info
        mock_factory.get_available_compilers.assert_called_once()

    def test_detect_compiler_not_found(self, compiler_manager: CompilerManager, mock_factory: Mock):
        """Test detection when detector not found"""
        # Setup mock
        mock_factory.get_available_compilers.return_value = {}
        
        # Execute
        result = compiler_manager.detect_compiler("unknown")
        
        # Verify
        assert result == []
        mock_factory.get_available_compilers.assert_called_once()

    def test_detect_compiler_empty_type(self, compiler_manager: CompilerManager):
        """Test detection with empty compiler type"""
        # Execute and verify exception
        with pytest.raises(ValueError, match="Compiler type cannot be empty"):
            compiler_manager.detect_compiler("")

    def test_detect_compiler_exception(self, compiler_manager: CompilerManager, mock_factory: Mock):
        """Test detection when detector raises exception"""
        # Setup mock
        mock_factory.get_available_compilers.side_effect = Exception("Detector failed")
        
        # Execute and verify exception
        with pytest.raises(Exception, match="Detector failed"):
            compiler_manager.detect_compiler("msvc")


class TestValidateCompiler:
    """Test validate_compiler method"""

    def test_validate_compiler_success(
        self,
        compiler_manager: CompilerManager,
        mock_factory: Mock,
        sample_compiler_info: CompilerInfo
    ):
        """Test successful compiler validation"""
        # Setup mock
        mock_factory.get_available_compilers.return_value = {
            "msvc": [sample_compiler_info]
        }
        
        # Execute
        result = compiler_manager.validate_compiler(sample_compiler_info)
        
        # Verify
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_compiler_failure(
        self,
        compiler_manager: CompilerManager,
        mock_factory: Mock,
        sample_compiler_info: CompilerInfo
    ):
        """Test compiler validation with errors"""
        # Setup mock - compiler doesn't exist
        mock_factory.get_available_compilers.return_value = {
            "msvc": [sample_compiler_info]
        }
        
        # Execute
        result = compiler_manager.validate_compiler(sample_compiler_info)
        
        # Verify - will fail because path doesn't exist
        assert result.is_valid is False
        assert len(result.errors) >= 1

    def test_validate_compiler_no_detector(
        self,
        compiler_manager: CompilerManager,
        mock_factory: Mock,
        sample_compiler_info: CompilerInfo
    ):
        """Test validation when detector not found"""
        # Setup mock
        mock_factory.get_available_compilers.return_value = {}
        
        # Execute
        result = compiler_manager.validate_compiler(sample_compiler_info)
        
        # Verify
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert "No detector found" in result.errors[0]


class TestGetCompiler:
    """Test get_compiler method"""

    def test_get_compiler_success(
        self,
        compiler_manager: CompilerManager,
        mock_factory: Mock,
        sample_compiler_info: CompilerInfo
    ):
        """Test successful retrieval of compiler"""
        # Setup mock
        mock_factory.create_compiler.return_value = sample_compiler_info
        
        # Execute
        result = compiler_manager.get_compiler("msvc", "x64")
        
        # Verify
        assert result == sample_compiler_info
        mock_factory.create_compiler.assert_called_once_with("msvc", "x64")

    def test_get_compiler_not_found(self, compiler_manager: CompilerManager, mock_factory: Mock):
        """Test retrieval when compiler not found"""
        # Setup mock
        mock_factory.create_compiler.return_value = None
        
        # Execute
        result = compiler_manager.get_compiler("msvc", "x64")
        
        # Verify
        assert result is None
        mock_factory.create_compiler.assert_called_once_with("msvc", "x64")

    def test_get_compiler_exception(self, compiler_manager: CompilerManager, mock_factory: Mock):
        """Test retrieval when factory raises exception"""
        # Setup mock
        mock_factory.create_compiler.side_effect = Exception("Factory failed")
        
        # Execute
        result = compiler_manager.get_compiler("msvc", "x64")
        
        # Verify
        assert result is None


class TestGetAllCompilers:
    """Test get_all_compilers method"""

    def test_get_all_compilers_cached(
        self,
        compiler_manager: CompilerManager,
        sample_compiler_info: CompilerInfo,
        sample_compiler_info_mingw: CompilerInfo
    ):
        """Test getting all compilers from cache"""
        # Setup cache
        compiler_manager._detected_compilers = {
            "msvc": [sample_compiler_info],
            "mingw_gcc": [sample_compiler_info_mingw]
        }
        
        # Execute
        result = compiler_manager.get_all_compilers()
        
        # Verify
        assert len(result) == 2
        assert "msvc" in result
        assert "mingw_gcc" in result
        assert result["msvc"][0] == sample_compiler_info
        assert result["mingw_gcc"][0] == sample_compiler_info_mingw

    def test_get_all_compilers_not_cached(
        self,
        compiler_manager: CompilerManager,
        mock_factory: Mock,
        sample_compiler_info: CompilerInfo
    ):
        """Test getting all compilers triggers detection when cache empty"""
        # Setup mock
        mock_factory.get_available_compilers.return_value = {
            "msvc": [sample_compiler_info]
        }
        
        # Execute
        result = compiler_manager.get_all_compilers()
        
        # Verify
        assert "msvc" in result
        mock_factory.get_available_compilers.assert_called_once()


class TestGetRecommendedCompiler:
    """Test get_recommended_compiler method"""

    def test_get_recommended_compiler_success(
        self,
        compiler_manager: CompilerManager,
        mock_factory: Mock,
        sample_compiler_info: CompilerInfo
    ):
        """Test successful recommendation of compiler"""
        # Setup mock
        mock_factory.select_best_compiler.return_value = sample_compiler_info
        
        # Execute
        result = compiler_manager.get_recommended_compiler("x64", "cpp23")
        
        # Verify
        assert result == sample_compiler_info
        
        # Verify requirements were built correctly
        call_args = mock_factory.select_best_compiler.call_args
        requirements = call_args[0][0]
        assert requirements.architecture == Architecture.X64
        assert requirements.required_capabilities == ["cpp23"]

    def test_get_recommended_compiler_no_match(
        self,
        compiler_manager: CompilerManager,
        mock_factory: Mock
    ):
        """Test recommendation when no suitable compiler found"""
        # Setup mock
        mock_factory.select_best_compiler.return_value = None
        
        # Execute
        result = compiler_manager.get_recommended_compiler("x64")
        
        # Verify
        assert result is None

    def test_get_recommended_compiler_exception(
        self,
        compiler_manager: CompilerManager,
        mock_factory: Mock
    ):
        """Test recommendation when factory raises exception"""
        # Setup mock
        mock_factory.select_best_compiler.side_effect = Exception("Selection failed")
        
        # Execute
        result = compiler_manager.get_recommended_compiler("x64")
        
        # Verify
        assert result is None


class TestGetCompilersByType:
    """Test get_compilers_by_type method"""

    def test_get_compilers_by_type_cached(
        self,
        compiler_manager: CompilerManager,
        sample_compiler_info: CompilerInfo
    ):
        """Test getting compilers by type from cache"""
        # Setup cache
        compiler_manager._detected_compilers = {
            "msvc": [sample_compiler_info]
        }
        
        # Execute
        result = compiler_manager.get_compilers_by_type("msvc")
        
        # Verify
        assert len(result) == 1
        assert result[0] == sample_compiler_info

    def test_get_compilers_by_type_not_cached(
        self,
        compiler_manager: CompilerManager,
        mock_factory: Mock,
        sample_compiler_info: CompilerInfo
    ):
        """Test getting compilers by type triggers detection when not cached"""
        # Setup mock
        mock_factory.get_available_compilers.return_value = {
            "msvc": [sample_compiler_info]
        }
        
        # Execute
        result = compiler_manager.get_compilers_by_type("msvc")
        
        # Verify
        assert len(result) == 1
        assert result[0] == sample_compiler_info
        mock_factory.get_available_compilers.assert_called_once()


class TestGetCompilersByArchitecture:
    """Test get_compilers_by_architecture method"""

    def test_get_compilers_by_architecture_success(
        self,
        compiler_manager: CompilerManager,
        sample_compiler_info: CompilerInfo,
        sample_compiler_info_mingw: CompilerInfo
    ):
        """Test getting compilers by architecture"""
        # Setup cache
        compiler_manager._detected_compilers = {
            "msvc": [sample_compiler_info],
            "mingw_gcc": [sample_compiler_info_mingw]
        }
        
        # Execute
        result = compiler_manager.get_compilers_by_architecture("x64")
        
        # Verify
        assert len(result) == 2
        assert sample_compiler_info in result
        assert sample_compiler_info_mingw in result

    def test_get_compilers_by_architecture_empty(
        self,
        compiler_manager: CompilerManager,
        sample_compiler_info: CompilerInfo
    ):
        """Test getting compilers by architecture when none match"""
        # Setup cache
        compiler_manager._detected_compilers = {
            "msvc": [sample_compiler_info]
        }
        
        # Execute
        result = compiler_manager.get_compilers_by_architecture("arm64")
        
        # Verify
        assert len(result) == 0

    def test_get_compilers_by_architecture_invalid(
        self,
        compiler_manager: CompilerManager,
        sample_compiler_info: CompilerInfo
    ):
        """Test getting compilers by architecture with invalid architecture"""
        # Setup cache
        compiler_manager._detected_compilers = {
            "msvc": [sample_compiler_info]
        }
        
        # Execute
        result = compiler_manager.get_compilers_by_architecture("invalid")
        
        # Verify
        assert len(result) == 0


class TestGetCompilersByCapability:
    """Test get_compilers_by_capability method"""

    def test_get_compilers_by_capability_success(
        self,
        compiler_manager: CompilerManager,
        sample_compiler_info: CompilerInfo,
        sample_compiler_info_mingw: CompilerInfo
    ):
        """Test getting compilers by capability"""
        # Setup cache
        compiler_manager._detected_compilers = {
            "msvc": [sample_compiler_info],
            "mingw_gcc": [sample_compiler_info_mingw]
        }
        
        # Execute
        result = compiler_manager.get_compilers_by_capability("cpp23")
        
        # Verify
        assert len(result) == 2
        assert sample_compiler_info in result
        assert sample_compiler_info_mingw in result

    def test_get_compilers_by_capability_none(
        self,
        compiler_manager: CompilerManager,
        sample_compiler_info: CompilerInfo
    ):
        """Test getting compilers by capability when none match"""
        # Setup cache with compiler that doesn't have the capability
        sample_compiler_info.capabilities.cpp23 = False
        compiler_manager._detected_compilers = {
            "msvc": [sample_compiler_info]
        }
        
        # Execute
        result = compiler_manager.get_compilers_by_capability("cpp23")
        
        # Verify
        assert len(result) == 0

    def test_get_compilers_by_capability_false(
        self,
        compiler_manager: CompilerManager,
        sample_compiler_info: CompilerInfo,
        sample_compiler_info_mingw: CompilerInfo
    ):
        """Test getting compilers that don't have a capability"""
        # Setup cache
        compiler_manager._detected_compilers = {
            "msvc": [sample_compiler_info],
            "mingw_gcc": [sample_compiler_info_mingw]
        }
        
        # Execute
        result = compiler_manager.get_compilers_by_capability("cpp23", value=False)
        
        # Verify
        assert len(result) == 0


class TestRefreshDetection:
    """Test refresh_detection method"""

    def test_refresh_detection_success(
        self,
        compiler_manager: CompilerManager,
        mock_factory: Mock,
        sample_compiler_info: CompilerInfo
    ):
        """Test successful refresh of detection"""
        # Setup cache
        compiler_manager._detected_compilers = {
            "msvc": [sample_compiler_info]
        }
        
        # Setup mock
        mock_factory.get_available_compilers.return_value = {
            "msvc": [sample_compiler_info],
            "mingw_gcc": []
        }
        
        # Execute
        result = compiler_manager.refresh_detection()
        
        # Verify
        assert "msvc" in result
        assert "mingw_gcc" in result
        mock_factory.clear_cache.assert_called_once()
        mock_factory.get_available_compilers.assert_called_once()

    def test_refresh_detection_clears_cache(
        self,
        compiler_manager: CompilerManager,
        mock_factory: Mock,
        sample_compiler_info: CompilerInfo
    ):
        """Test that refresh clears local cache"""
        # Setup cache
        compiler_manager._detected_compilers = {
            "msvc": [sample_compiler_info]
        }
        
        # Setup mock
        mock_factory.get_available_compilers.return_value = {}
        
        # Execute
        compiler_manager.refresh_detection()
        
        # Verify cache was cleared
        assert len(compiler_manager._detected_compilers) == 0
