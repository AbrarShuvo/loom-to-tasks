# Known issues (found Day 4)

1. short: missed the speaker's own task "I'll email the client for logos". Needs a rule: the speaker's commitments count as tasks.
2. short: summary says "finalized" and "underway"; transcript says "first version" and only requests. Needs a rule: the summary must not claim more than was said.
3. messy: green button priority came out high; transcript says "no rush". Needs a rule: an explicit statement about a task beats a general statement.

# Day 5: long transcript
- 7 tasks found, matching my key. No invented or duplicate tasks.
- Two runs were identical (compared with Compare-Object).
- Minor: summary says "documentation" for the onboarding copy and "assigned" for tasks nobody was assigned.
- Limit: I wrote this transcript and the key. Needs a transcript I didn't write.

   # Day 5: model and errors
   - 404 means the model name is wrong or retired. It fails at once, no retry.
   - 503 means the server is busy. extract.py retries up to 3 times.
   - gemini-2.5-flash was retired for new users. Pick a model from list_models.py and test it.
   - My current model: [the name from the Select-String command]