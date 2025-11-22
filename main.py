# Secure File Deletion Utility
# Originally by TiffinTech | Significantly enhanced and fully corrected

import os
import math
import hashlib
import shutil
import platform
from datetime import datetime
from typing import Optional

import numpy as np


# ==================== Utility Functions ====================

def file_exists(path: str) -> bool:
    """Safely check if path exists and is a regular file."""
    try:
        return os.path.isfile(path)
    except (OSError, TypeError, ValueError):
        return False


def get_file_size(path: str) -> Optional[int]:
    """Return file size in bytes or None if inaccessible."""
    if not file_exists(path):
        return None
    try:
        return os.path.getsize(path)
    except OSError:
        return None


def get_creation_time(path: str) -> Optional[str]:
    """Return file creation/birth time as formatted string (best effort, cross-platform)."""
    if not file_exists(path):
        return None
    try:
        stat = os.stat(path)
        if platform.system() == "Windows":
            timestamp = stat.st_ctime
        else:
            # macOS: st_birthtime | Linux: may not have birth time → fall back to mtime
            try:
                timestamp = stat.st_birthtime
            except AttributeError:
                timestamp = stat.st_mtime
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"[Error] Failed to get creation time: {e}")
        return None


def get_last_modified(path: str) -> Optional[str]:
    """Return last modified time as formatted string."""
    if not file_exists(path):
        return None
    try:
        timestamp = os.path.getmtime(path)
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def confirm_action(prompt: str = "Are you sure? (yes/no): ") -> bool:
    """Robust yes/no input with flexible affirmation."""
    while True:
        response = input(prompt).strip().lower()
        if response in {"yes", "y", "ye"}:
            return True
        if response in {"no", "n"}:
            return False
        print("Please respond with 'yes' or 'no'.")


# ==================== File Operations ====================

