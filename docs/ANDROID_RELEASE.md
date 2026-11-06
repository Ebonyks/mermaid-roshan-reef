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

A successful push of the exact commit through `Probe suite (graphics fork)`
permits Android packaging for `master` or `dev`. The automatic workflow checks
out that probe run's SHA, restores the persistent signing identity, assigns
`git rev-list --count HEAD` as the monotonic Android `versionCode`, imports
without ignored errors, and publishes the APK plus its SHA-256 file. The `dev`
channel is `android-dev`; the promoted release channel is `android-test`.

The pinned Godot archive is checksum-verified on cache hits and downloads.
Only `android_debug.apk` and `android_release.apk` are unpacked for the current
prebuilt, non-Gradle Android export. This saves 1,840,184,530 bytes versus the
complete 4.7.2 template bundle, leaving room for the APK signing copy. The cache,
engine/version pins and persistent signing setup stay in place.

If the signing secret is missing, the build intentionally fails instead of
silently rotating the signing identity.

Before accepting a new release path, install build N, create identifiable game
progress, then install build N+1 without uninstalling and verify that every save
field remains intact. Packaging and checksum verification do not establish this
physical-device acceptance.

## Development retry

GitHub loads an automatic `workflow_run` workflow from the default branch;
changing the workflow on `dev` alone does not change that automatic definition.
See [GitHub's workflow event reference](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_run).
The existing Android workflow also supports a manually requested development
retry using the workflow version on `dev`:

```text
gh workflow run android.yml --ref dev
```

Use this after the current `dev` commit has a successful push-probe run.
`tools/verify_android_build_source.py` requires that exact current SHA, the
canonical repository, the named probe workflow, completed success, and the
`dev` push event. It checks again immediately before publication. A changed
Dev head, unavailable API, missing credential, unrelated or incomplete result
stops the manual build. Manual packaging is restricted to `refs/heads/dev` and
publishes to `android-dev`. Existing master promotion/release authority and
signing identity remain unchanged. [GitHub CLI reference](https://cli.github.com/manual/gh_workflow_run).
