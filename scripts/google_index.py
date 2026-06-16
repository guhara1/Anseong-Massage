#!/usr/bin/env python3
"""구글 Indexing API 색인 통보 — 구글은 IndexNow에 참여하지 않으므로 별도로 알린다.
URL_UPDATED / URL_DELETED 알림을 보낸다.

준비(1회)
  1) Google Cloud 콘솔에서 프로젝트 생성 → "Indexing API" 사용 설정.
  2) 서비스 계정 생성 → JSON 키 발급.
  3) Search Console에서 해당 사이트(도메인) 속성에 그 서비스 계정 이메일을
     '소유자(Owner)'로 추가.
  4) pip install google-auth

사용법
  export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
  python3 scripts/google_index.py                 # sitemap.xml의 모든 URL 통보
  python3 scripts/google_index.py URL [URL ...]   # 지정 URL만
  python3 scripts/google_index.py --delete URL    # URL_DELETED 통보
  python3 scripts/google_index.py --dry-run

주의: 일일 쿼터(기본 200건/일)가 있다. 대량 최초 색인은 Search Console
사이트맵 제출이 정석이고, 본 API는 새 글/수정 건의 빠른 통보에 쓰는 것이 좋다.
"""
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def sitemap_urls():
    with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as f:
        return re.findall(r"<loc>(.*?)</loc>", f.read())


def get_token():
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred_path or not os.path.exists(cred_path):
        sys.exit("GOOGLE_APPLICATION_CREDENTIALS 환경변수에 서비스 계정 JSON 경로를 지정하세요.")
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request
    except ImportError:
        sys.exit("google-auth 패키지가 필요합니다:  pip install google-auth")
    creds = service_account.Credentials.from_service_account_file(
        cred_path, scopes=SCOPES)
    creds.refresh(Request())
    return creds.token


def submit(urls, kind="URL_UPDATED", dry_run=False):
    urls = [u for u in urls if u.startswith("http")]
    if not urls:
        print("제출할 URL이 없습니다."); return 1
    print(f"Google Indexing API → {kind}  ({len(urls)}건)")
    for u in urls:
        print("  -", u)
    if dry_run:
        print("\n[--dry-run] 전송하지 않음."); return 0
    token = get_token()
    ok = 0
    for u in urls:
        body = json.dumps({"url": u, "type": kind}).encode("utf-8")
        req = urllib.request.Request(
            ENDPOINT, data=body, method="POST",
            headers={"Authorization": f"Bearer {token}",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status == 200:
                    ok += 1
                    print(f"  ✓ {u}")
        except urllib.error.HTTPError as e:
            print(f"  ✗ {u} — HTTP {e.code}: {e.read().decode('utf-8','ignore')[:200]}")
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ {u} — {e}")
    print(f"\n성공 {ok}/{len(urls)}")
    return 0 if ok == len(urls) else 2


def main():
    argv = sys.argv[1:]
    kind = "URL_DELETED" if "--delete" in argv else "URL_UPDATED"
    dry = "--dry-run" in argv
    urls = [a for a in argv if not a.startswith("--")]
    if not urls:
        urls = sitemap_urls()
    raise SystemExit(submit(urls, kind=kind, dry_run=dry))


if __name__ == "__main__":
    main()
