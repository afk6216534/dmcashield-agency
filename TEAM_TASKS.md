# Team Task Queue for Claude Code
# ============================
# Add tasks here that you want Claude Code to complete

## How to add tasks:
# Just edit this file and add your task below

## Current Tasks:

### 🎨 Frontend UI Tasks (Assigned to: Claude Code)
- [ ] **Task Progress Visualization** (Priority: HIGH)
  - Add real-time visual progress indicator steps ("OSM nominatim lookup", "scraping directories", "extracting emails", "scoring validation") on the Task Manager and Task Launch pages.
- [ ] **Lead Selection Campaign Trigger** (Priority: MEDIUM)
  - Add checkboxes in the Lead Database page allowing the user to select multiple leads and launch a manual email outreach campaign.

### ⚙️ Backend Logic Tasks (Assigned to: OpenCode)
- [ ] **Automated Queue Scheduler** (Priority: HIGH)
  - Create a lightweight background worker or cron script that checks for "pending" scrape tasks and processes them sequentially in the background.
- [ ] **Scraping Task Retry Endpoint** (Priority: MEDIUM)
  - Implement `POST /api/tasks/<task_id>/retry` to re-trigger failed or incomplete scraping jobs.

## Notes:
# - Claude Code can read this file and pick up tasks
# - System runs autonomously 24/7
# - 100 skills available
# - Auto-training learns from results