"""
Unit tests for FallbackMechanism

Tests fallback registration, execution, chain retrieval, and clearing.
"""

import pytest
from typing import Optional

from scripts.python.compilers.fallback_mechanism import (
    FallbackMechanism,
    FallbackCondition,
    FallbackEntry,
    FallbackResult
)


class CustomError(Exception):
    """Custom exception for testing."""
    def __init__(self, message: str, code: Optional[str] = None):
        super().__init__(message)
        self.code = code


class TestFallbackCondition:
    """Test FallbackCondition class."""
    
    def test_matches_by_error_type(self):
        """Test matching by error type."""
        condition = FallbackCondition(error_type=ValueError)
        
        assert condition.matches(ValueError("test"))
        assert not condition.matches(TypeError("test"))
    
    def test_matches_by_error_code(self):
        """Test matching by error code."""
        error = CustomError("test", code="ERR_001")
        condition = FallbackCondition(error_code="ERR_001")
        
        assert condition.matches(error)
        
        error_no_code = CustomError("test")
        assert not condition.matches(error_no_code)
    
    def test_matches_by_custom_predicate(self):
        """Test matching by custom predicate."""
        condition = FallbackCondition(
            custom_predicate=lambda e: "timeout" in str(e).lower()
        )
        
        assert condition.matches(Exception("Operation timeout"))
        assert not condition.matches(Exception("Operation failed"))
    
    def test_matches_multiple_conditions(self):
        """Test matching with multiple conditions."""
        error = CustomError("test", code="ERR_001")
        condition = FallbackCondition(
            error_type=CustomError,
            error_code="ERR_001"
        )
        
        assert condition.matches(error)
        
        # Wrong type
        assert not condition.matches(ValueError("test", "ERR_001"))
        
        # Wrong code
        assert not condition.matches(CustomError("test", code="ERR_002"))
    
    def test_matches_no_conditions(self):
        """Test matching with no conditions (always matches)."""
        condition = FallbackCondition()
        
        assert condition.matches(Exception("any error"))
        assert condition.matches(ValueError("any error"))
        assert condition.matches(CustomError("any error"))


class TestFallbackEntry:
    """Test FallbackEntry class."""
    
    def test_comparison_by_priority(self):
        """Test comparison by priority."""
        def method1():
            return None
        
        def method2():
            return None
        
        def method3():
            return None
        
        entry1 = FallbackEntry(name="method1", method=method1, priority=5)
        entry2 = FallbackEntry(name="method2", method=method2, priority=10)
        entry3 = FallbackEntry(name="method3", method=method3, priority=5)
        
        # Higher priority should be "less than" (for sorting)
        assert entry2 < entry1
        assert not (entry1 < entry3)  # Equal priority
    
    def test_entry_creation(self):
        """Test creating fallback entry."""
        def test_method():
            return "result"
        
        condition = FallbackCondition(error_type=ValueError)
        
        entry = FallbackEntry(
            name="test_method",
            method=test_method,
            priority=10,
            condition=condition
        )
        
        assert entry.name == "test_method"
        assert entry.method == test_method
        assert entry.priority == 10
        assert entry.condition == condition


