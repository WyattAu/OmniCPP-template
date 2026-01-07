"""
Fallback Mechanism for Compiler Detection

This module provides a flexible fallback mechanism that allows operations to try
multiple methods in sequence, with support for priority-based ordering and
conditional fallback triggers.
"""

from typing import Callable, Optional, List, Dict, Any, Type
from dataclasses import dataclass, field


@dataclass
class FallbackCondition:
    """
    Condition for triggering a fallback.
    
    A fallback is triggered when an exception matches one or more of the
    specified conditions. All conditions must match for the fallback to trigger.
    
    Attributes:
        error_type: Exception type that triggers fallback (optional)
        error_code: Error code that triggers fallback (optional)
        custom_predicate: Custom function to evaluate error (optional)
    """
    error_type: Optional[Type[Exception]] = None
    error_code: Optional[str] = None
    custom_predicate: Optional[Callable[[Exception], bool]] = None
    
    def matches(self, error: Exception) -> bool:
        """
        Check if error matches this condition.
        
        Args:
            error: Exception to check
            
        Returns:
            True if error matches condition, False otherwise
        """
        # Check error type
        if self.error_type is not None:
            if not isinstance(error, self.error_type):
                return False
        
        # Check error code
        if self.error_code is not None:
            error_code = getattr(error, 'code', None)
            if error_code != self.error_code:
                return False
        
        # Check custom predicate
        if self.custom_predicate is not None:
            if not self.custom_predicate(error):
                return False
        
        return True


@dataclass
class FallbackEntry:
    """
    Entry in a fallback chain.
    
    Each entry represents a fallback method with its priority and condition.
    
    Attributes:
        name: Name of the fallback method
        method: Callable to execute for this fallback
        priority: Priority (higher values tried first)
        condition: Condition that triggers this fallback (optional)
    """
    name: str
    method: Callable[..., Any]
    priority: int
    condition: Optional[FallbackCondition] = None
    
    def __lt__(self, other: 'FallbackEntry') -> bool:
        """Compare entries by priority (for sorting)"""
        if self.priority == other.priority:
            return False
        return self.priority > other.priority


@dataclass
class FallbackResult:
    """
    Result of executing a fallback chain.
    
    Attributes:
        success: Whether any fallback succeeded
        result: Result from successful fallback (if any)
        method_name: Name of method that succeeded (if any)
        errors: List of errors from failed attempts
        attempts: Number of fallback attempts made
    """
    success: bool
    result: Optional[Any] = None
    method_name: Optional[str] = None
    errors: List[Exception] = field(default_factory=lambda: [])
    attempts: int = 0


