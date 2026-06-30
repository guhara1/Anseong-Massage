# 간다GO — 안성 출장마사지·홈타이 안내 사이트

경기도 안성시 전지역 방문 관리(출장마사지·홈타이) 안내용 지역 SEO 정적 사이트입니다.
예약전화: **0508-202-4719**

## 구조

안성시는 행정구가 없고 운영 중인 철도역도 없으므로 **안성시 → 읍·면·대표 동 → 생활권·교통거점** 순서로 구성합니다.
역세권 페이지를 억지로 만들지 않고, 읍·면·대표 동과 터미널·IC·대학·택지 같은 실제 이동 기준 거점 중심으로 묶습니다.

- 정적 HTML 사이트 — GitHub Pages / Netlify / 일반 웹서버 어디서나 서빙 가능
- `build.py` + `content/` 패키지에서 페이지를 생성하는 빌드 방식
- 생성물(각 디렉터리의 `index.html`, `sitemap.xml`, `robots.txt`)도 저장소에 포함

```
build.py            # 빌드 스크립트 (레이아웃·목차·글자수 검사·sitemap 생성)
content/
  site.py           # 상호(간다GO)·전화·BASE_URL·메뉴 구조
  main.py           # 메인 페이지 (+ WebPage/BreadcrumbList/Organization/FAQPage JSON-LD)
  areas.py          # 읍·면·대표 동 13개 (공도읍 + 11개 면 + 안성동)
  landmarks.py      # 생활권·교통거점 9개 (터미널·택지·대학·IC)
  info.py           # 예약 안내·이용 전 확인사항·홈타이 가이드·고객센터·개인정보 처리방침
assets/             # CSS, 모바일 내비 JS, 파비콘, OG 이미지
scripts/
  gen_thumbs.py     # 페이지별 og:image(검색 썸네일) 생성기 (Pillow)
  indexnow.py       # IndexNow 즉시 색인 통보 (빙·네이버)
  google_index.py   # 구글 Indexing API 통보
.github/workflows/indexnow.yml  # 푸시 시 자동 색인 통보
```

빌드 산출물: `index.html`(각 디렉터리), `sitemap.xml`, `rss.xml`, `robots.txt`, `{INDEXNOW_KEY}.txt`

## 페이지 구성 (총 28개)

| 구분 | 페이지 | URL |
|------|--------|-----|
| 메인 | 안성 출장마사지·홈타이 | `/` |
| 읍·면·동 | 공도읍 | `/anseong/gongdo-eup-chuljangmassage/` |
| 읍·면·동 | 보개면 | `/anseong/bogae-myeon-chuljangmassage/` |
| 읍·면·동 | 금광면 | `/anseong/geumgwang-myeon-chuljangmassage/` |
| 읍·면·동 | 서운면 | `/anseong/seoun-myeon-chuljangmassage/` |
| 읍·면·동 | 미양면 | `/anseong/miyang-myeon-chuljangmassage/` |
| 읍·면·동 | 대덕면 | `/anseong/daedeok-myeon-chuljangmassage/` |
| 읍·면·동 | 양성면 | `/anseong/yangseong-myeon-chuljangmassage/` |
| 읍·면·동 | 원곡면 | `/anseong/wongok-myeon-chuljangmassage/` |
| 읍·면·동 | 일죽면 | `/anseong/iljuk-myeon-chuljangmassage/` |
| 읍·면·동 | 죽산면 | `/anseong/juksan-myeon-chuljangmassage/` |
| 읍·면·동 | 삼죽면 | `/anseong/samjuk-myeon-chuljangmassage/` |
| 읍·면·동 | 고삼면 | `/anseong/gosam-myeon-chuljangmassage/` |
| 읍·면·동 | 안성동 (안성1·2·3동 통합) | `/anseong/anseong-dong-chuljangmassage/` |
| 생활권 | 안성터미널 | `/anseong/anseong-terminal-chuljangmassage/` |
| 생활권 | 공도 생활권 | `/anseong/gongdo-area-chuljangmassage/` |
| 생활권 | 아양지구 | `/anseong/ayang-area-chuljangmassage/` |
| 생활권 | 석정동 생활권 | `/anseong/seokjeong-dong-area-chuljangmassage/` |
| 생활권 | 중앙대 안성캠퍼스 인근 | `/anseong/chungang-univ-area-chuljangmassage/` |
| 생활권 | 한경국립대 인근 | `/anseong/hankyong-univ-area-chuljangmassage/` |
| 교통거점 | 안성IC 인근 | `/anseong/anseong-ic-chuljangmassage/` |
| 교통거점 | 서안성IC 인근 | `/anseong/west-anseong-ic-chuljangmassage/` |
| 교통거점 | 일죽IC 인근 | `/anseong/iljuk-ic-chuljangmassage/` |
| 안내 | 예약 안내 | `/reservation/` |
| 안내 | 이용 전 확인사항 | `/guide/` |
| 안내 | 홈타이 이용 가이드 | `/hometai/` |
| 안내 | 고객센터 | `/support/` |
| 정책 | 개인정보 처리방침 (noindex) | `/privacy/` |

