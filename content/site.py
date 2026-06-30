# 사이트 공통 설정
# 배포 도메인: Netlify
BASE_URL = "https://anseong-massage.netlify.app"

BRAND = "간다GO"
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# 사이트 한 줄 소개 — RSS 채널 설명 등에 사용.
SITE_DESC = "경기도 안성시 전지역 방문 출장마사지·홈타이 예약 안내"

# IndexNow 키 — 빙·네이버 등 IndexNow 참여 검색엔진에 즉시 색인 통보용.
# 루트에 {INDEXNOW_KEY}.txt 파일로도 배포되어야 검증을 통과한다(build.py가 자동 생성).
INDEXNOW_KEY = "ba152b16e80544d3bb1dc95247d8079cebcac931a36340a5a3b6bd71271b279c"

# 상단 메뉴 — 하위 메뉴에는 키워드를 반복하지 않고 지역명·거점명만 표시한다.
# 구조: 안성시 → 읍·면·대표 동 → 생활권·교통거점. 안성은 운영 중인 철도역이 없으므로
# 역세권 대신 읍·면·대표 동과 생활권·교통거점(터미널·IC·대학·택지) 중심으로 묶는다.
# 읍·면·대표 동/생활권 허브 페이지는 따로 두지 않고 메인 페이지의 해당 섹션 앵커로 묶는다.
NAV = [
    ("홈", "/", []),
    ("읍·면·대표 동별 안내", "/#areas", [
        ("공도읍", "/anseong/gongdo-eup-chuljangmassage/"),
        ("보개면", "/anseong/bogae-myeon-chuljangmassage/"),
        ("금광면", "/anseong/geumgwang-myeon-chuljangmassage/"),
        ("서운면", "/anseong/seoun-myeon-chuljangmassage/"),
        ("미양면", "/anseong/miyang-myeon-chuljangmassage/"),
        ("대덕면", "/anseong/daedeok-myeon-chuljangmassage/"),
        ("양성면", "/anseong/yangseong-myeon-chuljangmassage/"),
        ("원곡면", "/anseong/wongok-myeon-chuljangmassage/"),
        ("일죽면", "/anseong/iljuk-myeon-chuljangmassage/"),
        ("죽산면", "/anseong/juksan-myeon-chuljangmassage/"),
        ("삼죽면", "/anseong/samjuk-myeon-chuljangmassage/"),
        ("고삼면", "/anseong/gosam-myeon-chuljangmassage/"),
        ("안성동", "/anseong/anseong-dong-chuljangmassage/"),
    ]),
    ("생활권·교통거점별 안내", "/#landmarks", [
        ("안성터미널", "/anseong/anseong-terminal-chuljangmassage/"),
        ("공도 생활권", "/anseong/gongdo-area-chuljangmassage/"),
        ("아양지구", "/anseong/ayang-area-chuljangmassage/"),
        ("석정동 생활권", "/anseong/seokjeong-dong-area-chuljangmassage/"),
        ("중앙대 안성캠퍼스 인근", "/anseong/chungang-univ-area-chuljangmassage/"),
        ("한경국립대 인근", "/anseong/hankyong-univ-area-chuljangmassage/"),
        ("안성IC 인근", "/anseong/anseong-ic-chuljangmassage/"),
        ("서안성IC 인근", "/anseong/west-anseong-ic-chuljangmassage/"),
        ("일죽IC 인근", "/anseong/iljuk-ic-chuljangmassage/"),
    ]),
    ("예약 안내", "/reservation/", []),
    ("이용 전 확인사항", "/guide/", []),
    ("홈타이 이용 가이드", "/hometai/", []),
    ("고객센터", "/support/", []),
]
