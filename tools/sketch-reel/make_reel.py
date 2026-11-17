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
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:#000;font-family:'Pretendard',sans-serif;letter-spacing:-0.5px}}
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

def build_stages_html(cfg, base: pathlib.Path) -> tuple[str, float]:
    """빈집 채우기 모드: stages=[{image, caption}] 를 차례로 교차 전환. (formats/build-up-reel.md)"""
    st = cfg["stages"]
    hold, fade, tail = cfg.get("hold", 1.5), cfg.get("fade", 0.6), cfg.get("tail", 2.2)
    dur = len(st) * hold + (len(st) - 1) * fade + tail
    layers = "".join(
        f'<div class="layer" id="L{i}" style="background-image:url(\'{(base / s["image"]).resolve().as_uri()}\');opacity:{1 if i == 0 else 0}"></div>'
        for i, s in enumerate(st))
    caps = json.dumps([s["caption"] for s in st], ensure_ascii=False)
    info = cfg.get("info", "")
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:#000;font-family:'Pretendard',sans-serif;letter-spacing:-0.5px}}
#stage{{position:absolute;inset:0;transform-origin:50% 55%}}
.layer{{position:absolute;inset:0;background-size:cover;background-position:center}}
#shade{{position:absolute;left:0;right:0;top:0;height:520px;background:linear-gradient(rgba(40,30,22,.42),rgba(40,30,22,0))}}
#cap{{position:absolute;top:150px;width:100%;text-align:center;font-size:76px;color:#fff;text-shadow:0 3px 14px rgba(0,0,0,.45);padding:0 60px}}
#step{{position:absolute;top:96px;width:100%;text-align:center;font-family:sans-serif;font-size:30px;letter-spacing:4px;color:rgba(255,255,255,.85)}}
#card{{position:absolute;left:60px;right:60px;bottom:230px;background:rgba(250,247,242,.93);border-radius:36px;padding:44px 48px;font-size:54px;color:#2F2A27;line-height:1.35;opacity:0}}
#card .cta{{margin-top:22px;font-size:50px;color:#8A5A3C}}
#ai{{position:absolute;right:36px;bottom:120px;font-family:sans-serif;font-size:28px;color:rgba(255,255,255,.85);background:rgba(0,0,0,.28);padding:8px 16px;border-radius:12px}}
</style></head><body>
<div id="stage">{layers}</div><div id="shade"></div><div id="step"></div><div id="cap"></div>
<div id="card">{info}<div class="cta">🐿️ 예랑이한테 보내기 · 🌰 저장</div></div><div id="ai">AI 시뮬레이션</div>
<script>
const CAPS={caps}, N=CAPS.length, HOLD={hold}, FADE={fade};
const cl=(v,a,b)=>Math.min(1,Math.max(0,(v-a)/(b-a))); const ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
window.render=(t)=>{{
  stage.style.transform=`scale(${{1+0.08*cl(t,0,{dur})}})`;
  let cur=0;
  for(let i=1;i<N;i++){{ const s=i*HOLD+(i-1)*FADE; const k=ease(cl(t,s,s+FADE));
    document.getElementById('L'+i).style.opacity=k; if(t>=s+FADE*0.5) cur=i; }}
  cap.textContent=CAPS[cur]; step.textContent=cur===0?'':`STEP ${{cur}} / ${{N-1}}`;
  const end=N*HOLD+(N-1)*FADE, k=ease(cl(t,end-0.2,end+0.4));
  card.style.opacity=k; card.style.transform=`translateY(${{(1-k)*60}}px)`;
}};
</script></body></html>"""
    return html, dur

def build_ask_html(cfg, base: pathlib.Path) -> tuple[str, float]:
    """요청 문구 모드 (formats/request-reel.md): Before → 쓸어 넘기며 After → '업체에 이렇게 요청하세요' 체크리스트."""
    img = lambda p: (base / p).resolve().as_uri()
    lines = cfg["ask"]
    t_list = 6.0 + 1.1 * len(lines)
    dur = t_list + cfg.get("tail", 2.6)
    items = "".join(f'<li id="i{i}">{x}</li>' for i, x in enumerate(lines))
    c = cfg["captions"]
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:#000;font-family:'Pretendard',sans-serif;letter-spacing:-0.5px}}
.layer{{position:absolute;inset:0;background-size:cover;background-position:center;transform-origin:50% 50%}}
#after{{clip-path:inset(0 100% 0 0)}}
#bar{{position:absolute;top:0;bottom:0;width:6px;background:rgba(255,255,255,.9);box-shadow:0 0 18px rgba(0,0,0,.25);opacity:0}}
#shade{{position:absolute;left:0;right:0;top:0;height:520px;background:linear-gradient(rgba(40,30,22,.42),rgba(40,30,22,0))}}
#dim{{position:absolute;inset:0;background:rgba(250,247,242,.0)}}
#cap{{position:absolute;top:150px;width:100%;text-align:center;font-size:92px;font-weight:700;color:#fff;text-shadow:0 3px 18px rgba(0,0,0,.4);padding:0 60px;line-height:1.2}}
#tag{{position:absolute;top:0;left:0;right:0;text-align:center;font-size:34px;font-weight:600;letter-spacing:6px;color:rgba(255,255,255,.9);padding-top:92px}}
#panel{{position:absolute;left:48px;right:48px;top:430px;background:rgba(250,247,242,.95);border-radius:40px;padding:52px 50px 44px;opacity:0;box-shadow:0 14px 50px rgba(0,0,0,.2)}}
#panel h2{{font-size:74px;font-weight:800;color:#2F2A27;margin-bottom:28px;letter-spacing:-1.5px}}
#panel ul{{list-style:none}}
#panel li{{font-size:54px;font-weight:600;color:#2F2A27;line-height:1.32;padding:20px 0 20px 80px;position:relative;opacity:0;border-top:2px solid #E9DFD3;letter-spacing:-1px}}
#panel li:before{{content:'';position:absolute;left:0;top:30px;width:46px;height:46px;border:4px solid #8A5A3C;border-radius:10px;box-sizing:border-box}}
#panel li.on:before{{background:#8A5A3C}}
#panel li.on:after{{content:'';position:absolute;left:15px;top:37px;width:12px;height:24px;border:solid #fff;border-width:0 6px 6px 0;transform:rotate(45deg)}}
#panel .warn{{margin-top:24px;font-size:50px;font-weight:700;color:#9A4B2F;opacity:0;letter-spacing:-1px;line-height:1.3}}
#cta{{position:absolute;left:0;right:0;bottom:230px;text-align:center;font-size:56px;font-weight:700;color:#fff;text-shadow:0 3px 14px rgba(0,0,0,.5);opacity:0}}
#ai{{position:absolute;right:36px;bottom:120px;font-family:sans-serif;font-size:28px;color:rgba(255,255,255,.85);background:rgba(0,0,0,.28);padding:8px 16px;border-radius:12px}}
</style></head><body>
<div class="layer" id="before" style="background-image:url('{img(cfg['before'])}')"></div>
<div class="layer" id="after" style="background-image:url('{img(cfg['after'])}')"></div>
<div id="bar"></div><div id="dim"></div><div id="shade"></div><div id="tag"></div><div id="cap"></div>
<div id="panel"><h2>{c.get('ask_title', '업체에 이렇게 요청하세요 👇')}</h2><ul>{items}</ul>
<div class="warn">{cfg.get('warn', '')}</div></div>
<div id="cta">🌰 저장해두고 견적 받을 때 보여주세요</div><div id="ai">AI 시뮬레이션</div>
<script>
const C={json.dumps(c, ensure_ascii=False)}, N={len(lines)}, TL={t_list};
const cl=(v,a,b)=>Math.min(1,Math.max(0,(v-a)/(b-a))); const ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
window.render=(t)=>{{
  const z=1+0.06*cl(t,0,{dur}); before.style.transform=after.style.transform=`scale(${{z}})`;
  const w=ease(cl(t,2.2,3.2)); after.style.clipPath=`inset(0 ${{(1-w)*100}}% 0 0)`;
  bar.style.left=(w*{W}-3)+'px'; bar.style.opacity=(w>0&&w<1)?1:0;
  cap.textContent = t<2.2 ? C.before : C.after; tag.textContent = t<2.2 ? 'BEFORE' : 'AFTER';
  const p=ease(cl(t,5.2,5.9)); panel.style.opacity=p; panel.style.transform=`translateY(${{(1-p)*50}}px)`;
  dim.style.background=`rgba(40,30,22,${{0.35*p}})`; cap.style.opacity=tag.style.opacity=1-p;
  for(let i=0;i<N;i++){{ const s=6.0+1.1*i; const el=document.getElementById('i'+i);
    el.style.opacity=ease(cl(t,s,s+0.35)); el.className = t>s+0.6 ? 'on' : ''; }}
  document.querySelector('.warn').style.opacity=ease(cl(t,TL,TL+0.4));
  cta.style.opacity=ease(cl(t,TL+0.9,TL+1.4));
}};
</script></body></html>"""
    return html, dur

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
    if "stages" in cfg:
        html, dur = build_stages_html(cfg, base)
    elif "ask" in cfg:
        html, dur = build_ask_html(cfg, base)
    else:
        html, dur = build_html(cfg, base), cfg.get("duration", 10)
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        (td / "reel.html").write_text(html, encoding="utf-8")
        (td / "shot.js").write_text(SHOT_JS, encoding="utf-8")
        frames = td / "frames"; frames.mkdir()
        only = (",".join(f"{x:.2f}" for x in [0.5, dur*0.35, dur*0.7, dur-0.5])) if preview else ""
        subprocess.run(["node", str(td / "shot.js"), str(td / "reel.html"), str(frames), str(dur), str(FPS), only], check=True)
        if preview:
            for i, f in enumerate(sorted(frames.glob("*.png"))):
                shutil.copy(f, out.with_name(f"{out.stem}_preview{i}.png"))
            print("preview →", out.parent)
            return
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "f_%04d.png"),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-preset", "slow", "-movflags", "+faststart", str(out)], check=True)
        print("reel →", out)

if __name__ == "__main__":
    main()
