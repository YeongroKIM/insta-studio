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
