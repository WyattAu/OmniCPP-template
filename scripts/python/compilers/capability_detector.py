"""
Unified capability detection for all compiler types
"""

import logging
import re
import subprocess
import tempfile
import os
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple, Set
from enum import Enum


class CapabilityType(Enum):
    """Capability type enumeration"""
    CPP_STANDARD = "cpp_standard"
    LANGUAGE_FEATURE = "language_feature"
    LIBRARY_FEATURE = "library_feature"
    COMPILER_FLAG = "compiler_flag"


@dataclass
class CapabilityInfo:
    """Compiler capability information
    
    Attributes:
        cpp23: Support for C++23 standard
        cpp20: Support for C++20 standard
        cpp17: Support for C++17 standard
        cpp14: Support for C++14 standard
        cpp11: Support for C++11 standard
        modules: Support for C++20 modules
        coroutines: Support for C++20 coroutines
        concepts: Support for C++20 concepts
        ranges: Support for C++20 ranges
        std_format: Support for std::format (C++20)
        std_span: Support for std::span (C++20)
        std_string_view: Support for std::string_view (C++17)
        std_optional: Support for std::optional (C++17)
        std_variant: Support for std::variant (C++17)
        std_any: Support for std::any (C++17)
        std_filesystem: Support for std::filesystem (C++17)
        std_chrono: Support for std::chrono (C++11)
        std_thread: Support for std::thread (C++11)
        std_atomic: Support for std::atomic (C++11)
        std_mutex: Support for std::mutex (C++11)
        std_condition_variable: Support for std::condition_variable (C++11)
        std_future: Support for std::future (C++11)
        std_promise: Support for std::promise (C++11)
        std_shared_mutex: Support for std::shared_mutex (C++17)
        std_shared_future: Support for std::shared_future (C++11)
        constexpr_if: Support for constexpr if (C++17)
        fold_expressions: Support for fold expressions (C++17)
        structured_bindings: Support for structured bindings (C++17)
        inline_variables: Support for inline variables (C++17)
        std_byte: Support for std::byte (C++17)
        std_invoke: Support for std::invoke (C++17)
        std_apply: Support for std::apply (C++17)
        std_make_from_tuple: Support for std::make_from_tuple (C++17)
        std_clamp: Support for std::clamp (C++17)
        std_gcd: Support for std::gcd (C++17)
        std_lcm: Support for std::lcm (C++17)
        std_execution: Support for parallel algorithms (C++17)
        std_memory_resource: Support for std::pmr (C++17)
        std_string: Support for std::string (C++98)
        std_vector: Support for std::vector (C++98)
        std_map: Support for std::map (C++98)
        std_unordered_map: Support for std::unordered_map (C++11)
        std_set: Support for std::set (C++98)
        std_unordered_set: Support for std::unordered_set (C++11)
        std_array: Support for std::array (C++11)
        std_tuple: Support for std::tuple (C++11)
        std_function: Support for std::function (C++11)
        std_unique_ptr: Support for std::unique_ptr (C++11)
        std_shared_ptr: Support for std::shared_ptr (C++11)
        std_weak_ptr: Support for std::weak_ptr (C++11)
        msvc_compatibility: MSVC compatibility mode
        mingw_compatibility: MinGW compatibility mode
        gcc_compatibility: GCC compatibility mode
        clang_compatibility: Clang compatibility mode
    """
    cpp23: bool = False
    cpp20: bool = False
    cpp17: bool = False
    cpp14: bool = False
    cpp11: bool = False
    modules: bool = False
    coroutines: bool = False
    concepts: bool = False
    ranges: bool = False
    std_format: bool = False
    std_span: bool = False
    std_string_view: bool = False
    std_optional: bool = False
    std_variant: bool = False
    std_any: bool = False
    std_filesystem: bool = False
    std_chrono: bool = False
    std_thread: bool = False
    std_atomic: bool = False
    std_mutex: bool = False
    std_condition_variable: bool = False
    std_future: bool = False
    std_promise: bool = False
    std_shared_mutex: bool = False
    std_shared_future: bool = False
    constexpr_if: bool = False
    fold_expressions: bool = False
    structured_bindings: bool = False
    inline_variables: bool = False
    std_byte: bool = False
    std_invoke: bool = False
    std_apply: bool = False
    std_make_from_tuple: bool = False
    std_clamp: bool = False
    std_gcd: bool = False
    std_lcm: bool = False
    std_execution: bool = False
    std_memory_resource: bool = False
    std_string: bool = False
    std_vector: bool = False
    std_map: bool = False
    std_unordered_map: bool = False
    std_set: bool = False
    std_unordered_set: bool = False
    std_array: bool = False
    std_tuple: bool = False
    std_function: bool = False
    std_unique_ptr: bool = False
    std_shared_ptr: bool = False
    std_weak_ptr: bool = False
    msvc_compatibility: bool = False
    mingw_compatibility: bool = False
    gcc_compatibility: bool = False
    clang_compatibility: bool = False
    
    def to_dict(self) -> Dict[str, bool]:
        """Convert capabilities to dictionary
        
        Returns:
            Dictionary mapping capability names to boolean values
        """
        return {
            "cpp23": self.cpp23,
            "cpp20": self.cpp20,
            "cpp17": self.cpp17,
            "cpp14": self.cpp14,
            "cpp11": self.cpp11,
            "modules": self.modules,
            "coroutines": self.coroutines,
            "concepts": self.concepts,
            "ranges": self.ranges,
            "std_format": self.std_format,
            "std_span": self.std_span,
            "std_string_view": self.std_string_view,
            "std_optional": self.std_optional,
            "std_variant": self.std_variant,
            "std_any": self.std_any,
            "std_filesystem": self.std_filesystem,
            "std_chrono": self.std_chrono,
            "std_thread": self.std_thread,
            "std_atomic": self.std_atomic,
            "std_mutex": self.std_mutex,
            "std_condition_variable": self.std_condition_variable,
            "std_future": self.std_future,
            "std_promise": self.std_promise,
            "std_shared_mutex": self.std_shared_mutex,
            "std_shared_future": self.std_shared_future,
            "constexpr_if": self.constexpr_if,
            "fold_expressions": self.fold_expressions,
            "structured_bindings": self.structured_bindings,
            "inline_variables": self.inline_variables,
            "std_byte": self.std_byte,
            "std_invoke": self.std_invoke,
            "std_apply": self.std_apply,
            "std_make_from_tuple": self.std_make_from_tuple,
            "std_clamp": self.std_clamp,
            "std_gcd": self.std_gcd,
            "std_lcm": self.std_lcm,
            "std_execution": self.std_execution,
            "std_memory_resource": self.std_memory_resource,
            "std_string": self.std_string,
            "std_vector": self.std_vector,
            "std_map": self.std_map,
            "std_unordered_map": self.std_unordered_map,
            "std_set": self.std_set,
            "std_unordered_set": self.std_unordered_set,
            "std_array": self.std_array,
            "std_tuple": self.std_tuple,
            "std_function": self.std_function,
            "std_unique_ptr": self.std_unique_ptr,
            "std_shared_ptr": self.std_shared_ptr,
            "std_weak_ptr": self.std_weak_ptr,
            "msvc_compatibility": self.msvc_compatibility,
            "mingw_compatibility": self.mingw_compatibility,
            "gcc_compatibility": self.gcc_compatibility,
            "clang_compatibility": self.clang_compatibility
        }
    
    def supports_cpp_standard(self, standard: str) -> bool:
        """Check if compiler supports C++ standard
        
        Args:
            standard: C++ standard (e.g., "cpp23", "cpp20", "cpp17")
            
        Returns:
            True if compiler supports the standard, False otherwise
        """
        return getattr(self, standard.lower(), False)
    
    def get_highest_supported_standard(self) -> str:
        """Get highest supported C++ standard
        
        Returns:
            Highest supported C++ standard string
        """
        if self.cpp23:
            return "cpp23"
        elif self.cpp20:
            return "cpp20"
        elif self.cpp17:
            return "cpp17"
        elif self.cpp14:
            return "cpp14"
        elif self.cpp11:
            return "cpp11"
        else:
            return "unknown"


