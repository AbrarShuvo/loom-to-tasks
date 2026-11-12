# Loom to Tasks

Turns the transcript of a recorded meeting or Loom video into a clear, checked list of **decisions, tasks (owner, deadline, priority) and blockers**, so nobody has to rewatch a 20-minute video to find out what they need to do.

Built with Python and the Gemini API, using structured outputs and an automated test suite.

## Example

**Input** (`samples/transcript_short.txt`):

> Hey team, quick update on the Brightleaf pricing page. I finished the first version of the layout yesterday. Two things. First, we decided to go with the three-column pricing table instead of the toggle, because the toggle confused people in the last test. Second, Priya, can you update the icons to the new set by Thursday? Dan, I need you to send the final copy for the headlines by Friday. One blocker: we still don't have the logo files from the client, so I can't finish the header. I'll email them today.

**Output:**

| | Item | Owner | Deadline |
|---|---|---|---|
| Decision | Use the three-column pricing table instead of the toggle | | |
| Task | Update icons to the new set | Priya | Thursday |
| Task | Send final headline copy | Dan | Friday |
| Task | Email client for logo files | unknown (speaker not named) | Today |
| Blocker | Logo files from the client are missing | | |

## Key rules

- **It never guesses.** If an owner or deadline isn't said, it writes `unknown`.
- A tentative owner ("maybe Lena") is named but marked **unconfirmed**.
- The speaker's own commitments ("I'll email them") count as tasks.
- The summary never claims more than was said ("first version" stays "first version", not "finalized").
- A specific statement about a task ("no rush") beats a general one.

## How it works

1. `read_transcript.py` loads and cleans the transcript text
2. `gemini_client.py` sends it to Gemini with a strict output schema (`schema.py`), retrying on temporary server errors
3. `extract.py` validates the result and saves it as JSON
4. `render.py` turns it into readable Markdown (`--md`)

## Testing

Each sample transcript has an answer key written **before** running the tool, so results are checked against what a human expected, not against the tool's own output.

- 4 test transcripts: short, messy, long and written
- **67 of 67 automated checks pass** (`python src\run_tests.py`)
- Two runs on the same transcript gave identical results

## Setup

Requires Python 3.10+.

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your `GEMINI_API_KEY` and `GEMINI_MODEL`. Run `python src\list_models.py` to see available models.

## Run

```
python src\extract.py samples\transcript_short.txt --md
```

## Known limits

- Reads text transcripts only, not audio or video (a video-aware version is in progress)
- Tested on transcripts I wrote myself, not yet on real unscripted calls
- Transcripts are sent to Google's Gemini API. Use fake data, or a paid-tier key and permission, for real meetings.

## Tech

Python · Gemini API · structured outputs (JSON schema) · automated testing
