# VTC Visualizer — 프로젝트 가이드

**브랜딩**: 사용자에게 보이는 이름은 "VTC Visualizer", 저작자 표기는 하단 카피라이트 "© mrc"로만.

CSV/JSON을 브라우저에서 논문 스타일 인터랙티브 그래프로 그리는 범용 벤치마크 시각화 도구.
여러 사람이 각자 데이터를 가져와 쓰는 도구이므로 **입력 계약의 안정성**과 **파일 하나로 배포 가능한 단순함**이 최우선이다.

## 파일 구조 (소스·문서는 이 9개가 전부 — 파일을 늘리지 말 것. 예외: `assets/guide/`는 가이드 예시 이미지 전용 폴더)

| 파일 | 역할 |
|---|---|
| `index.html` | 메인 앱. **유일한 소스 코드** (HTML+CSS+JS 단일 파일, Plotly.js CDN) |
| `index-offline.html` | 자동 생성물. 직접 수정 금지 — `python visualizer.py build-offline`로 재생성 |
| `visualizer.py` | 보조 실행기: 로컬 서버(+폴더 자동 로드 API) 및 오프라인 빌더. CLI 출력은 영어 |
| `example.csv` | 예시 데이터 (4 method × 6 token budget = 24행, 중복 없음, 상식적 추세 내장) — 데모·문서용. 재생성 스크립트는 커밋하지 않음 |
| `README.md` | 사용자 문서 (한국어): 사용법, 입력 계약, 에이전트용 변환 요청문 |
| `README.en.md` | README.md의 영어 완역 — **내용 변경 시 두 README를 항상 함께 갱신** |
| `GUIDE.md` | 시각화 가이드 (한국어): 차트 선택 기준·시나리오별 레시피·전달 원칙·팀 공유 — 기능 문서가 아니라 "언제/어떻게" 문서 |
| `GUIDE.en.md` | GUIDE.md의 영어 완역 — **내용 변경 시 두 GUIDE를 항상 함께 갱신**. 레시피의 UI 라벨은 I18N 사전의 실제 문자열(ko/en)과 일치시킬 것 |
| `assets/guide/*.png` | 가이드 레시피별 예시 캡처(r1~r10, 헤드리스 Chrome으로 `.plot` 요소만 2x 크롭 — r10만 `#analysisCard` 크롭) — 레시피 설정이나 차트 렌더링이 바뀌면 재캡처. 재생성 스크립트는 커밋하지 않음 |
| `assets/readme/*.gif` | README 상단 미리보기 GIF(hero·bars·dim-filter·facet, 헤드리스로 상태 시퀀스 캡처→gif-encoder-2 인코딩, 각 2MB 이하). UI 크게 바뀌면 재생성. 스크립트는 커밋 안 함 |
| `CLAUDE.md` | 이 파일 |

## 절대 규칙

- **단일 HTML 유지**: 빌드 도구, 프레임워크, npm, 외부 JS/CSS 파일 금지. vanilla JS만.
- **Plotly 버전 고정**: CDN URL(`plotly-2.35.2.min.js`)을 올리려면 전체 기능 검증 후에만.
- **Python은 표준 라이브러리만**, 문법은 **3.8 호환** (`X | None` 타입 표기 금지 — 실제로 3.9에서 깨진 적 있음).
- **`index.html` 수정 후에는 반드시 `python visualizer.py build-offline` 실행**해 `index-offline.html`을 재생성.
- **입력 계약(데이터 포맷)을 바꾸면 README.md와 README.en.md 양쪽의 "데이터 포맷"·"에이전트 요청문" 섹션을 함께 갱신** — 세 문서(계약·한/영 README)는 항상 동기화. 기능 추가/변경 시에도 두 README의 기능 표를 함께 갱신하고, **UI 라벨이 바뀌거나 레시피에 영향을 주면 GUIDE.md/GUIDE.en.md의 해당 레시피도 함께 갱신**.
- 세션 하위 호환: `chartConfig`에 필드를 추가할 때는 `defaultChart()`에 기본값을 넣으면 된다
  (복원 시 `{...defaultChart(), ...saved}`로 병합되므로 이전 세션도 열린다). 기존 필드의 의미 변경/삭제는 금지.
