# 이렇게 요청하세요 — 1차 배치 (공간 6종)

> 상태: **준비 완료, 크레딧 대기** (필요 약 33 크레딧 = 6편 × 2장 × 2.75, high 2k). 근거: 지식 DB `knowledge/domains/10-interior.md`.
> 생성 → `tools/sketch-reel/work/<id>/before.png·after.png` 저장 → `python3 tools/sketch-reel/make_reel.py tools/sketch-reel/jobs/<id>.json`

공통: 모델 `gpt_image_2_6`, quality high, 2k, 9:16. Before는 생성, After는 Before job을 `image_references`로 넣고 편집.

## 02-kitchen · 주방
- 근거: 10-interior §3-3 #9·#10
**Before**
```
A kitchen in a newly built Korean apartment: a full row of plain white glossy upper cabinets above the counter from wall to wall, white lower cabinets, a simple stainless sink and faucet, white subway-tile backsplash, light oak floor, a small window on the side. Architectural interior photography, photorealistic, editorial magazine style, eye-level, wide 24mm lens, 3/4 view, soft natural daylight, warm neutral palette (warm white, beige, light oak), clean and minimal, no people, no text, no logos, straight vertical lines, high detail. Any window view shows only soft hazy sky and trees, no buildings.
```
**After (편집)**
```
Edit this photo. Keep everything else exactly identical — same camera angle, framing, perspective, lighting and all other objects. Only change: remove the two middle upper cabinets and replace them with two floating light-oak open shelves holding a few white bowls, cups and a small plant; add a warm-white LED line light under the remaining upper cabinets lighting the countertop.
```
**자막**: 이런 꽉 막힌 주방 상부장을 → 이렇게 바꾸려면?
**요청 체크리스트**
- 가운데 상부장 2칸을 떼고 오픈 선반 2줄로 바꿔주세요
- 남은 상부장 아래에 라인 조명을 넣어주세요
- 하부 조명 전원은 주방가구 설치 전에 준비해주세요
- 선반은 수전보다 충분히 높게 달아주세요
- ⚠️ 수납이 확 줄어요 → 그릇 많은 집은 신중하게!

## 03-living · 거실
- 근거: 10-interior §3-3 #3
**Before**
```
A living room in a newly built Korean apartment: a TV feature wall covered in glossy beige large porcelain tiles (typical Korean 'art wall'), a low white TV console with a TV, light oak floor, a light grey fabric sofa partly visible in the foreground, sheer curtains on the right. Architectural interior photography, photorealistic, editorial magazine style, eye-level, wide 24mm lens, 3/4 view, soft natural daylight, warm neutral palette (warm white, beige, light oak), clean and minimal, no people, no text, no logos, straight vertical lines, high detail. Any window view shows only soft hazy sky and trees, no buildings.
```
**After (편집)**
```
Edit this photo. Keep everything else exactly identical — same camera angle, framing, perspective, lighting and all other objects. Only change: replace the tile feature wall with a floor-to-ceiling vertical light-oak wood slat (louver) wall with thin dark gaps, mount the TV on it, and replace the console with a slim floating walnut TV console with a soft warm LED line underneath.
```
**자막**: 이런 흔한 타일 아트월을 → 이렇게 바꾸려면?
**요청 체크리스트**
- 타일 아트월을 철거하고 우드 루버(템바보드) 벽으로 해주세요
- TV 배선·콘센트 위치를 시공 전에 정해주세요
- TV장은 바닥에서 띄워서 달아주세요
- ⚠️ 기존 타일 철거비는 따로예요 → 견적에 포함됐는지 확인!

## 04-study · 서재
- 근거: 10-interior §3-3 #13
**Before**
```
An empty small bedroom in a newly built Korean apartment: plain white wallpaper on all walls, light oak floor, a window on the right wall with sheer curtain, flat white ceiling, completely empty room. Architectural interior photography, photorealistic, editorial magazine style, eye-level, wide 24mm lens, 3/4 view, soft natural daylight, warm neutral palette (warm white, beige, light oak), clean and minimal, no people, no text, no logos, straight vertical lines, high detail. Any window view shows only soft hazy sky and trees, no buildings.
```
**After (편집)**
```
Edit this photo. Keep everything else exactly identical — same camera angle, framing, perspective, lighting and all other objects. Only change: build a full-wall custom bookshelf on the back wall in light oak and warm white, floor to ceiling, with an integrated built-in desk top in the middle section, a slim desk lamp, some books and a few objects on the shelves, and a simple chair at the desk.
```
**자막**: 이런 텅 빈 작은방을 → 이렇게 서재로 만들려면?
**요청 체크리스트**
- 한쪽 벽 전체를 책장으로 짜고 가운데에 책상 상판을 붙여주세요
- 콘센트·랜선·스탠드 전원 위치를 제작 전에 정해주세요
- 책 무게를 버티게 선반 두께·간격을 맞춰주세요
- ⚠️ 전원 위치는 제작 후엔 못 바꿔요 → 먼저 정하기!

