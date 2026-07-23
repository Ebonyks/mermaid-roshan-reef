# Dirty Castle Cleaning — 36-Frame Cinematic Narrative

## Story purpose

Roshan returns to the Pearl Castle with Daddy Mermaid and Baby Eagle. The
castle is gently untidy, never ruined or frightening. They discover that the
lavender dust curls are a family of friendly dust bunnies, choose jobs, and
clean the castle together room by room.

The story models cooperation without taking the child's agency away. Each room
uses a clear visual rhythm:

1. discover the room and its large object groups;
2. assign one readable job to Roshan, Daddy, and Baby Eagle;
3. show an action with immediate progress;
4. show an unmistakably clean room and move forward.

Dust bunnies become helpers and neighbors. They are housed comfortably at the
end rather than defeated or discarded.

## Complete frame sequence

| # | Runtime frame | Narrative beat | Trio action / visual purpose |
| ---: | --- | --- | --- |
| 01 | `01_arrival_dirty.png` | Homecoming surprise | The trio sees the gentle Hall mess together. |
| 02 | `02_dust_bunnies_reveal.png` | The mess is alive and cute | Roshan discovers friendly lavender dust bunnies. |
| 03 | `03_choose_tools.png` | Everyone chooses a role | Roshan takes the sponge, Daddy the mop, Eagle the brush. |
| 04 | `04_dust_bunny_roundup.png` | Care instead of disposal | The trio guides bunnies toward a shell-and-cloud home. |
| 05 | `05_roshan_window.png` | Roshan's first hero beat | Roshan wipes the rainbow window while Daddy and Eagle support. |
| 06 | `06_daddy_floor.png` | Daddy models cleaning as play | Daddy mops footprints and the floor scuff. |
| 07 | `07_eagle_dust.png` | Baby Eagle gets a hero beat | Eagle clears the high cobweb while the family cheers. |
| 08 | `08_hall_clean_reveal.png` | Hall progress payoff | All three finish together; the clean Hall points them onward. |
| 09 | `09_playroom_doorway.png` | Enter the Playroom | The trio sees toys, dress-up, puzzle, and tea-set clutter. |
| 10 | `10_playroom_before.png` | Count the sorting zones | Roshan counts jobs, Daddy sets the basket, Eagle points to the chest. |
| 11 | `11_playroom_sort.png` | Big toy sorting action | The trio and bunnies put large objects into clear homes. |
| 12 | `12_playroom_details.png` | Small-object teamwork | Roshan completes the puzzle; Daddy arranges tea; Eagle returns dress-up. |
| 13 | `13_playroom_clean.png` | Playroom payoff | Open clean rug, completed puzzle, parked toys, stored balls, tidy tea set. |
| 14 | `14_library_doorway.png` | Enter the Royal Library | Books, ribbons, scrolls, cards, cart, and cushions need care. |
| 15 | `15_library_before.png` | Plan three Library jobs | The family identifies shelves, cart/basket, and reading-rug groups. |
| 16 | `16_library_bunny_helpers.png` | Mid-clean teamwork | Roshan stacks, Daddy dusts, Eagle returns ribbons, bunnies help. |
| 17 | `17_library_last_book.png` | Precise final action | One book, one ribbon, and one scroll finish the job. |
| 18 | `18_library_clean_storytime.png` | Quiet Library payoff | The clean room becomes a wordless family storytime. |
| 19 | `19_basement_descent.png` | Adventure below | Dust bunnies guide the trio down a bright, broad shell stair. |
| 20 | `20_pantry_team.png` | Pantry connector beat | The trio wipes, stacks, and carries before crossing to the Kitchen. |
| 21 | `21_kitchen_doorway.png` | Reveal the existing Royal Kitchen | Plates, flour, drips, cups, pan, and jars form safe target groups. |
| 22 | `22_kitchen_jobs.png` | Assign safe Kitchen jobs | Roshan takes sink/plates, Daddy counter/cool stove, Eagle cups/jars. |
| 23 | `23_kitchen_sink.png` | Roshan's Kitchen hero beat | Roshan washes plates while Daddy sweeps flour and Eagle sorts cups. |
| 24 | `24_kitchen_counter_stove.png` | Daddy's Kitchen hero beat | The stove is off; Daddy wipes a drip as Roshan and Eagle finish sorting. |
| 25 | `25_kitchen_clean.png` | Kitchen payoff | Plates, cups, pan, and jars are ordered; the floor and counter are open. |
| 26 | `26_bath_discovery.png` | Enter the Bubble Bath | Soap ring, fog, towels, toys, and clean droplets are introduced. |
| 27 | `27_bath_mirror.png` | Roshan's mirror hero beat | Roshan clears mirror fog; Daddy folds towels; Eagle dabs the vanity. |
| 28 | `28_bath_tub_toys.png` | Tub-and-toy teamwork | Daddy brushes the tub, Roshan baskets toys, Eagle dries droplets. |
| 29 | `29_bath_clean.png` | Bath payoff and secret clue | The clean Bubble Bath reveals a softly glowing hidden arch. |
| 30 | `30_loo_reveal.png` | Discover the hidden Royal Loo | Soap ring, rolls, holder, and clean splash are safe, matter-of-fact jobs. |
| 31 | `31_loo_team.png` | Royal Loo teamwork | Roshan sponges soap, Daddy stacks rolls, Eagle dries clean water. |
| 32 | `32_loo_clean.png` | Loo payoff and undercroft clue | The clean small room opens visually toward dusty storage and stair. |
| 33 | `33_undercroft_before.png` | Last three cleanup zones | Storage, cart/shelf, and stair cobweb/dust are broad and readable. |
| 34 | `34_undercroft_clean.png` | Undercroft payoff | Storage is safe and ordered; bunnies ride upstairs in a cozy basket. |
| 35 | `35_final_inspection.png` | Family inspection | The trio sees every area shining and the bunnies in their new home. |
| 36 | `36_all_clean.png` | High-five finale | Roshan, Daddy, and Baby Eagle celebrate what they did together. |

