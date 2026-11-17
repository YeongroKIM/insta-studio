"""다람이·곰곰이 v4 (복슬 납작떡체) SVG 생성기.
털 가장자리(삐죽 털)는 손으로 그리기 어려워 여기서 계산한다.
사용: python3 gen_v4.py <출력 디렉터리>
"""
from __future__ import annotations
import math, random, sys, pathlib

INK = "#1A1614"

def shape_pt(t, w, h, p, flat):
    c, s = math.cos(t), math.sin(t)
    x = w / 2 * math.copysign(abs(c) ** (2 / p), c)
    y = h / 2 * math.copysign(abs(s) ** (2 / p), s)
    if y > 0:
        y *= flat  # 아랫면은 납작하게
    return x, y

def fluffy(cx, cy, w, h, n=34, amp=7, seed=1, p=2.4, flat=0.75, smooth_bottom=True, rot=0):
    """삐죽삐죽한 털 외곽선 path d."""
    rnd = random.Random(seed)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        pts.append((t, *shape_pt(t, w, h, p, flat)))
    cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    def tr(x, y):
        return cx + x * cr - y * sr, cy + x * sr + y * cr
    d = []
    for i, (t, x, y) in enumerate(pts):
        t2, x2, y2 = pts[(i + 1) % n]
        px, py = tr(x, y)
        d.append(("M" if i == 0 else "L") + f"{px:.1f},{py:.1f}")
        mx, my = (x + x2) / 2, (y + y2) / 2
        bottom = math.sin((t + t2) / 2) > 0.45
        a = amp * (0.25 if (bottom and smooth_bottom) else rnd.uniform(0.6, 1.3))
        L = math.hypot(mx, my) or 1
        tx, ty = tr(mx + mx / L * a + rnd.uniform(-2, 2), my + my / L * a)
        d.append(f"L{tx:.1f},{ty:.1f}")
    return " ".join(d) + " Z"

def daram(x, y, s=1.0, veil=True, acorn=False, eyes="dot"):
    """다람이: 주황 납작떡 + 큰 복슬 꼬리 + 앞니."""
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    # 꼬리 (몸 뒤)
    g.append(f'<path d="{fluffy(60, -40, 62, 100, n=26, amp=4.5, seed=11, p=2.0, flat=1, smooth_bottom=False, rot=20)}" fill="#F0B07A"/>')
    g.append(f'<path d="{fluffy(80, -98, 56, 48, n=20, amp=4, seed=12, p=2.0, flat=1, smooth_bottom=False)}" fill="#F0B07A"/>')
    g.append(f'<path d="M74,-102 q10,4 6,14" fill="none" stroke-width="2.6"/>')
    # 베일 (몸 뒤로 늘어짐)
    if veil:
        g.append('<path d="M-8,-56 C-62,-64 -104,-34 -114,18 C-100,28 -86,24 -80,16 C-72,-14 -46,-38 -4,-48 Z" fill="#FFFFFF"/><path d="M-60,-40 C-80,-24 -92,-4 -96,14" fill="none" stroke="#C9C0B8" stroke-width="2"/>')
    # 귀
    g.append('<path d="M-40,-44 C-46,-62 -40,-74 -32,-76 C-24,-70 -20,-58 -20,-48" fill="#F7CFA2"/>')
    g.append('<path d="M20,-48 C22,-60 28,-72 36,-74 C42,-66 42,-54 38,-44" fill="#F7CFA2"/>')
    g.append('<path d="M-33,-80 l-2,-8 M36,-78 l3,-8" fill="none" stroke-width="2.6"/>')
    # 몸
    g.append(f'<path d="{fluffy(0, 0, 150, 100, n=30, amp=4.5, seed=7)}" fill="#F7CFA2"/>')
    # 이마 줄무늬
    g.append('<path d="M-8,-44 l-1,10 M2,-46 l0,11 M12,-44 l1,10" fill="none" stroke="#B9703F" stroke-width="3"/>')
    # 얼굴
    if eyes == "dot":
        g.append(f'<circle cx="-16" cy="-12" r="3.6" fill="{INK}" stroke="none"/><circle cx="16" cy="-12" r="3.6" fill="{INK}" stroke="none"/>')
    else:  # 웃는 눈
        g.append('<path d="M-22,-10 q6,-8 12,0 M10,-10 q6,-8 12,0" fill="none" stroke-width="2.8"/>')
    g.append('<path d="M-6,0 q3,4 6,0 q3,4 6,0" fill="none" stroke-width="2.4"/>')
    g.append('<path d="M-4,4 v6 h8 v-6 M0,4.5 v5" fill="#FFFFFF" stroke-width="2"/>')
    g.append('<ellipse cx="-34" cy="0" rx="9" ry="5.5" fill="#FF9EA5" stroke="none" opacity="0.8"/><ellipse cx="34" cy="0" rx="9" ry="5.5" fill="#FF9EA5" stroke="none" opacity="0.8"/>')
    # 발
    g.append('<path d="M-30,34 q4,7 12,4 M18,38 q8,3 12,-4" fill="none" stroke-width="2.6"/>')
    # 화관 꽃
    if veil:
        g.append('<g stroke-width="2.4"><circle cx="-2" cy="-58" r="5" fill="#FFFFFF"/><circle cx="8" cy="-60" r="5" fill="#FFFFFF"/><circle cx="3" cy="-52" r="5" fill="#FFFFFF"/><circle cx="3" cy="-57" r="2.6" fill="#F7C35F"/></g>')
    if acorn:
        g.append('<g transform="translate(0,22)"><ellipse cx="0" cy="6" rx="11" ry="12" fill="#C58A5C"/><path d="M-13,1 C-11,-10 11,-10 13,1 Z" fill="#7A4E33"/><path d="M0,-8 l2,-6" fill="none"/></g>')
        g.append('<path d="M-18,28 q-6,-6 2,-10 M18,28 q6,-6 -2,-10" fill="#F7CFA2" stroke-width="2.6"/>')
    g.append('</g>')
    return "\n".join(g)

