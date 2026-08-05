# VTC Visualizer — 프로젝트 가이드

**브랜딩**: 사용자에게 보이는 이름은 "VTC Visualizer", 저작자 표기는 하단 카피라이트 "© mrc"로만.

CSV/JSON을 브라우저에서 논문 스타일 인터랙티브 그래프로 그리는 범용 벤치마크 시각화 도구.
여러 사람이 각자 데이터를 가져와 쓰는 도구이므로 **입력 계약의 안정성**과 **파일 하나로 배포 가능한 단순함**이 최우선이다.

## 파일 구조 (소스·문서는 이 **10개**가 전부 — 파일을 늘리지 말 것. 예외: `assets/guide/`는 가이드 예시 이미지 전용 폴더)

> **9 → 10이 된 이유**(v0.29): `annotate.html`을 더했다. 이 도구는 Plotly도 데이터 모델도 쓰지 않아
> `index.html`에 넣으면 **공유하지 않는 코드**가 5,800줄짜리 파일을 더 키우고, 차트를 그리러 온 사람의
> 설정 패널에 상관없는 것이 끼어든다. 규칙을 깬 것이 아니라 **한 번 늘리고 다시 잠근 것**이다 —
> 다음에 파일을 더하려면 이 정도 근거를 대고 이 문장도 함께 고칠 것.

| 파일 | 역할 |
|---|---|
| `index.html` | 메인 앱. **유일한 소스 코드** (HTML+CSS+JS 단일 파일, Plotly.js CDN) |
| `index-offline.html` | 자동 생성물. 직접 수정 금지 — `python visualizer.py build-offline`로 재생성 |
| `visualizer.py` | 보조 실행기: 로컬 서버(+폴더 자동 로드 API) 및 오프라인 빌더. CLI 출력은 영어 |
| `example.csv` | 예시 데이터 (4 method × 6 token budget = 24행, 중복 없음, 상식적 추세 내장) — 데모·문서용. 재생성 스크립트는 커밋하지 않음 |
| (앱 내장) | `EXTRA_CSVS`(v0.31) — 가이드 레시피용 짝 데이터 5개(`methods.csv`·`wide.csv`·`repeat.csv`·`seeds.csv`·`scales.csv`). **`example.csv`는 건드리지 않는다** — 컬럼이 하나 늘면 자동 분석 골든 테스트와 문서 설명이 함께 흔들린다 |
| `README.md` | 사용자 문서 (한국어): 사용법, 입력 계약, 에이전트용 변환 요청문 |
| `README.en.md` | README.md의 영어 완역 — **내용 변경 시 두 README를 항상 함께 갱신** |
| `GUIDE.md` | 시각화 가이드 (한국어): 차트 선택 기준·시나리오별 레시피·전달 원칙·팀 공유 — 기능 문서가 아니라 "언제/어떻게" 문서 |
| `GUIDE.en.md` | GUIDE.md의 영어 완역 — **내용 변경 시 두 GUIDE를 항상 함께 갱신**. 레시피의 UI 라벨은 I18N 사전의 실제 문자열(ko/en)과 일치시킬 것 |
| `assets/guide/*.png` | 가이드 레시피별 예시 캡처(r1~r13, 헤드리스 Chrome으로 `.plot` 요소만 2x 크롭 — r10만 `#analysisCard`, r13은 주석 도구 결과물) — **레시피 설정이나 차트 렌더링이 바뀔 때만** 재캡처. 화면 UI가 바뀌어도 이 그림들은 플롯만 담으므로 대개 그대로다(v0.30에서 확인: 팔레트·`CHROME`·`faceColor`·`buildLayout` 변경 0줄이면 다시 찍을 이유가 없다). 재생성 스크립트는 커밋하지 않음 |
| `assets/readme/*.gif` | README 상단 미리보기 GIF(hero·bars·dim-filter·facet, 헤드리스로 상태 시퀀스 캡처→gif-encoder-2 인코딩, 각 2MB 이하). UI 크게 바뀌면 재생성. 스크립트는 커밋 안 함 |
| `annotate.html` | 이미지 주석 도구(v0.29). **독립 실행** — Plotly·데이터 모델을 쓰지 않는 단일 파일. i18n·테마 저장 키는 `index.html`과 공유 |
| `CLAUDE.md` | 이 파일 |

## 절대 규칙

- **단일 HTML 유지**: 빌드 도구, 프레임워크, npm, 외부 JS/CSS 파일 금지. vanilla JS만.
- **Plotly 버전 고정**: CDN URL(`plotly-2.35.2.min.js`)을 올리려면 전체 기능 검증 후에만.
- **Python은 표준 라이브러리만**, 문법은 **3.8 호환** (`X | None` 타입 표기 금지 — 실제로 3.9에서 깨진 적 있음).
- **`index.html` 수정 후에는 반드시 `python visualizer.py build-offline` 실행**해 `index-offline.html`을 재생성.
- **입력 계약(데이터 포맷)을 바꾸면 README.md와 README.en.md 양쪽의 "데이터 포맷"·"에이전트 요청문" 섹션을 함께 갱신** — 세 문서(계약·한/영 README)는 항상 동기화. 기능 추가/변경 시에도 두 README의 기능 표를 함께 갱신하고, **UI 라벨이 바뀌거나 레시피에 영향을 주면 GUIDE.md/GUIDE.en.md의 해당 레시피도 함께 갱신**.
- 세션 하위 호환: `chartConfig`에 필드를 추가할 때는 `defaultChart()`에 기본값을 넣으면 된다
  (복원 시 `{...defaultChart(), ...saved}`로 병합되므로 이전 세션도 열린다). 기존 필드의 의미 변경/삭제는 금지.
