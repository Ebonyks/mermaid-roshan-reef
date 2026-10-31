# Demo runbook: release candidate, device rehearsal and demo day

Status: `PROPOSED / CANDIDATE` procedure prepared by Claude for Codex and the
owner (written material only; no game change, no images). Entry point:
[README.md](README.md). Evidence baseline: dev `218ae766`.

This runbook turns the demo into a release that follows `DL-SAVE-05`: exact
Godot 4.7.2 import, trusted probes at the exact commit, save-upgrade evidence,
a matching APK hash and a device check. It adds no new approval checkpoint.
The owner's existing release shorthand ("ship it", "push to master") still
authorizes `gh workflow run promote.yml --ref dev`.

Roles: **Codex** builds, merges and runs CI. **The owner or another adult**
handles the device, the backups and the child session. **Claude** reviews on
request.

---

## R0. Protect what cannot be rebuilt (before anything else)

1. **Copy Roshan's save off her device.** Plug the device in with USB
   debugging on and run `./backup.sh` from the repository. It copies
   `reef_save.json`, `reef_save.json.bak` and `reef_save.json.before_new_game`
   with `adb exec-out run-as com.ebonyks.roshanreef cat files/...`
   (`backup.sh:60-70`). This works only while the installed APK is a debug
   build, which the current stable APK is.
2. Check that `reef_save-<stamp>.json` is not empty and opens as JSON. Keep
   one copy on the PC and one somewhere else.
