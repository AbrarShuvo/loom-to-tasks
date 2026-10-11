import sys
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
6. Priority: use what the speaker says. If priority is not stated, write "unknown".
7. Decisions are things the speaker says were decided. Blockers are things stopping progress.
8. The summary must be two sentences at most.
9. If the speaker commits to doing something themselves in the future (for example "I'll email them today"), record it as a task. If the speaker does not give their own name, write "speaker" as the owner and set owner_confirmed to true. Do not turn things the speaker already finished into tasks.
"""


def extract(transcript_text):
    raw = generate_structured(
        contents=f"Transcript:\n\n{transcript_text}",
        schema=Extraction,
        system_instruction=SYSTEM_PROMPT,
    )
    return Extraction.model_validate_json(raw)


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/extract.py <path to transcript>")
        sys.exit(1)
    try:
        text = read_transcript(sys.argv[1])
        result = extract(text)
    except (FileNotFoundError, ValueError) as error:
        print(f"Input error: {error}")
        sys.exit(1)
    except ValidationError as error:
        print(f"The model returned output that does not match the schema:\n{error}")
        sys.exit(1)
    except Exception as error:
        print(f"Request failed: {type(error).__name__}: {error}")
        sys.exit(1)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()