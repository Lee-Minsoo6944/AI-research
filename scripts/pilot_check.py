"""예비 실행: 원자료의 기록 항목에 빠진 것이 없는지 점검한다.

경력과 신뢰를 서로 견주는 계산(상관·교차표)은 하지 않는다.
열이 있는지, 응답 보기가 무엇인지, 빈값이 몇 건인지만 본다.

사용법:  python pilot_check.py <results.csv 경로>
"""
import csv
import sys
from collections import Counter

COLUMNS = ["YearsCode", "WorkExp", "AIAcc", "AISent", "AISelect", "MainBranch", "Age"]
EMPTY = {"", "NA"}


def main(path):
    csv.field_size_limit(10 ** 9)
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        print("열 개수:", len(header))
        for c in COLUMNS:
            print(f"  {c}: {'있음' if c in header else '없음'}")
        counts = {c: Counter() for c in COLUMNS if c in header}
        rows = 0
        both = 0
        for row in reader:
            rows += 1
            for c in counts:
                counts[c][row[c].strip()] += 1
            if row["YearsCode"].strip() not in EMPTY and row["AIAcc"].strip() not in EMPTY:
                both += 1
    print("전체 행(응답자) 수:", rows)
    print("YearsCode 와 AIAcc 에 모두 값이 있는 행:", both)
    for c in ["AIAcc", "AISent", "AISelect", "MainBranch", "Age"]:
        print(f"\n[{c}] 응답 보기와 건수")
        for value, n in counts[c].most_common():
            print(f"  {n:>6}  {value!r}")
    for c in ["YearsCode", "WorkExp"]:
        values = counts[c]
        empty = sum(n for v, n in values.items() if v in EMPTY)
        numeric = {v: n for v, n in values.items() if v not in EMPTY and v.replace(".", "", 1).isdigit()}
        other = {v: n for v, n in values.items() if v not in EMPTY and v not in numeric}
        nums = [float(v) for v in numeric]
        print(f"\n[{c}] 빈값 {empty}건, 숫자 {sum(numeric.values())}건, 숫자가 아닌 값 {sum(other.values())}건")
        if nums:
            print(f"  숫자 범위: {min(nums):g} ~ {max(nums):g}")
        if other:
            print("  숫자가 아닌 값:", dict(sorted(other.items(), key=lambda kv: -kv[1])[:10]))


if __name__ == "__main__":
    main(sys.argv[1])
