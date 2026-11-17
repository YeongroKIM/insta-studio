"""서체 후보 견본 이미지 생성 (타이틀/설명/강조). 사용: python3 gen_specimen.py <배경이미지> <출력폴더>
모두 상업적 무료(OFL 등) 한글 서체. 웹폰트 CDN에서 불러와 Playwright로 캡처한다."""
import pathlib, subprocess, sys, json
bg = pathlib.Path(sys.argv[1]).resolve().as_uri()
out = pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
LINKS = """
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/gh/sun-typeface/SUIT@2/fonts/static/woff2/SUIT.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/gh/wanteddev/wanted-sans@v1.0.3/packages/wanted-sans/fonts/webfonts/static/split/WantedSans.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Noto+Serif+KR:wght@700;900&family=Gowun+Batang:wght@700&family=Gowun+Dodum&family=Hahmlet:wght@700;800&family=IBM+Plex+Sans+KR:wght@500;700&family=Gothic+A1:wght@500&family=Black+Han+Sans&family=Do+Hyeon&family=Nanum+Myeongjo:wght@800&family=Nanum+Pen+Script&family=Nanum+Gothic:wght@700&display=swap" rel="stylesheet">
<style>@font-face{font-family:'GmarketSans';src:url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2001@1.1/GmarketSansBold.woff') format('woff');font-weight:700}</style>"""
T = [("T1","Pretendard","Pretendard",800),("T2","SUIT","SUIT",800),("T3","Wanted Sans","Wanted Sans",800),
     ("T4","G마켓 산스","GmarketSans",700),("T5","Noto Sans KR","Noto Sans KR",900),("T6","IBM Plex Sans KR","IBM Plex Sans KR",700),
     ("T7","Noto Serif KR (명조)","Noto Serif KR",700),("T8","고운바탕 (명조)","Gowun Batang",700),("T9","함렛 (명조)","Hahmlet",700),
     ("T10","검은고딕","Black Han Sans",400)]
D = [("D1","Pretendard","Pretendard",500),("D2","SUIT","SUIT",500),("D3","Wanted Sans","Wanted Sans",500),
     ("D4","Noto Sans KR","Noto Sans KR",500),("D5","IBM Plex Sans KR","IBM Plex Sans KR",500),("D6","Gothic A1","Gothic A1",500),
     ("D7","나눔고딕","Nanum Gothic",700),("D8","고운돋움","Gowun Dodum",400)]
H = [("H1","Pretendard Black + 마커","Pretendard",900),("H2","G마켓 산스 + 마커","GmarketSans",700),("H3","Noto Serif KR Black","Noto Serif KR",900),
     ("H4","함렛 ExtraBold","Hahmlet",800),("H5","나눔명조 ExtraBold","Nanum Myeongjo",800),("H6","검은고딕","Black Han Sans",400),
     ("H7","도현","Do Hyeon",400),("H8","나눔손글씨 펜 (포인트)","Nanum Pen Script",400)]
