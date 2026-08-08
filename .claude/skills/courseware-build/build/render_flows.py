#!/usr/bin/env python3
"""Render an n8n-canvas image for each lab from the lab's own workflow JSON.

The node coordinates, names, types and connections all come out of the .json the
learner actually imports, so the picture on the slide is the canvas they will see
rather than a hand-drawn diagram that can drift out of date.

Output: courseware/assets/canvas-lab<N>[-<suffix>].png
"""
import json, os, sys, math
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

def _find_repo(start):
    env = os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env):
        return env
    d = start
    for _ in range(8):
        d = os.path.dirname(d)
        if os.path.isdir(os.path.join(d, "courseware")) and os.path.isdir(os.path.join(d, "labs")):
            return d
    return os.path.dirname(os.path.dirname(HERE))

REPO = _find_repo(HERE)
LABS = os.path.join(REPO, "labs")
OUT  = os.path.join(REPO, "courseware", "assets")

# ---------------------------------------------------------------- style
SCALE     = 3                   # supersample, then downscale for clean edges
OUT_SCALE = 2                   # final pixels per canvas unit — keeps node captions
                                # legible once the image is placed in a slide panel
BG      = (255, 255, 255)
DOT     = (222, 228, 236)
NODE_BG = (255, 255, 255)
NODE_ED = (208, 215, 225)
INK     = (22, 27, 38)
GREY    = (110, 119, 133)
WIRE    = (150, 158, 170)

# n8n's own accent colours, by node family
TRIGGER = (255, 111, 0)
AI      = (128, 58, 237)
DATA    = (31, 111, 235)
COMMS   = (16, 185, 129)
LOGIC   = (245, 158, 11)
TOOL    = (245, 158, 11)

NODE_W, NODE_H = 150, 92        # canvas units before scaling
TRIG_W = 120

def _font(px, bold=False):
    names = (["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Helvetica.ttc"] if bold else
             ["/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"])
    for n in names:
        if os.path.exists(n):
            try:
                return ImageFont.truetype(n, px)
            except Exception:
                pass
    return ImageFont.load_default()

def classify(ntype, name):
    """Map an n8n node type to (accent colour, short kind label)."""
    t = ntype.lower()
    if "trigger" in t or t.endswith("webhook") or "manualtrigger" in t:
        if "webhook" in t:   return TRIGGER, "Webhook"
        if "form" in t:      return TRIGGER, "Form Trigger"
        if "manual" in t:    return TRIGGER, "Manual"
        return TRIGGER, "Trigger"
    if "agent" in t:                       return AI, "AI Agent"
    if "lmchat" in t or "chatmodel" in t:  return AI, "Chat Model"
    if "memory" in t:                      return AI, "Memory"
    if "embeddings" in t:                  return AI, "Embeddings"
    if "vectorstore" in t:                 return AI, "Vector Store"
    if "outputparser" in t:                return AI, "Output Parser"
    if "textsplitter" in t:                return AI, "Text Splitter"
    if "documentdefault" in t or "dataloader" in t: return AI, "Data Loader"
    if "googlesheetstool" in t:            return TOOL, "Sheets tool"
    if "gmailtool" in t:                   return TOOL, "Gmail tool"
    if "tool" in t:                        return TOOL, "Tool"
    if "googlesheets" in t:                return DATA, "Google Sheets"
    if "googledrive" in t:                 return DATA, "Google Drive"
    if "gmail" in t:
        return COMMS, ("Send and Wait" if "approval" in name.lower() else "Gmail")
    if "respondtowebhook" in t:            return COMMS, "Respond"
    if t.endswith(".if") or "switch" in t: return LOGIC, "IF"
    if t.endswith(".set"):                 return LOGIC, "Edit Fields"
    if t.endswith(".code"):                return LOGIC, "Code"
    return DATA, ntype.split(".")[-1][:16]

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def relax(nodes):
    """n8n stores sub-nodes closer together than a label can be drawn.

    Node positions are authored for n8n's own compact node chrome; rendered with
    readable names underneath, rows whose nodes sit <MIN_GAP apart overlap. Spread
    each row out to MIN_GAP while keeping the authored left-to-right order and the
    row's centre, so the picture still matches the canvas the learner sees.
    """
    MIN_GAP = NODE_W + 110
    rows = {}
    for n in nodes:
        rows.setdefault(round(n["position"][1] / 40) * 40, []).append(n)
    for _, row in rows.items():
        row.sort(key=lambda n: n["position"][0])
        for i in range(1, len(row)):
            need = row[i - 1]["position"][0] + MIN_GAP
            if row[i]["position"][0] < need:
                row[i]["position"][0] = need
        # re-centre the row on the span it originally occupied
        if len(row) > 1:
            span = row[-1]["position"][0] - row[0]["position"][0]
            centre = sum(n["position"][0] for n in row) / len(row)
            start = centre - span / 2
            for i, n in enumerate(row):
                n["position"][0] = start + MIN_GAP * i
    return nodes


