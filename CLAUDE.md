# VTC Visualizer — 프로젝트 가이드

**브랜딩**: 사용자에게 보이는 이름은 "VTC Visualizer", 저작자 표기는 하단 카피라이트 "© mrc"로만.

CSV/JSON을 브라우저에서 논문 스타일 인터랙티브 그래프로 그리는 범용 벤치마크 시각화 도구.
여러 사람이 각자 데이터를 가져와 쓰는 도구이므로 **입력 계약의 안정성**과 **파일 하나로 배포 가능한 단순함**이 최우선이다.

## 파일 구조 (이 7개가 전부 — 파일을 늘리지 말 것)

| 파일 | 역할 |
|---|---|
| `index.html` | 메인 앱. **유일한 소스 코드** (HTML+CSS+JS 단일 파일, Plotly.js CDN) |
| `index-offline.html` | 자동 생성물. 직접 수정 금지 — `python visualizer.py build-offline`로 재생성 |
| `visualizer.py` | 보조 실행기: 로컬 서버(+폴더 자동 로드 API) 및 오프라인 빌더. CLI 출력은 영어 |
| `example.csv` | 예시 데이터 (4 method × 6 token budget = 24행, 중복 없음, 상식적 추세 내장) — 데모·문서용. 재생성 스크립트는 커밋하지 않음 |
| `README.md` | 사용자 문서 (한국어): 사용법, 입력 계약, 에이전트용 변환 요청문 |
| `README.en.md` | README.md의 영어 완역 — **내용 변경 시 두 README를 항상 함께 갱신** |
| `CLAUDE.md` | 이 파일 |

## 절대 규칙

- **단일 HTML 유지**: 빌드 도구, 프레임워크, npm, 외부 JS/CSS 파일 금지. vanilla JS만.
- **Plotly 버전 고정**: CDN URL(`plotly-2.35.2.min.js`)을 올리려면 전체 기능 검증 후에만.
- **Python은 표준 라이브러리만**, 문법은 **3.8 호환** (`X | None` 타입 표기 금지 — 실제로 3.9에서 깨진 적 있음).
- **`index.html` 수정 후에는 반드시 `python visualizer.py build-offline` 실행**해 `index-offline.html`을 재생성.
- **입력 계약(데이터 포맷)을 바꾸면 README.md와 README.en.md 양쪽의 "데이터 포맷"·"에이전트 요청문" 섹션을 함께 갱신** — 세 문서(계약·한/영 README)는 항상 동기화. 기능 추가/변경 시에도 두 README의 기능 표를 함께 갱신.
- 세션 하위 호환: `chartConfig`에 필드를 추가할 때는 `defaultChart()`에 기본값을 넣으면 된다
  (복원 시 `{...defaultChart(), ...saved}`로 병합되므로 이전 세션도 열린다). 기존 필드의 의미 변경/삭제는 금지.
- **i18n**: UI는 KO/EN 이중 언어(`I18N` 사전 + `t()`/`tf()`, 토글 = `#btnLangToggle`, 저장 키 `vtc-visualizer:lang`).
  **사용자에게 보이는 문자열을 추가하면 반드시 I18N 사전의 ko/en 양쪽에 키를 추가**하고 `t()`로 호출할 것.
  정적 HTML은 `data-i18n`/`data-i18n-ph` 속성 + `applyLang()`. 내부 식별자(`' 추세'` 접미사, `__fillbase`, `__trendband`)는 번역 금지.

## 입력 계약 (요약 — 전문은 README.md)

- CSV(헤더+행, TSV 허용) 또는 JSON 객체 배열. 필수 컬럼 없음. 한 행 = 한 측정점(long-form).
- 숫자 컬럼 자동 감지(→ 축), 문자열 컬럼은 그룹/필터 후보. `_source` 컬럼은 파일명으로 자동 부여(예약어).
- `_`로 시작하는 키는 내부용으로 예약: `_source`(출처, 데이터셋 2개 이상일 때만 UI 노출 — `visibleColumns()`),
  `_excluded`(테이블 체크박스로 그래프 제외된 행). `columns()`가 그 외 `_` 키를 걸러낸다.

## index.html 코드 지도

모든 코드는 하나의 `<script>` 안에 있고, 상태는 전역 `state = {datasets, charts, nextId}` 하나다.

- **팔레트/스타일 상수** (`PALETTE`, `SYMBOLS`, `CHROME`, `FONTS`): dataviz 스킬의 검증된 카테고리 팔레트(라이트 서피스).
  순서가 색약 안전성 장치이므로 **순서를 바꾸거나 색을 추가하려면 dataviz 스킬을 로드해 validator로 검증**할 것.
- **파싱**: `parseCSV` / `parseAny` / `coerce`(숫자 자동 변환)
- **데이터 모델**: `addDataset`, `allRows`(병합), `columns`, `numericColumns`, `uniqueVals`, `applyFilters`
  (필터 op: 카테고리 기본 `in` = 다중 선택 배열 값·빈 배열은 통과, 그 외 `=`,`≠`,`포함`; 숫자는 비교 연산. 값 미입력 필터는 무시)