class TestFallbackMechanismRegistration:
    """Test fallback registration."""
    
    def test_register_single_fallback(self):
        """Test registering a single fallback."""
        fallback = FallbackMechanism()
        
        def test_method():
            return "result"
        
        fallback.register_fallback("test_op", test_method, priority=10)
        
        assert fallback.has_fallbacks("test_op")
        assert fallback.get_fallback_count("test_op") == 1
    
    def test_register_multiple_fallbacks(self):
        """Test registering multiple fallbacks."""
        fallback = FallbackMechanism()
        
        def method1():
            return "result1"
        
        def method2():
            return "result2"
        
        def method3():
            return "result3"
        
        fallback.register_fallback("test_op", method1, priority=10)
        fallback.register_fallback("test_op", method2, priority=5)
        fallback.register_fallback("test_op", method3, priority=15)
        
        assert fallback.get_fallback_count("test_op") == 3
    
    def test_register_different_operations(self):
        """Test registering fallbacks for different operations."""
        fallback = FallbackMechanism()
        
        def method1():
            return "result1"
        
        def method2():
            return "result2"
        
        fallback.register_fallback("op1", method1, priority=10)
        fallback.register_fallback("op2", method2, priority=10)
        
        assert fallback.get_fallback_count("op1") == 1
        assert fallback.get_fallback_count("op2") == 1
        assert len(fallback.get_operations()) == 2
    
    def test_register_with_condition(self):
        """Test registering fallback with condition."""
        fallback = FallbackMechanism()
        condition = FallbackCondition(error_type=ValueError)
        
        def test_method():
            return "result"
        
        fallback.register_fallback("test_op", test_method, priority=10, condition=condition)
        
        chain = fallback.get_fallback_chain("test_op")
        assert len(chain) == 1
        assert chain[0].condition == condition
    
    def test_register_empty_operation_name_raises_error(self):
        """Test that empty operation name raises error."""
        fallback = FallbackMechanism()
        
        with pytest.raises(ValueError, match="operation_name cannot be empty"):
            fallback.register_fallback("", lambda: "result", priority=10)
    
    def test_register_none_method_raises_error(self):
        """Test that None method raises error."""
        fallback = FallbackMechanism()
        
        with pytest.raises(ValueError, match="method cannot be None"):
            fallback.register_fallback("test_op", None, priority=10)  # type: ignore
    
    def test_priority_sorting(self):
        """Test that fallbacks are sorted by priority."""
        fallback = FallbackMechanism()
        
        def low_method():
            return "low"
        
        def high_method():
            return "high"
        
        def medium_method():
            return "medium"
        
        fallback.register_fallback("test_op", low_method, priority=1)
        fallback.register_fallback("test_op", high_method, priority=10)
        fallback.register_fallback("test_op", medium_method, priority=5)
        
        chain = fallback.get_fallback_chain("test_op")
        names = [entry.name for entry in chain]
        
        # Should be sorted by priority (highest first)
        assert names[0] == "high_method"
        assert names[1] == "medium_method"
        assert names[2] == "low_method"


