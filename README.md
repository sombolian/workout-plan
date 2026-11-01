# Workout plan JSON (for the "האימון שלי" Android app)

Local master copy: `/workspace/wellness/plan/plan.json`
App fetches (default): `https://raw.githubusercontent.com/sombolian/workout-plan/main/plan.json?t=<ms>`
 (cache-busting param + no-cache headers; GitHub raw CDN may still serve a copy up to ~5 min old)
The app also accepts a different URL: gear icon -> "כתובת התוכנית (URL)", or set top-level `"planUrl"` in a fetched plan to move it.

App loading order: remote URL (app start + pull-to-refresh + refresh icon) -> last good cached plan -> plan bundled in the APK.

## Schema (schemaVersion 1)
Top level: `schemaVersion` (1), `version` (int, BUMP ON EVERY EDIT), `updatedAt` (ISO-8601), `titleHe`, `defaultRestSec` (90), `exercises` [], optional `planUrl`.
Exercise: `id` (required, unique), `nameHe` (required), `nameEn`, `descriptionHe`, `type` (strength|cardio|timed, default strength),
`icon` (cardio|legs|back|chest|shoulders|arms|core), `imageUrl`, `weight` (free text), `sets` (int, default 1), `reps` (free text),
`durationSec` (cardio/timed per-set seconds), `restSec` (overrides defaultRestSec), `warmupHe`, `notesHe`, `repsAssumed` (bool -> "הערכה" badge).
Unknown fields are ignored, missing optional fields are fine. Note: done-set progress is stored per date + plan `version`,
so bumping `version` mid-workout resets that day's ticked sets.

## How a bot updates the plan
1. Edit `/workspace/wellness/plan/plan.json` (keep UTF-8 Hebrew, bump `version`, set `updatedAt`).
2. Validate: `python3 /workspace/wellness/plan/validate_plan.py`
3. Publish to the repo (once it exists and the box has push access):
   `cd /workspace/wellness/plan && git add plan.json && git commit -m "plan vN" && git push origin main`
   (or via a cloud agent commit to sombolian/workout-plan main:plan.json).
4. yuval pulls down to refresh in the app (or reopens it). Status chip shows "עודכן מהשרת" + last sync time.
