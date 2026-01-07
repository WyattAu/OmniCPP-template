# DES-016: Package Dependency Schema

## Overview
Defines the package dependency schema for managing and resolving package dependencies across different package managers.

## Schema Definition

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Package Dependency Schema",
  "description": "Package dependency schema for OmniCppController",
  "type": "object",
  "properties": {
    "dependencies": {
      "type": "object",
      "description": "Package dependencies",
      "properties": {
        "runtime": {
          "type": "array",
          "description": "Runtime dependencies",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "description": "Package name"
              },
              "version": {
                "type": "string",
                "description": "Package version constraint"
              },
              "package_manager": {
                "type": "string",
                "enum": ["conan", "vcpkg", "cpm"],
                "description": "Package manager to use"
              },
              "optional": {
                "type": "boolean",
                "default": false,
                "description": "Whether the dependency is optional"
              },
              "features": {
                "type": "array",
                "description": "Package features to enable",
                "items": {
                  "type": "string"
                }
              },
              "options": {
                "type": "object",
                "description": "Package options",
                "additionalProperties": {
                  "type": "string"
                }
              }
            }
          }
        },
        "build": {
          "type": "array",
          "description": "Build-time dependencies",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "description": "Package name"
              },
              "version": {
                "type": "string",
                "description": "Package version constraint"
              },
              "package_manager": {
                "type": "string",
                "enum": ["conan", "vcpkg", "cpm"],
                "description": "Package manager to use"
              },
              "optional": {
                "type": "boolean",
                "default": false,
                "description": "Whether the dependency is optional"
              },
              "features": {
                "type": "array",
                "description": "Package features to enable",
                "items": {
                  "type": "string"
                }
              },
              "options": {
                "type": "object",
                "description": "Package options",
                "additionalProperties": {
                  "type": "string"
                }
              }
            }
          }
        },
        "test": {
          "type": "array",
          "description": "Test dependencies",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "description": "Package name"
              },
              "version": {
                "type": "string",
                "description": "Package version constraint"
              },
              "package_manager": {
                "type": "string",
                "enum": ["conan", "vcpkg", "cpm"],
                "description": "Package manager to use"
              },
              "optional": {
                "type": "boolean",
                "default": false,
                "description": "Whether the dependency is optional"
              }
            }
          }
        },
        "development": {
          "type": "array",
          "description": "Development dependencies",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "description": "Package name"
              },
              "version": {
                "type": "string",
                "description": "Package version constraint"
              },
              "package_manager": {
                "type": "string",
                "enum": ["conan", "vcpkg", "cpm"],
                "description": "Package manager to use"
              },
              "optional": {
                "type": "boolean",
                "default": true,
                "description": "Whether the dependency is optional"
              }
            }
          }
        }
      }
    },
    "resolution": {
      "type": "object",
      "description": "Dependency resolution configuration",
      "properties": {
        "strategy": {
          "type": "string",
          "enum": ["eager", "lazy", "manual"],
          "default": "eager",
          "description": "Dependency resolution strategy"
        },
        "conflict_resolution": {
          "type": "string",
          "enum": ["first", "latest", "error"],
          "default": "first",
          "description": "Conflict resolution strategy"
        },
        "version_constraint": {
          "type": "string",
          "enum": ["exact", "minimum", "compatible", "any"],
          "default": "compatible",
          "description": "Version constraint type"
        },
        "cache_enabled": {
          "type": "boolean",
          "default": true,
          "description": "Enable dependency resolution caching"
        },
        "cache_ttl": {
          "type": "integer",
          "default": 3600,
          "description": "Cache time-to-live in seconds"
        }
      }
    },
    "lockfile": {
      "type": "object",
      "description": "Lockfile configuration",
      "properties": {
        "enabled": {
          "type": "boolean",
          "default": true,
          "description": "Enable lockfile generation"
        },
        "path": {
          "type": "string",
          "default": "dependencies.lock",
          "description": "Lockfile path"
        },
        "update_strategy": {
          "type": "string",
          "enum": ["auto", "manual", "never"],
          "default": "auto",
          "description": "Lockfile update strategy"
        }
      }
    }
  }
}
```

### Python Data Classes

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from enum import Enum
import hashlib
import json

class PackageManagerType(Enum):
    """Package manager types"""
    CONAN = "conan"
    VCPKG = "vcpkg"
    CPM = "cpm"

class DependencyScope(Enum):
    """Dependency scopes"""
    RUNTIME = "runtime"
    BUILD = "build"
    TEST = "test"
    DEVELOPMENT = "development"

class VersionConstraintType(Enum):
    """Version constraint types"""
    EXACT = "exact"
    MINIMUM = "minimum"
    COMPATIBLE = "compatible"
    ANY = "any"

class ConflictResolutionStrategy(Enum):
    """Conflict resolution strategies"""
    FIRST = "first"
    LATEST = "latest"
    ERROR = "error"

class ResolutionStrategy(Enum):
    """Dependency resolution strategies"""
    EAGER = "eager"
    LAZY = "lazy"
    MANUAL = "manual"

@dataclass
class PackageDependency:
    """Package dependency"""
    name: str
    version: Optional[str] = None
    package_manager: PackageManagerType = PackageManagerType.CPM
    optional: bool = False
    features: List[str] = field(default_factory=list)
    options: Dict[str, str] = field(default_factory=dict)
    scope: DependencyScope = DependencyScope.RUNTIME

@dataclass
class DependencyResolutionConfig:
    """Dependency resolution configuration"""
    strategy: ResolutionStrategy = ResolutionStrategy.EAGER
    conflict_resolution: ConflictResolutionStrategy = ConflictResolutionStrategy.FIRST
    version_constraint: VersionConstraintType = VersionConstraintType.COMPATIBLE
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hour

@dataclass
class LockfileConfig:
    """Lockfile configuration"""
    enabled: bool = True
    path: str = "dependencies.lock"
    update_strategy: str = "auto"

@dataclass
class DependencyGraph:
    """Dependency graph"""
    nodes: Dict[str, PackageDependency] = field(default_factory=dict)
    edges: Dict[str, List[str]] = field(default_factory=dict)
    resolved: Set[str] = field(default_factory=set)
    unresolved: Set[str] = field(default_factory=set)
    circular: List[List[str]] = field(default_factory=list)

@dataclass
class LockfileEntry:
    """Lockfile entry"""
    name: str
    version: str
    package_manager: PackageManagerType
    hash: str
    dependencies: List[str]
    features: List[str]
    options: Dict[str, str]

@dataclass
class PackageDependencySchema:
    """Main package dependency schema"""
    runtime: List[PackageDependency] = field(default_factory=list)
    build: List[PackageDependency] = field(default_factory=list)
    test: List[PackageDependency] = field(default_factory=list)
    development: List[PackageDependency] = field(default_factory=list)
    resolution: DependencyResolutionConfig = field(default_factory=DependencyResolutionConfig)
    lockfile: LockfileConfig = field(default_factory=LockfileConfig)

class DependencyResolver:
    """Dependency resolver"""

    def __init__(self, schema: PackageDependencySchema) -> None:
        """Initialize dependency resolver"""
        self._schema = schema
        self._graph = DependencyGraph()
        self._cache: Dict[str, LockfileEntry] = {}

    def resolve(self) -> DependencyGraph:
        """Resolve all dependencies"""
        # Build dependency graph
        self._build_graph()

        # Resolve dependencies based on strategy
        if self._schema.resolution.strategy == ResolutionStrategy.EAGER:
            self._resolve_eager()
        elif self._schema.resolution.strategy == ResolutionStrategy.LAZY:
            self._resolve_lazy()
        else:  # MANUAL
            self._resolve_manual()

        # Check for circular dependencies
        self._detect_circular()

        return self._graph

    def _build_graph(self) -> None:
        """Build dependency graph"""
        all_deps = (
            self._schema.runtime +
            self._schema.build +
            self._schema.test +
            self._schema.development
        )

        for dep in all_deps:
            self._graph.nodes[dep.name] = dep
            self._graph.edges[dep.name] = []

    def _resolve_eager(self) -> None:
        """Resolve dependencies eagerly"""
        visited = set()
        queue = list(self._graph.nodes.keys())

        while queue:
            current = queue.pop(0)

            if current in visited:
                continue

            visited.add(current)
            self._graph.resolved.add(current)

            # Add dependencies to queue
            for dep in self._get_dependencies(current):
                if dep not in visited:
                    queue.append(dep)

        self._graph.unresolved = set(self._graph.nodes.keys()) - visited

    def _resolve_lazy(self) -> None:
        """Resolve dependencies lazily"""
        # Mark all as unresolved initially
        self._graph.unresolved = set(self._graph.nodes.keys())
        self._graph.resolved = set()

    def _resolve_manual(self) -> None:
        """Resolve dependencies manually"""
        # Mark all as unresolved initially
        self._graph.unresolved = set(self._graph.nodes.keys())
        self._graph.resolved = set()

    def _detect_circular(self) -> None:
        """Detect circular dependencies"""
        visited = set()
        rec_stack = set()

        def visit(node: str) -> bool:
            if node in rec_stack:
                # Found circular dependency
                cycle = list(rec_stack)
                cycle.append(node)
                self._graph.circular.append(cycle)
                return True

            if node in visited:
                return False

            visited.add(node)
            rec_stack.add(node)

            for dep in self._graph.edges.get(node, []):
                if visit(dep):
                    return True

            rec_stack.remove(node)
            return False

        for node in self._graph.nodes:
            visit(node)

    def _get_dependencies(self, package_name: str) -> List[str]:
        """Get dependencies for a package"""
        # Check cache first
        if self._schema.resolution.cache_enabled and package_name in self._cache:
            entry = self._cache[package_name]
            return entry.dependencies

        # Get from graph
        return self._graph.edges.get(package_name, [])

    def generate_lockfile(self) -> str:
        """Generate lockfile"""
        if not self._schema.lockfile.enabled:
            return ""

        lockfile_entries = []

        for name, dep in self._graph.nodes.items():
            if name in self._graph.resolved:
                entry = LockfileEntry(
                    name=name,
                    version=dep.version or "latest",
                    package_manager=dep.package_manager,
                    hash=self._compute_hash(name, dep),
                    dependencies=self._graph.edges.get(name, []),
                    features=dep.features,
                    options=dep.options
                )
                lockfile_entries.append(entry)

        # Convert to JSON
        lockfile_data = {
            "version": "1.0",
            "dependencies": [
                {
                    "name": entry.name,
                    "version": entry.version,
                    "package_manager": entry.package_manager.value,
                    "hash": entry.hash,
                    "dependencies": entry.dependencies,
                    "features": entry.features,
                    "options": entry.options
                }
                for entry in lockfile_entries
            ]
        }

        return json.dumps(lockfile_data, indent=2)

    def _compute_hash(self, name: str, dep: PackageDependency) -> str:
        """Compute hash for dependency"""
        hash_input = f"{name}:{dep.version}:{dep.package_manager.value}:{','.join(sorted(dep.features))}:{','.join(sorted(dep.options.keys()))}"
        return hashlib.sha256(hash_input.encode()).hexdigest()

    def load_lockfile(self, lockfile_path: str) -> bool:
        """Load lockfile"""
        try:
            with open(lockfile_path, 'r') as f:
                data = json.load(f)

            for entry in data.get("dependencies", []):
                lock_entry = LockfileEntry(
                    name=entry["name"],
                    version=entry["version"],
                    package_manager=PackageManagerType(entry["package_manager"]),
                    hash=entry["hash"],
                    dependencies=entry.get("dependencies", []),
                    features=entry.get("features", []),
                    options=entry.get("options", {})
                )
                self._cache[lock_entry.name] = lock_entry

            return True
        except (IOError, json.JSONDecodeError):
            return False

    def validate_lockfile(self) -> bool:
        """Validate lockfile"""
        for name, entry in self._cache.items():
            # Check if package still exists in schema
            if name not in self._graph.nodes:
                return False

            # Check hash
            dep = self._graph.nodes[name]
            current_hash = self._compute_hash(name, dep)
            if current_hash != entry.hash:
                return False

        return True
```

