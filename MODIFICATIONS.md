# Modifications to Deoxys Control

This document describes the modifications made to the original [UT-Austin-RPL/deoxys_control](https://github.com/UT-Austin-RPL/deoxys_control) repository.

## Overview

This fork includes improvements to the build system (CMake) and enhancements to both the client-side (Python) and server-side (C++) behavior, focusing on robustness, error handling, and graceful shutdown mechanisms.

## Build System Changes (CMake)

### CMakeLists.txt Modifications

1. **RPATH Configuration**
   - Added RPATH settings for proper runtime library resolution
   - Configured `CMAKE_INSTALL_RPATH` and `CMAKE_BUILD_WITH_INSTALL_RPATH` to ensure libraries are found at runtime
   - Set default RPATH to `/usr/local/lib`

2. **Dependency Discovery Improvements**
   - **spdlog**: Prefer system package, fallback to bundled submodule if available
   - **yaml-cpp**: Prefer system package, fallback to bundled submodule with shared library build enabled
   - **zmqpp**: Use bundled submodule (required)
   - **libfranka**: Option to use bundled version via `USE_BUNDLED_FRANKA` flag (defaults to system package)

3. **Build Configuration**
   - Improved error messages for missing dependencies
   - Better handling of optional vs required dependencies

## Server-Side Changes (C++ - franka-interface)

### franka_control_node.cpp

1. **Graceful Shutdown**
   - Added signal handlers for SIGINT and SIGTERM
   - Implemented atomic flags for shutdown coordination (`g_shutdown_requested`, `g_signal_received`)
   - Proper thread cleanup using RAII pattern (`ThreadCleanup` helper)

2. **Error Handling & Recovery**
   - Service retry loop with exponential backoff (max 30 seconds)
   - Categorized exception handling:
     - Network errors: Retry with backoff
     - Control errors: Graceful controller stop, attempt recovery
     - Command errors: Retry with backoff
     - Version incompatibility: Fatal error
   - Automatic error recovery using `robot.automaticErrorRecovery()`
   - Thread-safe error handling during controller execution

3. **Threading Improvements**
   - RAII-based thread cleanup to ensure threads are properly joined on exceptions
   - Better coordination between control message subscription thread and main control loop
   - Proper state publisher shutdown coordination

4. **Configuration Loading**
   - Improved error handling for YAML configuration files
   - Fatal errors for missing or invalid configuration files
   - Support for optional second control config file argument

### gripper_control_node.cpp

1. **Similar Improvements**
   - Signal handling for graceful shutdown
   - Thread cleanup mechanisms
   - Better error handling and recovery
   - Non-blocking ZMQ receive for responsive shutdown

## Client-Side Changes (Python)

### franka_interface.py

1. **Threading Fixes**
   - Improved thread shutdown mechanism using `_stop_threads` event
   - Non-blocking ZMQ receive with timeout for responsive shutdown
   - Better exception handling in state receiving threads

2. **State Management**
   - Timeout-based ZMQ receive (100ms timeout) to allow periodic shutdown checks
   - Graceful handling of ZMQ.Again exceptions during shutdown

## Benefits

These modifications provide:

- **Better Reliability**: Automatic retry and recovery mechanisms reduce downtime
- **Cleaner Shutdown**: Proper signal handling and thread cleanup prevent resource leaks
- **Improved Build Flexibility**: Better dependency management allows for both system packages and bundled dependencies
- **Enhanced Debugging**: Better error messages and logging help identify issues faster
- **Production Readiness**: More robust error handling suitable for long-running services

## Compatibility

These changes maintain API compatibility with the original repository. Existing Python scripts and configuration files should work without modification.

## Testing Recommendations

When using this fork, test:
1. Graceful shutdown via Ctrl+C
2. Network interruption recovery
3. Robot error recovery
4. Build with both system packages and bundled dependencies

