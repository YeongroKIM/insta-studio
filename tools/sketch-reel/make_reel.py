"""펜 한 줄 인테리어 릴스 합성기 (formats/sketch-reel.md 4절 ④⑤).

Before·After 이미지 2장 + 바뀔 영역 → 손그림 선 애니메이션·전환·자막·정보 카드를 넣은 9:16 mp4.
사용: python3 make_reel.py <config.json> [--preview]
  --preview  0/3/6/9초 프레임 4장만 PNG로 (빠른 확인)
의존: node + playwright(크롬), ffmpeg. 새 pip 패키지 없음.
"""
from __future__ import annotations
import json, math, pathlib, random, shutil, subprocess, sys, tempfile

W, H, FPS = 1080, 1920, 30
HERE = pathlib.Path(__file__).resolve().parent

def wobbly_rect(x, y, w, h, seed=3):
    """바뀔 영역(0~1 비율)을 따라 대충 그은 손그림 선 path (끝이 살짝 삐져나오게)."""
    rnd = random.Random(seed)
    j = lambda a: a + rnd.uniform(-0.008, 0.008)
    X = lambda v: v * W
    Y = lambda v: v * H
    pts = [(x - 0.01, y + 0.004), (x + w + 0.012, y - 0.004), (x + w, y + h + 0.01),
           (x - 0.004, y + h), (x + 0.006, y - 0.012)]
    d = f"M{X(j(pts[0][0])):.1f},{Y(j(pts[0][1])):.1f}"
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        mx, my = (ax + bx) / 2 + rnd.uniform(-0.01, 0.01), (ay + by) / 2 + rnd.uniform(-0.006, 0.006)
        d += f" Q{X(mx):.1f},{Y(my):.1f} {X(j(bx)):.1f},{Y(j(by)):.1f}"
    return d

def build_html(cfg, base: pathlib.Path) -> str:
    def img(p):
        return (base / p).resolve().as_uri()
    x, y, w, h = cfg["area"]
    path = wobbly_rect(x, y, w, h, cfg.get("seed", 3))
    c = cfg["captions"]
    info = cfg.get("info", "")
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Gaegu:wght@700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:#000;font-family:'Gaegu',cursive}}
.layer{{position:absolute;inset:0;background-size:cover;background-position:center;transform-origin:50% 50%}}
#cap{{position:absolute;top:150px;width:100%;text-align:center;font-size:76px;color:#fff;
  text-shadow:0 3px 14px rgba(0,0,0,.45);letter-spacing:2px;padding:0 60px;line-height:1.25}}
#card{{position:absolute;left:60px;right:60px;bottom:230px;background:rgba(250,247,242,.93);border-radius:36px;
  padding:44px 48px;font-size:54px;color:#2F2A27;line-height:1.35;box-shadow:0 10px 40px rgba(0,0,0,.18)}}
#card .cta{{margin-top:22px;font-size:50px;color:#8A5A3C}}
#ai{{position:absolute;right:36px;bottom:120px;font-family:sans-serif;font-size:28px;color:rgba(255,255,255,.85);
  background:rgba(0,0,0,.28);padding:8px 16px;border-radius:12px}}
svg{{position:absolute;inset:0}}
#shade{{position:absolute;left:0;right:0;top:0;height:520px;background:linear-gradient(rgba(40,30,22,.42),rgba(40,30,22,0))}}
</style></head><body>
<div class="layer" id="before" style="background-image:url('{img(cfg['before'])}')"></div>
<div class="layer" id="after" style="background-image:url('{img(cfg['after'])}');opacity:0"></div>
<svg width="{W}" height="{H}"><path id="pen" d="{path}" fill="none" stroke="{cfg.get('pen_color', '#C8B48A')}"
  stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg>
<div id="shade"></div>
<div id="cap"></div>
<div id="card" style="opacity:0">{info}<div class="cta">🐿️ 예랑이한테 보내기 · 🌰 저장</div></div>
<div id="ai">AI 시뮬레이션</div>
<script>
const C = {json.dumps(c, ensure_ascii=False)};
const pen = document.getElementById('pen'); const L = pen.getTotalLength();
pen.style.strokeDasharray = L;
const cl = (v,a,b)=>Math.min(1,Math.max(0,(v-a)/(b-a)));
const ease = t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
window.render = (t)=>{{
  const zb = 1 + 0.03*cl(t,0,4), za = 1.02 + 0.05*cl(t,4.4,10);
  before.style.transform = `scale(${{zb}})`; after.style.transform = `scale(${{za}})`;
  const draw = ease(cl(t,2,3.6));
  pen.style.strokeDashoffset = L*(1-draw);
  pen.style.opacity = 1 - cl(t,3.8,4.6);
  after.style.opacity = ease(cl(t,3.6,4.4));
  cap.textContent = t<2 ? C.before : t<4.2 ? C.sketch : C.after;
  cap.style.opacity = (t>1.85&&t<2.05)||(t>4.05&&t<4.35) ? 0.2 : 1;
  const k = ease(cl(t,8,8.6));
  card.style.opacity = k; card.style.transform = `translateY(${{(1-k)*60}}px)`;
}};
</script></body></html>"""

SHOT_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const [html, outDir, dur, fps, only] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + html, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const times = only ? only.split(',').map(Number) : [...Array(Math.round(dur*fps)).keys()].map(i => i / fps);
  let i = 0;
  for (const t of times) {
    await p.evaluate(t => window.render(t), t);
    await p.screenshot({ path: `${outDir}/f_${String(i++).padStart(4,'0')}.png` });
  }
  await b.close();
})();
"""

def main():
    cfg_path = pathlib.Path(sys.argv[1]).resolve()
    preview = "--preview" in sys.argv
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    base = cfg_path.parent
    out = (base / cfg.get("out", cfg_path.stem + ".mp4")).resolve()
    dur = cfg.get("duration", 10)
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        (td / "reel.html").write_text(build_html(cfg, base), encoding="utf-8")
        (td / "shot.js").write_text(SHOT_JS, encoding="utf-8")
        frames = td / "frames"; frames.mkdir()
        only = "0.5,3,6,9" if preview else ""
        subprocess.run(["node", str(td / "shot.js"), str(td / "reel.html"), str(frames), str(dur), str(FPS), only], check=True)
        if preview:
            for i, f in enumerate(sorted(frames.glob("*.png"))):
                shutil.copy(f, out.with_name(f"{out.stem}_preview{i}.png"))
            print("preview →", out.parent)
            return
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "f_%04d.png"),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", str(out)], check=True)
        print("reel →", out)

if __name__ == "__main__":
    main()
