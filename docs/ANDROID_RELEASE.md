# Android test release safety

The package `com.ebonyks.roshanreef` must always be signed by the same key.
Changing the key prevents an in-place update and can force an uninstall that
removes `user://reef_save.json`.

## One-time repository setup

Generate one debug-channel key and keep an offline backup.  The alias and both
passwords intentionally match Godot's debug-export fields:

```powershell
keytool -genkeypair -keystore roshan-reef-debug.keystore -storepass android `
  -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 `
  -validity 10000 -dname "CN=Mermaid Roshan Debug,O=Mermaid Roshan,C=US"
[Convert]::ToBase64String([IO.File]::ReadAllBytes("roshan-reef-debug.keystore")) |
  gh secret set ANDROID_DEBUG_KEYSTORE_BASE64
```

Never commit the keystore or its Base64 representation.  Store the original in
the owner's normal encrypted backup.  Record its certificate fingerprint with:

```powershell
keytool -list -v -keystore roshan-reef-debug.keystore -storepass android `
  -alias androiddebugkey
```

## Publication contract

The Android workflow is triggered only by a successful `Probe suite (graphics
fork)` run on `master` (or the dedicated graphics test channel).  It checks out
that probe run's exact SHA, restores the persistent keystore, assigns a
monotonic Actions run number as Android `versionCode`, imports without ignored
errors, and publishes both the APK and its SHA-256 file.

If the signing secret is missing, the build intentionally fails instead of
silently rotating the signing identity.

Before accepting a new release path, install build N, create identifiable game
progress, then install build N+1 without uninstalling and verify that every save
field remains intact.
