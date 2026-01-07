"""
Test script for target platform implementations
"""

import sys
import os
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from targets.base import TargetBase
from targets.windows import WindowsTarget
from targets.linux import LinuxTarget
from targets.wasm import WasmTarget
from targets.factory import TargetFactory
from targets.manager import TargetManager


def test_base_class() -> bool:
    """Test base class abstract methods."""
    print("Testing base class...")
    
    # TargetBase should be abstract and cannot be instantiated
    try:
        base = TargetBase({})
        print("  FAIL: TargetBase should be abstract")
        return False
    except TypeError:
        print("  PASS: TargetBase is abstract")
        return True


def test_windows_target() -> bool:
    """Test Windows target implementation."""
    print("Testing Windows target...")
    
    config: Dict[str, Any] = {
        "build_type": "Release",
        "compiler": "msvc",
        "architecture": "x64",
    }
    
    target = WindowsTarget(config)
    
    # Test get_name
    name = target.get_name()
    if name != "windows":
        print(f"  FAIL: Expected name 'windows', got '{name}'")
        return False
    print(f"  PASS: get_name() = '{name}'")
    
    # Test get_platform
    platform = target.get_platform()
    if platform != "windows":
        print(f"  FAIL: Expected platform 'windows', got '{platform}'")
        return False
    print(f"  PASS: get_platform() = '{platform}'")
    
    # Test get_architecture
    arch = target.get_architecture()
    if arch != "x64":
        print(f"  FAIL: Expected architecture 'x64', got '{arch}'")
        return False
    print(f"  PASS: get_architecture() = '{arch}'")
    
    # Test configure
    try:
        target.configure(config)
        print("  PASS: configure() succeeded")
    except Exception as e:
        print(f"  FAIL: configure() raised exception: {e}")
        return False
    
    # Test validate
    if not target.validate():
        print("  FAIL: validate() returned False")
        return False
    print("  PASS: validate() returned True")
    
    # Test get_cmake_args
    args = target.get_cmake_args()
    if not isinstance(args, list):
        print(f"  FAIL: get_cmake_args() should return list, got {type(args)}")
        return False
    print(f"  PASS: get_cmake_args() returned {len(args)} arguments")
    
    # Test get_toolchain_file
    toolchain = target.get_toolchain_file()
    print(f"  PASS: get_toolchain_file() = {toolchain}")
    
    return True


def test_linux_target() -> bool:
    """Test Linux target implementation."""
    print("Testing Linux target...")
    
    config: Dict[str, Any] = {
        "build_type": "Release",
        "compiler": "gcc",
        "architecture": "x64",
    }
    
    target = LinuxTarget(config)
    
    # Test get_name
    name = target.get_name()
    if name != "linux":
        print(f"  FAIL: Expected name 'linux', got '{name}'")
        return False
    print(f"  PASS: get_name() = '{name}'")
    
    # Test get_platform
    platform = target.get_platform()
    if platform != "linux":
        print(f"  FAIL: Expected platform 'linux', got '{platform}'")
        return False
    print(f"  PASS: get_platform() = '{platform}'")
    
    # Test get_architecture
    arch = target.get_architecture()
    if arch != "x64":
        print(f"  FAIL: Expected architecture 'x64', got '{arch}'")
        return False
    print(f"  PASS: get_architecture() = '{arch}'")
    
    # Test configure
    try:
        target.configure(config)
        print("  PASS: configure() succeeded")
    except Exception as e:
        print(f"  FAIL: configure() raised exception: {e}")
        return False
    
    # Test validate
    if not target.validate():
        print("  FAIL: validate() returned False")
        return False
    print("  PASS: validate() returned True")
    
    # Test get_cmake_args
    args = target.get_cmake_args()
    if not isinstance(args, list):
        print(f"  FAIL: get_cmake_args() should return list, got {type(args)}")
        return False
    print(f"  PASS: get_cmake_args() returned {len(args)} arguments")
    
    # Test get_toolchain_file
    toolchain = target.get_toolchain_file()
    print(f"  PASS: get_toolchain_file() = {toolchain}")
    
    return True