def move_to_trash(path: str) -> Optional[str]:
    """Move file to ~/.trash with unique naming to prevent collisions."""
    trash_dir = os.path.expanduser("~/.trash")
    os.makedirs(trash_dir, exist_ok=True)

    if not file_exists(path):
        print("[Error] Cannot move: source file no longer exists.")
        return None

    base_name = os.path.basename(path)
    name, ext = os.path.splitext(base_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    counter = 0
    dest_path = os.path.join(trash_dir, f"{name}_{timestamp}{ext}")
    while os.path.exists(dest_path):
        counter += 1
        dest_path = os.path.join(trash_dir, f"{name}_{timestamp}_{counter}{ext}")

    try:
        shutil.move(path, dest_path)
        abs_dest = os.path.abspath(dest_path)
        print(f"[Success] File moved to trash: {abs_dest}")
        return abs_dest
    except Exception as e:
        print(f"[Error] Failed to move file to trash: {e}")
        return None


def backup_file(path: str) -> Optional[str]:
    """Create a timestamped backup with .bak extension."""
    if not file_exists(path):
        return None

    dir_name = os.path.dirname(path) or "."
    base_name = os.path.basename(path)
    name, ext = os.path.splitext(base_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{name}_{timestamp}{ext}.bak"
    backup_path = os.path.join(dir_name, backup_name)

    counter = 1
    original = backup_path
    while os.path.exists(backup_path):
        backup_path = os.path.join(dir_name, f"{name}_{timestamp}_{counter}{ext}.bak")
        counter += 1

    try:
        shutil.copy2(path, backup_path)
        print(f"[Info] Backup created: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"[Error] Backup failed: {e}")
        return original if os.path.exists(original) else None


# ==================== Analysis Functions ====================

def calculate_file_hash(path: str) -> None:
    """Compute and display SHA-256 hash."""
    if not file_exists(path):
        return
    hash_obj = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(131072), b""):  # 128 KB chunks
                hash_obj.update(chunk)
        print(f"[Hash] SHA-256: {hash_obj.hexdigest()}")
    except Exception as e:
        print(f"[Error] Hash computation failed: {e}")


def calculate_entropy(path: str) -> None:
    """Calculate Shannon entropy of file bytes."""
    if not file_exists(path):
        return
    try:
        with open(path, "rb") as f:
            data = f.read()
        if not data:
            print("[Analysis] Entropy: 0.0000 bits/byte (empty file)")
            return

        counts = np.bincount(np.frombuffer(data, dtype=np.uint8), minlength=256)
        probabilities = counts / len(data)
        probabilities = probabilities[probabilities > 0]
        entropy = -np.sum(probabilities * np.log2(probabilities))
        print(f"[Analysis] Entropy: {entropy:.4f} bits/byte (max possible: 8.0000)")
    except Exception as e:
        print(f"[Error] Entropy calculation failed: {e}")


def analyze_size(path: str) -> None:
    size = get_file_size(path)
    if size is None:
        print("[Analysis] Size: Unknown")
    elif size == 0:
        print("[Analysis] Size: 0 bytes (empty file)")
    else:
        log2_size = math.log2(size) if size > 0 else 0
        print(f"[Analysis] Size: {size:,} bytes | log₂(size): {log2_size:.2f} | √(size): {math.sqrt(size):.2f}")


def estimate_recreation_effort(size: Optional[int]) -> None:
    if not size or size <= 0:
        print("[Analysis] Estimated recreation effort: Unknown or zero")
        return
    effort = math.sqrt(size) / 10
    print(f"[Analysis] Estimated recreation effort: {effort:,.1f} arbitrary units")


# ==================== Logging & Display ====================

def log_action(path: str, action: str, success: bool) -> None:
    log_file = "deletion_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "FAILURE"
    line = f"{timestamp} | {status:7} | {action:15} | {path}\n"
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as e:
        print(f"[Warning] Could not write to log: {e}")


def show_metadata(path: str) -> None:
    print("\n" + "═" * 60)
    print(" FILE METADATA")
    print("═" * 60)
    print(f"Path           : {path}")
    print(f"Size           : {get_file_size(path):,} bytes" if get_file_size(path) is not None else "Size           : Unknown")
    print(f"Created        : {get_creation_time(path) or 'Unknown'}")
    print(f"Last Modified  : {get_last_modified(path) or 'Unknown'}")
    print("═" * 60)


def preview_file(path: str, lines: int = 5) -> None:
    if not file_exists(path):
        return
    print(f"\n[Preview] First {lines} lines (text preview only):")
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            displayed = 0
            for line in f:
                if displayed >= lines:
                    break
                print(f"  {displayed+1:02d}: {line.rstrip()}")
                displayed += 1
            if displayed == 0:
                print("  <File appears empty or contains only null bytes>")
    except UnicodeDecodeError:
        print("  <Binary file – text preview not available>")
    except Exception:
        print("  <Unable to preview file>")


# ==================== Main Workflow ====================

def interactive_delete(input_path: str) -> None:
    path = os.path.expanduser(input_path.strip().strip("\"'"))
    
    print("\n[System] Secure File Deletion Assistant Initialized")
    
    if not file_exists(path):
        print(f"[Error] File not found or inaccessible: {path}")
        log_action(path, "NOT_FOUND", False)
        return

    show_metadata(path)
    preview_file(path)
    calculate_file_hash(path)
    calculate_entropy(path)
    analyze_size(path)
    estimate_recreation_effort(get_file_size(path))

    print("\n[Backup] Creating automatic safety backup...")
    backup_path = backup_file(path)
    if backup_path:
        log_action(path, "BACKUP_CREATED", True)

    print("\n" + "!" * 70)
    print("!!! WARNING: This will move the file to ~/.trash (recoverable)")
    print("!" * 70)

    if confirm_action("\nDo you wish to proceed with moving this file to trash? (yes/no): "):
        dest = move_to_trash(path)
        success = dest is not None
        log_action(path, "MOVED_TO_TRASH", success)
        if success:
            print(f"\n[Success] File has been safely moved to trash.")
        else:
            print(f"\n[Failure] Failed to move file.")
    else:
        print("\n[Info] Operation cancelled by user.")
        log_action(path, "CANCELLED", True)


# ==================== Entry Point ====================

if __name__ == "__main__":
    print("═" * 70)
    print("   SECURE FILE DELETION UTILITY – SAFE MODE")
    print("   Files are moved to ~/.trash • Never permanently deleted")
    print("═" * 70)

    user_input = input("\nEnter the full path to the file: ").strip()
    
    if not user_input:
        print("[Error] No file path provided.")
    else:
        interactive_delete(user_input)
