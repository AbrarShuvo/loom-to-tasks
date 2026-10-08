   # Loom to Tasks: scope v0.1

   Input: a text transcript of a Loom video.
   Output: JSON with summary, decisions, tasks (title, owner, deadline, priority), blockers.
   Rule: if owner or deadline is not stated, write "unknown". Never guess.
   Out of scope for v1: audio/video, real-time use, integrations, user interface.
   Done when: it handles my 3 sample transcripts and one designer says it saves time.