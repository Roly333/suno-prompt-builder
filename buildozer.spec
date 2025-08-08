[app]
title = Suno Prompt Builder
package.name = sunoprompt
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

requirements = python3,kivy,pyjnius,android,six

orientation = portrait
icon.filename = icon.png

[android]
fullscreen = 0
android.archs = arm64-v8a
android.permissions = WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk_api = 21

[buildozer]
log_level = 2
warn_on_root = 0
