"""
Test script for compiler detection implementations
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compilers.base import CompilerBase, CompilerInfo
from compilers.msvc import MSVCCompiler
from compilers.msvc_clang import MSVCClangCompiler
from compilers.mingw_gcc import MinWGGCCCompiler
from compilers.mingw_clang import MinGWClangCompiler
from compilers.gcc import GCCCompiler
from compilers.clang import ClangCompiler
from compilers.factory import CompilerFactory
from compilers.manager import CompilerManager


def test_base_class():
    """Test base compiler class"""
    print("Testing base compiler class...")
    
    # Test CompilerInfo dataclass
    info = CompilerInfo(
        name="Test",
        version="1.0.0",
        path="/path/to/compiler",
        target="test-platform",
        flags=["-std=c++23"]
    )
    
    assert info.name == "Test"
    assert info.version == "1.0.0"
    assert info.path == "/path/to/compiler"
    assert info.target == "test-platform"
    assert info.flags == ["-std=c++23"]
    
    print("  [OK] CompilerInfo dataclass works correctly")


def test_compiler_factory():
    """Test compiler factory"""
    print("Testing compiler factory...")
    
    # Test creating compilers
    try:
        msvc = CompilerFactory.create("msvc")
        assert msvc.get_name() == "MSVC"
        print("  [OK] MSVC compiler created")
    except Exception as e:
        print(f"  [FAIL] MSVC compiler creation failed: {e}")
    
    try:
        msvc_clang = CompilerFactory.create("msvc-clang")
        assert msvc_clang.get_name() == "MSVC-Clang"
        print("  [OK] MSVC-Clang compiler created")
    except Exception as e:
        print(f"  [FAIL] MSVC-Clang compiler creation failed: {e}")
    
    try:
        mingw_gcc = CompilerFactory.create("mingw-gcc")
        assert mingw_gcc.get_name() == "MinGW-GCC"
        print("  [OK] MinGW-GCC compiler created")
    except Exception as e:
        print(f"  [FAIL] MinGW-GCC compiler creation failed: {e}")
    
    try:
        mingw_clang = CompilerFactory.create("mingw-clang")
        assert mingw_clang.get_name() == "MinGW-Clang"
        print("  [OK] MinGW-Clang compiler created")
    except Exception as e:
        print(f"  [FAIL] MinGW-Clang compiler creation failed: {e}")
    
    try:
        gcc = CompilerFactory.create("gcc")
        assert gcc.get_name() == "GCC"
        print("  [OK] GCC compiler created")
    except Exception as e:
        print(f"  [FAIL] GCC compiler creation failed: {e}")
    
    try:
        clang = CompilerFactory.create("clang")
        assert clang.get_name() == "Clang"
        print("  [OK] Clang compiler created")
    except Exception as e:
        print(f"  [FAIL] Clang compiler creation failed: {e}")
    
    # Test invalid compiler type
    try:
        CompilerFactory.create("invalid")
        print("  [FAIL] Invalid compiler type should raise ValueError")
    except ValueError:
        print("  [OK] Invalid compiler type raises ValueError")


def test_compiler_manager():
    """Test compiler manager"""
    print("Testing compiler manager...")
    
    manager = CompilerManager()
    
    # Test platform detection
    platform = manager.get_platform()
    print(f"  Platform: {platform}")
    assert platform in ["windows", "linux", "darwin"]
    
    # Test architecture detection
    arch = manager.get_architecture()
    print(f"  Architecture: {arch}")
    assert arch in ["x64", "arm64", "x86"]
    
    # Test compiler detection
    available = manager.detect_compilers()
    print(f"  Available compilers: {len(available)}")
    for info in available:
        print(f"    - {info.name} {info.version}")
    
    # Test recommended compiler
    recommended = manager.get_recommended_compiler()
    print(f"  Recommended compiler: {recommended}")
    
    # Test summary
    summary = manager.get_compiler_summary()
    print(f"  Compiler summary generated")
    assert "platform" in summary
    assert "available_compilers" in summary
    assert "recommended_compiler" in summary


def test_compiler_flags():
    """Test compiler flags"""
    print("Testing compiler flags...")
    
    compilers_to_test = [
        ("msvc", MSVCCompiler),
        ("msvc-clang", MSVCClangCompiler),
        ("mingw-gcc", MinWGGCCCompiler),
        ("mingw-clang", MinGWClangCompiler),
        ("gcc", GCCCompiler),
        ("clang", ClangCompiler)
    ]
    
    build_types = ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"]
    
    for name, compiler_class in compilers_to_test:
        try:
            compiler = compiler_class()
            for build_type in build_types:
                flags = compiler.get_flags(build_type)
                assert isinstance(flags, list)
                assert len(flags) > 0
            print(f"  [OK] {name} flags generated for all build types")
        except Exception as e:
            print(f"  ✗ {name} flags failed: {e}")


def main():
    """Main test function"""
    print("=" * 60)
    print("Compiler Detection Implementation Tests")
    print("=" * 60)
    print()
    
    try:
        test_base_class()
        print()
        test_compiler_factory()
        print()
        test_compiler_manager()
        print()
        test_compiler_flags()
        print()
        print("=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
        return 0
    except Exception as e:
        print()
        print("=" * 60)
        print(f"Test failed with error: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
