"""
Unit tests for RetryMechanism

Tests cover retry logic, exponential backoff, retryable error detection,
and statistics tracking.
"""

import subprocess
import time
import unittest
from unittest.mock import patch, MagicMock
from typing import Callable

import sys
import os

# Add parent directory to path to import module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'python'))

from compilers.retry_mechanism import RetryMechanism, RetryStats


class TestRetryMechanism(unittest.TestCase):
    """Test cases for RetryMechanism class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.retry_mech = RetryMechanism(max_retries=3, initial_delay=0.1, backoff_factor=2.0)

    def test_retry_success_on_first_attempt(self) -> None:
        """Test retry succeeds on first attempt"""
        def success_func() -> str:
            return "success"

        result = self.retry_mech.retry(success_func)
        self.assertEqual(result, "success")

        stats = self.retry_mech.get_retry_stats()
        self.assertEqual(stats.total_attempts, 1)
        self.assertEqual(stats.successful_retries, 0)
        self.assertEqual(stats.failed_retries, 0)

    def test_retry_success_after_one_retry(self) -> None:
        """Test retry succeeds after one retry"""
        attempt_count = [0]

        def flaky_func() -> str:
            attempt_count[0] += 1
            if attempt_count[0] < 2:
                raise subprocess.TimeoutExpired("cmd", 10)
            return "success"

        result = self.retry_mech.retry(flaky_func)
        self.assertEqual(result, "success")

        stats = self.retry_mech.get_retry_stats()
        self.assertEqual(stats.total_attempts, 2)
        self.assertEqual(stats.successful_retries, 0)
        self.assertEqual(stats.failed_retries, 0)

    def test_retry_success_after_multiple_retries(self) -> None:
        """Test retry succeeds after multiple retries"""
        attempt_count = [0]

        def very_flaky_func() -> str:
            attempt_count[0] += 1
            if attempt_count[0] < 3:
                raise ConnectionError("Connection failed")
            return "success"

        result = self.retry_mech.retry(very_flaky_func)
        self.assertEqual(result, "success")

        stats = self.retry_mech.get_retry_stats()
        self.assertEqual(stats.total_attempts, 3)

    def test_retry_all_attempts_fail(self) -> None:
        """Test retry fails after all attempts"""
        attempt_count = [0]

        def failing_func() -> str:
            attempt_count[0] += 1
            raise subprocess.TimeoutExpired("cmd", 10)

        with self.assertRaises(subprocess.TimeoutExpired):
            self.retry_mech.retry(failing_func)

        self.assertEqual(attempt_count[0], 4)  # 1 initial + 3 retries

        stats = self.retry_mech.get_retry_stats()
        self.assertEqual(stats.total_attempts, 4)
        self.assertEqual(stats.failed_retries, 1)

    def test_retry_non_retryable_error(self) -> None:
        """Test retry does not retry on non-retryable error"""
        attempt_count = [0]

        def non_retryable_func() -> str:
            attempt_count[0] += 1
            raise ValueError("Invalid argument")

        with self.assertRaises(ValueError):
            self.retry_mech.retry(non_retryable_func)

        # Should only attempt once for non-retryable error
        self.assertEqual(attempt_count[0], 1)

        stats = self.retry_mech.get_retry_stats()
        self.assertEqual(stats.total_attempts, 1)
        self.assertEqual(stats.failed_retries, 1)

    def test_retry_with_custom_retry_on(self) -> None:
        """Test retry with custom retry_on function"""
        attempt_count = [0]

        def custom_flaky_func() -> str:
            attempt_count[0] += 1
            if attempt_count[0] < 2:
                raise RuntimeError("Custom error")
            return "success"

        def custom_retry_on(error: Exception) -> bool:
            return isinstance(error, RuntimeError)

        result = self.retry_mech.retry(custom_flaky_func, retry_on=custom_retry_on)
        self.assertEqual(result, "success")

        self.assertEqual(attempt_count[0], 2)

    def test_retry_with_backoff_success(self) -> None:
        """Test retry_with_backoff succeeds"""
        attempt_count = [0]

        def flaky_func() -> str:
            attempt_count[0] += 1
            if attempt_count[0] < 2:
                raise subprocess.TimeoutExpired("cmd", 10)
            return "success"

        result = self.retry_mech.retry_with_backoff(flaky_func)
        self.assertEqual(result, "success")

        stats = self.retry_mech.get_retry_stats()
        self.assertEqual(stats.total_attempts, 2)

    def test_retry_with_backoff_exponential_delay(self) -> None:
        """Test retry_with_backoff uses exponential backoff"""
        attempt_count = [0]
        delays = []

        def flaky_func() -> str:
            attempt_count[0] += 1
            if attempt_count[0] < 3:
                raise subprocess.TimeoutExpired("cmd", 10)
            return "success"

        with patch('time.sleep') as mock_sleep:
            def capture_delay(delay: float) -> None:
                delays.append(delay)

            mock_sleep.side_effect = capture_delay
            self.retry_mech.retry_with_backoff(flaky_func)

            # Check exponential backoff: 0.1, 0.2, 0.4, ...
            # With initial_delay=0.1 and backoff_factor=2.0
            # First retry: 0.1 * (2.0 ** 0) = 0.1
            # Second retry: 0.1 * (2.0 ** 1) = 0.2
            self.assertEqual(len(delays), 2)
            self.assertAlmostEqual(delays[0], 0.1, places=1)
            self.assertAlmostEqual(delays[1], 0.2, places=1)

    def test_retry_with_backoff_all_attempts_fail(self) -> None:
        """Test retry_with_backoff fails after all attempts"""
        attempt_count = [0]

        def failing_func() -> str:
            attempt_count[0] += 1
            raise subprocess.TimeoutExpired("cmd", 10)

        with self.assertRaises(subprocess.TimeoutExpired):
            self.retry_mech.retry_with_backoff(failing_func)

        self.assertEqual(attempt_count[0], 4)  # 1 initial + 3 retries

    def test_retry_with_backoff_custom_retry_on(self) -> None:
        """Test retry_with_backoff with custom retry_on function"""
        attempt_count = [0]

        def custom_flaky_func() -> str:
            attempt_count[0] += 1
            if attempt_count[0] < 2:
                raise RuntimeError("Custom error")
            return "success"

        def custom_retry_on(error: Exception) -> bool:
            return isinstance(error, RuntimeError)

        result = self.retry_mech.retry_with_backoff(custom_flaky_func, retry_on=custom_retry_on)
        self.assertEqual(result, "success")

        self.assertEqual(attempt_count[0], 2)

    def test_get_retry_stats(self) -> None:
        """Test get_retry_stats returns correct statistics"""
        attempt_count = [0]

        def flaky_func() -> str:
            attempt_count[0] += 1
            if attempt_count[0] < 2:
                raise subprocess.TimeoutExpired("cmd", 10)
            return "success"

        self.retry_mech.retry(flaky_func)

        stats = self.retry_mech.get_retry_stats()
        self.assertIsInstance(stats, RetryStats)
        self.assertEqual(stats.total_attempts, 2)
        self.assertEqual(stats.successful_retries, 0)
        self.assertEqual(stats.failed_retries, 0)
        # total_retry_time is 0 because retry succeeded without exhausting all attempts
        self.assertEqual(stats.total_retry_time, 0.0)

    def test_get_retry_stats_after_failure(self) -> None:
        """Test get_retry_stats after failed retry"""
        attempt_count = [0]

        def failing_func() -> str:
            attempt_count[0] += 1
            raise subprocess.TimeoutExpired("cmd", 10)

        try:
            self.retry_mech.retry(failing_func)
        except subprocess.TimeoutExpired:
            pass

        stats = self.retry_mech.get_retry_stats()
        self.assertEqual(stats.failed_retries, 1)
        self.assertEqual(len(stats.retry_errors), 1)

    def test_clear_stats(self) -> None:
        """Test clear_stats resets statistics"""
        attempt_count = [0]

        def flaky_func() -> str:
            attempt_count[0] += 1
            if attempt_count[0] < 2:
                raise subprocess.TimeoutExpired("cmd", 10)
            return "success"

        self.retry_mech.retry(flaky_func)
        self.retry_mech.clear_stats()

        stats = self.retry_mech.get_retry_stats()
        self.assertEqual(stats.total_attempts, 0)
        self.assertEqual(stats.successful_retries, 0)
        self.assertEqual(stats.failed_retries, 0)
        self.assertEqual(stats.total_retry_time, 0.0)
        self.assertEqual(len(stats.retry_errors), 0)

    def test_retry_stats_to_dict(self) -> None:
        """Test RetryStats.to_dict() method"""
        stats = RetryStats(
            total_attempts=5,
            successful_retries=2,
            failed_retries=1,
            total_retry_time=1.5,
            retry_errors=["Error 1", "Error 2"]
        )

        stats_dict = stats.to_dict()
        self.assertEqual(stats_dict["total_attempts"], 5)
        self.assertEqual(stats_dict["successful_retries"], 2)
        self.assertEqual(stats_dict["failed_retries"], 1)
        self.assertEqual(stats_dict["total_retry_time"], 1.5)
        self.assertEqual(stats_dict["retry_errors"], ["Error 1", "Error 2"])

    def test_is_retryable_error_timeout_expired(self) -> None:
        """Test _is_retryable_error returns True for TimeoutExpired"""
        error = subprocess.TimeoutExpired("cmd", 10)
        self.assertTrue(self.retry_mech._is_retryable_error(error))

    def test_is_retryable_error_connection_error(self) -> None:
        """Test _is_retryable_error returns True for ConnectionError"""
        error = ConnectionError("Connection failed")
        self.assertTrue(self.retry_mech._is_retryable_error(error))

    def test_is_retryable_error_os_error_retryable(self) -> None:
        """Test _is_retryable_error returns True for retryable OSError"""
        # Create OSError with retryable errno (EAGAIN = 11)
        error = OSError(11, "Resource temporarily unavailable")
        self.assertTrue(self.retry_mech._is_retryable_error(error))

    def test_is_retryable_error_os_error_non_retryable(self) -> None:
        """Test _is_retryable_error returns False for non-retryable OSError"""
        # Create OSError with non-retryable errno (ENOENT = 2)
        error = OSError(2, "No such file or directory")
        self.assertFalse(self.retry_mech._is_retryable_error(error))

    def test_is_retryable_error_os_error_no_errno(self) -> None:
        """Test _is_retryable_error returns True for OSError without errno"""
        error = OSError("Generic OS error")
        # OSError without errno is considered retryable by default
        self.assertTrue(self.retry_mech._is_retryable_error(error))

    def test_is_retryable_error_other_exception(self) -> None:
        """Test _is_retryable_error returns False for other exceptions"""
        error = ValueError("Invalid value")
        self.assertFalse(self.retry_mech._is_retryable_error(error))

    def test_max_retries_property(self) -> None:
        """Test max_retries property"""
        self.assertEqual(self.retry_mech.max_retries, 3)

        retry_mech_custom = RetryMechanism(max_retries=5)
        self.assertEqual(retry_mech_custom.max_retries, 5)

    def test_initial_delay_property(self) -> None:
        """Test initial_delay property"""
        self.assertEqual(self.retry_mech.initial_delay, 0.1)

        retry_mech_custom = RetryMechanism(initial_delay=2.0)
        self.assertEqual(retry_mech_custom.initial_delay, 2.0)

    def test_backoff_factor_property(self) -> None:
        """Test backoff_factor property"""
        self.assertEqual(self.retry_mech.backoff_factor, 2.0)

        retry_mech_custom = RetryMechanism(backoff_factor=3.0)
        self.assertEqual(retry_mech_custom.backoff_factor, 3.0)

    def test_retry_with_function_arguments(self) -> None:
        """Test retry passes arguments to function correctly"""
        def func_with_args(x: int, y: str) -> str:
            return f"{x}-{y}"

        result = self.retry_mech.retry(func_with_args, 42, "test")
        self.assertEqual(result, "42-test")

    def test_retry_with_function_kwargs(self) -> None:
        """Test retry passes keyword arguments to function correctly"""
        def func_with_kwargs(a: int, b: str = "default") -> str:
            return f"{a}-{b}"

        result = self.retry_mech.retry(func_with_kwargs, a=42, b="custom")
        self.assertEqual(result, "42-custom")

    def test_retry_with_backoff_with_function_arguments(self) -> None:
        """Test retry_with_backoff passes arguments to function correctly"""
        def func_with_args(x: int, y: str) -> str:
            return f"{x}-{y}"

        result = self.retry_mech.retry_with_backoff(func_with_args, 42, "test")
        self.assertEqual(result, "42-test")

    def test_retry_with_backoff_with_function_kwargs(self) -> None:
        """Test retry_with_backoff passes keyword arguments to function correctly"""
        def func_with_kwargs(a: int, b: str = "default") -> str:
            return f"{a}-{b}"

        result = self.retry_mech.retry_with_backoff(func_with_kwargs, a=42, b="custom")
        self.assertEqual(result, "42-custom")

    def test_retry_default_parameters(self) -> None:
        """Test retry mechanism with default parameters"""
        retry_mech = RetryMechanism()

        self.assertEqual(retry_mech.max_retries, 3)
        self.assertEqual(retry_mech.initial_delay, 1.0)
        self.assertEqual(retry_mech.backoff_factor, 2.0)

    def test_retry_zero_retries(self) -> None:
        """Test retry with zero retries"""
        retry_mech = RetryMechanism(max_retries=0)
        attempt_count = [0]

        def failing_func() -> str:
            attempt_count[0] += 1
            raise subprocess.TimeoutExpired("cmd", 10)

        with self.assertRaises(subprocess.TimeoutExpired):
            retry_mech.retry(failing_func)

        # Should only attempt once (no retries)
        self.assertEqual(attempt_count[0], 1)

    def test_retry_multiple_operations(self) -> None:
        """Test retry mechanism with multiple operations"""
        attempt_count_1 = [0]
        attempt_count_2 = [0]

        def flaky_func_1() -> str:
            attempt_count_1[0] += 1
            if attempt_count_1[0] < 2:
                raise subprocess.TimeoutExpired("cmd", 10)
            return "success1"

        def flaky_func_2() -> str:
            attempt_count_2[0] += 1
            if attempt_count_2[0] < 2:
                raise ConnectionError("Connection failed")
            return "success2"

        result1 = self.retry_mech.retry(flaky_func_1)
        result2 = self.retry_mech.retry(flaky_func_2)

        self.assertEqual(result1, "success1")
        self.assertEqual(result2, "success2")

        stats = self.retry_mech.get_retry_stats()
        self.assertEqual(stats.total_attempts, 4)  # 2 for each operation


if __name__ == '__main__':
    unittest.main()