def test_wasm_target() -> bool:
    """Test WASM target implementation."""
    print("Testing WASM target...")
    
    config: Dict[str, Any] = {
        "build_type": "Release",
        "compiler": "emscripten",
        "architecture": "wasm32",
    }
    
    target = WasmTarget(config)
    
    # Test get_name
    name = target.get_name()
    if name != "wasm":
        print(f"  FAIL: Expected name 'wasm', got '{name}'")
        return False
    print(f"  PASS: get_name() = '{name}'")
    
    # Test get_platform
    platform = target.get_platform()
    if platform != "wasm":
        print(f"  FAIL: Expected platform 'wasm', got '{platform}'")
        return False
    print(f"  PASS: get_platform() = '{platform}'")
    
    # Test get_architecture
    arch = target.get_architecture()
    if arch != "wasm32":
        print(f"  FAIL: Expected architecture 'wasm32', got '{arch}'")
        return False
    print(f"  PASS: get_architecture() = '{arch}'")
    
    # Test configure
    try:
        target.configure(config)
        print("  PASS: configure() succeeded")
    except Exception as e:
        print(f"  FAIL: configure() raised exception: {e}")
        return False
    
    # Test validate
    if not target.validate():
        print("  FAIL: validate() returned False")
        return False
    print("  PASS: validate() returned True")
    
    # Test get_cmake_args
    args = target.get_cmake_args()
    if not isinstance(args, list):
        print(f"  FAIL: get_cmake_args() should return list, got {type(args)}")
        return False
    print(f"  PASS: get_cmake_args() returned {len(args)} arguments")
    
    # Test get_toolchain_file
    toolchain = target.get_toolchain_file()
    print(f"  PASS: get_toolchain_file() = {toolchain}")
    
    return True


def test_factory() -> bool:
    """Test target factory."""
    print("Testing target factory...")
    
    config: Dict[str, Any] = {
        "build_type": "Release",
        "compiler": "auto",
        "architecture": "x64",
    }
    
    # Test creating Windows target
    try:
        windows_target = TargetFactory.create("windows", config)
        if not isinstance(windows_target, WindowsTarget):
            print("  FAIL: Factory did not create WindowsTarget")
            return False
        print("  PASS: Factory created WindowsTarget")
    except Exception as e:
        print(f"  FAIL: Factory failed to create Windows target: {e}")
        return False
    
    # Test creating Linux target
    try:
        linux_target = TargetFactory.create("linux", config)
        if not isinstance(linux_target, LinuxTarget):
            print("  FAIL: Factory did not create LinuxTarget")
            return False
        print("  PASS: Factory created LinuxTarget")
    except Exception as e:
        print(f"  FAIL: Factory failed to create Linux target: {e}")
        return False
    
    # Test creating WASM target
    try:
        wasm_target = TargetFactory.create("wasm", config)
        if not isinstance(wasm_target, WasmTarget):
            print("  FAIL: Factory did not create WasmTarget")
            return False
        print("  PASS: Factory created WasmTarget")
    except Exception as e:
        print(f"  FAIL: Factory failed to create WASM target: {e}")
        return False
    
    # Test invalid target type
    try:
        TargetFactory.create("invalid", config)
        print("  FAIL: Factory should raise ValueError for invalid target type")
        return False
    except ValueError:
        print("  PASS: Factory raised ValueError for invalid target type")
    except Exception as e:
        print(f"  FAIL: Factory raised unexpected exception: {e}")
        return False
    
    # Test get_all_targets
    all_targets = TargetFactory.get_all_targets()
    if set(all_targets) != {"windows", "linux", "wasm"}:
        print(f"  FAIL: Expected ['windows', 'linux', 'wasm'], got {all_targets}")
        return False
    print(f"  PASS: get_all_targets() = {all_targets}")
    
    # Test get_target_info
    for target_type in ["windows", "linux", "wasm"]:
        try:
            info = TargetFactory.get_target_info(target_type)
            if not isinstance(info, dict):
                print(f"  FAIL: get_target_info() should return dict for {target_type}")
                return False
            print(f"  PASS: get_target_info('{target_type}') = {info}")
        except Exception as e:
            print(f"  FAIL: get_target_info() failed for {target_type}: {e}")
            return False
    
    return True


