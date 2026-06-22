#!/usr/bin/env python3
# Harness: persistence -- remembering across the session boundary.
"""
s09_memory_system.py - Memory System
<<<<<<< HEAD
This teaching version focuses on one core idea:
some information should survive the current conversation, but not everything
belongs in memory.
=======

This teaching version focuses on one core idea:
some information should survive the current conversation, but not everything
belongs in memory.

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
Use memory for:
  - user preferences
  - repeated user feedback
  - project facts that are NOT obvious from the current code
  - pointers to external resources
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
Do NOT use memory for:
  - code structure that can be re-read from the repo
  - temporary task state
  - secrets
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
Storage layout:
  .memory/
    MEMORY.md
    prefer_tabs.md
    review_style.md
    incident_board.md
<<<<<<< HEAD
Each memory is a small Markdown file with frontmatter.
The agent can save a memory through save_memory(), and the memory index
is rebuilt after each write.
An optional "Dream" pass can later consolidate, deduplicate, and prune
stored memories. It is useful, but it is not the first thing readers need
to understand.
=======

Each memory is a small Markdown file with frontmatter.
The agent can save a memory through save_memory(), and the memory index
is rebuilt after each write.

An optional "Dream" pass can later consolidate, deduplicate, and prune
stored memories. It is useful, but it is not the first thing readers need
to understand.

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
Key insight: "Memory only stores cross-session information that is still
worth recalling later and is not easy to re-derive from the current repo."
"""

import json
import os
import re
import subprocess
from pathlib import Path
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv(override=True)

if os.getenv("ANTHROPIC_BASE_URL"):
    os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)

WORKDIR = Path.cwd()
<<<<<<< HEAD

client = Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"))

MODEL = os.environ["MODEL_ID"]

MEMORY_DIR = WORKDIR / ".memory"

MEMORY_INDEX = MEMORY_DIR / "MEMORY.md"

MEMORY_TYPES = ("user", "feedback", "project", "reference")

MAX_INDEX_LINES = 200

class MemoryManager:
    """
    Load, build, and save persistent memories across sessions.
    The teaching version keeps memory explicit:
    one Markdown file per memory, plus one compact index file.
    """
=======
client = Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"))
MODEL = os.environ["MODEL_ID"]

MEMORY_DIR = WORKDIR / ".memory"
MEMORY_INDEX = MEMORY_DIR / "MEMORY.md"
MEMORY_TYPES = ("user", "feedback", "project", "reference")
MAX_INDEX_LINES = 200


class MemoryManager:
    """
    Load, build, and save persistent memories across sessions.

    The teaching version keeps memory explicit:
    one Markdown file per memory, plus one compact index file.
    """

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
    def __init__(self, memory_dir: Path = None):
        self.memory_dir = memory_dir or MEMORY_DIR
        self.memories = {}  # name -> {description, type, content}

    def load_all(self):
        """Load MEMORY.md index and all individual memory files."""
        self.memories = {}
        if not self.memory_dir.exists():
            return
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        # Scan all .md files except MEMORY.md
        for md_file in sorted(self.memory_dir.glob("*.md")):
            if md_file.name == "MEMORY.md":
                continue
            parsed = self._parse_frontmatter(md_file.read_text())
            if parsed:
                name = parsed.get("name", md_file.stem)
                self.memories[name] = {
                    "description": parsed.get("description", ""),
                    "type": parsed.get("type", "project"),
                    "content": parsed.get("content", ""),
                    "file": md_file.name,
                }
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        count = len(self.memories)
        if count > 0:
            print(f"[Memory loaded: {count} memories from {self.memory_dir}]")

    def load_memory_prompt(self) -> str:
        """Build a memory section for injection into the system prompt."""
        if not self.memories:
            return ""
<<<<<<< HEAD
        sections = []
        sections.append("# Memories (persistent across sessions)")
        sections.append("")
=======

        sections = []
        sections.append("# Memories (persistent across sessions)")
        sections.append("")

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        # Group by type for readability
        for mem_type in MEMORY_TYPES:
            typed = {k: v for k, v in self.memories.items() if v["type"] == mem_type}
            if not typed:
                continue
            sections.append(f"## [{mem_type}]")
            for name, mem in typed.items():
                sections.append(f"### {name}: {mem['description']}")
                if mem["content"].strip():
                    sections.append(mem["content"].strip())
                sections.append("")
