#!/usr/bin/env python3
"""IndexNow 즉시 색인 통보 — 빙(bingbot)·네이버(Yeti) 등 IndexNow 참여 검색엔진에
URL 변경을 즉시 알린다. 글을 올리거나 수정한 뒤 실행하면 된다.

사전 조건
  - 루트에 {INDEXNOW_KEY}.txt 키 파일이 실제 도메인에 배포되어 있어야 한다(build.py가 생성).
  - 사이트가 BASE_URL 도메인에 실제로 떠 있어야 검증을 통과한다.

사용법
  python3 scripts/indexnow.py                 # sitemap.xml의 모든 색인 URL 제출
  python3 scripts/indexnow.py URL [URL ...]   # 지정한 URL만 제출(글 1건 올렸을 때)
  python3 scripts/indexnow.py --dry-run       # 전송 없이 페이로드만 출력

참고: IndexNow는 한 엔드포인트에 보내면 참여 검색엔진 전체에 공유된다.
구글은 IndexNow 미참여 → scripts/google_index.py 또는 Search Console 사용.
"""
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL, INDEXNOW_KEY

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://api.indexnow.org/indexnow"
HOST = re.sub(r"^https?://", "", BASE_URL.rstrip("/")).split("/")[0]


def sitemap_urls():
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, encoding="utf-8") as f:
        return re.findall(r"<loc>(.*?)</loc>", f.read())


def submit(urls, dry_run=False):
    urls = [u for u in urls if u.startswith("http")]
    if not urls:
        print("제출할 URL이 없습니다."); return 1
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL.rstrip('/')}/{INDEXNOW_KEY}.txt",
        "urlList": urls,
    }
    body = json.dumps(payload).encode("utf-8")
    print(f"IndexNow → {ENDPOINT}")
    print(f"host={HOST}  urls={len(urls)}")
    for u in urls:
        print("  -", u)
    if dry_run:
        print("\n[--dry-run] 전송하지 않음. 페이로드:")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    req = urllib.request.Request(
        ENDPOINT, data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"\n응답 {resp.status} {resp.reason}")
            # 200/202 = 접수 성공. 빙·네이버 등에 공유됨.
            return 0 if resp.status in (200, 202) else 2
    except urllib.error.HTTPError as e:
        print(f"\nHTTP 오류 {e.code}: {e.read().decode('utf-8', 'ignore')}")
        return 2
    except Exception as e:  # noqa: BLE001
        print(f"\n전송 실패: {e}")
        return 2


def main():
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry = "--dry-run" in sys.argv
    urls = args if args else sitemap_urls()
    raise SystemExit(submit(urls, dry_run=dry))


if __name__ == "__main__":
    main()
