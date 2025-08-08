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
android.allow_backup = True
# --- THIS IS THE CRUCIAL NEW LINE ---
android.accept_sdk_license = True

p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1