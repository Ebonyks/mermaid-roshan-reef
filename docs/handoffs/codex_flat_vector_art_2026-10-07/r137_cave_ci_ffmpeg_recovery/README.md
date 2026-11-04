# Geologist cave CI dependency recovery

The published cave candidate passed all local gameplay probes and its GitHub gameplay job. The Windows area-music job failed when the existing FFmpeg archive provider returned HTTP 503. Two failed-jobs-only retries kept the original successful gameplay result. The provider error recurred.

The installer now downloads the same publisher's FFmpeg 8.1.2 archive from its GitHub Release. The pinned SHA-256 matches the released archive and was checked before extraction on a fresh local installation. All 44 deterministic music checks passed using that binary. The workflow, verifier and cave runtime are byte-identical to the published cave source. [Proof](DEPENDENCY_PROOF.json), [publisher release](https://github.com/GyanD/codexffmpeg/releases/tag/8.1.2), [prior CI](https://github.com/Ebonyks/mermaid-roshan-reef/actions/runs/41838014853).

The new source head still requires exact GitHub CI before Dev integration. Cave acceptance remains separate. This recovery adds zero artwork, roles, or frame events.
