# sketch-reel — 펜 한 줄 인테리어 릴스 합성기

`formats/sketch-reel.md`의 ④ 손그림 선 + ⑤ 합성을 자동으로 한다.

```
python3 make_reel.py examples/demo.json            # mp4 (10초, 1080x1920, 30fps)
python3 make_reel.py examples/demo.json --preview  # 확인용 프레임 4장
```

config (JSON, 경로는 config 기준 상대):
| 키 | 뜻 |
|---|---|
| `before`, `after` | 같은 구도의 이미지 2장 (9:16 권장, 아니면 가운데 기준 잘림) |
| `area` | 바뀔 영역 `[x, y, w, h]` — 화면 비율 0~1 |
| `captions` | `before` / `sketch` / `after` 단계 자막 |
| `info` | 마지막 정보 카드 문구 (디자인 이름 · 비용 범위 · 주의점, 지식 DB 근거) |
| `out`, `duration`, `seed`, `pen_color` | 선택 |

- 완성 영상과 이미지는 **저장소에 커밋하지 않는다** (`.gitignore`). 클라우드 폴더에 보관
- 우하단 "AI 시뮬레이션" 표기는 항상 들어간다 (검수표 G)

## stages 모드 — 빈집 채우기 (`formats/build-up-reel.md`)
config에 `stages`가 있으면 단계별 교차 전환 영상을 만든다 (길이 자동 계산).
```json
{"stages": [{"image": "0-empty.png", "caption": "입주 전 빈 거실"},
            {"image": "1-ceiling.png", "caption": "천장 라인 조명"}],
 "info": "정보 카드 문구", "out": "build.mp4", "hold": 1.5, "fade": 0.6}
```
- 상단에 `STEP n / N` 표시, 전체가 아주 느리게 줌인
- 모든 단계 이미지는 같은 구도여야 한다 (앞 단계를 넣고 편집하는 연쇄 편집으로 만든다)
