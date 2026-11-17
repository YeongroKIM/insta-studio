# 펜 한 줄 인테리어 — 실사 이미지 프롬프트 팩

> 이미지 생성 모델(힉스필드 등)에 그대로 붙여넣는다. **영어 프롬프트가 품질이 더 안정적**이다.
> 설정: 비율 **9:16**, 최고 품질, 한 번에 **4장** 뽑아 가장 좋은 것 선택.

## 검증된 설정 (2026-11-17, #01 니치 제작)
- 모델 `gpt_image_2_6` · quality `high` · resolution `2k` · 9:16 → 1520×2688, **장당 2.75 크레딧** (Before + After = 5.5)
- After는 Before의 job_id를 `image_references`로 넣고 편집 → 구도 유지 성공 (붙박이장 분할만 약간 달라짐 — 전환에서 자연스러움)
- 합성 `area` 값: 니치 영역 `[0.19, 0.46, 0.44, 0.11]`

## 크레딧 기준표 (2026-11-17 실측)
| 품질 | 장당 | 요청형 1편(2장) | 빈집 채우기 1편(6장) | 비고 |
|---|---|---|---|---|
| medium 2k | 1 | 2 | 6 | #02·#03 제작. 폰 화면에선 충분 |
| high 2k | 2.75 | 5.5 | 16.5 | #01 제작. 디테일·질감 더 좋음 |
- 매일 1편 기준(30일): medium 약 60 / high 약 165 + 다시 뽑기 여유 30%

## 공통 원칙
1. **Before는 "생성", After는 Before를 넣고 "편집"**. After를 새로 생성하면 구도가 달라져 전환이 어색해진다
2. 편집 지시는 항상 "나머지는 그대로(keep everything else identical)" + 바꿀 것 하나만
3. 버릴 것: 휜 직선, 떠 있는 물건, 이상한 글자·로고, 사람, 창밖 고층 단지 풍경
4. 고른 2장을 겹쳐 깜빡여 봤을 때 벽·바닥·커튼 위치가 같아야 합격

## 공통 꼬리말 (모든 Before 프롬프트 끝에)
```
architectural interior photography, photorealistic, editorial magazine style, eye-level, wide 24mm lens,
3/4 view, soft natural daylight through sheer white curtains, warm neutral palette (warm white, beige, light oak),
clean and minimal, no people, no text, no logos, straight vertical lines, high detail, 9:16
```

---

## 01. 안방 붙박이장 → 니치 + 간접조명
**Before (생성)**
```
A bedroom in a newly built Korean apartment. A full-height wall of plain flat white built-in wardrobe doors
(eight tall panels, handleless, thin vertical gaps), light oak laminate floor, low beige rug, a curved boucle
armchair at the right edge, sheer curtains on the right. Ceiling height about 2.3m, simple flat ceiling.
+ 공통 꼬리말
```
**After (편집, Before 이미지를 입력으로)**
```
Keep everything else identical — same camera, composition, lighting, floor, rug, curtains and chair.
Only change: carve a wide horizontal open niche into the middle of the wardrobe wall at waist-to-chest height,
spanning four panels, with a warm-white LED strip hidden along the top edge, a light travertine back panel,
and a few minimal objects (a black ceramic vase, a cream sculptural object, two stacked books).
```

## 02. 붙박이장 끝 모서리 → 아치형 오픈 수납
**Before (생성)**
```
A bedroom corner in a Korean apartment: plain white handleless built-in wardrobe ending at the left wall,
a bed with beige linen bedding on the right, a walnut-veneer floating bedside shelf, a round glass table lamp.
Recessed ceiling cove with warm indirect light.
+ 공통 꼬리말
```
**After (편집)**
```
Keep everything else identical. Only change: replace the leftmost wardrobe section with a built-in open
display unit with a rounded arch top, walnut wood interior, one floating shelf with a warm LED strip underneath,
and a curved low walnut cabinet at the bottom holding a ceramic vase and a framed checkered wood art piece.
```

## 03. 거실 타일 아트월 → 우드 루버 월
**Before (생성)**
```
A living room in a Korean apartment with a typical glossy beige porcelain-tile TV feature wall, a low white
TV console, light oak floor, a light grey fabric sofa in the foreground, sheer curtains on the right.
+ 공통 꼬리말
```
**After (편집)**
```
Keep everything else identical. Only change: replace the tile feature wall with a floor-to-ceiling vertical
oak wood slat (louver) wall with thin black gaps, a slim floating walnut TV console, and a soft warm LED line
at the floor edge behind the console.
```

---

## 고른 뒤
1. Before·After 2장을 `tools/sketch-reel/work/<주제>/`에 저장 (저장소에 커밋되지 않음)
2. config에 `area`(바뀐 영역 비율)·자막·정보 카드 작성 → `python3 tools/sketch-reel/make_reel.py <config>`
3. 정보 카드 문구는 `knowledge/domains/10-interior.md` 근거로
