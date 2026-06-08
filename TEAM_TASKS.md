# Team Task Queue for Claude Code
# ============================
# Add tasks here that you want Claude Code to complete

## How to add tasks:
# Just edit this file and add your task below

## Current Tasks:

### 🎨 Frontend UI Tasks (Assigned to: Claude Code)
- [ ] **Task Phase Stats Display** (Priority: 🔴 CRITICAL)
  - The `GET /api/tasks` response now returns `leads_validated`, `leads_in_funnel`, `leads_emailed`, `campaign_id`, and `phase_*` flags. Update Task Manager card to display real counts under each phase icon.
- [ ] **Task Progress Visualization** (Priority: HIGH)
  - Add real-time visual progress indicator steps ("Scraping 50 leads", "Validating MX", "Building Funnels", "Sending Emails", "Tracking", "Sales Ready") on the Task Manager and Task Launch pages.
- [ ] **Lead Selection Campaign Trigger** (Priority: MEDIUM)
  - Add checkboxes in the Lead Database page allowing the user to select multiple leads and launch a manual email outreach campaign.
- [ ] **Lead Funnel Step Badge** (Priority: MEDIUM)
  - Show funnel_step (1-4) as colored badges on LeadDatabase rows: Step 1 = "Queued", Step 2 = "Day 1 Sent", Step 3 = "Follow-up", Step 4 = "Breakup".

### ⚙️ Backend Logic Tasks (Assigned to: OpenCode)
- [x] **Follow-Up Email Cron** (Priority: 🔴 CRITICAL)
  - Create `POST /api/campaigns/send-followups` (implemented via `/api/drip/send` unified scheduler) that iterates over all leads and auto-sends follow-ups when delay has elapsed.
- [ ] **Automated Queue Scheduler** (Priority: HIGH)
  - Create a lightweight background worker or cron script that checks for "pending" scrape tasks and processes them sequentially in the background.
- [ ] **Scraping Task Retry Endpoint** (Priority: MEDIUM)
  - Implement `POST /api/tasks/<task_id>/retry` to re-trigger failed or incomplete scraping jobs.

## Notes:
# - Claude Code can read this file and pick up tasks
# - System runs autonomously 24/7
# - 100 skills available
# - Auto-training learns from results