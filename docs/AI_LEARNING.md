# AI Learning & Mistake Tracker

## Overview
The DMCAShield system now includes an **AI Learning** subsystem that continuously improves based on campaign performance and recorded mistakes.

### Key Components
- **Learning Sources** – Email opens, clicks, replies, bounces.
- **Mistake Tracker** – `/api/ai/learn-from-mistakes` endpoint records failures with category, context, and reason.
- **Improvement Plan** – `/api/ai/improvement-plan` returns prioritized suggestions generated from aggregated mistake patterns.
- **Frontend UI** – `SelfLearning.jsx` provides a form for reporting mistakes and a live view of the improvement plan.

## API Endpoints
| Method | Path | Description |
|---|---|---|
| `POST` | `/api/ai/learn-from-mistakes` | Record a mistake. Body JSON: `{ "category": "sales|marketing|email|general", "context": { "description": "..." }, "reason": "..." }` |
| `GET` | `/api/ai/improvement-plan` | Retrieve current improvement suggestions. Returns `{ "issues": [{"category":"...","priority":"high|medium","suggestion":"..."}], "success_rate":0.xx, "total_improvements":N, "pending_issues":M }` |

## Frontend Usage (SelfLearning page)
- **Report a Mistake** – Fill the form, select a category, describe the context, and submit. The UI calls the POST endpoint and then refreshes the improvement plan.
- **View Improvements** – The panel lists each issue with priority badges and the AI‑generated suggestion.
- **Success Metrics** – Shows success rate and total improvements applied.

## How It Works
1. When a mistake is posted, `LearnFromMistakes.record_mistake` logs it and updates pattern counters.
2. Periodically or on demand, `/api/ai/improvement-plan` aggregates patterns with a count > 1 and creates high/medium priority suggestions.
3. The frontend pulls this data and presents it to the user for actionable changes.

## Team Guidelines
- **Always report** any failure you encounter via the UI. This fuels the improvement cycle.
- **Review the improvement plan** before making large changes; the AI prioritizes high‑impact fixes.
- **Update the frontend** if new categories or fields are needed—extend the form and API payload accordingly.
- **Collaborate**: share insights in the #ai‑learning channel. Discuss patterns, edge cases, and validation rules.

---
*This documentation is part of the ongoing effort to make DMCAShield a self‑optimizing autonomous agency.*