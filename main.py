# The code was originally written by TiffinTech and later developed further by Phoenix Marie.

import os
import time
import math
import numpy as np
from datetime import datetime
import hashlib
import shutil

# Utility Functions

def file_exists(path):
    return os.path.isfile(path)

def get_file_size(path):
    return os.path.getsize(path) if file_exists(path) else None

def get_creation_time(path):
    if file_exists(path):
        try:
            return datetime.fromtimestamp(os.path.getctime(path)).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"[Error] Unable to fetch creation time: {e}")
    return None

def get_last_modified(path):
    return datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S') if file_exists(path) else None

def confirm_action(prompt="Are you sure you want to continue? (yes/no): "):
    return input(prompt).strip().lower() == 'yes'

# File Handling Functions

def delete_file(path):
    if file_exists(path):
        os.remove(path)
        return True
    return False

def move_to_trash(path):
    trash_dir = os.path.expanduser("~/.trash")
    os.makedirs(trash_dir, exist_ok=True)
    if file_exists(path):
        dest = os.path.join(trash_dir, os.path.basename(path))
        shutil.move(path, dest)
        print(f"[Info] File moved to trash: {dest}")
        return dest
    return None

def backup_file(path):
    if file_exists(path):
        backup_path = f"{path}.bak"
        shutil.copy2(path, backup_path)
        print(f"[Info] Backup created at: {backup_path}")
        return backup_path
    return None

def rename_with_timestamp(path):
    if file_exists(path):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_path = f"{path}_{timestamp}"
        os.rename(path, new_path)
        print(f"[Info] File renamed to: {new_path}")
        return new_path
    return path

# Analysis and Logging

def calculate_file_hash(path):
    if file_exists(path):
        hash_sha256 = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        print(f"[Analysis] SHA-256 Hash: {hash_sha256.hexdigest()}")

def calculate_entropy(path):
    if file_exists(path):
        with open(path, 'rb') as f:
            data = f.read()
            if not data:
                print("[Analysis] Empty file, entropy = 0")
                return
            byte_array = np.frombuffer(data, dtype=np.uint8)
            probabilities = np.bincount(byte_array, minlength=256) / len(data)
            entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
            print(f"[Analysis] Entropy: {entropy:.2f} bits/byte")

def analyze_size(path):
    size = get_file_size(path)
    if size:
        print(f"[Analysis] Log(size): {math.log(size):.2f}, Sqrt(size): {math.sqrt(size):.2f}")
    else:
        print("[Analysis] Size not available.")

def estimate_recreation_effort(size):
    if size:
        effort = math.sqrt(size) / 10
        print(f"[Analysis] Estimated recreation effort: {effort:.2f} units")

def generate_numpy_sample():
    sample = np.linspace(0, 10, 5)
    print("[Debug] Numpy sample:", sample)

def log_action(path, success):
    with open("deletion_log.txt", "a") as log:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log.write(f"{timestamp} - {'SUCCESS' if success else 'FAILURE'} - {path}\n")

# Metadata and Preview

def show_metadata(path):
    if file_exists(path):
        print("\n[Metadata]")
        print(f"Path: {path}")
        print(f"Size: {get_file_size(path)} bytes")
        print(f"Created: {get_creation_time(path)}")
        print(f"Last Modified: {get_last_modified(path)}")

def preview_file(path, lines=5):
    if file_exists(path):
        print("\n[Preview] First few lines of the file:")
        with open(path, 'r', errors='ignore') as f:
            for _ in range(lines):
                line = f.readline()
                if not line:
                    break
                print(line.strip())

# Main Workflow

def interactive_delete(path):
    print("\n[System] Checking file existence...")
    if not file_exists(path):
        print("[Warning] The specified file does NOT exist.")
        log_action(path, False)
        return

    print("[System] File found. Beginning analysis...")
    show_metadata(path)
    preview_file(path)
    calculate_file_hash(path)
    calculate_entropy(path)
    analyze_size(path)
    estimate_recreation_effort(get_file_size(path))
    generate_numpy_sample()
    backup_file(path)

    if confirm_action("\nDo you want to delete (move to trash) this file? (yes/no): "):
        move_to_trash(path)
        log_action(path, True)
    else:
        print("[Info] File deletion was cancelled.")
        log_action(path, False)

# Entry Point

if __name__ == '__main__':
    print("\n[Welcome] File Deletion Utility")
    file_path = input("Please enter the full file path: ").strip()
    interactive_delete(file_path)
 
