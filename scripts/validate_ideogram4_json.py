#!/usr/bin/env python3
"""Validador offline do structuredPrompt do Ideogram 4.0.

Uso:
    python validate_ideogram4_json.py prompt.json
    echo '<json>' | python validate_ideogram4_json.py -

Checks (baseados na pesquisa do schema; confira docs.ideogram.ai para o schema
canônico atual):
  - JSON parseável
  - chaves snake_case
  - ordem canônica das chaves de nível superior e de style_description
  - style_description: photo XOR art_style
  - color_palette: hex válidos, <=16 cores (nível estilo), <=5 por elemento
  - bbox: 4 inteiros 0..1000, ordem [y_min, x_min, y_max, x_max], y_min<x_max? (na verdade y_min<y_max e x_min<x_max)
  - text: string entre aspas duplas quando presente
  - high_level_description: existe e e' uma string

Exit code 0 = OK, 1 = erro(s) encontrado(s).
"""
import json, re, sys

HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

TOP_ORDER = ["high_level_description", "style_description", "compositional_deconstruction"]
STYLE_ORDER = ["aesthetics", "lighting", "photo", "art_style", "color_palette"]
ELEM_ORDER = ["object", "text", "description", "bbox", "color_palette"]

def snake_case(k: str) -> bool:
    return bool(re.fullmatch(r"[a-z][a-z0-9_]*", k))

def check_order(obj: dict, expected: list, path: str, errs: list):
    keys = list(obj.keys())
    for k in keys:
        if k not in expected:
            errs.append(f"{path}: chave inesperada '{k}'")
    idx = [expected.index(k) for k in keys if k in expected]
    if idx != sorted(idx):
        errs.append(f"{path}: ordem das chaves fora do canônico {expected} (veio {keys})")

def validate(p) -> list:
    errs = []
    if not isinstance(p, dict):
        return ["raiz deve ser um objeto JSON"]

    check_order(p, TOP_ORDER, "$", errs)
    for k in p:
        if not snake_case(k):
            errs.append(f"$: chave '{k}' não é snake_case")

    hld = p.get("high_level_description")
    if not isinstance(hld, str) or not hld.strip():
        errs.append("high_level_description ausente ou vazio")

    sd = p.get("style_description")
    if not isinstance(sd, dict):
        errs.append("style_description ausente ou não-objeto")
    else:
        check_order(sd, STYLE_ORDER, "$.style_description", errs)
        for k in sd:
            if not snake_case(k):
                errs.append(f"$.style_description: chave '{k}' não é snake_case")
        if "photo" in sd and "art_style" in sd:
            errs.append("style_description: use 'photo' OU 'art_style', nunca ambos")
        pal = sd.get("color_palette")
        if pal is not None:
            if not isinstance(pal, list):
                errs.append("color_palette deve ser lista")
            else:
                if len(pal) > 16:
                    errs.append(f"color_palette com {len(pal)} cores (máx 16)")
                for c in pal:
                    if not HEX_RE.match(str(c)):
                        errs.append(f"cor inválida '{c}' (use #RRGGBB)")

    cd = p.get("compositional_deconstruction")
    if not isinstance(cd, dict):
        errs.append("compositional_deconstruction ausente ou não-objeto")
    else:
        if not isinstance(cd.get("background"), str):
            errs.append("compositional_deconstruction.background ausente")
        els = cd.get("elements")
        if not isinstance(els, list) or not els:
            errs.append("elements deve ser lista não-vazia")
        else:
            for i, e in enumerate(els):
                path = f"$.elements[{i}]"
                if not isinstance(e, dict):
                    errs.append(f"{path}: não-objeto"); continue
                check_order(e, ELEM_ORDER, path, errs)
                t = e.get("text")
                if t is not None:
                    ts = str(t)
                    if not (ts.startswith('"') and ts.endswith('"')):
                        errs.append(f"{path}.text deve vir entre aspas duplas: {ts!r}")
                bb = e.get("bbox")
                if bb is not None:
                    if (not isinstance(bb, list) or len(bb) != 4
                            or not all(isinstance(v, int) for v in bb)):
                        errs.append(f"{path}.bbox deve ser [y_min, x_min, y_max, x_max] de inteiros")
                    else:
                        y0, x0, y1, x1 = bb
                        if not (0 <= y0 < y1 <= 1000 and 0 <= x0 < x1 <= 1000):
                            errs.append(f"{path}.bbox fora de 0..1000 ou invertido: {bb}")
                ep = e.get("color_palette")
                if ep is not None:
                    if not isinstance(ep, list) or len(ep) > 5:
                        errs.append(f"{path}.color_palette: lista com no máx 5 cores")
                    else:
                        for c in ep:
                            if not HEX_RE.match(str(c)):
                                errs.append(f"{path}: cor inválida '{c}'")
    return errs

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "-"
    raw = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[ERRO] JSON inválido: {e}"); sys.exit(1)
    prompts = data if isinstance(data, list) else [data]
    all_ok = True
    for n, p in enumerate(prompts):
        errs = validate(p)
        if errs:
            all_ok = False
            print(f"[prompt {n}] {len(errs)} problema(s):")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"[prompt {n}] OK")
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
