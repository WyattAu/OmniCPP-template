"""
Compiler factory for creating compiler instances
"""

import platform
from typing import Any
from .base import CompilerBase, CompilerInfo
from .msvc import MSVCCompiler
from .msvc_clang import MSVCClangCompiler
from .mingw_gcc import MinWGGCCCompiler
from .mingw_clang import MinGWClangCompiler
from .gcc import GCCCompiler
from .clang import ClangCompiler


class CompilerFactory:
    """Factory for creating compiler instances"""
    
    # Cache for compiler instances
    _cache: dict[str, CompilerBase] = {}
    
    @staticmethod
    def create(compiler_type: str, version: str | None = None) -> CompilerBase:
        """Create compiler instance
        
        Args:
            compiler_type: Compiler type (msvc, msvc-clang, mingw-gcc, mingw-clang, gcc, clang)
            version: Compiler version (auto-detect if None)
            
        Returns:
            Compiler instance
            
        Raises:
            ValueError: If compiler type is invalid
        """
        # Check cache first
        cache_key = f"{compiler_type}_{version or 'auto'}"
        if cache_key in CompilerFactory._cache:
            return CompilerFactory._cache[cache_key]
        
        # Create compiler instance based on type
        compiler_type_lower = compiler_type.lower()
        
        if compiler_type_lower == "msvc":
            compiler = MSVCCompiler(version)
        elif compiler_type_lower == "msvc-clang":
            compiler = MSVCClangCompiler(version)
        elif compiler_type_lower == "mingw-gcc":
            compiler = MinWGGCCCompiler(version)
        elif compiler_type_lower == "mingw-clang":
            compiler = MinGWClangCompiler(version)
        elif compiler_type_lower == "gcc":
            compiler = GCCCompiler(version)
        elif compiler_type_lower == "clang":
            compiler = ClangCompiler(version)
        else:
            raise ValueError(f"Unknown compiler type: {compiler_type}")
        
        # Cache the instance
        CompilerFactory._cache[cache_key] = compiler
        return compiler
    
    @staticmethod
    def detect_available() -> list[CompilerInfo]:
        """Detect all available compilers
        
        Returns:
            List of available compilers
        """
        available: list[CompilerInfo] = []
        current_platform = platform.system().lower()
        
        # Detect Windows compilers
        if current_platform == "windows":
            # Try MSVC
            msvc = MSVCCompiler()
            msvc_info = msvc.get_info()
            if msvc_info:
                available.append(msvc_info)
            
            # Try MSVC-Clang
            msvc_clang = MSVCClangCompiler()
            msvc_clang_info = msvc_clang.get_info()
            if msvc_clang_info:
                available.append(msvc_clang_info)
            
            # Try MinGW-GCC
            mingw_gcc = MinWGGCCCompiler()
            mingw_gcc_info = mingw_gcc.get_info()
            if mingw_gcc_info:
                available.append(mingw_gcc_info)
            
            # Try MinGW-Clang
            mingw_clang = MinGWClangCompiler()
            mingw_clang_info = mingw_clang.get_info()
            if mingw_clang_info:
                available.append(mingw_clang_info)
        
        # Detect Linux compilers
        elif current_platform == "linux":
            # Try GCC
            gcc = GCCCompiler()
            gcc_info = gcc.get_info()
            if gcc_info:
                available.append(gcc_info)
            
            # Try Clang
            clang = ClangCompiler()
            clang_info = clang.get_info()
            if clang_info:
                available.append(clang_info)
        
        return available
    
    @staticmethod
    def get_default_compiler() -> CompilerBase | None:
        """Get default compiler for current platform
        
        Returns:
            Default compiler instance or None if not found
        """
        current_platform = platform.system().lower()
        
        if current_platform == "windows":
            # Prefer MSVC on Windows
            msvc = MSVCCompiler()
            if msvc.detect():
                return msvc
            
            # Fall back to MinGW-GCC
            mingw_gcc = MinWGGCCCompiler()
            if mingw_gcc.detect():
                return mingw_gcc
        
        elif current_platform == "linux":
            # Prefer GCC on Linux
            gcc = GCCCompiler()
            if gcc.detect():
                return gcc
            
            # Fall back to Clang
            clang = ClangCompiler()
            if clang.detect():
                return clang
        
        return None
    
    @staticmethod
    def clear_cache() -> None:
        """Clear compiler instance cache"""
        CompilerFactory._cache.clear()
