# Technical Design Documents

This directory contains the technical design documents for the OmniCPP-template project refactoring. Each design document defines interfaces, classes, structs, and schemas with Python and C++ code examples, JSON schemas, dependencies, related requirements, and ADRs.

## Design Documents

### Python Build System Design (DES-001 to DES-006)

| ID | Document | Description |
|----|----------|-------------|
| [DES-001](DES-001-omnicpp-controller-interface.md) | OmniCpp Controller Interface | Defines the main OmniCppController interface and implementation with command execution, build, clean, configure, install, test, lint, format, package, and config operations |
| [DES-002](DES-002-controller-base-class.md) | Controller Base Class | Defines the IController base interface and BaseController implementation with derived controllers for build, clean, configure, install, test, lint, format, package, and config operations |
| [DES-003](DES-003-configuration-schema.md) | Configuration Schema | Defines the complete JSON schema for project configuration with Python dataclasses for type-safe configuration handling |
| [DES-004](DES-004-logging-configuration-schema.md) | Logging Configuration Schema | Defines the JSON schema for logging configuration with formatters, handlers, and loggers supporting file rotation, async logging, and multiple output sinks |
| [DES-005](DES-005-exception-hierarchy.md) | Exception Hierarchy Design | Defines the OmniCppException base class with message, details, and traceback, organized by domain (configuration, platform, compiler, build system, package manager, terminal, controller, testing, formatting, linting, security, IO, network) |
| [DES-006](DES-006-command-line-argument-schema.md) | Command-Line Argument Schema | Defines the ArgumentParserBuilder class for building argparse configuration with command definitions for build, clean, configure, install, test, lint, format, package, and config |

### Cross-Platform Compilation Design (DES-007 to DES-011)

| ID | Document | Description |
|----|----------|-------------|
| [DES-007](DES-007-platform-detection-interface.md) | Platform Detection Interface | Defines the IPlatformDetector interface and PlatformDetector implementation with OSType, Architecture, and CompilerABI enums for cross-platform detection |
| [DES-008](DES-008-compiler-detection-interface.md) | Compiler Detection Interface | Defines the ICompilerDetector interface and CompilerDetector implementation with CompilerType, CompilerStatus enums and compiler-specific implementations for GCC, Clang, MSVC, and MinGW |
| [DES-009](DES-009-terminal-invocation-interface.md) | Terminal Invocation Interface | Defines the ITerminalInvoker interface and TerminalInvoker implementation with TerminalType enum for secure command execution across different terminal types |
| [DES-010](DES-010-compiler-configuration-schema.md) | Compiler Configuration Schema | Defines the JSON schema for compiler configuration with Python dataclasses for BaseCompilerConfig, GCCCompilerConfig, ClangCompilerConfig, MSVCCompilerConfig, MinGWCompilerConfig, and ToolchainConfig |
| [DES-011](DES-011-toolchain-configuration-schema.md) | Toolchain Configuration Schema | Defines the JSON schema for toolchain configuration with Python dataclasses for CompilerConfig, LinkerConfig, ArchiverConfig, BuildSystemConfig, DebuggerConfig, ProfilerConfig, TargetConfig, ToolchainFlags, ToolchainConfig, QEMUConfig, CrossCompilationConfig, and ToolchainConfiguration |

### Package Manager Design (DES-012 to DES-016)

| ID | Document | Description |
|----|----------|-------------|
| [DES-012](DES-012-package-manager-interface.md) | Package Manager Interface | Defines the IPackageManager interface and BasePackageManager implementation with PackageManagerFactory for creating package managers and PackageManagerSelector for priority-based selection |
| [DES-013](DES-013-conan-integration.md) | Conan Integration Design | Defines the IConanManager interface and ConanManager implementation with ConanProfileGenerator for generating profiles and ConanProfile, ConanPackage, ConanConfig dataclasses |
| [DES-014](DES-014-vcpkg-integration.md) | vcpkg Integration Design | Defines the IVcpkgManager interface and VcpkgManager implementation with VcpkgTripletGenerator for generating triplets and VcpkgPackage, VcpkgConfig dataclasses |
| [DES-015](DES-015-cpm-integration.md) | CPM Integration Design | Defines the ICPMManager interface and CPMManager implementation with CPMPackageGenerator for generating packages and CPMPackage, CPMConfig dataclasses |
| [DES-016](DES-016-package-dependency-schema.md) | Package Dependency Schema | Defines the JSON schema for package dependencies with DependencyResolver class and PackageDependency, DependencyResolutionConfig, LockfileConfig, DependencyGraph, LockfileEntry, and PackageDependencySchema dataclasses |

