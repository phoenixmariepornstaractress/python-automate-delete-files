# File Deletion Utility

This Python utility script provides a comprehensive and interactive way to safely analyze, back up, and delete files. It combines file metadata inspection, entropy and hash analysis, and intelligent user interaction to help ensure intentional file removal. It also supports backup creation, file previewing, and logging for audit purposes.

## Features

* Interactive deletion confirmation
* Backup and move-to-trash before deletion
* File preview and metadata display
* SHA-256 hash and entropy calculation
* File size analysis and effort estimation
* Numpy-generated samples for diagnostics
* Comprehensive logging to `deletion_log.txt`

## Requirements

* Python 3.6 or later
* `numpy`

Install dependencies via pip:

```bash
pip install numpy
```

## Usage

Run the script and follow the on-screen prompts:

```bash
python delete_file_script.py
```

You'll be asked to enter the full file path of the file you want to delete. The script will display metadata, preview file contents, analyze entropy and size, then ask for confirmation before deletion.

## Logging

All deletion attempts (successful or not) are logged in `deletion_log.txt` with a timestamp.

## Contributing

Contributions are welcome! If you have suggestions, bug fixes, or enhancements:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to your branch (`git push origin feature-name`)
5. Open a Pull Request

Please ensure your code follows PEP8 standards and includes clear, concise documentation.

## License

This project is open-source and available under the MIT License.
