# 페이지별 검색 썸네일(og:image) 생성기. 다크 럭스 골드 테마, 1200x630.
import os
from PIL import Image, ImageDraw, ImageFont

OUT = "assets/og"
os.makedirs(OUT, exist_ok=True)
W, H = 1200, 630
NAVY=(7,11,20); GOLD=(200,162,94); GOLD_SOFT=(233,215,171); TEXT=(234,237,244); DIM=(151,161,184)
KO="/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
SE="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
def ko(sz): return ImageFont.truetype(KO, sz)
def se(sz): return ImageFont.truetype(SE, sz)
PHONE="0508-202-4719"

# slug -> (tag, line1, line2)
PAGES = {
 # 읍·면·대표 동
 "gongdo-eup-chuljangmassage":        ("경기 · 안성", "공도읍 출장마사지", "공도 생활권 · 평택 인접 홈타이"),
 "bogae-myeon-chuljangmassage":       ("경기 · 안성", "보개면 출장마사지", "시내 인접 · 차량 방문 관리"),
 "geumgwang-myeon-chuljangmassage":   ("경기 · 안성", "금광면 출장마사지", "금광호수 인근 생활권 홈타이"),
 "seoun-myeon-chuljangmassage":       ("경기 · 안성", "서운면 출장마사지", "산업·주거권 차량 방문 안내"),
 "miyang-myeon-chuljangmassage":      ("경기 · 안성", "미양면 출장마사지", "안성천 평야권 차량 이동"),
 "daedeok-myeon-chuljangmassage":     ("경기 · 안성", "대덕면 출장마사지", "중앙대 안성캠퍼스 인근"),
 "yangseong-myeon-chuljangmassage":   ("경기 · 안성", "양성면 출장마사지", "용인·평택 인접 생활권"),
 "wongok-myeon-chuljangmassage":      ("경기 · 안성", "원곡면 출장마사지", "서안성IC · 평택 인접권"),
 "iljuk-myeon-chuljangmassage":       ("경기 · 안성", "일죽면 출장마사지", "일죽IC 생활권 방문 안내"),
 "juksan-myeon-chuljangmassage":      ("경기 · 안성", "죽산면 출장마사지", "죽산터미널 외곽 생활권"),
 "samjuk-myeon-chuljangmassage":      ("경기 · 안성", "삼죽면 출장마사지", "38번 국도 생활권 방문"),
 "gosam-myeon-chuljangmassage":       ("경기 · 안성", "고삼면 출장마사지", "고삼호수 인근 생활권"),
 "anseong-dong-chuljangmassage":      ("경기 · 안성", "안성동 출장마사지", "안성터미널 · 아양지구 홈타이"),
 # 생활권·교통거점
 "anseong-terminal-chuljangmassage":  ("경기 · 안성", "안성터미널 출장마사지", "안성동 중심 생활권 안내"),
 "gongdo-area-chuljangmassage":       ("경기 · 안성", "공도 생활권 출장마사지", "공도읍 주거·상업권 안내"),
 "ayang-area-chuljangmassage":        ("경기 · 안성", "아양지구 출장마사지", "안성 신도심 홈타이 안내"),
 "seokjeong-dong-area-chuljangmassage":("경기 · 안성", "석정동 생활권 출장마사지", "안성 중심 상권 방문 안내"),
 "chungang-univ-area-chuljangmassage":("경기 · 안성", "중앙대 인근 출장마사지", "대덕면 대학가 생활권"),
 "hankyong-univ-area-chuljangmassage":("경기 · 안성", "한경국립대 인근 출장마사지", "안성동·석정 생활권"),
 "anseong-ic-chuljangmassage":        ("경기 · 안성", "안성IC 인근 출장마사지", "차량 이동 기준 홈타이"),
 "west-anseong-ic-chuljangmassage":   ("경기 · 안성", "서안성IC 인근 출장마사지", "공도·원곡 인접권 안내"),
 "iljuk-ic-chuljangmassage":          ("경기 · 안성", "일죽IC 인근 출장마사지", "일죽·죽산 생활권 안내"),
 # 안내 페이지
 "reservation": ("간다GO · 안성", "예약 안내", "방문 절차 · 이동비 · 결제 기준"),
 "guide":       ("간다GO · 안성", "이용 전 확인사항", "준비물 · 위생 · 안전 기준"),
 "hometai":     ("간다GO · 안성", "홈타이 이용 가이드", "진행 방식 · 추천 대상 안내"),
 "support":     ("간다GO · 안성", "고객센터", "공지 · 자주 묻는 질문 · 문의"),
}

def fit(draw, text, font_factory, max_w, start, min_sz=44):
    sz=start
    while sz>min_sz:
        f=font_factory(sz); bb=draw.textbbox((0,0),text,font=f)
        if bb[2]-bb[0]<=max_w: return f
        sz-=4
    return font_factory(min_sz)

def ctext(d,cx,y,text,font,fill):
    bb=d.textbbox((0,0),text,font=font); w=bb[2]-bb[0]
    d.text((cx-w/2-bb[0], y), text, font=font, fill=fill)