CSS = """*{margin:0;padding:0;box-sizing:border-box}body{background:#1f1d1b;padding:28px;font-family:Pretendard}
h1{color:#fff;font:800 40px Pretendard;margin:0 0 6px}p.sub{color:#bbb;font:500 22px Pretendard;margin-bottom:22px}
.g{display:grid;grid-template-columns:repeat(5,340px);gap:18px}.c{width:340px}
.card{position:relative;width:340px;height:520px;border-radius:18px;overflow:hidden;background:url('BG') center/cover}
.card:before{content:'';position:absolute;inset:0;background:linear-gradient(rgba(40,30,22,.45),rgba(40,30,22,0) 45%)}
.lab{color:#fff;font:700 24px Pretendard;margin-top:10px}.lab span{color:#aaa;font-weight:500;font-size:19px;margin-left:6px}
.t{position:absolute;top:44px;left:0;right:0;text-align:center;color:#fff;font-size:40px;line-height:1.2;text-shadow:0 2px 12px rgba(0,0,0,.4);padding:0 14px;letter-spacing:-.5px}
.t small{display:block;font-size:20px;letter-spacing:4px;opacity:.85;margin-bottom:8px}
.panel{position:absolute;left:14px;right:14px;top:100px;background:rgba(250,247,242,.96);border-radius:20px;padding:22px 20px;color:#2F2A27}
.panel b{display:block;font-size:25px;margin-bottom:10px;white-space:nowrap;letter-spacing:-1px}.panel li{list-style:none;font-size:21px;line-height:1.4;padding:10px 0 10px 32px;position:relative;border-top:1.5px solid #E9DFD3}
.panel li:before{content:'';position:absolute;left:0;top:13px;width:22px;height:22px;border-radius:6px;background:#8A5A3C}
.hl{position:absolute;left:18px;right:18px;top:150px;text-align:center}
.hl .k{display:inline-block;white-space:nowrap;font-size:42px;color:#2F2A27;padding:0 10px;background:linear-gradient(transparent 55%,#E9C9A0 55%)}
.hl .w{margin-top:26px;display:inline-block;background:rgba(250,247,242,.95);border-radius:16px;padding:16px 18px;font-size:27px;color:#9A4B2F;line-height:1.3}"""
def page(title, sub, cards):
    return f"<!doctype html><html><head><meta charset=utf-8>{LINKS}<style>{CSS.replace('BG', bg)}</style></head><body><h1>{title}</h1><p class=sub>{sub}</p><div class=g>{cards}</div></body></html>"
tc = "".join(f'<div class=c><div class=card><div class=t style="font-family:\'{f}\';font-weight:{w}"><small>BEFORE</small>이런 밋밋한<br>붙박이장을</div></div><div class=lab>{k}<span>{n}</span></div></div>' for k,n,f,w in T)
dc = "".join(f'<div class=c><div class=card><div class=panel style="font-family:\'{f}\';font-weight:{w}"><b style="font-family:Pretendard;font-weight:800">업체에 이렇게 요청하세요</b><ul><li>붙박이장 가운데 3~4칸을 가로로 긴 \'니치\'로 바꿔주세요</li><li>니치 위쪽에 간접조명(LED)을 숨겨서 넣어주세요</li><li>배선 위치는 목공 마감 전에</li></ul></div></div><div class=lab>{k}<span>{n}</span></div></div>' for k,n,f,w in D)
hc = "".join(f'<div class=c><div class=card><div class=hl style="font-family:\'{f}\';font-weight:{w}"><div class=k>니치 + 간접조명</div><div class=w>⚠️ 콘크리트 벽은<br>못 파요, 실측부터!</div></div></div><div class=lab>{k}<span>{n}</span></div></div>' for k,n,f,w in H)
pages = {"1-title": page("타이틀용 (상단 큰 자막)", "릴스 첫 화면 훅 · 캐러셀 표지 제목", tc),
         "2-description": page("설명용 (체크리스트·본문)", "카드 제목은 Pretendard 고정, 목록 서체만 바꿔 비교", dc),
         "3-highlight": page("강조용 (키워드·주의 문구)", "핵심 단어 마커 · ⚠️ 주의 문구", hc)}
js = r"""const {chromium}=require('playwright');(async()=>{const [h,o]=process.argv.slice(2);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1820,height:900},deviceScaleFactor:1});await p.goto('file://'+h,{waitUntil:'networkidle'});
await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);await p.screenshot({path:o,fullPage:true});await b.close();})();"""
(out/"shot.js").write_text(js)
for name, html in pages.items():
    hp = out/f"{name}.html"; hp.write_text(html, encoding="utf-8")
    subprocess.run(["node", str(out/"shot.js"), str(hp), str(out/f"{name}.png")], check=True)
    hp.unlink()
(out/"shot.js").unlink()
print("ok", out)
