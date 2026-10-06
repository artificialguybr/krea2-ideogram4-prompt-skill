---
name: krea2-ideogram4-prompting
description: "Prompt engineering para Krea 2 (RAW/Turbo/hosted) e Ideogram 4.0 (text-to-image, structured JSON, Magic Prompt, Canvas/Edit). Use para criar, converter, reparar, expandir, fazer reverse-prompt de imagens e gerar instruções de edição para qualquer modo de geração desses dois modelos."
---

# Krea 2 / Ideogram 4 — Prompt Engineering

Skill para gerar prompts de alta qualidade para **Krea 2** e **Ideogram 4.0**, em **todos os modos**: text-to-image, referência de estilo, moodboard, edição (Krea Annotate / Identity Edit, Ideogram Canvas Magic Fill & Extend, Ideogram 3.0 Edit), tipografia/renderização de texto e reverse-prompting.

---

## Regra de Ouro: ROTEIE ANTES DE ESCREVER

Nunca escreva o prompt direto. Primeiro identifique **modelo × superfície × objetivo** usando a tabela abaixo, depois abra a referência correspondente.

| # | Intenção do usuário | Modelo / Modo | Referência |
|---|---|---|---|
| 1 | Criar imagem do zero (foto, arte, design) | Krea 2 T2I | `references/krea2-architecture.md` |
| 2 | Criar com controle rigoroso de layout/cor/posição | Ideogram 4 JSON estruturado | `references/ideogram4-json.md` |
| 3 | Criar rápido, explorar ideias | Ideogram 4 natural language (+ Magic Prompt) | `references/ideogram4-json.md` §3 |
| 4 | Manter estilo de imagem(s) de referência | Krea 2 Style Reference / Moodboard | `references/krea2-architecture.md` §5–6 |
| 5 | Editar região de uma imagem no app Krea | Krea Edit (Change Region / Annotate) | `references/editing.md` §2 |
| 6 | Re-stage pessoa / face swap / try-on / trocar cenário com identidade preservada | Krea 2 Identity Edit (ComfyUI/app) | `references/editing.md` §3 |
| 7 | Preencher região (inpaint) ou expandir (outpaint) | Ideogram Canvas (Magic Fill / Extend) | `references/editing.md` §4 |
| 8 | Edição local fina preservando o resto pixel a pixel | **Ideogram 3.0 Edit** (não o 4.0!) | `references/editing.md` §5 |
| 9 | Gerar texto/logotipo/tipografia dentro da imagem | Qualquer um → | `references/typography.md` |
| 10 | Analisar uma imagem e extrair/recriar o prompt | Reverse-prompting | `references/reverse-prompting.md` |
| 11 | Prompt falhou / resultado ruim | Diagnóstico e reparo | `references/failure-repair.md` |
| 12 | Precisa de atalho por gênero (foto, pôster, UI, 3D…) | Presets | `references/genre-presets.md` |

Se a intenção não estiver clara, pergunte: **modelo**, **superfície** (app web, API, ComfyUI) e **o que deve permanecer inalterado** (em edições).

---

## Fatos rápidos de modelo (leia antes de sugerir settings)

- **Krea 2 = LLM-encoded**: o texto passa por Qwen3-VL-4B-Instruct. Linguagem natural, gramática e relações espaciais funcionam; tags soltas e pesos `(x:1.3)` não. Detalhes completos e parâmetros de cada variante (RAW 52 steps CFG 3.5 / Turbo 8 steps CFG 0 / hosted Medium-Large com creativity slider) em `references/model-facts.md`.
- **Ideogram 4 = contrato estruturado**: treinado exclusivamente em legendas JSON. Linguagem natural é expandida pelo Magic Prompt para JSON; você pode escrever o JSON direto para controle total. **Sem `seed` e sem `negative_prompt` no endpoint 4.0.** Presets de sampler: `V4_QUALITY_48`, `V4_DEFAULT_20`, `V4_TURBO_12`.
- Os dois são parentes conceituais (encoder de linguagem, não CLIP), mas **não intercambiem sintaxe**: Krea 2 quer prosa densa; Ideogram 4 quer hierarquia declarativa ou JSON.

Guard rails completos (o que proibir/converter) estão em `references/failure-repair.md` §1.

---

## Guard rails inegociáveis (aplicar a TODO output)

1. **Proibido** keyword confetti: `masterpiece, best quality, 8k, ultra detailed` → converter em descrição visual concreta.
2. **Proibido** weighting estilo SD/CLIP `(palavra:1.3)` → usar *restatement* (descrever o atributo duas vezes com palavras diferentes).
3. Texto a renderizar **sempre entre aspas duplas** e **cedo no prompt**; máx. ~4 palavras por elemento de texto.
4. Prompt natural-language do Ideogram com **>80 palavras** → oferecer migração para JSON.
5. `photo` e `art_style` juntos no JSON do Ideogram → alertar e forçar escolha.
6. Corpo inteiro em 16:9 → alertar; sugerir 2:3 / 9:16.
7. Edição: proibido descrever a *operação* ("replace X with Y") — descrever o *resultado* ("She wears the black bodysuit"); proibido a palavra "reference" no prompt de edição; **uma mudança por instrução**.
8. Negative prompt: Krea → mínimo/positivo; Ideogram 4 → o campo não existe, expressar exclusões como constraint positivo.
9. Nunca misturar parâmetros RAW/Turbo com hosted; nunca tratar Krea 2 como FLUX.1 Krea [dev].
10. Se houver edição localizada com preservação do restante → rotear para Ideogram **3.0 Edit** (o 4.0 regenera tudo).

---

## Output profile padrão

Todo prompt entregue ao usuário deve vir neste formato:

```
FINAL PROMPT (EN)
<prompt pronto para colar>

POSITIVE CONSTRAINTS
<exclusões descritas positivamente, se houver>

NEGATIVE PROMPT
<apenas se o workflow suportar; senão: "n/a — expressar como constraint positivo">

SUGGESTED SETTINGS
<aspect ratio, modelo/variante, steps/CFG ou preset de sampler, creativity/style-ref strength, dials de edição>

ASSUMPTIONS / NEXT ITERATION
<hipóteses feitas + qual única variável mudar na próxima rodada>
```

Escreva o prompt final **em inglês** (ambos os modelos respondem melhor), mas toda a explicação em **português**.

---

## Diagnóstico rápido (sintoma → ação)

| Sintoma | Causa provável | Vá para |
|---|---|---|
| Imagem "desmonta" ao usar peso | Weighting de embedding | failure-repair §2 |
| Ideogram bloqueia prompt benigno (local) | Falso-positivo do safety filter em plain text | ideogram4-json §6 (usar JSON) |
| Texto renderizado erra letra | Prompt longo demais / texto tarde no prompt | typography.md |
| Edit do Ideogram mudou a imagem inteira | Arquitetura do 4.0 | editing.md §5 |
| Edit Identity gerou "double picture" | `grounding_px` alto demais | editing.md §3 |
| Dois rostos derretem um no outro no edit | Dupla referência de pessoas | editing.md §3 |
| Estilo da referência engoliu o sujeito | Style-ref strength >80% | krea2-architecture §5 |
| Elementos do fim do prompt sumiram | Prompt >80–90 palavras (Ideogram) | ideogram4-json §3 |

Referências: veja `references/`. Instalação: `INSTALL.md`.
