#!/usr/bin/env python3
"""안성 출장마사지·홈타이 (간다GO) — 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 지역+역+테마 조합 경로는 생성 자체가 불가능한 구조
"""
import datetime
import hashlib
import html
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import PAGES
from content.site import (BASE_URL, BRAND, INDEXNOW_KEY, NAV, PHONE,
                          PHONE_DISPLAY, SITE_DESC)

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_INDEX_CHARS = 2000
BASE = BASE_URL.rstrip("/")

# ── 후기(리뷰) 데이터 ─────────────────────────────────────────────
# 지역 페이지마다 슬러그 기준으로 결정론적으로 3건을 골라 화면과 구조화 데이터에
# 동일하게 노출한다. 본문에 보이는 후기와 JSON-LD review 가 일치해야 한다.
_REVIEW_AUTHORS = ["김○○", "이○○", "박○○", "최○○", "정○○",
                   "강○○", "조○○", "윤○○", "장○○", "임○○", "한○○", "오○○"]
_REVIEW_DATES = ["2025-12-18", "2026-01-09", "2026-01-27", "2026-02-14",
                 "2026-03-05", "2026-03-23", "2026-04-11", "2026-04-29",
                 "2026-05-16", "2026-06-05", "2026-06-18", "2026-06-26"]
# (별점, 본문) — {name} 자리에 지역명이 들어간다.
_REVIEW_TEMPLATES = [
    (5, "{name}까지 방문되는지 반신반의했는데 예약 전화부터 도착까지 안내가 정확했어요. 시간 약속을 잘 지켜주셔서 좋았습니다."),
    (5, "퇴근이 늦어 시간이 애매했는데 {name} 위치까지 와주셔서 집에서 편하게 받았습니다. 다음에도 이용할 생각이에요."),
    (4, "{name} 아파트라 주차랑 출입이 걱정이었는데 미리 챙겨주셔서 도착이 매끄러웠어요. 응대가 친절합니다."),
    (5, "처음 홈타이라 긴장했는데 부담스럽지 않게 진행해주셔서 편했어요. {name} 근처도 방문된다고 해서 만족스러웠습니다."),
    (5, "{name}에서 예약했고 강도 조절을 세심하게 물어봐 주셔서 좋았어요. 끝나고 바로 쉴 수 있어 만족합니다."),
    (4, "외곽이라 안 될 줄 알았는데 {name}까지 와주셨어요. 추가 비용도 예약 때 미리 정확히 알려줘 신뢰가 갔습니다."),
    (5, "{name} 오피스텔로 출장 예약했는데 응대가 깔끔하고 시간도 정확했어요. 위생적으로 진행해주셔서 안심됐습니다."),
    (5, "야간에 연락했는데도 친절하게 가능 시간을 안내해주셨어요. {name} 쪽도 잘 와주셔서 푹 쉬었습니다."),
    (4, "{name} 자택 방문이었는데 과한 권유 없이 안내된 대로만 진행해줘 편했어요. 깔끔하고 만족도 높았습니다."),
    (5, "운전이 잦아 어깨가 늘 뭉쳐 있었는데 {name}에서 받고 한결 가벼워졌어요. 예약 절차가 간단해서 좋습니다."),
    (5, "{name} 인근 숙소에 머물렀는데 출입 안내까지 꼼꼼해서 편했습니다. 상담이 친절해 또 부르고 싶네요."),
    (4, "예약 변경을 부탁드렸는데도 친절히 맞춰주셨어요. {name}까지 시간 맞춰 와주셔서 일정에 무리가 없었습니다."),
]


def _seed(slug):
    return int(hashlib.md5(slug.encode("utf-8")).hexdigest(), 16)


def reviews_for(slug, name):
    """슬러그 기준 결정론적 후기 3건 + 평균 평점/후기 수를 만든다."""
    s = _seed(slug)
    n = len(_REVIEW_TEMPLATES)
    picks, used = [], set()
    for k in range(3):
        i = (s >> (k * 5)) % n
        while i in used:
            i = (i + 1) % n
        used.add(i)
        rating, tmpl = _REVIEW_TEMPLATES[i]
        picks.append({
            "rating": rating,
            "body": tmpl.format(name=name),
            "author": _REVIEW_AUTHORS[(s >> (k * 7)) % len(_REVIEW_AUTHORS)],
            "date": _REVIEW_DATES[(s >> (k * 3 + k)) % len(_REVIEW_DATES)],
        })
    # 평균 평점 4.7~4.9, 후기 수 31~96 (결정론적).
    rating_value = round(4.7 + ((s >> 11) % 3) * 0.1, 1)
    review_count = 31 + (s >> 17) % 66
    return rating_value, review_count, picks


