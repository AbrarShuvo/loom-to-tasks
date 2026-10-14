import sys
import time
from render import to_markdown
from pydantic import ValidationError

from read_transcript import read_transcript
from gemini_client import generate_structured
from schema import Extraction

SYSTEM_PROMPT = """You extract structured information from the transcript of a Loom video
(a design review, client call or internal update).

Rules:
1. Use only information stated in the transcript. Never guess or invent anything.
2. If a task's owner is not stated, write "unknown". If its deadline is not stated, write "unknown".
3. If an owner is only suggested tentatively (for example "maybe Lena"), write that name and set owner_confirmed to false. If the owner is clearly stated, set owner_confirmed to true. If the owner is unknown, set owner_confirmed to false.
4. If the speaker changes their mind or corrects a date, use the final version only.
5. Ignore filler words and tangents, but keep real tasks even if they are unrelated to the main topic.
6. Priority: set a task's priority only from words the speaker says about that specific task (for example "no rush" means low, "urgent" means high). A general statement about a different topic does not set the priority of an unrelated task. If nothing is said about that task, write "unknown".6. Priority: use what the speaker says. If priority is not stated, write "unknown".
7. Decisions are things the speaker says were decided. Blockers are things stopping progress.
8. The summary must be two sentences at most. It must only describe what the speaker actually said or asked for. Do not say work is finished, final or underway unless the speaker says so. Say "asked Priya to update the icons" and not "work is underway".8. The summary must be two sentences at most.
9. If the speaker commits to doing something themselves in the future (for example "I'll email them today"), record it as a task. If the speaker does not give their own name, write "speaker" as the owner and set owner_confirmed to true. Do not turn things the speaker already finished into tasks.
"""


RETRY_CODES = {429, 500, 503}
MAX_ATTEMPTS = 3


def extract(transcript_text):
    last_error = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            raw = generate_structured(
                contents=f"Transcript:\n\n{transcript_text}",
                schema=Extraction,
                system_instruction=SYSTEM_PROMPT,
            )
            if not raw or not raw.strip():
                raise ValueError("The model returned an empty reply.")
            return Extraction.model_validate_json(raw)
        except ValueError as error:
            last_error = error
        except Exception as error:
            if getattr(error, "code", None) not in RETRY_CODES:
                raise
            last_error = error
        if attempt < MAX_ATTEMPTS:
            wait = 2 ** attempt
            print(f"Attempt {attempt} failed ({type(last_error).__name__}: {str(last_error)[:150]}). Retrying in {wait}s...", file=sys.stderr)
            time.sleep(wait)
    raise last_error


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_markdown = "--md" in sys.argv
    if not args:
        print("Usage: python src/extract.py <path to transcript> [--md]")
        sys.exit(1)
    try:
        text = read_transcript(args[0])
    except (FileNotFoundError, ValueError) as error:
        print(f"Input error: {error}")
        sys.exit(1)
    try:
        result = extract(text)
    except ValidationError as error:
        print(f"The model returned output that does not match the schema:\n{error}")
        sys.exit(1)
    except ValueError as error:
        print(f"Bad model reply: {error}")
        sys.exit(1)
    except Exception as error:
        print(f"Request failed: {type(error).__name__}: {error}")
        sys.exit(1)
    if as_markdown:
        print(to_markdown(result))
    else:
        print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()