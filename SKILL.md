---
name: krea2-ideogram4-prompting
description: "Prompt engineering para Krea 2 (RAW/Turbo/hosted, com Generative Sliders) e Ideogram 4.0/4.5 (text-to-image, structured JSON, Magic/Expand Prompt, Canvas, Precise Edit com mask e multi-turn). Use para criar, converter, reparar, expandir, fazer reverse-prompt de imagens e gerar instruções de edição para qualquer modo desses modelos."
---

# Krea 2 / Ideogram 4.x — Prompt Engineering

Skill para gerar prompts de alta qualidade para **Krea 2** e **Ideogram 4.0/4.5**, em **todos os modos**: text-to-image, referência de estilo, moodboard, edição (Krea Annotate / Identity Edit, Ideogram Canvas e o Precise Edit do 4.5 com mask), tipografia e reverse-prompting.

> **Nota de versão (out/2026):** inclui Ideogram **4.5** (edição precisa multi-turn) e os **Generative Sliders** do Krea 2 na API.

---

## Regra de Ouro: ROTEIE ANTES DE ESCREVER

Nunca escreva o prompt direto. Primeiro identifique **modelo × superfície × objetivo** usando a tabela abaixo, depois abra a referência correspondente.

| # | Intenção do usuário | Modelo / Modo | Referência |
|---|---|---|---|
| 1 | Criar imagem do zero (foto, arte, design) | Krea 2 T2I | `references/krea2-architecture.md` |
| 2 | Criar com controle rigoroso de layout/cor/posição | Ideogram 4 JSON estruturado (4.5 aceita o mesmo formato) | `references/ideogram4-json.md` |
| 3 | Criar rápido, explorar ideias | Ideogram 4.x natural language (+ Magic/Expand Prompt) | `references/ideogram4-json.md` §2 |
| 4 | Manter estilo de imagem(s) de referência | Krea 2 Style Reference / Moodboard | `references/krea2-architecture.md` §5–6 |
| 5 | Editar região de uma imagem no app Krea | Krea Edit (Change Region / Annotate) | `references/editing.md` §2 |
| 6 | Re-stage pessoa / face swap / try-on com identidade preservada | Krea 2 Identity Edit (ComfyUI/app) | `references/editing.md` §3 |
| 7 | Inpaint/outpaint com janela de geração (prompt descreve a CENA da janela) | Ideogram Canvas (Magic Fill / Extend) | `references/editing.md` §4 |
| 8 | **Editar parte preservando o resto** (trocar texto, roupa, cor; correção fina) | **Ideogram 4.5 Precise Edit** (Edit Precision High + mask; multi-turn) | `references/editing.md` §5 |
| 8b | Editar imagem enviada por upload na API do 4.0 | Ideogram 4.0 **remix** (v2) | `references/editing.md` §6 |
| 9 | Editar sem API 4.5 | **Edição hosted do Ideogram**: v1/edit ou v2 remix do 4.0 (máscara só no 4.5) | `references/editing.md` §6 |
| 10 | Gerar texto/logotipo/tipografia na imagem | Qualquer um → | `references/typography.md` |
| 11 | Analisar imagem e extrair/recriar o prompt | Reverse-prompting (Ideogram MCP `describe_image` faz isso nativamente) | `references/reverse-prompting.md` |
| 12 | Prompt falhou / resultado ruim | Diagnóstico e reparo | `references/failure-repair.md` |
| 13 | Atalho por gênero (foto, pôster, UI, 3D…) | Presets | `references/genre-presets.md` |

Se a intenção não estiver clara, pergunte: **modelo**, **superfície** (app Krea, Ideogram app/API, ComfyUI, pesos locais) e **o que deve permanecer inalterado** (em edições).

**Dica de superfície:** o app Krea também hospeda o **Ideogram 4.0 nativo em 2K** — se o usuário está no ecossistema Krea, pode preferir gerar o Ideogram lá.

---

## Fatos rápidos de modelo (leia antes de sugerir settings)

- **Krea 2 = LLM-encoded**: **12.9B** DiT, encoder Qwen3-VL multi-camada. Prosa natural funciona; tags e pesos `(x:1.3)` não. Variantes RAW (52 steps, CFG 3.5, **não destilado**) / Turbo (8 steps, CFG 0) / hosted (`krea-2/medium`, `large`, `medium-turbo`). Sliders na API: `intensity`, `complexity`, `movement` (−100 a 100) + Creativity. RAW treinado até ~1K; Turbo de 1K a 2K (não force 2K no RAW). **Aesthetic-first**: exploração > aderência literal — briefing rígido vai pro Ideogram JSON.
- **Ideogram 4.0 = contrato estruturado**: treinado exclusivamente em legendas JSON. NL passa pelo Magic Prompt (expansão automática na API); JSON direto = "what you write is what renders". **v2 atual aceita `seed`; `negative_prompt` não existe em 4.0 nem 4.5** (v1 legado: confirmar na doc). Presets: `V4_QUALITY_48` / `V4_DEFAULT_20` / `V4_TURBO_12`.
- **Ideogram 4.5 (30/set/2026) = o modelo de EDIÇÃO**: multi-turn com mínimo drift, **Edit Precision High** preserva pixels não tocados (~96% byte-idênticos após 3 turnos), mask precisa (preto = editar, branco = manter, mesmo tamanho da fonte), até 4 imagens de referência, seed voltou a existir, 2K nativo, 4 tiers de qualidade. Schema de geração = mesmo JSON do 4.0.
- **Não intercambie sintaxe**: Krea 2 quer prosa densa (medium no início!); Ideogram quer hierarquia declarativa/JSON. Os dois são parentes conceituais, não iguais.

