#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '..', 'config.json');
const config = fs.existsSync(CONFIG_FILE) ? JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8')) : {};
const STATE_FILE = config.state_file || path.join(__dirname, '..', 'session-state.md');
const BRAIN_PATH = config.brain_path || null;
const CLASSIFICATION_PROMPT = config.classification_prompt || null;

function readState(content) {
  const state = {};
  for (const line of content.split('\n')) {
    const match = line.match(/^(\w+):\s*(.*)$/);
    if (match) state[match[1]] = match[2].trim();
  }
  return state;
}

function writeState(state) {
  const lines = [
    '# Session State',
    '',
    '> Written and read by the stateful classifier. Updated every turn.',
    '> Do not edit manually. The classifier owns this file.',
    '',
    '---',
    '',
    `session_id: ${state.session_id || ''}`,
    `current_topic: ${state.current_topic || ''}`,
    `topic_start_index: ${state.topic_start_index || ''}`,
    `current_message_index: ${state.current_message_index || ''}`,
    `adjacent_counter: ${state.adjacent_counter || ''}`,
  ];
  fs.writeFileSync(STATE_FILE, lines.join('\n'));
}

try {
  if (!fs.existsSync(STATE_FILE)) {
    process.exit(0);
  }

  const content = fs.readFileSync(STATE_FILE, 'utf8');
  const state = readState(content);

  if (!state.current_topic) {
    process.exit(0);
  }

  state.current_message_index = String(parseInt(state.current_message_index || '0') + 1);

  writeState(state);

  const classificationPrompt = CLASSIFICATION_PROMPT && fs.existsSync(CLASSIFICATION_PROMPT)
    ? '\n\nCLASSIFICATION PROMPT — active:\n' + fs.readFileSync(CLASSIFICATION_PROMPT, 'utf8')
    : '';

  const context = [
    'DRIFT CHECK — run before responding:',
    `Current topic: ${state.current_topic}`,
    `Message index: ${state.current_message_index}`,
    `Adjacent counter: ${state.adjacent_counter || '0'} / 3`,
    '',
    'Steps:',
    '1. Is this message consistent with the current topic? → proceed, no change.',
    '2. Is it adjacent (related but not primary)? → reply normally, then update adjacent_counter +1 in session-state.md.',
    '3. Has the topic clearly shifted? → drift confirmed. Notify: "This is moving toward [topic]. New session?" Then update session-state.md.',
    '',
    `Eviction pointer if drift confirmed: ${state.session_id}:${state.topic_start_index}:${state.current_message_index}`,
    classificationPrompt,
  ].join('\n');

  const output = {
    hookSpecificOutput: {
      hookEventName: 'UserPromptSubmit',
      additionalContext: context,
    },
  };

  process.stdout.write(JSON.stringify(output));
} catch (e) {
  process.exit(0);
}