- **버전·변경이력**: 릴리스마다 ① `index.html`의 `APP_VERSION` 상수 상향(헤더·푸터 자동 표시) + ② 같은 이름 **git 태그**(v0.1, v0.2, …) main에 생성 + ③ **README.md·README.en.md의 "변경 이력/Changelog" 섹션에 항목 추가** + ④ 기능표/GUIDE 동기화. 별도 CHANGELOG 파일은 만들지 않음(9파일 규칙). 이력: v0.1 초기, v0.2 바 차트·가이드·프리셋, v0.3 범례(사분면·이름), v0.4 연속 색상·점 집계·강조흐리게·내보내기, v0.5 작은 다중 차트(facet)·계산 컬럼, v0.6 흐리게 필터, v0.6.1 계산 컬럼 드롭다운 즉시 반영, v0.7 차트 크기·배치(높이·전체/절반 폭), v0.8 다크 모드, v0.9 페이지 폭 토글(기본/넓게/최대 — `applyWidth`, 키 `vtc-visualizer:width`), v0.10 히트맵·덤벨 차트, v0.11 자동 분석 패널, v0.11.1 분석 정합성 수정(행 제외 시 무효화·자동로드 갱신·다중 설계값 블록), v0.12 사용성·보고서·계산 컬럼(부분 렌더링·삭제 되돌리기·카드 순서/접기·필터 복사·예시 데이터 / 캡션·마크다운 리포트·인사이트 복사 / 상수·정규화·순위·구간화·그룹집계·편집/순서·프리셋 동반), v0.12.1 리뷰 수정(캡션 유실·파생-부모 상관·flag 그룹·포화 오버슈트·이상치 정렬), v0.13 속도(크기 컬럼 O(n²) 제거·컬럼 캐시·WebGL 자동 전환), v0.13.1 계산 컬럼 삭제 시 사용처 확인·참조 정리, v0.14 갱신 시 큐레이션 보존·분포 차트·보조 Y축·축 눈금·적합도·설정 검색·세션 번들, v0.15 텍스트 마커 점 앵커(행 정체성)·기준 상실 감지/다시 지정·고정 메모(paper 좌표), v0.16 컬럼 숨김(`state.hiddenCols`)·표 숫자 우측 정렬·내보내기 메뉴·드롭존 축소, v0.16.1 프리셋이 쓰는 숨긴 컬럼 자동 해제·보조축 계산 컬럼 동반·안내 문구 합치기, v0.17 기본 프리셋 5종(역할 매칭)·분포 차트 X축 요구 제거, v0.17.1 역할 판정을 이름 패턴에서 `anProfile` 분포 기반으로, v0.18 라벨 조합 계산 컬럼(concat), v0.19 차트별 데이터셋 선택(`cfg.dataset`), v0.20 필터 규칙 문장·모드 4종(조건 밖/맞는 것 × 제거/흐리게), v0.20.1 파레토 재점검(집계·흐리게·facet·이름), v0.21 파레토 가독성(실선 잉크색·지배당한 점 흐리게), v0.21.1 프런티어 선 모양·굵기 선택, v0.21.2 프런티어 선 색(빈 값=테마 자동), v0.22 절반 폭 카드 헤더 접힘 수정·문서 그림 재캡처, v0.23 하위 폴더 자동 로드(숨김 폴더·폴더 밖 링크 제외)·심볼릭 링크 탈출 차단·`--host`·스레드 서버·`allRows()` 캐시, v0.24 키보드·접근성(`row()` 라벨 연결·`main`/건너뛰기 링크·팝오버/모달 포커스 복귀·표 헤더 Enter 정렬·흐리게 표 열·베이스라인 값 입력)·패널 밀도(그룹 펼침 기억 `vtc-visualizer:groups`·검색 선택지 매치/0건 안내·시리즈 접기·팝오버 focusout 닫힘·행 선택 텍스트 마커), v0.25 파일 간 결합(`lookup` 계산 컬럼 — 행 증가 없음·짝 수 미리보기)·행 정체성에서 계산 컬럼 제외(갱신 시 제외/흐리게 유실 수정), v0.26 제출용 그림(내보내기 규격 mm/inch·dpi `exportSize()`·오차 컬럼 `errCol`·구간 음영 `spans`·누적 영역 `areaFill:stack`·차트를 표로 `_asTable`), v0.27 데이터 유입·유출(가로→세로 녹이기 `meltRows`·폴더 감시 `/api/stat`+`vtc-visualizer:watch`·공유용 HTML 한 장 `exportStandalone`/`PRISTINE_BODY`), v0.28 베이스라인 점 앵커(`resolveBaseline`·`_blStaleN`·`tmPending` 종류 일반화)·분석 속도는 재 보고 원복(이유는 코드 주석에), v0.29 이미지 주석 도구 `annotate.html`(파일 규칙 9→10, 서버 라우트 1개·내보내기 메뉴 링크), v0.29.1 글자 배경 온/오프(불투명·선택 시 입력 되비침), v0.29.2 드롭존 점선 정리·이미지 교체 확인, v0.30 가이드 레시피 3종 추가(녹이기·결합·제출 규격)+기존 레시피에 v0.26~v0.29 기능 반영·새 레시피 그림만 신규 캡처, v0.31 레시피용 예시 데이터 3종(`EXTRA_CSVS`·`예시 더` 버튼), v0.31.1 주석 페이지 버전 표시 수정·`t('all')` 리터럴화(preflight가 잡은 것), v0.32 바이올린·ECDF·시리즈 순서(`seriesOrder`, 색은 엔티티 고정)·최적점 표시(`markBest`), v0.32.1 분포 차트 X축 가드 수정, v0.33 분포 레시피 ⑱·`seeds.csv` 짝 데이터·분포/히트맵/덤벨의 데이터셋 선택 무시 수정(`chartBaseRows`).
- **패널 스크롤**(v0.38): 세 가지가 함께 간다 — ① `.cfg`의 `max-height`가 **화면을 따른다**(`min(calc(100vh - 150px), 900px)`, 640px 고정이었다),
  ② `ACCORDION`(키 `vtc-visualizer:accordion`, 기본 켜짐)이 한 묶음만 남긴다,
  ③ 시리즈 목록은 **항상** `details.sub-grp`로 접는다(키 `vtc-visualizer:seriesopen`) — 스타일 975px 중 437px이 이 목록이었다.
  **아코디언은 `summary`의 click에 건다 — `toggle`에 걸면 검색이 여러 묶음을 펼치는 것까지 닫는다**(`grpSilent`는 비동기 toggle과 경합해 믿을 수 없다).
  형제를 닫을 때 `groupPrefs`도 함께 내린다(안 그러면 새로고침에 여럿이 되살아난다). 복원 시 강제로 줄이지는 않는다 — 예전 상태를 말없이 바꾸면 "열어 둔 것이 사라졌다"가 된다.
  **2열 배치는 재 보고 접었다**: 라벨+컨트롤 행만 반 폭으로 접어도 시리즈 목록이 반 폭에 밀려 스타일이 975 → 1,670px로 **늘어났다**(실측).
- **간단 ⇄ 전부**(v0.42): 기본 상태 46줄 중 16줄만 보인다(전부 펼쳐 3,004 → 1,520px). `SIMPLE`(키 `vtc-visualizer:simple`, 기본 켜짐) + `.cfg.simple .row.adv{display:none}`.
  표시는 `buildCfgPanel` 안의 지역 헬퍼 **`A(node, keep)`** 하나로 한다 — `row()`는 라벨 연결 규칙이 걸려 있으므로 손대지 말고 결과에 클래스만 붙인다.
  **`keep`이 핵심이다**: 값이 들어 있는 고급 줄은 감추지 않는다 — 감추면 켜 둔 보조축·분할·범위를 **끌 길이 사라져** 화면과 설정이 어긋난 채 남는다.
  **검색은 이걸 이긴다**(`.cfg.searching`) — 감춘 줄이 결과에서도 빠지면 "그런 옵션은 없다"가 된다. `cfgSearchBox`의 input 핸들러에서 클래스를 토글한다.
  줄이 하나도 안 남는 묶음은 `alladv`로 통째로 감추되 **줄이 애초에 없는 묶음(필터·기준선)은 폼이 본체**라 세지 않는다.
  새 옵션을 더할 때의 판정: **안 건드리면 그림이 안 나오는가(기본), 덜 좋은가(고급)**. 곁들여 유형 select는 `optgroup` 셋(`기본`/`분포`/`특수`)이고,
  `select()`가 `{label, options:[...]}` 항목을 optgroup으로 받는다. `xTick`/`yTick`은 v0.14부터 필드·렌더는 있고 UI만 없던 것을 이때 냈다(`TICK_OPTS()`).
