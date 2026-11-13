# 과제 10 재현 패키지 — 코딩 경력과 AI 도구 출력에 대한 신뢰의 관계

- 작성자: 이민수 · 작성일: 2026-11-13
- 논문: [paper/paper.pdf](paper/paper.pdf) (원본 `paper/paper.html`)
- 가설: 개발자는 코딩 경력(연수)이 길수록 AI 도구 출력의 정확도를 신뢰하는 정도가 낮다.
- 결과 한 줄: 2025년 설문에서는 약한 음의 관계가 있어 가설이 지지되었고(ρ = −0.1336, n = 32,924), 문항이 다른 2026년 설문에서는 재현되지 않았다(ρ = +0.0137, n = 7,158).

## 짧은 확인 방법

Python 3.9 이상만 있으면 됩니다(추가 설치 없음). 이 폴더에서 아래 명령 하나를 실행합니다.

```bash
python scripts/verify.py
```

1. 원자료 두 파일의 SHA-256 이 아래 표의 값과 같은지 확인합니다.
2. 본 분석, 탐색 분석, 2026년 추가 검증을 `results_check` 폴더에 다시 실행합니다.
3. 제출한 `results` 폴더의 파일과 한 글자도 다르지 않은지 견줍니다.

마지막 줄에 `재현 확인: 모두 일치`가 나오면 됩니다. 출력의 `분석 대상(두 문항 모두 응답): 32924` 와 `rho = -0.1336` 이 논문 표 6과 같은지 보면 됩니다. 실행에는 1분 안팎이 걸립니다.

## 하나씩 실행하기

```bash
python scripts/pilot_check.py data/raw/results.csv
python scripts/analyze.py data/raw/results.csv results_check
python scripts/explore.py data/raw/results.csv results_check
python scripts/pilot_check_2026.py data/raw2026/survey_results_public.csv
python scripts/replicate_2026.py data/raw2026/survey_results_public.csv results_check
```

## 원자료

| | 2025년 (주 분석) | 2026년 (추가 검증) |
|---|---|---|
| 자료 | Stack Overflow Developer Survey 2025 공개 응답 자료 | Stack Overflow Developer Survey 2026 공개 응답 자료 |
| 제공 기관·라이선스 | Stack Exchange Inc., ODbL 1.0 | Stack Exchange Inc., ODbL 1.0 |
| 출처 | https://github.com/StackExchange/Survey/tree/main/packages/archive/2025 | https://github.com/StackExchange/Survey/tree/main/packages/archive/2026 |
| 내려받은 날(접근일) | 2026-11-13 11:37 (KST) | 2026-11-13 11:44 (KST) |
| 파일 | `data/raw/results.csv` (49,191행), `data/raw/schema.csv` | `data/raw2026/survey_results_public.csv` (30,903행), `data/raw2026/survey_results_schema.csv` |
| SHA-256 (응답 파일) | `2d1f65308877282edfb4470520eabbc08cb499118432a3dcec6a66c086aa2baa` | `ad520b4d5d71f240141e63f0d6f81a3b1898cbdc69efe9ea985496533b15fc2c` |

원자료는 내려받은 그대로이며 고치지 않았습니다. 직접 다시 받으려면 위 출처의 같은 이름 파일을 내려받아 같은 폴더에 넣으면 됩니다(로그인 없음).

## 파일 구성

| 위치 | 내용 |
|---|---|
| `paper/paper.pdf`, `paper/paper.html`, `paper/figure_trust_by_experience.svg` | 논문과 원본, 그림 |
| `data/raw/`, `data/raw2026/` | 원자료와 문항 설명 |
| `data/pilot_output.txt`, `data/pilot_output_2026.txt` | 예비 실행 출력 |
| `scripts/pilot_check.py`, `scripts/pilot_check_2026.py` | 예비 실행(열·응답 보기·빈값 점검) |
| `scripts/analyze.py` | 본 분석(가설 판정) |
| `scripts/explore.py` | 탐색 분석(본 분석 뒤에 추가, 판정에 쓰지 않음) |
| `scripts/replicate_2026.py` | 2026년 자료를 쓴 추가 검증 |
| `scripts/verify.py` | 재현 확인 |
| `results/summary.txt`, `results/table_by_experience.csv`, `results/figure_trust_by_experience.svg` | 본 분석 출력, 구간별 표, 그림 |
| `results/exploratory.txt` | 탐색 분석 출력 |
| `results/replication_2026.txt`, `results/table_by_experience_2026.csv` | 추가 검증 출력, 구간별 표 |
| `results/prerun_hashes.txt`, `results/prerun_hashes_2026.txt` | 본 분석·추가 검증 실행 직전의 문서·스크립트 해시 |
| `01-hypothesis.md` ~ `05-replication.md` | 단계별 작업 기록(가설, 선행 연구, 설계, 결과, 추가 검증) |

`results/prerun_hashes.txt` 의 해시는 실행 직전 상태의 값입니다. 그 뒤 단계 문서에는 직접 확인 표시가 더해졌고, `02-literature.md` 는 DOI 표기를 주소에서 식별자로 바꿨으며 `03-design.md` 에는 설계 변경 기록이 더해졌으므로, 단계 문서의 지금 해시는 기록된 값과 다릅니다. 스크립트와 원자료의 해시는 그대로입니다.

## AI와 나의 판단 3줄

1. AI에게는 후보 주제와 공개 자료 찾기, 문헌의 실재 확인, 분석 스크립트 작성과 실행, 문서 초안을 맡겼다.
2. 나는 직접 실험 대신 공개 데이터 분석으로 방법을 정하고, 주제 범위를 넓혀 최종 가설을 확정했으며, 원자료 내려받기·본 분석 실행·2026년 재확인을 단계마다 결정했다.
3. AI가 기억으로 말한 내용 가운데 원출처와 다른 것(초록에 없던 문헌 내용, 예상과 달랐던 2026년 문항)은 쓰지 않았고, 가설이 재현되지 않은 결과도 고치지 않고 그대로 실었다.
