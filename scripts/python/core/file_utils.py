"""
File Utils - Cross-platform file operations, path manipulation, directory management

This module provides cross-platform file operations, path manipulation,
directory management, and file utilities for OmniCPP build system.
"""

import os
import shutil
import hashlib
import tempfile
from pathlib import Path
from typing import Optional, List

from core.exception_handler import PermissionError as OmniPermissionError


def ensure_directory(path: str) -> None:
    """Ensure directory exists, create if needed.
    
    Args:
        path: Directory path
        
    Raises:
        OmniPermissionError: If directory creation fails
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OmniPermissionError(
            f"Failed to create directory: {path}",
            {"path": path, "error": str(e)}
        )


def copy_file(src: str, dst: str) -> None:
    """Copy file from source to destination.
    
    Args:
        src: Source file path
        dst: Destination file path
        
    Raises:
        OmniPermissionError: If copy fails
    """
    try:
        shutil.copy2(src, dst)
    except OSError as e:
        raise OmniPermissionError(
            f"Failed to copy file from {src} to {dst}",
            {"src": src, "dst": dst, "error": str(e)}
        )


def copy_directory(src: str, dst: str) -> None:
    """Copy directory recursively.
    
    Args:
        src: Source directory path
        dst: Destination directory path
        
    Raises:
        OmniPermissionError: If copy fails
    """
    try:
        shutil.copytree(src, dst, dirs_exist_ok=True)
    except OSError as e:
        raise OmniPermissionError(
            f"Failed to copy directory from {src} to {dst}",
            {"src": src, "dst": dst, "error": str(e)}
        )


def delete_file(path: str) -> None:
    """Delete file.
    
    Args:
        path: File path to delete
        
    Raises:
        OmniPermissionError: If deletion fails
    """
    try:
        os.remove(path)
    except OSError as e:
        raise OmniPermissionError(
            f"Failed to delete file: {path}",
            {"path": path, "error": str(e)}
        )


def delete_directory(path: str) -> None:
    """Delete directory recursively.
    
    Args:
        path: Directory path to delete
        
    Raises:
        OmniPermissionError: If deletion fails
    """
    try:
        shutil.rmtree(path)
    except OSError as e:
        raise OmniPermissionError(
            f"Failed to delete directory: {path}",
            {"path": path, "error": str(e)}
        )


def hash_file(path: str, algorithm: str = "sha256") -> str:
    """Calculate file hash.
    
    Args:
        path: File path
        algorithm: Hash algorithm (default: sha256)
            
    Returns:
        File hash as hexadecimal string
    """
    hash_obj = hashlib.new(algorithm)
    
    try:
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                hash_obj.update(chunk)
    except OSError as e:
        raise OmniPermissionError(
            f"Failed to read file for hashing: {path}",
            {"path": path, "error": str(e)}
        )
    
    return hash_obj.hexdigest()


def create_temp_directory(prefix: str = "omnicpp_") -> str:
    """Create temporary directory.
    
    Args:
        prefix: Directory name prefix
            
    Returns:
        Path to temporary directory
    """
    return tempfile.mkdtemp(prefix=prefix)


def create_temp_file(suffix: str = ".tmp", prefix: str = "omnicpp_") -> str:
    """Create temporary file.
    
    Args:
        suffix: File suffix
        prefix: File name prefix
            
    Returns:
        Path to temporary file
    """
    fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
    os.close(fd)
    return path


def file_exists(path: str) -> bool:
    """Check if file exists.
    
    Args:
        path: File path to check
            
    Returns:
        True if file exists, False otherwise
    """
    return os.path.isfile(path)


def directory_exists(path: str) -> bool:
    """Check if directory exists.
    
    Args:
        path: Directory path to check
            
    Returns:
        True if directory exists, False otherwise
    """
    return os.path.isdir(path)


def get_file_size(path: str) -> int:
    """Get file size in bytes.
    
    Args:
        path: File path
            
    Returns:
        File size in bytes
    """
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


def list_files(directory: str, pattern: str = "*") -> List[str]:
    """List files in directory matching pattern.
    
    Args:
        directory: Directory path
        pattern: File pattern (default: *)
            
    Returns:
        List of file paths
    """
    try:
        return [
            str(p) for p in Path(directory).glob(pattern)
            if p.is_file()
        ]
    except OSError:
        return []


def list_directories(directory: str) -> List[str]:
    """List subdirectories.
    
    Args:
        directory: Directory path
            
    Returns:
        List of directory paths
    """
    try:
        return [
            str(p) for p in Path(directory).iterdir()
            if p.is_dir()
        ]
    except OSError:
        return []


def normalize_path(path: str) -> str:
    """Normalize path for current platform.
    
    Args:
        path: Path to normalize
            
    Returns:
        Normalized path
    """
    return str(Path(path).resolve())


def join_paths(*paths: str) -> str:
    """Join path components.
    
    Args:
        *paths: Path components to join
            
    Returns:
        Joined path
    """
    return str(Path(*paths))


def get_relative_path(path: str, start: str) -> str:
    """Get relative path from start to path.
    
    Args:
        path: Target path
        start: Start path
            
    Returns:
        Relative path
    """
    try:
        return str(Path(path).relative_to(Path(start)))
    except ValueError:
        return path


def get_absolute_path(path: str) -> str:
    """Get absolute path.
    
    Args:
        path: Path to convert
            
    Returns:
        Absolute path
    """
    return str(Path(path).resolve())


def read_text_file(path: str, encoding: str = "utf-8") -> str:
    """Read text file.
    
    Args:
        path: File path
        encoding: File encoding (default: utf-8)
            
    Returns:
        File content as string
            
    Raises:
        OmniPermissionError: If read fails
    """
    try:
        with open(path, "r", encoding=encoding) as f:
            return f.read()
    except OSError as e:
        raise OmniPermissionError(
            f"Failed to read file: {path}",
            {"path": path, "error": str(e)}
        )


def write_text_file(path: str, content: str, encoding: str = "utf-8") -> None:
    """Write text file.
    
    Args:
        path: File path
        content: Content to write
        encoding: File encoding (default: utf-8)
            
    Raises:
        OmniPermissionError: If write fails
    """
    try:
        # Ensure directory exists
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        
        with open(path, "w", encoding=encoding) as f:
            f.write(content)
    except OSError as e:
        raise OmniPermissionError(
            f"Failed to write file: {path}",
            {"path": path, "error": str(e)}
        )


def get_file_extension(path: str) -> str:
    """Get file extension.
    
    Args:
        path: File path
            
    Returns:
        File extension (including dot)
    """
    return Path(path).suffix


def change_extension(path: str, new_extension: str) -> str:
    """Change file extension.
    
    Args:
        path: File path
        new_extension: New extension (with or without dot)
            
    Returns:
        Path with new extension
    """
    return str(Path(path).with_suffix(new_extension))


def is_executable(path: str) -> bool:
    """Check if file is executable.
    
    Args:
        path: File path
            
    Returns:
        True if executable, False otherwise
    """
    return os.access(path, os.X_OK)


def make_executable(path: str) -> None:
    """Make file executable.
    
    Args:
        path: File path
            
    Raises:
        OmniPermissionError: If operation fails
    """
    try:
        os.chmod(path, 0o755)
    except OSError as e:
        raise OmniPermissionError(
            f"Failed to make file executable: {path}",
            {"path": path, "error": str(e)}
        )
