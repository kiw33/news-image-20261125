# news-image-20261125 — The World in One Image

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/kiw33/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/kiw33/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Entry for make.fun competition `news-image-20261125`: sum up the world
news of Wednesday 25 November 2026 in a single 1024x1024 image.

## Run it

```sh
python3 main.py
```

`main.py` (Python 3, Pillow + DejaVu fonts) redraws the image
deterministically and writes `entry.png` to `$MAKEFUN_OUTPUT_DIR`
(or `/output` when unset). Two runs give the same sha256.

## Files

- `main.py` — entrypoint: draws the masthead, six story panels with flat
  pictograms, and the "Also today" ticker into `entry.png`.
- `entry.png` — the finished image (1024x1024), rendered by `main.py`.
- `SOURCES.md` — every fact in the image, with sources dated 25 Nov 2026.
- `BUILD-NOTE.md` — gate, verification hashes, opens/closes.

## Stories

1. Ukraine claims Baltic ship strike — Zelenskiy confirms Kyiv's drones hit a Russian cargo ship in the Gulf of Finland
2. Moscow warns of nuclear strike — Medvedev floats a "preventive nuclear attack" as Ukraine and NATO cross lines
3. NATO sends AWACS to Poland — early-warning aircraft after Kh-101 missiles fell in Poland
4. Houthis hit Riyadh's top tower — drone strike wounds 11, second hit in under a week
5. Huawei convicted in US trial — guilty over its Iran business and stolen trade secrets
6. CIA and ODNI hit by breach — cybersecurity breach involving some unclassified information

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
