# Gabby — removed from the game 2026-07-19 (owner directive)

Gabby represents an IP conflict for the moment; she is out of the build until
she can be redeveloped as an original character. Nothing here is deleted —
these are the exact bytes that used to live in the game, preserved for that
future redevelopment:

| file | former path |
|---|---|
| friend_gabby.png | assets/characters/friends/gabby.png |
| sticker_gabby.png | assets/characters/stickers/gabby.png |
| p_gabby.jpg | assets/book/hall/p_gabby.jpg |
| gabby_stage.jpg | assets/book/gabby_stage.jpg (melody-theater design ref) |
| gabby.ogg / gabby_win.ogg / gabby_fail.ogg | assets/audio/voices/ (Kokoro TTS — regenerable, NOT family recordings) |

The whole `attic/` tree is behind a `.gdignore`, so Godot never imports or
exports any of it. In-game, Daddy Mermaid took over her reef-friend slot and
the rainbow theater; saves migrate her found/won progress to him
(scripts/save_state.gd LEGACY_FRIEND_SAVE_KEYS).
