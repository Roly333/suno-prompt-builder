[app]
title = Suno Prompt Builder
package.name = sunoprompt
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# --- MODIFICATION: Using stable, explicit versions for dependencies ---
requirements = python3==3.11.5,kivy==2.2.1,pyjnius==1.6.1,android,six,pillow

orientation = portrait
icon.filename = icon.png

[android]
fullscreen = 0
android.archs = arm64-v8a
android.permissions = WRITE_EXTERNAL_STORAGE
android.allow_backup = True

# --- MODIFICATION: Setting explicit, stable API and NDK versions ---
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.ndk = 25b

[buildozer]
log_level = 2
# This setting is required by the build action
warn_on_root = 0