def make(slug, tag, l1, l2):
    img=Image.new("RGB",(W,H),NAVY); d=ImageDraw.Draw(img,"RGBA")
    # top gold glow
    for i,r in enumerate(range(540,0,-44)):
        a=int(11*(1-i/13))
        if a>0: d.ellipse([600-r,-300-r//3,600+r,-300+r],fill=(200,162,94,a))
    # frame
    d.rectangle([24,24,W-25,H-25],outline=GOLD,width=3)
    d.rectangle([34,34,W-35,H-35],outline=(200,162,94,90),width=1)
    # tag pill (outline)
    tf=ko(30); bb=d.textbbox((0,0),tag,font=tf); tw=bb[2]-bb[0]
    px0=600-tw/2-26; px1=600+tw/2+26; py0=70; py1=70+54
    d.rounded_rectangle([px0,py0,px1,py1],radius=27,outline=GOLD,width=2)
    d.text((600-tw/2-bb[0], py0+(54-(bb[3]-bb[1]))/2-bb[1]), tag, font=tf, fill=GOLD_SOFT)
    # line1 (auto-fit), line2
    f1=fit(d,l1,ko,1000,96); ctext(d,600,196,l1,f1,GOLD_SOFT)
    f2=fit(d,l2,ko,1000,52); ctext(d,600,322,l2,f2,TEXT)
    # divider
    d.line([520,406,680,406],fill=GOLD,width=3)
    # brand row: G ring + 간다GO
    cx,cy,R=600,468,40
    # measure brand text to center the (mark + gap + text) group
    bf=ko(46); tb=d.textbbox((0,0),"간다GO",font=bf); btw=tb[2]-tb[0]
    gap=18; total=R*2+gap+btw; gx=600-total/2+R  # mark center x
    d.ellipse([gx-R,cy-R,gx+R,cy+R],fill=(10,17,32,255))
    d.ellipse([gx-R+3,cy-R+3,gx+R-3,cy+R-3],outline=GOLD,width=4)
    gf=se(50); gbb=d.textbbox((0,0),"G",font=gf)
    d.text((gx-(gbb[2]-gbb[0])/2-gbb[0], cy-(gbb[3]-gbb[1])/2-gbb[1]),"G",font=gf,fill=GOLD_SOFT)
    d.text((gx+R+gap, cy-(tb[3]-tb[1])/2-tb[1]),"간다GO",font=bf,fill=TEXT)
    # phone pill
    pt=f"예약전화  {PHONE}"; pf=ko(38); pb=d.textbbox((0,0),pt,font=pf); ptw=pb[2]-pb[0]
    qx0=600-ptw/2-34; qx1=600+ptw/2+34; qy0=536; qy1=536+62
    d.rounded_rectangle([qx0,qy0,qx1,qy1],radius=31,fill=GOLD)
    d.text((600-ptw/2-pb[0], qy0+(62-(pb[3]-pb[1]))/2-pb[1]), pt, font=pf, fill=(18,14,6))
    img.save(f"{OUT}/{slug}.png")
    return f"{OUT}/{slug}.png"

def make_main():
    """메인 대표 이미지 assets/og-image.png — G 링 + 간다GO + 안성 출장마사지·홈타이."""
    img=Image.new("RGB",(W,H),NAVY); d=ImageDraw.Draw(img,"RGBA")
    for i,r in enumerate(range(540,0,-44)):
        a=int(11*(1-i/13))
        if a>0: d.ellipse([600-r,-300-r//3,600+r,-300+r],fill=(200,162,94,a))
    d.rectangle([24,24,W-25,H-25],outline=GOLD,width=3)
    d.rectangle([34,34,W-35,H-35],outline=(200,162,94,90),width=1)
    # G ring (top center)
    cx,cy,R=600,180,72
    d.ellipse([cx-R,cy-R,cx+R,cy+R],fill=(10,17,32,255))
    d.ellipse([cx-R+5,cy-R+5,cx+R-5,cy+R-5],outline=GOLD,width=6)
    gf=se(86); gbb=d.textbbox((0,0),"G",font=gf)
    d.text((cx-(gbb[2]-gbb[0])/2-gbb[0], cy-(gbb[3]-gbb[1])/2-gbb[1]),"G",font=gf,fill=GOLD_SOFT)
    # brand
    bf=ko(66); ctext(d,600,300,"간다GO",bf,TEXT)
    # main line
    f1=fit(d,"안성 출장마사지 · 홈타이",ko,1040,72); ctext(d,600,392,"안성 출장마사지 · 홈타이",f1,GOLD_SOFT)
    # subtitle
    sf=ko(34); ctext(d,600,478,"경기도 안성시 전지역 방문 관리",sf,DIM)
    # phone pill
    pt=f"예약전화  {PHONE}"; pf=ko(38); pb=d.textbbox((0,0),pt,font=pf); ptw=pb[2]-pb[0]
    qx0=600-ptw/2-34; qx1=600+ptw/2+34; qy0=534; qy1=534+62
    d.rounded_rectangle([qx0,qy0,qx1,qy1],radius=31,fill=GOLD)
    d.text((600-ptw/2-pb[0], qy0+(62-(pb[3]-pb[1]))/2-pb[1]), pt, font=pf, fill=(18,14,6))
    img.save("assets/og-image.png")
    return "assets/og-image.png"


for slug,(tag,l1,l2) in PAGES.items():
    print("wrote", make(slug,tag,l1,l2))
print("wrote", make_main())
print("done", len(PAGES)+1)
