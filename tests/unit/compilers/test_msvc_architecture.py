"""
Unit tests for MSVC Architecture module

Tests for MSVCArchitecture enum, validator, and mapper classes.
"""

import pytest
import logging
from scripts.python.compilers.msvc_architecture import (
    MSVCArchitecture,
    MSVCArchitectureValidator,
    MSVCArchitectureMapper,
    detect_system_architecture,
    get_recommended_architecture
)


class TestMSVCArchitectureEnum:
    """Test MSVCArchitecture enum properties and methods"""
    
    def test_all_architectures_exist(self):
        """Test that all required architectures are defined"""
        required_archs = [
            MSVCArchitecture.X64,
            MSVCArchitecture.X86,
            MSVCArchitecture.X86_AMD64,
            MSVCArchitecture.AMD64_X86,
            MSVCArchitecture.AMD64_ARM,
            MSVCArchitecture.AMD64_ARM64
        ]
        
        for arch in required_archs:
            assert arch in MSVCArchitecture.get_all_architectures()
    
    def test_x64_properties(self):
        """Test X64 architecture properties"""
        arch = MSVCArchitecture.X64
        
        assert arch.value == "amd64"
        assert arch.host_architecture == "x64"
        assert arch.target_architecture == "x64"
        assert arch.is_native is True
        assert arch.is_cross_compilation is False
        assert arch.is_arm_target is False
        assert arch.is_x86_target is True
    
    def test_x86_properties(self):
        """Test X86 architecture properties"""
        arch = MSVCArchitecture.X86
        
        assert arch.value == "x86"
        assert arch.host_architecture == "x86"
        assert arch.target_architecture == "x86"
        assert arch.is_native is True
        assert arch.is_cross_compilation is False
        assert arch.is_arm_target is False
        assert arch.is_x86_target is True
    
    def test_x86_amd64_properties(self):
        """Test X86_AMD64 cross-compilation architecture properties"""
        arch = MSVCArchitecture.X86_AMD64
        
        assert arch.value == "x86_amd64"
        assert arch.host_architecture == "x86"
        assert arch.target_architecture == "x64"
        assert arch.is_native is False
        assert arch.is_cross_compilation is True
        assert arch.is_arm_target is False
        assert arch.is_x86_target is True
    
    def test_amd64_x86_properties(self):
        """Test AMD64_X86 cross-compilation architecture properties"""
        arch = MSVCArchitecture.AMD64_X86
        
        assert arch.value == "amd64_x86"
        assert arch.host_architecture == "x64"
        assert arch.target_architecture == "x86"
        assert arch.is_native is False
        assert arch.is_cross_compilation is True
        assert arch.is_arm_target is False
        assert arch.is_x86_target is True
    
    def test_amd64_arm_properties(self):
        """Test AMD64_ARM cross-compilation architecture properties"""
        arch = MSVCArchitecture.AMD64_ARM
        
        assert arch.value == "amd64_arm"
        assert arch.host_architecture == "x64"
        assert arch.target_architecture == "arm"
        assert arch.is_native is False
        assert arch.is_cross_compilation is True
        assert arch.is_arm_target is True
        assert arch.is_x86_target is False
    
    def test_amd64_arm64_properties(self):
        """Test AMD64_ARM64 cross-compilation architecture properties"""
        arch = MSVCArchitecture.AMD64_ARM64
        
        assert arch.value == "amd64_arm64"
        assert arch.host_architecture == "x64"
        assert arch.target_architecture == "arm64"
        assert arch.is_native is False
        assert arch.is_cross_compilation is True
        assert arch.is_arm_target is True
        assert arch.is_x86_target is False
    
    def test_get_native_architectures(self):
        """Test getting native architectures"""
        native_archs = MSVCArchitecture.get_native_architectures()
        
        assert len(native_archs) == 2
        assert MSVCArchitecture.X64 in native_archs
        assert MSVCArchitecture.X86 in native_archs
        assert MSVCArchitecture.X86_AMD64 not in native_archs
        assert MSVCArchitecture.AMD64_X86 not in native_archs
    
    def test_get_cross_compilation_architectures(self):
        """Test getting cross-compilation architectures"""
        cross_archs = MSVCArchitecture.get_cross_compilation_architectures()
        
        assert len(cross_archs) == 4
        assert MSVCArchitecture.X86_AMD64 in cross_archs
        assert MSVCArchitecture.AMD64_X86 in cross_archs
        assert MSVCArchitecture.AMD64_ARM in cross_archs
        assert MSVCArchitecture.AMD64_ARM64 in cross_archs
        assert MSVCArchitecture.X64 not in cross_archs
        assert MSVCArchitecture.X86 not in cross_archs
    
    def test_get_arm_architectures(self):
        """Test getting ARM target architectures"""
        arm_archs = MSVCArchitecture.get_arm_architectures()
        
        assert len(arm_archs) == 2
        assert MSVCArchitecture.AMD64_ARM in arm_archs
        assert MSVCArchitecture.AMD64_ARM64 in arm_archs
        assert MSVCArchitecture.X64 not in arm_archs
        assert MSVCArchitecture.X86 not in arm_archs
    
    def test_get_x86_architectures(self):
        """Test getting x86 target architectures"""
        x86_archs = MSVCArchitecture.get_x86_architectures()
        
        assert len(x86_archs) == 4
        assert MSVCArchitecture.X64 in x86_archs
        assert MSVCArchitecture.X86 in x86_archs
        assert MSVCArchitecture.X86_AMD64 in x86_archs
        assert MSVCArchitecture.AMD64_X86 in x86_archs
        assert MSVCArchitecture.AMD64_ARM not in x86_archs
        assert MSVCArchitecture.AMD64_ARM64 not in x86_archs


