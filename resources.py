# DMCAShield Resource Integrations
# ================================
# Connects your cloned repos as resources

RESOURCES = {
    "memory_repos": {
        "path": "F:/Anti gravity projects/Memory github skill repo",
        "description": "Memory tracking repo",
        "uses": ["long-term memory", "context tracking"],
        "integrate": True
    },
    "godmode": {
        "path": "F:/Anti gravity projects/github repos skills etc/G0DM0D3",
        "description": "Godmode AI interface",
        "uses": ["AI orchestration", "multi-model race"],
        "integrate": True
    },
    "claude_antigravity": {
        "path": "F:/Anti gravity projects/claude and antigravity",
        "description": "Claude + Antigravity setup",
        "uses": ["API proxy", "team coordination"],
        "integrate": True
    },
    "opencode": {
        "path": "F:/Anti gravity projects/opencode",
        "description": "OpenCode CLI",
        "uses": ["file operations", "agent tasks"],
        "integrate": True
    },
    "system_design": {
        "path": "F:/Anti gravity projects/system-design-101",
        "description": "System design templates",
        "uses": ["architecture patterns"],
        "integrate": True
    },
    "pinterest_automation": {
        "path": "F:/Anti gravity projects/pintrest automation",
        "description": "Pinterest automation",
        "uses": ["social automation", "scraping"],
        "integrate": False
    },
    "saas_project": {
        "path": "F:/Anti gravity projects/SaaS project",
        "description": "SaaS project template",
        "uses": ["project setup", "boilerplate"],
        "integrate": True
    },
    "how_to_kick": {
        "path": "F:/Anti gravity projects/how-to-kick-saas",
        "description": "SaaS validation guides",
        "uses": ["business validation", "go-to-market"],
        "integrate": True
    },
    "openwolf": {
        "path": "F:/Anti gravity projects/openwolf",
        "description": "OpenWolf design system",
        "uses": ["UI components", "design patterns"],
        "integrate": True
    },
    "prompt_maker": {
        "path": "F:/Anti gravity projects/prompts making",
        "description": "Prompt engineering tools",
        "uses": ["prompt optimization", "AI training"],
        "integrate": True
    }
}

# Resource helper functions
def get_resource(name: str) -> dict:
    """Get resource by name"""
    return RESOURCES.get(name, {})

def list_all_resources() -> list:
    """List all available resources"""
    return [{"name": k, **v} for k, v in RESOURCES.items()]