- **i18n**: UI는 KO/EN 이중 언어(`I18N` 사전 + `t()`/`tf()`, 토글 = `#btnLangToggle`, 저장 키 `vtc-visualizer:lang`).
  **사용자에게 보이는 문자열을 추가하면 반드시 I18N 사전의 ko/en 양쪽에 키를 추가**하고 `t()`로 호출할 것.
  정적 HTML은 `data-i18n`/`data-i18n-ph` 속성 + `applyLang()`. 내부 식별자(`' 추세'` 접미사, `__fillbase`, `__trendband`)는 번역 금지, **그룹 없는 차트의 시리즈 이름 `'all'`도 마찬가지**(`seriesStyles`/`seriesLabels`의 키라 번역하면 언어 전환 때 사용자가 정한 색·이름이 사라진다 — v0.31.1에서 `t('all')`을 리터럴로 되돌렸다).
  **릴리스 전에는 `visualizer-local/vtc-tests/preflight.sh`를 돌린다** — 버전 3곳 일치·오프라인 동기화·i18n 짝·문서 대칭·그림 링크·파일 수를 검사한다(`run.sh`가 먼저 부른다).

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
  필터 `mode` 4종(v0.20): `exclude`(기본, 조건 밖 제거) | `excludeIn`(맞는 것 제거) | `dim`(조건 밖 흐리게) | `dimIn`(맞는 것 흐리게).
  흐리게는 행을 남기고 `isMutedRow`로 렌더 단계에서 옅게 처리한다.
  **방향을 둘 다 두는 이유**: "조건에 맞는 쪽을 남긴다"와 "고른 행에 동작을 적용한다"가 둘 다 자연스러운 읽기라
  한쪽만 두면 반대로 이해한 사람이 조용히 틀린 그림을 얻는다(실제로 그런 보고가 있었다).
  `excludeIn`/`dimIn`은 **`filterActive(f)` 판정이 필수** — 미완성 필터에서 `matchFilter`가 true를 주므로 가드가 없으면 전부를 지운다.
  헷갈림을 막기 위해
  필터마다 `filterRuleInfo(cfg, f)`로 맞는 행 수를 세어 `.filter-rule` 문장으로 보여준다(`cfg.filterRuleExc`/`Dim`).
  값 입력 중에도 따라와야 하므로 행을 다시 그리지 말고 **`syncRule()`로 그 줄만 제자리 갱신**할 것 — 다시 그리면 입력 포커스가 날아간다.)
- **차트 설정 스키마**: `defaultChart()` — 새 옵션은 여기에 필드 추가부터.
  차트 유형: scatter|line|scatter+line|bar|heatmap|dumbbell|break.
  **축 끊기**(v0.36, `isBreakType`/`brkAxisOf`/`breakRange`/`buildBreak`/`applyBreakRefs`/`chartShapes`):
    Plotly에 끊긴 축이 없으므로 **축 둘을 domain으로 쪼개고 같은 trace를 두 벌** 그린다(뒤 벌은 `y3`/`x3`, `showlegend:false`).
    각 축이 범위 밖을 잘라내므로 끊긴 축이 된다. **값은 절대 변환하지 않는다** — 접힌 좌표로 그리면 hover·표·CSV·리포트가 전부 가짜다.
    **옵션이 아니라 유형인 이유**: 옵션이면 막대·보조축·facet·쌓기와 배타 조건을 손으로 다 걸어야 하고 하나만 새면 깨진 그림이 나온다.
    한 번에 한 축만(`brkAxis`) — 둘 다 끊으면 패널이 2×2가 되고 참조 조합이 넷이 된다.
    구간은 비우면 자동(가장 큰 빈 구간, 전체의 25% 초과 + 양쪽 점 2개 이상), 없으면 `cfg._brkNone`로 패널에 알린다.
    **함정 셋**: ① 새 주석(축 제목·`⁄⁄`)은 **배열 끝에** 붙인다 — `plotly_relayout`이 `annotations[i]` 인덱스로 마커 드래그를 저장한다.
    ② 도형 입구는 `chartShapes(cfg, gd)` **하나**다 — 줌 때 `baselineShapes`를 직접 부르면 참조 보정을 건너뛴다.
    ③ 끊긴 축은 로그가 될 수 없다(UI에서 감추고 축 선택 때 그 축 스케일을 linear로 되돌린다).
    축 제목은 회전한 paper 주석 하나로 두되 **비율을 상수로 박지 말 것** — 여백 밖으로 나가 잘린다(픽셀에서 되계산). heatmap/dumbbell은 `buildTraces` 앞부분에서 `buildHeatmap`/`buildDumbbell`로 분기(facet·베이스라인·레이블 비활성),
  buildLayout에 전용 축 분기(heatmap=이산 X·Y+컬러바, dumbbell=값 X·카테고리 Y 가로). heatmap 필드 `heatZ`/`heatAgg`/`heatText`, 덤벨은 x=카테고리·group=짝·y=값.
  v0.26 필드: `errCol`(행마다의 ± 오차 컬럼 — **집계 중에는 무시**한다. 점 하나가 여러 행을 대표하면 행마다의 오차는 그 점의 오차가 아니다.
  `DERIVED_REF_FIELDS`·`DATASET_COL_FIELDS` 양쪽에 등록되어 있다),
  `spans[{axis,from,to,label}]`(구간 음영 — 한 축은 데이터 좌표, 다른 축은 paper. 라벨은 `spanAnnotations()`가 따로 만든다:
  **shapes는 원시 값, annotation은 log10**이라는 Plotly의 비대칭 규약 때문에 한 함수에 못 담는다),
  `areaFill: 'stack'`(누적 영역 — `stackgroup`은 **본 시리즈 trace에만** 준다. 추세선·흐리게·`__fillbase`가 끼면 합이 틀어진다.
  `scattergl`은 stackgroup을 지원하지 않으므로 `useGl()`이 쌓기일 때 **무조건 SVG**를 고른다 — 안 그러면 조용히 겹쳐 그려진다),
  `expUnit`/`expW`/`expH`/`expDpi`(내보내기 규격 — `exportSize()`가 물리 크기를 **96 CSS dpi 기준 픽셀**로 바꾸고 `scale`에 dpi/96을 준다.
  이래야 글자가 dpi와 무관하게 같은 물리 크기로 나온다(픽셀만 키우면 글자만 작아진다). 리포트 그림도 같은 함수를 쓴다).
  주요 필드: `baselines[{x,y,shade,dir}]`(다중, dir=both|h|v — 가로/세로 단독 선, 음영은 both만), `textMarkers[{x,y,text,ax,ay,rk?,xc?,yc?,anchor?}]`(→ 아래 "텍스트 마커 앵커"), `hiddenLabels[pointKey]`, `labelOffsets{key:{ax,ay}}`,
  `group2`(마커 모양 2차 그룹 — **`group`이 비어도 단독으로 시리즈를 나눈다**(색은 하나, 모양만 구분). 범례는 `legendPos: 'none'`일 때만 숨긴다 — 시리즈 수로 자동 판단하지 않는다 — 시리즈는 `seriesDefs()`가 (group×group2) 콤보로 생성, 색=colorIdx·모양=symIdx, trace에 `_g`/`_g2` 메타),
  `trend`(none|linear|poly2|log|exp|power|movavg — 시리즈별 피팅, `trendTraces`/`linreg`/`poly2fit`) + `trendDash`/`trendWidth` + `trendBand`(none|1|2 — 잔차 ±kσ `__trendband` 음영 trace 쌍),
  `tmFontSize`/`tmColor`/`tmBg`/`tmArrow`(텍스트 마커 전역 스타일, `textMarkers[i].color/.size`로 개별 오버라이드),
  `lineShape`(linear|spline), `lineDash`(전역 선 종류, 시리즈별 `seriesStyles[name].dash`/`lwidth`로 오버라이드),
  `seriesStyles[name].mode`(v0.34 — 시리즈별 표시 모드 markers|lines|both, **빈 값 = 차트 유형을 따름**. `seriesMode(st, lineMode)` 하나가 해석하고
    `buildFacetTraces`(facet·비facet 공용 경로)가 흐리게 조각·본 trace·보조축에 같은 값을 쓴다. **`hasLine`을 이 모드로 판정**해야 한다 —
    차트 유형으로 판정하면 선이 없는 시리즈에 영역 채우기·쌓기가 걸려 그리지 못할 것을 그리려 든다. 모르는 값은 유형으로 폴백(옛 세션 방어).
    UI는 선/산점도 계열에서만 노출한다 — 분포·히트맵·덤벨은 모드를 스스로 정한다),
  `seriesLabels{원본시리즈명:표시명}`(범례·hover 표시만 덮어씀 — 내부 키(스타일·추세·`__fillbase`/`__trendband`)는 `def.name` 원본 유지, buildTraces의 `dname`),
  `legendPos`(right|top|inside-tl|inside-tr|inside-bl|inside-br|none — 구 `inside`는 좌상단으로 매핑),
  `colorBy`(숫자 컬럼 연속 색상 — group 없을 때만, 단일 trace `marker.color`+`SEQ_SCALE` 컬러바; group 있으면 무시),
  `ptAgg`(none|mean|median|min|max — 같은 X 점 집계, `aggregateBars` 재사용)/`ptError`(none|std|sem → `error_y`)/`ptBand`(none|1|2 → `__ptband` 음영),
  행 플래그 `_muted`(제외 아님 — 옅은 배경화 focus+context; buildTraces에서 muted/일반 조각 분리, `__muted` trace는 저불투명·범례/추세 제외, 레이블도 생략.
    색은 `cfg.mutedStyle`(v0.41, gray|color) — 기본은 회색(배경 맥락은 시리즈 정체성을 버려야 강조가 튄다)이고,
    흐리게가 여러 시리즈에 걸릴 때 어느 시리즈였는지 못 읽는 문제 때문에 시리즈 색을 남기는 쪽을 고를 수 있게 두었다.
    **불투명도(0.28)는 어느 쪽이든 같다** — 물러나는 정도를 바꾸는 옵션이 아니다. 파레토 `paretoFade`는 원래부터 색을 유지한다),
  `plotHeight`/`cardWidth`(full|half — 차트 높이·폭, `applyChartSize()`가 카드 재생성 없이 반영+`Plotly.Plots.resize`; #charts는 flex-wrap.
    카드 헤더도 `flex-wrap: wrap` + 버튼 `flex: none`이다 — 버튼 높이가 26px로 고정돼 있어 좁아지면 글자가 **박스 밖으로 흘러넘친다**(v0.22에서 고침).
    이 결함은 겉보기 높이로는 안 잡히고 `scrollHeight > clientHeight`로 봐야 한다),
  `facetBy`/`facetCols`(작은 다중 차트 — `buildTraces`가 `buildFacetTraces`를 값별로 호출해 subplot축(xaxisN) 배정, `buildLayout`가 `grid`+가장자리 축제목+값 라벨; facet 시 베이스라인·마커·레이블 비활성),
  `areaFill`(none|tozeroy — 실제 구현은 데이터 최소값 바닥의 `__fillbase` 보조 trace + `tonexty` 파스텔 밴드; 축이 0으로 늘어나지 않게 하기 위함),
  막대 전용 `barMode`(group|stack)/`barOrient`(v|h — 가로면 buildTraces·buildLayout에서 x/y 스왑)/`barAgg`(none|mean|sum|median|min|max|count — `aggregateBars()`가 같은 X의 행을 하나의 막대로 요약)/`barError`(none|std|sem — barAgg=mean일 때만 error_x/y)/`barText`(none|value — 막대 끝 값, 포인트 레이블 annotation은 bar에서 비활성)/`barOpacity`/`barSort`(auto|label|asc|desc → 카테고리 축 categoryorder)/`barCatX`(숫자 X를 카테고리 축으로 — buildLayout `axis()`의 isCat 판정. 문자열 컬럼은 어느 유형이든 자동 category 축).
  bar 전용 UI는 `buildCfgPanel`의 "막대 옵션" 그룹(type=bar일 때만, 유형 변경 시 패널 전체 재구성 `rebuildPanel`), bar에서는 선/마커/추세선/Pareto/포인트 레이블 UI 숨김
