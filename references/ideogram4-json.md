# Ideogram 4.x — Linguagem natural × JSON estruturado (schema canônico)

> Schema validado contra o repo oficial `ideogram-oss/ideogram4` (docs/prompting.md). O 4.5 aceita o mesmo formato na geração.

## 1. Os dois caminhos

| Caminho | Como funciona | Quando usar |
|---|---|---|
| **Natural language** (`positivePrompt`) | Magic/Expand Prompt expande para JSON automaticamente (na API 4.0 sempre rola; no app há toggle) | Exploração, ideias rápidas, prompts <80 palavras |
| **Structured JSON** (`structuredPrompt`) | O modelo recebe o JSON como escrito — "what you write is what renders" | Copy exata, layout, paleta, posição, iteração fina, pesos locais |

⚠️ Expand/Magic Prompt **reescreve** seu texto — em testes mudou a CAIXA DE LETRAS e adicionou cena não pedida. Com toggle, desligue quando wording/case importarem (OFF = "keeps your wording and only converts it into a structured prompt").
⚠️ Nos **pesos locais**, plain text direto NÃO funciona e ainda dispara falso-positivo do safety filter. Use o Magic Prompt local (`ideogram-4-v1` grátis, ou `claude-opus-v1`/`claude-sonnet-v1` via OpenRouter — system prompts open-source no repo) ou escreva o JSON.

## 2. Prompt em linguagem natural (quando usar)

```
[FRASE 1 — o que a imagem mostra; texto exato entre aspas aqui]
[FRASE 2 — estilo/medium e características do sujeito]
[FRASE 3 — iluminação, câmera, ambiente, mood, cores]
```

- 2–3 frases cheias > parágrafos; **>80–90 palavras arriscam descartar elementos do final** → migre para JSON.
- Mais importante primeiro (o modelo pesa o início).
- Fotógrafo, não poeta: "single soft key light from the upper left", "shot on 50mm f/1.8, shallow depth of field".
- Substantivos específicos > adjetivos vazios. Exclusões como instrução positiva ("clean white background, no other text") — não existe negative_prompt.
- Fecho útil para layouts limpos: **"No other text."**

## 3. Schema JSON canônico

Três chaves de topo (ordem fixa): `high_level_description` → `style_description` → `compositional_deconstruction` (este **obrigatório**).

```json
{
  "high_level_description": "Uma ou duas frases resumindo a cena inteira.",

  "style_description": {
    "aesthetics": "moody, cinematic, desaturated",
    "lighting": "low-key, deep shadows, single warm practical",
    "photo": "35mm, f/1.4, shallow depth of field, eye-level",
    "medium": "photograph",
    "color_palette": ["#1B1B2F", "#162447", "#E43F5A", "#F5F5F5"]
  },

  "compositional_deconstruction": {
    "background": "só cenário/superfície/atmosfera — objetos e textos vão em elements",
    "elements": [
      {"type": "obj", "bbox": [200, 300, 800, 900], "desc": "..."},
      {"type": "text", "bbox": [80, 100, 220, 900], "text": "HEADLINE", "desc": "..."}
    ]
  }
}
```

### Regras estritas (verificadas pelo CaptionVerifier — warnings em violações)

1. **`style_description`** exige exatamente UM de: `photo` (fotos) ou `art_style` (todo o resto: ilustração, pintura, 3D, graphic_design). Ambos são **strings** (não objetos). `aesthetics`, `lighting`, `medium` obrigatórios; `color_palette` opcional.
2. **Ordem das chaves depende do caminho**:
   - foto: `aesthetics` → `lighting` → `photo` → `medium` → `color_palette`
   - não-foto: `aesthetics` → `lighting` → `medium` → `art_style` → `color_palette`
3. **`medium`** é string: "photograph", "illustration", "3d_render", "painting", "graphic_design"…
4. **Elementos** (`obj`/`text`), ordem fixa:
   - `obj`: `type` → `bbox` → `desc` → `color_palette`
   - `text`: `type` → `bbox` → `text` → `desc` → `color_palette`
   - `bbox` e `color_palette` opcionais; se presentes, nessas posições.
