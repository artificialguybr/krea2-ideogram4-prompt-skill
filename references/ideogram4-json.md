# Ideogram 4.0 — Linguagem natural × JSON estruturado

## 1. Os dois caminhos

| Caminho | Como funciona | Quando usar |
|---|---|---|
| **Natural language** (`positivePrompt`) | Magic Prompt expande para JSON automaticamente (na API sempre; no app há toggle) | Exploração, ideias rápidas, prompts <80 palavras |
| **Structured JSON** (`structuredPrompt`) | O JSON que você escreve É o contrato de geração | Controle de layout, paleta, posição, iteração fina |

⚠️ Magic Prompt **pode reescrever** seu texto (incluindo texto a renderizar). Com toggle no app, desligue quando a precisão importar.

## 2. Estrutura do prompt em linguagem natural

```
[FRASE 1 — o que a imagem mostra, texto entre aspas aqui se houver]
[FRASE 2 — estilo/medium e características do sujeito]
[FRASE 3 — iluminação, câmera, ambiente, mood, cores]
```

- 2–3 frases cheias são melhores que parágrafos; **>80–90 palavras arriscam descartar elementos do final** (nesse caso, migre para JSON).
- Hierarquia: coloque o mais importante primeiro (o modelo pesa mais o início).
- Trate como direção de fotografia: "single soft key light from the upper left", "shot on 50mm f/1.8, shallow depth of field".
- Substantivos específicos > adjetivos vazios ("wet asphalt" > "beautiful street").
- **Exclusões como instrução positiva**: "clean white background, no other objects in frame" — não há negative_prompt no 4.0.

## 3. Schema JSON (reconstruído da pesquisa — valide contra docs.ideogram.ai antes de produção)

```json
{
  "high_level_description": "Uma frase resumindo a cena inteira.",

  "style_description": {
    "aesthetics": ["movement / vibe / era"],
    "lighting": "fonte + direção + qualidade",
    "photo": {
      "camera_type": "...",
      "lens": "...",
      "aperture": "...",
      "iso": "...",
      "shutter_speed": "...",
      "film": "..."
    },
    "art_style": {
      "movement": "...",
      "medium": "...",
      "surface": "...",
      "line_quality": "..."
    },
    "color_palette": ["#hex", "...", "até 16 cores"]
  },

  "compositional_deconstruction": {
    "background": "o que preenche o fundo",
    "elements": [
      {
        "object": "nome do objeto (ou vazio se for só texto)",
        "text": "TEXTO ENTRE ASPAS",
        "description": "detalhes do elemento",
        "bbox": [y_min, x_min, y_max, x_max],
        "color_palette": ["#hex", "até 5 cores"]
      }
    ]
  }
}
```

Regras do schema:
- **snake_case**, ordem das chaves importa (é validado).
- **`photo` OU `art_style` — nunca ambos.** É um fork de comportamento do modelo, não um rótulo. Pôster/print/gráfico mesmo "fotorrealista" → `art_style`. Escolher errado é das causas mais comuns de resultado abaixo do esperado.
- `bbox`: 4 inteiros 0–1000, **linha antes de coluna** (`[y_min, x_min, y_max, x_max]`).
- Paletas: até 16 cores no nível de estilo, até 5 por elemento. Hex é condicionamento direto (melhor que descrever cor em prosa).
- `text` sempre com a string exata entre aspas.

## 4. Enquadramento por aspect ratio (bbox aproximadas, coordenadas 0–1000)

| Aspect | Headshot | Meio corpo | Corpo inteiro |
|---|---|---|---|
| 1:1 | y 120–380 | y 150–750 | y 90–960 |
| 2:3 / 9:16 | y 60–320 | y 100–800 | y 20–50 → 930–970 |
| 3:2 / 4:3 | y 100–400 | y 150–850 | y 80–960 |
| 16:9 | y 120–420 | y 150–880 | ⚠️ evitar — altura vertical insuficiente |

Dica: descreva posição em linguagem primeiro ("centered, upper third"); use bbox só quando o descritivo não bastar.

## 5. O loop de iteração (o superpoder do JSON)

1. Envie `positivePrompt` (NL) → a resposta da API inclui o JSON expandido.
2. Copie o JSON, **altere exatamente um** elemento/paleta/bbox.
3. Reenvie como `structuredPrompt`.

O resto da cena se mantém porque o JSON é o contrato. Isso substitui o seed (que não existe no 4.0). Consistência = composição similar, não pixel-perfect — alinhe a expectativa do usuário.

## 6. Dicas avançadas

- Plain text local leva mais falso-positivo de safety filter → preferir JSON quando o conteúdo for borderline-legítimo (ex.: anatomia artística, medical, editorial polêmico).
- Passos: além de ~12–14, passos extras mais ajudam cenas complexas/fotorrealismo (preset QUALITY já inclui polimento final).
- Para edições: o 4.0 regenera tudo — veja editing.md §5 para o roteamento correto com 3.0 Edit.