def test_manager() -> bool:
    """Test target manager."""
    print("Testing target manager...")
    
    config: Dict[str, Any] = {
        "build_type": "Release",
        "compiler": "auto",
        "architecture": "x64",
    }
    
    manager = TargetManager(config)
    
    # Test create_target
    try:
        windows_target = manager.create_target("windows")
        if not isinstance(windows_target, WindowsTarget):
            print("  FAIL: Manager did not create WindowsTarget")
            return False
        print("  PASS: Manager created WindowsTarget")
    except Exception as e:
        print(f"  FAIL: Manager failed to create target: {e}")
        return False
    
    # Test get_current_target
    current = manager.get_current_target()
    if current is None:
        print("  FAIL: get_current_target() returned None")
        return False
    print("  PASS: get_current_target() returned target")
    
    # Test set_current_target
    try:
        manager.set_current_target("linux")
        current = manager.get_current_target()
        if not isinstance(current, LinuxTarget):
            print("  FAIL: set_current_target() did not set LinuxTarget")
            return False
        print("  PASS: set_current_target() set LinuxTarget")
    except Exception as e:
        print(f"  FAIL: set_current_target() failed: {e}")
        return False
    
    # Test validate_target
    if not manager.validate_target("windows"):
        print("  FAIL: validate_target() returned False for windows")
        return False
    print("  PASS: validate_target('windows') returned True")
    
    # Test get_all_targets
    all_targets = manager.get_all_targets()
    if set(all_targets) != {"windows", "linux", "wasm"}:
        print(f"  FAIL: Expected ['windows', 'linux', 'wasm'], got {all_targets}")
        return False
    print(f"  PASS: get_all_targets() = {all_targets}")
    
    # Test get_cmake_args
    try:
        args = manager.get_cmake_args("windows")
        if not isinstance(args, list):
            print(f"  FAIL: get_cmake_args() should return list, got {type(args)}")
            return False
        print(f"  PASS: get_cmake_args('windows') returned {len(args)} arguments")
    except Exception as e:
        print(f"  FAIL: get_cmake_args() failed: {e}")
        return False
    
    # Test get_toolchain_file
    try:
        toolchain = manager.get_toolchain_file("windows")
        print(f"  PASS: get_toolchain_file('windows') = {toolchain}")
    except Exception as e:
        print(f"  FAIL: get_toolchain_file() failed: {e}")
        return False
    
    # Test supports_cross_compilation
    if not manager.supports_cross_compilation("windows"):
        print("  FAIL: supports_cross_compilation() returned False")
        return False
    print("  PASS: supports_cross_compilation() returned True")
    
    # Test get_cross_compile_args
    try:
        args = manager.get_cross_compile_args("wasm", "windows")
        if not isinstance(args, list):
            print(f"  FAIL: get_cross_compile_args() should return list, got {type(args)}")
            return False
        print(f"  PASS: get_cross_compile_args('wasm', 'windows') returned {len(args)} arguments")
    except Exception as e:
        print(f"  FAIL: get_cross_compile_args() failed: {e}")
        return False
    
    return True


def main() -> int:
    """Run all tests."""
    print("=" * 60)
    print("Target Platform Implementation Tests")
    print("=" * 60)
    print()
    
    tests = [
        ("Base Class", test_base_class),
        ("Windows Target", test_windows_target),
        ("Linux Target", test_linux_target),
        ("WASM Target", test_wasm_target),
        ("Target Factory", test_factory),
        ("Target Manager", test_manager),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        print(f"\n--- {name} ---")
        try:
            if test_func():
                passed += 1
                print(f"[PASS] {name}")
            else:
                failed += 1
                print(f"[FAIL] {name}")
        except Exception as e:
            failed += 1
            print(f"[FAIL] {name} with exception: {e}")
            import traceback
            traceback.print_exc()
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
