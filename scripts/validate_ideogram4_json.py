#!/usr/bin/env python3
"""Validador offline do structuredPrompt do Ideogram 4.0/4.5.

Schema canônico conforme docs/prompting.md do repo oficial ideogram-oss/ideogram4.

Uso:
    python validate_ideogram4_json.py prompt.json
    echo '<json>' | python validate_ideogram4_json.py -

Checks:
  - parse JSON
  - chaves snake_case conhecidas
  - ordem estrita: topo (high_level_description, style_description, compositional_deconstruction)
  - style_description: exatamente UM de photo/art_style; ordem muda por caminho:
      foto:      aesthetics, lighting, photo, medium, color_palette
      nao-foto:  aesthetics, lighting, medium, art_style, color_palette
  - medium presente (string); color_palette opcional no FIM
  - hex MAIUSCULO #RRGGBB; <=16 cores (estilo), <=5 por elemento
  - compositional_deconstruction: background antes de elements (ambos obrigatórios)
  - elementos: type 'obj'|'text'; ordem obj = type,bbox,desc,color_palette;
               ordem text = type,bbox,text,desc,color_palette
  - text = string LITERAL (sem aspas internas)
  - bbox = [y_min, x_min, y_max, x_max], inteiros 0..1000, y_min<y_max, x_min<x_max

Exit 0 = OK, 1 = erro(s).
"""
import json, re, sys

HEX_RE = re.compile(r"^#[0-9A-F]{6}$")
TOP_ORDER = ["high_level_description", "style_description", "compositional_deconstruction"]
PHOTO_ORDER = ["aesthetics", "lighting", "photo", "medium", "color_palette"]
ART_ORDER = ["aesthetics", "lighting", "medium", "art_style", "color_palette"]
OBJ_ORDER = ["type", "bbox", "desc", "color_palette"]
TEXT_ORDER = ["type", "bbox", "text", "desc", "color_palette"]

def snake(k): return bool(re.fullmatch(r"[a-z][a-z0-9_]*", k))

def order_err(obj, expected, path, errs, allow_missing=()):
    keys = list(obj.keys())
    for k in keys:
        if k not in expected:
            errs.append(f"{path}: chave desconhecida '{k}'")
    idx = [expected.index(k) for k in keys if k in expected]
    if idx != sorted(idx):
        errs.append(f"{path}: ordem errada {keys}; esperado {expected}")

def check_palette(pal, maxc, path, errs):
    if not isinstance(pal, list):
        errs.append(f"{path}: color_palette deve ser lista"); return
    if len(pal) > maxc:
        errs.append(f"{path}: {len(pal)} cores (max {maxc})")
    for c in pal:
        if not HEX_RE.match(str(c)):
            errs.append(f"{path}: hex invalido '{c}' (use #RRGGBB maiusculo)")

def validate(p):
    errs = []
    if not isinstance(p, dict):
        return ["raiz deve ser objeto JSON"]
    order_err(p, TOP_ORDER, "$", errs)
    for k in p:
        if not snake(k): errs.append(f"$: chave '{k}' nao e snake_case")

    if "high_level_description" in p and not isinstance(p["high_level_description"], str):
        errs.append("high_level_description deve ser string (1-2 frases)")

    sd = p.get("style_description")
    if sd is not None:
        if not isinstance(sd, dict):
            errs.append("style_description deve ser objeto")
        else:
            has_photo, has_art = "photo" in sd, "art_style" in sd
            if has_photo and has_art:
                errs.append("style_description: use 'photo' OU 'art_style', nunca ambos")
            if not has_photo and not has_art:
                errs.append("style_description: precisa de 'photo' ou 'art_style'")
            order_err(sd, PHOTO_ORDER if has_photo else ART_ORDER, "$.style_description", errs)
            for k in sd:
                if not snake(k): errs.append(f"$.style_description: chave '{k}' nao e snake_case")
            for req in ("aesthetics", "lighting", "medium"):
                if req not in sd:
                    errs.append(f"style_description: '{req}' obrigatorio")
            for k in ("photo", "art_style"):
                if k in sd and not isinstance(sd[k], str):
                    errs.append(f"style_description.{k} deve ser STRING (ex.: '35mm, f/1.4')")
            if "color_palette" in sd:
                check_palette(sd["color_palette"], 16, "style_description.color_palette", errs)

    cd = p.get("compositional_deconstruction")
    if not isinstance(cd, dict):
        errs.append("compositional_deconstruction obrigatorio (objeto)")
    else:
        keys = list(cd.keys())
        if "background" not in keys: errs.append("compositional_decomposition: 'background' obrigatorio")
        if keys and keys[0] != "background":
            errs.append("compositional_deconstruction: 'background' deve vir antes de 'elements'")
        bg = cd.get("background")
        if bg is not None and not isinstance(bg, str):
            errs.append("background deve ser string (cenario, nunca sujeito)")
        els = cd.get("elements")
        if not isinstance(els, list) or not els:
            errs.append("elements deve ser lista nao-vazia")
        else:
            for i, e in enumerate(els):
                path = f"elements[{i}]"
                if not isinstance(e, dict):
                    errs.append(f"{path}: nao-objeto"); continue
                t = e.get("type")
                if t not in ("obj", "text"):
                    errs.append(f"{path}.type deve ser 'obj' ou 'text' (veio {t!r})")
                    continue
                order_err(e, TEXT_ORDER if t == "text" else OBJ_ORDER, path, errs)
                if t == "text":
                    tx = e.get("text")
                    if not isinstance(tx, str) or not tx:
                        errs.append(f"{path}.text obrigatorio (string literal a renderizar)")
                    elif tx != tx.strip() or (tx.startswith('"') and tx.endswith('"')):
                        errs.append(f"{path}.text deve ser o literal, sem aspas internas: {tx!r}")
                if "desc" not in e:
                    errs.append(f"{path}.desc obrigatorio")
                bb = e.get("bbox")
                if bb is not None:
                    if (not isinstance(bb, list) or len(bb) != 4
                            or not all(isinstance(v, int) for v in bb)):
                        errs.append(f"{path}.bbox = [y_min, x_min, y_max, x_max] inteiros 0..1000")
                    else:
                        y0, x0, y1, x1 = bb
                        if not (0 <= y0 < y1 <= 1000 and 0 <= x0 < x1 <= 1000):
                            errs.append(f"{path}.bbox fora de 0..1000 ou invertido: {bb}")
                if "color_palette" in e:
                    check_palette(e["color_palette"], 5, f"{path}.color_palette", errs)
    return errs

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "-"
    raw = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    if "\\u" in raw:
        print("[aviso] escapes \\uXXXX detectados — prefira ensure_ascii=False")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[ERRO] JSON invalido: {e}"); sys.exit(1)
    prompts = data if isinstance(data, list) else [data]
    ok = True
    for n, p in enumerate(prompts):
        errs = validate(p)
        if errs:
            ok = False
            print(f"[prompt {n}] {len(errs)} problema(s):")
            for e in errs: print(f"  - {e}")
        else:
            print(f"[prompt {n}] OK — schema canônico 4.0/4.5")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
