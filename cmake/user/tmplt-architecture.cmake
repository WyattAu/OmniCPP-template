# Licensed under the Apache License, Version 2.0 (the "License");

include(CheckCXXCompilerFlag)

function(apply_architecture_optimizations target)
    if(NOT ENABLE_ARCH_OPTIMIZATIONS)
        return()
    endif()

    message(STATUS "Applying architecture-specific optimizations for ${target}")

    # x86/x86_64 optimizations
    if(CMAKE_SYSTEM_PROCESSOR MATCHES "(x86)|(X86)|(amd64)|(AMD64)")
        # Check for AVX2 support
        check_cxx_compiler_flag("-mavx2" COMPILER_SUPPORTS_AVX2)
        if(COMPILER_SUPPORTS_AVX2)
            target_compile_options(${target} PRIVATE -mavx2)
            message(STATUS "Enabled AVX2 optimizations for ${target}")
        endif()

        # Check for AVX-512 support (more advanced CPUs)
        check_cxx_compiler_flag("-mavx512f" COMPILER_SUPPORTS_AVX512)
        if(COMPILER_SUPPORTS_AVX512 AND ENABLE_AVX512)
            target_compile_options(${target} PRIVATE -mavx512f -mavx512bw -mavx512dq -mavx512vl)
            message(STATUS "Enabled AVX-512 optimizations for ${target}")
        endif()

        # Enable FMA (Fused Multiply-Add) if available
        check_cxx_compiler_flag("-mfma" COMPILER_SUPPORTS_FMA)
        if(COMPILER_SUPPORTS_FMA)
            target_compile_options(${target} PRIVATE -mfma)
            message(STATUS "Enabled FMA optimizations for ${target}")
        endif()

    # ARM64 optimizations
    elseif(CMAKE_SYSTEM_PROCESSOR MATCHES "(aarch64)|(arm64)|(ARM64)")
        # Enable NEON by default for ARM64
        target_compile_definitions(${target} PRIVATE __ARM_NEON__)

        # Enable SVE (Scalable Vector Extension) if available (ARMv8.2+)
        check_cxx_compiler_flag("-march=armv8.2-a+sve" COMPILER_SUPPORTS_SVE)
        if(COMPILER_SUPPORTS_SVE AND ENABLE_SVE)
            target_compile_options(${target} PRIVATE -march=armv8.2-a+sve)
            message(STATUS "Enabled SVE optimizations for ${target}")
        endif()

        # Enable crypto extensions if available
        check_cxx_compiler_flag("-march=armv8-a+crypto" COMPILER_SUPPORTS_CRYPTO)
        if(COMPILER_SUPPORTS_CRYPTO AND ENABLE_CRYPTO)
            target_compile_options(${target} PRIVATE -march=armv8-a+crypto)
            message(STATUS "Enabled crypto extensions for ${target}")
        endif()

    # WebAssembly optimizations
    elseif(CMAKE_SYSTEM_NAME STREQUAL "Emscripten")
        # WebAssembly-specific optimizations
        target_compile_options(${target} PRIVATE
            -msimd128  # Enable SIMD
            -mbulk-memory  # Enable bulk memory operations
        )
        message(STATUS "Enabled WebAssembly optimizations for ${target}")
    endif()

    # Generic optimizations for all architectures
    if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        # Enable fast math optimizations (be careful with floating point precision)
        if(ENABLE_FAST_MATH)
            target_compile_options(${target} PRIVATE -ffast-math)
            message(STATUS "Enabled fast math optimizations for ${target}")
        endif()

        # Enable function sections for better LTO
        target_compile_options(${target} PRIVATE -ffunction-sections -fdata-sections)
    endif()
endfunction()