"""짧은 확인: 원자료 해시를 확인하고, 모든 분석을 다시 실행해 제출한 결과와 견준다.

사용법 (ZIP 을 푼 폴더에서):  python scripts/verify.py
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import analyze          # noqa: E402
import explore          # noqa: E402
import replicate_2026   # noqa: E402

RAW_2025 = os.path.join(ROOT, "data", "raw", "results.csv")
RAW_2026 = os.path.join(ROOT, "data", "raw2026", "survey_results_public.csv")
EXPECTED_HASH = {
    RAW_2025: "2d1f65308877282edfb4470520eabbc08cb499118432a3dcec6a66c086aa2baa",
    RAW_2026: "ad520b4d5d71f240141e63f0d6f81a3b1898cbdc69efe9ea985496533b15fc2c",
}
OUTPUTS = [
    "summary.txt",
    "table_by_experience.csv",
    "figure_trust_by_experience.svg",
    "exploratory.txt",
    "replication_2026.txt",
    "table_by_experience_2026.csv",
]


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def text(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read().splitlines()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    ok = True

    print("== 1. 원자료 해시 확인 ==")
    for path, expected in EXPECTED_HASH.items():
        same = sha256(path) == expected
        ok = ok and same
        print(f"{'일치' if same else '불일치'}  {os.path.relpath(path, ROOT)}")

    out = os.path.join(ROOT, "results_check")
    print("\n== 2. 본 분석 (2025) ==")
    analyze.main(RAW_2025, out)
    print("\n== 3. 탐색 분석 (2025) ==")
    explore.main(RAW_2025, out)
    print("\n== 4. 추가 검증 (2026) ==")
    replicate_2026.main(RAW_2026, out)

    print("\n== 5. 제출한 결과(results)와 다시 실행한 결과(results_check) 견주기 ==")
    for name in OUTPUTS:
        same = text(os.path.join(ROOT, "results", name)) == text(os.path.join(out, name))
        ok = ok and same
        print(f"{'일치' if same else '불일치'}  {name}")

    print("\n재현 확인: " + ("모두 일치" if ok else "일치하지 않는 항목이 있음"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
