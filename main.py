import os
import argparse
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Setup command-line argument parsing.
    """
    parser = argparse.ArgumentParser(
        description="Securely delete files by overwriting them multiple times before deletion."
    )
    parser.add_argument(
        "file_path",
        type=str,
        help="Path to the file you want to securely delete."
    )
    parser.add_argument(
        "--passes",
        type=int,
        default=3,
        help="Number of overwriting passes to perform (default: 3). Must be at least 1; a count below 1 is refused at exit 1 before the file is touched."
    )
    parser.add_argument(
        "--follow-symlink",
        action="store_true",
        help="Follow a symlink argument: overwrite and delete the resolved target file itself, and log the resolved path. Without this flag a symlink argument is refused at exit 1."
    )
    return parser

def securely_delete(file_path, passes, follow_symlink=False):
    """
    Securely delete a file by overwriting it multiple times.
    :param file_path: Path to the file to be securely deleted.
    :param passes: Number of overwrite passes.
    :param follow_symlink: If True, a symlink argument is resolved and the
        target file itself is overwritten and deleted.
    """
    if passes < 1:
        logging.error(f"Pass count must be at least 1, got {passes}. Refusing before touching the file.")
        raise ValueError(f"Pass count must be at least 1, got {passes}")

    try:
        file = Path(file_path)

        if file.is_symlink():
            if not follow_symlink:
                logging.error(f"Path is a symlink: {file_path}. Refusing without --follow-symlink.")
                raise ValueError(f"Path is a symlink: {file_path}. Refusing without --follow-symlink.")
            resolved = file.resolve()
            logging.info(f"Following symlink {file_path} to resolved target: {resolved}")
            file = resolved

        # Validate file existence
        if not file.is_file():
            logging.error(f"File does not exist: {file}")
            raise FileNotFoundError(f"File does not exist: {file}")

        file_size = file.stat().st_size
        logging.info(f"Starting secure deletion for: {file} (Size: {file_size} bytes)")

        # Overwrite the file in place on the same inode (r+b, no truncate),
        # flushing and syncing after each pass.
        with open(file, "r+b") as f:
            for i in range(passes):
                logging.info(f"Overwriting pass {i + 1}/{passes}")
                f.seek(0)
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
            f.flush()
            os.fsync(f.fileno())

        # Delete the file
        file.unlink()
        logging.info(f"File securely deleted: {file}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

def main():
    """
    Main function to parse arguments and invoke the secure delete functionality.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if args.passes < 1:
        logging.error(f"Pass count must be at least 1, got {args.passes}. Refusing before touching the file.")
        print(f"Pass count must be at least 1, got {args.passes}. The file was not touched.")
        sys.exit(1)

    try:
        securely_delete(args.file_path, args.passes, follow_symlink=args.follow_symlink)
    except Exception as e:
        logging.error(f"Failed to securely delete file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()