import sys
from pathlib import Path


def read_transcript(path):
    """Read a transcript file and return its text."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Transcript not found: {path}")
    text = file_path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"Transcript is empty: {path}")
    return text


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/read_transcript.py <path to transcript>")
        sys.exit(1)
    try:
        text = read_transcript(sys.argv[1])
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        sys.exit(1)
    print(f"Loaded {len(text.split())} words, {len(text)} characters.\n")
    print(text)


if __name__ == "__main__":
    main()