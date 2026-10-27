# Changelog

## 1.1.1 — 2026-10-27

1.1.0 was built and tested but never released; 1.1.1 is its first public form and includes everything below.

- Fix (2026-10-27): profile counts for sectors, treaties, investor home States (and the other multi-value fields) are now per value. UNCTAD lists several values in one cell separated by ";" + newline; the engine previously counted each cell string as one category, which understated, e.g., a two-sector case. Each distinct value counts once per case: UNCTAD repeats a sector once per subsector ("Manufacturing; Manufacturing; …"), and such a case counts once. A bare ";" is not a separator ("Water supply; sewerage, …" is one label). This was also present in 1.0.0.
- Fix (2026-10-27): shortlist scoring now uses each candidate's full case record. Sector and respondent were scored from the top-5 display lists (rules top 6, issues top 10), so a sector or State outside a candidate's top five scored 0 and `--respondent-gate` dropped candidates who do have cases against the State. Also present in 1.0.0.
- New (2026-10-27): `--subsector` filter and `subsector_match` signal (default weight 1.0) over UNCTAD's ECONOMIC SUBSECTOR; profiles show top subsectors. Template wording rule: sector figures are labelled by the UNCTAD category counted.
- New (2026-10-27): profiles list cases whose UNCTAD follow-on record contains an annulment or set-aside, with the arbitrator's role and the full follow-on sequence (outcome only; UNCTAD records no ground); shortlists show the count (not scored). New scoped record check "check the record on annulled awards".
- Tests: `tests/test_fixes_2026_10_27.py` (needs the 31/12/2025 workbook).
- Data: moves to UNCTAD's 31/12/2025 full-data release (1,463 cases, up from 1,332). This version works only with that release; any other prints `WRONG_RELEASE` with download links. An older file left in `data/` is ignored when the 31/12/2025 file is present.
- Fix: the header row is now found by its text and all 28 columns are checked before anything is read. (The 2025 file moved the header from row 12 to row 13; the fixed row number would have read the header line as a case.)
- Data-freshness footer, Sources sheet and docs updated for the new snapshot.
- UNCTAD renamed "Hoffmann, A." to "Hoffmann, A. K."; the `distinct` guard in `assets/curated-aliases.json` now names the new form.
- Worked example (`references/example-profile.md`) regenerated on the 31/12/2025 data; this also corrects the previous specimen's annulment-committee row and its dissent and appointing-side arithmetic.

## 1.0.0 — 2026-08-10

Initial public release.

- Two workflows: structured arbitrator profiles (single or multiple arbitrators) and case-based shortlisting with transparent, user-adjustable ranking weights.
- Profiles grounded in the user's own UNCTAD ISDS Navigator dataset (31/12/2023 snapshot) plus targeted live lookups of ICSID arbitrator profile pages; record checks retrieve and read the underlying decisions via the companion [isds-research](https://github.com/ccrnyc/isds-research) skill.
- Shortlist scoring normalised against the candidate pool (raw-count mode available via `--raw-scores`); ranking weights always printed with the shortlist.
- Delta workflow for cases newer than the snapshot, classified by the arbitrator's acceptance date.
- Hard sourcing rules throughout: no issue-outcome claims from secondary sources; table values read from the page's own text; availability never asserted without a named, dated source; conflicting values shown, never silently resolved.
- Compliance gates on by default: targeted, user-initiated lookups only; default-deny for hosts not in the compliance table; no bulk harvesting.
- Delivery checklist enforced on every run (work-product headers, archived extracts for everything quoted, formatting spec, run-folder verification).
