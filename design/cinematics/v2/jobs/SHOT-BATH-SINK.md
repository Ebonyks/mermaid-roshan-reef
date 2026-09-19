# Job envelope — SHOT-BATH-SINK (still only)

Hand Grok **only** these files:

1. `design/cinematics/v2/START_GROK.txt`
2. `design/cinematics/v2/shots/SHOT-BATH-SINK/CARD.json`
3. `design/cinematics/v2/shots/SHOT-BATH-SINK/PROMPT.txt`
4. `design/cinematics/v2/canon/IDENTITY.json` — `CHAR-ROSHAN` only
5. `design/cinematics/v2/canon/KNOCKOUTS.json`
6. `design/cinematics/v2/exchange/attempts/SHOT-BATH-SINK/A001/REQUEST.json`

Bind bytes (private packet, not this repo):

| Slot | Ref | SHA-256 prefix | Job |
|---|---|---|---|
| IMAGE_1 | `REF-90bcc501e471b8d8` | `90bcc501e471b8d8` | empty dirty bathroom |
| IMAGE_2 | `REF-69827625a8a795f1` | `69827625a8a795f1` | Roshan |
| IMAGE_3 | `REF-17e76b7f758f31a9` | `17e76b7f758f31a9` | brush |

Return a still + SHA-256 in `RETURN.json`. Do not animate. Do not open any other shot folder.
