![Banner](banner.png)

# file-secure-delete

## Project Description

This tool securely deletes files by overwriting them multiple times, preventing data recovery. It focuses on file operations and analysis.

Each overwrite pass is flushed and synced to storage with `os.fsync`, and the file is flushed and synced again before its name is removed. The file is overwritten in place on the same inode.

A pass count below 1 (`--passes 0` or a negative count) is refused at exit 1 before the file is touched, so it never performs a plain delete under a secure deletion claim. Any failure exits 1.

Symlinks: a symlink argument is refused at exit 1 by default, and neither the link nor its target is touched. With `--follow-symlink`, the link is resolved, the resolved target file itself is overwritten and deleted, and the resolved path is logged. The symlink itself is left in place as a dangling link in that case.

## Installation

There is no package to install. Clone the repository and run `main.py` directly:

```
git clone https://github.com/ShadowGuard-AI/file-secure-delete.git
cd file-secure-delete
```

## Usage

```
usage: main.py [-h] [--passes PASSES] [--follow-symlink] file_path

Securely delete files by overwriting them multiple times before deletion.

positional arguments:
  file_path              Path to the file you want to securely delete.

options:
  -h, --help             show this help message and exit
  --passes PASSES        Number of overwriting passes to perform (default: 3). Must be at least 1.
  --follow-symlink       Follow a symlink argument: overwrite and delete the resolved target file itself, and log the resolved path.
```

## Examples

### Delete a single file securely

```
python main.py myfile.txt
```

### Delete a file with 5 overwriting passes

```
python main.py --passes 5 myfile.txt
```

### Delete the target of a symlink

```
python main.py --follow-symlink mylink.txt
```

## Security Warnings

This tool is intended to securely delete files, but it is not foolproof. Deleted data may still be recoverable using advanced techniques. Use it at your own discretion.

## License

This tool is licensed under the GNU General Public License v3.0 to CY83R-3X71NC710N.