<<<<<<< HEAD
        return "\n".join(sections)
    
    def save_memory(self, name: str, description: str, mem_type: str, content: str) -> str:
        """
        Save a memory to disk and update the index.
=======

        return "\n".join(sections)

    def save_memory(self, name: str, description: str, mem_type: str, content: str) -> str:
        """
        Save a memory to disk and update the index.

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        Returns a status message.
        """
        if mem_type not in MEMORY_TYPES:
            return f"Error: type must be one of {MEMORY_TYPES}"
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        # Sanitize name for filename
        safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", name.lower())
        if not safe_name:
            return "Error: invalid memory name"
<<<<<<< HEAD
        self.memory_dir.mkdir(parents=True, exist_ok=True)
=======

        self.memory_dir.mkdir(parents=True, exist_ok=True)

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        # Write individual memory file with frontmatter
        frontmatter = (
            f"---\n"
            f"name: {name}\n"
            f"description: {description}\n"
            f"type: {mem_type}\n"
            f"---\n"
            f"{content}\n"
        )
        file_name = f"{safe_name}.md"
        file_path = self.memory_dir / file_name
        file_path.write_text(frontmatter)
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        # Update in-memory store
        self.memories[name] = {
            "description": description,
            "type": mem_type,
            "content": content,
            "file": file_name,
        }
<<<<<<< HEAD
        # Rebuild MEMORY.md index
        self._rebuild_index()
        return f"Saved memory '{name}' [{mem_type}] to {file_path.relative_to(WORKDIR)}"
    
=======

        # Rebuild MEMORY.md index
        self._rebuild_index()

        return f"Saved memory '{name}' [{mem_type}] to {file_path.relative_to(WORKDIR)}"

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
    def _rebuild_index(self):
        """Rebuild MEMORY.md from current in-memory state, capped at 200 lines."""
        lines = ["# Memory Index", ""]
        for name, mem in self.memories.items():
            lines.append(f"- {name}: {mem['description']} [{mem['type']}]")
            if len(lines) >= MAX_INDEX_LINES:
                lines.append(f"... (truncated at {MAX_INDEX_LINES} lines)")
                break
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        MEMORY_INDEX.write_text("\n".join(lines) + "\n")

    def _parse_frontmatter(self, text: str) -> dict | None:
<<<<<<< HEAD
        """解析由 --- 分隔的 frontmatter 和正文内容。"""
        # 匹配文件开头的 frontmatter，并把后续内容作为正文。
=======
        """Parse --- delimited frontmatter + body content."""
>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
        if not match:
            return None
        header, body = match.group(1), match.group(2)
        result = {"content": body.strip()}
<<<<<<< HEAD
        # 将 frontmatter 中的 key: value 行解析到结果字典中。
=======
>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        for line in header.splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                result[key.strip()] = value.strip()
        return result
<<<<<<< HEAD
    
class DreamConsolidator:
    """
    Auto-consolidation of memories between sessions ("Dream").
=======


class DreamConsolidator:
    """
    Auto-consolidation of memories between sessions ("Dream").

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
    This is an optional later-stage feature. Its job is to prevent the memory
    store from growing into a noisy pile by merging, deduplicating, and
    pruning entries over time.
    """
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
    COOLDOWN_SECONDS = 86400       # 24 hours between consolidations
    SCAN_THROTTLE_SECONDS = 600    # 10 minutes between scan attempts
    MIN_SESSION_COUNT = 5          # need enough data to consolidate
    LOCK_STALE_SECONDS = 3600      # PID lock considered stale after 1 hour
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
    PHASES = [
        "Orient: scan MEMORY.md index for structure and categories",
        "Gather: read individual memory files for full content",
        "Consolidate: merge related memories, remove stale entries",
        "Prune: enforce 200-line limit on MEMORY.md index",
    ]
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
    def __init__(self, memory_dir: Path = None):
        self.memory_dir = memory_dir or MEMORY_DIR
        self.lock_file = self.memory_dir / ".dream_lock"
        self.enabled = True
        self.mode = "default"
        self.last_consolidation_time = 0.0
        self.last_scan_time = 0.0
        self.session_count = 0