class TestFallbackMechanismExecution:
    """Test fallback execution."""
    
    def test_execute_successful_fallback(self):
        """Test executing a successful fallback."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("test_op", lambda: "result", priority=10)
        
        result = fallback.execute_with_fallback("test_op")
        
        assert result == "result"
    
    def test_execute_with_arguments(self):
        """Test executing fallback with arguments."""
        fallback = FallbackMechanism()
        
        def add(a: int, b: int) -> int:
            return a + b
        
        fallback.register_fallback("add", add, priority=10)
        
        result = fallback.execute_with_fallback("add", 3, 5)
        
        assert result == 8
    
    def test_execute_with_keyword_arguments(self):
        """Test executing fallback with keyword arguments."""
        fallback = FallbackMechanism()
        
        def greet(name: str, greeting: str = "Hello") -> str:
            return f"{greeting}, {name}!"
        
        fallback.register_fallback("greet", greet, priority=10)
        
        result = fallback.execute_with_fallback("greet", name="World", greeting="Hi")
        
        assert result == "Hi, World!"
    
    def test_execute_fallback_chain_primary_success(self):
        """Test fallback chain where primary succeeds."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("test_op", lambda: "primary", priority=10)
        fallback.register_fallback("test_op", lambda: "secondary", priority=5)
        fallback.register_fallback("test_op", lambda: "tertiary", priority=1)
        
        result = fallback.execute_with_fallback("test_op")
        
        assert result == "primary"
    
    def test_execute_fallback_chain_secondary_success(self):
        """Test fallback chain where secondary succeeds."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("test_op", lambda: (_ for _ in ()).throw(ValueError("fail")), priority=10)
        fallback.register_fallback("test_op", lambda: "secondary", priority=5)
        fallback.register_fallback("test_op", lambda: "tertiary", priority=1)
        
        result = fallback.execute_with_fallback("test_op")
        
        assert result == "secondary"
    
    def test_execute_fallback_chain_tertiary_success(self):
        """Test fallback chain where tertiary succeeds."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("test_op", lambda: (_ for _ in ()).throw(ValueError("fail1")), priority=10)
        fallback.register_fallback("test_op", lambda: (_ for _ in ()).throw(ValueError("fail2")), priority=5)
        fallback.register_fallback("test_op", lambda: "tertiary", priority=1)
        
        result = fallback.execute_with_fallback("test_op")
        
        assert result == "tertiary"
    
    def test_execute_all_fallbacks_fail(self):
        """Test when all fallbacks fail."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("test_op", lambda: (_ for _ in ()).throw(ValueError("fail1")), priority=10)
        fallback.register_fallback("test_op", lambda: (_ for _ in ()).throw(ValueError("fail2")), priority=5)
        fallback.register_fallback("test_op", lambda: (_ for _ in ()).throw(ValueError("fail3")), priority=1)
        
        result = fallback.execute_with_fallback("test_op")
        
        assert result is None
    
    def test_execute_with_condition_matching(self):
        """Test fallback with matching condition."""
        fallback = FallbackMechanism()
        condition = FallbackCondition(error_type=ValueError)
        
        fallback.register_fallback(
            "test_op",
            lambda: (_ for _ in ()).throw(ValueError("fail")),
            priority=10,
            condition=condition
        )
        fallback.register_fallback("test_op", lambda: "fallback", priority=5)
        
        result = fallback.execute_with_fallback("test_op")
        
        assert result == "fallback"
    
    def test_execute_with_condition_not_matching(self):
        """Test fallback with non-matching condition (should re-raise)."""
        fallback = FallbackMechanism()
        condition = FallbackCondition(error_type=ValueError)
        
        fallback.register_fallback(
            "test_op",
            lambda: (_ for _ in ()).throw(TypeError("fail")),
            priority=10,
            condition=condition
        )
        fallback.register_fallback("test_op", lambda: "fallback", priority=5)
        
        with pytest.raises(TypeError):
            fallback.execute_with_fallback("test_op")
    
    def test_execute_with_error_code_condition(self):
        """Test fallback with error code condition."""
        fallback = FallbackMechanism()
        condition = FallbackCondition(error_code="ERR_TIMEOUT")
        
        def failing_method():
            error = CustomError("timeout", code="ERR_TIMEOUT")
            raise error
        
        fallback.register_fallback("test_op", failing_method, priority=10, condition=condition)
        fallback.register_fallback("test_op", lambda: "fallback", priority=5)
        
        result = fallback.execute_with_fallback("test_op")
        
        assert result == "fallback"
    
    def test_execute_with_custom_predicate_condition(self):
        """Test fallback with custom predicate condition."""
        fallback = FallbackMechanism()
        condition = FallbackCondition(
            custom_predicate=lambda e: "timeout" in str(e).lower()
        )
        
        fallback.register_fallback(
            "test_op",
            lambda: (_ for _ in ()).throw(Exception("Operation timeout")),
            priority=10,
            condition=condition
        )
        fallback.register_fallback("test_op", lambda: "fallback", priority=5)
        
        result = fallback.execute_with_fallback("test_op")
        
        assert result == "fallback"
    
    def test_execute_with_detailed_result(self):
        """Test execute_with_fallback_result returns detailed result."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("test_op", lambda: "result", priority=10)
        
        result = fallback.execute_with_fallback_result("test_op")
        
        assert result.success is True
        assert result.result == "result"
        assert result.method_name == "<lambda>"
        assert result.attempts == 1
        assert len(result.errors) == 0
    
    def test_execute_with_detailed_result_failure(self):
        """Test execute_with_fallback_result on failure."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("test_op", lambda: (_ for _ in ()).throw(ValueError("fail")), priority=10)
        fallback.register_fallback("test_op", lambda: (_ for _ in ()).throw(ValueError("fail")), priority=5)
        
        result = fallback.execute_with_fallback_result("test_op")
        
        assert result.success is False
        assert result.result is None
        assert result.method_name is None
        assert result.attempts == 2
        assert len(result.errors) == 2
    
    def test_execute_with_detailed_result_secondary_success(self):
        """Test execute_with_fallback_result with secondary success."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("test_op", lambda: (_ for _ in ()).throw(ValueError("fail1")), priority=10)
        fallback.register_fallback("test_op", lambda: "secondary", priority=5)
        
        result = fallback.execute_with_fallback_result("test_op")
        
        assert result.success is True
        assert result.result == "secondary"
        assert result.method_name == "<lambda>"
        assert result.attempts == 2
        assert len(result.errors) == 1
    
    def test_execute_no_fallbacks_raises_error(self):
        """Test that executing non-existent operation raises error."""
        fallback = FallbackMechanism()
        
        with pytest.raises(ValueError, match="No fallbacks registered for operation"):
            fallback.execute_with_fallback("nonexistent")
    
    def test_execute_returns_none_on_none_result(self):
        """Test that None result is treated as failure."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("test_op", lambda: None, priority=10)
        fallback.register_fallback("test_op", lambda: "fallback", priority=5)
        
        result = fallback.execute_with_fallback("test_op")
        
        assert result == "fallback"


class TestFallbackMechanismChainRetrieval:
    """Test fallback chain retrieval."""
    
    def test_get_fallback_chain(self):
        """Test getting fallback chain."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("test_op", lambda: "result1", priority=10)
        fallback.register_fallback("test_op", lambda: "result2", priority=5)
        
        chain = fallback.get_fallback_chain("test_op")
        
        assert len(chain) == 2
        assert chain[0].priority == 10
        assert chain[1].priority == 5
    
    def test_get_fallback_chain_sorted(self):
        """Test that fallback chain is sorted by priority."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("test_op", lambda: "low", priority=1)
        fallback.register_fallback("test_op", lambda: "high", priority=10)
        fallback.register_fallback("test_op", lambda: "medium", priority=5)
        
        chain = fallback.get_fallback_chain("test_op")
        
        assert chain[0].priority == 10
        assert chain[1].priority == 5
        assert chain[2].priority == 1
    
    def test_get_fallback_chain_returns_copy(self):
        """Test that get_fallback_chain returns a copy."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("test_op", lambda: "result", priority=10)
        
        chain1 = fallback.get_fallback_chain("test_op")
        chain2 = fallback.get_fallback_chain("test_op")
        
        assert chain1 is not chain2
        assert chain1 == chain2
    
    def test_get_fallback_chain_nonexistent_raises_error(self):
        """Test that getting chain for non-existent operation raises error."""
        fallback = FallbackMechanism()
        
        with pytest.raises(ValueError, match="No fallbacks registered for operation"):
            fallback.get_fallback_chain("nonexistent")
    
    def test_get_fallback_names(self):
        """Test getting fallback method names."""
        fallback = FallbackMechanism()
        
        def method1():
            return "result1"
        
        def method2():
            return "result2"
        
        fallback.register_fallback("test_op", method1, priority=10)
        fallback.register_fallback("test_op", method2, priority=5)
        
        names = fallback.get_fallback_names("test_op")
        
        assert len(names) == 2
        assert "method1" in names
        assert "method2" in names
    
    def test_get_operations(self):
        """Test getting all registered operations."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("op1", lambda: "result1", priority=10)
        fallback.register_fallback("op2", lambda: "result2", priority=10)
        fallback.register_fallback("op3", lambda: "result3", priority=10)
        
        operations = fallback.get_operations()
        
        assert len(operations) == 3
        assert "op1" in operations
        assert "op2" in operations
        assert "op3" in operations
    
    def test_has_fallbacks_true(self):
        """Test has_fallbacks returns True when fallbacks exist."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("test_op", lambda: "result", priority=10)
        
        assert fallback.has_fallbacks("test_op") is True
    
    def test_has_fallbacks_false(self):
        """Test has_fallbacks returns False when no fallbacks exist."""
        fallback = FallbackMechanism()
        
        assert fallback.has_fallbacks("nonexistent") is False
    
    def test_get_fallback_count(self):
        """Test getting fallback count."""
        fallback = FallbackMechanism()
        
        assert fallback.get_fallback_count("test_op") == 0
        
        fallback.register_fallback("test_op", lambda: "result1", priority=10)
        assert fallback.get_fallback_count("test_op") == 1
        
        fallback.register_fallback("test_op", lambda: "result2", priority=5)
        assert fallback.get_fallback_count("test_op") == 2


