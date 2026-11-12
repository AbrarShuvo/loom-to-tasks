# Development notes

## Known issues found on Day 4 (all fixed)

1. **short:** missed the speaker's own task "I'll email the client for logos". Fixed with a rule: the speaker's commitments count as tasks.
2. **short:** summary said "finalized" and "underway"; the transcript says "first version" and only requests. Fixed with a rule: the summary must not claim more than was said.
3. **messy:** green button priority came out high; the transcript says "no rush". Fixed with a rule: an explicit statement about a task beats a general statement.

## Day 5: long transcript

- 7 tasks found, matching my key. No invented or duplicate tasks.
- Two runs were identical (compared with Compare-Object).
- Minor: summary says "documentation" for the onboarding copy and "assigned" for tasks nobody was assigned.
- Limit: I wrote this transcript and the key. Needs a transcript I didn't write.

## Day 5: model and errors

- 404 means the model name is wrong or retired. It fails at once, no retry.
- 503 means the server is busy. extract.py retries up to 3 times.
- gemini-2.5-flash was retired for new users. Pick a model from list_models.py and test it.
- The model is set in `.env` as `GEMINI_MODEL`, so it can be changed without touching code.

## Day 7: timing

- Tool: about 6 seconds per transcript (about 330 words), plus a short manual review of the output.
- Manual time is not measured fairly yet: I wrote the transcript, so I already knew the answers. Needs timing on a transcript someone else recorded.