### Build System Design (DES-017 to DES-020)

| ID | Document | Description |
|----|----------|-------------|
| [DES-017](DES-017-cmake-configuration-schema.md) | CMake Configuration Schema | Defines the JSON schema for CMake configuration with CMakeConfigManager class and CMakeConfig, CMakeWarnings, CMakeErrors, CMakeDebug, CMakeConfigurePreset, CMakeBuildPreset, CMakeTestOutput, CMakeTestExecution, CMakePackageOutput, CMakePackagePreset, CMakeWorkflowStep, CMakeWorkflowPreset, and CMakePresets dataclasses |
| [DES-018](DES-018-cmake-presets-schema.md) | CMake Presets Schema | Defines the JSON schema for CMake Presets v3 with dataclasses for build, configure, test, package, and workflow presets |
| [DES-019](DES-019-build-configuration-schema.md) | Build Configuration Schema | Defines the JSON schema for build configuration with TargetConfig, BuildConfiguration, LTOConfig, IPOConfig, PGOConfig, ParallelConfig, CacheConfig, IncrementalConfig, and BuildConfigurationSchema dataclasses supporting multiple build targets and configurations |
| [DES-020](DES-020-toolchain-file-design.md) | Toolchain File Design | Defines the C++ header for toolchain file interfaces with ToolchainConfig, PlatformConfig, CompilerConfig, LinkerConfig, ArchiverConfig, and BuildSystemConfig structs and ToolchainFile interface with DefaultToolchainFile implementation |

### C++ Engine Design (DES-021 to DES-028)

| ID | Document | Description |
|----|----------|-------------|
| [DES-021](DES-021-engine-core-interfaces.md) | Engine Core Interfaces | Defines the C++ header for engine core interfaces with EngineConfig, EngineState, EngineStats structs and IEngine, IEngineFactory, IEngineBuilder, IEngineEventManager, IEngineContext, IEngineModule, IEngineModuleManager, IEngineProfiler, IEngineMemoryManager, and IEngineTaskScheduler interfaces |
| [DES-022](DES-022-ecs-component-design.md) | ECS Component Design | Defines the C++ header for ECS component interfaces with IComponent base class, ComponentTraits, component manager and pool interfaces, and specific components: TransformComponent, MeshComponent, CameraComponent, LightComponent, RigidBodyComponent, ColliderComponent, AudioSourceComponent, ScriptComponent, and TagComponent |
| [DES-023](DES-023-ecs-system-design.md) | ECS System Design | Defines the C++ header for ECS system interfaces with ISystem base class, SystemTraits, system manager interface, specific systems: TransformSystem, RenderSystem, PhysicsSystem, AudioSystem, ScriptSystem, and SystemQuery, ISystemExecutor, ISystemScheduler, and ISystemProfiler interfaces |
| [DES-024](DES-024-renderer-interface.md) | Renderer Interface | Defines the C++ header for renderer interfaces with RendererConfig, RenderTarget, Viewport, ScissorRect, RendererStats structs, ClearFlag, PrimitiveType, BlendMode, CullMode, CompareFunction, StencilOperation enums, and IRenderer, IShader, ITexture, IMesh, IMaterial, ICamera, ILight, and IRendererFactory interfaces |
| [DES-025](DES-025-audio-manager-interface.md) | Audio Manager Interface | Defines the C++ header for audio manager interfaces with AudioConfig, AudioStats structs, AudioFormat, AudioState, AudioLoopMode enums, and IAudioManager, IAudioSource, IAudioListener, IAudioBuffer, and IAudioManagerFactory interfaces |
| [DES-026](DES-026-physics-engine-interface.md) | Physics Engine Interface | Defines the C++ header for physics engine interfaces with PhysicsConfig, CollisionFilter, PhysicsStats, CollisionContact, CollisionEvent structs, BodyType, CollisionShapeType, JointType enums, and IPhysicsEngine, IRigidBody, ICollider, IPhysicsMaterial, IJoint, and IPhysicsEngineFactory interfaces |
| [DES-027](DES-027-resource-manager-interface.md) | Resource Manager Interface | Defines the C++ header for resource manager interfaces with ResourceConfig, ResourceStats, ResourceMetadata structs, ResourceType, ResourceState, LoadingMode enums, and IResourceManager, IResource, IResourceLoader, IResourceCache, and IResourceManagerFactory interfaces with specific resource types: TextureResource, MeshResource, ShaderResource, AudioResource, FontResource, ScriptResource, and DataResource |
| [DES-028](DES-028-scene-manager-interface.md) | Scene Manager Interface | Defines the C++ header for scene manager interfaces with SceneConfig, SceneStats structs, SceneState, SceneTransitionType enums, and ISceneManager, IScene, ISceneNode, IEntity, and ISceneManagerFactory interfaces |

