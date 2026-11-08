# Reef Grand Prix split-screen controllers and item guides

Scope is the standalone Windows demo on branch `codex/reef-kart-art-20261104` from `a0ca3bc777408f80064ca8d3c8b9e825a6a06af9`. The four courses are Playroom Speedway, Copper Pan Circuit, Seahorse Bridgeway and Footlight Finale.

## Reproduction and repairs

- **Dropped gas.** An A press and release or a complete right-trigger pulse between two simulation polls registered zero throttle at the next step. The reproduction repeated on every course. The PC race now retains a pending nonzero sample per assigned pad and uses it for one step when the held gas level is zero. Pause, disconnect and the normal rearm gate clear or suppress pending gas. Held controls continue to use their current level.
- **Cross-seat item cues.** The shared queue suppressed equal items across seats during the first quarter-second of a cue, and a click on either badge skipped the globally active cue. The queue now retains separate eligible awards, and badge dismissal belongs to the selected seat. The common opening boost still has one centered guide.
- **Stereo and visual ownership.** One voice plays at a time through the existing Voice controls. A temporary race bus positions P1 left and P2 right. The first stereo capture measured peaks above full scale because the panner boosted the near channel. Gain compensation preserves the original near-channel peak, and the owning item badge lights during speech. The far channel remains audible. The game uses the PC audio output with a stereo mix and an on-screen owner signal.

The panner behavior is documented in the [Godot 4.7 AudioEffectPanner reference](https://docs.godotengine.org/en/4.7/classes/class_audioeffectpanner.html).

## Machine and physical evidence

Windows listed only the synthetic Xbox gamepad bus at the initial check. Godot reported zero connected gamepads. Runtime input tests inject events and report the simulation step at which gas is used. This measures the game path after event delivery. USB/Bluetooth transport, a physical button press to visible response, and human listening require the controllers and local players.

The [runtime evidence](../../../audit/cycles/reef-kart-controller-audio-20261107/RUNTIME_EVIDENCE.json) records the four-course reproduction, tests and limitations. The [impact record](../../../design/audit_impacts/reef-kart-controller-audio-20261107.json) binds the scoped repair to the project audit.

### Verified desktop results

- Four full-speed split-screen races finished with injected devices. Both seats visited all four zones on both laps. The focused probe independently exercises separate gas pulses, pause and rejoin behavior, item ownership, and stereo bus cleanup.
- All 36 WASAPI sample checks passed. Each of four item guides was captured for each seat on each track, plus the centered shared opening guide. No isolated cue capture exceeded full scale after the gain correction.
- All 82 trusted gameplay probes passed across the original run, the resumed probe loop and five exact retries after local disk exhaustion. The initial storage failures remain in the evidence.
- The owner identified a different PC for the physical session. USB/Bluetooth transport and button-to-display latency on that computer remain unverified.

## Portable Windows build

The local Windows x64 ZIP contains the official Godot 4.7.2 release executable, a standalone resource pack, asset and engine credits, and a controller-test launcher. The exported game starts in the mode menu with split-screen selected. The full game story entry and save path are outside the export. The resource pack uses the project race, view and controller sources, a catalog-only extract of the existing legacy portrait table, and an exit scene for the standalone menu.

The actual exported executable loaded all four courses with both views and verified twelve portraits, all thirty-six driver/ride previews, the course scenery and the item recordings. The optional Windows controller launcher writes `controller-trace.jsonl` beside the executable. The [reproducible build script](../../../audit/cycles/reef-kart-controller-audio-20261107/build_portable.py) and [runtime evidence](../../../audit/cycles/reef-kart-controller-audio-20261107/RUNTIME_EVIDENCE.json) track the exact output and engine checks.

## Physical follow-up

The opt-in [physical trace script](../../../audit/cycles/reef-kart-controller-audio-20261107/physical_playtest.gd) starts the standard PC menus and logs hardware detection, assigned seat, input received, applied gas, item cue ownership and finish. It injects no events. To start it, pass this argument to the approved Godot executable from the project directory.

```text
-s res://audit/cycles/reef-kart-controller-audio-20261107/physical_playtest.gd
```

Pair the Bluetooth controller and plug in the wired controller. Use the wired pad to enter split-screen and the Bluetooth pad to join P2. On each course, alternate and overlap A and right trigger, hold and release both through bends, let each player collect an item, and finish the race. Listen from the PC stereo output. Repeat the gas and item checks with the devices assigned to the opposite seats if a symptom follows a controller. A high-frame-rate video showing the physical press and the first visible response can separate transport and display delay from the Godot event-to-step time in the trace.