- **렌더링**: `buildTraces`(시리즈→trace), `buildLayout`(축/폰트/범례 — 축 범위는 min/max 한쪽만 입력해도 데이터 범위로 보완;
  `uirevision`이 축·범위·스케일 키로 구성돼 스타일 변경 시 줌 유지), `buildAnnotations`(포인트 레이블: 중복 제거→그리디 겹침 회피→텍스트 마커, `_kind`로 구분),
  `baselineShapes`(베이스라인 배열→점선+사분면 음영), `paretoTrace`, 그리고 `renderPlot`(Plotly.react + 이벤트 바인딩)
  - **파레토**(v0.20.1 재점검): `paretoTrace(cfg, rows)`는 **화면에 그려진 점 기준**으로 계산한다 —
    흐리게 행 제외(`isMutedRow`, 추세선과 같은 규칙) + `ptAgg`가 켜져 있으면 시리즈별 집계 점을 쓴다.
    **원본 행으로 계산하면 집계 모드에서 선이 어느 점도 지나지 않는다**(실제 버그였다).
    facet에서는 그리지 않는다(전체 데이터 선이 첫 패널에만 얹힌다). 막대·히트맵·덤벨·분포는 앞에서 return되어 도달하지 않는다.
    trace 이름은 번역되므로 식별은 `_pareto` 플래그로 한다(`plotly_click` 가드가 이 플래그를 본다 — 이름 문자열로 비교하지 말 것).
    4방향(`min/max-x` × `min/max-y`) 계산은 독립 구현과 대조해 정확함을 확인했다(`e2e-pareto`).
    **가독성**(v0.21): 계산(`paretoFront`)과 선 그리기(`paretoTrace`)를 나눠 시리즈 trace가 프런티어 집합을 먼저 알 수 있게 했다.
    선은 **잉크색(`CHROME.ink2`) 실선**이 기본 — 회색 점선은 베이스라인과 톤이 같아 묻혔다.
    모양·굵기는 `cfg.paretoDash`/`paretoWidth`, 색은 `cfg.paretoColor`(v0.21.2 — **빈 값 = 테마 자동**, `cfg.fontColor`와 같은 규칙).
    기본을 시리즈 색이 아닌 테마 잉크로 두는 이유: 프런티어는 특정 시리즈가 아니라 전체에 대한 판정이라
    시리즈 색을 주면 그 그룹의 선처럼 읽힌다. 색 입력은 빈 값을 가질 수 없으므로 **`자동` 버튼으로 되돌릴 길을 함께 둔다**.
    `cfg.paretoFade`면 시리즈 trace의 `marker.opacity`/`size`를 **점별 배열**로 준다(trace를 쪼개지 않는다 — 쪼개면 선이 끊기고,
    프런티어 점이 없는 시리즈는 Plotly가 범례에서 지운다). 선이 없는 차트에서만 프런티어 점을 앞으로 당겨
    범례 견본이 진하게 나오게 한다 → **견본이 옅다 = 그 시리즈는 프런티어에 하나도 못 올렸다**는 읽기가 된다.
    dataviz 지침상 마크에 테두리를 둘러 구분하는 것은 금지이므로 focus+context(옅게)로 처리한다.
  - **주의**: `renderPlot`에서 플롯이 이미 있는 div의 innerHTML을 지우면 안 된다(placeholder일 때만 지움) —
    지우면 Plotly.react가 증분 업데이트만 해서 화면이 빈 채로 남는다 (실제 있었던 버그)
