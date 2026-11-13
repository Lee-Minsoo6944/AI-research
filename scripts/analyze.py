"""본 분석: 코딩 경력(YearsCode)과 AI 정확도 신뢰(AIAcc)의 관계.

판정 기준은 research/01-hypothesis.md 5절, 설계는 research/03-design.md 에 적힌 대로이다.
파이썬 표준 라이브러리만 쓴다(추가 설치 없음).

사용법:  python analyze.py <results.csv 경로> <결과를 쓸 폴더>
"""
import csv
import math
import os
import sys

TRUST = {
    "Highly distrust": 1,
    "Somewhat distrust": 2,
    "Neither trust nor distrust": 3,
    "Somewhat trust": 4,
    "Highly trust": 5,
}
SENTIMENT = {  # 'Unsure' 는 순서를 정할 수 없어 제외한다
    "Very unfavorable": 1,
    "Unfavorable": 2,
    "Indifferent": 3,
    "Favorable": 4,
    "Very favorable": 5,
}
BINS = [("1-4년", 1, 4), ("5-9년", 5, 9), ("10-19년", 10, 19), ("20년 이상", 20, 10 ** 9)]
RHO_THRESHOLD = -0.05
ALPHA = 0.05
MAX_PLAUSIBLE_YEARS = 50  # 민감도 분석용(03-design.md 6절)


def number(text):
    text = text.strip()
    try:
        return float(text)
    except ValueError:
        return None


def ranks(values):
    """같은 값에는 평균 순위를 준다."""
    order = sorted(range(len(values)), key=values.__getitem__)
    result = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        average = (i + j) / 2 + 1
        for k in range(i, j + 1):
            result[order[k]] = average
        i = j + 1
    return result


def spearman(pairs):
    """(x, y) 쌍의 스피어만 순위상관 = 순위끼리의 피어슨 상관."""
    n = len(pairs)
    rx = ranks([p[0] for p in pairs])
    ry = ranks([p[1] for p in pairs])
    mx = sum(rx) / n
    my = sum(ry) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sxx = sum((a - mx) ** 2 for a in rx)
    syy = sum((b - my) ** 2 for b in ry)
    return sxy / math.sqrt(sxx * syy)


def lower_tail_p(rho, n):
    """귀무가설 rho >= 0 에 대한 한쪽 p 값(t 통계량의 정규 근사, n 이 클 때)."""
    t = rho * math.sqrt((n - 2) / (1 - rho * rho))
    return 0.5 * math.erfc(-t / math.sqrt(2))


def interval(rho, n):
    """피셔 z 변환으로 구한 근사 95% 신뢰구간."""
    z = math.atanh(rho)
    half = 1.96 / math.sqrt(n - 3)
    return math.tanh(z - half), math.tanh(z + half)


def describe(label, pairs):
    n = len(pairs)
    rho = spearman(pairs)
    p = lower_tail_p(rho, n)
    low, high = interval(rho, n)
    p_text = "< 1e-300" if p == 0 else f"{p:.3g}"
    line = f"{label}: n = {n}, rho = {rho:.4f}, 근사 95% 구간 [{low:.4f}, {high:.4f}], 한쪽 p = {p_text}"
    return rho, p, line


def load(path):
    csv.field_size_limit(10 ** 9)
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            rows.append({
                "years": number(row["YearsCode"]),
                "work": number(row["WorkExp"]),
                "trust": TRUST.get(row["AIAcc"].strip()),
                "sentiment": SENTIMENT.get(row["AISent"].strip()),
                "ai_user": row["AISelect"].strip().startswith("Yes"),
            })
    return rows


def bin_table(rows):
    table = []
    for name, low, high in BINS:
        scores = [r["trust"] for r in rows if low <= r["years"] <= high]
        n = len(scores)
        counts = [scores.count(k) for k in (1, 2, 3, 4, 5)]
        table.append({
            "bin": name,
            "n": n,
            "counts": counts,
            "trust_pct": 100 * (counts[3] + counts[4]) / n,
            "distrust_pct": 100 * (counts[0] + counts[1]) / n,
            "mean": sum(scores) / n,
        })
    return table


def write_table(table, path):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["경력 구간", "응답자 수", "Highly distrust", "Somewhat distrust",
                    "Neither trust nor distrust", "Somewhat trust", "Highly trust",
                    "신뢰 비율(%)", "불신 비율(%)", "평균 점수(1-5)"])
        for t in table:
            w.writerow([t["bin"], t["n"], *t["counts"],
                        f"{t['trust_pct']:.1f}", f"{t['distrust_pct']:.1f}", f"{t['mean']:.3f}"])