class FallbackMechanism:
    """
    Fallback mechanism for compiler detection operations.
    
    This class allows registration of multiple fallback methods for a given
    operation. When execute_with_fallback is called, methods are tried in
    priority order until one succeeds or all fail.
    
    Example:
        >>> fallback = FallbackMechanism()
        >>> fallback.register_fallback("detect", method1, priority=10)
        >>> fallback.register_fallback("detect", method2, priority=5)
        >>> result = fallback.execute_with_fallback("detect", arg1, arg2)
    """
    
    def __init__(self) -> None:
        """Initialize fallback mechanism."""
        self._fallbacks: Dict[str, List[FallbackEntry]] = {}
    
    def register_fallback(
        self,
        operation_name: str,
        method: Callable[..., Any],
        priority: int,
        condition: Optional[FallbackCondition] = None
    ) -> None:
        """
        Register a fallback method for an operation.
        
        Args:
            operation_name: Name of the operation
            method: Callable to execute for this fallback
            priority: Priority (higher values tried first)
            condition: Condition that triggers this fallback (optional)
            
        Raises:
            ValueError: If operation_name is empty or method is None
        """
        if not operation_name:
            raise ValueError("operation_name cannot be empty")
        
        if method is None:
            raise ValueError("method cannot be None")
        
        # Create fallback entry
        entry = FallbackEntry(
            name=method.__name__,
            method=method,
            priority=priority,
            condition=condition
        )
        
        # Add to fallbacks dictionary
        if operation_name not in self._fallbacks:
            self._fallbacks[operation_name] = []
        
        self._fallbacks[operation_name].append(entry)
        
        # Sort by priority (highest first)
        self._fallbacks[operation_name].sort()
    
    def execute_with_fallback(
        self,
        operation_name: str,
        *args: Any,
        **kwargs: Any
    ) -> Optional[Any]:
        """
        Execute operation with fallback chain.
        
        Tries each registered fallback method in priority order until one
        succeeds or all fail. A method succeeds if it returns a non-None
        value and doesn't raise an exception.
        
        Args:
            operation_name: Name of the operation to execute
            *args: Positional arguments to pass to fallback methods
            **kwargs: Keyword arguments to pass to fallback methods
            
        Returns:
            Result from first successful fallback, or None if all fail
            
        Raises:
            ValueError: If operation_name has no registered fallbacks
        """
        if operation_name not in self._fallbacks:
            raise ValueError(f"No fallbacks registered for operation: {operation_name}")
        
        fallbacks = self._fallbacks[operation_name]
        
        # Try each fallback in priority order
        for entry in fallbacks:
            try:
                result = entry.method(*args, **kwargs)
                
                # Check if result is not None
                if result is not None:
                    return result
                    
            except Exception as e:
                # Check if this exception should trigger next fallback
                if entry.condition is not None:
                    if not entry.condition.matches(e):
                        # Condition doesn't match, re-raise
                        raise
                
                # Condition matches or no condition, continue to next fallback
                continue
        
        # All fallbacks failed
        return None
    
    def execute_with_fallback_result(
        self,
        operation_name: str,
        *args: Any,
        **kwargs: Any
    ) -> FallbackResult:
        """
        Execute operation with fallback chain and return detailed result.
        
        Similar to execute_with_fallback, but returns a FallbackResult
        object with detailed information about the execution.
        
        Args:
            operation_name: Name of the operation to execute
            *args: Positional arguments to pass to fallback methods
            **kwargs: Keyword arguments to pass to fallback methods
            
        Returns:
            FallbackResult with execution details
            
        Raises:
            ValueError: If operation_name has no registered fallbacks
        """
        if operation_name not in self._fallbacks:
            raise ValueError(f"No fallbacks registered for operation: {operation_name}")
        
        fallbacks = self._fallbacks[operation_name]
        errors: List[Exception] = []
        
        # Try each fallback in priority order
        for entry in fallbacks:
            try:
                result = entry.method(*args, **kwargs)
                
                # Check if result is not None
                if result is not None:
                    return FallbackResult(
                        success=True,
                        result=result,
                        method_name=entry.name,
                        errors=errors,
                        attempts=len(errors) + 1
                    )
                    
            except Exception as e:
                errors.append(e)
                
                # Check if this exception should trigger next fallback
                if entry.condition is not None:
                    if not entry.condition.matches(e):
                        # Condition doesn't match, return failure
                        return FallbackResult(
                            success=False,
                            errors=errors,
                            attempts=len(errors)
                        )
                
                # Condition matches or no condition, continue to next fallback
                continue
        
        # All fallbacks failed
        return FallbackResult(
            success=False,
            errors=errors,
            attempts=len(errors)
        )
    
    def get_fallback_chain(self, operation_name: str) -> List[FallbackEntry]:
        """
        Get fallback chain for an operation.
        
        Returns the list of fallback entries for the specified operation,
        sorted by priority (highest first).
        
        Args:
            operation_name: Name of the operation
            
        Returns:
            List of fallback entries sorted by priority
            
        Raises:
            ValueError: If operation_name has no registered fallbacks
        """
        if operation_name not in self._fallbacks:
            raise ValueError(f"No fallbacks registered for operation: {operation_name}")
        
        # Return a copy to prevent external modification
        return list(self._fallbacks[operation_name])
    
    def get_fallback_names(self, operation_name: str) -> List[str]:
        """
        Get names of fallback methods for an operation.
        
        Args:
            operation_name: Name of the operation
            
        Returns:
            List of fallback method names
            
        Raises:
            ValueError: If operation_name has no registered fallbacks
        """
        chain = self.get_fallback_chain(operation_name)
        return [entry.name for entry in chain]
    
    def get_operations(self) -> List[str]:
        """
        Get list of all registered operations.
        
        Returns:
            List of operation names
        """
        return list(self._fallbacks.keys())
    
    def has_fallbacks(self, operation_name: str) -> bool:
        """
        Check if operation has registered fallbacks.
        
        Args:
            operation_name: Name of the operation
            
        Returns:
            True if operation has fallbacks, False otherwise
        """
        return operation_name in self._fallbacks and len(self._fallbacks[operation_name]) > 0
    
    def clear_fallbacks(self, operation_name: Optional[str] = None) -> None:
        """
        Clear fallbacks.
        
        If operation_name is provided, clears fallbacks for that operation.
        If operation_name is None, clears all fallbacks.
        
        Args:
            operation_name: Name of operation to clear (optional)
        """
        if operation_name is None:
            # Clear all fallbacks
            self._fallbacks.clear()
        else:
            # Clear fallbacks for specific operation
            if operation_name in self._fallbacks:
                del self._fallbacks[operation_name]
    
    def remove_fallback(
        self,
        operation_name: str,
        method_name: str
    ) -> bool:
        """
        Remove a specific fallback from an operation.
        
        Args:
            operation_name: Name of the operation
            method_name: Name of the method to remove
            
        Returns:
            True if fallback was removed, False if not found
        """
        if operation_name not in self._fallbacks:
            return False
        
        # Find and remove the fallback
        original_length = len(self._fallbacks[operation_name])
        self._fallbacks[operation_name] = [
            entry for entry in self._fallbacks[operation_name]
            if entry.name != method_name
        ]
        
        # Check if any were removed
        return len(self._fallbacks[operation_name]) < original_length
    
    def get_fallback_count(self, operation_name: str) -> int:
        """
        Get number of fallbacks for an operation.
        
        Args:
            operation_name: Name of the operation
            
        Returns:
            Number of registered fallbacks
        """
        if operation_name not in self._fallbacks:
            return 0
        return len(self._fallbacks[operation_name])
