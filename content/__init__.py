# 전체 페이지 목록 집계
# 구조: 메인 1 + 읍·면·대표 동 13 + 생활권·교통거점 9 + 안내 페이지 5 = 28
from . import main, areas, landmarks, info

PAGES = [main.PAGE] + areas.PAGES + landmarks.PAGES + info.PAGES
