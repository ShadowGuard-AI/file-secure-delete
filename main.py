import os
import argparse
import logging
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
        help="Number of overwriting passes to perform (default: 3)."
    )
    return parser

def securely_delete(file_path, passes):
    """
    Securely delete a file by overwriting it multiple times.
    :param file_path: Path to the file to be securely deleted.
    :param passes: Number of overwrite passes.
    """
    try:
        file = Path(file_path)

        # Validate file existence
        if not file.is_file():
            logging.error(f"File does not exist: {file_path}")
            raise FileNotFoundError(f"File does not exist: {file_path}")

        file_size = file.stat().st_size
        logging.info(f"Starting secure deletion for: {file_path} (Size: {file_size} bytes)")

        # Overwrite file with random data for the specified number of passes
        with open(file, "wb") as f:
            for i in range(passes):
                logging.info(f"Overwriting pass {i + 1}/{passes}")
                f.seek(0)
                f.write(os.urandom(file_size))

        # Delete the file
        file.unlink()
        logging.info(f"File securely deleted: {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

def main():
    """
    Main function to parse arguments and invoke the secure delete functionality.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    try:
        securely_delete(args.file_path, args.passes)
    except Exception as e:
        logging.error(f"Failed to securely delete file: {e}")

if __name__ == "__main__":
    main()