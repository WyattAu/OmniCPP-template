# ============================================================================
# OmniCpp Template - Compiler Flags Configuration
# ============================================================================
# Defines compiler-specific flags for all supported compilers
# Supports: MSVC, MSVC-Clang, MinGW-GCC, MinGW-Clang, GCC, Clang
# ============================================================================

# ============================================================================
# Compiler Detection
# ============================================================================
if(MSVC)
    set(OMNICPP_COMPILER_MSVC ON)
    set(OMNICPP_COMPILER_NAME "MSVC")
elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND MSVC)
    set(OMNICPP_COMPILER_MSVC_CLANG ON)
    set(OMNICPP_COMPILER_NAME "MSVC-Clang")
elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND MINGW)
    set(OMNICPP_COMPILER_MINGW_CLANG ON)
    set(OMNICPP_COMPILER_NAME "MinGW-Clang")
elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU" AND MINGW)
    set(OMNICPP_COMPILER_MINGW_GCC ON)
    set(OMNICPP_COMPILER_NAME "MinGW-GCC")
elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    set(OMNICPP_COMPILER_GCC ON)
    set(OMNICPP_COMPILER_NAME "GCC")
elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    set(OMNICPP_COMPILER_CLANG ON)
    set(OMNICPP_COMPILER_NAME "Clang")
else()
    message(WARNING "Unknown compiler: ${CMAKE_CXX_COMPILER_ID}")
    set(OMNICPP_COMPILER_NAME "Unknown")
endif()

# ============================================================================
# Warning Flags
# ============================================================================
if(MSVC OR OMNICPP_COMPILER_MSVC_CLANG)
    # MSVC warning flags
    add_compile_options(/W4)

    if(OMNICPP_WARNINGS_AS_ERRORS)
        add_compile_options(/WX)
    endif()
elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    # GCC/Clang warning flags
    add_compile_options(-Wall -Wextra -Wpedantic)
    add_compile_options(-Wformat=2 -Wno-format-nonliteral)
    add_compile_options(-Wshadow -Wpointer-arith -Wcast-qual)
    add_compile_options(-Wunreachable-code)

    if(OMNICPP_WARNINGS_AS_ERRORS)
        add_compile_options(-Werror)
    endif()
endif()

# ============================================================================
# MSVC-Specific Flags
# ============================================================================
if(MSVC OR OMNICPP_COMPILER_MSVC_CLANG)
    # Disable specific warnings
    add_compile_options(/wd4251) # class needs to have dll-interface
    add_compile_options(/wd4275) # non dll-interface class used as base
    add_compile_options(/wd4996) # deprecated functions

    # Enable multi-processor compilation
    add_compile_options(/MP)

    # Enable large object files
    add_compile_options(/bigobj)

    # Enable strict conformance
    add_compile_options(/permissive-)

    # Enable runtime type information
    add_compile_options(/GR)

    # Enable exception handling
    add_compile_options(/EHsc)

    # Use Unicode
    add_definitions(-DUNICODE -D_UNICODE)

    # Disable Windows macros
    add_definitions(-DNOMINMAX -DWIN32_LEAN_AND_MEAN)
endif()

# ============================================================================
# GCC-Specific Flags
# ============================================================================
if(OMNICPP_COMPILER_GCC OR OMNICPP_COMPILER_MINGW_GCC)
    # Enable color diagnostics
    add_compile_options(-fdiagnostics-color=always)

    # Enable position-independent code
    add_compile_options(-fPIC)

    # Enable hidden visibility by default
    add_compile_options(-fvisibility=hidden)

    # Enable link-time optimization
    if(CMAKE_BUILD_TYPE MATCHES "Release|RelWithDebInfo|MinSizeRel")
        add_compile_options(-flto)
        add_link_options(-flto)
    endif()

    # Enable stack protection
    add_compile_options(-fstack-protector-strong)

    # Enable fortify source
    if(CMAKE_BUILD_TYPE MATCHES "Release|RelWithDebInfo|MinSizeRel")
        add_compile_options(-D_FORTIFY_SOURCE=2)
    endif()
endif()

# ============================================================================
# Clang-Specific Flags
# ============================================================================
if(OMNICPP_COMPILER_CLANG OR OMNICPP_COMPILER_MSVC_CLANG OR OMNICPP_COMPILER_MINGW_CLANG)
    # Enable color diagnostics
    add_compile_options(-fcolor-diagnostics)

    # Enable position-independent code
    add_compile_options(-fPIC)

    # Enable hidden visibility by default
    add_compile_options(-fvisibility=hidden)

    # Enable link-time optimization
    if(CMAKE_BUILD_TYPE MATCHES "Release|RelWithDebInfo|MinSizeRel")
        add_compile_options(-flto)
        add_link_options(-flto)
    endif()

    # Enable static analyzer
    if(CMAKE_BUILD_TYPE MATCHES "Debug")
        add_compile_options(-Xanalyzer -analyzer-checker=core)
    endif()
endif()

# ============================================================================
# MinGW-Specific Flags
# ============================================================================
if(MINGW)
    # Enable static linking
    add_link_options(-static -static-libgcc -static-libstdc++)

    # Enable Unicode
    add_definitions(-DUNICODE -D_UNICODE)

    # Disable Windows macros
    add_definitions(-DNOMINMAX -DWIN32_LEAN_AND_MEAN)
endif()

# ============================================================================
# Debug Flags
# ============================================================================
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0")

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    list(APPEND CMAKE_CXX_FLAGS_DEBUG "-fno-omit-frame-pointer")
    list(APPEND CMAKE_CXX_FLAGS_DEBUG "-fno-optimize-sibling-calls")
endif()

# ============================================================================
# Release Flags
# ============================================================================
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    list(APPEND CMAKE_CXX_FLAGS_RELEASE "-march=native")
endif()

# ============================================================================
# RelWithDebInfo Flags
# ============================================================================
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "-O2 -g -DNDEBUG")

# ============================================================================
# MinSizeRel Flags
# ============================================================================
set(CMAKE_CXX_FLAGS_MINSIZEREL "-Os -DNDEBUG")

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    list(APPEND CMAKE_CXX_FLAGS_MINSIZEREL "-ffunction-sections -fdata-sections")
    list(APPEND CMAKE_CXX_FLAGS_MINSIZEREL "-Wl,--gc-sections")
endif()

# ============================================================================
# Additional Compiler Flags
# ============================================================================
if(OMNICPP_COMPILER_FLAGS)
    add_compile_options(${OMNICPP_COMPILER_FLAGS})
endif()

# ============================================================================
# Export variables
# ============================================================================
set(OMNICPP_COMPILER_NAME ${OMNICPP_COMPILER_NAME} PARENT_SCOPE)
set(OMNICPP_COMPILER_MSVC ${OMNICPP_COMPILER_MSVC} PARENT_SCOPE)
set(OMNICPP_COMPILER_MSVC_CLANG ${OMNICPP_COMPILER_MSVC_CLANG} PARENT_SCOPE)
set(OMNICPP_COMPILER_MINGW_GCC ${OMNICPP_COMPILER_MINGW_GCC} PARENT_SCOPE)
set(OMNICPP_COMPILER_MINGW_CLANG ${OMNICPP_COMPILER_MINGW_CLANG} PARENT_SCOPE)
set(OMNICPP_COMPILER_GCC ${OMNICPP_COMPILER_GCC} PARENT_SCOPE)
set(OMNICPP_COMPILER_CLANG ${OMNICPP_COMPILER_CLANG} PARENT_SCOPE)

message(STATUS "Compiler flags configured for ${OMNICPP_COMPILER_NAME}")
