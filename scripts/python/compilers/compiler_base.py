"""
Base compiler interface
"""

from typing import Any, Dict
from dataclasses import dataclass


@dataclass
class CompilerInfo:
    """Compiler information"""
    name: str
    version: str
    path: str
    target: str
    flags: list[str]


class CompilerBase:
    """Base compiler interface"""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize compiler"""
        self.config = config
    
    def detect(self) -> CompilerInfo | None:
        """Detect compiler"""
        # TODO: Implement compiler detection
        return None
    
    def get_flags(self) -> list[str]:
        """Get compiler flags"""
        # TODO: Implement flag retrieval
        return []