### C++ Game Design (DES-029 to DES-032)

| ID | Document | Description |
|----|----------|-------------|
| [DES-029](DES-029-game-core-interfaces.md) | Game Core Interfaces | Defines the C++ header for game core interfaces with GameConfig, GameStats structs, GameState, GameModeType enums, and IGame, IGameState, IGameMode, IGameSession, IGameFactory, IGameStateManager, IGameEventManager, and IGameProfiler interfaces |
| [DES-030](DES-030-game-scene-design.md) | Game Scene Design | Defines the C++ header for game scene interfaces with GameSceneConfig, GameSceneStats structs, GameSceneState, GameSceneType enums, and IGameScene, IGameObject, IGameCamera, IGameLight, and IGameSceneFactory interfaces |
| [DES-031](DES-031-game-entity-design.md) | Game Entity Design | Defines the C++ header for game entity interfaces with EntityConfig, EntityStats structs, EntityState enum, and IGameEntity, IEntityManager, IEntityFactory, IEntityPool, IEntityQueryExecutor, and IEntityEventManager interfaces |
| [DES-032](DES-032-game-component-design.md) | Game Component Design | Defines the C++ header for game component interfaces with ComponentConfig, ComponentStats structs, ComponentState enum, and IGameComponent, IComponentManager, IComponentFactory interfaces with specific components: TransformComponent, MeshComponent, AudioComponent, and ScriptComponent |

### Logging Design (DES-033 to DES-036)

| ID | Document | Description |
|----|----------|-------------|
| [DES-033](DES-033-cpp-logging-interface.md) | C++ Logging Interface | Defines the C++ header for C++ logging interface wrapping spdlog with LogMessage, LogSinkConfig, LoggerConfig, LogStatistics structs, LogLevel, LogPattern, LogSinkType enums, and ILogger, ILoggerFactory, ILoggerManager, ILogListenerManager, and ILogStatisticsCollector interfaces with default implementations |
| [DES-034](DES-034-python-logging-interface.md) | Python Logging Interface | Defines the Python code for Python logging interface with LogLevel, LogFormat, LogHandlerType enums, LogMessage, LogHandlerConfig, LoggerConfig dataclasses, and ILogger, ILoggerManager, ILoggerFactory interfaces with default implementations |
| [DES-035](DES-035-log-message-schema.md) | Log Message Schema | Defines the JSON schema for log messages with Python dataclasses and C++ structs for LogMessage with serialization methods supporting level, message, logger_name, timestamp, file, line, function, thread_id, process_id, and extra fields |
| [DES-036](DES-036-log-file-rotation-schema.md) | Log File Rotation Schema | Defines the JSON schema for log file rotation with Python dataclasses and C++ structs for LogRotationConfig with rotation handler, RotationType, RotationWhen, CompressionLevel enums, and LogRotationHandler classes supporting size-based and time-based rotation, compression, and backup management |

### Testing Design (DES-037 to DES-039)