<<<<<<< HEAD
        
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
    def should_consolidate(self) -> tuple[bool, str]:
        """
        Check 7 gates in sequence. All must pass.
        Returns (can_run, reason) where reason explains the first failed gate.
        """
        import time
<<<<<<< HEAD
        now = time.time()
        # Gate 1: enabled flag
        if not self.enabled:
            return False, "Gate 1: consolidation is disabled"
=======

        now = time.time()

        # Gate 1: enabled flag
        if not self.enabled:
            return False, "Gate 1: consolidation is disabled"

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        # Gate 2: memory directory exists and has memory files
        if not self.memory_dir.exists():
            return False, "Gate 2: memory directory does not exist"
        memory_files = list(self.memory_dir.glob("*.md"))
        # Exclude MEMORY.md itself from the count
        memory_files = [f for f in memory_files if f.name != "MEMORY.md"]
        if not memory_files:
            return False, "Gate 2: no memory files found"
<<<<<<< HEAD
        # Gate 3: not in plan mode (only consolidate in active modes)
        if self.mode == "plan":
            return False, "Gate 3: plan mode does not allow consolidation"
=======

        # Gate 3: not in plan mode (only consolidate in active modes)
        if self.mode == "plan":
            return False, "Gate 3: plan mode does not allow consolidation"

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        # Gate 4: 24-hour cooldown since last consolidation
        time_since_last = now - self.last_consolidation_time
        if time_since_last < self.COOLDOWN_SECONDS:
            remaining = int(self.COOLDOWN_SECONDS - time_since_last)
            return False, f"Gate 4: cooldown active, {remaining}s remaining"
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        # Gate 5: 10-minute throttle since last scan attempt
        time_since_scan = now - self.last_scan_time
        if time_since_scan < self.SCAN_THROTTLE_SECONDS:
            remaining = int(self.SCAN_THROTTLE_SECONDS - time_since_scan)
            return False, f"Gate 5: scan throttle active, {remaining}s remaining"