- **설정 UI**: `buildCfgPanel` — 그룹(details)별 입력 위젯. 새 옵션의 UI는 여기에. 동적 목록(베이스라인/마커/숨긴 레이블)은 `cfg._refreshLists()`로 갱신
  - **라벨 규칙**(v0.24): `row(label, ...ctrl)`은 **labelable 컨트롤이 정확히 하나일 때만** id(`vzc<n>`, 전역 `ctlSeq`)를 발급해 `<label class="lbl" for>`로 잇는다.
    둘 이상이면 `<span class="lbl">`를 그대로 두고 각 컨트롤에 `aria-label`(자기 `title`/`placeholder`/앞 보조 라벨, 없으면 순번)을 준다 —
    **하나에만 이으면 나머지를 조용히 잘못 이름 짓는다**(이름이 없는 것보다 나쁘다). CSS는 `.row > .lbl`이다(`span.lbl`로 좁히지 말 것 — 검증 스위트가 이걸로 라벨을 찾는다).
    감싼 `<label class="inline">` 안의 체크박스는 이미 이름이 있으므로 세지 않는다.
  - **그룹 펼침**(v0.24): 차트별 `cfg._open`은 여전히 세션에서 빠진다(차트 UI 상태 규칙). 대신 마지막으로 연 그룹을
    `localStorage['vtc-visualizer:groups']`(`groupPrefs`)에 브라우저 기본값으로 두고 `restoreGroupState()`가 `_open`이 없을 때 쓴다.
    **`<details>`의 `toggle`은 비동기로 온다** — 검색이 프로그램으로 여닫을 때는 `grpSilent`를 켜고 `setTimeout(…, 0)`으로 풀어야 한다(같은 턴에 풀면 검색 결과가 기본값으로 저장된다).
  - **설정 검색**(`cfgSearchBox`): `.lbl` 텍스트 + 행 전체 텍스트로 매치(선택지 이름 `로그`가 잡히게), 0건이면 `.cfg-noresult` 안내.
    시리즈가 6개(`SERIES_FOLD`)를 넘으면 시리즈 목록을 `details.sub-grp`로 한 겹 더 접는다 — **`grp` 클래스를 주지 말 것**(검색이 `details.grp`만 훑는다).
- **팝오버·모달 포커스**(v0.24): 팝오버는 `<body>` 끝에 붙은 단일 노드라 Tab 순서가 트리거를 따라오지 않는다 →
  `placePopover()`가 `role="dialog"`+이름을 붙이고 **안의 첫 focusable로 포커스를 옮기며** 트리거를 `ppOpener`에 기억한다.
  `hidePopover(restore)`는 **`restore === true`일 때만**(= Escape) 포커스를 되돌린다 — 바깥 클릭으로 닫혔는데 끌어오면 방금 누른 것을 빼앗는다.
  `hidePopover`가 onclick 핸들러로도 쓰이므로(첫 인자 = MouseEvent) 반드시 `=== true`로 볼 것.
  `focusout`으로도 닫지만 **검사를 `setTimeout(…, 0)`으로 미룬다** — 목록을 다시 그리는 경로(컬럼 메뉴의 `모두 표시` 등)는
  innerHTML을 갈아 끼우는 사이 잠깐 포커스를 잃으므로 즉시 닫으면 방금 누른 메뉴가 사라진다.
  점 앵커 텍스트 마커의 키보드 경로는 `showMarkerAddPopover()` — 점 대신 **행**을 고른다(앵커가 어차피 `rk`라 같은 것을 다른 입구로 고르는 것).
  행이 `MARKER_PICK_MAX`(300)를 넘으면 목록 대신 클릭을 안내한다.
  붙여넣기 모달은 `role="dialog" aria-modal` + `closeModal()`(→ `#btnPaste` 복귀) + Tab 트랩.
- **이벤트**: `plotly_click` → `showPointPopover`(베이스라인 추가/제거 · 포인트 제외(`_excluded`, 전 차트 공통) · 텍스트 마커 추가 메뉴),
  `plotly_clickannotation` → 포인트 레이블 개별 숨김 / 텍스트 마커 편집(`showMarkerEditPopover`),
  `plotly_relayout` → 주석 드래그 오프셋 저장(`_kind`별로 `labelOffsets` 또는 `textMarkers`) 및 줌 시 음영 재계산
- **카드 요약**(v0.39): `cardSpecText(cfg)` + `applyCardSpec(cfg)` — **설정을 접었을 때만** 보인다(펼쳐져 있으면 같은 내용이 두 번이다).
  리포트용 `chartSpecText`와 따로 두는 이유: 그쪽은 로그축·집계까지 적어 헤더 한 줄에서 흐른다.
  갱신은 `renderPlot`(모든 설정 변경이 거친다) · 설정 토글 · `relabelCards`(언어) 세 곳.
- **차트를 표로**(v0.26): 카드 헤더 `표` → `toggleChartTable()`/`renderChartTable()`, 상태는 `cfg._asTable`(`_` 접두사라 세션 제외).
  컬럼은 `chartTableCols()`(그 차트가 실제로 쓰는 필드만), 행은 `chartRows()`(그 차트의 필터·데이터셋 적용) —
  **그림과 다른 행을 보여주면 표가 거짓말이 된다**. 그래서 `renderPlot`이 끝날 때마다 다시 그린다.
  `CHART_TABLE_MAX`(300)에서 자르고 캡션에 전체 행 수를 적는다.
  **카드 헤더에 버튼을 추가·이동하면 `relabelCards()`의 labels/titles 배열도 같이 고쳐야 한다** — 위치로 붙인다.
  헤더에는 이름 다음에 `.spec`(요약, v0.39)이 있다 — `relabelCards`는 `.head button`만 세므로 안전하지만,
  **`nth-child`로 헤더 버튼을 집는 코드는 전부 어긋난다**(검증 스위트가 실제로 깨졌다). 텍스트로 찾을 것.
- **부분 렌더링**(v0.12): `refreshCharts()`(전체 재생성)는 세션 복원·전체 초기화·init에서만 쓴다. 그 외에는
  `appendChartCard()`(추가) · 카드 `remove()`(삭제) · `relabelCards()`(언어 전환) · `refreshCfgPanels()`(데이터 변경) ·
  카드 하나 `replaceWith`(프리셋) 로 국소 갱신 — **전체 재생성은 줌·설정 패널 접힘·스크롤·포커스를 모두 날린다**.
  차트별 UI 상태는 `_` 접두사 필드(`_open`{그룹키}·`_cfgHidden`)에 두면 `serializableChart()`가 세션에서 자동 제외.
  **예외: 카드 접힘 `collapsed`는 정식 필드로 세션에 남긴다**(v0.40) — 줌·패널 펼침 같은 일시 상태가 아니라
  "이 차트는 지금 안 본다"는 의도다. 대신 `chartPreset()`에서는 지운다(프리셋을 적용했더니 접히면 놀란다).
  접기는 `setCollapsed(cfg, on)` 한 곳으로 — 카드에 `.folded` 클래스를 걸어 **몸통 전체**(설정 패널·그림·표·캡션·안내)를 감춘다.
  **그림만 감추면 안 된다**(v0.40.1에서 고쳤다): 설정을 펼쳐 둔 카드는 길이가 그대로라 "접었는데 아무 일도 안 일어난다"가 된다.
  접힌 카드에서는 설정이 열려 있어도 헤더 요약을 보인다(`applyCardSpec`) — 아래에 아무것도 없으니 유일한 단서다.
  검증에서 접힘을 볼 때는 `plot.style.display`가 아니라 **실제로 보이는 높이**를 봐야 한다(클래스로 감춘다).
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
- **행 정체성**(v0.14): `rowKeyCols(src)`가 "조건 컬럼"(문자열 + 고유값이 행 수/3 이하인 숫자)을 골라 `rowKey(r)`를 만든다.
  **판정은 파일마다 따로 한다**(v0.35) — 합집합으로 고르면 파일이 하나 더 들어올 때 그 파일에만 있는 컬럼이
  나머지 행에서 빈 값이라 "값이 몇 개뿐"으로 보여 **측정값이 키에 섞이고**, 저장해 둔 `rk` 문자열이 통째로 어긋난다
  (`예시 더` 한 번에 기준선 2개가 사라졌다). `rowKey(r)`는 인자가 없으면 `r._source`의 키를 쓴다.
  `markerAnchorRows()`는 새 키와 **옛 합집합 키를 함께** 담아 예전 세션의 앵커도 찾아간다.
  같은 이름 데이터셋을 다시 넣으면 `addDataset`이 이 키로 `_excluded`/`_muted`를 되붙이고, 포인트 레이블은
  `pointKeyRow()`(행 정체성) 키를 우선 쓰되 예전 값 기반 키(`pointKey`)도 계속 읽는다.
  **측정값이 키에 들어가면 갱신 때 전부 어긋난다** — 임계값을 느슨하게 바꾸지 말 것.
  **계산 컬럼도 키에서 뺀다**(v0.25) — 데이터에서 다시 만들어지는 값이라 정체성에 넣으면 순환이다.
  실제로 깨졌다: `bin`이나 `lookup`처럼 값이 몇 개뿐인 파생 컬럼이 있으면, 같은 파일을 다시 넣을 때
  `addDataset`이 **옛 행의 파생값 vs 아직 계산되지 않은 새 행**을 비교해 `_excluded`/`_muted`가 통째로 사라졌다.
  (숨김과는 다른 이야기다 — 숨김은 원본 컬럼을 화면에서만 뺀 것이라 `columns()` 기준 그대로다.)
