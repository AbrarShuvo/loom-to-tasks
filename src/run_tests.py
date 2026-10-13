import json
import sys
import time
from datetime import datetime
from pathlib import Path

from read_transcript import read_transcript
from extract import extract

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "samples"
OUTPUTS = ROOT / "outputs"
PAUSE_SECONDS = 4


def norm(text):
    return " ".join(str(text).lower().split())


def find_task(tasks, keyword):
    for task in tasks:
        if norm(keyword) in norm(task.title):
            return task
    return None


def check_transcript(result, expected):
    """Return a list of (passed, message) pairs."""
    checks = []

    count = expected.get("task_count")
    if count is not None:
        checks.append(
            (len(result.tasks) == count,
             f"task count is {len(result.tasks)}, expected {count}")
        )

    for spec in expected.get("tasks", []):
        keyword = spec["keyword"]
        task = find_task(result.tasks, keyword)
        if task is None:
            checks.append((False, f"task '{keyword}' not found"))
            continue
        for field in ("owner", "deadline", "priority"):
            if field in spec:
                got = getattr(task, field)
                checks.append(
                    (norm(got) == norm(spec[field]),
                     f"task '{keyword}' {field}: got '{got}', expected '{spec[field]}'")
                )
        if "owner_confirmed" in spec:
            checks.append(
                (task.owner_confirmed == spec["owner_confirmed"],
                 f"task '{keyword}' owner_confirmed: got {task.owner_confirmed}, "
                 f"expected {spec['owner_confirmed']}")
            )

    for keyword in expected.get("decisions", []):
        found = any(norm(keyword) in norm(d) for d in result.decisions)
        checks.append((found, f"decision containing '{keyword}' not found"))

    for keyword in expected.get("blockers", []):
        found = any(norm(keyword) in norm(b) for b in result.blockers)
        checks.append((found, f"blocker containing '{keyword}' not found"))

    for keyword in expected.get("forbidden_task_keywords", []):
        absent = find_task(result.tasks, keyword) is None
        checks.append((absent, f"a task containing '{keyword}' should not exist"))

    return checks


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    expected_all = json.loads((SAMPLES / "expected.json").read_text(encoding="utf-8"))
    names = [n for n in expected_all if only is None or only in n]
    if not names:
        print(f"No transcript matches '{only}'.")
        sys.exit(1)

    OUTPUTS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    total_checks = total_passed = errors = 0

    for index, name in enumerate(names):
        if index > 0:
            time.sleep(PAUSE_SECONDS)
        print(f"\n{name}")
        try:
            text = read_transcript(SAMPLES / name)
            result = extract(text)
        except Exception as error:
            errors += 1
            print(f"  ERROR: {type(error).__name__}: {str(error)[:200]}")
            continue

        out_file = OUTPUTS / f"{Path(name).stem}_{stamp}.json"
        out_file.write_text(result.model_dump_json(indent=2), encoding="utf-8")

        checks = check_transcript(result, expected_all[name])
        passed = sum(1 for ok, _ in checks if ok)
        for ok, message in checks:
            if not ok:
                print(f"  FAIL: {message}")
        print(f"  {passed}/{len(checks)} checks passed")
        total_checks += len(checks)
        total_passed += passed

    print(f"\nTotal: {total_passed}/{total_checks} checks passed, {errors} transcript(s) errored")
    if errors or total_passed < total_checks:
        sys.exit(1)


if __name__ == "__main__":
    main()