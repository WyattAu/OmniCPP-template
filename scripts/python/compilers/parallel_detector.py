"""
Parallel Compiler Detector

This module provides parallel detection of compiler installations,
allowing multiple compiler types to be detected concurrently for improved performance.
"""

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple, Any
from enum import Enum


class CompilerType(Enum):
    """Compiler type enumeration"""
    MSVC = "msvc"
    MSVC_CLANG = "msvc_clang"
    MINGW_GCC = "mingw_gcc"
    MINGW_CLANG = "mingw_clang"
    GCC = "gcc"
    CLANG = "clang"


class Architecture(Enum):
    """Architecture enumeration"""
    X64 = "x64"
    X86 = "x86"
    ARM = "arm"
    ARM64 = "arm64"


@dataclass
class VersionInfo:
    """Compiler version information"""
    major: int
    minor: int
    patch: int
    build: Optional[str] = None
    full_version: str = ""

    def __str__(self) -> str:
        if self.build:
            return f"{self.major}.{self.minor}.{self.patch}.{self.build}"
        return f"{self.major}.{self.minor}.{self.patch}"

    def __lt__(self, other: 'VersionInfo') -> bool:
        """Compare versions"""
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        if self.patch != other.patch:
            return self.patch < other.patch
        return False


@dataclass
class CapabilityInfo:
    """Compiler capability information"""
    cpp23: bool = False
    cpp20: bool = False
    cpp17: bool = False
    cpp14: bool = False
    modules: bool = False
    coroutines: bool = False
    concepts: bool = False
    ranges: bool = False
    std_format: bool = False
    msvc_compatibility: bool = False
    mingw_compatibility: bool = False

    def to_dict(self) -> Dict[str, bool]:
        return {
            "cpp23": self.cpp23,
            "cpp20": self.cpp20,
            "cpp17": self.cpp17,
            "cpp14": self.cpp14,
            "modules": self.modules,
            "coroutines": self.coroutines,
            "concepts": self.concepts,
            "ranges": self.ranges,
            "std_format": self.std_format,
            "msvc_compatibility": self.msvc_compatibility,
            "mingw_compatibility": self.mingw_compatibility
        }

    def supports_cpp_standard(self, standard: str) -> bool:
        """Check if compiler supports C++ standard"""
        return getattr(self, standard.lower(), False)


@dataclass
class EnvironmentInfo:
    """Compiler environment information"""
    path: str
    include_paths: List[str] = field(default_factory=list)
    library_paths: List[str] = field(default_factory=list)
    environment_variables: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "include_paths": self.include_paths,
            "library_paths": self.library_paths,
            "environment_variables": self.environment_variables
        }


@dataclass
class CompilerInfo:
    """Compiler information"""
    compiler_type: CompilerType
    version: VersionInfo
    path: str
    architecture: Architecture
    capabilities: CapabilityInfo
    environment: EnvironmentInfo
    metadata: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "compiler_type": self.compiler_type.value,
            "version": str(self.version),
            "path": self.path,
            "architecture": self.architecture.value,
            "capabilities": self.capabilities.to_dict(),
            "environment": self.environment.to_dict(),
            "metadata": self.metadata
        }

    def is_valid(self) -> bool:
        """Check if compiler is valid"""
        import os
        return os.path.exists(self.path)


@dataclass
class ParallelDetectionResult:
    """Result of parallel compiler detection"""
    compiler_type: str
    compilers: List[CompilerInfo]
    success: bool
    error: Optional[str] = None
    detection_time: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "compiler_type": self.compiler_type,
            "compilers": [c.to_dict() for c in self.compilers],
            "success": self.success,
            "error": self.error,
            "detection_time": self.detection_time
        }


@dataclass
class ParallelDetectionSummary:
    """Summary of parallel detection operations"""
    total_compilers: int
    successful_detections: int
    failed_detections: int
    total_time: float
    results: Dict[str, ParallelDetectionResult]
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_compilers": self.total_compilers,
            "successful_detections": self.successful_detections,
            "failed_detections": self.failed_detections,
            "total_time": self.total_time,
            "results": {k: v.to_dict() for k, v in self.results.items()},
            "errors": self.errors
        }