3. Read four values from it and send them to Codex (values only, not the
   file): `day_one_active`, `day_one_completed_rooms`,
   `day_one_giant_dust_bunny_boss_triggered` and `opera_stars`. They decide
   README Q1 (see [AUDIT E2](AUDIT.md#e2-her-save-in-the-new-build--check-before-choosing-continue)).
4. **Never commit her save file.** The repository is public. Desktop
   rehearsal uses a private copy outside the repository.
5. **Keep the current stable APK.** Promotion replaces the `android-test`
   asset, so download today's stable `roshan-reef.apk` and its `.sha256`
   (build of `ff68f955`, 604,039,545 bytes) before promoting. It is the
   rollback build.
6. **Push work that exists on only one disk.** The Grand Puff care branch
   `codex/grand-puff-care-20261017` (`e0abe9c9`) has never been pushed. Push
   it (or the owner confirms it may be discarded) before more work happens in
   that worktree.

## R1. Release candidate (RC)

1. When every package the owner kept in scope has merged into `dev` with a
   green Probe Suite, Codex records the RC: the full 40-character dev SHA, the
   Probe Suite run ID and the `android-dev` APK SHA-256 published for that
   SHA.
2. From the RC on, `dev` takes only fixes for problems found in R2-R4. Every
   such fix restarts R1 with a new RC SHA.
3. The RC is promoted as-is. Do not promote a later head that nobody
   rehearsed.

## R2. Save-upgrade rehearsal on a computer

Run the RC with exact Godot 4.7.2 (`python -B tools/resolve_godot.py`) on a
private copy of her real save, in an isolated user-data folder like
`scripts/ci.sh` uses (fresh `APPDATA` and `LOCALAPPDATA`), never the desktop's
real profile.

Record, without copying her save into the repository:

- where Continue takes her (room, Day One step or Day Two state);
- that every visible milestone she had is still there (Day One step, rescued
  friends, stickers, medals, outfits, stars, companion);
- that the game saves again cleanly (`reef_save.json` and `.bak` both
  rewritten, no key removed: compare the key sets before and after);
- that New Game still needs the press-and-hold and archives her save
  (`start_menu.gd:215-268`).

If her save routes somewhere wrong or loses anything, stop: that is a demo
blocker for Codex, not something to fix on the device.

## R3. Install-over check

Installing over the old app must keep her data. Android refuses an update
signed with a different key or carrying a lower version code. Both are
expected to be fine: the version code is the branch's commit count
(`android.yml:160-168`; 1575 for the August build, 2123 for `218ae766`), and
the August and current builds were signed with the same certificate
([AUDIT E1](AUDIT.md#e1-installing-over-the-old-app-keeps-her-save--ok)).
If the installer still reports a conflict, **do not uninstall**:
uninstalling deletes her save. Stop and report the exact message.

Recommended order:

1. Rehearse on the demo device with the RC's `android-dev` APK using
   `adb install -r` (keeps data). `./pull-apk.sh` only knows the
   `android-test` and `android-graphics` channels, so download the
   `android-dev` asset by hand and compare it with its `.sha256` first.
2. After promotion, install the stable APK the normal way (the phone's
   bookmark or `./pull-apk.sh`) and confirm Continue still lands where R2
   said it would.

## R4. Adult rehearsal on the demo device (about 40 minutes)

Use the device Roshan will hold, at normal brightness with sound on. Write
works / does not work / unsure for each line.

1. Cold start: time from the icon tap to the start menu. Note any black
   screen longer than about 5 seconds.
2. Options (adult): set Music, Quality and Mic the way the owner chose
   (see README owner question Q4). Close Options.
3. Start the way README Q1 decided. Continue: does she land where R2 said?
   New Game: press and hold, then confirm the old save was archived (R0
   already holds a copy).
4. Play the Day One route from where she is to the Day Two card (or to the
   end of the demo scope). The castle reveal, the Grand Puff transformation
   and the epilogue must be pictures, not a black screen. At each room: is there a spoken line and a moving
   pointer for what to do? Note any moment with nothing to do.
5. Interruptions, once each: press Home in the middle of a room, during a
   story clip and during the Grand Puff fight; reopen. Turn the screen off
   and on. Nothing should be lost and nothing should play twice.
6. Back button: press Android Back on the start menu, in a room, during a
   clip and during the fight. Write down what happens. The app must not quit
   to the home screen by itself during play.
7. Fast taps: in the Pool seahorse rescue tap quickly eight times; in any
   drag activity put a second finger down. Nothing should be dropped or
   stolen.
8. Part 2 boundary: walk to every door that is visible after the Day Two
   card. Each one either works to its end and back, or is visibly closed with
   a spoken reason. No door opens onto an empty or adult screen.
9. Sustained play: 20 minutes in total. Note stutter, heat, long loads or
   sound that cuts out.
10. Look for anything a child must not reach: menus with words only, a DEV or
    playtest label, numbers, a permission pop-up.

Any "does not work" in 3-8 or 10 goes back to Codex as a demo blocker with
the device model, the RC SHA and what happened.

## R5. Promote and verify

1. Keep `dev` frozen at the RC. Wait until the RC's Probe Suite run is green
   **and** the `android-dev` release notes name the RC SHA. `promote.yml`
   waits only about 33 minutes for probes (the suite takes 46-62), and a push
   to `dev` during promotion can cancel the APK build
   ([AUDIT E5](AUDIT.md#e5-promotion-timing--follow-the-runbook-order)).
2. The owner gives the release instruction. Codex runs
   `gh workflow run promote.yml --ref dev`, monitors it to completion and
   reports the promoted SHA, both APK URLs and the stable APK SHA-256.
3. Check that the promoted SHA equals the RC SHA.
4. Install on the demo device (R3 step 2) and repeat R4 lines 1, 3 and 5.

## R6. Rollback

If the promoted build fails on the device before or during the demo:

1. Do not uninstall.
2. Reinstall the saved stable APK from R0 step 4 with `adb install -r -d`
   (debug builds allow the downgrade flag).
3. Only if her progress is wrong afterwards, put back the R0 save while the
   game is closed: `adb shell am force-stop com.ebonyks.roshanreef`, then
   `adb exec-in run-as com.ebonyks.roshanreef sh -c 'cat > files/reef_save.json' < reef_save-<stamp>.json`
   (the reverse of the `exec-out` read in `backup.sh`). Rehearse this once on
   a spare install before demo day; do not try it for the first time on her
   device.
4. Report what failed to Codex with the device model and the RC SHA.

## R7. Demo day: watching without helping

This is the first observed session for findings `MA-CHILD-001` and
`MA-PERF-001`. Keep notes in words only. No photos, video or audio of the
child are needed, and nothing about her goes into the repository.

Let her start. Help only if she asks or is upset. For each room or activity,
note:

| Question | Note |
|---|---|
| Did she find the first thing to do without help? | |
| Did she understand what the voice asked? | |
| Did any tap seem ignored? | |
| Did she get stuck or wait with nothing happening? | |
| Did she find the way out and back in? | |
| Did she want to repeat anything? | |
| Where did she stop, and why? | |
| How many times did an adult help, and with what? | |

Afterwards, give the notes to Claude or Codex as plain text. They become the
post-demo backlog, ranked by the same child-first rules.
