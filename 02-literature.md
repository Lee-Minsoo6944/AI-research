# 과제 10 — 2단계: 선행 연구와 인용 근거 검증

> 작성일: 2026-11-13 · 가설: **개발자는 코딩 경력(연수)이 길수록 AI 도구 출력의 정확도를 신뢰하는 정도가 낮다.** ([01-hypothesis.md](01-hypothesis.md))
> 이 문서의 문헌은 AI(Claude)가 기억으로 낸 목록을 **하나씩 원출처에서 대조**한 결과입니다. 대조하지 못한 문헌·주장은 근거로 쓰지 않고 4절에 따로 적었습니다.

---

## 1. 출처 검증 방법 (T10-C20)

AI가 낸 문헌 목록은 지어낸 것(환각)일 수 있으므로, 문헌마다 아래 순서로 확인했습니다. 확인한 날은 모두 2026-11-13 입니다.

1. **실재·서지 확인** — 학술지·학회 논문은 DOI 등록 기관(Crossref)의 등록 정보(Crossref 가 공개하는 DOI 별 등록 정보)에서, 사전 공개 논문은 arXiv 초록 페이지에서 **제목·저자 전원·연도·게재처·권호·쪽**을 AI가 말한 것과 대조했습니다.
2. **내용 확인** — 초록을 Crossref 등록 초록, arXiv 초록 페이지, 미국 국립과학재단 공개 저장소(NSF PAR), 학술 색인(RePEc) 가운데 열리는 곳에서 읽고, AI가 말한 "이 논문의 결과"가 초록에 실제로 있는지 확인했습니다.
3. **다르면 기록** — AI의 기억과 초록이 다르거나 초록에서 확인되지 않는 주장은 쓰지 않고 4절에 남겼습니다.
4. **기관 자료** — 설문 보고서는 스택오버플로 공식 사이트의 해당 페이지를 직접 열어 숫자를 확인했습니다.

한계: 확인은 초록과 서지 정보 수준입니다. 논문 본문 전체를 읽은 것은 아니므로, 초록에 없는 세부 결과는 인용하지 않았습니다. 영어 초록은 AI가 요약했고, 숫자는 초록 원문 기준으로 적었습니다.

**내가 직접 확인할 것** — 2026-11-13 확인함

- [x] 2절 표의 링크를 하나씩 열어 제목·저자·연도가 맞는지 봄.
- [x] 가설과 가장 가까운 두 편(Logg 외 2019, Brynjolfsson 외 2025)의 초록을 직접 읽고 3절의 한 줄 요약이 맞는지 확인.

---

## 2. 참고문헌 목록 (T10-C11, C12, C13, C19)

표기 형식은 APA 7판으로 통일했습니다(저자. (연도). 제목. 출처. DOI 또는 URL). 학술지·학회 논문의 DOI 는 주소가 아닌 식별자로 적었습니다.