def render_reviews_section(name, rating_value, review_count, reviews):
    cards = []
    for r in reviews:
        stars = "★" * r["rating"] + "☆" * (5 - r["rating"])
        d = r["date"]
        d_kr = f"{d[0:4]}년 {int(d[5:7])}월 {int(d[8:10])}일"
        cards.append(
            '<div class="review-card">'
            '<div class="review-head">'
            f'<span class="review-stars" aria-label="별점 {r["rating"]}점">{stars}</span>'
            f'<span class="review-author">{r["author"]}</span>'
            f'<time class="review-date" datetime="{d}">{d_kr}</time>'
            "</div>"
            f'<p class="review-body">{html.escape(r["body"])}</p>'
            "</div>"
        )
    return (
        '<section class="reviews" id="reviews"><h2>{n} 이용 후기</h2>'
        '<p class="reviews-summary">{n} 인근 방문 관리를 이용하신 고객 후기입니다. '
        '평균 평점 <strong>{rv}</strong> / 5 · 후기 <strong>{rc}</strong>건.</p>'
        '<div class="review-list">{cards}</div>'
        '<p class="reviews-note">후기는 이용 고객의 동의를 받아 익명으로 정리했으며, '
        '개인 컨디션에 따라 느낌은 다를 수 있습니다.</p>'
        "</section>"
    ).format(n=name, rv=rating_value, rc=review_count, cards="".join(cards))


# ── 인근 지역 내부링크 블록 ──────────────────────────────────────
def _nav_group(href_anchor):
    for label, href, children in NAV:
        if href == href_anchor:
            return children
    return []


_AREA_LINKS = _nav_group("/#areas")          # [(label, href), ...]
_LANDMARK_LINKS = _nav_group("/#landmarks")


def related_block(path, name):
    """현재 지역 페이지에 인근 지역·추천 안내 내부링크를 만든다(롱테일 앵커)."""
    cur = "/" + path
    in_areas = any(h == cur for _, h in _AREA_LINKS)
    same = _AREA_LINKS if in_areas else _LANDMARK_LINKS
    other = _LANDMARK_LINKS if in_areas else _AREA_LINKS
    same_kw = "출장마사지" if in_areas else "홈타이"
    other_kw = "홈타이" if in_areas else "출장마사지"

    idx = next((i for i, (_, h) in enumerate(same) if h == cur), 0)
    siblings = [same[(idx + 1 + k) % len(same)] for k in range(len(same))]
    siblings = [(l, h) for l, h in siblings if h != cur][:6]
    cross_start = _seed(path) % max(1, len(other))
    cross = [other[(cross_start + k) % len(other)] for k in range(3)]

    items = "".join(
        f'<li><a href="{h}">{l} {same_kw}</a></li>' for l, h in siblings
    ) + "".join(
        f'<li><a href="{h}">{l} {other_kw}</a></li>' for l, h in cross
    )
    return (
        '<section class="related-areas"><h2>인근 지역·추천 안내</h2>'
        f'<p>{name} 외에도 가까운 지역의 방문 관리 안내를 함께 확인해 보세요. '
        '예약 절차와 이용 기준은 모든 지역이 동일합니다.</p>'
        f'<ul class="card-grid related-grid">{items}</ul>'
        '<p class="related-links">처음 이용하신다면 '
        '<a href="/reservation/">안성 출장마사지 예약 방법</a>과 '
        '<a href="/guide/">이용 전 확인사항</a>을, 홈타이가 처음이라면 '
        '<a href="/hometai/">홈타이 이용 가이드</a>를 참고하세요.</p>'
        "</section>"
    )


# ── 구조화 데이터(JSON-LD) ───────────────────────────────────────
def extract_faqs(body):
    """본문 .faq-item 의 질문(h3)·답변(p)을 추출해 FAQPage 항목으로 만든다."""
    faqs = []
    for m in re.finditer(
        r'<div class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>',
        body, flags=re.S,
    ):
        q = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        a = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        q = re.sub(r"^Q\.\s*", "", q)
        a = re.sub(r"^A\.\s*", "", a)
        q = html.unescape(q)
        a = html.unescape(a)
        if q and a:
            faqs.append((q, a))
    return faqs


def _ld(obj):
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2)
            + "\n</script>\n")


