# Secure File Deletion Utility — Safe Mode  
**A paranoid, user-friendly, and fully auditable file “deletion” tool**

```text
GitHub: https://github.com/your-username/secure-delete-utility
Language: Python 3.8+
License: MIT
```

## Overview

The **Secure File Deletion Utility** is a safety-first command-line tool that never permanently deletes a file without explicit safeguards. Instead of calling `os.remove()`, it:

- Displays detailed metadata, text preview, SHA-256 hash, and Shannon entropy  
- Performs automatic timestamped backup in the original directory  
- Moves the file to a dedicated `~/.trash` folder with a collision-proof name  
- Logs every action to `deletion_log.txt` for audit purposes  
- Requires explicit user confirmation before any move occurs  

Designed for security-conscious developers, system administrators, forensic analysts, and anyone who has ever regretted an accidental deletion.

## Features

- Cross-platform (Windows, macOS, Linux)  
- Robust path handling (`~` expansion, quoted paths)  
- Unique backup & trash filenames (timestamp + counter)  
- Forensic-grade analysis (hash, entropy, size metrics)  
- Comprehensive UTF-8 logging with timestamps  
- Graceful error handling and user feedback  
- No external dependencies beyond standard library + NumPy  

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/secure-delete-utility.git
cd secure-delete-utility

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
# .\venv\Scripts\activate  # Windows

# Install dependency
pip install numpy
```

## Usage

```bash
python secure_delete.py
```

You will be prompted to enter the full path of the file. The tool will then:

1. Analyze and display file information  
2. Create a backup copy (`filename_YYYYMMDD_HHMMSS.ext.bak`)  
3. Ask for final confirmation  
4. On approval, move the file to `~/.trash` (recoverable)  

Files in `~/.trash` can be restored manually or with a future recovery script.

## Example Output

```text
Enter the full path to the file: /home/user/confidential.docx

[System] Secure File Deletion Assistant Initialized

════════════════════════════════════════════════════════════
 FILE METADATA
════════════════════════════════════════════════════════════
Path           : /home/user/confidential.docx
Size           : 145,782 bytes
Created        : 2025-03-15 14:22:10
Last Modified  : 2025-11-20 09:11:05
════════════════════════════════════════════════════════════

[Hash] SHA-256: a1b2c3d4e5f6...

[Analysis] Entropy: 7.8921 bits/byte (max possible: 8.0000)

[Backup] Creating automatic safety backup...
[Info] Backup created: /home/user/confidential_20251123_142305.docx.bak

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!! WARNING: This will move the file to ~/.trash (recoverable)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Do you wish to proceed with moving this file to trash? (yes/no): yes

[Success] File moved to trash: /home/user/.trash/confidential_20251123_142305.docx
[Success] File has been safely moved to trash.
```

## Contributing

Contributions are very welcome! Whether you want to:

- Add secure overwrite + permanent deletion mode  
- Implement a trash recovery/restoration tool  
- Improve the UI with rich/textual  
- Add support for directories or batch processing  
- Enhance logging (JSON, encryption)  
- Write tests (pytest) or CI workflows  

…your help will make this tool even more valuable to the community.

### How to contribute
1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/amazing-idea`)  
3. Commit your changes (`git commit -m 'Add amazing idea'`)  
4. Push to the branch (`git push origin feature/amazing-idea`)  
5. Open a Pull Request  

Please include tests and update documentation where appropriate.

## License

MIT License – see [LICENSE](LICENSE) for details.

---

**Never lose a file again.**  
Built with caution, clarity, and community in mind.