def render(json_path, out_name, title=None):
    wf = json.load(open(json_path))
    nodes = [n for n in wf.get("nodes", [])
             if not n.get("type", "").endswith("stickyNote")]
    if not nodes:
        return None
    relax(nodes)

    # --- lay out in canvas coordinates -----------------------------------
    xs = [n["position"][0] for n in nodes]
    ys = [n["position"][1] for n in nodes]
    PAD = 70
    minx, maxx = min(xs), max(xs) + NODE_W
    # leave room under the lowest row for the two-line node name beneath it
    miny, maxy = min(ys), max(ys) + NODE_H + 60

    # A tall, narrow graph (Lab 5's sub-node chains) would be scaled to the slide
    # panel's HEIGHT, leaving the nodes small. Spreading the deep rows sideways
    # flattens the graph so it scales to the panel WIDTH instead — the nodes come
    # out substantially larger without changing what the picture shows.
    # The slide's image panel is roughly 11.6in x 3.2in — about 3.6:1. Flatten the
    # graph to match, so it scales to the panel's WIDTH and the nodes come out as
    # large as the panel allows.
    TARGET_AR = 3.6
    gw, gh = (maxx - minx), (maxy - miny)
    if gh > 0 and gw / gh < TARGET_AR:
        rows = {}
        for n in nodes:
            rows.setdefault(round(n["position"][1] / 40) * 40, []).append(n)
        # widen each row about the graph's centre until the whole graph is flat enough
        k = (TARGET_AR * gh) / gw
        cx = (minx + maxx) / 2
        for row in rows.values():
            for n in row:
                n["position"][0] = cx + (n["position"][0] - cx) * k
        xs = [n["position"][0] for n in nodes]
        minx, maxx = min(xs), max(xs) + NODE_W
    W = int(maxx - minx + PAD * 2)
    H = int(maxy - miny + PAD * 2)

    img = Image.new("RGB", (W * SCALE, H * SCALE), BG)
    d = ImageDraw.Draw(img)

    def px(x, y):
        return int((x - minx + PAD) * SCALE), int((y - miny + PAD) * SCALE)

    # dotted canvas background, like the n8n editor
    step = 20
    for gx in range(0, W, step):
        for gy in range(0, H, step):
            cx, cy = gx * SCALE, gy * SCALE
            r = max(1, SCALE // 2)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=DOT)

    by_name = {n["name"]: n for n in nodes}

    def anchor(node, side):
        x, y = node["position"]
        col, _ = classify(node.get("type", ""), node["name"])
        w = TRIG_W if col is TRIGGER else NODE_W
        if side == "out":
            return x + w, y + NODE_H / 2
        return x, y + NODE_H / 2

    # --- wires ------------------------------------------------------------
    conns = wf.get("connections", {})
    for src, outs in conns.items():
        if src not in by_name:
            continue
        for kind, branches in outs.items():
            sub = (kind != "main")     # ai_languageModel / ai_tool / ai_memory …
            for branch in branches or []:
                for link in branch or []:
                    dst = link.get("node")
                    if dst not in by_name:
                        continue
                    a, b = by_name[src], by_name[dst]
                    if sub:
                        # sub-nodes hang BELOW their parent: draw upward into it
                        ax, ay = a["position"][0] + NODE_W / 2, a["position"][1]
                        bx, by_ = b["position"][0] + NODE_W / 2, b["position"][1] + NODE_H
                        x1, y1 = px(ax, ay); x2, y2 = px(bx, by_)
                        d.line([x1, y1, x1, (y1 + y2) // 2, x2, (y1 + y2) // 2, x2, y2],
                               fill=WIRE, width=max(1, SCALE - 1))
                        continue
                    ax, ay = anchor(a, "out"); bx, by_ = anchor(b, "in")
                    x1, y1 = px(ax, ay); x2, y2 = px(bx, by_)
                    midx = (x1 + x2) // 2
                    d.line([x1, y1, midx, y1, midx, y2, x2, y2],
                           fill=WIRE, width=max(1, SCALE - 1))
                    # arrow head
                    ah = 5 * SCALE
                    d.polygon([(x2, y2), (x2 - ah, y2 - ah // 2), (x2 - ah, y2 + ah // 2)],
                              fill=WIRE)

    # --- nodes ------------------------------------------------------------
    # The whole canvas is scaled down to fit the slide's image panel, so type sized
    # for the canvas alone comes out unreadable on the slide. Size the labels
    # relative to the node box instead — big enough to survive that reduction.
    f_name = _font(int(20 * SCALE), bold=True)
    f_kind = _font(int(15 * SCALE))
    for n in nodes:
        x, y = n["position"]
        col, kind = classify(n.get("type", ""), n["name"])
        w = TRIG_W if col is TRIGGER else NODE_W
        x1, y1 = px(x, y); x2, y2 = px(x + w, y + NODE_H)
        r = int(10 * SCALE)
        d.rounded_rectangle([x1, y1, x2, y2], radius=r, fill=NODE_BG,
                            outline=NODE_ED, width=max(1, SCALE - 1))
        # left accent bar in the node's family colour
        d.rounded_rectangle([x1, y1, x1 + int(7 * SCALE), y2], radius=r, fill=col)
        d.rectangle([x1 + int(4 * SCALE), y1, x1 + int(7 * SCALE), y2], fill=col)
        # kind label inside the node
        tw = (x2 - x1) - int(20 * SCALE)
        lines = wrap(d, kind, f_kind, tw)
        lh = int(18 * SCALE)
        ty = y1 + int(NODE_H * SCALE / 2) - int(len(lines) * lh / 2)
        for ln in lines:
            lw = d.textlength(ln, font=f_kind)
            d.text((x1 + int(13 * SCALE) + (tw - lw) / 2, ty), ln, font=f_kind, fill=GREY)
            ty += lh
        # node name underneath, like the canvas
        nlines = wrap(d, n["name"], f_name, (w + 30) * SCALE)
        ny = y2 + int(8 * SCALE)
        for ln in nlines:
            lw = d.textlength(ln, font=f_name)
            d.text((x1 + ((x2 - x1) - lw) / 2, ny), ln, font=f_name, fill=INK)
            ny += int(24 * SCALE)

    # Downscale the supersampled canvas for clean edges, but keep the result at
    # OUT_SCALE× canvas units: these are placed into a ~11in slide panel, and a
    # 1:1 render leaves the node captions at about 4pt on the projected slide.
    img = img.resize((W * OUT_SCALE, H * OUT_SCALE), Image.LANCZOS)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, out_name)
    img.save(path)
    print(f"  {out_name}  ({len(nodes)} nodes, {W*OUT_SCALE}x{H*OUT_SCALE})")
    return path

JOBS = [
    ("lab1-trigger-actions/lab-trigger-actions.json",          "canvas-lab1.png"),
    ("lab2-webhook-agent/lab2-webhook-agent.json",             "canvas-lab2.png"),
    ("lab3-chatbot-webhook/lab3-chatbot-webhooks.json",        "canvas-lab3.png"),
    ("lab4-human-in-the-loop/lab4-human-in-the-loop.json",     "canvas-lab4.png"),
    ("lab5-rag/lab5-Ingest-Simple-Vector-Store.json",          "canvas-lab5-ingest.png"),
    ("lab5-rag/LU5-rag-chatbot.json",                          "canvas-lab5-agent.png"),
]

if __name__ == "__main__":
    print("Rendering n8n canvases from the lab workflow JSON files:")
    for rel, out in JOBS:
        p = os.path.join(LABS, rel)
        if os.path.exists(p):
            render(p, out)
        else:
            print(f"  MISSING {rel}", file=sys.stderr)
