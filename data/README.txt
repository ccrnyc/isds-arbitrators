data/ — the user's own UNCTAD ISDS Navigator full-data Excel goes here.

Download it yourself — this version needs the 31/12/2025 release:
  https://investmentpolicy.unctad.org/uploaded-files/document/UNCTAD-ISDS-Navigator-data-set-31December2025.xlsx
  (release page: https://investmentpolicy.unctad.org/publications/1325/investment-dispute-settlement-navigator-full-isds-data-release-as-of-31-12-2025-)
Any other release is refused with a WRONG_RELEASE message; an older file
may stay here beside it. UNCTAD terms prevent redistribution of the Excel dataset with this skill; this folder holds only your local copy.

Any filename with the UNCTAD schema will be accepted — the engine
validates the header row and prints a load-verification line
("[dataset loaded: ... — 1463 cases x 28 data columns]"). If no workbook is
here, the engine searches this folder and the current directory and tells
you exactly what to do; the skill also checks the connected project folder
(e.g. isds-arbitrators/data/) before asking for a fresh upload.

CLOUD SESSIONS: Cloud folders do not persist between sessions (a fresh
cloud container starts empty), so keep your copy in the connected local project
folder and let the skill stage it each session; the recorded path lives in
user-config.json saved to the connected run root. If only a run folder
is connected, keeping the workbook there is fine — just record its path in
user-config.json so future sessions find it.

Both setup gates (UNCTAD workbook present + writable run folder connected) will fire in
every fresh cloud session. Connect the run root and keep the Excel in the connected local folder
before the first prompt to clear both setup gates.
