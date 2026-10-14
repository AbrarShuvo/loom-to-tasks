def to_markdown(result):
    lines = ["# Summary", "", result.summary, "", "## Decisions"]
    lines += [f"- {d}" for d in result.decisions] or ["- none"]
    lines += ["", "## Tasks"]
    if result.tasks:
        for t in result.tasks:
            owner = t.owner
            if t.owner != "unknown" and not t.owner_confirmed:
                owner = f"{t.owner} (unconfirmed)"
            lines.append(
                f"- [ ] {t.title} | owner: {owner} | due: {t.deadline} | priority: {t.priority}"
            )
    else:
        lines.append("- none")
    lines += ["", "## Blockers"]
    lines += [f"- {b}" for b in result.blockers] or ["- none"]
    return "\n".join(lines)