- **베이스라인 앵커**(v0.28): 마커와 **같은 기계를 쓴다** — `resolveBaseline(cfg, b, rowsByKey)`가 `resolveMarker`와 같은 모양이고
  행 조회도 `markerAnchorRows()`를 재사용한다. 클릭으로 만든 것만 `{rk, xc, yc}`를 갖고(`markerAnchorFor` 그대로),
  **설정 패널에서 값으로 넣은 것(`rk` 없음)은 좌표에 고정**한다 — "정확히 0.80"은 값 자체가 의미이지 행을 가리키지 않는다.
  **점에 묶기 ↔ 값 고정은 목록에서 토글한다**(v0.36.1): 뗄 때는 저장 좌표가 아니라 **해석된 값**을 굳혀야 한다
  (갱신 뒤에는 둘이 다르다). 묶을 때는 `startReanchor(cfg, i, 'baseline')`을 그대로 쓴다.
  기준을 잃으면 그리지 않고 `cfg._blStaleN`에 세어 `renderPlot`이 한 번만 토스트한다(`_blStaleShown`, 마커와 같은 규칙).
  `showPointPopover`의 "이미 있는 기준선인가" 판정은 **저장 좌표가 아니라 해석된 값**으로 한다 —
  갱신 뒤에는 둘이 다르므로 좌표로 보면 같은 점에 기준선이 겹쳐 쌓인다.
  재지정 대기 상태 `tmPending`은 `{kind:'marker'|'baseline', chartId, idx}`로 **하나만** 둔다(두 벌이면 둘 다 대기 중인 상태가 생긴다).
- **텍스트 마커 앵커**(v0.15): 마커는 늘 포인트 클릭으로 만들어지므로 **좌표가 아니라 점에 묶는다** —
  **앵커를 고르는 행 집합은 푸는 집합과 같아야 한다**(v0.35.1) — `markerAnchorFor`가 `allRows()`를 훑으면
  값이 같은 다른 파일의 행·필터로 빠진 행을 물어 **만들자마자 stale**이 된다(`chartRows(c)`에서 고른다).
  못 찾은 앵커는 `anchorRescue()`가 **저장 좌표와 완전 일치**하는 점이 있을 때만 되살린다(가까운 점 스냅 금지).
  `markerAnchorFor(cfg, p)`가 클릭한 점의 행을 찾아 `{rk: rowKey(row), xc, yc}`(행 정체성 + 그때의 축 컬럼)를 마커에 담고,
  `resolveMarker(cfg, m, rowsByKey)`가 그릴 때마다 `markerAnchorRows()`(chartRows의 rowKey 맵)에서 행을 찾아 **현재 값을 다시 읽는다**.
  세 가지 모드: `paper`(고정 메모 — x·y가 0~1 비율, `xref/yref:'paper'`, `_paper` 플래그) · `xy`(rk 없는 예전 마커, 좌표 그대로) · `point`(행 앵커).
  **기준을 잃으면(행이 없음 = `gone`, 축 컬럼이 바뀜 = `axis`) 그리지 않는다** — 어긋난 주석은 그대로 보고서로 나가므로 조용히 틀리는 쪽이 가장 나쁘다.
  `buildAnnotations`가 `cfg._tmStaleN`에 개수를 남기고, `renderPlot`이 직전 값(`_tmStaleShown`)과 다를 때만 토스트 + `refreshPanels`,
  설정 목록(`renderLabelLists`)이 ⚠ 사유와 `다시 지정`(`startReanchor`→다음 `plotly_click`→`applyReanchor`, 대기 상태는 모듈 스코프 `tmPending`)을 띄운다.
  고정 메모를 끌어 옮기려면 config `edits.annotationPosition`이 필요하고, relayout 핸들러는 **`_paper` 마커일 때만** `x`/`y`를 받는다
  (점 앵커의 머리 좌표는 행이 정하므로 무시 — 받으면 앵커와 어긋난다).
- **분포 차트**: `buildDistribution(cfg, kind)` — 유형 판정은 `isDistType()`/`DIST_TYPES` 한 곳에서(문자열 비교를 네 군데로 늘리지 말 것).
  값 컬럼은 `cfg.y`이고 **X축은 필요 없다** — `renderPlot`의 `needsX`도 `isDistType()`을 본다(유형 이름을 손으로 나열해 두었다가 v0.32에서 새 둘이 빈 화면이 됐다), 그룹이 있으면 그룹별로 겹쳐 그린다(히스토그램은 `barmode:'overlay'`).
  v0.32: `violin`(Plotly 기본형 + 상자·평균선), `ecdf`(정렬 후 계단선 `shape:'hv'` — 직선으로 이으면 관측되지 않은 값에 확률을 준다.
  같은 값은 계단 하나로 접는다). **ECDF만 축이 반대다** — X=값, Y=0~1 비율이라 `buildLayout`에 전용 분기가 있다.
- **시리즈 순서**(v0.32): `cfg.seriesOrder[]` — `seriesDefs()`가 `seriesDefsNatural()` 결과를 이 순서로 정렬한다.
  **색은 `colorIdx`가 def에 붙어 있어 순서를 바꿔도 엔티티를 따라간다**(색은 자리가 아니라 엔티티의 것 — 이 계약을 깨지 말 것).
  목록에 없는 시리즈는 뒤에 자연 순서로(안정 정렬). UI의 `순서 되돌리기`는 **`seriesBox` 안**에 둔다 —
  `gStyle`에 두면 패널을 통째로 다시 지을 때까지 안 보인다(실제로 그랬다).
- **최적점 표시**(v0.32): `cfg.markBest`(none|max|min)/`markBestScope`(all|series) → `bestAnnotations()`.
  **계산된 주석**이라 `textMarkers`와 섞지 않는다 — 마커는 사용자가 놓고 행에 묶여 stale 판정을 받지만 이건 그릴 때마다 다시 고른다.
  분포·히트맵·덤벨·facet에서는 그리지 않는다(그 좌표계에서 "가장 좋은 점"이 그 뜻이 아니다).
