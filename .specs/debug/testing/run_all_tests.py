#!/usr/bin/env python3
"""
Comprehensive Testing Script for OmniCppController.py

This script tests all functionalities of OmniCppController.py with all compilers:
- Compilers: MSVC, MSVC-clang, mingw-gcc, mingw-clang
- Functionalities: help, configure, build, clean, install, test, package, format, lint
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Test configuration
COMPILERS = ["msvc", "clang-msvc", "mingw-gcc", "mingw-clang"]
FUNCTIONALITIES = {
    "help": ["--help"],
    "configure": ["configure", "--build-type", "Release"],
    "clean": ["clean"],
    "format": ["format"],
    "lint": ["lint"],
}

# Build/test/install/package commands require additional arguments
BUILD_ARGS = {
    "build": ["build", "engine", "Clean Build Pipeline", "default", "release"],
    "test": ["test", "engine", "release"],
    "install": ["install", "engine", "release"],
    "package": ["package", "engine", "release"],
}

# Output directory
OUTPUT_DIR = Path(".specs/debug/testing")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Results tracking
results = {}

def run_command(cmd, test_name, compiler=None):
    """Run a command and capture output."""
    full_cmd = ["python", "OmniCppController.py"] + cmd
    
    # Add compiler flag if specified
    if compiler and "--compiler" not in cmd:
        full_cmd.extend(["--compiler", compiler])
    
    print(f"Running: {' '.join(full_cmd)}")
    
    result = subprocess.run(
        full_cmd,
        capture_output=True,
        text=True,
        timeout=300  # 5 minute timeout
    )
    
    # Generate output filename
    if compiler:
        filename = f"{test_name}_{compiler}.md"
    else:
        filename = f"{test_name}.md"
    
    output_path = OUTPUT_DIR / filename
    
    # Write output to file
    with open(output_path, "w") as f:
        f.write(f"# Test: {test_name}")
        if compiler:
            f.write(f"\n# Compiler: {compiler}")
        f.write(f"\n# Command: {' '.join(full_cmd)}")
        f.write(f"\n# Timestamp: {datetime.now().isoformat()}")
        f.write(f"\n# Exit Code: {result.returncode}")
        f.write("\n\n## STDOUT\n")
        f.write(result.stdout)
        f.write("\n\n## STDERR\n")
        f.write(result.stderr)
    
    return {
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "output_file": str(output_path)
    }

def main():
    """Run all tests."""
    print("=" * 80)
    print("Comprehensive Testing of OmniCppController.py")
    print("=" * 80)
    
    # Test help (no compiler needed)
    print("\n[1/9] Testing --help command...")
    results["help"] = run_command(FUNCTIONALITIES["help"], "help")
    
    # Test configure with all compilers
    print("\n[2/9] Testing configure command with all compilers...")
    for compiler in COMPILERS:
        print(f"  Testing with {compiler}...")
        key = f"configure_{compiler}"
        results[key] = run_command(FUNCTIONALITIES["configure"], "configure", compiler)
    
    # Test clean (no compiler needed)
    print("\n[3/9] Testing clean command...")
    results["clean"] = run_command(FUNCTIONALITIES["clean"], "clean")
    
    # Test format (no compiler needed)
    print("\n[4/9] Testing format command...")
    results["format"] = run_command(FUNCTIONALITIES["format"], "format")
    
    # Test lint (no compiler needed)
    print("\n[5/9] Testing lint command...")
    results["lint"] = run_command(FUNCTIONALITIES["lint"], "lint")
    
    # Test build with all compilers
    print("\n[6/9] Testing build command with all compilers...")
    for compiler in COMPILERS:
        print(f"  Testing with {compiler}...")
        key = f"build_{compiler}"
        results[key] = run_command(BUILD_ARGS["build"], "build", compiler)
    
    # Test install with all compilers
    print("\n[7/9] Testing install command with all compilers...")
    for compiler in COMPILERS:
        print(f"  Testing with {compiler}...")
        key = f"install_{compiler}"
        results[key] = run_command(BUILD_ARGS["install"], "install", compiler)
    
    # Test test with all compilers
    print("\n[8/9] Testing test command with all compilers...")
    for compiler in COMPILERS:
        print(f"  Testing with {compiler}...")
        key = f"test_{compiler}"
        results[key] = run_command(BUILD_ARGS["test"], "test", compiler)
    
    # Test package with all compilers
    print("\n[9/9] Testing package command with all compilers...")
    for compiler in COMPILERS:
        print(f"  Testing with {compiler}...")
        key = f"package_{compiler}"
        results[key] = run_command(BUILD_ARGS["package"], "package", compiler)
    
    # Generate summary report
    generate_summary_report(results)
    
    print("\n" + "=" * 80)
    print("Testing complete!")
    print("=" * 80)

def generate_summary_report(results):
    """Generate a summary report of all test results."""
    report_path = OUTPUT_DIR.parent / "COMPREHENSIVE_TESTING_REPORT_ALL_COMPILERS.md"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Comprehensive Testing Report - All Compilers\n\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
        
        # Test Matrix
        f.write("## Test Matrix\n\n")
        f.write("| Functionality | MSVC | MSVC-clang | mingw-gcc | mingw-clang |\n")
        f.write("|---------------|------|------------|-----------|--------------|\n")
        
        # Help
        f.write(f"| help | {'PASS' if results['help']['exit_code'] == 0 else 'FAIL'} | N/A | N/A | N/A |\n")
        
        # Configure
        configure_row = "| configure | "
        for compiler in COMPILERS:
            key = f"configure_{compiler}"
            status = "PASS" if results[key]["exit_code"] == 0 else "FAIL"
            configure_row += f"{status} | "
        configure_row += "\n"
        f.write(configure_row)
        
        # Build
        build_row = "| build | "
        for compiler in COMPILERS:
            key = f"build_{compiler}"
            status = "PASS" if results[key]["exit_code"] == 0 else "FAIL"
            build_row += f"{status} | "
        build_row += "\n"
        f.write(build_row)
        
        # Clean
        f.write(f"| clean | {'PASS' if results['clean']['exit_code'] == 0 else 'FAIL'} | N/A | N/A | N/A |\n")
        
        # Install
        install_row = "| install | "
        for compiler in COMPILERS:
            key = f"install_{compiler}"
            status = "PASS" if results[key]["exit_code"] == 0 else "FAIL"
            install_row += f"{status} | "
        install_row += "\n"
        f.write(install_row)
        
        # Test
        test_row = "| test | "
        for compiler in COMPILERS:
            key = f"test_{compiler}"
            status = "PASS" if results[key]["exit_code"] == 0 else "FAIL"
            test_row += f"{status} | "
        test_row += "\n"
        f.write(test_row)
        
        # Package
        package_row = "| package | "
        for compiler in COMPILERS:
            key = f"package_{compiler}"
            status = "PASS" if results[key]["exit_code"] == 0 else "FAIL"
            package_row += f"{status} | "
        package_row += "\n"
        f.write(package_row)
        
        # Format
        f.write(f"| format | {'PASS' if results['format']['exit_code'] == 0 else 'FAIL'} | N/A | N/A | N/A |\n")
        
        # Lint
        f.write(f"| lint | {'PASS' if results['lint']['exit_code'] == 0 else 'FAIL'} | N/A | N/A | N/A |\n")
        
        # Errors Encountered
        f.write("\n## Errors Encountered\n\n")
        errors_found = False
        for key, result in results.items():
            if result["exit_code"] != 0:
                errors_found = True
                f.write(f"### {key}\n\n")
                f.write(f"**Exit Code:** {result['exit_code']}\n\n")
                if result["stderr"]:
                    f.write(f"**Error Output:**\n```\n{result['stderr']}\n```\n\n")
                f.write(f"**Full Output:** See `{result['output_file']}`\n\n")
        
        if not errors_found:
            f.write("No errors encountered.\n\n")
        
        # Working Functionalities
        f.write("## Working Functionalities\n\n")
        working = []
        for key, result in results.items():
            if result["exit_code"] == 0:
                working.append(key)
        
        for item in working:
            f.write(f"- {item}\n")
        
        # Broken Functionalities
        f.write("\n## Broken Functionalities\n\n")
        broken = []
        for key, result in results.items():
            if result["exit_code"] != 0:
                broken.append(key)
        
        for item in broken:
            f.write(f"- {item} (exit code: {results[item]['exit_code']})\n")
        
        # Recommendations
        f.write("\n## Recommendations\n\n")
        if broken:
            f.write("The following issues were found:\n\n")
            for item in broken:
                f.write(f"1. **{item}**: Review the error output in the corresponding test file.\n")
        else:
            f.write("All tests passed successfully. No issues found.\n")
    
    print(f"\nSummary report generated: {report_path}")

if __name__ == "__main__":
    main()
