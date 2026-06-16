# 지역 출장마사지·홈타이 사이트 제작 플레이북 (간다GO 템플릿)

> 이 저장소(안성 출장마사지·홈타이 / 간다GO) 구조를 그대로 복제해
> 다른 지역에도 동일한 사이트를 만들 수 있습니다.
> 핵심 설계: **행정구가 없는 시 → 대표 행정동(읍·면·동) → 지하철역 또는 생활권·교통거점**, 페이지 수를 과하게 늘리지 않는 린(lean) 구조.
> 안성처럼 **운영 중인 철도역이 없는 시**는 지하철역 페이지를 만들지 않고, 터미널·IC·대학·택지 등 실제 이동 기준 거점(landmarks)으로 대체한다.

---

## 0. 핵심 원칙 (절대 규칙)

```
구조는 시 → 읍·면·대표 동 → 지하철역(또는 생활권·교통거점) 순서. 허브 페이지는 따로 두지 않고 메인 앵커로 묶는다.
번호 행정동은 통합한다 (예: 안성1·2·3동 → 안성동, 교문1·2동 → 교문동).
지하철역은 역 1개당 페이지 1개 — 환승역도 URL 하나, 노선별·출구별 페이지 금지.
철도역이 없는 시는 역 페이지를 만들지 않는다 — 폐역·예정역 단독 색인 페이지 금지, 예정 철도는 본문 보조 설명으로만.
생활권·교통거점은 터미널·IC·대학·택지처럼 실제 이동 기준이 있을 때만 만든다.
지역+거점+테마 조합 페이지 금지 (도어웨이 방지).
모든 색인 페이지 본문 2,000~2,500자 (2,000자 미만은 빌드가 자동 noindex).
지역명만 바꾼 복붙 페이지 금지 — 동·역마다 실제 지역 사실로 다르게 작성.
메타 디스크립션은 전 페이지 80자 이내.
타이틀은 "지역명 출장마사지｜…" 처럼 키워드 선두 배치.
실제 오프라인 매장 주소가 없으면 LocalBusiness Schema 금지 → Organization 사용.
모든 페이지에 페이지별 고유 og:image(검색 썸네일) 지정.
불법·선정적 표현 금지, 신뢰 요소(방문지역·시간·이동비·결제·취소·개인정보) 명시.
```

---

## 1. 기술 구조

```
build.py            # 빌드: 레이아웃·목차·글자수 검사·sitemap·robots 생성 + 페이지별 og:image 주입
content/
  site.py           # BASE_URL·상호·전화·메뉴(NAV) 정의
  main.py           # 메인 (히어로 + WebPage/BreadcrumbList/Organization/FAQPage JSON-LD)
  areas.py          # 읍·면·대표 동 N개 (_area 헬퍼)
  landmarks.py      # 생활권·교통거점 N개 (_landmark 헬퍼) — 철도역 있는 시는 stations.py(_station)로 대체
  info.py           # 예약 안내·이용 전 확인사항·홈타이 가이드·고객센터·개인정보 처리방침
  __init__.py       # PAGES = main + areas + landmarks + info
assets/
  style.css         # 다크 럭스 골드 디자인 시스템
  nav.js            # 모바일 메뉴 + 목차 스크롤스파이
  favicon.svg/ico, favicon-16/32, apple-touch-icon, icon-192/512  # 브랜드 이니셜 마크
  og-image.png      # 메인 대표 이미지(검색/SNS 썸네일)
  og/{slug}.png     # 페이지별 검색 썸네일
scripts/
  gen_thumbs.py     # 페이지별 og 썸네일 생성기 (Pillow + cairosvg)
```

페이지 정의는 dict 하나:

```python
{
  "path": "anseong/gongdo-eup-chuljangmassage/",  # 끝에 / (메인은 "")
  "title": "...",          # 28~40자, 키워드 선두
  "desc": "...",           # 80자 이내
  "h1": "...",
  "body": "...HTML...",     # <section><h2>…</h2><p>…</p></section> 반복
  "breadcrumb": [("읍·면·대표 동별 안내", "/#areas"), ("공도읍", None)],
  "og_image": "/assets/og/gongdo-eup-chuljangmassage.png",  # 페이지 썸네일(선택)
  "extra_head": "...",     # JSON-LD 등 (선택)
  "hero": "...",           # 히어로 (메인 전용, 선택)
  "noindex": True,         # 강제 noindex (개인정보 처리방침 등, 선택)
}
```

빌드 자동 처리: H2 섹션 id·좌측 목차(TOC) 생성, 2,000자 미만 noindex + sitemap 제외,
2,500자 초과 경고(⚠), canonical/og:image/image_src/파비콘 head 삽입.

빌드: `python3 build.py` → 페이지별 글자수·색인 리포트 출력.

---

## 2. 페이지 구성 (이 저장소 = 28페이지)

```
메인 1                      /
읍·면·대표 동 13            /anseong/{dong}-chuljangmassage/    (예: gongdo-eup, anseong-dong)
생활권·교통거점 9           /anseong/{landmark}-chuljangmassage/ (예: anseong-terminal, iljuk-ic)
예약 안내                   /reservation/
이용 전 확인사항            /guide/
홈타이 이용 가이드          /hometai/
개인정보 처리방침(noindex)  /privacy/
고객센터                    /support/
```

상단 메뉴(NAV)는 짧게: 하위 메뉴엔 키워드 반복 없이 **동·거점 이름만**.
읍·면·동·거점 그룹의 부모는 페이지가 아니라 메인 앵커(`/#areas`, `/#landmarks`)로 연결.

