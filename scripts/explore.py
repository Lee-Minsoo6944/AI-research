"""탐색 분석: 본 분석(analyze.py) 결과를 본 **뒤에** 추가한 계산.

목적: 코딩 경력(YearsCode)으로는 rho = -0.134 인데 직업 경력(WorkExp)으로는
rho = -0.033 으로 약했던 불일치의 원인 후보를 데이터로 대조한다.
여기서 나온 숫자는 가설 판정에 쓰지 않으며, 논문에서 '탐색적 결과'로 구분한다.

원인 후보와 대조 방법 (실행 전에 적음, 2026-11-13)
  E1 표본이 다르다: WorkExp 는 직업 경력이 0이면 비워 두게 되어 있어 배우는 사람이 빠진다.
     -> 세 문항에 모두 답한 같은 사람들로 두 상관을 다시 계산하고,
        WorkExp 가 빈 사람들만으로 YearsCode 상관을 계산한다.
  E2 관계가 초반 몇 해에 몰려 있다: 1-4년에서 5-9년 사이에 신뢰가 크게 떨어졌다.
     -> YearsCode 5년 이상, 10년 이상만으로 상관을 계산한다.
  E3 응답자 유형이 다르다: 배우는 사람과 직업 개발자의 신뢰가 다를 수 있다.
     -> MainBranch 별 신뢰 비율과, 직업 개발자만의 상관을 계산한다.
  E4 나이와 겹친다: 경력이 길면 나이도 많다.
     -> 나이대별 신뢰 비율과, 나이대 안에서의 상관을 계산한다.

사용법:  python explore.py <results.csv 경로> <결과를 쓸 폴더>
"""
import csv
import os
import sys

from analyze import TRUST, describe, number

BINS = [("1-4년", 1, 4), ("5-9년", 5, 9), ("10-19년", 10, 19), ("20년 이상", 20, 10 ** 9)]
AGE_ORDER = ["18-24 years old", "25-34 years old", "35-44 years old",
             "45-54 years old", "55-64 years old", "65 years or older", "Prefer not to say"]


def load(path):
    csv.field_size_limit(10 ** 9)
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            trust = TRUST.get(row["AIAcc"].strip())
            if trust is None:
                continue
            rows.append({
                "years": number(row["YearsCode"]),
                "work": number(row["WorkExp"]),
                "trust": trust,
                "branch": row["MainBranch"].strip(),
                "age": row["Age"].strip(),
            })
    return rows


def share(rows):
    n = len(rows)
    trust = sum(1 for r in rows if r["trust"] >= 4)
    distrust = sum(1 for r in rows if r["trust"] <= 2)
    mean = sum(r["trust"] for r in rows) / n
    return f"n = {n}, 신뢰 {100 * trust / n:.1f}%, 불신 {100 * distrust / n:.1f}%, 평균 점수 {mean:.3f}"


def main(path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    rows = load(path)
    with_years = [r for r in rows if r["years"] is not None]
    lines = ["탐색 분석 (본 분석 뒤에 추가, 판정에 쓰지 않음)",
             f"AIAcc 응답자: {len(rows)}, 그중 YearsCode 응답자: {len(with_years)}", ""]

    lines.append("[E1] 표본 차이")
    same = [r for r in with_years if r["work"] is not None]
    no_work = [r for r in with_years if r["work"] is None]
    lines.append(describe("세 문항 모두 응답 - YearsCode x AIAcc", [(r["years"], r["trust"]) for r in same])[2])
    lines.append(describe("세 문항 모두 응답 - WorkExp x AIAcc", [(r["work"], r["trust"]) for r in same])[2])
    lines.append(describe("WorkExp 가 빈 응답자 - YearsCode x AIAcc", [(r["years"], r["trust"]) for r in no_work])[2])
    lines.append("WorkExp 가 있는 응답자: " + share(same))
    lines.append("WorkExp 가 빈 응답자: " + share(no_work))
    lines.append("직업 경력 구간별 (세 문항 모두 응답)")
    for name, low, high in BINS:
        lines.append(f"   WorkExp {name}: " + share([r for r in same if low <= r["work"] <= high]))
    lines.append("")

    lines.append("[E2] 초반 몇 해에 몰려 있는가")
    for floor in (5, 10):
        part = [(r["years"], r["trust"]) for r in with_years if r["years"] >= floor]
        lines.append(describe(f"YearsCode {floor}년 이상만", part)[2])
    lines.append("")

    lines.append("[E3] 응답자 유형(MainBranch)")
    branches = sorted({r["branch"] for r in with_years}, key=lambda b: -sum(1 for r in with_years if r["branch"] == b))
    for b in branches:
        lines.append(f"   {b}: " + share([r for r in with_years if r["branch"] == b]))
    pro = [(r["years"], r["trust"]) for r in with_years if r["branch"] == "I am a developer by profession"]
    lines.append(describe("직업 개발자만 - YearsCode x AIAcc", pro)[2])
    lines.append("")

    lines.append("[E4] 나이대")
    for age in AGE_ORDER:
        part = [r for r in with_years if r["age"] == age]
        if len(part) < 30:
            continue
        lines.append(f"   {age}: " + share(part))
        lines.append("      " + describe("이 나이대 안에서 YearsCode x AIAcc", [(r["years"], r["trust"]) for r in part])[2])

    text = "\n".join(lines)
    print(text)
    with open(os.path.join(out_dir, "exploratory.txt"), "w", encoding="utf-8") as f:
        f.write(text + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