## 빌드

```bash
python3 build.py
```

빌드 시 페이지별 본문 글자수와 색인 여부가 출력됩니다.
검색 썸네일(og:image)을 다시 만들려면 `pip install Pillow` 후 `python3 scripts/gen_thumbs.py`를 실행합니다.

## SEO 운영 원칙 (빌드에 강제됨)

- 본문 **2,000자 미만 페이지는 자동 `noindex`** 처리되고 sitemap에서 제외
- 모든 페이지 **메타 디스크립션 80자 이내**
- 읍·면·동은 대표 단위만 — 번호 행정동(안성1·2·3동)은 안성동으로 통합, 개별 페이지 없음
- **운영 중인 철도역이 없으므로 지하철역 페이지를 만들지 않음** (안성역·예정역 단독 색인 페이지 금지, 예정 철도는 본문 보조 설명으로만 처리)
- 생활권·교통거점은 안성터미널·공도·아양지구·IC·대학처럼 **실제 이동 기준이 있을 때만** 생성
- **지역+거점+테마 조합 페이지 없음** (도어웨이 방지)
- 실제 오프라인 매장 주소가 없으므로 **LocalBusiness 대신 Organization Schema** 사용
- 모든 페이지 본문은 페이지별 고유 작성 (지역명만 바꾼 복붙 없음)

## 색인 (검색엔진 즉시 등록)

빌드 시 다음 색인 자산이 함께 생성됩니다 (배포 도메인: `https://anseong-massage.netlify.app`).

| 파일 | 용도 |
|------|------|
| `sitemap.xml` | 색인 허용 27개 URL + `lastmod`/`changefreq`/`priority` |
| `rss.xml` | RSS 2.0 피드 (피드 발견·구독, 모든 페이지 `<link rel="alternate">`로 연결) |
| `robots.txt` | Googlebot·Yeti(네이버)·bingbot·Daum 명시 허용 + 사이트맵 2종 안내 |
| `{INDEXNOW_KEY}.txt` | IndexNow 키 검증 파일 (루트 평문) |

### 1) 검색엔진 콘솔 등록 (최초 1회)
- **구글 Search Console**: 도메인 등록 → `sitemap.xml` 제출
- **네이버 서치어드바이저**: 사이트 소유확인(메인페이지 메타태그 적용됨) → `sitemap.xml`·`rss.xml` 제출
- **빙 Webmaster Tools**: 사이트 등록 → `sitemap.xml` 제출

### 2) IndexNow — 빙·네이버 즉시 통보
IndexNow는 한 번 보내면 참여 검색엔진(**빙·네이버**·Yandex·Seznam 등)에 공유됩니다.
글을 올리거나 수정한 뒤:
```bash
python3 scripts/indexnow.py                 # 전체 색인 URL 통보
python3 scripts/indexnow.py <URL> [URL ...] # 변경된 글만 통보
```
키 파일(`{INDEXNOW_KEY}.txt`)이 도메인에 배포되어 있어야 검증을 통과합니다.

### 3) 구글 Indexing API — 구글 즉시 통보 (선택)
구글은 IndexNow에 참여하지 않으므로 별도 통보합니다. 서비스 계정 JSON을
Search Console에 '소유자'로 추가한 뒤:
```bash
pip install google-auth
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
python3 scripts/google_index.py             # 또는 변경 URL만 인자로
```

### 4) 자동화 — 푸시할 때마다 자동 통보
`.github/workflows/indexnow.yml`이 운영 브랜치(`main`)에 콘텐츠가 푸시되면
빌드 후 IndexNow(빙·네이버)에 자동 통보합니다. 구글 Indexing API는 저장소
시크릿 `GOOGLE_INDEXING_CREDENTIALS`(서비스 계정 JSON 전체)를 넣으면 함께 동작합니다.
> 운영 배포 브랜치가 `main`이 아니면 워크플로의 `branches` 값을 바꾸세요.

> 참고: 구글·빙의 옛 `ping?sitemap=` 방식은 2023년에 폐지되었습니다.
> 현재 빠른 색인 경로는 **IndexNow(빙·네이버) + 구글 Indexing API + Search Console 사이트맵**입니다.

## 배포 전 해야 할 일

1. `content/site.py`의 `BASE_URL` 확인 (현재 `https://anseong-massage.netlify.app`)
2. `python3 build.py` 재실행 (canonical·sitemap·rss·robots·IndexNow 키에 반영됨)
3. Google Search Console / 네이버 서치어드바이저 / 빙에 `sitemap.xml` 제출
4. 새 글/수정 시 `scripts/indexnow.py`(+선택 `scripts/google_index.py`) 실행, 또는 자동화 워크플로 사용
