# Ingredient-level interaction — owner direction, 2026-08-03

> "If we're having this complexity of ingredients, the gameplay should impact
> it. You should have to crack the eggs, for example, in a visceral motion."

## What this changes

Everything so far has been **a gesture mode with a skin on it**: the beat is
`hold`, and the art behind it is a bowl. The child's finger acts on *the
surface*, and the picture reacts in the abstract.

The direction is now **direct manipulation of the depicted objects**. The
scene is not a backdrop for a gesture — the scene IS the interaction. Each
ingredient is a thing on screen with its own state, and the motion that
changes it should be the motion you would really make:

| Object | The real motion | State change |
|---|---|---|
| egg | a sharp downward flick/tap on the egg itself | whole -> cracked -> contents fall into the bowl |
| milk jug | drag the jug over the bowl and tip it, hold while it streams | full -> pouring -> empty; the bowl's level rises |
| flour scoop | drag and shake | heaped -> dusting -> emptied |
| batter | circular drag ON the batter | streaky -> combining -> smooth |
| piping bag | squeeze-and-drag along the cake | full -> ribbon laid -> decorated |

"Visceral" is the operative word: the crack should be a *snap*, with a sound,
a shell that splits, a yolk that drops and lands. Not a meter filling.

## Why this is reachable, not a rewrite

The engine already does per-object hit-testing and per-object state in the
world: `bop` mode holds an array of targets with position, radius, hp and
popped state, and hit-tests taps AND swipe segments against them; `lens` does
dwell-on-target. An **ingredient mode is the same shape**: an array of objects,
each with a position, a required motion, and a state that advances.

So the work is: one new surface mode driving a small per-beat object list,
where each object declares its motion (flick / tip-hold / circle-on / drag-along)
and its state art. The gesture vocabulary already exists — it is being pointed
at objects instead of at the whole panel.

## The consequence for the art request

Every ingredient the art depicts now needs its **states**, not just its
presence:
- egg: whole, cracking, split with yolk falling, empty shell
- jug: upright, tipping, streaming, empty
- bowl contents: empty, streaky, mixed, finished
- piping bag: full, squeezing with ribbon, done

That is more art per beat than "backdrop + fill overlay" — but it is what makes
the beat a *thing you do* rather than a bar you fill, and it is the same
painted-layer economy (states are layers the engine swaps or reveals, not frame
sequences).

## Sequencing within a beat

A beat becomes a short recipe rather than one sustained gesture: *crack two
eggs -> tip the milk -> stir it smooth*. Three small satisfying actions beat one
long abstract hold, which also answers the earlier pacing finding that holds
were the least legible beats. Order should be forgiving — any ingredient can be
handled at any time, and the beat completes when all are done.

## Status

Direction captured. The art-concept pass in flight is writing the rich scenes;
the interaction design (which object takes which motion, per beat, across all
~60 beats) is the next pass, and the two merge into one codex handoff plus one
engine work item.