class CapabilityDetector:
    """Unified capability detector for all compiler types
    
    This class provides a unified interface for detecting, parsing, and validating
    compiler capabilities across all supported compiler types (MSVC, MSVC-Clang,
    MinGW-GCC, MinGW-Clang, GCC, Clang).
    """
    
    # Compiler type constants
    COMPILER_MSVC = "msvc"
    COMPILER_MSVC_CLANG = "msvc_clang"
    COMPILER_MINGW_GCC = "mingw_gcc"
    COMPILER_MINGW_CLANG = "mingw_clang"
    COMPILER_GCC = "gcc"
    COMPILER_CLANG = "clang"
    
    # Capability test code snippets for different features
    CAPABILITY_TESTS: Dict[str, str] = {
        "cpp23": """
            #if __cplusplus >= 202302L
            // C++23 is supported
            #endif
        """,
        "cpp20": """
            #if __cplusplus >= 202002L
            // C++20 is supported
            #endif
        """,
        "cpp17": """
            #if __cplusplus >= 201703L
            // C++17 is supported
            #endif
        """,
        "cpp14": """
            #if __cplusplus >= 201402L
            // C++14 is supported
            #endif
        """,
        "cpp11": """
            #if __cplusplus >= 201103L
            // C++11 is supported
            #endif
        """,
        "modules": """
            #if __has_include(<version>)
            #include <version>
            #endif
            #ifdef __cpp_modules
            // Modules are supported
            #endif
        """,
        "coroutines": """
            #ifdef __cpp_coroutines
            // Coroutines are supported
            #endif
        """,
        "concepts": """
            #ifdef __cpp_concepts
            // Concepts are supported
            #endif
        """,
        "ranges": """
            #ifdef __cpp_ranges
            // Ranges are supported
            #endif
        """,
        "std_format": """
            #ifdef __cpp_lib_format
            // std::format is supported
            #endif
        """,
        "std_span": """
            #ifdef __cpp_lib_span
            // std::span is supported
            #endif
        """,
        "std_string_view": """
            #ifdef __cpp_lib_string_view
            // std::string_view is supported
            #endif
        """,
        "std_optional": """
            #ifdef __cpp_lib_optional
            // std::optional is supported
            #endif
        """,
        "std_variant": """
            #ifdef __cpp_lib_variant
            // std::variant is supported
            #endif
        """,
        "std_any": """
            #ifdef __cpp_lib_any
            // std::any is supported
            #endif
        """,
        "std_filesystem": """
            #ifdef __cpp_lib_filesystem
            // std::filesystem is supported
            #endif
        """,
        "std_chrono": """
            #ifdef __cpp_lib_chrono
            // std::chrono is supported
            #endif
        """,
        "std_thread": """
            #ifdef __cpp_lib_thread
            // std::thread is supported
            #endif
        """,
        "std_atomic": """
            #ifdef __cpp_lib_atomic
            // std::atomic is supported
            #endif
        """,
        "std_mutex": """
            #ifdef __cpp_lib_mutex
            // std::mutex is supported
            #endif
        """,
        "std_condition_variable": """
            #ifdef __cpp_lib_condition_variable
            // std::condition_variable is supported
            #endif
        """,
        "std_future": """
            #ifdef __cpp_lib_future
            // std::future is supported
            #endif
        """,
        "std_promise": """
            #ifdef __cpp_lib_promise
            // std::promise is supported
            #endif
        """,
        "std_shared_mutex": """
            #ifdef __cpp_lib_shared_mutex
            // std::shared_mutex is supported
            #endif
        """,
        "std_shared_future": """
            #ifdef __cpp_lib_shared_future
            // std::shared_future is supported
            #endif
        """,
        "constexpr_if": """
            #ifdef __cpp_if_constexpr
            // constexpr if is supported
            #endif
        """,
        "fold_expressions": """
            #ifdef __cpp_fold_expressions
            // Fold expressions are supported
            #endif
        """,
        "structured_bindings": """
            #ifdef __cpp_structured_bindings
            // Structured bindings are supported
            #endif
        """,
        "inline_variables": """
            #ifdef __cpp_inline_variables
            // Inline variables are supported
            #endif
        """,
        "std_byte": """
            #ifdef __cpp_lib_byte
            // std::byte is supported
            #endif
        """,
        "std_invoke": """
            #ifdef __cpp_lib_invoke
            // std::invoke is supported
            #endif
        """,
        "std_apply": """
            #ifdef __cpp_lib_apply
            // std::apply is supported
            #endif
        """,
        "std_make_from_tuple": """
            #ifdef __cpp_lib_make_from_tuple
            // std::make_from_tuple is supported
            #endif
        """,
        "std_clamp": """
            #ifdef __cpp_lib_clamp
            // std::clamp is supported
            #endif
        """,
        "std_gcd": """
            #ifdef __cpp_lib_gcd_lcm
            // std::gcd is supported
            #endif
        """,
        "std_lcm": """
            #ifdef __cpp_lib_gcd_lcm
            // std::lcm is supported
            #endif
        """,
        "std_execution": """
            #ifdef __cpp_lib_execution
            // Parallel algorithms are supported
            #endif
        """,
        "std_memory_resource": """
            #ifdef __cpp_lib_memory_resource
            // std::pmr is supported
            #endif
        """,
        "std_string": """
            #include <string>
            // std::string is always supported
        """,
        "std_vector": """
            #include <vector>
            // std::vector is always supported
        """,
        "std_map": """
            #include <map>
            // std::map is always supported
        """,
        "std_unordered_map": """
            #ifdef __cpp_lib_unordered_map
            // std::unordered_map is supported
            #endif
        """,
        "std_set": """
            #include <set>
            // std::set is always supported
        """,
        "std_unordered_set": """
            #ifdef __cpp_lib_unordered_set
            // std::unordered_set is supported
            #endif
        """,
        "std_array": """
            #ifdef __cpp_lib_array
            // std::array is supported
            #endif
        """,
        "std_tuple": """
            #ifdef __cpp_lib_tuple
            // std::tuple is supported
            #endif
        """,
        "std_function": """
            #ifdef __cpp_lib_functional
            // std::function is supported
            #endif
        """,
        "std_unique_ptr": """
            #ifdef __cpp_lib_smart_ptr
            // std::unique_ptr is supported
            #endif
        """,
        "std_shared_ptr": """
            #ifdef __cpp_lib_shared_ptr
            // std::shared_ptr is supported
            #endif
        """,
        "std_weak_ptr": """
            #ifdef __cpp_lib_shared_ptr
            // std::weak_ptr is supported
            #endif
        """
    }
    
    # Compiler-specific flags for capability detection
    COMPILER_FLAGS: Dict[str, List[str]] = {
        COMPILER_MSVC: ["/EHsc", "/std:c++latest"],
        COMPILER_MSVC_CLANG: ["/EHsc", "/std:c++latest"],
        COMPILER_MINGW_GCC: ["-std=c++23", "-E"],
        COMPILER_MINGW_CLANG: ["-std=c++23", "-E"],
        COMPILER_GCC: ["-std=c++23", "-E"],
        COMPILER_CLANG: ["-std=c++23", "-E"]
    }
    
    # Predefined capabilities based on compiler type and version
    PREDEFINED_CAPABILITIES: Dict[str, Dict[str, Set[str]]] = {
        COMPILER_MSVC: {
            "19.30": {"cpp20", "cpp17", "cpp14", "cpp11", "concepts", "ranges", "std_format", "std_span", "std_string_view", "std_optional", "std_variant", "std_any", "std_filesystem", "std_chrono", "std_thread", "std_atomic", "std_mutex", "std_condition_variable", "std_future", "std_promise", "std_shared_mutex", "std_shared_future", "constexpr_if", "fold_expressions", "structured_bindings", "inline_variables", "std_byte", "std_invoke", "std_apply", "std_make_from_tuple", "std_clamp", "std_gcd", "std_lcm", "std_execution", "std_memory_resource", "std_string", "std_vector", "std_map", "std_unordered_map", "std_set", "std_unordered_set", "std_array", "std_tuple", "std_function", "std_unique_ptr", "std_shared_ptr", "std_weak_ptr", "msvc_compatibility"},
            "19.40": {"cpp23", "cpp20", "cpp17", "cpp14", "cpp11", "modules", "coroutines", "concepts", "ranges", "std_format", "std_span", "std_string_view", "std_optional", "std_variant", "std_any", "std_filesystem", "std_chrono", "std_thread", "std_atomic", "std_mutex", "std_condition_variable", "std_future", "std_promise", "std_shared_mutex", "std_shared_future", "constexpr_if", "fold_expressions", "structured_bindings", "inline_variables", "std_byte", "std_invoke", "std_apply", "std_make_from_tuple", "std_clamp", "std_gcd", "std_lcm", "std_execution", "std_memory_resource", "std_string", "std_vector", "std_map", "std_unordered_map", "std_set", "std_unordered_set", "std_array", "std_tuple", "std_function", "std_unique_ptr", "std_shared_ptr", "std_weak_ptr", "msvc_compatibility"}
        },
        COMPILER_MSVC_CLANG: {
            "16.0": {"cpp20", "cpp17", "cpp14", "cpp11", "modules", "coroutines", "concepts", "ranges", "std_format", "std_span", "std_string_view", "std_optional", "std_variant", "std_any", "std_filesystem", "std_chrono", "std_thread", "std_atomic", "std_mutex", "std_condition_variable", "std_future", "std_promise", "std_shared_mutex", "std_shared_future", "constexpr_if", "fold_expressions", "structured_bindings", "inline_variables", "std_byte", "std_invoke", "std_apply", "std_make_from_tuple", "std_clamp", "std_gcd", "std_lcm", "std_execution", "std_memory_resource", "std_string", "std_vector", "std_map", "std_unordered_map", "std_set", "std_unordered_set", "std_array", "std_tuple", "std_function", "std_unique_ptr", "std_shared_ptr", "std_weak_ptr", "msvc_compatibility", "clang_compatibility"},
            "17.0": {"cpp23", "cpp20", "cpp17", "cpp14", "cpp11", "modules", "coroutines", "concepts", "ranges", "std_format", "std_span", "std_string_view", "std_optional", "std_variant", "std_any", "std_filesystem", "std_chrono", "std_thread", "std_atomic", "std_mutex", "std_condition_variable", "std_future", "std_promise", "std_shared_mutex", "std_shared_future", "constexpr_if", "fold_expressions", "structured_bindings", "inline_variables", "std_byte", "std_invoke", "std_apply", "std_make_from_tuple", "std_clamp", "std_gcd", "std_lcm", "std_execution", "std_memory_resource", "std_string", "std_vector", "std_map", "std_unordered_map", "std_set", "std_unordered_set", "std_array", "std_tuple", "std_function", "std_unique_ptr", "std_shared_ptr", "std_weak_ptr", "msvc_compatibility", "clang_compatibility"}
        },
        COMPILER_MINGW_GCC: {
            "12.0": {"cpp20", "cpp17", "cpp14", "cpp11", "modules", "coroutines", "concepts", "ranges", "std_format", "std_span", "std_string_view", "std_optional", "std_variant", "std_any", "std_filesystem", "std_chrono", "std_thread", "std_atomic", "std_mutex", "std_condition_variable", "std_future", "std_promise", "std_shared_mutex", "std_shared_future", "constexpr_if", "fold_expressions", "structured_bindings", "inline_variables", "std_byte", "std_invoke", "std_apply", "std_make_from_tuple", "std_clamp", "std_gcd", "std_lcm", "std_execution", "std_memory_resource", "std_string", "std_vector", "std_map", "std_unordered_map", "std_set", "std_unordered_set", "std_array", "std_tuple", "std_function", "std_unique_ptr", "std_shared_ptr", "std_weak_ptr", "mingw_compatibility", "gcc_compatibility"},
            "13.0": {"cpp23", "cpp20", "cpp17", "cpp14", "cpp11", "modules", "coroutines", "concepts", "ranges", "std_format", "std_span", "std_string_view", "std_optional", "std_variant", "std_any", "std_filesystem", "std_chrono", "std_thread", "std_atomic", "std_mutex", "std_condition_variable", "std_future", "std_promise", "std_shared_mutex", "std_shared_future", "constexpr_if", "fold_expressions", "structured_bindings", "inline_variables", "std_byte", "std_invoke", "std_apply", "std_make_from_tuple", "std_clamp", "std_gcd", "std_lcm", "std_execution", "std_memory_resource", "std_string", "std_vector", "std_map", "std_unordered_map", "std_set", "std_unordered_set", "std_array", "std_tuple", "std_function", "std_unique_ptr", "std_shared_ptr", "std_weak_ptr", "mingw_compatibility", "gcc_compatibility"}
        },
        COMPILER_MINGW_CLANG: {
            "16.0": {"cpp20", "cpp17", "cpp14", "cpp11", "modules", "coroutines", "concepts", "ranges", "std_format", "std_span", "std_string_view", "std_optional", "std_variant", "std_any", "std_filesystem", "std_chrono", "std_thread", "std_atomic", "std_mutex", "std_condition_variable", "std_future", "std_promise", "std_shared_mutex", "std_shared_future", "constexpr_if", "fold_expressions", "structured_bindings", "inline_variables", "std_byte", "std_invoke", "std_apply", "std_make_from_tuple", "std_clamp", "std_gcd", "std_lcm", "std_execution", "std_memory_resource", "std_string", "std_vector", "std_map", "std_unordered_map", "std_set", "std_unordered_set", "std_array", "std_tuple", "std_function", "std_unique_ptr", "std_shared_ptr", "std_weak_ptr", "mingw_compatibility", "clang_compatibility"},
            "17.0": {"cpp23", "cpp20", "cpp17", "cpp14", "cpp11", "modules", "coroutines", "concepts", "ranges", "std_format", "std_span", "std_string_view", "std_optional", "std_variant", "std_any", "std_filesystem", "std_chrono", "std_thread", "std_atomic", "std_mutex", "std_condition_variable", "std_future", "std_promise", "std_shared_mutex", "std_shared_future", "constexpr_if", "fold_expressions", "structured_bindings", "inline_variables", "std_byte", "std_invoke", "std_apply", "std_make_from_tuple", "std_clamp", "std_gcd", "std_lcm", "std_execution", "std_memory_resource", "std_string", "std_vector", "std_map", "std_unordered_map", "std_set", "std_unordered_set", "std_array", "std_tuple", "std_function", "std_unique_ptr", "std_shared_ptr", "std_weak_ptr", "mingw_compatibility", "clang_compatibility"}
        },
        COMPILER_GCC: {
            "11.0": {"cpp20", "cpp17", "cpp14", "cpp11", "modules", "coroutines", "concepts", "ranges", "std_format", "std_span", "std_string_view", "std_optional", "std_variant", "std_any", "std_filesystem", "std_chrono", "std_thread", "std_atomic", "std_mutex", "std_condition_variable", "std_future", "std_promise", "std_shared_mutex", "std_shared_future", "constexpr_if", "fold_expressions", "structured_bindings", "inline_variables", "std_byte", "std_invoke", "std_apply", "std_make_from_tuple", "std_clamp", "std_gcd", "std_lcm", "std_execution", "std_memory_resource", "std_string", "std_vector", "std_map", "std_unordered_map", "std_set", "std_unordered_set", "std_array", "std_tuple", "std_function", "std_unique_ptr", "std_shared_ptr", "std_weak_ptr", "gcc_compatibility"},
            "13.0": {"cpp23", "cpp20", "cpp17", "cpp14", "cpp11", "modules", "coroutines", "concepts", "ranges", "std_format", "std_span", "std_string_view", "std_optional", "std_variant", "std_any", "std_filesystem", "std_chrono", "std_thread", "std_atomic", "std_mutex", "std_condition_variable", "std_future", "std_promise", "std_shared_mutex", "std_shared_future", "constexpr_if", "fold_expressions", "structured_bindings", "inline_variables", "std_byte", "std_invoke", "std_apply", "std_make_from_tuple", "std_clamp", "std_gcd", "std_lcm", "std_execution", "std_memory_resource", "std_string", "std_vector", "std_map", "std_unordered_map", "std_set", "std_unordered_set", "std_array", "std_tuple", "std_function", "std_unique_ptr", "std_shared_ptr", "std_weak_ptr", "gcc_compatibility"}
        },
        COMPILER_CLANG: {
            "16.0": {"cpp20", "cpp17", "cpp14", "cpp11", "modules", "coroutines", "concepts", "ranges", "std_format", "std_span", "std_string_view", "std_optional", "std_variant", "std_any", "std_filesystem", "std_chrono", "std_thread", "std_atomic", "std_mutex", "std_condition_variable", "std_future", "std_promise", "std_shared_mutex", "std_shared_future", "constexpr_if", "fold_expressions", "structured_bindings", "inline_variables", "std_byte", "std_invoke", "std_apply", "std_make_from_tuple", "std_clamp", "std_gcd", "std_lcm", "std_execution", "std_memory_resource", "std_string", "std_vector", "std_map", "std_unordered_map", "std_set", "std_unordered_set", "std_array", "std_tuple", "std_function", "std_unique_ptr", "std_shared_ptr", "std_weak_ptr", "clang_compatibility"},
            "17.0": {"cpp23", "cpp20", "cpp17", "cpp14", "cpp11", "modules", "coroutines", "concepts", "ranges", "std_format", "std_span", "std_string_view", "std_optional", "std_variant", "std_any", "std_filesystem", "std_chrono", "std_thread", "std_atomic", "std_mutex", "std_condition_variable", "std_future", "std_promise", "std_shared_mutex", "std_shared_future", "constexpr_if", "fold_expressions", "structured_bindings", "inline_variables", "std_byte", "std_invoke", "std_apply", "std_make_from_tuple", "std_clamp", "std_gcd", "std_lcm", "std_execution", "std_memory_resource", "std_string", "std_vector", "std_map", "std_unordered_map", "std_set", "std_unordered_set", "std_array", "std_tuple", "std_function", "std_unique_ptr", "std_shared_ptr", "std_weak_ptr", "clang_compatibility"}
        }
    }
    
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        """Initialize capability detector
        
        Args:
            logger: Logger instance (optional)
        """
        self._logger = logger or logging.getLogger(__name__)
    
    def detect_capabilities(
        self,
        compiler_path: str,
        compiler_type: str,
        version: Optional[str] = None
    ) -> CapabilityInfo:
        """Detect compiler capabilities
        
        Args:
            compiler_path: Path to compiler executable
            compiler_type: Type of compiler (msvc, msvc_clang, mingw_gcc, etc.)
            version: Compiler version string (optional, for predefined capabilities)
            
        Returns:
            CapabilityInfo with detected capabilities
        """
        self._logger.info(
            f"Detecting capabilities for {compiler_type} at {compiler_path}"
        )
        
        # Try to use predefined capabilities first
        if version:
            predefined_caps = self._get_predefined_capabilities(
                compiler_type,
                version
            )
            if predefined_caps:
                self._logger.info(
                    f"Using predefined capabilities for {compiler_type} {version}"
                )
                return predefined_caps
        
        # Fall back to runtime detection
        self._logger.info(
            f"Performing runtime capability detection for {compiler_type}"
        )
        return self._detect_capabilities_runtime(
            compiler_path,
            compiler_type
        )
    
    def parse_capabilities(
        self,
        output: str,
        compiler_type: str
    ) -> CapabilityInfo:
        """Parse capabilities from compiler output
        
        Args:
            output: Compiler output text
            compiler_type: Type of compiler
            
        Returns:
            CapabilityInfo with parsed capabilities
        """
        self._logger.debug(
            f"Parsing capabilities from {compiler_type} output"
        )
        
        capabilities = CapabilityInfo()
        
        # Parse C++ standard macros
        cpp_standard = self._parse_cpp_standard(output)
        if cpp_standard:
            self._logger.debug(f"Detected C++ standard: {cpp_standard}")
            if cpp_standard >= 23:
                capabilities.cpp23 = True
                capabilities.cpp20 = True
                capabilities.cpp17 = True
                capabilities.cpp14 = True
                capabilities.cpp11 = True
            elif cpp_standard >= 20:
                capabilities.cpp20 = True
                capabilities.cpp17 = True
                capabilities.cpp14 = True
                capabilities.cpp11 = True
            elif cpp_standard >= 17:
                capabilities.cpp17 = True
                capabilities.cpp14 = True
                capabilities.cpp11 = True
            elif cpp_standard >= 14:
                capabilities.cpp14 = True
                capabilities.cpp11 = True
            elif cpp_standard >= 11:
                capabilities.cpp11 = True
        
        # Parse feature macros
        feature_macros = self._parse_feature_macros(output)
        for feature in feature_macros:
            setattr(capabilities, feature, True)
        
        # Set compatibility flags based on compiler type
        if compiler_type == self.COMPILER_MSVC:
            capabilities.msvc_compatibility = True
        elif compiler_type == self.COMPILER_MSVC_CLANG:
            capabilities.msvc_compatibility = True
            capabilities.clang_compatibility = True
        elif compiler_type == self.COMPILER_MINGW_GCC:
            capabilities.mingw_compatibility = True
            capabilities.gcc_compatibility = True
        elif compiler_type == self.COMPILER_MINGW_CLANG:
            capabilities.mingw_compatibility = True
            capabilities.clang_compatibility = True
        elif compiler_type == self.COMPILER_GCC:
            capabilities.gcc_compatibility = True
        elif compiler_type == self.COMPILER_CLANG:
            capabilities.clang_compatibility = True
        
        return capabilities
    
    def has_capability(
        self,
        compiler_path: str,
        compiler_type: str,
        capability: str,
        version: Optional[str] = None
    ) -> bool:
        """Check if compiler has a specific capability
        
        Args:
            compiler_path: Path to compiler executable
            compiler_type: Type of compiler
            capability: Capability name to check
            version: Compiler version string (optional)
            
        Returns:
            True if compiler has the capability, False otherwise
        """
        self._logger.debug(
            f"Checking capability '{capability}' for {compiler_type}"
        )
        
        # Detect capabilities
        capabilities = self.detect_capabilities(
            compiler_path,
            compiler_type,
            version
        )
        
        # Check if capability exists
        has_cap = getattr(capabilities, capability, False)
        
        self._logger.debug(
            f"Capability '{capability}' for {compiler_type}: {has_cap}"
        )
        
        return has_cap
    
    def get_supported_standards(
        self,
        compiler_path: str,
        compiler_type: str,
        version: Optional[str] = None
    ) -> List[str]:
        """Get supported C++ standards
        
        Args:
            compiler_path: Path to compiler executable
            compiler_type: Type of compiler
            version: Compiler version string (optional)
            
        Returns:
            List of supported C++ standards
        """
        self._logger.debug(
            f"Getting supported standards for {compiler_type}"
        )
        
        # Detect capabilities
        capabilities = self.detect_capabilities(
            compiler_path,
            compiler_type,
            version
        )
        
        # Build list of supported standards
        supported_standards: List[str] = []
        
        if capabilities.cpp23:
            supported_standards.append("cpp23")
        if capabilities.cpp20:
            supported_standards.append("cpp20")
        if capabilities.cpp17:
            supported_standards.append("cpp17")
        if capabilities.cpp14:
            supported_standards.append("cpp14")
        if capabilities.cpp11:
            supported_standards.append("cpp11")
        
        self._logger.debug(
            f"Supported standards for {compiler_type}: {supported_standards}"
        )
        
        return supported_standards
    
    def validate_capabilities(
        self,
        capabilities: CapabilityInfo,
        required_capabilities: Optional[List[str]] = None
    ) -> Tuple[bool, List[str]]:
        """Validate capabilities against requirements
        
        Args:
            capabilities: CapabilityInfo to validate
            required_capabilities: List of required capabilities (optional)
            
        Returns:
            Tuple of (is_valid, list_of_missing_capabilities)
        """
        self._logger.debug("Validating capabilities")
        
        missing_capabilities: List[str] = []
        
        if required_capabilities:
            for required_cap in required_capabilities:
                if not getattr(capabilities, required_cap, False):
                    missing_capabilities.append(required_cap)
                    self._logger.warning(
                        f"Missing required capability: {required_cap}"
                    )
        
        is_valid = len(missing_capabilities) == 0
        
        if is_valid:
            self._logger.info("All required capabilities are present")
        else:
            self._logger.warning(
                f"Missing capabilities: {missing_capabilities}"
            )
        
        return is_valid, missing_capabilities
    
    def _get_predefined_capabilities(
        self,
        compiler_type: str,
        version: str
    ) -> Optional[CapabilityInfo]:
        """Get predefined capabilities for compiler type and version
        
        Args:
            compiler_type: Type of compiler
            version: Compiler version string
            
        Returns:
            CapabilityInfo if predefined capabilities exist, None otherwise
        """
        # Parse version to get major.minor
        version_parts = version.split(".")
        if len(version_parts) >= 2:
            version_key = f"{version_parts[0]}.{version_parts[1]}"
        else:
            version_key = version
        
        # Get predefined capabilities
        predefined = self.PREDEFINED_CAPABILITIES.get(compiler_type, {})
        capabilities_set = predefined.get(version_key)
        
        if not capabilities_set:
            return None
        
        # Create CapabilityInfo from set
        capabilities = CapabilityInfo()
        
        # Set compatibility flags
        if compiler_type == self.COMPILER_MSVC:
            capabilities.msvc_compatibility = True
        elif compiler_type == self.COMPILER_MSVC_CLANG:
            capabilities.msvc_compatibility = True
            capabilities.clang_compatibility = True
        elif compiler_type == self.COMPILER_MINGW_GCC:
            capabilities.mingw_compatibility = True
            capabilities.gcc_compatibility = True
        elif compiler_type == self.COMPILER_MINGW_CLANG:
            capabilities.mingw_compatibility = True
            capabilities.clang_compatibility = True
        elif compiler_type == self.COMPILER_GCC:
            capabilities.gcc_compatibility = True
        elif compiler_type == self.COMPILER_CLANG:
            capabilities.clang_compatibility = True
        
        # Set capabilities from set
        for cap_name in capabilities_set:
            setattr(capabilities, cap_name, True)
        
        return capabilities
    
    def _detect_capabilities_runtime(
        self,
        compiler_path: str,
        compiler_type: str
    ) -> CapabilityInfo:
        """Detect capabilities by running compiler tests
        
        Args:
            compiler_path: Path to compiler executable
            compiler_type: Type of compiler
            
        Returns:
            CapabilityInfo with detected capabilities
        """
        capabilities = CapabilityInfo()
        
        # Get compiler flags
        flags = self.COMPILER_FLAGS.get(compiler_type, [])
        
        # Test each capability
        for cap_name, test_code in self.CAPABILITY_TESTS.items():
            try:
                # Create temporary file with test code
                with tempfile.NamedTemporaryFile(
                    mode='w',
                    suffix='.cpp',
                    delete=False
                ) as temp_file:
                    temp_file.write(test_code)
                    temp_file_path = temp_file.name
                
                try:
                    # Try to compile test code
                    command = [compiler_path] + flags + [temp_file_path]
                    result = subprocess.run(
                        command,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    # Check if compilation succeeded
                    if result.returncode == 0:
                        setattr(capabilities, cap_name, True)
                        self._logger.debug(
                            f"Capability '{cap_name}' detected"
                        )
                    else:
                        self._logger.debug(
                            f"Capability '{cap_name}' not supported"
                        )
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                        
            except subprocess.TimeoutExpired:
                self._logger.warning(
                    f"Timeout while testing capability '{cap_name}'"
                )
            except Exception as e:
                self._logger.error(
                    f"Error testing capability '{cap_name}': {e}"
                )
        
        # Set compatibility flags based on compiler type
        if compiler_type == self.COMPILER_MSVC:
            capabilities.msvc_compatibility = True
        elif compiler_type == self.COMPILER_MSVC_CLANG:
            capabilities.msvc_compatibility = True
            capabilities.clang_compatibility = True
        elif compiler_type == self.COMPILER_MINGW_GCC:
            capabilities.mingw_compatibility = True
            capabilities.gcc_compatibility = True
        elif compiler_type == self.COMPILER_MINGW_CLANG:
            capabilities.mingw_compatibility = True
            capabilities.clang_compatibility = True
        elif compiler_type == self.COMPILER_GCC:
            capabilities.gcc_compatibility = True
        elif compiler_type == self.COMPILER_CLANG:
            capabilities.clang_compatibility = True
        
        return capabilities
    
    def _parse_cpp_standard(self, output: str) -> Optional[int]:
        """Parse C++ standard from compiler output
        
        Args:
            output: Compiler output text
            
        Returns:
            C++ standard year (e.g., 2023, 2020, 2017) or None
        """
        # Look for __cplusplus macro
        match = re.search(r'__cplusplus\s+(\d+)', output)
        if match:
            cpp_value = int(match.group(1))
            
            # Map __cplusplus values to standard years
            if cpp_value >= 202302:
                return 2023
            elif cpp_value >= 202002:
                return 2020
            elif cpp_value >= 201703:
                return 2017
            elif cpp_value >= 201402:
                return 2014
            elif cpp_value >= 201103:
                return 2011
        
        return None
    
    def _parse_feature_macros(self, output: str) -> List[str]:
        """Parse feature macros from compiler output
        
        Args:
            output: Compiler output text
            
        Returns:
            List of detected feature names
        """
        features: List[str] = []
        
        # Look for feature macros
        feature_patterns = {
            r'__cpp_modules\b': 'modules',
            r'__cpp_coroutines\b': 'coroutines',
            r'__cpp_concepts\b': 'concepts',
            r'__cpp_ranges\b': 'ranges',
            r'__cpp_lib_format\b': 'std_format',
            r'__cpp_lib_span\b': 'std_span',
            r'__cpp_lib_string_view\b': 'std_string_view',
            r'__cpp_lib_optional\b': 'std_optional',
            r'__cpp_lib_variant\b': 'std_variant',
            r'__cpp_lib_any\b': 'std_any',
            r'__cpp_lib_filesystem\b': 'std_filesystem',
            r'__cpp_lib_chrono\b': 'std_chrono',
            r'__cpp_lib_thread\b': 'std_thread',
            r'__cpp_lib_atomic\b': 'std_atomic',
            r'__cpp_lib_mutex\b': 'std_mutex',
            r'__cpp_lib_condition_variable\b': 'std_condition_variable',
            r'__cpp_lib_future\b': 'std_future',
            r'__cpp_lib_promise\b': 'std_promise',
            r'__cpp_lib_shared_mutex\b': 'std_shared_mutex',
            r'__cpp_lib_shared_future\b': 'std_shared_future',
            r'__cpp_if_constexpr\b': 'constexpr_if',
            r'__cpp_fold_expressions\b': 'fold_expressions',
            r'__cpp_structured_bindings\b': 'structured_bindings',
            r'__cpp_inline_variables\b': 'inline_variables',
            r'__cpp_lib_byte\b': 'std_byte',
            r'__cpp_lib_invoke\b': 'std_invoke',
            r'__cpp_lib_apply\b': 'std_apply',
            r'__cpp_lib_make_from_tuple\b': 'std_make_from_tuple',
            r'__cpp_lib_clamp\b': 'std_clamp',
            r'__cpp_lib_gcd_lcm\b': 'std_gcd',
            r'__cpp_lib_gcd_lcm\b': 'std_lcm',
            r'__cpp_lib_execution\b': 'std_execution',
            r'__cpp_lib_memory_resource\b': 'std_memory_resource',
            r'__cpp_lib_unordered_map\b': 'std_unordered_map',
            r'__cpp_lib_unordered_set\b': 'std_unordered_set',
            r'__cpp_lib_array\b': 'std_array',
            r'__cpp_lib_tuple\b': 'std_tuple',
            r'__cpp_lib_functional\b': 'std_function',
            r'__cpp_lib_smart_ptr\b': 'std_unique_ptr',
            r'__cpp_lib_shared_ptr\b': 'std_shared_ptr',
            r'__cpp_lib_shared_ptr\b': 'std_weak_ptr'
        }
        
        for pattern, feature in feature_patterns.items():
            if re.search(pattern, output):
                features.append(feature)
                self._logger.debug(f"Detected feature: {feature}")
        
        return features