class TestFallbackMechanismClearing:
    """Test fallback clearing."""
    
    def test_clear_all_fallbacks(self):
        """Test clearing all fallbacks."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("op1", lambda: "result1", priority=10)
        fallback.register_fallback("op2", lambda: "result2", priority=10)
        
        assert len(fallback.get_operations()) == 2
        
        fallback.clear_fallbacks()
        
        assert len(fallback.get_operations()) == 0
    
    def test_clear_specific_operation_fallbacks(self):
        """Test clearing fallbacks for specific operation."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("op1", lambda: "result1", priority=10)
        fallback.register_fallback("op2", lambda: "result2", priority=10)
        
        assert len(fallback.get_operations()) == 2
        
        fallback.clear_fallbacks("op1")
        
        assert len(fallback.get_operations()) == 1
        assert "op1" not in fallback.get_operations()
        assert "op2" in fallback.get_operations()
    
    def test_clear_nonexistent_operation(self):
        """Test clearing non-existent operation (should be safe)."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("op1", lambda: "result1", priority=10)
        
        # Should not raise error
        fallback.clear_fallbacks("nonexistent")
        
        assert len(fallback.get_operations()) == 1
    
    def test_remove_specific_fallback(self):
        """Test removing a specific fallback."""
        fallback = FallbackMechanism()
        
        def method1():
            return "result1"
        
        def method2():
            return "result2"
        
        fallback.register_fallback("test_op", method1, priority=10)
        fallback.register_fallback("test_op", method2, priority=5)
        
        assert fallback.get_fallback_count("test_op") == 2
        
        removed = fallback.remove_fallback("test_op", "method1")
        
        assert removed is True
        assert fallback.get_fallback_count("test_op") == 1
        assert "method1" not in fallback.get_fallback_names("test_op")
        assert "method2" in fallback.get_fallback_names("test_op")
    
    def test_remove_nonexistent_fallback(self):
        """Test removing non-existent fallback."""
        fallback = FallbackMechanism()
        
        fallback.register_fallback("test_op", lambda: "result", priority=10)
        
        removed = fallback.remove_fallback("test_op", "nonexistent")
        
        assert removed is False
        assert fallback.get_fallback_count("test_op") == 1
    
    def test_remove_from_nonexistent_operation(self):
        """Test removing fallback from non-existent operation."""
        fallback = FallbackMechanism()
        
        removed = fallback.remove_fallback("nonexistent", "method")
        
        assert removed is False


class TestFallbackMechanismIntegration:
    """Integration tests for fallback mechanism."""
    
    def test_compiler_detection_fallback_scenario(self):
        """Test realistic compiler detection fallback scenario."""
        fallback = FallbackMechanism()
        
        # Simulate compiler detection methods
        def detect_via_vswhere():
            # Simulate vswhere not found
            raise FileNotFoundError("vswhere.exe not found")
        
        def detect_via_registry():
            # Simulate registry access failure
            raise PermissionError("Cannot access registry")
        
        def detect_via_standard_paths():
            # Simulate successful detection
            return {"compiler": "msvc", "version": "19.40.0"}
        
        # Register fallbacks with conditions
        fallback.register_fallback(
            "detect_compiler",
            detect_via_vswhere,
            priority=10,
            condition=FallbackCondition(error_type=FileNotFoundError)
        )
        fallback.register_fallback(
            "detect_compiler",
            detect_via_registry,
            priority=5,
            condition=FallbackCondition(error_type=PermissionError)
        )
        fallback.register_fallback(
            "detect_compiler",
            detect_via_standard_paths,
            priority=1
        )
        
        result = fallback.execute_with_fallback("detect_compiler")
        
        assert result is not None
        assert result["compiler"] == "msvc"
        assert result["version"] == "19.40.0"
    
    def test_terminal_detection_fallback_scenario(self):
        """Test realistic terminal detection fallback scenario."""
        fallback = FallbackMechanism()
        
        def detect_msvc_terminal():
            # Simulate MSVC terminal not found
            return None
        
        def detect_msys2_terminal():
            # Simulate MSYS2 terminal found
            return {"terminal": "msys2", "path": r"C:\msys64\ucrt64.exe"}
        
        def detect_generic_terminal():
            # Simulate generic terminal found
            return {"terminal": "cmd", "path": r"C:\Windows\System32\cmd.exe"}
        
        # Register fallbacks
        fallback.register_fallback("detect_terminal", detect_msvc_terminal, priority=10)
        fallback.register_fallback("detect_terminal", detect_msys2_terminal, priority=5)
        fallback.register_fallback("detect_terminal", detect_generic_terminal, priority=1)
        
        result = fallback.execute_with_fallback("detect_terminal")
        
        assert result is not None
        assert result["terminal"] == "msys2"
    
    def test_version_detection_fallback_scenario(self):
        """Test realistic version detection fallback scenario."""
        fallback = FallbackMechanism()
        
        def get_version_via_executable():
            # Simulate executable not working
            raise RuntimeError("Executable failed")
        
        def get_version_via_registry():
            # Simulate registry version found
            return "19.40.0"
        
        def get_version_via_config():
            # Simulate config version found
            return "19.0.0"
        
        # Register fallbacks with conditions
        fallback.register_fallback(
            "get_version",
            get_version_via_executable,
            priority=10,
            condition=FallbackCondition(error_type=RuntimeError)
        )
        fallback.register_fallback("get_version", get_version_via_registry, priority=5)
        fallback.register_fallback("get_version", get_version_via_config, priority=1)
        
        result = fallback.execute_with_fallback("get_version")
        
        assert result == "19.40.0"
    
    def test_capability_detection_fallback_scenario(self):
        """Test realistic capability detection fallback scenario."""
        fallback = FallbackMechanism()
        
        def detect_capabilities_via_test():
            # Simulate test compilation failure
            raise Exception("Test compilation failed")
        
        def detect_capabilities_via_version():
            # Simulate version-based capability detection
            return {
                "cpp23": True,
                "cpp20": True,
                "cpp17": True,
                "modules": True
            }
        
        def detect_capabilities_default():
            # Simulate default capabilities
            return {
                "cpp23": False,
                "cpp20": True,
                "cpp17": True,
                "modules": False
            }
        
        # Register fallbacks
        fallback.register_fallback(
            "detect_capabilities",
            detect_capabilities_via_test,
            priority=10,
            condition=FallbackCondition(
                custom_predicate=lambda e: "compilation" in str(e).lower()
            )
        )
        fallback.register_fallback("detect_capabilities", detect_capabilities_via_version, priority=5)
        fallback.register_fallback("detect_capabilities", detect_capabilities_default, priority=1)
        
        result = fallback.execute_with_fallback("detect_capabilities")
        
        assert result is not None
        assert result["cpp20"] is True
        assert result["cpp17"] is True
    
    def test_complex_fallback_chain_with_conditions(self):
        """Test complex fallback chain with multiple conditions."""
        fallback = FallbackMechanism()
        
        def method1():
            raise CustomError("Error 1", code="ERR_001")
        
        def method2():
            raise CustomError("Error 2", code="ERR_002")
        
        def method3():
            return "success"
        
        # Register with different error code conditions
        fallback.register_fallback(
            "test_op",
            method1,
            priority=10,
            condition=FallbackCondition(error_code="ERR_001")
        )
        fallback.register_fallback(
            "test_op",
            method2,
            priority=5,
            condition=FallbackCondition(error_code="ERR_002")
        )
        fallback.register_fallback("test_op", method3, priority=1)
        
        result = fallback.execute_with_fallback("test_op")
        
        assert result == "success"
    
    def test_fallback_with_detailed_result_analysis(self):
        """Test analyzing detailed fallback result."""
        fallback = FallbackMechanism()
        
        def failing_method():
            raise ValueError("Test error")
        
        def success_method():
            return "success"
        
        fallback.register_fallback("test_op", failing_method, priority=10)
        fallback.register_fallback("test_op", success_method, priority=5)
        
        result = fallback.execute_with_fallback_result("test_op")
        
        assert result.success is True
        assert result.result == "success"
        assert result.attempts == 2
        assert len(result.errors) == 1
        assert isinstance(result.errors[0], ValueError)
        assert str(result.errors[0]) == "Test error"