## 05-entrance · 현관
- 근거: 10-interior §3-3 #5
**Before**
```
The entrance hallway of a newly built Korean apartment seen from inside: a plain full-height white shoe cabinet standing on the floor along one wall, light grey porcelain tile floor at the entry step, white walls, the front door at the end. Architectural interior photography, photorealistic, editorial magazine style, eye-level, wide 24mm lens, 3/4 view, soft natural daylight, warm neutral palette (warm white, beige, light oak), clean and minimal, no people, no text, no logos, straight vertical lines, high detail. Any window view shows only soft hazy sky and trees, no buildings.
```
**After (편집)**
```
Edit this photo. Keep everything else exactly identical — same camera angle, framing, perspective, lighting and all other objects. Only change: make the shoe cabinet a floating wall-hung cabinet raised about 25cm above the floor, with a warm-white LED strip hidden underneath softly lighting the floor and a pair of shoes below.
```
**자막**: 이런 평범한 현관 신발장을 → 이렇게 바꾸려면?
**요청 체크리스트**
- 신발장을 바닥에서 띄워서 벽에 달아주세요
- 아래 빈 공간에 간접조명(센서등)을 넣어주세요
- 조명 전원·스위치 위치는 가구 제작 전에 정해주세요
- ⚠️ 벽에 매다는 구조 → 석고보드 벽이면 보강 필요!

## 06-bathroom · 화장실
- 근거: 10-interior §3-3 #11
**Before**
```
A bathroom in a newly built Korean apartment: a white wall-mounted vanity sink, a plain surface-mounted mirror cabinet with visible frame above it, light grey large-format wall tiles, a simple ceiling light. Architectural interior photography, photorealistic, editorial magazine style, eye-level, wide 24mm lens, 3/4 view, soft natural daylight, warm neutral palette (warm white, beige, light oak), clean and minimal, no people, no text, no logos, straight vertical lines, high detail. Any window view shows only soft hazy sky and trees, no buildings.
```
**After (편집)**
```
Edit this photo. Keep everything else exactly identical — same camera angle, framing, perspective, lighting and all other objects. Only change: replace the surface mirror cabinet with a flush recessed mirror cabinet built into the wall, with a soft warm LED glow around its edges and underneath, lighting the sink area.
```
**자막**: 이런 튀어나온 욕실 거울장을 → 이렇게 바꾸려면?
**요청 체크리스트**
- 세면대 위 거울장을 벽 안으로 매립해주세요
- 거울 테두리·아래에 간접조명을 넣어주세요
- 욕실이라 방습형 조명으로 해주세요
- ⚠️ 배관이 지나가는 벽이면 매립이 안 돼요 → 실측부터!

## 07-balcony · 베란다
- 근거: 10-interior §3-3 #14
**Before**
```
A non-extended balcony of a Korean apartment: white PVC sliding windows along the length, grey ceramic tile floor, plain white walls, an empty corner, bright daylight. Architectural interior photography, photorealistic, editorial magazine style, eye-level, wide 24mm lens, 3/4 view, soft natural daylight, warm neutral palette (warm white, beige, light oak), clean and minimal, no people, no text, no logos, straight vertical lines, high detail. Any window view shows only soft hazy sky and trees, no buildings.
```
**After (편집)**
```
Edit this photo. Keep everything else exactly identical — same camera angle, framing, perspective, lighting and all other objects. Only change: turn one end of the balcony into a cozy home cafe corner: a light-oak bar counter along the window with two stools, a floating shelf with mugs and a small coffee machine, a warm pendant light, and a potted olive tree.
```
**자막**: 이런 텅 빈 베란다를 → 이렇게 홈카페로 만들려면?
**요청 체크리스트**
- 창가에 바 테이블과 선반으로 카페 코너를 만들어주세요
- 베란다 쪽에도 조명·콘센트를 추가해주세요
- 새시 틈 단열·환기 대책도 같이 봐주세요
- ⚠️ 싱크대를 두려면 오수관이 있어야 해요 (우수관 연결 불가)