<<<<<<< HEAD
        # Gate 6: need at least 5 sessions worth of data
        if self.session_count < self.MIN_SESSION_COUNT:
            return False, f"Gate 6: only {self.session_count} sessions, need {self.MIN_SESSION_COUNT}"
        # Gate 7: no active lock file (check PID staleness)
        if not self._acquire_lock():
            return False, "Gate 7: lock held by another process"
        return True, "All 7 gates passed"
    
    def consolidate(self) -> list[str]:
        """
        Run the 4-phase consolidation process.
=======

        # Gate 6: need at least 5 sessions worth of data
        if self.session_count < self.MIN_SESSION_COUNT:
            return False, f"Gate 6: only {self.session_count} sessions, need {self.MIN_SESSION_COUNT}"

        # Gate 7: no active lock file (check PID staleness)
        if not self._acquire_lock():
            return False, "Gate 7: lock held by another process"

        return True, "All 7 gates passed"

    def consolidate(self) -> list[str]:
        """
        Run the 4-phase consolidation process.

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        The teaching version returns phase descriptions to make the flow
        visible without requiring an extra LLM pass here.
        """
        import time
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        can_run, reason = self.should_consolidate()
        if not can_run:
            print(f"[Dream] Cannot consolidate: {reason}")
            return []
<<<<<<< HEAD
        print("[Dream] Starting consolidation...")
        self.last_scan_time = time.time()
=======

        print("[Dream] Starting consolidation...")
        self.last_scan_time = time.time()

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        completed_phases = []
        for i, phase in enumerate(self.PHASES, 1):
            print(f"[Dream] Phase {i}/4: {phase}")
            completed_phases.append(phase)
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        self.last_consolidation_time = time.time()
        self._release_lock()
        print(f"[Dream] Consolidation complete: {len(completed_phases)} phases executed")
        return completed_phases
<<<<<<< HEAD
    
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
    def _acquire_lock(self) -> bool:
        """
        Acquire a PID-based lock file. Returns False if locked by another
        live process. Stale locks (older than LOCK_STALE_SECONDS) are removed.
        """
        import time
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        if self.lock_file.exists():
            try:
                lock_data = self.lock_file.read_text().strip()
                pid_str, timestamp_str = lock_data.split(":", 1)
                pid = int(pid_str)
                lock_time = float(timestamp_str)
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
                # Check if lock is stale
                if (time.time() - lock_time) > self.LOCK_STALE_SECONDS:
                    print(f"[Dream] Removing stale lock from PID {pid}")
                    self.lock_file.unlink()
                else:
                    # Check if owning process is still alive
                    try:
                        os.kill(pid, 0)
                        return False  # process alive, lock is valid
                    except OSError:
                        print(f"[Dream] Removing lock from dead PID {pid}")
                        self.lock_file.unlink()
            except (ValueError, OSError):
                # Corrupted lock file, remove it
                self.lock_file.unlink(missing_ok=True)
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        # Write new lock
        try:
            self.memory_dir.mkdir(parents=True, exist_ok=True)
            self.lock_file.write_text(f"{os.getpid()}:{time.time()}")
            return True
        except OSError:
            return False
<<<<<<< HEAD
    
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
    def _release_lock(self):
        """Release the lock file if we own it."""
        try:
            if self.lock_file.exists():
                lock_data = self.lock_file.read_text().strip()
                pid_str = lock_data.split(":")[0]
                if int(pid_str) == os.getpid():
                    self.lock_file.unlink()
        except (ValueError, OSError):
            pass


# -- Tool implementations --
def safe_path(p: str) -> Path:
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"Path escapes workspace: {p}")
    return path

<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
def run_bash(command: str) -> str:
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        r = subprocess.run(command, shell=True, cwd=WORKDIR,
                           capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"
<<<<<<< HEAD
    
=======


>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
def run_read(path: str, limit: int = None) -> str:
    try:
        lines = safe_path(path).read_text().splitlines()
        if limit and limit < len(lines):
            lines = lines[:limit] + [f"... ({len(lines) - limit} more)"]
        return "\n".join(lines)[:50000]
    except Exception as e:
        return f"Error: {e}"
<<<<<<< HEAD
    
=======


>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
def run_write(path: str, content: str) -> str:
    try:
        fp = safe_path(path)
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content)
        return f"Wrote {len(content)} bytes"
    except Exception as e:
        return f"Error: {e}"
<<<<<<< HEAD
    
=======


>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
def run_edit(path: str, old_text: str, new_text: str) -> str:
    try:
        fp = safe_path(path)
        content = fp.read_text()
        if old_text not in content:
            return f"Error: Text not found in {path}"
        fp.write_text(content.replace(old_text, new_text, 1))
        return f"Edited {path}"
    except Exception as e:
        return f"Error: {e}"

<<<<<<< HEAD
# Global memory manager
memory_mgr = MemoryManager()

def run_save_memory(name: str, description: str, mem_type: str, content: str) -> str:
    return memory_mgr.save_memory(name, description, mem_type, content)

=======

# Global memory manager
memory_mgr = MemoryManager()


def run_save_memory(name: str, description: str, mem_type: str, content: str) -> str:
    return memory_mgr.save_memory(name, description, mem_type, content)


>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
TOOL_HANDLERS = {
    "bash":         lambda **kw: run_bash(kw["command"]),
    "read_file":    lambda **kw: run_read(kw["path"], kw.get("limit")),
    "write_file":   lambda **kw: run_write(kw["path"], kw["content"]),
    "edit_file":    lambda **kw: run_edit(kw["path"], kw["old_text"], kw["new_text"]),
    "save_memory":  lambda **kw: run_save_memory(kw["name"], kw["description"], kw["type"], kw["content"]),
}
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
TOOLS = [
    {"name": "bash", "description": "Run a shell command.",
     "input_schema": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}},
    {"name": "read_file", "description": "Read file contents.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "limit": {"type": "integer"}}, "required": ["path"]}},
    {"name": "write_file", "description": "Write content to file.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}},
    {"name": "edit_file", "description": "Replace exact text in file.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "old_text": {"type": "string"}, "new_text": {"type": "string"}}, "required": ["path", "old_text", "new_text"]}},
    {"name": "save_memory", "description": "Save a persistent memory that survives across sessions.",
     "input_schema": {"type": "object", "properties": {
         "name": {"type": "string", "description": "Short identifier (e.g. prefer_tabs, db_schema)"},
         "description": {"type": "string", "description": "One-line summary of what this memory captures"},
         "type": {"type": "string", "enum": ["user", "feedback", "project", "reference"],
                  "description": "user=preferences, feedback=corrections, project=non-obvious project conventions or decision reasons, reference=external resource pointers"},
         "content": {"type": "string", "description": "Full memory content (multi-line OK)"},
     }, "required": ["name", "description", "type", "content"]}},
]

<<<<<<< HEAD

=======
>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
MEMORY_GUIDANCE = """
When to save memories:
- User states a preference ("I like tabs", "always use pytest") -> type: user
- User corrects you ("don't do X", "that was wrong because...") -> type: feedback
- You learn a project fact that is not easy to infer from current code alone
  (for example: a rule exists because of compliance, or a legacy module must
  stay untouched for business reasons) -> type: project