def gom(x, y, s=1.0, sweat=False):
    """곰곰이: 갈색 큰 납작떡 + 나비넥타이."""
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    g.append('<circle cx="-50" cy="-56" r="15" fill="#CFA47C"/><circle cx="50" cy="-56" r="15" fill="#CFA47C"/>')
    g.append('<circle cx="-50" cy="-56" r="6" fill="#E3C3A0" stroke="none"/><circle cx="50" cy="-56" r="6" fill="#E3C3A0" stroke="none"/>')
    g.append(f'<path d="{fluffy(0, 0, 190, 120, n=34, amp=4.5, seed=21)}" fill="#CFA47C"/>')
    g.append('<ellipse cx="0" cy="-2" rx="22" ry="15" fill="#E8CDAE" stroke-width="2.6"/>')
    g.append(f'<ellipse cx="0" cy="-8" rx="6" ry="4.2" fill="{INK}" stroke="none"/>')
    g.append('<path d="M0,-4 v5 M-6,4 q6,4 12,0" fill="none" stroke-width="2.4"/>')
    g.append(f'<circle cx="-26" cy="-20" r="3.8" fill="{INK}" stroke="none"/><circle cx="26" cy="-20" r="3.8" fill="{INK}" stroke="none"/>')
    g.append('<ellipse cx="-46" cy="-2" rx="10" ry="6" fill="#FF9EA5" stroke="none" opacity="0.7"/><ellipse cx="46" cy="-2" rx="10" ry="6" fill="#FF9EA5" stroke="none" opacity="0.7"/>')
    g.append(f'<path d="M0,26 l-14,-8 v16 z M0,26 l14,-8 v16 z" fill="{INK}" stroke-width="2"/>')
    g.append('<path d="M-40,40 q4,6 12,4 M28,44 q8,2 12,-4" fill="none" stroke-width="2.6"/>')
    if sweat:
        g.append('<path d="M70,-40 q-6,10 0,14 q6,-4 0,-14 z" fill="#9FD3F2" stroke-width="2.2"/>')
    g.append('</g>')
    return "\n".join(g)

HEAD = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {{w}} {{h}}" width="{{w}}" height="{{h}}">
<defs><filter id="wob" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="2.5"/></filter></defs>
<rect width="{{w}}" height="{{h}}" fill="#FFFDF9"/>
<g filter="url(#wob)" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round">'''
TAIL = "</g></svg>"

HEART = '<path d="M{x},{y} c-2,-12 13,-16 17,-4 c4,-12 19,-8 17,4 c-2,12 -17,18 -17,24 c0,-6 -15,-12 -17,-24 z" fill="#FF8E99" stroke-width="2.8"/>'

def main(out: pathlib.Path):
    out.mkdir(parents=True, exist_ok=True)
    pair = HEAD.format(w=800, h=420) + "\n".join([
        daram(270, 290, 1.25, eyes="happy"),
        gom(540, 290, 1.25),
        HEART.format(x=388, y=210),
        '<path d="M50,370 C200,360 600,362 750,370" fill="none" stroke="#7DBB6F" stroke-width="5"/>',
    ]) + TAIL
    (out / "v4-fluffy.svg").write_text(pair, encoding="utf-8")
    # 스티커 시트용 단품
    for name, body in {
        "daram-veil": daram(200, 230, 1.3),
        "daram-acorn": daram(200, 230, 1.3, veil=False, acorn=True, eyes="happy"),
        "gom-basic": gom(200, 230, 1.15),
        "gom-sweat": gom(200, 230, 1.15, sweat=True),
    }.items():
        (out / f"v4-{name}.svg").write_text(HEAD.format(w=400, h=320) + body + TAIL, encoding="utf-8")

if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."))
