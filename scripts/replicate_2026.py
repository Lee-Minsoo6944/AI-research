"""추가 검증: 2026년 설문 자료로 다시 확인한다.

계산 방법과 예측 P1~P4 는 research/05-replication.md 3절에 실행 전에 적은 대로이다.
1단계 가설의 판정(2025년 자료)에는 쓰지 않는다.

사용법:  python replicate_2026.py <survey_results_public.csv 경로> <결과를 쓸 폴더>
"""
import csv
import os
import sys

from analyze import ALPHA, RHO_THRESHOLD, describe, number

NO_TRUST = "I do not trust it for most work tasks"
LOW_RISK = "I trust it for low-risk work tasks only"
VERIFY = "I trust it when I can easily verify the output"
MANY = "I trust it for many tasks, but not important work decisions"
MANY_IMPORTANT = "I trust it for many tasks, including important work decisions"

FOUR = {NO_TRUST: 1, LOW_RISK: 2, MANY: 3, MANY_IMPORTANT: 4}          # 주 계산
FIVE = {NO_TRUST: 1, LOW_RISK: 2, VERIFY: 3, MANY: 4, MANY_IMPORTANT: 5}  # 민감도 계산
BINS = [("1-4년", 1, 4), ("5-9년", 5, 9), ("10-19년", 10, 19), ("20년 이상", 20, 10 ** 9)]
AGES = ["18-24 years old", "25-34 years old", "35-44 years old",
        "45-54 years old", "55-64 years old", "65 years or older"]


def load(path):
    csv.field_size_limit(10 ** 9)
    rows = []
    total = 0
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            total += 1
            answer = (row["AITrust"] or "").strip()
            if answer not in FIVE:
                continue  # 빈값과 'Not sure / I do not use AI tools' 제외
            rows.append({
                "years": number(row["YearsCode"] or ""),
                "work": number(row["WorkExp"] or ""),
                "age": (row["Age"] or "").strip(),
                "answer": answer,
            })
    return total, rows


def shares(rows):
    n = len(rows)
    count = {key: sum(1 for r in rows if r["answer"] == key) for key in FIVE}
    return {
        "n": n,
        "count": count,
        "trust": 100 * (count[MANY] + count[MANY_IMPORTANT]) / n,
        "verify": 100 * count[VERIFY] / n,
        "low": 100 * count[LOW_RISK] / n,
        "distrust": 100 * count[NO_TRUST] / n,
    }


def main(path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    total, rows = load(path)
    with_years = [r for r in rows if r["years"] is not None]
    lines = [f"전체 행: {total}",
             f"AITrust 응답자('Not sure'·빈값 제외): {len(rows)}",
             f"그중 YearsCode 응답자: {len(with_years)}",
             f"그중 조건부 보기('when I can easily verify') 응답자: {sum(1 for r in with_years if r['answer'] == VERIFY)}",
             ""]

    lines.append("[P1] 코딩 경력이 길수록 신뢰가 낮다")
    rho4, p4, line = describe("주 계산 YearsCode x AITrust(4단계, 조건부 보기 제외)",
                              [(r["years"], FOUR[r["answer"]]) for r in with_years if r["answer"] in FOUR])
    lines.append(line)
    rho5, p5, line = describe("민감도 YearsCode x AITrust(5단계, 조건부 보기를 가운데에)",
                              [(r["years"], FIVE[r["answer"]]) for r in with_years])
    lines.append(line)

    def verdict(rho, p):
        if rho >= 0:
            return "재현 실패 (rho >= 0)"
        if rho <= RHO_THRESHOLD and p < ALPHA:
            return "충족"
        return "방향만 일치 (기준 미달)"

    lines.append(f"P1 주 계산: {verdict(rho4, p4)} / 민감도: {verdict(rho5, p5)}")
    lines.append("")

    lines.append("[P2] 차이는 초반에 가장 크다 - 코딩 경력 구간별")
    table = []
    for name, low, high in BINS:
        s = shares([r for r in with_years if low <= r["years"] <= high])
        s["bin"] = name
        table.append(s)
        lines.append(f"   {name}: n = {s['n']}, 신뢰 {s['trust']:.1f}%, 조건부 {s['verify']:.1f}%, "
                     f"저위험만 {s['low']:.1f}%, 불신 {s['distrust']:.1f}%")
    drops = [table[i]["trust"] - table[i + 1]["trust"] for i in range(3)]
    lines.append("   신뢰 비율 감소 폭(%p): " + ", ".join(f"{d:.1f}" for d in drops))
    p2 = drops[0] > 0 and drops[0] == max(drops)
    lines.append(f"P2: {'충족' if p2 else '불충족'}")
    lines.append("")

    lines.append("[P3] 직업 경력으로 보면 관계가 더 약하다 - 세 문항 모두 응답, 4단계")
    same = [r for r in with_years if r["work"] is not None and r["answer"] in FOUR]
    rho_years, _, line = describe("YearsCode x AITrust", [(r["years"], FOUR[r["answer"]]) for r in same])
    lines.append(line)
    rho_work, _, line = describe("WorkExp x AITrust", [(r["work"], FOUR[r["answer"]]) for r in same])
    lines.append(line)
    lines.append(f"P3: {'충족' if abs(rho_work) < abs(rho_years) else '불충족'}")
    lines.append("")

    lines.append("[P4] 신뢰는 나이보다 코딩 기간에 따라 더 달라진다")
    age_trust = []
    for age in AGES:
        s = shares([r for r in with_years if r["age"] == age])
        age_trust.append(s["trust"])
        lines.append(f"   {age}: n = {s['n']}, 신뢰 {s['trust']:.1f}%, 불신 {s['distrust']:.1f}%")
    age_range = max(age_trust) - min(age_trust)
    bin_trust = [t["trust"] for t in table]
    bin_range = max(bin_trust) - min(bin_trust)
    lines.append(f"   나이대 사이 최대-최소: {age_range:.1f}%p, 코딩 경력 구간 사이 최대-최소: {bin_range:.1f}%p")
    lines.append(f"P4: {'충족' if age_range < bin_range else '불충족'}")

    text = "\n".join(lines)
    print(text)
    with open(os.path.join(out_dir, "replication_2026.txt"), "w", encoding="utf-8") as f:
        f.write(text + "\n")
    with open(os.path.join(out_dir, "table_by_experience_2026.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["경력 구간", "응답자 수", NO_TRUST, LOW_RISK, VERIFY, MANY, MANY_IMPORTANT,
                    "신뢰 비율(%)", "조건부 비율(%)", "불신 비율(%)"])
        for t in table:
            w.writerow([t["bin"], t["n"], *[t["count"][k] for k in (NO_TRUST, LOW_RISK, VERIFY, MANY, MANY_IMPORTANT)],
                        f"{t['trust']:.1f}", f"{t['verify']:.1f}", f"{t['distrust']:.1f}"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