Guard rails completos em `references/failure-repair.md` §1. Schema canônico do JSON em `references/ideogram4-json.md` §3 (baseado no repo oficial ideogram-oss/ideogram4 — `type`/`desc`, hex MAIÚSCULO, ordem de chaves estrita).

---

## Guard rails inegociáveis (aplicar a TODO output)

1. **Proibido** keyword confetti: `masterpiece, best quality, 8k, ultra detailed` → converter em descrição visual concreta.
2. **Proibido** weighting estilo SD/CLIP `(palavra:1.3)` → usar *restatement* (descrever o atributo duas vezes com palavras diferentes).
3. **Krea 2: nomeie o MEDIUM primeiro** ("35mm film photograph", "gouache painting") — sem medium, o modelo explora estilos a cada geração.
4. Texto a renderizar: **string literal exata** no campo `text` do JSON (sem aspas extras — as aspas envolvem o valor, não vão dentro dele); em NL Krea, entre aspas duplas e cedo no prompt; ~4 palavras por elemento costuma segurar a legibilidade (conselho, não limite da API).
5. JSON do Ideogram: snake_case, **ordem estrita de chaves** (`type`/`desc` em elementos — NUNCA `object`/`description`), hex **MAIÚSCULO** `#RRGGBB`, `photo` XOR `art_style` (strings, não objetos), `medium` obrigatório, `compositional_deconstruction` sempre presente.
6. Prompt NL do Ideogram com **>~80 palavras** tende a perder elementos do fim (conselho de densidade, não limite da API) — acima disso, o JSON estruturado costuma segurar melhor. E em pesos **locais**, plain text direto NÃO funciona (vai pro Magic Prompt ou escreva o JSON).
7. Edição Ideogram 4.5: **uma mudança por turno** + "Keep everything else exactly the same." é o padrão confiável (vira estratégia de debug quando precisar isolar uma variável); Edit Precision **High** para construir em cima; **mask cobrindo o elemento antigo COM margem** ao substituir texto; High/mask exigem Image Size = Auto; use **Regular** só para mudar tamanho/proporção.
8. Edição Krea Identity: resultado (não operação), sem a palavra "reference", uma mudança por passo como debug (dials antes de mais palavras).
9. Negative prompt: Krea → mínimo/positivo (Turbo CFG 0 ignora); Ideogram 4.x → o campo não existe, expressar exclusões como constraint positivo ("clean background, no other text").
10. Nunca misturar parâmetros RAW/Turbo com hosted; nunca tratar Krea 2 como FLUX.1 Krea [dev].

---

## Output profile padrão

```
FINAL PROMPT (EN)
<prompt pronto para colar — prosa para Krea 2; JSON serializado (separators=(",",":"), ensure_ascii=False) para Ideogram>

POSITIVE CONSTRAINTS
<exclusões descritas positivamente, se houver>

NEGATIVE PROMPT
<apenas se o workflow suporta; senão: "n/a — expressar como constraint positivo">

SUGGESTED SETTINGS
<aspect ratio, modelo/variante, sampler preset ou steps/CFG, sliders Krea (intensity/complexity/movement/creativity), style-ref strength, dials de edição, Edit Precision/mask>

ASSUMPTIONS / NEXT ITERATION
<hipóteses + qual única variável mudar na próxima rodada>
```

Prompt final **em inglês**; explicação em **português**.

---

## Diagnóstico rápido (sintoma → ação)

| Sintoma | Causa provável | Vá para |
|---|---|---|
| Imagem "desmonta" ao usar peso | Weighting de embedding | failure-repair §2 |
| Toda geração sai num estilo diferente (Krea) | Medium não nomeado no início | krea2-architecture §2 |
| Parece stock photo genérica | "photorealistic" vago | krea2-architecture §2 (nomear câmera/filme/grão) |
| Ideogram bloqueia prompt benigno | Falso-positivo do safety filter em plain text (pior em pesos locais) | ideogram4-json §2 (usar JSON) |
| Letra trocada / case alterado (Ideogram) | Expand/Magic Prompt ligado | typography.md (desligar) |
| Sobraram traços do texto antigo após troca | Mask pequena demais | editing.md §5 (margem) |
| Cor/textura deriva após várias edições | Edit Precision Regular | editing.md §5 (High) |
| JSON do Ideogram gera warning | `object`/`description` ou hex minúsculo ou ordem errada | ideogram4-json §3 + validator |
| Elementos do fim do prompt sumiram | Prompt >80–90 palavras | ideogram4-json §2 |
| Edit mudou a imagem inteira | Edit Precision Regular / modelo errado | editing.md §5 |
| Style-ref engoliu o sujeito | Strength >80–90% | krea2-architecture §5 |
| "Double picture" no Identity Edit | `grounding_px` >768 | editing.md §3 |
| Geração amorfa/mushy (Krea) | Duas ações competindo ou zero luz | krea2-architecture §3 |
| Canvas mudou meu prompt | Magic Prompt ligado no Canvas | editing.md §4 (OFF) |
| Rostos/mãos ruins no Canvas | Janela grande = poucos pixels | editing.md §4 (upscale + janela < ½) |
| Estilo diferente a cada geração (Krea) | Sem medium no início | krea2-architecture §2 |

Referências: `references/`.