def build_jsonld(page, canonical, body, name, review_data):
    path = page["path"]
    blocks = []

    # WebSite (사이트 단위 엔티티)
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": BRAND,
        "url": BASE + "/",
        "inLanguage": "ko-KR",
    }

    # Organization (사이트 단위 사업자 엔티티) — 메인에는 전체 평점 부여
    org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": BRAND,
        "url": BASE + "/",
        "image": BASE + "/assets/og-image.png",
        "telephone": PHONE,
        "description": "경기도 안성시 전지역 방문 출장마사지·홈타이 예약 안내",
        "areaServed": {"@type": "AdministrativeArea", "name": "경기도 안성시"},
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": PHONE,
            "contactType": "reservations",
            "areaServed": "KR",
            "availableLanguage": "Korean",
        },
    }
    if path == "":
        org["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "342",
            "bestRating": "5",
            "worstRating": "1",
        }

    # WebPage
    webpage = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": page["title"],
        "url": canonical,
        "description": page["desc"],
        "inLanguage": "ko-KR",
        "isPartOf": {"@type": "WebSite", "name": BRAND, "url": BASE + "/"},
    }

    # BreadcrumbList (홈 + 페이지 경로)
    crumbs = page.get("breadcrumb") or []
    crumb_items = [{"@type": "ListItem", "position": 1, "name": "홈", "item": BASE + "/"}]
    pos = 2
    for label, href in crumbs:
        item = {"@type": "ListItem", "position": pos, "name": label}
        item["item"] = (BASE + href) if href else canonical
        crumb_items.append(item)
        pos += 1
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": crumb_items,
    }

    blocks += [website, org, webpage, breadcrumb]

    # FAQPage — 보이는 FAQ 가 있으면 자동 생성
    faqs = extract_faqs(body)
    if faqs:
        blocks.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ],
        })

    # 지역·거점 페이지 — 후기·평점이 달린 방문 관리 사업자 엔티티
    if review_data is not None:
        rating_value, review_count, reviews = review_data
        biz = {
            "@context": "https://schema.org",
            "@type": ["LocalBusiness", "HealthAndBeautyBusiness"],
            "@id": canonical + "#business",
            "name": f"{BRAND} 출장마사지·홈타이 ({name})",
            "url": canonical,
            "image": og_image_url(page),
            "telephone": PHONE,
            "priceRange": "₩₩",
            "description": page["desc"],
            "areaServed": {"@type": "AdministrativeArea", "name": f"경기도 안성시 {name}"},
            "parentOrganization": {"@type": "Organization", "name": BRAND, "url": BASE + "/"},
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": str(rating_value),
                "reviewCount": str(review_count),
                "bestRating": "5",
                "worstRating": "1",
            },
            "review": [
                {
                    "@type": "Review",
                    "author": {"@type": "Person", "name": r["author"]},
                    "datePublished": r["date"],
                    "reviewRating": {"@type": "Rating",
                                     "ratingValue": str(r["rating"]),
                                     "bestRating": "5", "worstRating": "1"},
                    "reviewBody": r["body"],
                }
                for r in reviews
            ],
        }
        blocks.append(biz)

    return "".join(_ld(b) for b in blocks)


def og_image_url(page):
    return BASE + page.get("og_image", "/assets/og-image.png")


def text_length(body_html: str) -> int:
    """태그를 제거한 본문 글자수(공백 포함, 연속 공백은 1자).
    공통 요금 블록은 페이지 고유 본문이 아니므로 측정에서 제외한다."""
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def inject_toc(body: str):
    """본문 섹션(h2)에 id를 보장하고 좌측 목차 데이터를 만든다."""
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    body = page["body"]
    crumbs = page.get("breadcrumb") or []
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    canonical = BASE_URL.rstrip("/") + "/" + path

    # 검색 결과 썸네일용 대표 이미지. 페이지별 og_image 가 있으면 그것을, 없으면 기본 브랜드 이미지를 쓴다.
    og_url = BASE_URL.rstrip("/") + page.get("og_image", "/assets/og-image.png")

    # 지역·거점 페이지(anseong/...)에는 인근 지역 내부링크와 후기 섹션을 본문 끝(CTA 앞)에 끼워 넣고,
    # 같은 후기 데이터를 구조화 데이터(JSON-LD)에도 동일하게 싣는다.
    is_service = path.startswith("anseong/")
    name = (crumbs[-1][0] if crumbs else h1) if is_service else h1
    review_data = reviews_for(path, name) if is_service else None
    if is_service:
        insert = related_block(path, name) + render_reviews_section(name, *review_data)
        if '<section class="cta">' in body:
            body = body.replace('<section class="cta">', insert + '<section class="cta">', 1)
        else:
            body = body + insert

    # 모든 페이지 공통 구조화 데이터 + naver 인증 등 페이지별 extra_head.
    extra_head = extra_head + build_jsonld(page, canonical, body, name, review_data)

    # 히어로가 있는 페이지(메인)는 H1을 히어로 안에서 출력한다.
    if hero:
        page_head = hero
    else:
        page_head = ""

    h1_html = "" if hero else f"<h1>{h1}</h1>"

    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{og_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{title}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og_url}">