- **버전·변경이력**: 릴리스마다 ① `index.html`의 `APP_VERSION` 상수 상향(헤더·푸터 자동 표시) + ② 같은 이름 **git 태그**(v0.1, v0.2, …) main에 생성 + ③ **README.md·README.en.md의 "변경 이력/Changelog" 섹션에 항목 추가** + ④ 기능표/GUIDE 동기화. 별도 CHANGELOG 파일은 만들지 않음(9파일 규칙). 이력: v0.1 초기, v0.2 바 차트·가이드·프리셋, v0.3 범례(사분면·이름), v0.4 연속 색상·점 집계·강조흐리게·내보내기, v0.5 작은 다중 차트(facet)·계산 컬럼, v0.6 흐리게 필터, v0.6.1 계산 컬럼 드롭다운 즉시 반영, v0.7 차트 크기·배치(높이·전체/절반 폭), v0.8 다크 모드, v0.9 페이지 폭 토글(기본/넓게/최대 — `applyWidth`, 키 `vtc-visualizer:width`), v0.10 히트맵·덤벨 차트, v0.11 자동 분석 패널, v0.11.1 분석 정합성 수정(행 제외 시 무효화·자동로드 갱신·다중 설계값 블록), v0.12 사용성·보고서·계산 컬럼(부분 렌더링·삭제 되돌리기·카드 순서/접기·필터 복사·예시 데이터 / 캡션·마크다운 리포트·인사이트 복사 / 상수·정규화·순위·구간화·그룹집계·편집/순서·프리셋 동반), v0.12.1 리뷰 수정(캡션 유실·파생-부모 상관·flag 그룹·포화 오버슈트·이상치 정렬), v0.13 속도(크기 컬럼 O(n²) 제거·컬럼 캐시·WebGL 자동 전환), v0.13.1 계산 컬럼 삭제 시 사용처 확인·참조 정리, v0.14 갱신 시 큐레이션 보존·분포 차트·보조 Y축·축 눈금·적합도·설정 검색·세션 번들, v0.15 텍스트 마커 점 앵커(행 정체성)·기준 상실 감지/다시 지정·고정 메모(paper 좌표), v0.16 컬럼 숨김(`state.hiddenCols`)·표 숫자 우측 정렬·내보내기 메뉴·드롭존 축소, v0.16.1 프리셋이 쓰는 숨긴 컬럼 자동 해제·보조축 계산 컬럼 동반·안내 문구 합치기, v0.17 기본 프리셋 5종(역할 매칭)·분포 차트 X축 요구 제거.
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

- **팔레트 테마**(v0.14): `PALETTE_THEMES`(default·carbon·okabe·ink) × light/dark — **전부 dataviz 검증기를 통과시킨 값**이다.
  `PALETTE_THEME`(키 `vtc-visualizer:palette`) + `setPaletteTheme()`가 스왑하고 `applyTheme()`가 모드에 맞는 단계를 고른다.
  **색을 손으로 고치지 말 것** — `scripts/validate_palette.js`를 라이트/다크 각각 다시 돌려 통과시킨 값만 넣는다.
  순서 자체가 색약 안전 장치이므로 순서를 바꾸지 말 것(색은 엔티티를 따라간다).
  `cfg.plotFace`(none|soft|tint) → `faceColor()`가 팔레트×모드에 맞는 면 색을, `gridColorOf()`가 격자색을 정한다
  (면에 색이 있으면 격자는 카드색으로 빼서 뒤로 물린다). 면 색을 바꾸면 **대비 검증 기준이 달라지므로** 검증기를 다시 돌릴 것.
  디자인 토큰: 글자 4단계(`--fs-xs/sm/md/lg`), 간격 4px 배수(`--sp-1..6`), 컨트롤 규격(`--ctl-h`·`--radius`) — 새 UI는 이 토큰만 쓸 것.
- **팔레트/스타일 상수** (`PALETTE`, `SYMBOLS`, `CHROME`, `SEQ_SCALE`, `FONTS`): dataviz 스킬의 검증된 카테고리 팔레트.
  순서가 색약 안전성 장치이므로 **순서를 바꾸거나 색을 추가하려면 dataviz 스킬을 로드해 validator로 검증**할 것.
  테마별로 `LIGHT_/DARK_` 변형이 있고 `applyTheme()`가 `PALETTE`/`SEQ_SCALE` 스왑 + `CHROME` Object.assign(참조 유지) 후 전 차트 재렌더.
  다크 팔레트는 같은 hue 유지, 다크 서피스 대비가 낮은 진초록·진보라만 밝은 스텝으로. `cfg.fontColor` 빈 값 = 테마 잉크 자동(`inkOf(cfg)`).
