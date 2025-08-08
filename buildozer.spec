[app]
title = Suno Prompt Builder
package.name = sunoprompt
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Use flexible versions for maximum compatibility with the build server
requirements = python3,kivy,pyjnius,android,six

orientation = portrait
icon.filename = icon.png

[android]
fullscreen = 0
# Build for the modern 64-bit architecture
android.archs = arm64-v8a
android.allow_backup = True

# Use the latest stable build toolchain
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1