- **차트 설정 스키마**: `defaultChart()` — 새 옵션은 여기에 필드 추가부터.
  주요 필드: `baselines[{x,y,shade}]`(다중), `textMarkers[{x,y,text,ax,ay}]`, `hiddenLabels[pointKey]`, `labelOffsets{key:{ax,ay}}`,
  `group2`(마커 모양 2차 그룹 — 시리즈는 `seriesDefs()`가 (group×group2) 콤보로 생성, 색=colorIdx·모양=symIdx, trace에 `_g`/`_g2` 메타),
  `trend`(none|linear|poly2|log|exp|power|movavg — 시리즈별 피팅, `trendTraces`/`linreg`/`poly2fit`) + `trendDash`/`trendWidth` + `trendBand`(none|1|2 — 잔차 ±kσ `__trendband` 음영 trace 쌍),
  `tmFontSize`/`tmColor`/`tmBg`/`tmArrow`(텍스트 마커 전역 스타일, `textMarkers[i].color/.size`로 개별 오버라이드),
  `lineShape`(linear|spline), `lineDash`(전역 선 종류, 시리즈별 `seriesStyles[name].dash`/`lwidth`로 오버라이드),
  `areaFill`(none|tozeroy — 실제 구현은 데이터 최소값 바닥의 `__fillbase` 보조 trace + `tonexty` 파스텔 밴드; 축이 0으로 늘어나지 않게 하기 위함)
- **렌더링**: `buildTraces`(시리즈→trace), `buildLayout`(축/폰트/범례 — 축 범위는 min/max 한쪽만 입력해도 데이터 범위로 보완;
  `uirevision`이 축·범위·스케일 키로 구성돼 스타일 변경 시 줌 유지), `buildAnnotations`(포인트 레이블: 중복 제거→그리디 겹침 회피→텍스트 마커, `_kind`로 구분),
  `baselineShapes`(베이스라인 배열→점선+사분면 음영), `paretoTrace`, 그리고 `renderPlot`(Plotly.react + 이벤트 바인딩)
  - **주의**: `renderPlot`에서 플롯이 이미 있는 div의 innerHTML을 지우면 안 된다(placeholder일 때만 지움) —
    지우면 Plotly.react가 증분 업데이트만 해서 화면이 빈 채로 남는다 (실제 있었던 버그)
- **설정 UI**: `buildCfgPanel` — 그룹(details)별 입력 위젯. 새 옵션의 UI는 여기에. 동적 목록(베이스라인/마커/숨긴 레이블)은 `cfg._refreshLists()`로 갱신
- **이벤트**: `plotly_click` → `showPointPopover`(베이스라인 추가/제거 · 포인트 제외(`_excluded`, 전 차트 공통) · 텍스트 마커 추가 메뉴),
  `plotly_clickannotation` → 포인트 레이블 개별 숨김 / 텍스트 마커 편집(`showMarkerEditPopover`),
  `plotly_relayout` → 주석 드래그 오프셋 저장(`_kind`별로 `labelOffsets` 또는 `textMarkers`) 및 줌 시 음영 재계산
- **테이블**: `renderTable` (검색/정렬/페이지네이션 200행, 행 앞 체크박스로 `_excluded` 토글 → 전 차트에서 제외)
- **세션**: `save`(debounce→localStorage), `exportSession`/`restoreSession`, 키 `vtc-visualizer:session`
  (구 키 `visualizer-by-mrc:session`은 `loadSaved()`가 읽어 자동 마이그레이션)
- **서버 연동**: `tryServerAutoload` — `api/files`/`api/file` (http로 열렸을 때만)

새 차트 옵션 추가 절차: `defaultChart()`에 필드 → `buildCfgPanel`에 입력 UI → `buildTraces`/`buildLayout`에 반영 → 세션 저장은 자동.

주의: Plotly에서 로그축의 shape/annotation 좌표는 log10 값이어야 한다 — `axCoord()` 헬퍼를 거칠 것.

## 차트 스타일 작업 시

색상·팔레트·마커 등 시각 스타일을 바꾸는 작업이면 **먼저 `dataviz` 스킬을 로드**하고 그 규칙(팔레트 검증, 마크 스펙, 안티패턴)을 따를 것.

## 검증 방법

```bash
# 1) 서버 + 샘플 폴더 (샘플은 README의 CSV 예시로 만들면 됨)
python3 visualizer.py <샘플폴더> --port 8642
curl -s http://127.0.0.1:8642/api/files          # 파일 목록 확인
# 2) 브라우저에서: 자동 로드, 산점도, 로그축, 포인트 클릭 베이스라인, 레이블 드래그,
#    차트 추가, 테이블 검색/정렬, PNG 내보내기, 새로고침 후 세션 복원 확인
# 3) 오프라인 빌드 후 index-offline.html을 네트워크 차단 상태로 열어 렌더 확인
python3 visualizer.py build-offline
```

헤드리스 검증이 필요하면 puppeteer-core + 시스템 Chrome으로 `state`/`plotDivs` 전역을 evaluate하는 방식이 쉽다
(전역이 의도적으로 노출되어 있음).
