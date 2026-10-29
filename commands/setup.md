---
name: setup
description: Create your Off My Plate workspace (default ~/plate, never inside a project repo) and answer the three questions that size every Plate.
argument-hint: '[optional workspace path]'
---

Set up the Off My Plate workspace.

1. Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/init_workspace.py" $ARGUMENTS` (if the variable is unset, the plugin root is the directory above `commands/`). It creates the workspace at `~/plate` unless a path or `$OFF_MY_PLATE_DIR` says otherwise, never overwrites an existing file, and adds the folder to `.gitignore` if it sits inside a git repo. Show its output.
2. If the workspace is new, or `config.md` still has blank ★ lines, ask the three ★ questions in ONE message: waking window and real work hours on a good and a bad day; life anchors with rough times; the buckets the work is for. Offer to skip any of them; a skipped answer becomes a labeled ASSUMED default.
3. Write the answers into `config.md` (show the change first). Fill nothing the human did not say.
4. End with one line: the next command to run, which is `/plate`.

Ask nothing else. Do not read mail or calendar here.