1. Becker, J., Rush, N., Barnes, E., & Rein, D. (2025). *Measuring the impact of early-2025 AI on experienced open-source developer productivity*. arXiv. https://arxiv.org/abs/2507.09089
2. Brynjolfsson, E., Li, D., & Raymond, L. (2025). Generative AI at work. *The Quarterly Journal of Economics, 140*(2), 889–942. DOI: 10.1093/qje/qjae044
3. Logg, J. M., Minson, J. A., & Moore, D. A. (2019). Algorithm appreciation: People prefer algorithmic to human judgment. *Organizational Behavior and Human Decision Processes, 151*, 90–103. DOI: 10.1016/j.obhdp.2018.12.005
4. Noy, S., & Zhang, W. (2023). Experimental evidence on the productivity effects of generative artificial intelligence. *Science, 381*(6654), 187–192. DOI: 10.1126/science.adh2586
5. Peng, S., Kalliamvakou, E., Cihon, P., & Demirer, M. (2023). *The impact of AI on developer productivity: Evidence from GitHub Copilot*. arXiv. https://arxiv.org/abs/2302.06590
6. Perry, N., Srivastava, M., Kumar, D., & Boneh, D. (2023). Do users write more insecure code with AI assistants? In *Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security (CCS '23)* (pp. 2785–2799). https://arxiv.org/abs/2211.03622
7. Stack Overflow. (2025a). *2025 Developer Survey: AI*. Stack Exchange Inc. https://survey.stackoverflow.co/2025/ai
8. Stack Overflow. (2025b). *2025 Developer Survey: Methodology*. Stack Exchange Inc. https://survey.stackoverflow.co/2025/methodology
9. Vaithilingam, P., Zhang, T., & Glassman, E. L. (2022). Expectation vs. experience: Evaluating the usability of code generation tools powered by large language models. In *CHI Conference on Human Factors in Computing Systems Extended Abstracts (CHI EA '22)* (pp. 1–7). DOI: 10.1145/3491101.3519665
10. Wang, R., Cheng, R., Ford, D., & Zimmermann, T. (2024). Investigating and designing for trust in AI-powered code generation tools. In *Proceedings of the 2024 ACM Conference on Fairness, Accountability, and Transparency (FAccT '24)*. https://arxiv.org/abs/2305.11248

---

## 3. 문헌별 확인 결과와 가설과의 연결 (T10-C14, C16)

| # | 문헌 | 연구 종류 | 어디서 확인했나 | 확인한 내용(초록 기준) | 가설의 어느 부분과 이어지나 |
|---|---|---|---|---|---|
| 3 | Logg 외 (2019) | **실험** 6개 | 서지: Crossref / 초록: 학술 색인(RePEc) | 일반인은 사람보다 알고리즘의 조언을 더 따랐지만, 예측을 직업으로 하는 숙련자는 일반인보다 알고리즘 조언에 덜 의존했다(실험 4). | **"경력이 길수록 덜 신뢰한다"는 방향의 직접 근거** — 다만 대상이 개발자·생성형 AI가 아니라 예측 전문가·알고리즘 조언이다. |
| 2 | Brynjolfsson 외 (2025) | **현장 데이터**(상담원 5,172명, 단계적 도입) | 서지·초록: Crossref | AI 도우미로 생산성이 평균 15% 올랐고, 경력·숙련도가 낮은 상담원은 속도와 품질이 모두 좋아졌지만 가장 숙련된 상담원은 속도 향상이 작고 품질은 조금 떨어졌다. | **왜 경력에 따라 신뢰가 다를 수 있는지** — 경험이 적을수록 AI에서 얻는 것이 많다. 대상은 개발자가 아니라 고객 상담원이다. |
| 4 | Noy & Zhang (2023) | **무작위 실험**(453명, 사전 등록) | 서지·초록: Crossref | ChatGPT를 쓴 집단은 글쓰기 과제 시간이 약 40% 줄고 품질이 약 18% 올랐으며, 참가자 사이의 격차가 줄었다. | 위와 같은 맥락 — AI의 도움이 능력이 낮은 쪽에 더 커서 격차가 줄어든다는 실험 근거. 글쓰기 과제이며 경력 변수는 아니다. |
| 5 | Peng 외 (2023) | **통제 실험** | 서지·초록: arXiv | GitHub Copilot 을 쓴 집단이 코딩 과제를 55.8% 더 빨리 끝냈고, 효과가 사람마다 달랐다(heterogeneous effects). | **대상이 개발자**인 실험 — AI 도구가 개발 작업에 실제 효과가 있고 그 크기가 개발자마다 다르다는 배경. |
| 1 | Becker 외 (2025) | **무작위 실험**(숙련 개발자 16명, 과제 246개) | 서지·초록: arXiv | 숙련 오픈소스 개발자는 AI를 허용했을 때 작업 시간이 19% 늘었는데, 본인들은 20% 줄었다고 느꼈다. | **경력이 긴 개발자에게는 AI가 덜 도움이 될 수 있다**는 근거. 동시에 숙련자도 AI의 효과를 실제보다 좋게 느꼈다는 점은 **가설과 반대 방향일 수 있는 근거**이다. |
| 6 | Perry 외 (2023) | **사용자 실험** | 서지·초록: arXiv | AI 도우미를 쓴 참가자가 보안성이 더 낮은 코드를 쓰면서도 안전하게 썼다고 더 믿었고, AI를 덜 신뢰한 참가자의 코드에 취약점이 더 적었다. | **'AI 출력에 대한 신뢰'가 결과물의 질과 관련된 중요한 변수**라는 근거 — 이 연구가 신뢰를 종속변수로 잡은 이유. |
| 9 | Vaithilingam 외 (2022) | **사용자 실험**(24명, 피험자 내 설계) | 서지: Crossref / 초록: NSF PAR | Copilot 이 과제 완료 시간·성공률을 꼭 높이지는 않았지만 대다수가 Copilot 을 선호했고, 생성된 코드를 이해·수정·디버깅하는 데 어려움을 겪었다. | **도구에 대한 호감과 실제 성과가 다를 수 있다**는 근거 — 보조 분석에서 신뢰(`AIAcc`)와 호감(`AISent`)을 따로 보는 이유. |
| 10 | Wang 외 (2024) | 질적 연구(개발자 17명 인터뷰 등) | 서지·초록: arXiv | 개발자가 AI 코드 생성 도구에 적절한 신뢰를 갖기 어렵게 하는 세 가지(기대 설정, 도구 설정, 제안 검증)를 찾았다. | **개발자의 AI 신뢰가 연구 대상이 되는 개념**이라는 배경. 숫자로 검증한 연구는 아니다. |
| 7 | Stack Overflow (2025a) | 설문 보고서(기관) | 공식 사이트 | AI 정확도 신뢰 문항 응답자 33,244명(전체의 67.8%). 전체 비율: Highly trust 3.1%, Somewhat trust 29.6%, Somewhat distrust 26.1%, Highly distrust 19.6%. | **종속변수(`AIAcc`)의 출처와 전체 분포** — 이 연구가 분석할 자료의 공식 요약. |
| 8 | Stack Overflow (2025b) | 조사 방법 설명(기관) | 공식 사이트 | 조사 기간 2025-05-29~06-23, 177개국 49,009건 응답. 응답자는 주로 스택오버플로가 운영하는 채널로 모집. | **자료의 범위와 한계** — 자발적 응답이라 전체 개발자를 대표하지 않는다. |

- **실험이나 데이터로 검증된 연구(T10-C16)**: 1, 2, 3, 4, 5, 6, 9번.
- 7번에서 확인한 네 보기의 합은 78.4%입니다. 나머지 21.6%에 해당하는 보기(중립 보기로 추정)는 보고서 페이지에 문구가 보이지 않아, **원자료에서 보기 종류를 확인한 뒤** 점수표를 확정합니다(3단계).

---

## 4. 걸러낸 문헌·주장과 이유 (T10-C15)

| 걸러낸 것 | 확인 결과 | 제외 이유 |
|---|---|---|
| Dietvorst, Simmons, & Massey (2015), "Algorithm aversion", *Journal of Experimental Psychology: General, 144*(1), 114–126 | 실재하고 서지는 Crossref 에서 확인됨. 초록은 열어 보지 못함. | 초록을 직접 확인하지 못했고, 내용(알고리즘의 실수를 본 뒤의 회피)이 "경력"과 직접 이어지지 않습니다. |
| "Peng 외 (2023)에서 경험이 적은 개발자가 더 큰 도움을 받았다"는 주장 | AI가 기억으로 말했지만 **초록에는 없는 내용**. 2차 요약 글에서만 보였고 요약 글끼리 세부 내용이 서로 달랐음. | 원문에서 확인하지 못한 주장이라 쓰지 않습니다. 문헌 자체는 초록에 있는 내용(55.8% 단축, 효과가 사람마다 다름)만 인용합니다. |
| The Decoder 기사 (2025), "경력 많은 개발자의 20%가 AI를 강하게 불신" | 기사는 실재하나 2차 보도이고, 경력별 수치의 원출처를 공식 보고서에서 찾지 못함. | 근거로 쓰지 않습니다. 이 내용은 이번 연구가 원자료로 직접 계산해 확인할 대상입니다. |
| Cui 외 (2025), 개발자 대상 현장 실험 3건 | 검색 요약에서 이름만 확인. 원문·서지를 확인하지 못함. | 실재와 내용을 확인하지 못해 제외합니다. |
| Kahneman & Tversky (1979), Buehler, Griffin, & Ross (1994) — 계획 오류 | 원문 확인을 하지 않음. | 처음 검토한 주제(다이어리 예상 시간)용 문헌이며, 주제를 바꾸면서 가설과 관련이 없어졌습니다. |

---

## 5. 알려진 사실과 이번 연구의 주장 (T10-C17)

**선행 연구에서 확인된 사실** (위 표의 초록에서 확인한 것만)

- 생성형 AI 도구는 실험에서 글쓰기·코딩 과제의 수행 시간을 줄였다(Noy & Zhang, 2023; Peng 외, 2023).
- AI의 도움은 경력·숙련도가 낮은 사람에게 더 컸고, 가장 숙련된 사람에게는 작거나 품질이 조금 떨어졌다(Brynjolfsson 외, 2025). 사람 사이의 격차도 줄었다(Noy & Zhang, 2023).
- 숙련 오픈소스 개발자는 AI를 썼을 때 실제로는 더 느려졌지만 스스로는 빨라졌다고 느꼈다(Becker 외, 2025).
- 예측을 직업으로 하는 숙련자는 일반인보다 알고리즘의 조언에 덜 의존했다(Logg 외, 2019).
- AI 도우미를 쓴 사람은 덜 안전한 코드를 쓰면서 더 안전하다고 믿었고, AI를 덜 신뢰한 사람의 코드에 취약점이 적었다(Perry 외, 2023). 도구에 대한 선호와 실제 성과는 다를 수 있다(Vaithilingam 외, 2022).
- 개발자가 AI 코드 생성 도구에 적절한 신뢰를 갖는 데에는 어려움이 있다(Wang 외, 2024).
- 2025년 스택오버플로 설문에서 AI 정확도를 "Highly trust"한다는 응답은 3.1%, "Highly distrust"는 19.6%였다(Stack Overflow, 2025a).

**이번 연구의 주장** (아직 검증되지 않았고, 이번에 원자료로 확인할 것)

- 스택오버플로 2025 설문 응답자 안에서, **코딩 경력 연수와 AI 정확도 신뢰 점수 사이에 음의 순위상관(ρ ≤ −0.05)이 있다.**

**둘 사이의 간격**

- 선행 연구가 보여 준 것은 주로 "AI의 **도움 크기**가 경력에 따라 다르다"와 "다른 분야 숙련자가 알고리즘 조언에 덜 의존한다"입니다. "개발자의 **신뢰**가 경력에 따라 다르다"를 이 설문 원자료로 직접 계산한 학술 문헌은 이번 검색 범위에서 확인하지 못했습니다.
- 검색 범위는 AI가 제시한 문헌과 그 주변 검색 결과로 한정되며, 체계적 문헌 검색은 아닙니다. 이 점은 논문의 한계에 적습니다.
- 이번 연구는 한 시점의 설문이므로, 관계가 확인되더라도 "경력이 신뢰를 낮춘다"는 인과가 아니라 "경력이 긴 응답자일수록 신뢰 점수가 낮은 경향이 있다"까지만 말합니다.

---

## 6. 본문 인용과 목록의 대응 (T10-C18)

이 문서 본문(3절·5절)에서 근거로 인용한 문헌은 Becker 외(2025), Brynjolfsson 외(2025), Logg 외(2019), Noy & Zhang(2023), Peng 외(2023), Perry 외(2023), Stack Overflow(2025a, 2025b), Vaithilingam 외(2022), Wang 외(2024)의 10건이며, 모두 2절 목록에 있습니다. 4절의 문헌은 근거로 쓰지 않았으므로 목록에 넣지 않았습니다. 논문 본문을 쓸 때도 2절 목록에 있는 문헌만 인용합니다.

---

## 남길 것 (요약)

- **참고문헌 목록**: 2절의 10건.
- **문헌별 연결 한 줄**: 3절 표의 마지막 열.
- **걸러낸 항목**: 4절의 5건(문헌 4건, 주장 1건).
