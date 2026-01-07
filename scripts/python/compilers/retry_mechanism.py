"""
Retry Mechanism for Compiler Detection

This module provides a robust retry mechanism for handling transient errors
during compiler detection operations. It supports configurable retry attempts,
exponential backoff, and retryable error detection.
"""

import subprocess
import time
from typing import Callable, TypeVar, Optional, Dict, Any, List
from dataclasses import dataclass, field

T = TypeVar('T')




@dataclass
class RetryStats:
    """Statistics for retry operations"""
    total_attempts: int = 0
    successful_retries: int = 0
    failed_retries: int = 0
    total_retry_time: float = 0.0
    retry_errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary"""
        return {
            "total_attempts": self.total_attempts,
            "successful_retries": self.successful_retries,
            "failed_retries": self.failed_retries,
            "total_retry_time": self.total_retry_time,
            "retry_errors": self.retry_errors
        }


class RetryMechanism:
    """
    Retry mechanism for handling transient errors during compiler detection.

    This class provides configurable retry logic with exponential backoff
    for operations that may fail due to transient issues such as
    network timeouts, file locks, or temporary resource unavailability.
    """

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        backoff_factor: float = 2.0
    ) -> None:
        """
        Initialize retry mechanism.

        Args:
            max_retries: Maximum number of retry attempts (default: 3)
            initial_delay: Initial delay in seconds before first retry (default: 1.0)
            backoff_factor: Multiplier for exponential backoff (default: 2.0)
        """
        self._max_retries = max_retries
        self._initial_delay = initial_delay
        self._backoff_factor = backoff_factor
        self._stats: RetryStats = RetryStats()

    def retry(
        self,
        func: Callable[..., T],
        *args: Any,
        retry_on: Optional[Callable[[Exception], bool]] = None,
        **kwargs: Any
    ) -> T:
        """
        Execute function with retry logic.

        This method attempts to execute the provided function, retrying on
        retryable errors up to the maximum number of attempts. If all
        attempts fail, the last exception is raised.

        Args:
            func: Function to execute
            *args: Positional arguments to pass to function
            retry_on: Optional function to determine if exception should trigger retry.
                      If None, uses default retryable error detection.
            **kwargs: Keyword arguments to pass to function

        Returns:
            Result of successful function execution

        Raises:
            Exception: If all retry attempts fail

        Example:
            >>> retry_mech = RetryMechanism(max_retries=3)
            >>> result = retry_mech.retry(subprocess.run, ["gcc --version"])
        """
        last_exception: Optional[Exception] = None
        delay = self._initial_delay
        total_time = 0.0

        for attempt in range(self._max_retries + 1):
            self._stats.total_attempts += 1

            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Check if we should retry
                should_retry = retry_on(e) if retry_on else self._is_retryable_error(e)

                if not should_retry:
                    # Non-retryable error, raise immediately
                    self._stats.failed_retries += 1
                    self._stats.retry_errors.append(str(e))
                    raise

                # Check if we have retries left
                if attempt < self._max_retries:
                    # Wait before retry
                    time.sleep(delay)
                    total_time += delay
                    delay *= self._backoff_factor
                else:
                    # All retries exhausted
                    self._stats.failed_retries += 1
                    self._stats.retry_errors.append(str(e))
                    self._stats.total_retry_time += total_time
                    raise

        # This should never be reached, but type checker needs it
        if last_exception:
            raise last_exception
        raise RuntimeError("Retry failed with no exception")

    def retry_with_backoff(
        self,
        func: Callable[..., T],
        *args: Any,
        retry_on: Optional[Callable[[Exception], bool]] = None,
        **kwargs: Any
    ) -> T:
        """
        Execute function with exponential backoff retry logic.

        This method is similar to retry() but provides explicit control
        over the backoff strategy. It uses exponential backoff with
        the configured initial delay and backoff factor.

        Args:
            func: Function to execute
            *args: Positional arguments to pass to function
            retry_on: Optional function to determine if exception should trigger retry.
                      If None, uses default retryable error detection.
            **kwargs: Keyword arguments to pass to function

        Returns:
            Result of successful function execution

        Raises:
            Exception: If all retry attempts fail

        Example:
            >>> retry_mech = RetryMechanism(max_retries=3, initial_delay=1.0)
            >>> result = retry_mech.retry_with_backoff(
            ...     subprocess.run,
            ...     ["cmake --version"],
            ...     timeout=10
            ... )
        """
        last_exception: Optional[Exception] = None
        delay = self._initial_delay
        total_time = 0.0

        for attempt in range(self._max_retries + 1):
            self._stats.total_attempts += 1

            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Check if we should retry
                should_retry = retry_on(e) if retry_on else self._is_retryable_error(e)

                if not should_retry:
                    # Non-retryable error, raise immediately
                    self._stats.failed_retries += 1
                    self._stats.retry_errors.append(str(e))
                    raise

                # Check if we have retries left
                if attempt < self._max_retries:
                    # Calculate backoff delay
                    backoff_delay = delay * (self._backoff_factor ** attempt)
                    time.sleep(backoff_delay)
                    total_time += backoff_delay
                else:
                    # All retries exhausted
                    self._stats.failed_retries += 1
                    self._stats.retry_errors.append(str(e))
                    self._stats.total_retry_time += total_time
                    raise

        # This should never be reached, but type checker needs it
        if last_exception:
            raise last_exception
        raise RuntimeError("Retry failed with no exception")

    def get_retry_stats(self) -> RetryStats:
        """
        Get retry statistics.

        Returns:
            RetryStats object containing statistics about retry operations

        Example:
            >>> retry_mech = RetryMechanism()
            >>> # ... perform some retries ...
            >>> stats = retry_mech.get_retry_stats()
            >>> print(f"Total attempts: {stats.total_attempts}")
        """
        return self._stats

    def clear_stats(self) -> None:
        """
        Clear retry statistics.

        This resets all retry counters and error logs.

        Example:
            >>> retry_mech = RetryMechanism()
            >>> # ... perform some retries ...
            >>> retry_mech.clear_stats()
        """
        self._stats = RetryStats()

    def _is_retryable_error(self, error: Exception) -> bool:
        """
        Determine if an error is retryable.

        Args:
            error: Exception to check

        Returns:
            True if error is retryable, False otherwise
        """
        # Check for subprocess timeout
        if isinstance(error, subprocess.TimeoutExpired):
            return True

        # Check for connection errors
        if isinstance(error, ConnectionError):
            return True

        # Check for OS errors (file locks, temporary unavailability)
        if isinstance(error, OSError):
            # Some OS errors are not retryable (e.g., file not found)
            # We retry on specific error codes
            if hasattr(error, 'errno') and error.errno is not None:
                # Retry on: EAGAIN (11), EWOULDBLOCK (11), EINTR (4)
                # These are typically transient errors
                retryable_errnos = [11, 4]  # EAGAIN/EWOULDBLOCK, EINTR
                return error.errno in retryable_errnos
            return True

        # Default to not retryable for unknown errors
        return False

    @property
    def max_retries(self) -> int:
        """Get maximum number of retry attempts"""
        return self._max_retries

    @property
    def initial_delay(self) -> float:
        """Get initial delay in seconds"""
        return self._initial_delay

    @property
    def backoff_factor(self) -> float:
        """Get backoff factor"""
        return self._backoff_factor