- **테마**: 라이트/다크 — 키 `vtc-visualizer:theme`(auto|light|dark), CSS 토큰은 `:root` + `@media(prefers-color-scheme)` + `[data-theme]`, JS는 `applyTheme()`/`toggleTheme()`(#btnTheme). 첫 실행 OS 따름.
- **파싱**: `parseCSV` / `parseAny` / `coerce`(숫자 자동 변환). `parseAny`는 세션 스키마(JSON에 datasets+charts 배열)를
  감지해 전용 에러를 던짐 — 자동 로드는 이를 skip, 수동 입력은 "세션 가져오기" 안내. 함수 내 지역변수를 `t`로 짓지 말 것(i18n `t()` 가림).
- **데이터 모델**: `addDataset`, `allRows`(병합), `columns`, `numericColumns`, `uniqueVals`, `matchFilter`(단일 필터), `applyFilters`(제외 모드만 행 제거), `isDimmed`/`isMutedRow`
  (필터 op: `in` = 다중 선택 체크박스 — 카테고리는 기본, 숫자도 선택 가능·빈 배열은 통과; 그 외 카테고리 `=`,`≠`,`포함`, 숫자 비교 연산. 값 미입력 필터는 무시.
  필터 `mode`: `exclude`(기본, 조건 밖 제거) | `dim`(조건 밖 행을 `_muted`처럼 옅게 배경 처리 — buildTraces가 `isMutedRow`로 판정))
- **차트 설정 스키마**: `defaultChart()` — 새 옵션은 여기에 필드 추가부터.
  차트 유형: scatter|line|scatter+line|bar|heatmap|dumbbell. heatmap/dumbbell은 `buildTraces` 앞부분에서 `buildHeatmap`/`buildDumbbell`로 분기(facet·베이스라인·레이블 비활성),
  buildLayout에 전용 축 분기(heatmap=이산 X·Y+컬러바, dumbbell=값 X·카테고리 Y 가로). heatmap 필드 `heatZ`/`heatAgg`/`heatText`, 덤벨은 x=카테고리·group=짝·y=값.
  주요 필드: `baselines[{x,y,shade,dir}]`(다중, dir=both|h|v — 가로/세로 단독 선, 음영은 both만), `textMarkers[{x,y,text,ax,ay,rk?,xc?,yc?,anchor?}]`(→ 아래 "텍스트 마커 앵커"), `hiddenLabels[pointKey]`, `labelOffsets{key:{ax,ay}}`,
  `group2`(마커 모양 2차 그룹 — **`group`이 비어도 단독으로 시리즈를 나눈다**(색은 하나, 모양만 구분). 범례는 `legendPos: 'none'`일 때만 숨긴다 — 시리즈 수로 자동 판단하지 않는다 — 시리즈는 `seriesDefs()`가 (group×group2) 콤보로 생성, 색=colorIdx·모양=symIdx, trace에 `_g`/`_g2` 메타),
  `trend`(none|linear|poly2|log|exp|power|movavg — 시리즈별 피팅, `trendTraces`/`linreg`/`poly2fit`) + `trendDash`/`trendWidth` + `trendBand`(none|1|2 — 잔차 ±kσ `__trendband` 음영 trace 쌍),
  `tmFontSize`/`tmColor`/`tmBg`/`tmArrow`(텍스트 마커 전역 스타일, `textMarkers[i].color/.size`로 개별 오버라이드),
  `lineShape`(linear|spline), `lineDash`(전역 선 종류, 시리즈별 `seriesStyles[name].dash`/`lwidth`로 오버라이드),
  `seriesLabels{원본시리즈명:표시명}`(범례·hover 표시만 덮어씀 — 내부 키(스타일·추세·`__fillbase`/`__trendband`)는 `def.name` 원본 유지, buildTraces의 `dname`),
  `legendPos`(right|top|inside-tl|inside-tr|inside-bl|inside-br|none — 구 `inside`는 좌상단으로 매핑),
  `colorBy`(숫자 컬럼 연속 색상 — group 없을 때만, 단일 trace `marker.color`+`SEQ_SCALE` 컬러바; group 있으면 무시),
  `ptAgg`(none|mean|median|min|max — 같은 X 점 집계, `aggregateBars` 재사용)/`ptError`(none|std|sem → `error_y`)/`ptBand`(none|1|2 → `__ptband` 음영),
  행 플래그 `_muted`(제외 아님 — 옅은 회색 배경화 focus+context; buildTraces에서 muted/일반 조각 분리, `__muted` trace는 저불투명 회색·범례/추세 제외, 레이블도 생략),
  `plotHeight`/`cardWidth`(full|half — 차트 높이·폭, `applyChartSize()`가 카드 재생성 없이 반영+`Plotly.Plots.resize`; #charts는 flex-wrap),
  `facetBy`/`facetCols`(작은 다중 차트 — `buildTraces`가 `buildFacetTraces`를 값별로 호출해 subplot축(xaxisN) 배정, `buildLayout`가 `grid`+가장자리 축제목+값 라벨; facet 시 베이스라인·마커·레이블 비활성),
  `areaFill`(none|tozeroy — 실제 구현은 데이터 최소값 바닥의 `__fillbase` 보조 trace + `tonexty` 파스텔 밴드; 축이 0으로 늘어나지 않게 하기 위함),
  막대 전용 `barMode`(group|stack)/`barOrient`(v|h — 가로면 buildTraces·buildLayout에서 x/y 스왑)/`barAgg`(none|mean|sum|median|min|max|count — `aggregateBars()`가 같은 X의 행을 하나의 막대로 요약)/`barError`(none|std|sem — barAgg=mean일 때만 error_x/y)/`barText`(none|value — 막대 끝 값, 포인트 레이블 annotation은 bar에서 비활성)/`barOpacity`/`barSort`(auto|label|asc|desc → 카테고리 축 categoryorder)/`barCatX`(숫자 X를 카테고리 축으로 — buildLayout `axis()`의 isCat 판정. 문자열 컬럼은 어느 유형이든 자동 category 축).
  bar 전용 UI는 `buildCfgPanel`의 "막대 옵션" 그룹(type=bar일 때만, 유형 변경 시 패널 전체 재구성 `rebuildPanel`), bar에서는 선/마커/추세선/Pareto/포인트 레이블 UI 숨김
- **렌더링**: `buildTraces`(시리즈→trace), `buildLayout`(축/폰트/범례 — 축 범위는 min/max 한쪽만 입력해도 데이터 범위로 보완;
  `uirevision`이 축·범위·스케일 키로 구성돼 스타일 변경 시 줌 유지), `buildAnnotations`(포인트 레이블: 중복 제거→그리디 겹침 회피→텍스트 마커, `_kind`로 구분),
  `baselineShapes`(베이스라인 배열→점선+사분면 음영), `paretoTrace`, 그리고 `renderPlot`(Plotly.react + 이벤트 바인딩)
  - **주의**: `renderPlot`에서 플롯이 이미 있는 div의 innerHTML을 지우면 안 된다(placeholder일 때만 지움) —
    지우면 Plotly.react가 증분 업데이트만 해서 화면이 빈 채로 남는다 (실제 있었던 버그)
- **설정 UI**: `buildCfgPanel` — 그룹(details)별 입력 위젯. 새 옵션의 UI는 여기에. 동적 목록(베이스라인/마커/숨긴 레이블)은 `cfg._refreshLists()`로 갱신
- **이벤트**: `plotly_click` → `showPointPopover`(베이스라인 추가/제거 · 포인트 제외(`_excluded`, 전 차트 공통) · 텍스트 마커 추가 메뉴),
  `plotly_clickannotation` → 포인트 레이블 개별 숨김 / 텍스트 마커 편집(`showMarkerEditPopover`),
  `plotly_relayout` → 주석 드래그 오프셋 저장(`_kind`별로 `labelOffsets` 또는 `textMarkers`) 및 줌 시 음영 재계산
- **부분 렌더링**(v0.12): `refreshCharts()`(전체 재생성)는 세션 복원·전체 초기화·init에서만 쓴다. 그 외에는
  `appendChartCard()`(추가) · 카드 `remove()`(삭제) · `relabelCards()`(언어 전환) · `refreshCfgPanels()`(데이터 변경) ·
  카드 하나 `replaceWith`(프리셋) 로 국소 갱신 — **전체 재생성은 줌·설정 패널 접힘·스크롤·포커스를 모두 날린다**.
  차트별 UI 상태는 `_` 접두사 필드(`_open`{그룹키}·`_cfgHidden`·`_collapsed`)에 두면 `serializableChart()`가 세션에서 자동 제외.
  설정 그룹은 `data-g` 속성으로 식별하고 `restoreGroupState()`가 복원(요약 텍스트는 언어 종속이라 키로 쓰면 안 된다).
  카드를 버릴 때는 `purgePlot()` — `responsive:true`가 등록한 resize 리스너는 purge에서만 해제된다. 단 **렌더 중(`gd._vizRendering`)에는 purge 금지**(Plotly 내부 promise가 깨진다),
  전체 재생성 경로에서는 참조만 끊는다. `Plotly.Plots.resize`는 접힌 차트(`_collapsed`, display:none)에서 reject하므로 항상 건너뛴다.
  `removeChart()`는 삭제한 cfg를 토스트 undo로 되살린다(그 사이 초기화·세션 가져오기가 있었으면 id를 새로 발급). `moveChart()`는 배열 swap + DOM 이동 후 `renumberCards()`.
- **보고서 출력**(v0.12): `cfg.caption`(카드 하단 `.plot-caption`, `applyCaption()`으로 부분 갱신) →
  `buildReportMd()`가 차트별 섹션(캡션 + `chartSpecText()` + `filterText()`)과 분석 요약(`anInsText`)을 마크다운으로 조립,
  `exportReport()`가 .md와 각 차트 PNG를 순차 저장(파일명은 `reportImgName()`으로 링크와 일치). 리포트 본문은 현재 언어를 따른다.
  이미지 한 장이 실패해도 나머지를 계속 저장하고(`failed` 목록으로 보고), 아직 그려지지 않은 차트는 이미지 링크 대신 안내 문구를 넣는다. 제목의 대괄호는 `mdEsc()`로 escape.
  클립보드는 `copyText()` — `navigator.clipboard`는 `file://`에서 막히므로 textarea+execCommand 폴백이 필수.
- **성능**(v0.13): 규모가 커질 때의 병목은 **추측하지 말고 실측**할 것(scratchpad의 perf 스크립트 패턴 — 행 수별로 addDataset/renderPlot/analyze/패널 빌드 시간 측정).
  고친 것: `sizeScale`이 점마다 `chartRows()`를 돌던 O(n²)(2만 행 49.5초 → 0.43초, `sizeRange` 캐시),
  `columns`/`numericColumns`/`uniqueVals`의 전 행 스캔(`dataVer` 캐시 — **데이터·계산 컬럼을 바꾸는 코드는 반드시 `invalidateDataCaches()` 호출**),
  5천 점 초과 시 `scattergl` 자동 전환(`useGl()`, `cfg.renderMode` = auto|svg|gl).
  scattergl은 SVG 내보내기가 래스터가 되므로 `exportImg`가 `_forceSvg`로 잠시 SVG로 되돌린 뒤 저장하고 복구한다.
  대량 배열에 `Math.min(...arr)` 스프레드 금지(스택 초과) — 루프로 쓸 것.
- **행 정체성**(v0.14): `rowKeyCols()`가 "조건 컬럼"(문자열 + 고유값이 행 수/3 이하인 숫자)을 골라 `rowKey(r)`를 만든다.
  같은 이름 데이터셋을 다시 넣으면 `addDataset`이 이 키로 `_excluded`/`_muted`를 되붙이고, 포인트 레이블은
  `pointKeyRow()`(행 정체성) 키를 우선 쓰되 예전 값 기반 키(`pointKey`)도 계속 읽는다.
  **측정값이 키에 들어가면 갱신 때 전부 어긋난다** — 임계값을 느슨하게 바꾸지 말 것.
- **텍스트 마커 앵커**(v0.15): 마커는 늘 포인트 클릭으로 만들어지므로 **좌표가 아니라 점에 묶는다** —
  `markerAnchorFor(cfg, p)`가 클릭한 점의 행을 찾아 `{rk: rowKey(row), xc, yc}`(행 정체성 + 그때의 축 컬럼)를 마커에 담고,
  `resolveMarker(cfg, m, rowsByKey)`가 그릴 때마다 `markerAnchorRows()`(chartRows의 rowKey 맵)에서 행을 찾아 **현재 값을 다시 읽는다**.
  세 가지 모드: `paper`(고정 메모 — x·y가 0~1 비율, `xref/yref:'paper'`, `_paper` 플래그) · `xy`(rk 없는 예전 마커, 좌표 그대로) · `point`(행 앵커).
  **기준을 잃으면(행이 없음 = `gone`, 축 컬럼이 바뀜 = `axis`) 그리지 않는다** — 어긋난 주석은 그대로 보고서로 나가므로 조용히 틀리는 쪽이 가장 나쁘다.
  `buildAnnotations`가 `cfg._tmStaleN`에 개수를 남기고, `renderPlot`이 직전 값(`_tmStaleShown`)과 다를 때만 토스트 + `refreshPanels`,
  설정 목록(`renderLabelLists`)이 ⚠ 사유와 `다시 지정`(`startReanchor`→다음 `plotly_click`→`applyReanchor`, 대기 상태는 모듈 스코프 `tmPending`)을 띄운다.
  고정 메모를 끌어 옮기려면 config `edits.annotationPosition`이 필요하고, relayout 핸들러는 **`_paper` 마커일 때만** `x`/`y`를 받는다
  (점 앵커의 머리 좌표는 행이 정하므로 무시 — 받으면 앵커와 어긋난다).
- **분포 차트**: `buildDistribution(cfg, 'histogram'|'box')` — 값 컬럼은 `cfg.y`이고 **X축은 필요 없다**(`renderPlot`의 가드가 이 두 유형에서 `cfg.x`를 요구하지 않는다), 그룹이 있으면 그룹별로 겹쳐 그린다(히스토그램은 `barmode:'overlay'`).
- **보조 Y축**: `cfg.y2` → `hasY2()`/`y2Layout()`. 기본 경로 레이아웃은 `baseLayout`을 쓰지 않으므로 **두 곳 모두에 적용**해야 한다.
- **테이블**: `renderTable` (검색/정렬/페이지네이션 200행, 행 앞 체크박스로 `_excluded` 토글 → 전 차트에서 제외).
  숫자 컬럼은 `numericColumns()`로 판정해 `th`/`td`에 `.num`(우측 정렬)을 붙인다.
- **컬럼 숨김**(v0.16): `state.hiddenCols[]`(세션 저장, 뷰 계층 — `state.derived`와 같은 급).
  **적용 지점은 `visibleColumns()` 하나**다 — 표·축/그룹 드롭다운·필터·자동 분석·계산 컬럼 입력·CSV 내보내기가 전부 이걸 거친다.
  `numericColumns()`도 같은 필터를 거치지만 **캐시하지 않는다**(hiddenCols는 `dataVer`와 무관하게 바뀐다);
  데이터의 성질 그대로가 필요한 곳은 `numericColumnsAll()`을 쓴다 — **그리는 코드는 항상 All 쪽**이어야 한다
  (숨겼다고 이미 그린 차트의 연속 색상·필터 연산자 UI가 바뀌면 안 된다: `buildTraces`의 `useColorBy`, `renderFilters`의 `nums`).
  **`rowKeyCols()`는 `columns()`를 쓴다 — 절대 `visibleColumns()`로 바꾸지 말 것**: 숨김이 행 정체성을 흔들면
  제외·흐리게·포인트 레이블·마커 앵커가 전부 어긋난다. 계산 컬럼 이름 충돌 검사도 `columns()` 기준(숨긴 이름 재사용 금지).
  **숨김은 삭제가 아니다** — `clearDerivedRefs()`를 부르지 않으며 이미 그 컬럼으로 그린 차트는 그대로 그린다.
  UI는 `showColumnsMenu()`(표 `#btnCols` → 팝오버 체크리스트, 사용처는 `colUsage()`로 표기, `모두 표시`/`쓰는 것만`).
  숫자만 남기는 단축은 두지 않았다 — 숨김이 도구 전체에 적용되므로 그룹 컬럼이 통째로 사라진다.
  토글 시 `renderTable()`+`refreshCfgPanels()`+`analysisStale()`+`save()`. `invalidateDataCaches()`는 부르지 않는다(데이터 키 집합은 그대로).
- **사용처 조회**: `colUsage(name)` = 임의 컬럼의 사용처(차트 축·필터 + 그 컬럼을 입력으로 쓰는 계산 컬럼).
  `derivedUsage`는 이 함수의 별칭이다. 참조 필드 목록은 `DERIVED_REF_FIELDS`(`y2` 포함 — v0.14 보조 축이 빠져 있던 것을 v0.16에서 보완).
- **세션**: `save`(debounce→localStorage), `exportSession`/`restoreSession`, 키 `vtc-visualizer:session`
  (구 키 `visualizer-by-mrc:session`은 `loadSaved()`가 읽어 자동 마이그레이션)
- **프리셋**: 차트 설정만 저장/재적용 — 키 `vtc-visualizer:presets`(세션과 분리), `chartPreset()`(id·title·포인트 종속 필드
  textMarkers/labelOffsets/hiddenLabels 제외), `applyPreset()`({...defaultChart(), ...preset} 병합 후 refreshCharts),
  `showPresetMenu()`(카드 `프리셋` 버튼 팝오버: 기본 프리셋 / 저장한 프리셋 / JSON 내보내기·가져오기)
- **기본 프리셋**(v0.17): `STARTER_PRESETS`(avg·sweep·tradeoff·heat·dist) — **컬럼 이름을 박아 두지 않는다.**
  `starterRoles()`가 지금 데이터에서 역할을 찾고(`cat` 범주 2~12레벨 · `design` 값이 몇 개뿐인 숫자 · `score` 점수형 · `cost` 비용형,
  이름 패턴은 `addChart()`의 기본 추측과 같은 결), `starterList()`가 **역할이 채워지는 레시피만** 내놓는다 —
  눌렀더니 빈 차트가 되는 것이 가장 나쁘므로 목록에 아예 띄우지 않는다. 로그축은 `logFits()`(최대/최소 ≥ 8)일 때만.
  적용은 기존 `applyPreset()`을 그대로 쓰고 저장은 하지 않는다(사용자가 다듬은 뒤 직접 저장).
  **실무 시나리오용 프리셋은 이 목록에 넣지 않는다** — 공개 레포이고 컬럼 이름이 곧 실험 설계다(로컬 전용 JSON으로 유지).
- **계산 컬럼**: `state.derived[]`(세션 저장, 입력 계약 아님 — 뷰 계층) → `applyDerived()`가 로드/변경 시 각 행에 파생 값 주입
  (`derivedApplied`로 직전 컬럼까지 제거해 삭제 반영). 종류: binary(A∘B, `bConst`로 상수 피연산자), refdelta(키 매칭 기준행 대비 차이/유지율),
  norm(minmax|max|z), rank(desc 여부), bin(동일 폭 N구간 → **문자열** 라벨이라 그룹·필터로 쓰인다), groupagg(그룹 통계를 행에 브로드캐스트).
  norm/rank/bin/groupagg는 `by`(빈 값이면 전체)로 그룹 범위를 정하고 한 버킷 루프에서 함께 계산한다.
  **정의 순서가 곧 계산 순서**(체인 의존성) — UI에 ↑/↓와 편집(`derivedEditIdx`)이 있다. 설명 문구는 `derivedDesc()`.
  삭제는 `removeDerived()` — `derivedUsage()`로 사용처(차트 축·필터, 이 컬럼을 입력으로 쓰는 다른 정의)를 먼저 보여주고 확인을 받은 뒤
  `clearDerivedRefs()`로 참조를 정리한다. **컬럼을 없애는 코드는 참조 정리를 함께 해야 한다** — 안 하면 차트가 조용히 빈 그래프가 된다.
  프리셋은 `presetDerivedFor()`로 그 차트가 쓰는 정의를 의존성까지 모아 `_derived`에 담고, `applyPreset()`이 없는 정의를 복원한다.
  참조 컬럼 수집은 `chartRefCols(cfg)` 하나로 모은다(`DERIVED_REF_FIELDS` + 필터 컬럼) — 손으로 적은 목록을 두면 필드가 늘 때 빠진다(실제로 `y2`가 빠져 있었다).
  `applyPreset()`은 프리셋이 쓰는 컬럼이 `state.hiddenCols`에 있으면 **숨김을 풀어 준다**(v0.16.1) — 차트는 그려지지만 축 선택기에서 고를 수 없는 반쪽 상태를 막는다.
  곁들여 한 일(계산 컬럼 복원·숨김 해제)은 **토스트를 따로 띄우지 않고 적용 안내 한 줄에 모은다** — `showToast`는 요소 하나를 재사용해 연달아 부르면 앞 안내가 덮인다. UI는 `renderDerived()`(데이터 카드의 `#derivedPanel`)
- **자동 분석**(v0.11): 헤더 `#btnAnalyze` → `toggleAnalysis()`/`runAnalysis()` → `analyzeData()` → `renderAnalysis()`(`#analysisCard`).
  **세션에 저장하지 않는다** — 모듈 스코프 `let analysis`(캐시)만 두고 `save`/`exportSession`/`restoreSession`은 건드리지 않음. `onDataChanged`가 무효화.
  인사이트는 `{tier, kind, params, score, chart}`로만 보관하고 문장은 렌더 시 `anInsText()`가 i18n 템플릿(`an.ins.*`)에 넣는다 —
  **분석 시점에 언어 종속 문자열을 굽지 말 것**(방향어는 `dirUp` 불리언, "전체 행"은 `AN_ALL` 자리표시자로 전달). 임계값은 전부 `AN` 상수에.
  순수 통계: `anDescribe`/`anPearson`/`anSpearman`/`anRobustZ`(수정 z, MAD=0이면 평균절대편차 폴백)/`anCV`. 컬럼 분류 `anProfile()` —
  `id`(식별자·seed)·`design`(설계 노브)·`flag`·`cont`·`cat`·`mixed`·`const`·`empty`, 분류 결과가 곧 스캔 가드다(design×design 상관 금지, id는 전부 제외).
  거짓 발견 방지 규칙(수정 시 반드시 유지): 정의상 같은 컬럼(비율/차이 CV<`defCV`, 또는 |r|≥`rDup`)은 `alias`로 대표 하나에 접고,
  pooled 상관이 그룹별 중앙값과 어긋나면(`simpsonGap`) 수치 대신 `simpson` 경고, 그룹 간 우열이 블록마다 뒤집히면 평균 대신 `cross`,
  이상치는 (모든 설계 노브가 같은) 셀 내부 또는 국소 추세 잔차에서만 판정하고 자동 제외 금지. **p값·"유의" 표현 금지** — 원단위 차이 + 방향 일관성 + `anBootMean()`(백분위 부트스트랩, **리샘플링 단위 = 블록**, `anRng` 결정적 난수라 재실행해도 같은 구간, 구간이 0을 포함하면 발견 자체를 내보내지 않음)으로 대체. UI 문구는 "신뢰구간"이 아니라 "부트스트랩 구간".
  파생 컬럼과 그 입력의 상관은 자명하므로 `derivedPairs`에 **kind별 부모 필드를 모두** 등록한다(binary→a,b / refdelta→valueCol,refCol,keys / 그 외→col,by).
  `flag`(2값)도 `catCols`에 포함 — fp16 on/off 같은 A/B 조건이 가장 전형적인 그룹 비교 대상이다.
  이상치 점수는 `anOutScore(z)`로 |z|를 따라간다(상수 점수면 상한이 '먼저 스캔된 것'을 남긴다).
  **행 집합이 바뀌는 모든 경로에서 `analysisStale()` 호출**(표 체크박스·복원 버튼·포인트 팝오버·계산 컬럼) — 빠뜨리면 낡은 인사이트가 조용히 남는다.
  블록(짝 비교 단위) = **모든 설계 노브 조합**(`blockKeyOf`), 1:1로 대응하는 설계 노브는 `samePartition()`으로 대표 하나만 남기고 `dupdesign`으로 보고.
  포화는 노브별로 계산하되 다른 노브에 대해 균형(레벨별 행 수 동일)일 때만. 기본 목록은 `anPickShown()`이 티어 할당량(데이터 3·주의 3·나머지 발견)으로 뽑아 발견이 밀려나지 않게 한다.
  `meta.scope`(그룹 후보·설계값·제외 컬럼과 이유)를 패널에 한 줄로 노출 — 발견이 0건일 때의 설명이다.
  성능: 프로파일은 전체 행, 스캔은 `maxRows` 초과 시 결정적 stride 표본. 근거 차트는 `runInsightChart()` — `anFindChart()`로 같은 (type,x,y,group) 차트가 있으면 그리로 스크롤, 없으면 `addChart(override)`로 **새 차트만** 추가(기존 cfg 수정 금지). UI: 티어가 바뀔 때마다 `.ins-tier`로 검증 안내(`an.verify0/1/2`), 차트가 있는 항목은 `anChartSpec()`이 설정을 `.ins-spec` 회색 줄로 표기.
- **서버 연동**: `tryServerAutoload` — `api/files`/`api/file` (http로 열렸을 때만)

새 차트 옵션 추가 절차: `defaultChart()`에 필드 → `buildCfgPanel`에 입력 UI → `buildTraces`/`buildLayout`에 반영 → 세션 저장은 자동.

주의: Plotly 로그축 좌표 규약은 **비대칭**이다 (실측 검증됨) — annotation의 x/y는 log10 값(`axCoord()` 헬퍼 사용),
**layout.shapes의 x0/y0 등은 원시 데이터 값**(axCoord 금지). `gd._fullLayout.[xy]axis.range`는 로그축이면 log10 값이므로
shapes 계산에 쓸 때는 `Math.pow(10, v)`로 되돌릴 것 (`baselineShapes()`의 `unlog` 참고).

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
