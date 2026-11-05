# Godot MCP development integration

Owner-requested satelliteoflove/godot-mcp 4.1.11 is installed alongside the existing Godot AI bridge. This is development tooling, not new gameplay or accepted 3D world code.

## Setup

Use Node.js 20 or newer. From the repository root run `npm ci --prefix tools/godot_mcp --ignore-scripts`. The exact server and transitive dependencies are locked in package-lock.json; the matching MIT-licensed addon, with three explicit type annotations, unchanged-startup save suppression and debugger-inactive callback suppression, is committed under addons/godot_mcp. Open this project with the resolver-selected Godot 4.7.2-stable, then restart the Codex chat/client connection to load the satellite_godot MCP server from .codex/config.toml. The Godot MCP bottom panel reports connection status. The existing Godot AI bridge remains separate.

Run `node tools/godot_mcp/smoke.mjs` with the editor open to verify server version, tool discovery and actual editor state. It only reads state. The server talks to 127.0.0.1:6550; usage logging is disabled. No credentials or additional network permissions are configured. Keep the bind mode on Localhost. Only one client can hold this addon's connection at once.

## Owner decision and scope

On 2026-11-04 the owner answered: "Use the full add-on with a narrowly documented exception for development tools only" after being told that the addon's generic spatial inspection helpers conflict with the strict project 3D inventory. Decision: ODR-GODOT-MCP-DEVTOOLS-20261104. Exact evidence is in tools/godot_mcp/owner_authorization.json.

The exception covers only the exact GDScript files authenticated by tools/godot_mcp/addon_manifest.json and its hardcoded digest in tools/audit_game_2d.py. Any added, missing or changed payload file invalidates the exception and restores normal inventory scanning. Model binaries, new game scenes, materials, shaders, source art and gameplay/world logic retain the full existing audit contract. Generic spatial inspection commands are developer diagnostics only; do not use them to author new 3D game content.

Upstream registers MCPGameBridge as an autoload for editor playtesting. It reaches the game over Godot's debugger transport; it opens no runtime network port and its ready path disables process/physics callbacks and frees the bridge when EngineDebugger is inactive. The source scripts can be packaged with the game's autoload dependencies. This is not a claim of zero shipped debug-code bytes or phone acceptance. Never start a child play session under an agent-controlled debugger. Device/child/owner acceptance and game-wide UNSATISFIED are unchanged.

## Updating or removing

Do not run the upstream installer over the committed addon casually. Updates need a pinned package/lockfile, matching addon payload, license/provenance, renewed exception review and manifest digest, negative controls, editor handshake and project regression gates. For removal, remove the MCP config entry, enabled plugin and MCPGameBridge autoload together with the package/addon and scoped exception.

## Sources

[Upstream installation](https://github.com/satelliteoflove/godot-mcp/blob/345aba8b86cc94daec3577b04df31b0c5f9c2b3b/INSTALL.md), [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli). Package provenance and exact hashes are in the manifest and npm lockfile. No art, voices, saves or release authority are changed.

## Probe compatibility

The Fetch, Skins and Verbs probes now retain the exact main scene they instantiate. Selecting the last root child after a wait could select the newly created autoload instead. Only fixture setup changes; all gameplay actions, assertions, waits and deadlines remain intact. The initial failed full run is retained in evidence/initial_full_ci_failed.txt under tools/godot_mcp; a separate unexplained passive exit127 is not attributed to this selector defect.

## Prior candidate verification

The actual server/editor handshake exposes21tools on official Godot4.7.2; Codex reads the enabled configuration. The combined82 audit tests,95visual contract tests,44music checks,862audio checks, castle/static/import/2D regression phases and clean82/82 native gameplay probes pass. Source was stable through the native full roster. Original/ordered Windows Bash failures are preserved; three unexplained127 exits remain a platform-validation limit despite successful native and Bash component controls. This is a manual per-probe local validation claim; exact published-head CI is required before integration. See tools/godot_mcp/evidence/verification.json.

## Concurrent integration reconciliation

The 2026-11-05 integration at `208a12cf` independently installed the same release for Claude Code. Its `.mcp.json` is retained alongside the locked Codex setup above. Both use the same editor listener; connect one client at a time. Claude uses the pinned npx release; Codex uses the local lockfile installation.

The combined payload retains bridge removal without a debugger, three explicit type annotations and conditional startup save. Both upstream LICENSE and npm LICENSE.txt remain as attribution. The authenticated addon_manifest.json supersedes tools/third_party_tooling_manifest.json as audit authority; the latter preserves the earlier integration's provenance only. The audit reports approved diagnostics on its TOOLING line. Arbitrary addon prefixes and self-edited manifests cannot grant an exemption.

The painted Dolls progress code and assets are preserved byte-for-byte. MCP is now CHG-147 because dev used CHG-146 for Dolls. Old work-head CI was cancelled as superseded. Dev run42007402685 failed because its MCP delta lacked audit-impact coverage; the combined impact supplies exact path coverage. Fresh combined verification is pending; earlier logs retain their original scope.

## Current reconciled local verification

The combined implementation retains Codex and Claude setup, the newer inactive-bridge removal, both MIT attribution files and the exact whole-payload audit anchor. Both clients explicitly use local-only connections with usage logging off. Project settings contain one copy of each MCP section, byte-identical to incoming dev. Start Codex in this repository root: its local stdio launcher uses the chat runtime working directory when cwd is omitted ([official implementation](https://github.com/openai/codex/blob/86ac0916597244a2e67a197822a5483924660ff1/codex-rs/rmcp-client/src/stdio_server_launcher.rs)).

All shared static/asset/import gates pass with exit0 and NO_REGRESSION; all82 cleaned-settings native probes exit0 with unchanged4027-source snapshot and both Dolls PNG hashes. Final syntax/inference, seven scope controls, standalone bridge removal and native Codex configuration checks pass. Full receipts, raw logs, code hashes and the superseded63-invocation run are in tools/godot_mcp/evidence/reconciliation.json and evidence/reconciled/. Exact published-head remote CI remains required before integration; its completion is reported separately. Earlier failed/interrupted attempts retain their original scope. Advanced bridge input/frozen-time, device/child and game-wide acceptance remain open.

The startup patch avoids automatic settings rewrites. Applying new bind settings in the MCP panel still calls Godot's settings save; restore the required Godot-baseline header if that explicit save removes it, before committing.