- **보조 Y축**: `cfg.y2` → `hasY2()`/`y2Layout()`. 기본 경로 레이아웃은 `baseLayout`을 쓰지 않으므로 **두 곳 모두에 적용**해야 한다.
- **차트별 데이터셋**(v0.19): `cfg.dataset`(빈 값 = 전체) — 행 한정은 **`chartBaseRows(cfg)` 하나를 거친다**(v0.33).
  `chartRows()`는 그 위에 축 값 유무를 더한 것이고, 분포·히트맵·덤벨은 x/y가 다른 뜻이라 `chartBaseRows`를 직접 쓴다.
  **`allRows()`를 직접 쓰면 데이터셋 선택이 조용히 무시된다** — v0.19부터 넷이 그랬고 가이드 그림을 찍다가 드러났다.
  `chartColumns(cfg)`/`chartNumCols(cfg)`가 축·그룹·필터·계산 컬럼 드롭다운을 그 파일에 **실제로 값이 있는 컬럼**으로 좁힌다
  (`datasetColumns(name)`, `dataVer` 캐시). UI는 파일이 2개 이상일 때만 노출.
  전환은 반드시 `switchDataset()`을 통할 것 — 그 파일에 없는 컬럼을 쓰던 설정(`DATASET_COL_FIELDS` + 필터)을 비우고
  `guessAxes()`로 축을 다시 고른 뒤 무엇을 비웠는지 알린다. **비우지 않으면 드롭다운에 없는 값이 남아 화면과 설정이 어긋난다.**
  데이터셋이 사라질 때(`onDataChanged`)도 같은 경로를 태운다 — `dataset`만 되돌리면 그 파일에만 있던 컬럼을 가리키는 축이 남아 빈 차트가 된다.
  `applyPreset()`은 프리셋이 가리키는 파일이 없으면 전체로 열고 알린다.
  원래도 `_source`를 분할·그룹·필터로 쓰면 파일별로 볼 수 있었다 — 이건 그 위의 지름길이고, 여러 파일을 **겹쳐** 비교하려면 분할=`_source`가 맞다.
- **테이블**: `renderTable` (검색/정렬/페이지네이션 200행, 행 앞 체크박스로 `_excluded` 토글 → 전 차트에서 제외).
  숫자 컬럼은 `numericColumns()`로 판정해 `th`/`td`에 `.num`(우측 정렬)을 붙인다.
  v0.24: 두 번째 열이 **흐리게(`_muted`) 체크박스**다 — 포인트 클릭 말고는 경로가 없던 것을 표에도 낸 것이다(`analysisStale()` 필수).
  헤더는 `tabindex="0"` + Enter/Space + `aria-sort`, 체크박스는 `rowKeyCols()` 값으로 만든 `aria-label`을 갖는다.
  **행을 다시 그리면 포커스가 사라지므로**(`renderTable`은 innerHTML을 통째로 갈아 끼운다) 정렬·토글 뒤에는 같은 자리로 포커스를 되돌린다.
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
  `starterRoles()`가 지금 데이터에서 역할을 찾는다 — **종류는 `anProfile()`(값의 분포, 이름을 보지 않음)이 가르고
  이름 패턴(`SP_SCORE_RE`/`SP_COST_RE`)은 같은 종류 안에서 순서를 정하는 데만 쓴다**(v0.17.1). `anProfile`은 독립 함수라
  분석을 돌리지 않고 부를 수 있고, `id`(시드·일련번호)는 자동으로 축 후보에서 빠진다.
  비용 축은 연속량을 스윕 노브보다 먼저 고른다(노브를 X로 쓰면 스윕 레시피와 같은 그림이 된다).
  결과는 `dataVer + hiddenCols` 키로 캐시(`starterRoleCache`) — 5만 행 첫 호출 536ms, 이후 1ms.
  `starterList()`가 **역할이 채워지는 레시피만** 내놓는다 —
  눌렀더니 빈 차트가 되는 것이 가장 나쁘므로 목록에 아예 띄우지 않는다. 로그축은 `logFits()`(최대/최소 ≥ 8)일 때만.
  적용은 기존 `applyPreset()`을 그대로 쓰고 저장은 하지 않는다(사용자가 다듬은 뒤 직접 저장).
  **실무 시나리오용 프리셋은 이 목록에 넣지 않는다** — 공개 레포이고 컬럼 이름이 곧 실험 설계다(로컬 전용 JSON으로 유지).
- **계산 컬럼**: `state.derived[]`(세션 저장, 입력 계약 아님 — 뷰 계층) → `applyDerived()`가 로드/변경 시 각 행에 파생 값 주입
  (`derivedApplied`로 직전 컬럼까지 제거해 삭제 반영). 종류: binary(A∘B, `bConst`로 상수 피연산자), refdelta(키 매칭 기준행 대비 차이/유지율),
  norm(minmax|max|z), rank(desc 여부), bin(동일 폭 N구간 → **문자열** 라벨이라 그룹·필터로 쓰인다), groupagg(그룹 통계를 행에 브로드캐스트),
  **concat**(v0.18 — 계산이 아니라 라벨 만들기: `parts[{col,pre,post}]`를 `sep`으로 이어 붙인 **문자열** 컬럼. 값이 없는 조각은 건너뛰고(구분자만 남지 않게)
  전부 비면 null. 결과가 문자열이라 그룹·분할·필터·막대 X축 후보가 된다),
  **lookup**(v0.25 — 파일 간 결합: `{from, keys[], col, agg}`. `from` 데이터셋 행을 `keys`로 Map에 담아 전 행에 값을 붙인다.
  **행을 절대 늘리지 않는다** — 늘리면 `rowKeyCols()`의 행 정체성이 깨져 제외·흐리게·레이블·마커 앵커가 전부 어긋난다.
  짝이 여럿이면 `agg`(first|mean|sum|min|max|count)로 접고, 짝이 없으면 **0이 아니라 null**.
  키는 `` 조인(`rowKey`와 같은 규칙, `|`는 값에 나올 수 있다).
  **정의 하나 = 컬럼 하나**가 불변이다(`derivedApplied`·이름 충돌 검사·`colUsage`가 전제) — 메타 넷을 붙이려면 정의 넷.
  UI는 키 후보를 **양쪽 파일에 다 있는 컬럼**으로 좁히고 `syncHint()`로 몇 행이 짝을 찾는지 미리 센다 —
  조용히 빈 컬럼이 생기는 것이 가장 나쁜 실패다. 파일이 2개 이상일 때만 종류 목록에 나온다).
  **kind를 추가하면 `derivedInputs(d)`(입력 컬럼 목록)와 분석의 `derivedPairs` 부모 등록에도 반영할 것** — 안 하면 삭제 시 사용처가 안 잡히고 자명한 상관이 발견으로 나온다.
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
- **폴더 감시**(v0.27): `/api/stat`이 `{상대경로: "mtime-size"}`를 준다 — **목록(`_data_files`)과 같은 규칙으로 훑어야** 감시가 목록에 없는 파일을 물지 않는다.
  프런트는 `watchStat`과 비교해 **바뀐 파일만** 다시 받는다(전부 받으면 큰 폴더에서 화면이 계속 덜컹인다). 키 `vtc-visualizer:watch`, 주기 `WATCH_MS`.
  갱신은 `addDataset`을 그대로 태우므로 행 정체성으로 제외·흐리게가 되붙는다.
  **사라진 파일은 지우지 않는다** — 쓰는 중·이름 바꾸는 중에 잠깐 없을 수 있고, 화면에서 사라지면 되돌릴 길이 없다.
