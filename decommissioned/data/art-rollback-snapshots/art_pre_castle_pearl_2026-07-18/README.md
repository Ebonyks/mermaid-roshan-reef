# Pre-Pearl Castle Reversal Archive

`castle_pre_pearl_assets.zip` is a byte-exact `git archive` from commit
`9943f16`. It preserves the files changed in the pearl-castle pass before any
new geometry was generated or integrated:

- `assets/castle/bathroom_toilet.glb`
- `assets_src/blender/bathroom_toilet_v2.blend`
- `assets_src/blender/qa_bathroom_props/bathroom_toilet.png`
- `scripts/arena/castle_hall.gd`
- `tools/build_bathroom_toilet_v2.py`

SHA-256:
`467869F4B88ACC3C46D5818D6875F823F7E30CF23A3D97FB458D8F0A3FEE46CA`

The archive keeps original repository-relative paths. Extract it at a temporary
location and restore only the disputed files, or restore the same baseline from
Git with:

```powershell
git restore --source=9943f16 -- <path>
```

The new `assets/castle/pearl_kit/` files did not exist in the baseline and can
be removed independently if the complete architecture pass is reverted.