def write_figure(table, path):
    width, height, left, top, plot_h = 720, 420, 70, 60, 280
    group_w = (width - left - 30) / len(table)
    bar_w = 54
    top_value = 60
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" font-family="sans-serif">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        '<text x="70" y="28" font-size="17" font-weight="bold" fill="#1a1a1a">코딩 경력 구간별 AI 정확도 신뢰·불신 비율</text>',
        '<rect x="470" y="14" width="14" height="14" fill="#2a78d6"/><text x="490" y="26" font-size="13" fill="#1a1a1a">신뢰</text>',
        '<rect x="540" y="14" width="14" height="14" fill="#d9822b"/><text x="560" y="26" font-size="13" fill="#1a1a1a">불신</text>',
    ]
    for tick in range(0, top_value + 1, 10):
        y = top + plot_h - plot_h * tick / top_value
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width - 30}" y2="{y:.1f}" stroke="#dddddd"/>')
        parts.append(f'<text x="{left - 8}" y="{y + 4:.1f}" font-size="12" text-anchor="end" fill="#555555">{tick}%</text>')
    for i, t in enumerate(table):
        center = left + group_w * (i + 0.5)
        for offset, key, color in ((-bar_w - 2, "trust_pct", "#2a78d6"), (2, "distrust_pct", "#d9822b")):
            value = t[key]
            h = plot_h * min(value, top_value) / top_value
            x = center + offset
            y = top + plot_h - h
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w}" height="{h:.1f}" fill="{color}"/>')
            parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{y - 6:.1f}" font-size="12" text-anchor="middle" fill="#1a1a1a">{value:.1f}%</text>')
        parts.append(f'<text x="{center:.1f}" y="{top + plot_h + 22}" font-size="13" text-anchor="middle" fill="#1a1a1a">{t["bin"]}</text>')
        parts.append(f'<text x="{center:.1f}" y="{top + plot_h + 40}" font-size="11" text-anchor="middle" fill="#555555">n = {t["n"]}</text>')
    parts.append(f'<text x="{left}" y="{height - 12}" font-size="11" fill="#555555">신뢰 = Somewhat/Highly trust, 불신 = Somewhat/Highly distrust. 자료: Stack Overflow Developer Survey 2025</text>')
    parts.append("</svg>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))


def main(path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    rows = load(path)
    lines = []
    total = len(rows)
    no_years = sum(1 for r in rows if r["years"] is None)
    no_trust = sum(1 for r in rows if r["trust"] is None)
    main_rows = [r for r in rows if r["years"] is not None and r["trust"] is not None]
    lines.append(f"전체 응답자: {total}")
    lines.append(f"YearsCode 빈값: {no_years}, AIAcc 빈값: {no_trust}")
    lines.append(f"분석 대상(두 문항 모두 응답): {len(main_rows)}, 제외: {total - len(main_rows)}")
    lines.append("")

    lines.append("[주 분석] 판정에 쓰는 유일한 분석")
    rho, p, line = describe("YearsCode x AIAcc", [(r["years"], r["trust"]) for r in main_rows])
    lines.append(line)
    if rho >= 0:
        verdict = "반증 (rho >= 0)"
    elif rho <= RHO_THRESHOLD and p < ALPHA:
        verdict = f"지지 (rho <= {RHO_THRESHOLD} 이고 p < {ALPHA})"
    else:
        verdict = f"지지되지 않음 (방향만 일치: {RHO_THRESHOLD} < rho < 0 또는 p >= {ALPHA})"
    lines.append(f"판정: {verdict}")
    lines.append("")

    lines.append("[보조 분석] 판정에 쓰지 않음")
    table = bin_table(main_rows)
    lines.append("1) 경력 구간별 신뢰·불신 비율")
    for t in table:
        lines.append(f"   {t['bin']}: n = {t['n']}, 신뢰 {t['trust_pct']:.1f}%, 불신 {t['distrust_pct']:.1f}%, 평균 점수 {t['mean']:.3f}")
    _, _, line = describe("2) WorkExp x AIAcc", [(r["work"], r["trust"]) for r in rows
                                                if r["work"] is not None and r["trust"] is not None])
    lines.append(line)
    _, _, line = describe("3) YearsCode x AISent", [(r["years"], r["sentiment"]) for r in rows
                                                   if r["years"] is not None and r["sentiment"] is not None])
    lines.append(line)
    lines.append("")

    lines.append("[민감도 분석] 예비 실행 뒤에 추가함(03-design.md 6절), 판정에 쓰지 않음")
    _, _, line = describe(f"4) YearsCode <= {MAX_PLAUSIBLE_YEARS} 만",
                          [(r["years"], r["trust"]) for r in main_rows if r["years"] <= MAX_PLAUSIBLE_YEARS])
    lines.append(line)
    _, _, line = describe("5) AI 도구를 쓰는 응답자만",
                          [(r["years"], r["trust"]) for r in main_rows if r["ai_user"]])
    lines.append(line)

    text = "\n".join(lines)
    print(text)
    with open(os.path.join(out_dir, "summary.txt"), "w", encoding="utf-8") as f:
        f.write(text + "\n")
    write_table(table, os.path.join(out_dir, "table_by_experience.csv"))
    write_figure(table, os.path.join(out_dir, "figure_trust_by_experience.svg"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