class ParallelDetector:
    """Parallel detector for concurrent compiler detection

    This class provides parallel detection of multiple compiler types,
    significantly reducing the time required to detect all available compilers.
    """

    def __init__(self, max_workers: int = 4, logger: Optional[logging.Logger] = None):
        """
        Initialize parallel detector

        Args:
            max_workers: Maximum number of parallel detection workers
            logger: Logger instance for logging detection steps
        """
        self._max_workers = max_workers
        self._logger = logger or logging.getLogger(__name__)
        self._detectors: Dict[str, Callable[[], List[CompilerInfo]]] = {}
        self._results: Dict[str, ParallelDetectionResult] = {}
        self._summary: Optional[ParallelDetectionSummary] = None

    def register_detector(
        self,
        compiler_type: str,
        detector_func: Callable[[], List[CompilerInfo]]
    ) -> None:
        """
        Register a compiler detector function

        Args:
            compiler_type: Type of compiler (e.g., "msvc", "mingw_gcc")
            detector_func: Function that returns list of CompilerInfo
        """
        self._logger.debug(f"Registering detector for {compiler_type}")
        self._detectors[compiler_type] = detector_func

    def detect_all_parallel(
        self,
        compiler_types: Optional[List[str]] = None
    ) -> ParallelDetectionSummary:
        """
        Detect all registered compilers in parallel

        Args:
            compiler_types: List of compiler types to detect (None = all registered)

        Returns:
            Summary of parallel detection results
        """
        self._logger.info("Starting parallel compiler detection")
        start_time = time.time()

        # Determine which compilers to detect
        types_to_detect = compiler_types or list(self._detectors.keys())
        self._logger.info(f"Detecting {len(types_to_detect)} compiler types: {types_to_detect}")

        # Clear previous results
        self._results.clear()

        # Execute detection in parallel
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            # Submit all detection tasks
            future_to_type: Dict[Future, str] = {}
            for compiler_type in types_to_detect:
                if compiler_type in self._detectors:
                    detector_func = self._detectors[compiler_type]
                    future = executor.submit(self._detect_compiler_safe, compiler_type, detector_func)
                    future_to_type[future] = compiler_type
                    self._logger.debug(f"Submitted detection task for {compiler_type}")

            # Collect results as they complete
            for future in as_completed(future_to_type):
                compiler_type = future_to_type[future]
                try:
                    result = future.result()
                    self._results[compiler_type] = result
                    if result.success:
                        self._logger.info(
                            f"Completed detection for {compiler_type}: "
                            f"found {len(result.compilers)} compilers in {result.detection_time:.2f}s"
                        )
                    else:
                        self._logger.error(
                            f"Failed detection for {compiler_type}: {result.error}"
                        )
                except Exception as e:
                    self._logger.error(
                        f"Exception during {compiler_type} detection: {str(e)}"
                    )
                    self._results[compiler_type] = ParallelDetectionResult(
                        compiler_type=compiler_type,
                        compilers=[],
                        success=False,
                        error=str(e),
                        detection_time=0.0
                    )

        total_time = time.time() - start_time

        # Build summary
        total_compilers = sum(len(r.compilers) for r in self._results.values())
        successful_detections = sum(1 for r in self._results.values() if r.success)
        failed_detections = sum(1 for r in self._results.values() if not r.success)
        errors = [r.error for r in self._results.values() if r.error]

        self._summary = ParallelDetectionSummary(
            total_compilers=total_compilers,
            successful_detections=successful_detections,
            failed_detections=failed_detections,
            total_time=total_time,
            results=self._results.copy(),
            errors=errors
        )

        self._logger.info(
            f"Parallel detection complete: "
            f"{total_compilers} compilers found in {total_time:.2f}s "
            f"({successful_detections} successful, {failed_detections} failed)"
        )

        return self._summary

    def detect_compiler_parallel(
        self,
        compiler_type: str
    ) -> ParallelDetectionResult:
        """
        Detect a specific compiler type in parallel

        Args:
            compiler_type: Type of compiler to detect

        Returns:
            Detection result for the specified compiler type
        """
        self._logger.info(f"Starting parallel detection for {compiler_type}")

        if compiler_type not in self._detectors:
            error_msg = f"No detector registered for compiler type: {compiler_type}"
            self._logger.error(error_msg)
            return ParallelDetectionResult(
                compiler_type=compiler_type,
                compilers=[],
                success=False,
                error=error_msg,
                detection_time=0.0
            )

        # Execute detection
        result = self._detect_compiler_safe(
            compiler_type,
            self._detectors[compiler_type]
        )

        self._results[compiler_type] = result

        if result.success:
            self._logger.info(
                f"Completed detection for {compiler_type}: "
                f"found {len(result.compilers)} compilers in {result.detection_time:.2f}s"
            )
        else:
            self._logger.error(f"Failed detection for {compiler_type}: {result.error}")

        return result

    def get_parallel_results(self) -> Dict[str, ParallelDetectionResult]:
        """
        Get all parallel detection results

        Returns:
            Dictionary mapping compiler types to detection results
        """
        return self._results.copy()

    def get_parallel_summary(self) -> Optional[ParallelDetectionSummary]:
        """
        Get summary of parallel detection

        Returns:
            Detection summary or None if no detection has been performed
        """
        return self._summary

    def get_compilers_by_type(
        self,
        compiler_type: str
    ) -> List[CompilerInfo]:
        """
        Get detected compilers for a specific type

        Args:
            compiler_type: Type of compiler

        Returns:
            List of detected compilers or empty list if not found
        """
        result = self._results.get(compiler_type)
        if result and result.success:
            return result.compilers
        return []

    def get_all_compilers(self) -> List[CompilerInfo]:
        """
        Get all detected compilers

        Returns:
            List of all detected compilers
        """
        all_compilers: List[CompilerInfo] = []
        for result in self._results.values():
            if result.success:
                all_compilers.extend(result.compilers)
        return all_compilers

    def clear_results(self) -> None:
        """Clear all detection results"""
        self._logger.debug("Clearing parallel detection results")
        self._results.clear()
        self._summary = None

    def _detect_compiler_safe(
        self,
        compiler_type: str,
        detector_func: Callable[[], List[CompilerInfo]]
    ) -> ParallelDetectionResult:
        """
        Safely execute compiler detection with error handling

        Args:
            compiler_type: Type of compiler being detected
            detector_func: Detection function to execute

        Returns:
            Detection result with error handling
        """
        start_time = time.time()

        try:
            self._logger.debug(f"Executing detection for {compiler_type}")
            compilers = detector_func()
            detection_time = time.time() - start_time

            # Validate compiler info
            valid_compilers = [c for c in compilers if c.is_valid()]

            if len(valid_compilers) < len(compilers):
                self._logger.warning(
                    f"Filtered {len(compilers) - len(valid_compilers)} invalid compilers "
                    f"from {compiler_type} detection"
                )

            return ParallelDetectionResult(
                compiler_type=compiler_type,
                compilers=valid_compilers,
                success=True,
                detection_time=detection_time
            )

        except Exception as e:
            detection_time = time.time() - start_time
            self._logger.error(
                f"Error during {compiler_type} detection: {str(e)}",
                exc_info=True
            )
            return ParallelDetectionResult(
                compiler_type=compiler_type,
                compilers=[],
                success=False,
                error=str(e),
                detection_time=detection_time
            )

    def get_detection_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about parallel detection performance

        Returns:
            Dictionary containing detection statistics
        """
        if not self._summary:
            return {}

        stats = {
            "total_time": self._summary.total_time,
            "total_compilers": self._summary.total_compilers,
            "successful_detections": self._summary.successful_detections,
            "failed_detections": self._summary.failed_detections,
            "average_detection_time": 0.0,
            "fastest_detection": None,
            "slowest_detection": None,
            "compilers_by_type": {}
        }

        # Calculate per-type statistics
        detection_times: List[Tuple[str, float]] = []
        for compiler_type, result in self._results.items():
            if result.success:
                detection_times.append((compiler_type, result.detection_time))
                stats["compilers_by_type"][compiler_type] = {
                    "count": len(result.compilers),
                    "detection_time": result.detection_time
                }

        if detection_times:
            # Calculate average
            avg_time = sum(t[1] for t in detection_times) / len(detection_times)
            stats["average_detection_time"] = avg_time

            # Find fastest and slowest
            detection_times.sort(key=lambda x: x[1])
            stats["fastest_detection"] = {
                "compiler_type": detection_times[0][0],
                "time": detection_times[0][1]
            }
            stats["slowest_detection"] = {
                "compiler_type": detection_times[-1][0],
                "time": detection_times[-1][1]
            }

        return stats
