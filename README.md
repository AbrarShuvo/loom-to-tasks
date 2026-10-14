# Loom to Tasks

Turns a text transcript of a Loom video into a checked list: summary, decisions, tasks (owner, deadline, priority) and blockers.

## What it does not do
- No audio or video. It reads text transcripts.
- It never guesses: an unstated owner or deadline becomes "unknown". A tentative owner is marked unconfirmed.
- Tested on [N] transcripts I wrote or recorded myself. Not tested on real client calls.

## Setup
1. Install Python (3.10 or newer).
2. In the project folder: python -m venv .venv
3. Activate it: .venv\Scripts\activate
4. pip install -r requirements.txt
5. Copy .env.example to .env and fill in your Gemini key and model name.

## Run
python src\extract.py samples\transcript_short.txt --md

## Test
python src\run_tests.py

## Privacy
Transcripts go to Google's Gemini API. Use fake data unless you have permission to send real content and have checked the provider's terms.

## Known limits
- [your list, from NOTES.md]