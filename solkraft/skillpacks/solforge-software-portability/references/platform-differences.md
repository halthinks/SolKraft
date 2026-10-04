<!-- solkraft-doc-sync: contract-aware-v1 | validation-100k-100-family | 2026-10 -->

# Platform differences

## Windows, macOS, and Linux

Audit path syntax, case sensitivity, executable lookup, signals, service managers, process groups, permissions, symlinks, sockets, package locations, GUI toolkits, signing, updates, and native libraries.

## Android and iOS

Audit touch interaction, application lifecycle, background limits, sandboxed storage, permissions, secrets, networking policy, deep links, notifications, power use, native bridges, store packaging, signing, and device testing. A desktop GUI normally requires a platform shell or redesign.

## Browser and WebAssembly

Audit filesystem and process assumptions, native libraries, threads, sockets, secrets, CORS, browser security, persistent storage, offline behavior, accessibility, and bundle size. Native system access often requires redesign or a service boundary.

## CPU architectures

Audit native dependencies, endianness, word size, SIMD, assembly, FFI layouts, toolchains, emulation, and release artifacts. Cross-build success does not prove target execution.
