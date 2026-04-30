{
  "version": "1.0.0",
  "team": "Antigravity + Claude Code + OpenCode",
  "project": "DMCAShield Agency",
  "roles": {
    "opencode": {
      "name": "OpenCode",
      "responsibilities": [
        "File operations (read, write, edit)",
        "Glob and grep searches",
        "API endpoint creation",
        "Database models",
        "FastAPI server setup"
      ],
      "strengths": ["Quick file operations", "Glob/search", "JSON handling"],
      "prefer_not_to_repeat": ["Frontend React", "Complex debugging", "Multi-file refactors"]
    },
    "claude_code": {
      "name": "Claude Code",
      "responsibilities": [
        "Frontend React components",  
        "Complex debugging",
        "Architecture decisions",
        "Code review",
        "Testing"
      ],
      "strengths": ["React/Frontend", "Complex logic", "Debugging"],
      "prefer_not_to_repeat": ["Basic API endpoints", "Simple CRUD"]
    }
  },
  "task_divisions": {
    "phase_1_backend": {
      "assigned_to": "opencode",
      "description": "Create FastAPI server, models, basic endpoints",
      "do_not_repeat": true
    },
    "phase_1_frontend": {
      "assigned_to": "claude_code", 
      "description": "Create React dashboard and pages",
      "do_not_repeat": true
    },
    "additional_features": {
      "assigned_to": "opencode",
      "allow_duplicates": false,
      "coordination": "Check TEAM_CHAT.md first"
    }
  },
  "coordination": {
    "communication_file": "TEAM_CHAT.md",
    "status_check": "Check project files before starting",
    "avoid_duplicates": "Read AGENTS.md or TEAM_CHAT.md first"
  },
  "rules": [
    "Check TEAM_CHAT.md before starting new work",
    "Read AGENTS.md for project context",
    "Avoid repeating what others have done",
    "Update TEAM_CHAT.md when completing tasks",
    "Use existing cloned repos when possible"
  ]
}