class TestMSVCArchitectureFromString:
    """Test MSVCArchitecture.from_string() method"""
    
    def test_from_string_x64(self):
        """Test parsing x64 from string"""
        arch = MSVCArchitecture.from_string("x64")
        assert arch == MSVCArchitecture.X64
    
    def test_from_string_amd64(self):
        """Test parsing amd64 from string (alias for x64)"""
        arch = MSVCArchitecture.from_string("amd64")
        assert arch == MSVCArchitecture.X64
    
    def test_from_string_x86(self):
        """Test parsing x86 from string"""
        arch = MSVCArchitecture.from_string("x86")
        assert arch == MSVCArchitecture.X86
    
    def test_from_string_32(self):
        """Test parsing 32 from string (alias for x86)"""
        arch = MSVCArchitecture.from_string("32")
        assert arch == MSVCArchitecture.X86
    
    def test_from_string_x86_amd64(self):
        """Test parsing x86_amd64 from string"""
        arch = MSVCArchitecture.from_string("x86_amd64")
        assert arch == MSVCArchitecture.X86_AMD64
    
    def test_from_string_x86_x64(self):
        """Test parsing x86-x64 from string (alias for x86_amd64)"""
        arch = MSVCArchitecture.from_string("x86-x64")
        assert arch == MSVCArchitecture.X86_AMD64
    
    def test_from_string_amd64_x86(self):
        """Test parsing amd64_x86 from string"""
        arch = MSVCArchitecture.from_string("amd64_x86")
        assert arch == MSVCArchitecture.AMD64_X86
    
    def test_from_string_amd64_arm(self):
        """Test parsing amd64_arm from string"""
        arch = MSVCArchitecture.from_string("amd64_arm")
        assert arch == MSVCArchitecture.AMD64_ARM
    
    def test_from_string_amd64_arm64(self):
        """Test parsing amd64_arm64 from string"""
        arch = MSVCArchitecture.from_string("amd64_arm64")
        assert arch == MSVCArchitecture.AMD64_ARM64
    
    def test_from_string_case_insensitive(self):
        """Test that parsing is case-insensitive"""
        arch1 = MSVCArchitecture.from_string("X64")
        arch2 = MSVCArchitecture.from_string("x64")
        arch3 = MSVCArchitecture.from_string("X64")
        
        assert arch1 == arch2 == arch3 == MSVCArchitecture.X64
    
    def test_from_string_whitespace(self):
        """Test that parsing handles whitespace"""
        arch = MSVCArchitecture.from_string("  x64  ")
        assert arch == MSVCArchitecture.X64
    
    def test_from_string_invalid(self):
        """Test that invalid string raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            MSVCArchitecture.from_string("invalid")
        
        assert "Invalid MSVC architecture" in str(exc_info.value)
        assert "valid architectures are" in str(exc_info.value).lower()


class TestMSVCArchitectureFromHostTarget:
    """Test MSVCArchitecture.from_host_target() method"""
    
    def test_from_host_target_x64_x64(self):
        """Test parsing x64 host, x64 target"""
        arch = MSVCArchitecture.from_host_target("x64", "x64")
        assert arch == MSVCArchitecture.X64
    
    def test_from_host_target_amd64_amd64(self):
        """Test parsing amd64 host, amd64 target (alias for x64)"""
        arch = MSVCArchitecture.from_host_target("amd64", "amd64")
        assert arch == MSVCArchitecture.X64
    
    def test_from_host_target_x86_x86(self):
        """Test parsing x86 host, x86 target"""
        arch = MSVCArchitecture.from_host_target("x86", "x86")
        assert arch == MSVCArchitecture.X86
    
    def test_from_host_target_32_32(self):
        """Test parsing 32 host, 32 target (alias for x86)"""
        arch = MSVCArchitecture.from_host_target("32", "32")
        assert arch == MSVCArchitecture.X86
    
    def test_from_host_target_x86_x64(self):
        """Test parsing x86 host, x64 target"""
        arch = MSVCArchitecture.from_host_target("x86", "x64")
        assert arch == MSVCArchitecture.X86_AMD64
    
    def test_from_host_target_x64_x86(self):
        """Test parsing x64 host, x86 target"""
        arch = MSVCArchitecture.from_host_target("x64", "x86")
        assert arch == MSVCArchitecture.AMD64_X86
    
    def test_from_host_target_x64_arm(self):
        """Test parsing x64 host, arm target"""
        arch = MSVCArchitecture.from_host_target("x64", "arm")
        assert arch == MSVCArchitecture.AMD64_ARM
    
    def test_from_host_target_x64_arm64(self):
        """Test parsing x64 host, arm64 target"""
        arch = MSVCArchitecture.from_host_target("x64", "arm64")
        assert arch == MSVCArchitecture.AMD64_ARM64
    
    def test_from_host_target_x64_aarch64(self):
        """Test parsing x64 host, aarch64 target (alias for arm64)"""
        arch = MSVCArchitecture.from_host_target("x64", "aarch64")
        assert arch == MSVCArchitecture.AMD64_ARM64
    
    def test_from_host_target_case_insensitive(self):
        """Test that parsing is case-insensitive"""
        arch1 = MSVCArchitecture.from_host_target("X64", "X64")
        arch2 = MSVCArchitecture.from_host_target("x64", "x64")
        
        assert arch1 == arch2 == MSVCArchitecture.X64
    
    def test_from_host_target_whitespace(self):
        """Test that parsing handles whitespace"""
        arch = MSVCArchitecture.from_host_target("  x64  ", "  x64  ")
        assert arch == MSVCArchitecture.X64
    
    def test_from_host_target_invalid_host(self):
        """Test that invalid host raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            MSVCArchitecture.from_host_target("invalid", "x64")
        
        assert "Invalid host architecture" in str(exc_info.value)
    
    def test_from_host_target_invalid_target(self):
        """Test that invalid target raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            MSVCArchitecture.from_host_target("x64", "invalid")
        
        assert "Invalid target architecture" in str(exc_info.value)
    
    def test_from_host_target_invalid_combination(self):
        """Test that invalid host/target combination raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            MSVCArchitecture.from_host_target("x86", "arm")
        
        assert "Invalid host/target combination" in str(exc_info.value)


