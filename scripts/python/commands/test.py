"""
Test command - Run tests with coverage reporting

This module provides test command for executing tests with
coverage reporting, test filtering, and result aggregation.
"""

import argparse
import os
import json
from typing import Any, Dict, Optional
from dataclasses import dataclass

from core.logger import Logger
from core.exception_handler import BuildError
from core.terminal_invoker import TerminalInvoker
from core.terminal_detector import TerminalDetector
from cmake.cmake_wrapper import CMakeWrapper


@dataclass
class CoverageReport:
    """Code coverage report data class."""
    
    line_coverage: float
    branch_coverage: float
    function_coverage: float
    total_lines: int
    covered_lines: int
    total_branches: int
    covered_branches: int
    total_functions: int
    covered_functions: int
    
    def get_summary(self) -> str:
        """Get coverage summary string.
        
        Returns:
            Formatted summary string
        """
        return (
            f"Line Coverage: {self.line_coverage:.1f}%\n"
            f"Branch Coverage: {self.branch_coverage:.1f}%\n"
            f"Function Coverage: {self.function_coverage:.1f}%"
        )


class TestCommand:
    """Run tests with coverage reporting.
    
    This command handles test execution including:
    - Test execution
    - Test selection and filtering
    - Coverage report generation
    - Test result aggregation
    - Parallel test execution
    - Progress display
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize test command.
        
        Args:
            config: Configuration dictionary containing build settings
        """
        self.config = config
        self.logger = Logger("test", config.get("logging", {}))
        
        # Initialize terminal invoker
        terminal_detector = TerminalDetector()
        terminal = terminal_detector.get_default()
        if not terminal:
            raise BuildError("No terminal detected")
        
        self.terminal_invoker = TerminalInvoker(terminal)
        
        # Initialize CMake wrapper
        self.cmake_wrapper = CMakeWrapper(config)
    
    def execute(self, args: argparse.Namespace) -> int:
        """Execute test command.
        
        Args:
            args: Command-line arguments
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            self.logger.info("Starting test execution...")
            
            # Get configuration parameters
            build_dir = getattr(args, "build_dir", "build")
            test_filter = getattr(args, "filter", None)
            coverage = getattr(args, "coverage", False)
            parallel = getattr(args, "parallel", False)
            verbose = getattr(args, "verbose", False)
            output_file = getattr(args, "output", None)
            
            # Validate build directory exists
            if not os.path.exists(build_dir):
                raise BuildError(
                    f"Build directory does not exist: {build_dir}. "
                    "Run configure and compile commands first."
                )
            
            # Build CMake test arguments
            cmake_args = self._build_cmake_args(
                build_dir=build_dir,
                test_filter=test_filter,
                coverage=coverage,
                parallel=parallel,
                verbose=verbose
            )
            
            # Execute CMake test
            self.logger.info(f"Running tests in: {os.path.abspath(build_dir)}")
            if test_filter:
                self.logger.info(f"Test filter: {test_filter}")
            if coverage:
                self.logger.info("Coverage reporting enabled")
            
            result = self.cmake_wrapper.build(cmake_args)
            
            # Parse test results
            test_results = self._parse_test_results(build_dir)
            
            # Display test results
            self._display_test_results(test_results)
            
            # Generate coverage report if requested
            if coverage:
                coverage_report = self.generate_coverage(build_dir)
                self._display_coverage_report(coverage_report)
                
                # Save coverage report if output file specified
                if output_file:
                    self._save_coverage_report(coverage_report, output_file)
            
            # Check if all tests passed
            if result.return_code != 0:
                self.logger.error("Some tests failed")
                return 1
            
            self.logger.info("All tests passed successfully")
            return 0
            
        except BuildError as e:
            self.logger.error(f"Test execution failed: {e}")
            return 1
        except Exception as e:
            self.logger.error(f"Unexpected error during test execution: {e}")
            return 1
    
    def generate_coverage(self, build_dir: str) -> CoverageReport:
        """Generate coverage report.
        
        Args:
            build_dir: Build directory
            
        Returns:
            Coverage report
        """
        self.logger.info("Generating coverage report...")
        
        # Look for coverage data files
        coverage_file = os.path.join(build_dir, "coverage.json")
        
        if not os.path.exists(coverage_file):
            self.logger.warning("Coverage data file not found")
            return CoverageReport(
                line_coverage=0.0,
                branch_coverage=0.0,
                function_coverage=0.0,
                total_lines=0,
                covered_lines=0,
                total_branches=0,
                covered_branches=0,
                total_functions=0,
                covered_functions=0
            )
        
        # Parse coverage data
        try:
            with open(coverage_file, "r", encoding="utf-8") as f:
                coverage_data = json.load(f)
            
            # Extract coverage metrics
            line_coverage = coverage_data.get("line_coverage", 0.0)
            branch_coverage = coverage_data.get("branch_coverage", 0.0)
            function_coverage = coverage_data.get("function_coverage", 0.0)
            
            total_lines = coverage_data.get("total_lines", 0)
            covered_lines = coverage_data.get("covered_lines", 0)
            total_branches = coverage_data.get("total_branches", 0)
            covered_branches = coverage_data.get("covered_branches", 0)
            total_functions = coverage_data.get("total_functions", 0)
            covered_functions = coverage_data.get("covered_functions", 0)
            
            return CoverageReport(
                line_coverage=line_coverage,
                branch_coverage=branch_coverage,
                function_coverage=function_coverage,
                total_lines=total_lines,
                covered_lines=covered_lines,
                total_branches=total_branches,
                covered_branches=covered_branches,
                total_functions=total_functions,
                covered_functions=covered_functions
            )
            
        except Exception as e:
            self.logger.error(f"Failed to parse coverage data: {e}")
            return CoverageReport(
                line_coverage=0.0,
                branch_coverage=0.0,
                function_coverage=0.0,
                total_lines=0,
                covered_lines=0,
                total_branches=0,
                covered_branches=0,
                total_functions=0,
                covered_functions=0
            )
    
    def _build_cmake_args(
        self,
        build_dir: str,
        test_filter: Optional[str],
        coverage: bool,
        parallel: bool,
        verbose: bool
    ) -> list[str]:
        """Build CMake test arguments.
        
        Args:
            build_dir: Build directory
            test_filter: Test filter regex
            coverage: Whether to enable coverage
            parallel: Whether to run tests in parallel
            verbose: Whether to enable verbose output
            
        Returns:
            List of CMake arguments
        """
        args: list[str] = []
        
        # Add test command
        args.extend(["--build", build_dir, "--target", "test"])
        
        # Add test filter if specified
        if test_filter:
            args.extend(["--test-filter", test_filter])
        
        # Add coverage flag if requested
        if coverage:
            args.append("--coverage")
        
        # Add parallel flag if requested
        if parallel:
            args.append("--parallel")
        
        # Add verbose flag if requested
        if verbose:
            args.append("--verbose")
        
        return args
    
    def _parse_test_results(self, build_dir: str) -> Dict[str, Any]:
        """Parse test results from build directory.
        
        Args:
            build_dir: Build directory
            
        Returns:
            Test results dictionary
        """
        # Look for test results file
        results_file = os.path.join(build_dir, "Testing", "TestResults.xml")
        
        if not os.path.exists(results_file):
            self.logger.warning("Test results file not found")
            return {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0
            }
        
        # Parse test results (simplified parsing)
        try:
            with open(results_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Count test results (simplified)
            total = content.count("<Test ")
            passed = content.count('Status="passed"')
            failed = content.count('Status="failed"')
            skipped = content.count('Status="skipped"')
            
            return {
                "total": total,
                "passed": passed,
                "failed": failed,
                "skipped": skipped
            }
            
        except Exception as e:
            self.logger.error(f"Failed to parse test results: {e}")
            return {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0
            }
    
    def _display_test_results(self, results: Dict[str, Any]) -> None:
        """Display test results.
        
        Args:
            results: Test results dictionary
        """
        total = results.get("total", 0)
        passed = results.get("passed", 0)
        failed = results.get("failed", 0)
        skipped = results.get("skipped", 0)
        
        self.logger.info(f"Total tests: {total}")
        self.logger.info(f"Passed: {passed}")
        self.logger.info(f"Failed: {failed}")
        self.logger.info(f"Skipped: {skipped}")
        
        if failed > 0:
            self.logger.error(f"{failed} test(s) failed")
    
    def _display_coverage_report(self, report: CoverageReport) -> None:
        """Display coverage report.
        
        Args:
            report: Coverage report
        """
        self.logger.info("\n" + "=" * 50)
        self.logger.info("Coverage Report")
        self.logger.info("=" * 50)
        self.logger.info(report.get_summary())
        self.logger.info("=" * 50)
    
    def _save_coverage_report(
        self,
        report: CoverageReport,
        output_file: str
    ) -> None:
        """Save coverage report to file.
        
        Args:
            report: Coverage report
            output_file: Output file path
        """
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({
                    "line_coverage": report.line_coverage,
                    "branch_coverage": report.branch_coverage,
                    "function_coverage": report.function_coverage,
                    "total_lines": report.total_lines,
                    "covered_lines": report.covered_lines,
                    "total_branches": report.total_branches,
                    "covered_branches": report.covered_branches,
                    "total_functions": report.total_functions,
                    "covered_functions": report.covered_functions
                }, f, indent=2)
            
            self.logger.info(f"Coverage report saved to: {output_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save coverage report: {e}")
