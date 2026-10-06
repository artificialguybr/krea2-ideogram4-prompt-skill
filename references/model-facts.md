# Fatos de modelo — Krea 2 × Ideogram 4.0

> Síntese da pesquisa (docs oficiais krea-ai/krea-2 no GitHub, blog/paper do Ideogram 4.0, docs.ideogram.ai, runware.ai, fal.ai). Confira sempre a doc oficial se algo parecer desatualizado.

## 1. Krea 2 — arquitetura relevante para prompting

- 12B MMDiT single-stream; text encoder **Qwen3-VL-4B-Instruct** (um VLM real — lê gramática, possessivos, contagens, relações espaciais); VAE Qwen Image.
- Consequência: **prosa natural > tags**. O encoder entende "the brass key on the second shelf from the top". Ele NÃO dá boost por `masterpiece, 8k`.
- Ordem importa: o que vem primeiro é lido como sujeito principal (front-loading).
- "Restatement" funciona como ênfase: repetir o atributo com palavras diferentes pesa mais que qualquer sintaxe de peso.
- Palavras de **textura/material** condicionam melhor que palavras de cor abstrata ("sun-bleached linen" > "warm orange tones").
- **Iluminação é o atributo mais sensível**: nomeie fonte, direção e qualidade ("low golden sun through a window from camera-left, soft falloff").
- Exclusões: descreva o espaço negativo como instrução positiva ("clean white background, no other objects in frame"). Negative prompt carregado reduz qualidade.

## 2. Variantes e parâmetros (NÃO misturar)

| Variante | Steps | CFG | Resolução | Notas |
|---|---|---|---|---|
| Krea 2 **RAW** (open) | 52 | 3.5 | ~1K | Fidelidade máxima ao prompt; mais lento |
| Krea 2 **Turbo** (open) | 8 | 0 | 1K–2K | ~2s; guidance distillation `mu 1.15`; negative prompt pode nem afetar (CFG 0) |
| Krea 2 **Medium** (hosted) | — | — | — | Ilustração/artístico; sliders de creativity/intensity |
| Krea 2 **Large** (hosted) | — | — | — | Fotorrealismo / máxima qualidade |

- Hosted (app/API Krea) usa sliders (`creativity`, `intensity`, força de style-ref) — não exporte steps/CFG de RAW/Turbo para lá, e vice-versa.
- **Krea 2 ≠ FLUX.1 Krea [dev]**: modelo anterior, regras de prompt diferentes.
- No ComfyUI, se usar o node de atenção do Kijai, o weighting vira *attention value scaling* (funciona) — mas é exceção; o padrão continua sendo restatement.
- Criatividade como knob de workflow: baixa = execução fiel (trabalho de cliente); alta = exploração/surpresa controlada.

## 3. Ideogram 4.0 — arquitetura relevante

- 9.3B open-weight; treinado **exclusivamente em legendas JSON estruturadas** (bloco de estilo + elementos com bbox + paletas de cor).
- **CFG assimétrica**: no passo incondicional os tokens de texto são dropados.
- O prompt é **validado contra o schema** antes de gerar — JSON inválido é rejeitado.
- **Endpoint 4.0 NÃO tem `seed` nem `negative_prompt`.** Mesmo JSON reenviado dá consistência de composição, não reprodução pixel a pixel.
- **Magic Prompt**: expande linguagem natural → JSON automaticamente. Na API 4.0 roda sempre que `positivePrompt` é enviado (sem toggle); no app há toggle on/off. Desligue quando o texto exato importa (ele pode reescrever).
- Presets de sampler: `V4_QUALITY_48` (45 passos gw≈7 + 3 de polimento gw≈3), `V4_DEFAULT_20`, `V4_TURBO_12`. Dica: passos extras depois dos ~12-14 ajudam mais em cenas complexas e fotorrealismo.
- Edição: o 4.0 **regenera a imagem inteira** a cada chamada. Edição com mask preservando o resto existe no Ideogram **3.0 Edit** (use seed + mask lá).
- Safety filter local: plain text tem taxa maior de falso-positivo; JSON reduz bloqueios em conteúdo borderline-legítimo.

## 4. Tabela decisória — qual caminho de prompt?

| Precisa de… | Krea 2 | Ideogram 4 |
|---|---|---|
| Exploração livre de estilo | Prompt curto vago (mood-sweep) | Magic Prompt ligado |
| Fidelidade total ao briefing denso | Prosa densa 1–2 parágrafos | JSON estruturado escrito à mão |
| Posicionamento por coordenadas | — | JSON com `bbox` |
| Paleta de cor exata (hex) | Descrever materiais/cores | JSON `color_palette` (≤16 cores/img, ≤5/elemento) |
| Identidade de personagem em edição | Identity Edit LoRA | — |
| Tipografia longa / logotipo | Aspas + layout descrito | JSON: `text` + `art_style`; verificar OCR depois |
