"""2026 설문 자료의 예비 실행: 재확인에 쓸 열이 있는지와 응답 보기를 점검한다.

경력과 신뢰를 서로 견주는 계산(상관·교차표)은 하지 않는다.

사용법:  python pilot_check_2026.py <survey_results_public.csv 경로>
"""
import csv
import sys
from collections import Counter

KEYWORDS = ["YearsCode", "WorkExp", "AITrust", "AISelect", "AISent", "Age", "MainBranch", "Valid", "valid"]
EMPTY = {"", "NA"}


def main(path):
    csv.field_size_limit(10 ** 9)
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        chosen = [c for c in header if any(k in c for k in KEYWORDS)]
        print("열 개수:", len(header))
        print("점검할 열:", chosen)
        counts = {c: Counter() for c in chosen}
        rows = 0
        both = 0
        for row in reader:
            rows += 1
            for c in chosen:
                counts[c][(row[c] or "").strip()] += 1
            if ("YearsCode" in row and "AITrust" in row
                    and (row["YearsCode"] or "").strip() not in EMPTY
                    and (row["AITrust"] or "").strip() not in EMPTY):
                both += 1
    print("전체 행 수:", rows)
    print("YearsCode 와 AITrust 에 모두 값이 있는 행:", both)
    for c in chosen:
        values = counts[c]
        empty = sum(n for v, n in values.items() if v in EMPTY)
        print(f"\n[{c}] 서로 다른 값 {len(values)}개, 빈값 {empty}건")
        if len(values) <= 12:
            for value, n in values.most_common():
                print(f"  {n:>6}  {value!r}")
        else:
            numeric = [float(v) for v in values if v not in EMPTY and v.replace(".", "", 1).isdigit()]
            other = [v for v in values if v not in EMPTY and not v.replace(".", "", 1).isdigit()]
            if numeric:
                print(f"  숫자 범위: {min(numeric):g} ~ {max(numeric):g}")
            print(f"  숫자가 아닌 값 {len(other)}종, 예: {other[:5]}")


if __name__ == "__main__":
    main(sys.argv[1])
