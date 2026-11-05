# Launch-time 301 map (PREPARED, NOT APPLIED)

Applied only at launch of the new brand (step 7 of the plan). Targets are **placeholders** under `/learn/`; replace with real paths once the new Learn section exists. Anything not listed goes to the new homepage `/`. Priority comes from Search Console (Oct 2026 report: per-90 118 clicks, Python ML posts ~21 each, pick-players growing).

## Pages with real search traffic

| Old URL | New path (placeholder) | Why |
|---|---|---|
| /per-90-stats-explained/ | /learn/per-90-stats/ | 118 clicks in Oct; top queries are per-90 maths |
| /understanding-pick-players-draftkings/ | /learn/dfs-scoring-and-player-pricing/ | growing |
| /set-pieces-daily-fantasy-football/ | /learn/set-pieces/ | evergreen |
| /python-for-fantasy-football-introduction/ | /learn/python-for-fantasy-football/ (series hub) | Python series, ~21 clicks each on the ML intro posts |
| /python-for-fantasy-football-matchup-adjustment/ | /learn/python-for-fantasy-football/ (series hub) | Python series, ~21 clicks each on the ML intro posts |
| /python-for-fantasy-football-getting-and-cleaning-data/ | /learn/python-for-fantasy-football/ (series hub) | Python series, ~21 clicks each on the ML intro posts |
| /python-for-fantasy-football-apis-and-json-data/ | /learn/python-for-fantasy-football/ (series hub) | Python series, ~21 clicks each on the ML intro posts |
| /python-for-fantasy-football-introduction-to-machine-learning/ | /learn/python-for-fantasy-football/ (series hub) | Python series, ~21 clicks each on the ML intro posts |
| /python-for-fantasy-football-addressing-class-imbalance-in-machine-learning/ | /learn/python-for-fantasy-football/ (series hub) | Python series, ~21 clicks each on the ML intro posts |
| /python-for-fantasy-football-addressing-class-imbalance-part-2/ | /learn/python-for-fantasy-football/ (series hub) | Python series, ~21 clicks each on the ML intro posts |
| /python-for-fantasy-football-understanding-random-forests/ | /learn/python-for-fantasy-football/ (series hub) | Python series, ~21 clicks each on the ML intro posts |
| /python-for-fantasy-football-feature-engineering-for-machine-learning/ | /learn/python-for-fantasy-football/ (series hub) | Python series, ~21 clicks each on the ML intro posts |
| /python-for-fantasy-football-random-forest-and-xgboost-hyperparameter-tuning/ | /learn/python-for-fantasy-football/ (series hub) | Python series, ~21 clicks each on the ML intro posts |

## Other evergreen
| Old URL | New path | Note |
|---|---|---|
| /how-to-play-daily-fantasy-football/ | / | operator offers stale |
| /understanding-how-to-pick-yahoo-players/ | / | Yahoo DFS gone for UK |
| /january-transfers-fantasy-perspective/ | / | dated |
| /common-cognitive-biases-in-daily-fantasy-football/ | /learn/ if a biases page is written, else / | |
| /glossary/ | /learn/glossary/ | |
| /about/ | /about/ | |

## Everything else
- All gameweek/seasonal previews and reviews, `/book/`, `/faq/`, `/articles/`: `/` (301).
- Attachment pages: parent post's new path where mapped above, else `/`.
- Catch-all `/*`: `/` (301).

## Mechanics
GitHub Pages cannot send real 301s (stub pages plus 404.html are used today). At launch the new site must serve these as true 301s; `docs/_redirects` is the starting list.
Also at launch: add one line to the `twhelan22/python-for-fantasy-football` README pointing at the new site.