| ID | Document | Description |
|----|----------|-------------|
| [DES-037](DES-037-test-fixture-design.md) | Test Fixture Design | Defines the test fixture design for testing the build system and C++ engine with ITestFixture interface, BaseTestFixture implementation, domain-specific fixtures (BuildSystemFixture, CompilerFixture, PackageManagerFixture, EngineFixture), and TestFixtureManager for fixture management |
| [DES-038](DES-038-test-configuration-schema.md) | Test Configuration Schema | Defines the JSON schema for test configuration with Python dataclasses for TestSuiteConfig, FixtureConfig, OutputConfig, CoverageConfig, ReportingConfig, EnvironmentConfig, LoggingConfig, ParallelConfig, TimeoutConfig, RetryConfig, FilterConfig, and TestConfiguration supporting test suites, fixtures, output, coverage, reporting, environment, logging, parallel execution, timeout, retry, and filter configuration |
| [DES-039](DES-039-coverage-report-schema.md) | Coverage Report Schema | Defines the JSON schema for coverage report with Python dataclasses and C++ structs for LineCoverage, BranchCoverage, FunctionCoverage, FileCoverage, DirectoryCoverage, ModuleCoverage, UncoveredLine, UncoveredBranch, UncoveredFunction, CoverageSummary, CoverageThresholds, CoverageMetadata, and CoverageReport supporting line, branch, and function coverage metrics, threshold checking, and coverage analysis |

### Linux Support Design (DES-040 to DES-045)

| ID | Document | Description |
|----|----------|-------------|
| [DES-040](DES-040-omnicppcontroller-linux-extensions.md) | OmniCppController.py Extensions | Defines the extensions to OmniCppController.py for comprehensive Linux support, including platform detection, CachyOS detection, Nix environment detection, package manager detection, compiler flags, and build command generation interfaces |
| [DES-041](DES-041-flake-nix-schema.md) | flake.nix Schema | Defines the schema and structure for Nix flake configuration file, including package definitions, shell environment configuration, CMake integration, and Conan integration |
| [DES-042](DES-042-vscode-configuration-schema.md) | VSCode Configuration Schema | Defines the schema and structure for VSCode configuration files ([`tasks.json`](../../.vscode/tasks.json:1) and [`launch.json`](../../.vscode/launch.json:1)) with comprehensive Linux support, including platform-specific variants, Nix environment integration, and CachyOS optimizations |
| [DES-043](DES-043-conan-profile-schema.md) | Conan Profile Schema | Defines the schema and structure for Conan profile files, including Linux, CachyOS, GCC, and Clang profiles with support for Nix environments and CachyOS-specific optimizations |
| [DES-044](DES-044-setup-script-architecture.md) | Setup Script Architecture | Defines the architecture and interfaces for setup scripts that handle Linux environment configuration, Nix environment activation, CachyOS optimization setup, and development environment validation |
| [DES-045](DES-045-cmake-preset-schema.md) | CMake Preset Schema | Defines the schema and structure for CMake preset files, including Nix-aware presets, CachyOS presets, and platform detection enhancement schemas |

## Design Document Structure

Each design document follows a consistent structure:

1. **Overview** - Brief description of the design document
2. **JSON Schema** - Complete JSON schema definition (if applicable)
3. **Python Code** - Python code with type hints, dataclasses, and interfaces
4. **C++ Code** - C++ code with type definitions, structs, and interfaces (if applicable)
5. **Dependencies** - Internal and external dependencies
6. **Related Requirements** - Links to related requirements
7. **Related ADRs** - Links to related Architecture Decision Records
8. **Implementation Notes** - Key implementation details and considerations
9. **Usage Example** - Example code demonstrating usage

## Design Principles

The technical design documents follow these principles:

- **Type Safety** - All Python code uses type hints for compile-time type checking
- **Cross-Platform** - All designs support Windows, Linux, and macOS
- **Modularity** - Components are designed to be modular and reusable
- **Extensibility** - Interfaces allow for easy extension and customization
- **Documentation** - All interfaces and classes are well-documented
- **Testing** - All designs include testing considerations
- **Performance** - Performance considerations are included where applicable

## Related Documentation

- [Requirements](../reqs/) - Requirements documents
- [Architecture Decision Records](../adrs/) - ADR documents
- [Current State](../01_current_state/) - Current state analysis
- [Future State](../04_future_state/) - Future state vision
- [Threat Model](../03_threat_model/) - Threat model analysis

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2026-01-07 | Initial design documents created |
| 1.1.0 | 2026-01-27 | Added Linux support design documents (DES-040 to DES-045) |

## Contributors

- Kilo Code - Senior Backend Engineer

## License

See project LICENSE file for details.
