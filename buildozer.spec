[app]
title = Suno Prompt Builder
package.name = sunoprompt
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Let the build tool resolve the best dependency versions
requirements = python3,kivy,pyjnius,android,six

orientation = portrait
icon.filename = icon.png

[android]
fullscreen = 0
# Let the build tool choose the best NDK version
# android.ndk = 25b 
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Use the latest stable build toolchain
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