## Visual continuity rules

- The same Mermaid Roshan, Daddy Mermaid, and Baby Eagle designs remain present
  across the sequence. Reflections do not count as duplicate characters.
- Room transitions follow the castle's real layout. The Royal Kitchen, Bubble
  Bath, hidden Royal Loo, and undercroft are existing basement spaces.
- “Before” frames use a few large target groups and retain a safe open route.
- “Clean” frames have broad open floor, explicit stored-object destinations,
  and restrained completion sparkles.
- The cool Royal Kitchen stove never has a flame during cleaning.
- Bathroom and Royal Loo mess is soap and clean water only.
- The undercroft is warmly lit, intact, and non-frightening.
- Dust bunnies are the only living mess characters. They help, listen, clap,
  ride in baskets, and receive a home.

## Runtime sequencing direction

- Display each image at 1024x576 or scale uniformly to the 1280x720 canvas.
- Do not place captions over the frames. Use the manifest's `voice_intent`
  through the existing `_say()`/recorded-voice path.
- A room-intro frame may bridge into play, and its clean-room frame may play
  only after the corresponding target set has been saved complete.
- The cinematic must resume from saved progress rather than replay already
  completed room actions after a reload.
- The final inspection and high-five must never trigger from passive time; they
  require completion of the last child-driven target.

## QA decisions

- Rejected the first Playroom completion generation because the floor remained
  cluttered; the accepted frame has a clean open rug and explicit destinations.
- Rejected one Bubble Bath action generation because it duplicated Baby Eagle;
  the accepted frame contains exactly one.
- Rejected one undercroft survey generation because it duplicated Daddy
  Mermaid; the accepted frame contains exactly one.
- The rejected images were not copied into the project.
