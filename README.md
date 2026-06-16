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
scripts/gen_thumbs.py  # 페이지별 og:image(검색 썸네일) 생성기 (Pillow)
```

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

## 배포 전 해야 할 일

1. `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경
2. `python3 build.py` 재실행 (canonical·sitemap·robots.txt에 반영됨)
3. Google Search Console / 네이버 서치어드바이저에 `sitemap.xml` 제출
