"""
Compiler detection and management package
"""

from .base import CompilerBase, CompilerInfo
from .msvc import MSVCCompiler
from .msvc_clang import MSVCClangCompiler
from .mingw_gcc import MinWGGCCCompiler
from .mingw_clang import MinGWClangCompiler
from .gcc import GCCCompiler
from .clang import ClangCompiler
from .factory import CompilerFactory
from .manager import CompilerManager
from .msvc_terminal_detector import (
    MSVCTerminalDetector,
    TerminalType,
    TerminalInfo,
    ITerminalDetector
)
from .chocolatey_detector import (
    ChocolateyDetector,
    PackageManagerType,
    PackageInfo,
    ValidationResult
)
from .linux_cross_compiler import (
    LinuxCrossCompiler,
    ToolchainInfo as LinuxToolchainInfo,
    CrossCompilerInfo as LinuxCrossCompilerInfo,
    ICrossCompiler as ICrossCompilerInterface
)
from .wasm_cross_compiler import (
    WASMCrossCompiler,
    EmscriptenInfo,
    CrossCompilerInfo as WASMCrossCompilerInfo
)
from .android_cross_compiler import (
    AndroidCrossCompiler,
    NDKInfo,
    ToolchainInfo as AndroidToolchainInfo,
    CrossCompilerInfo as AndroidCrossCompilerInfo
)
from .cmake_generator_selector import (
    CMakeGeneratorSelector,
    CMakeGeneratorType,
    CompilerType as CMakeCompilerCompilerType,
    TargetPlatform,
    GeneratorInfo,
    GeneratorSelectionResult,
    CMakeGeneratorError
)

__all__ = [
    "CompilerBase",
    "CompilerInfo",
    "MSVCCompiler",
    "MSVCClangCompiler",
    "MinWGGCCCompiler",
    "MinGWClangCompiler",
    "GCCCompiler",
    "ClangCompiler",
    "CompilerFactory",
    "CompilerManager",
    "MSVCTerminalDetector",
    "TerminalType",
    "TerminalInfo",
    "ITerminalDetector",
    "ChocolateyDetector",
    "PackageManagerType",
    "PackageInfo",
    "ValidationResult",
    "LinuxCrossCompiler",
    "LinuxToolchainInfo",
    "LinuxCrossCompilerInfo",
    "ICrossCompilerInterface",
    "WASMCrossCompiler",
    "EmscriptenInfo",
    "WASMCrossCompilerInfo",
    "AndroidCrossCompiler",
    "NDKInfo",
    "AndroidToolchainInfo",
    "AndroidCrossCompilerInfo",
    "CMakeGeneratorSelector",
    "CMakeGeneratorType",
    "CMakeCompilerCompilerType",
    "TargetPlatform",
    "GeneratorInfo",
    "GeneratorSelectionResult",
    "CMakeGeneratorError"
]
