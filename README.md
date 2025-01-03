# file-secure-delete

## Project Description

This tool securely deletes files by overwriting them multiple times, preventing data recovery. It focuses on file operations and analysis.

## Installation

```
pip install file-secure-delete
```

## Usage

```
usage: file-secure-delete [-h] [-v] [-n NUM] file1 file2 ...

Securely delete files with multiple overwrites

positional arguments:
  file1                  First file to delete
  file2                  Second file to delete
  ...                    Additional files to delete

optional arguments:
  -h, --help             show this help message and exit
  -v, --verbose          Enable verbose logging
  -n NUM, --num NUM      Number of overwrites (default: 3)
```

## Examples

### Delete a single file securely

```
file-secure-delete myfile.txt
```

### Delete multiple files securely

```
file-secure-delete file1.txt file2.txt file3.txt
```

### Delete files with 5 overwrites

```
file-secure-delete -n 5 myfile.txt
```

## Security Warnings

This tool is intended to securely delete files, but it is not foolproof. Deleted data may still be recoverable using advanced techniques. Use it at your own discretion.

## License

This tool is licensed under the GNU General Public License v3.0 to CY83R-3X71NC710N.