class TestMSVCArchitectureValidator:
    """Test MSVCArchitectureValidator class"""
    
    def test_validate_valid_architecture(self):
        """Test validating a valid architecture"""
        validator = MSVCArchitectureValidator()
        is_valid, errors = validator.validate_architecture(MSVCArchitecture.X64)
        
        assert is_valid is True
        assert len(errors) == 0
    
    def test_validate_invalid_type(self):
        """Test validating an invalid type"""
        validator = MSVCArchitectureValidator()
        is_valid, errors = validator.validate_architecture("x64")  # type: ignore[arg-type]
        
        assert is_valid is False
        assert len(errors) > 0
        assert "Invalid architecture type" in errors[0]
    
    def test_validate_architecture_string_valid(self):
        """Test validating a valid architecture string"""
        validator = MSVCArchitectureValidator()
        is_valid, errors, arch = validator.validate_architecture_string("x64")
        
        assert is_valid is True
        assert len(errors) == 0
        assert arch == MSVCArchitecture.X64
    
    def test_validate_architecture_string_invalid(self):
        """Test validating an invalid architecture string"""
        validator = MSVCArchitectureValidator()
        is_valid, errors, arch = validator.validate_architecture_string("invalid")
        
        assert is_valid is False
        assert len(errors) > 0
        assert arch is None
    
    def test_validate_host_target_valid(self):
        """Test validating a valid host/target combination"""
        validator = MSVCArchitectureValidator()
        is_valid, errors, arch = validator.validate_host_target("x64", "x64")
        
        assert is_valid is True
        assert len(errors) == 0
        assert arch == MSVCArchitecture.X64
    
    def test_validate_host_target_invalid(self):
        """Test validating an invalid host/target combination"""
        validator = MSVCArchitectureValidator()
        is_valid, errors, arch = validator.validate_host_target("x86", "arm")
        
        assert is_valid is False
        assert len(errors) > 0
        assert arch is None
    
    def test_get_supported_architectures_for_x64_host(self):
        """Test getting supported architectures for x64 host"""
        validator = MSVCArchitectureValidator()
        archs = validator.get_supported_architectures_for_host("x64")
        
        assert len(archs) == 4
        assert MSVCArchitecture.X64 in archs
        assert MSVCArchitecture.AMD64_X86 in archs
        assert MSVCArchitecture.AMD64_ARM in archs
        assert MSVCArchitecture.AMD64_ARM64 in archs
        assert MSVCArchitecture.X86 not in archs
        assert MSVCArchitecture.X86_AMD64 not in archs
    
    def test_get_supported_architectures_for_x86_host(self):
        """Test getting supported architectures for x86 host"""
        validator = MSVCArchitectureValidator()
        archs = validator.get_supported_architectures_for_host("x86")
        
        assert len(archs) == 2
        assert MSVCArchitecture.X86 in archs
        assert MSVCArchitecture.X86_AMD64 in archs
        assert MSVCArchitecture.X64 not in archs
        assert MSVCArchitecture.AMD64_X86 not in archs
    
    def test_get_supported_architectures_for_amd64_host(self):
        """Test getting supported architectures for amd64 host (alias for x64)"""
        validator = MSVCArchitectureValidator()
        archs = validator.get_supported_architectures_for_host("amd64")
        
        assert len(archs) == 4
        assert MSVCArchitecture.X64 in archs
    
    def test_get_supported_architectures_for_32_host(self):
        """Test getting supported architectures for 32 host (alias for x86)"""
        validator = MSVCArchitectureValidator()
        archs = validator.get_supported_architectures_for_host("32")
        
        assert len(archs) == 2
        assert MSVCArchitecture.X86 in archs
    
    def test_get_supported_architectures_for_unknown_host(self):
        """Test getting supported architectures for unknown host"""
        validator = MSVCArchitectureValidator()
        archs = validator.get_supported_architectures_for_host("unknown")
        
        assert len(archs) == 0