---

## 3. 메인 페이지 작성법

- H1: `OO 출장마사지 · OO시 홈타이 지역별 예약 안내`
- 섹션: 서비스 안내(리드) → 찾는 이유 → 홈타이 확인사항 → 대표 행정동(카드 N) →
  역세권(카드 N) → 예약 전 기준 → 사이트 이용 가이드 → FAQ(5) → CTA
- JSON-LD 4종: **WebPage + BreadcrumbList + Organization + FAQPage** (LocalBusiness 금지)
- 총 2,100~2,500자.

## 4. 대표 행정동 페이지 (8섹션 템플릿, 2,000~2,500자)

```
Title: {동} 출장마사지｜핵심역·랜드마크 홈타이 안내
H1:    {동} 방문 관리 안내
리드 → {동} 생활권 특징(그 동만의 사실) → 가까운 역세권(역 내부링크) →
이런 상황에 많이 이용(동별 시나리오 3~4) → 방문 가능 형태와 시간 →
{동}에서 많이 찾는 관리(테마 페이지 없으므로 프로즈로 설명, /hometai/ 1회) →
방문 전 확인사항 → FAQ 4(통합 행정동 질문 + 도착 소요시간 + 동 특수질문)
```

## 5. 지하철역 페이지 (7섹션 템플릿, 2,000~2,500자)

```
Title: {역} 출장마사지｜인근 동·생활권 홈타이 안내
H1:    {역} 인근 방문 관리 안내
리드 → {역} 역세권 분위기(역마다 다르게) → 인근 생활권과 대표 동(동 내부링크) →
이런 일정에 자주 이용(역별 시나리오) → 방문 형태와 시간대 →
{역} 인근 예약 팁(이 역만의 실전 팁) → FAQ 3(역 고유 질문)
```

환승역도 페이지 하나. 본문·FAQ에 "노선이 둘이라도 페이지는 하나, 출구별 안내 없음" 명시.

## 6. 내부링크 설계 (예시)

메인 → 모든 동·역 + 예약 안내. 동 페이지 → 인접 역 1~2 + 인접 동 1~2 + 안내 페이지 1.
역 페이지 → 소속 동 1~2 + /hometai/ + /reservation/. 깨진 링크 0 유지.

---

## 7. 검색 썸네일(og:image) 만들기

- 검색 결과 우측 썸네일은 `og:image`에서 나온다. **페이지마다 고유 썸네일**을 쓰면 CTR↑.
- `scripts/gen_thumbs.py`의 `PAGES` 딕셔너리에 `슬러그 → (지역태그, 1줄, 2줄)`만 채우고 실행.
  ```bash
  pip install Pillow cairosvg        # 최초 1회
  python3 scripts/gen_thumbs.py      # assets/og/*.png 생성
  ```
- 각 페이지 dict에 `"og_image": "/assets/og/{slug}.png"` 추가 → build.py가 자동 주입.
- 한글 폰트: WenQuanYi Zen Hei(설치 환경 기준). 더 좋은 결과는 Noto Sans KR 사용.

---

## 8. 다른 지역으로 복제하는 절차

1. 저장소 복사 후 `content/site.py` 수정: `BASE_URL`·`BRAND`·`PHONE`·`NAV`(동/역 교체).
2. 대상 시의 **대표 행정동 목록**(번호 행정동 통합 규칙)과 **노선·역 목록** 조사.
3. `areas.py`: 동 수만큼 `_dong(...)` — §4 템플릿으로 **전부 새로 작성**(복붙 금지).
4. `landmarks.py`: 거점 수만큼 `_landmark(...)` — §5 템플릿. (철도역이 있는 시는 `stations.py`의 `_station(...)` 사용)
5. `main.py`: §3 구성으로 새 지역 버전, JSON-LD 지역명·FAQ 교체.
6. `info.py`: 지역 언급·상호 교체(예약/이용/홈타이/고객센터/개인정보).
7. 브랜드 이니셜 마크 교체: `assets/favicon.svg`의 글자 → 새 이니셜, 아래 재생성.
   ```bash
   # favicon PNG/ico + 메인 og-image.png 재생성은 git 히스토리의 생성 스니펫 참고
   python3 scripts/gen_thumbs.py   # 페이지 썸네일
   ```
8. `python3 build.py` → 글자수 리포트 전부 index 확인, 디스크립션 80자 이내 확인.
9. 검색엔진 등록: Google Search Console + 네이버 서치어드바이저에 `sitemap.xml` 제출.

**주의**: 여러 지역 사이트를 운영할 때 info/홈타이 본문을 도메인 간 그대로 복사하면
중복 콘텐츠가 된다. 도메인마다 본문을 다시 써야 안전하다.

---

## 9. 배포 체크리스트

- [ ] `content/site.py` `BASE_URL` 실제 도메인으로 변경 후 재빌드
- [ ] HTTPS 활성화
- [ ] `python3 build.py` — 색인 페이지 글자수 2,000+ / 디스크립션 80자 이내
- [ ] 페이지별 og:image 정상(검색 썸네일), 깨진 내부링크 0
- [ ] 모바일 실기기 확인 (햄버거, 전화 FAB)
- [ ] Search Console / 네이버 서치어드바이저 등록 + sitemap.xml 제출
- [ ] `/support/`, `/privacy/` 연락처·상호 실제 값 확인
