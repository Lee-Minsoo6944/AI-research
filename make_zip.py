"""제출용 ZIP 을 만든다 (제출물에는 들어가지 않는 도구).

사용법 (research 폴더에서):  python make_zip.py
결과: dist/task10_leeminsoo.zip
"""
import os
import shutil
import sys
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
NAME = "task10_leeminsoo"
INCLUDE = [
    "README.md",
    "01-hypothesis.md", "02-literature.md", "03-design.md", "04-results.md", "05-replication.md",
    "paper/paper.pdf", "paper/paper.html", "paper/figure_trust_by_experience.svg",
    "data/raw/results.csv", "data/raw/schema.csv",
    "data/raw2026/survey_results_public.csv", "data/raw2026/survey_results_schema.csv",
    "data/pilot_output.txt", "data/pilot_output_2026.txt",
    "scripts/pilot_check.py", "scripts/pilot_check_2026.py", "scripts/analyze.py",
    "scripts/explore.py", "scripts/replicate_2026.py", "scripts/verify.py",
    "results/summary.txt", "results/table_by_experience.csv", "results/figure_trust_by_experience.svg",
    "results/exploratory.txt", "results/replication_2026.txt", "results/table_by_experience_2026.csv",
    "results/prerun_hashes.txt", "results/prerun_hashes_2026.txt",
]
MARKERS = ["[ ]", "TODO", "____", "( 예:", "작성 중", "미완성"]


def main():
    shutil.copyfile(os.path.join(ROOT, "results", "figure_trust_by_experience.svg"),
                    os.path.join(ROOT, "paper", "figure_trust_by_experience.svg"))
    missing = [p for p in INCLUDE if not os.path.exists(os.path.join(ROOT, p))]
    if missing:
        print("없는 파일:", missing)
        return 1

    warnings = 0
    for p in INCLUDE:
        if not p.endswith((".md", ".html", ".py", ".txt")) or p.startswith("data/"):
            continue
        with open(os.path.join(ROOT, p), encoding="utf-8-sig") as f:
            for number, line in enumerate(f, 1):
                for marker in MARKERS:
                    if marker in line and "MARKERS" not in line:
                        warnings += 1
                        print(f"미완성 표시 {marker!r}: {p}:{number}")

    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    target = os.path.join(ROOT, "dist", NAME + ".zip")
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in INCLUDE:
            z.write(os.path.join(ROOT, p), f"{NAME}/{p}")
    print(f"만든 파일: {target} ({os.path.getsize(target):,} 바이트, 파일 {len(INCLUDE)}개)")
    print(f"미완성 표시 {warnings}건")
    return 0


if __name__ == "__main__":
    sys.exit(main())