## Dependencies

### Internal Dependencies
- `DES-005` - Exception hierarchy
- `DES-012` - Package manager interface

### External Dependencies
- `json` - JSON parsing
- `hashlib` - Hash computation
- `typing` - Type hints
- `dataclasses` - Data structures
- `enum` - Enumerations

## Related Requirements
- REQ-019: Priority-Based Package Manager Selection
- REQ-020: Package Security Verification
- REQ-021: Dependency Resolution & Caching

## Related ADRs
- ADR-001: Python Build System Architecture

## Implementation Notes

### Dependency Resolution
1. Build dependency graph
2. Detect circular dependencies
3. Resolve based on strategy
4. Handle version constraints
5. Resolve conflicts

### Lockfile Management
1. Generate lockfile from resolved dependencies
2. Compute hashes for integrity
3. Load and validate lockfile
4. Update lockfile on changes

### Caching Strategy
1. Cache resolved dependencies
2. Use TTL for cache expiration
3. Invalidate cache on changes
4. Share cache across builds

### Error Handling
- Handle circular dependencies
- Handle version conflicts
- Handle missing dependencies
- Provide clear error messages

## Usage Example

```python
from omni_scripts.dependencies import (
    PackageDependencySchema,
    PackageDependency,
    DependencyResolver,
    PackageManagerType,
    DependencyScope
)

# Create dependency schema
schema = PackageDependencySchema(
    runtime=[
        PackageDependency(
            name="fmt",
            version="^10.0.0",
            package_manager=PackageManagerType.CPM,
            optional=False
        ),
        PackageDependency(
            name="spdlog",
            version="^1.12.0",
            package_manager=PackageManagerType.CPM,
            optional=False
        )
    ],
    build=[
        PackageDependency(
            name="gtest",
            version="^1.14.0",
            package_manager=PackageManagerType.CPM,
            optional=True
        )
    ]
)

# Create resolver
resolver = DependencyResolver(schema)

# Resolve dependencies
graph = resolver.resolve()

# Generate lockfile
lockfile = resolver.generate_lockfile()
print(lockfile)
```
