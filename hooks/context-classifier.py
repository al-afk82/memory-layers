#!/usr/bin/env python3
import sys
import json
import os

CAPTURE_TRIGGERS = [
    'wrap up', 'wrapping up', 'done for today', 'that\'s it for today',
    'end session', 'close out', 'signing off', 'we done', 'finish up',
    'session done', 'calling it', 'that\'s all for now', 'run capture',
    'capture protocol', 'run the delta',
]

PROJECT_TRIGGERS = {
    'outreach-agent': [
        'malec', 'malec systems', 'outreach', 'pipeline', 'discovery',
        'intelligence', 'scoring', 'leather', 'hello pacer', 'max', 'bike',
        'client', 'campaign', 'prospect', 'reply', 'follow up', 'cold email',
        'linkedin note', 'stage 0', 'stage 1', 'stage 2', 'stage 3', 'stage 4',
    ],
    'learning-loop': [
        'corrections', 'learning loop', 'log', 'delta', 'pattern',
        'brain update', 'conclude', 'session log', 'pending loop',
    ],
    'alignment': [
        'alignment', 'misalignment', 'aligned', 'session capture',
        'constraint dialogue', 'root cause', 'pending alignment',
    ],
    'drift': [
        'drift', 'constraint hold', 'mid-session', 'guard rail',
        'enforcement', 'guardrail',
    ],
    'memory-layers': [
        'memory layers', 'memory-layers', 'layer 1', 'layer 2', 'layer 3',
        'variance', 'cup overflow', 'recognition layer', 'david vogel',
        'context gathering', 'classifier', 'harness', 'auto context',
        'automatic context', 'routing context', 'context engineering',
        'context router', 'context classifier',
    ],
    'health-check': [
        'can you run to see if everything is organised',
        'organised', 'health check', 'data room', 'inventory',
        'everything organised',
    ],
}

BRAIN_TRIGGERS = [
    'voice', 'writing style', 'how i write', 'constraints', 'quality criteria',
    'anti patterns', 'anti-patterns', 'how the system works', 'echosystem',
]

PROJECT_MAP = {
    'outreach-agent': '~/Documents/alecs-echosystem/projects/outreach-agent/CLAUDE.md',
    'learning-loop':  '~/Documents/alecs-echosystem/projects/learning-loop/CLAUDE.md',
    'alignment':      '~/Documents/alecs-echosystem/projects/alignment/CLAUDE.md',
    'drift':          '~/Documents/alecs-echosystem/projects/drift/CLAUDE.md',
    'memory-layers':  '~/Documents/alecs-echosystem/projects/memory-layers/CLAUDE.md',
    'health-check':   '~/Documents/alecs-echosystem/brain/knowledge/data-room-protocol.md',
}

def match_project(text):
    text_lower = text.lower()
    for project, triggers in PROJECT_TRIGGERS.items():
        for trigger in triggers:
            if trigger in text_lower:
                return project
    return None

def match_brain(text):
    text_lower = text.lower()
    return any(t in text_lower for t in BRAIN_TRIGGERS)

def read_file(path):
    expanded = os.path.expanduser(path)
    if os.path.exists(expanded):
        with open(expanded) as f:
            return f.read()
    return None

def match_capture(text):
    text_lower = text.lower()
    return any(t in text_lower for t in CAPTURE_TRIGGERS)

def main():
    try:
        input_data = json.loads(sys.stdin.read())
        prompt = input_data.get('prompt', '')
    except Exception:
        sys.exit(0)

    if not prompt:
        sys.exit(0)

    # Capture trigger takes priority — session-end detected
    if match_capture(prompt):
        capture = read_file('~/Documents/alecs-echosystem/projects/learning-loop/protocol/capture.md')
        pending = read_file('~/Documents/alecs-echosystem/projects/learning-loop/discussions/pending.md')
        parts = []
        if capture:
            parts.append(f"CAPTURE PROTOCOL — run this now:\n{capture}")
        if pending:
            parts.append(f"CURRENT PENDING ENTRIES:\n{pending}")
        if parts:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": "\n\n".join(parts)
                }
            }
            print(json.dumps(output))
        sys.exit(0)

    project = match_project(prompt)

    if project:
        path = PROJECT_MAP.get(project)
        content = read_file(path) if path else None
        if content:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": f"PROJECT CONTEXT — {project.upper()}:\n{content}"
                }
            }
            print(json.dumps(output))
        sys.exit(0)

    if match_brain(prompt):
        content = read_file('~/Documents/alecs-echosystem/brain/constraints/constraints.md')
        if content:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": f"BRAIN — CONSTRAINTS:\n{content}"
                }
            }
            print(json.dumps(output))

if __name__ == '__main__':
    main()
