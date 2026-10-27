"""Checks for the 2026-10-27 fixes (1, 2, 5, 6). Needs the 31/12/2025 workbook.
Run: python3 tests/test_fixes_2026_10_27.py [path/to/workbook.xlsx]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import query_arbitrators as q

XL = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "data",
                                                         "UNCTAD-ISDS-Navigator-data-set-31December2025.xlsx")
ov = json.load(open(os.path.join(HERE, "..", "assets", "curated-aliases.json")))
ds = q.Dataset(XL, ov)
fails = []
def check(name, got, want):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + f"{name}: got {got!r}, want {want!r}")
    if not ok: fails.append(name)

# Fix 1 — value splitting and per-value counts
check("split keeps a label containing '; '",
      q.split_values("Tertiary - E - Water supply; sewerage, waste management and remediation activities"),
      ["Tertiary - E - Water supply; sewerage, waste management and remediation activities"])
check("split on ';' + newline", q.split_values("Panama;\nUnited States of America"),
      ["Panama", "United States of America"])
kk = ds.profile("Kaufmann-Kohler, G.")
check("KK appointments unchanged", kk["seats"], 88)
check("KK pending unchanged", kk["pending_at_snapshot"], 16)
check("KK opinions denominator unchanged", kk["opinions_known_denominator"], 62)
check("KK annulment committees unchanged", kk["annulment_committees"], 1)
check("KK mining (per value)", kk["sectors"].get("Primary - B - Mining and quarrying"), 19)
check("KK manufacturing (per case; Bahari (II) lists it twice)", kk["sectors"].get("Secondary - C - Manufacturing"), 15)
# N1 — a value repeated within one cell counts once for that case
check("repeated value in one cell counts once (Pizzorno v. Morocco, Ziadé)",
      ds.profile(next(t for t in ds.resolve("Ziad") if t.endswith(", N.")))["sectors_all"].get(
          "Tertiary - E - Water supply; sewerage, waste management and remediation activities"), 1)
check("sector J score: Stern (Al Awamleh lists J twice)",
      next(r["subscores"]["sector_match"] for r in ds.shortlist(sector="Information and communication", top=2000, min_seats=1) if r["token"] == "Stern, B."),
      len({c for c in {s["case"] for s in ds.seats if s["token"] == "Stern, B."} if "Information and communication" in str(ds.rows[c][q.COL["sector"]])}))
check("KK distinct IIAs (per value)", kk["iias_total"], 77)
check("KK home US (per value)", kk["home_states"].get("United States of America"), 15)
check("KK home Netherlands (per value)", kk["home_states"].get("Netherlands"), 9)

# Fix 2 — scoring on full rows
def sub_of(res, tok):
    return next((r["subscores"] for r in res if r["token"] == tok), None)
res = ds.shortlist(sector="Information and communication", respondent="Mozambique", top=2000, min_seats=1)
check("Fortier ICT sector score (6th+ sector)", sub_of(res, "Fortier, L. Y.")["sector_match"], 4)
check("Alexandrov ICT sector score", sub_of(res, "Alexandrov, S. A.")["sector_match"], 3)
check("Alexandrov Mozambique score", sub_of(res, "Alexandrov, S. A.")["respondent_match"], 1)
gated = {r["token"] for r in ds.shortlist(respondent="Mozambique", respondent_gate=True, top=2000, min_seats=1)}
check("respondent gate keeps Mozambique arbitrators",
      {"Alexandrov, S. A.", "Fortier, L. Y.", "van den Berg, A. J."} <= gated, True)

# Fix 5 — subsector signal
res = ds.shortlist(subsector="61 - Telecommunications", top=2000, min_seats=1)
check("Hanotiau telecoms subsector", sub_of(res, "Hanotiau, B.")["subsector_match"], 3)
check("Grigera Naón telecoms subsector", sub_of(res, "Grigera Naón, H. A.")["subsector_match"], 4)

# Fix 6 — annulled / set-aside awards
pon = ds.profile("Poncet, C.")
check("Poncet: Rockhopper listed as annulled",
      any(u["case"] == "Rockhopper v. Italy" for u in pon["annulled_or_set_aside"]), True)
inf = ds.profile("Hanotiau, B.")
yuk = next(u for u in pon["annulled_or_set_aside"] if u["case"] == "Yukos Universal v. Russia")
check("Yukos full sequence kept (upheld -> set aside -> upheld)", [x.split(" Judicial")[0] for x in yuk["follow_on"]],
      ["Award/decision upheld", "Award/decision set aside in its entirety", "Award/decision upheld"])
check("Hanotiau: Infinito (annulment discontinued) NOT listed",
      any(u["case"] == "Infinito Gold v. Costa Rica" for u in inf["annulled_or_set_aside"]), False)

# Unchanged behaviour — the two Scherers stay distinct
check("Scherer markers resolve to two names", sorted(ds.resolve("Scherer, M.")), ["Scherer, M. (*)", "Scherer, M. (**)"])

print(f"\n{len(fails)} failure(s)" + (": " + ", ".join(fails) if fails else ""))
sys.exit(1 if fails else 0)