- **가로 → 세로 녹이기**(v0.27): `meltRows(rows, idCols, valCols, varName, valName)` + `showMeltPopover()`.
  **행이 늘어나므로 계산 컬럼이 아니다** — 계산 컬럼은 행 안에서만 동작하고 행 증가는 행 정체성을 깬다.
  그래서 원본을 두고 **새 데이터셋**(`meltName()`으로 안 겹치는 이름)을 만든다. 빈 칸은 건너뛴다(측정점이 아니다).
  기본 추정은 "숫자 = 녹일 값, 나머지 = 남길 조건"이고, 자주 틀리므로(스윕 노브가 숫자다) 체크박스로 고치게 둔다.
- **공유용 HTML 한 장**(v0.27): `exportStandalone()` = `document.head.outerHTML`(오프라인 빌드라면 Plotly가 여기 인라인돼 있다)
  + `window.__VTC_EMBED = {...}` 스크립트 + **렌더 전에 붙잡아 둔 `PRISTINE_BODY`**.
  **body를 지금 DOM에서 뜨면 안 된다** — 그려진 차트·표·팝오버가 섞여 열리지 않는다. 그래서 스크립트 첫 줄에서 붙잡는다.
  상태 스크립트는 앱 스크립트보다 **앞**에 놓아야 한다(`loadSaved()`가 그걸 먼저 본다). `<`/`>`는 escape — 데이터에 `</script>`가 들어가면 페이지가 깨진다.
- **서버 연동**: `tryServerAutoload` — `api/files`/`api/file` (http로 열렸을 때만).
  **목록과 접근 규칙은 반드시 같아야 한다**(`visualizer.py`의 `_data_files()` / `_inside()`) — 목록에 있는데 404가 나는 파일이 있으면
  자동 로드가 그걸 물고 늘어져 `networkidle0`가 영영 안 떨어진다(헤드리스 검증 전체가 이것 때문에 멈춘 적이 있다.
  `_send`의 404 응답은 브라우저 쪽에서 요청이 끝난 것으로 보이지 않는다 — 예전부터 그랬다).
  목록은 `os.walk(followlinks=False)`로 훑어 **숨김 폴더·숨김 파일·폴더 밖을 가리키는 링크를 건너뛰고 500개에서 멈춘다**:
  `.git`/`.venv`/도구 설정 폴더의 json을 데이터로 읽어 들이면 안 되고, 링크를 따라가면 폴더 밖으로 나가거나 순환에 빠진다.
- **창 크기 변경**: Plotly `responsive: true`가 이미 처리한다. 리사이즈 리스너를 따로 달지 말 것 —
  차트마다 `Plotly.Plots.resize`가 한 번 더 도는 중복 경로가 될 뿐이다(디바운스를 얹어도 Plotly 쪽 핸들러는 그대로 돈다).

새 차트 옵션 추가 절차: `defaultChart()`에 필드 → `buildCfgPanel`에 입력 UI → `buildTraces`/`buildLayout`에 반영 → 세션 저장은 자동.

주의: Plotly 로그축 좌표 규약은 **비대칭**이다 (실측 검증됨) — annotation의 x/y는 log10 값(`axCoord()` 헬퍼 사용),
**layout.shapes의 x0/y0 등은 원시 데이터 값**(axCoord 금지). `gd._fullLayout.[xy]axis.range`는 로그축이면 log10 값이므로
shapes 계산에 쓸 때는 `Math.pow(10, v)`로 되돌릴 것 (`baselineShapes()`의 `unlog` 참고).

## annotate.html (이미지 주석)

- **좌표는 원본 이미지 픽셀로 저장한다.** 화면에서는 `view` 배율로 축소해 보여주고, 그릴 때·집을 때만 환산한다.
  화면 좌표로 저장하면 **창 크기가 결과를 바꾼다**.
- **화면과 저장이 같은 `paint(ctx, scale, withSel)`을 쓴다** — 두 벌로 두면 화면에는 맞는데 저장본만 어긋난다.
  선택 표시는 `withSel`로만 나오므로 저장본에 들어가지 않는다.
- **가리기는 불투명이어야 한다** — 반투명이면 아래 글자가 비쳐 가린 의미가 없다.
- **글자 배경도 같은 이유로 불투명이다**(v0.29.1, `m.bg`) — 85%로 두었더니 아래 선이 비쳐 글자색이 탁해졌다.
  대신 **끌 수 있게** 했다(배경이 그림을 가리는 자리가 있다). 텍스트가 아닌 마크에는 이 필드를 남기지 않는다.
  마크를 고르면 `syncStyleInputs()`가 입력을 그 마크 값으로 되비춘다 — 안 하면 체크 상태가 고른 것과 어긋나 보인다.
- **새 이미지는 마크를 전부 지운다 — 되돌리기가 없는 유일한 경로**라 `loadFile`에서 확인을 받는다(v0.29.2).
  드롭존 점선은 이미지가 들어오면 거둔다(`#dropzone.has`) — 드래그 중에만 되살린다.
  캔버스의 파란 점선은 **선택 표시**이고 `paint(c, s, withSel)`의 `withSel`로만 나오므로 저장본에는 없다.
- 되돌리기는 `marks` 스냅샷 통째로(`JSON.stringify`)다. 연산별 역함수를 두는 것보다 짧고 안 틀린다. 50개까지.
- 저장 키(`vtc-visualizer:lang`/`:theme`)를 `index.html`과 **공유**한다 — 두 페이지의 언어·테마가 따로 놀면 같은 도구로 보이지 않는다.
- 서버는 `/annotate.html` **한 경로만** 준다(`visualizer.py`). 정적 파일 서버로 만들면 레포 전체가 읽힌다.
- 안 넣은 것: 레이어 · 자유 곡선 · 여러 이미지 · **작업 상태 저장**(저장을 넣으면 세션·포맷 호환이라는 새 계약이 생긴다).

## 일부러 안 고친 것 (다시 판단하지 말 것)

재 보고 값이 안 나온다고 결론 낸 것들. 사용자 문서에도 "알려진 한계"로 적혀 있다.

- **분석 속도**: 상관 쌍마다 그룹을 다시 나누는 부분을 미리 계산해 봤더니 최악 조건에서 **10%**(3,177 → 2,865 ms)였고
  미묘한 순서 불변이 생겨 되돌렸다. 프로파일상 비용이 흩어져 있다(analyzeData 본문 826 · anPairXY 356 · anDescribe 355 · anRanks 252 ms).
  **다시 손대려면 프로파일부터 다시 뜰 것** — 지배적인 한 곳이 생겼는지 보고 나서.
- **WebGL 컨텍스트 한도**: 브라우저 제한이고 `renderMode: 'svg'` 고정 경로가 이미 있다. 자동 폴백은 컨텍스트 수를 믿을 만하게 셀 방법이 없다.
- **기본 프리셋이 데이터당 한 벌**: 후보를 여러 개 내면 목록이 금세 길어져 "누르면 되는 것"이라는 성질을 잃는다.
- **폴더 감시 폴링(4초)**: 로컬 폴더에는 충분하다. 파일 감시 API를 쓰려면 서버가 상태를 들고 있어야 한다.
- **결합은 정의 1개 = 컬럼 1개**: 한 정의가 여러 컬럼을 내면 `derivedApplied`·이름 충돌 검사·`colUsage`의 전제가 깨진다.

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