- You learn where an external resource lives (ticket board, dashboard, docs URL)
  -> type: reference
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
When NOT to save:
- Anything easily derivable from code (function signatures, file structure, directory layout)
- Temporary task state (current branch, open PR numbers, current TODOs)
- Secrets or credentials (API keys, passwords)
"""

<<<<<<< HEAD
def build_system_prompt() -> str:
    """Assemble system prompt with memory content included."""
    parts = [f"You are a coding agent at {WORKDIR}. Use tools to solve tasks."]
=======

def build_system_prompt() -> str:
    """Assemble system prompt with memory content included."""
    parts = [f"You are a coding agent at {WORKDIR}. Use tools to solve tasks."]

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
    # Inject memory content if available
    memory_section = memory_mgr.load_memory_prompt()
    if memory_section:
        parts.append(memory_section)
<<<<<<< HEAD
    parts.append(MEMORY_GUIDANCE)
    return "\n\n".join(parts)

def agent_loop(messages: list):
    """
    Agent loop with memory-aware system prompt.
=======

    parts.append(MEMORY_GUIDANCE)
    return "\n\n".join(parts)


def agent_loop(messages: list):
    """
    Agent loop with memory-aware system prompt.

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
    The system prompt is rebuilt each call so newly saved memories
    are visible in the next LLM turn within the same session.
    """
    while True:
        system = build_system_prompt()
        response = client.messages.create(
            model=MODEL, system=system, messages=messages,
            tools=TOOLS, max_tokens=8000,
        )
        messages.append({"role": "assistant", "content": response.content})
<<<<<<< HEAD
        if response.stop_reason != "tool_use":
            return
=======

        if response.stop_reason != "tool_use":
            return

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            handler = TOOL_HANDLERS.get(block.name)
            try:
                output = handler(**(block.input or {})) if handler else f"Unknown: {block.name}"
            except Exception as e:
                output = f"Error: {e}"
            print(f"> {block.name}: {str(output)[:200]}")
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(output),
            })
<<<<<<< HEAD
        messages.append({"role": "user", "content": results})

=======

        messages.append({"role": "user", "content": results})


>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
if __name__ == "__main__":
    # Load existing memories at session start
    memory_mgr.load_all()
    mem_count = len(memory_mgr.memories)
    if mem_count:
        print(f"[{mem_count} memories loaded into context]")
    else:
        print("[No existing memories. The agent can create them with save_memory.]")
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
    history = []
    while True:
        try:
            query = input("\033[36ms09 >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() in ("q", "exit", ""):
            break
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        # /memories command to list current memories
        if query.strip() == "/memories":
            if memory_mgr.memories:
                for name, mem in memory_mgr.memories.items():
                    print(f"  [{mem['type']}] {name}: {mem['description']}")
            else:
                print("  (no memories)")
            continue
<<<<<<< HEAD
=======

>>>>>>> 5dfe67f4bd2a807e257351a14996b5ca58777969
        history.append({"role": "user", "content": query})
        agent_loop(history)
        response_content = history[-1]["content"]
        if isinstance(response_content, list):
            for block in response_content:
                if hasattr(block, "text"):
                    print(block.text)
        print()
