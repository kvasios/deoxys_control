# Modifications to Deoxys Control

This document describes the modifications made to the original [UT-Austin-RPL/deoxys_control](https://github.com/UT-Austin-RPL/deoxys_control) repository.

## Overview

This fork includes improvements to the build system (CMake) and enhancements to both client-side (Python) and server-side (C++) behavior, focusing on robustness, error handling, and graceful shutdown mechanisms. Additionally, SpaceMouse support has been updated to use USB HID interface for better Linux compatibility.

## Key Changes

### Build System (CMake)
- **RPATH Configuration**: Added proper runtime library resolution settings
- **Dependency Discovery**: Improved handling of spdlog, yaml-cpp, zmqpp, and libfranka with fallback to bundled submodules
- **Better Error Messages**: Enhanced diagnostics for missing dependencies

### Server-Side (C++ - franka-interface)
- **Graceful Shutdown**: Signal handlers (SIGINT/SIGTERM) with proper thread cleanup
- **Error Recovery**: Service retry loop with exponential backoff and automatic robot error recovery
- **Threading**: RAII-based thread management to prevent resource leaks

### Client-Side (Python)
- **Threading Improvements**: Better shutdown coordination and non-blocking ZMQ receive with timeouts
- **SpaceMouse Support**: Switched to USB HID interface (hidapi) for improved Linux compatibility and support for multiple SpaceMouse models

## Benefits

- **Better Reliability**: Automatic retry and recovery mechanisms
- **Cleaner Shutdown**: Proper signal handling prevents resource leaks
- **Improved Build Flexibility**: Better dependency management
- **Enhanced SpaceMouse Support**: USB HID interface works reliably on Linux

## Compatibility

These changes maintain API compatibility with the original repository. Existing Python scripts and configuration files should work without modification.
