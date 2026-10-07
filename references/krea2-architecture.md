# Arquitetura de prompt — Krea 2

## 1. Filosofia

Krea 2 (12.9B, aesthetic-first) é "direção de arte em prosa": 1–2 parágrafos densos e legíveis, não listas de tags. O **medium vem primeiro** — é o maior knob de estilo do modelo. E lembre: por design ele prefere exploração estética a aderência literal — composição rígida é trabalho do Ideogram (JSON).

## 2. Medium primeiro (regra nº 1)

- "35mm film photograph, fine grain" → fotorealismo, grão, halation, DOF — sem dizer "photorealistic".
- "gouache painting" → superfície mate, brushstrokes, bordas soltas. "risograph print", "VHS still", "disposable camera flash", "medium format", "low-poly 3D render" — cada medium carrega um pacote estético inteiro.
- **Sem medium**: estilo diferente a cada geração (bom para mood-sweep, péssimo para consistência).
- **"photo"/"photorealistic" sozinho** = meio genérico (cara de stock). Nomeie câmera + artefatos dela.
- Paleta: 2–3 cores concretas ("warm ochre and teal"); "vibrant colors" não segura nada.

## 3. A forma do prompt que funciona

Descreva a foto pronta para uma pessoa ao telefone. A forma que mais gera "keepers":

```
<sujeito> <UMA ação> <fonte(s) de luz com direção> <uma textura que importa> <medium/formato>
```

> `a fishmonger in a yellow rubber apron arranging silver mackerel on crushed ice at a covered market stall, early morning, cold blue daylight mixing with warm tungsten bulbs overhead, wet reflective concrete floor, 35mm film photograph, slight motion blur on his hands`

- **Diagnóstico de "mushy": quando a geração amolece, o prompt quase sempre tem DUAS ações competindo ou ZERO luz descrita.** Corte uma ação ou nomeie a luz.
- Concordância: atributo colado ao sujeito ("the woman wearing the red coat").
- Restatement = ênfase (repetir com palavras diferentes). Nada de `(x:1.3)`.

## 4. Dois regimes de comprimento

| Regime | Como | Quando |
|---|---|---|
| **Exploração** | 1 frase vaga de propósito | Pesquisa de direção |
| **Controle** | 1–2 parágrafos densos | Briefing fechado |

## 5. Style Reference (hosted)

- Até 4 referências, slider 0–100%: **20%** sutil · **50%** equilibrado · **80%** referência domina · **>80–90%** o estilo sobrescreve o SUJEITO.
- 1 referência forte > 4 medianas. Gallery do Krea tem style refs one-click.
- Prompt descreve CONTEÚDO; a referência carrega o estilo.
- Style transfer clássico com slider de influência (25/50/75% testar) está no **Krea 1**, não no Krea 2 Turbo.

## 6. Moodboard

- Prompt mínimo ("a frog"); clustering extrai taste profile (keywords + avoids). Compartilhável por link. Aplique "avoids" como positive constraints.

## 7. Generative Sliders + Creativity (API hosted)

| Slider | Efeito | Uso típico |
|---|---|---|
| `intensity` −100..100 | quão estilizado | + expressivo, − sóbrio |
| `complexity` | densidade da composição | − minimalista |
| `movement` | energia de pose/câmera | + dinâmico |
| `creativity` | quanto o Krea expande o prompt | baixa = briefing; alta = exploração |

Funcionam SEM mudar o prompt — ajuste sliders antes de reescrever texto.

## 8. LoRAs oficiais — as 9 trigger phrases (tabela completa)

| LoRA | Trigger phrase |
|---|---|
| Darkbrush | `monochrome ink wash style` |
| Dotmatrix | `monochrome stippling style` |
| Kidsdrawing | `naive expressive sketch style` |
| Neondrip | `textured abstract style` |
| Rainywindow | `rainy window style` |
| Retroanime | `purple retro anime style` |
| Softwatercolor | `art deco watercolor style` |
| Sunsetblur | `ethereal motion blur style` |
| Vintagetarot | `vintage tarot style` |

- Treinadas no Raw, funcionam no Turbo. Prompt fala de CONTEÚDO; a LoRA carrega o estilo.
- Teste de estilo: mesmo sujeito + trocar só a trigger phrase ("a lighthouse on a rocky coast at dusk, waves breaking below").
- LoRA training aberto a todos (capture estilo/personagem/produto).

## 9. Workflow recomendado

1. **Turbo** para acertar o prompt (2s, ~2 units) → 2. **Medium/Large** (render) ou **Krea 1** (fotorreal/4K). 3. Resolução por checkpoint (RAW ~1K, Turbo 1K–2K) — não force 2K no RAW; upscale só no final. 4. Aspecto ANTES (1:1, 4:3, 3:4, 16:9, 9:16, 21:9, 3:2, 2:3). 5. Batch: "reuse parameters" + trocar só o sujeito. 6. Pós: aba Enhance (relight, background removal, detail).

## 10. Troubleshooting Krea 2

| Sintoma | Causa | Correção |
|---|---|---|
| Geração "mushy"/amorfa | Duas ações competindo ou zero luz descrita | Uma ação + fonte de luz nomeada |
| Cada draft num estilo diferente | Medium não nomeado | Medium primeiro |
| Cara de stock | "photo" vago | Câmera + grão/flash/DOF |
| Fundo errado | Não especificado | Diga o que o fundo É |
| Cores fora | Adjetivos de cor | 2–3 cores concretas |
| Texto gibberish | Limite do modelo | Ideogram/Seedream p/ texto |
| Turbo ≠ Medium no "mesmo" prompt | Modelos diferentes | Esperado |
| Resultado lindo mas errado do briefing | Aesthetic-first | Suba `creativity` não — BAIXE; ou vá de Ideogram JSON |