class TestMSVCArchitectureMapper:
    """Test MSVCArchitectureMapper class"""
    
    def test_get_vcvarsall_argument_x64(self):
        """Test getting vcvarsall argument for x64"""
        mapper = MSVCArchitectureMapper()
        arg = mapper.get_vcvarsall_argument(MSVCArchitecture.X64)
        
        assert arg == "amd64"
    
    def test_get_vcvarsall_argument_x86(self):
        """Test getting vcvarsall argument for x86"""
        mapper = MSVCArchitectureMapper()
        arg = mapper.get_vcvarsall_argument(MSVCArchitecture.X86)
        
        assert arg == "x86"
    
    def test_get_vcvarsall_argument_x86_amd64(self):
        """Test getting vcvarsall argument for x86_amd64"""
        mapper = MSVCArchitectureMapper()
        arg = mapper.get_vcvarsall_argument(MSVCArchitecture.X86_AMD64)
        
        assert arg == "x86_amd64"
    
    def test_get_vcvarsall_argument_amd64_x86(self):
        """Test getting vcvarsall argument for amd64_x86"""
        mapper = MSVCArchitectureMapper()
        arg = mapper.get_vcvarsall_argument(MSVCArchitecture.AMD64_X86)
        
        assert arg == "amd64_x86"
    
    def test_get_vcvarsall_argument_amd64_arm(self):
        """Test getting vcvarsall argument for amd64_arm"""
        mapper = MSVCArchitectureMapper()
        arg = mapper.get_vcvarsall_argument(MSVCArchitecture.AMD64_ARM)
        
        assert arg == "amd64_arm"
    
    def test_get_vcvarsall_argument_amd64_arm64(self):
        """Test getting vcvarsall argument for amd64_arm64"""
        mapper = MSVCArchitectureMapper()
        arg = mapper.get_vcvarsall_argument(MSVCArchitecture.AMD64_ARM64)
        
        assert arg == "amd64_arm64"
    
    def test_get_cl_path_x64(self):
        """Test getting cl.exe path for x64"""
        mapper = MSVCArchitectureMapper()
        path = mapper.get_cl_path(MSVCArchitecture.X64)
        
        assert path == "Hostx64/x64"
    
    def test_get_cl_path_x86(self):
        """Test getting cl.exe path for x86"""
        mapper = MSVCArchitectureMapper()
        path = mapper.get_cl_path(MSVCArchitecture.X86)
        
        assert path == "Hostx86/x86"
    
    def test_get_cl_path_x86_amd64(self):
        """Test getting cl.exe path for x86_amd64"""
        mapper = MSVCArchitectureMapper()
        path = mapper.get_cl_path(MSVCArchitecture.X86_AMD64)
        
        assert path == "Hostx86/x64"
    
    def test_get_cl_path_amd64_x86(self):
        """Test getting cl.exe path for amd64_x86"""
        mapper = MSVCArchitectureMapper()
        path = mapper.get_cl_path(MSVCArchitecture.AMD64_X86)
        
        assert path == "Hostx64/x86"
    
    def test_get_cl_path_amd64_arm(self):
        """Test getting cl.exe path for amd64_arm"""
        mapper = MSVCArchitectureMapper()
        path = mapper.get_cl_path(MSVCArchitecture.AMD64_ARM)
        
        assert path == "Hostx64/arm"
    
    def test_get_cl_path_amd64_arm64(self):
        """Test getting cl.exe path for amd64_arm64"""
        mapper = MSVCArchitectureMapper()
        path = mapper.get_cl_path(MSVCArchitecture.AMD64_ARM64)
        
        assert path == "Hostx64/arm64"
    
    def test_get_batch_file_x64(self):
        """Test getting batch file for x64"""
        mapper = MSVCArchitectureMapper()
        batch_file = mapper.get_batch_file(MSVCArchitecture.X64)
        
        assert batch_file == "vcvars64.bat"
    
    def test_get_batch_file_x86(self):
        """Test getting batch file for x86"""
        mapper = MSVCArchitectureMapper()
        batch_file = mapper.get_batch_file(MSVCArchitecture.X86)
        
        assert batch_file == "vcvars32.bat"
    
    def test_get_batch_file_x86_amd64(self):
        """Test getting batch file for x86_amd64"""
        mapper = MSVCArchitectureMapper()
        batch_file = mapper.get_batch_file(MSVCArchitecture.X86_AMD64)
        
        assert batch_file == "vcvarsx86_amd64.bat"
    
    def test_get_batch_file_amd64_x86(self):
        """Test getting batch file for amd64_x86"""
        mapper = MSVCArchitectureMapper()
        batch_file = mapper.get_batch_file(MSVCArchitecture.AMD64_X86)
        
        assert batch_file == "vcvarsamd64_x86.bat"
    
    def test_get_batch_file_amd64_arm(self):
        """Test getting batch file for amd64_arm"""
        mapper = MSVCArchitectureMapper()
        batch_file = mapper.get_batch_file(MSVCArchitecture.AMD64_ARM)
        
        assert batch_file == "vcvarsamd64_arm.bat"
    
    def test_get_batch_file_amd64_arm64(self):
        """Test getting batch file for amd64_arm64"""
        mapper = MSVCArchitectureMapper()
        batch_file = mapper.get_batch_file(MSVCArchitecture.AMD64_ARM64)
        
        assert batch_file == "vcvarsamd64_arm64.bat"
    
    def test_get_full_cl_path(self):
        """Test getting full cl.exe path"""
        mapper = MSVCArchitectureMapper()
        vs_path = r"C:\Program Files\Microsoft Visual Studio\2022\Community"
        
        full_path = mapper.get_full_cl_path(MSVCArchitecture.X64, vs_path)
        
        expected = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\Hostx64\x64\cl.exe"
        assert full_path == expected
    
    def test_get_vcvarsall_path(self):
        """Test getting vcvarsall.bat path"""
        mapper = MSVCArchitectureMapper()
        vs_path = r"C:\Program Files\Microsoft Visual Studio\2022\Community"
        
        vcvarsall_path = mapper.get_vcvarsall_path(vs_path)
        
        expected = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"
        assert vcvarsall_path == expected
    
    def test_get_all_mappings(self):
        """Test getting all mappings"""
        mapper = MSVCArchitectureMapper()
        mappings = mapper.get_all_mappings()
        
        assert len(mappings) == 6
        
        # Check that all architectures are present
        for arch in MSVCArchitecture:
            assert arch in mappings
            
            # Check that all required keys are present
            mapping = mappings[arch]
            assert "vcvarsall_arg" in mapping
            assert "cl_path" in mapping
            assert "batch_file" in mapping
            assert "host_arch" in mapping
            assert "target_arch" in mapping
            assert "is_native" in mapping
            assert "is_cross_compilation" in mapping
    
    def test_get_vcvarsall_argument_invalid(self):
        """Test that invalid architecture raises ValueError"""
        mapper = MSVCArchitectureMapper()
        
        with pytest.raises(ValueError) as exc_info:
            mapper.get_vcvarsall_argument("invalid")  # type: ignore[arg-type]
        
        assert "Unsupported architecture" in str(exc_info.value)
    
    def test_get_cl_path_invalid(self):
        """Test that invalid architecture raises ValueError for cl path"""
        mapper = MSVCArchitectureMapper()
        
        with pytest.raises(ValueError) as exc_info:
            mapper.get_cl_path("invalid")  # type: ignore[arg-type]
        
        assert "Unsupported architecture" in str(exc_info.value)
    
    def test_get_batch_file_invalid(self):
        """Test that invalid architecture raises ValueError for batch file"""
        mapper = MSVCArchitectureMapper()
        
        with pytest.raises(ValueError) as exc_info:
            mapper.get_batch_file("invalid")  # type: ignore[arg-type]
        
        assert "Unsupported architecture" in str(exc_info.value)


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_detect_system_architecture(self):
        """Test system architecture detection"""
        arch = detect_system_architecture()
        
        # Should return either x64 or x86
        assert arch in ["x64", "x86"]
    
    def test_get_recommended_architecture(self):
        """Test getting recommended architecture"""
        arch = get_recommended_architecture()
        
        # Should return a valid MSVCArchitecture
        assert isinstance(arch, MSVCArchitecture)
        
        # Should be either X64 or X86
        assert arch in [MSVCArchitecture.X64, MSVCArchitecture.X86]


class TestLoggingIntegration:
    """Test logging integration"""
    
    def test_validator_with_logger(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test validator with custom logger"""
        logger = logging.getLogger("test_logger")
        logger.setLevel(logging.DEBUG)
        
        validator = MSVCArchitectureValidator(logger)
        
        with caplog.at_level(logging.DEBUG):
            is_valid, errors, arch = validator.validate_architecture_string("x64")
        
        assert is_valid is True
        assert arch == MSVCArchitecture.X64
        assert any("Successfully parsed architecture" in record.message for record in caplog.records)  # type: ignore[attr-defined]
    
    def test_mapper_with_logger(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test mapper with custom logger"""
        logger = logging.getLogger("test_mapper_logger")
        logger.setLevel(logging.DEBUG)
        
        mapper = MSVCArchitectureMapper(logger)
        
        with caplog.at_level(logging.DEBUG):
            arg = mapper.get_vcvarsall_argument(MSVCArchitecture.X64)
        
        assert arg == "amd64"
        assert any("vcvarsall argument" in record.message for record in caplog.records)  # type: ignore[attr-defined]