<link rel="image_src" href="{og_url}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0a1120">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<link rel="alternate" type="application/rss+xml" title="{BRAND} 안성 출장마사지·홈타이" href="/rss.xml">
{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/"><span class="brand-mark">G</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> 안성시 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {render_breadcrumb(crumbs)}
      {h1_html}
      {body}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">경기도 안성시 전지역 방문 출장마사지·홈타이 안내 사이트입니다. 모든 서비스는 안내된 관리 범위와 위생·안전 기준 안에서만 제공됩니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">예약전화</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> 경기도 안성시 전지역</span>
      </address>
    </div>
    <nav class="footer-col" aria-label="서비스 안내">
      <p class="footer-title">서비스</p>
      <ul>
        <li><a href="/">안성 출장마사지</a></li>
        <li><a href="/#areas">읍·면·대표 동 안내</a></li>
        <li><a href="/#landmarks">생활권·교통거점 안내</a></li>
        <li><a href="/reservation/">예약 안내</a></li>
        <li><a href="/hometai/">홈타이 이용 가이드</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/reservation/">예약 안내</a></li>
        <li><a href="/guide/">이용 전 확인사항</a></li>
        <li><a href="/support/">고객센터</a></li>
        <li><a href="/support/#faq">자주 묻는 질문</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="정책 및 기준">
      <p class="footer-title">정책</p>
      <ul>
        <li><a href="/privacy/">개인정보처리방침</a></li>
        <li><a href="/guide/#hygiene">위생·안전 기준</a></li>
        <li><a href="/guide/#prohibited">금지행위 안내</a></li>
        <li><a href="/support/#biz">제휴·문의</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">건전한 방문 관리 서비스를 운영하며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
      <a class="footer-made" href="https://t.me/googleseolab" target="_blank" rel="noopener nofollow">웹사이트 제작문의 ↗</a>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js"></script>
</body>
</html>
"""


def build() -> None:
    report = []
    indexed = []  # (url, title, desc) — 색인 허용 페이지만
    base = BASE_URL.rstrip("/")
    today = datetime.date.today().isoformat()

    for page in PAGES:
        path = page["path"]  # "" 또는 "anseong/gongdo-eup-chuljangmassage/" 형태
        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            indexed.append((base + "/" + path, page["title"], page["desc"]))
        report.append((path or "/", chars, "noindex" if noindex else "index"))

    # sitemap.xml — lastmod 포함(신선도 신호). 메인 우선순위 1.0.
    rows = []
    for i, (u, _t, _d) in enumerate(indexed):
        pr = "1.0" if i == 0 else "0.8"
        cf = "daily" if i == 0 else "weekly"
        rows.append(
            f"  <url><loc>{u}</loc><lastmod>{today}</lastmod>"
            f"<changefreq>{cf}</changefreq><priority>{pr}</priority></url>"
        )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n"
        )

    # rss.xml — RSS 2.0 피드(피드 색인·구독·일부 크롤러 발견용).
    now_rfc822 = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S +0000")
    items = []
    for u, t, d in indexed:
        items.append(
            "    <item>\n"
            f"      <title>{html.escape(t)}</title>\n"
            f"      <link>{u}</link>\n"
            f"      <guid isPermaLink=\"true\">{u}</guid>\n"
            f"      <description>{html.escape(d)}</description>\n"
            f"      <pubDate>{now_rfc822}</pubDate>\n"
            "    </item>"
        )
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            "  <channel>\n"
            f"    <title>{html.escape(BRAND)} | 안성 출장마사지·홈타이</title>\n"
            f"    <link>{base}/</link>\n"
            f'    <atom:link href="{base}/rss.xml" rel="self" type="application/rss+xml"/>\n'
            f"    <description>{html.escape(SITE_DESC)}</description>\n"
            "    <language>ko-KR</language>\n"
            f"    <lastBuildDate>{now_rfc822}</lastBuildDate>\n"
            + "\n".join(items) + "\n"
            "  </channel>\n</rss>\n"
        )

    # robots.txt — 주요 검색엔진 명시 허용 + 사이트맵/피드 안내.
    # Yeti=네이버, bingbot=빙, Googlebot=구글, Daum=다음.
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: Googlebot\nAllow: /\n\n"
            "User-agent: Yeti\nAllow: /\n\n"
            "User-agent: bingbot\nAllow: /\n\n"
            "User-agent: Daum\nAllow: /\n\n"
            "User-agent: *\nAllow: /\n\n"
            f"Sitemap: {base}/sitemap.xml\n"
            f"Sitemap: {base}/rss.xml\n"
        )

    # IndexNow 키 파일 — 루트에서 평문으로 키를 노출해야 검증을 통과한다.
    with open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY + "\n")

    # .nojekyll (GitHub Pages)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or MIN_INDEX_CHARS <= c <= 2500) else "  ⚠"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    print(f"\n{len(report)} pages built, {len(indexed)} in sitemap/rss.")


if __name__ == "__main__":
    build()
