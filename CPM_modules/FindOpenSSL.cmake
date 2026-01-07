include("E:/syncfold/Filen_private/dev/template/OmniCPP-template/cmake/CPM_0.40.2.cmake")

# Use a CMake-friendly OpenSSL build
CPMAddPackage(
    NAME openssl-cmake
    GITHUB_REPOSITORY janbar/openssl-cmake
    GIT_TAG master
    OPTIONS
        "BUILD_SHARED_LIBS OFF"
        "OPENSSL_BUILD_EXAMPLES OFF"
        "OPENSSL_BUILD_TESTS OFF"
        "OPENSSL_BUILD_COMMANDLINE OFF"
)

if(openssl-cmake_ADDED)
    # Debug: Print all available targets
    get_property(_targets DIRECTORY PROPERTY BUILDSYSTEM_TARGETS)
    message(STATUS "Available targets after OpenSSL CPM: ${_targets}")

    # Create the targets that Qt6 expects
    # Check what targets are available from openssl-cmake
    if(TARGET openssl::ssl)
        if(NOT TARGET OpenSSL::SSL)
            add_library(OpenSSL::SSL ALIAS openssl::ssl)
        endif()
    elseif(TARGET libssl)
        if(NOT TARGET OpenSSL::SSL)
            add_library(OpenSSL::SSL ALIAS libssl)
        endif()
    endif()

    if(TARGET openssl::crypto)
        if(NOT TARGET OpenSSL::Crypto)
            add_library(OpenSSL::Crypto ALIAS openssl::crypto)
        endif()
    elseif(TARGET libcrypto)
        if(NOT TARGET OpenSSL::Crypto)
            add_library(OpenSSL::Crypto ALIAS libcrypto)
        endif()
    endif()

    # If we have the targets, set FOUND
    if(TARGET OpenSSL::SSL AND TARGET OpenSSL::Crypto)
        set(OpenSSL_FOUND TRUE)
        message(STATUS "OpenSSL targets created successfully: OpenSSL::SSL and OpenSSL::Crypto")
    else()
        set(OpenSSL_FOUND FALSE)
        message(WARNING "OpenSSL targets not found after CPM build")
    endif()
else()
    set(OpenSSL_FOUND FALSE)
endif()