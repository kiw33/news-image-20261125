# BUILD-NOTE — news-image-20261125

- Competition: `news-image-20261125`
- Prize: $100 USDC shared by top 50 (1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20)
- Opens: already open at build time — status `open`, `acceptingSubmissions: true`,
  escrow funded 100 USDC, verified via the make.fun API 2026-11-25 ~09:39 WIB
- Closes: 2026-11-27 00:00 UTC (Friday 27 Nov 2026, 07:00 WIB); final window
  starts then; result due 2026-12-11 08:00 UTC
- Gate: whole PNG or JPEG, at most 1 MiB and 1024×1024 pixels; program runs
  twice, both runs byte-identical.
- Entrypoint: `main.py` at repo root (Python 3, Pillow + DejaVu fonts, harness
  program/v1). It REDRAWS the image at grading time — it does not copy a
  shipped PNG.

## Entry image

- File: `entry.png`, 1024×1024 RGB
- Size: 125,705 bytes (limit 1,048,576)
- SHA-256: `65498f0d0b266e923cea0ffa5f80e78cd77d35639aad7509c78edfed42733a59`
- Layout: header naming the date ("WEDNESDAY · 25 NOVEMBER 2026"), six panels
  (2 columns × 3 rows), each with a drawn pictogram, a headline and a
  three-line caption; "Also today" ticker strip at the bottom.
- Six stories: Zelenskiy confirms the Gulf of Finland ship strike; Medvedev's
  "preventive nuclear attack" warning; NATO sends AWACS to Poland; Houthis hit
  Riyadh's tallest tower (11 wounded); Huawei convicted in a US trial; CIA and
  ODNI hit by a cyber breach. All six were reported on 25 November 2026
  (see SOURCES.md).

## Why this image

It names the day up front, covers six consequential stories across regions
and beats — war/diplomacy, nuclear signalling, alliance response, Middle
East, tech/business, cyber — each readable from its picture plus a short
label with nothing self-contradictory, stays to what was reported without
hype, and is one clean composition, legible at small size, with no garbled
text.

The drawing code was written fresh for this day: no file from the 23 or
24 November entries was read or copied (their layout pattern was reviewed
for the series format only). The headlines and ticker were revised once
after the first render (four headlines were wrapping to a cut-off third
line; the ticker overflowed the bottom edge) — the entrypoint's final
content comes from several writing passes.

## Verification (local, run 2026-11-25)

1. Rendered with `MAKEFUN_OUTPUT_DIR=/tmp/news25a python3 main.py` → entry.png written.
2. Rendered a second time to a clean directory; both runs byte-identical
   (SHA-256 `65498f0d…733a59` on both runs, and again for the shipped `entry.png`).
3. Gate check passed: PNG magic bytes, 1024×1024, RGB, 125,705 bytes ≤ 1 MiB.
4. Visual check of the render: header, six panels, pictograms, headlines and
   captions all legible, no overlap, no clipped text; ticker fits in three
   lines with margin to spare.

Run the check yourself:

```sh
rm -rf /tmp/news25a && mkdir -p /tmp/news25a
MAKEFUN_OUTPUT_DIR=/tmp/news25a python3 main.py && sha256sum /tmp/news25a/entry.png
rm -f /tmp/news25a/entry.png
MAKEFUN_OUTPUT_DIR=/tmp/news25a python3 main.py && sha256sum /tmp/news25a/entry.png
python3 -c "from PIL import Image; im=Image.open('/tmp/news25a/entry.png'); print(im.size, im.mode)"
```

## Repo note for the submitter

- Repo must be created after the competition opened and carry
  `.makefun/owner.json` naming the linked wallet (included).
- Push the text files via push_files; upload `entry.png` via the browser
  (push_files rejects binary files).
- README badges above use `kiw33/news-image-20261125` as the repo name; adjust
  the rank/reward badge URLs if the repo is created under a different name.
- GitHub About must have a website on make.fun and the topic `makefun` before
  submitting (kit check `repo_about`).
- Title for submit: "The World in One Image".