5. **`text` = string LITERAL** a renderizar ("DR. FAUKLAND'S") — sem aspas extras dentro do valor; acentos/apóstrofos são reproduzidos como escritos.
6. **`bbox`**: `[y_min, x_min, y_max, x_max]`, inteiros 0–1000, origem no canto superior esquerdo, **linha antes de coluna**.
7. **Hex MAIÚSCULO `#RRGGBB`** — sem shorthand (#fff é inválido). ≤16 cores no nível de imagem; ≤5 por elemento; inclua a cor do fundo na paleta; inclua par contraste (highlight + shadow).
8. **`background`** antes de `elements`; `background` = cenário, NUNCA sujeito/objeto discreto.
9. **Ordene `elements` em ordem de leitura** (topo→baixo, fundo→frente) — descricões tipo "directly beneath the title block" precisam que o título venha antes.
10. **Serialização Python**: `json.dumps(caption, separators=(",", ":"), ensure_ascii=False)` — escapes `\uXXXX` geram warning.
11. Print/pôster/gráfico "que parece foto" = **`art_style`** mesmo assim (fork de comportamento do modelo; errar aqui é das causas mais comuns de resultado ruim).

## 4. Enquadramento por aspect ratio (bbox aproximadas, 0–1000)

| Aspect | Headshot | Meio corpo | Corpo inteiro |
|---|---|---|---|
| 1:1 | y 120–380 | y 150–750 | y 90–960 |
| 2:3 / 9:16 | y 60–320 | y 100–800 | y 20–50 → 930–970 |
| 3:2 / 4:3 | y 100–400 | y 150–850 | y 80–960 |
| 16:9 | y 120–420 | y 150–880 | ⚠️ evitar — altura vertical insuficiente |

Posição em linguagem no `desc` primeiro ("centered along the top"); `bbox` quando o descritivo continuar derivando.

## 5. Quando IR DE JSON (6 casos oficiais)

1. **Copy exata importa** — headlines, nomes de marca, preços, datas.
2. **Múltiplos textos com hierarquia** — título + subtítulo + data + selo.
3. **5+ objetos distintos** — a frase única perde elementos.
4. **Cor precisa** — `color_palette` em hex é sinal mais direto que prosa.
5. **Posição precisa** — `bbox` fixa a região.
6. **Iterar uma parte sem reescrever tudo** — mude um `desc` e reenvie.

## 6. O loop de iteração (substituto do seed no 4.0)

1. Gere com `positivePrompt` → a resposta traz o JSON expandido.
2. Capture o JSON, altere **exatamente um** elemento/cor/bbox.
3. Reenvie como `structuredPrompt` — o resto da cena se mantém porque o JSON é o contrato.
4. Regra prática: **a 1ª geração quase sempre deve vir de NL**; hand-authoring total do JSON raramente é o ponto de partida certo.
5. Consistência = composição similar, NÃO pixel-perfect (sem seed no 4.0). No 4.5, seed + mesmo tier = repetível.

## 7. Exemplo real (negócio/cartão — do guia oficial)

```json
{"high_level_description":"A clean, modern business card layout for a tech company.","style_description":{"aesthetics":"minimal, professional, geometric","lighting":"even, diffuse studio lighting","medium":"graphic_design","art_style":"flat vector design, generous whitespace, sans-serif typography","color_palette":["#FFFFFF","#F0F0F0","#333333","#0066FF","#00CC88"]},"compositional_deconstruction":{"background":"A solid off-white card surface with subtle paper texture.","elements":[{"type":"text","text":"ACME TECH","desc":"Bold dark grey sans-serif company name across the upper third of the card."},{"type":"text","text":"hello@acme.tech","desc":"Small blue sans-serif contact email near the bottom of the card."}]}}
```

## 8. Dicas avançadas

- `photo` vs `art_style` errado = pior que prompt vago. Print gráfico = `art_style`.
- `high_level_description` vago deixa o modelo derivar — seja específico.
- Passos: além de ~12–14, extras ajudam mais em cena complexa/fotorrealismo (QUALITY já inclui polimento).
- Background Remover (4.0/3.0) gera alpha cutout para composição.
- 4.5: mesmo JSON + Expand Prompt OFF para copy exata; tipo de tipografia é seguido "mais solto" — tranque o tier de qualidade antes de refinar lettering.
