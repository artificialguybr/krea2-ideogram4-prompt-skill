# Modos de EDIÇÃO — Krea (app + Identity Edit) × Ideogram (Canvas + 4.5 Precise Edit)

## 1. Princípios universais de prompt de edição

1. **Descreva o RESULTADO, não a operação.** "She wears the black bodysuit" ✔ — "replace her dress with a bodysuit" ✘.
2. **Nunca escreva a palavra "reference"** no prompt. Anexe a imagem e nomeie a coisa normalmente.
3. **Uma mudança por turno é a estratégia de DEBUG** (isola a variável quando algo saiu errado). Em produção, o **Krea Annotate aceita múltiplas anotações independentes numa passada só**; no 4.5 Precise Edit, uma mudança + cláusula de preservação segue sendo o padrão confiável.
4. **Não re-descreva o que deve ficar.** Preservação é o default.
5. **Presente, terceira pessoa**: "She wears…", "The car is now red…".
6. Dials/settings antes de inflar o prompt com mais palavras.

## 2. Krea app — Edit (Change Region / Annotate / Expand / Relight)

- Linguagem natural simples, zero sintaxe especial.
- **Annotate**: marque várias regiões, cada uma com prompt próprio (e até imagem própria), e gere **uma única vez**.
- Crop/Expand: descreva o que preenche a área nova. Relight: descreva a nova luz, não o objeto.
- Selecionar → descrever resultado → gerar → avaliar 1 variável por vez.

## 3. Krea 2 Identity Edit (LoRA, app/ComfyUI) — re-stage, face swap, try-on

> ⚠️ **Adapter NÃO-oficial da comunidade** (autor: conradlocke — "unofficial community fine-tune… not affiliated with Krea.ai"). Exige o **node pack ComfyUI-Krea2Edit** (conditioning duplo que nós comuns não fornecem). Trate como experimento da comunidade, não como feature nativa do Krea.

**Wiring (ComfyUI):**
- Fluxo base (RAW ou Turbo) → nó Krea2IdentityEdit (cond poz + cond neg) → sampler.
- **Cond negativa = MESMA imagem com prompt vazio** ("keep the image"). Prompt vazio = preservar.
- Ordem fixa em cena+pessoa: **cena = imagem 1, pessoa = imagem 2**. Inverter degrada muito.
- Vocabulário que o LoRA entende: "edit", "inpaint", "outpaint" ("swap"/"replace" funcionam pior).

**Dials:**

| Dial | O que faz | Faixa útil |
|---|---|---|
| `grounding_px` | Prendedura literal na imagem | 384–768 (acima: "double picture") |
| `ref_boost` | Fidelidade da referência | ~4 = forte; >10 quebra remoções; <1 solta |
| `ref_boost_a` / `ref_boost_b` | Força por imagem de referência | subir se a 2ª imagem for ignorada |
| steps | ~8 composição; ~12+ detalhe facial | 8–12 |

**Limitações honestas:**
- **2 pessoas juntas**: roupas se mantêm, rostos derivam → encadear inserções individuais.
- **>2MP**: duplicação/sangramento → gerar em ≤2MP (1–1.5MP) e upscale depois.
- **Remoção de objeto**: funciona mas não é confiável (às vezes re-renderiza); reroll/rephrase; Raw/CFG 3 ajuda.
- **Troca de roupa no corpo**: parcialmente confiável; cenário simples ajuda.
- Troubleshooting: "double picture" → baixar `grounding_px`; identidade escorregando → subir `ref_boost`; 2ª ref ignorada → `ref_boost_b`.

**Template:**
```
She wears the black bodysuit.        ← resultado, 1 mudança
[anexar: pessoa, bodysuit]  grounding_px ~512 · ref_boost ~4 · 8–12 steps
```

## 4. Ideogram Canvas — Magic Fill (inpaint) & Extend (outpaint) — técnicas oficiais

⚠️ **Canvas e 4.5 Precise Edit pedem prompts de ESTILOS OPOSTOS:**

| | Canvas Magic Fill | 4.5 Precise Edit |
|---|---|---|
| Prompt | descreve **a cena inteira dentro da janela de geração** (não só a mudança) | **uma mudança** + "Keep everything else exactly the same." |
| Magic/Expand Prompt | **OFF recomendado** (altera prompt otimizado) | só geração; edição não usa |
| Preservação | máscara + contexto visual | pixels copiados da fonte (High) |

**Regras do Canvas:**
- Janela de geração tem **orçamento FIXO de pixels por aspect ratio** → janela PEQUENA e custom (ex.: 17:14) = mais densidade de pixel na região editada. Para corrigir rostos/mãos pequenos: **upscale primeiro (2×)**, depois Magic Fill com janela **< metade** do tamanho da imagem upscalada.
- Prompt = cena completa da janela, com a modificação incluída (ex.: "A photo of a woman holding a glass of milk in a modern white kitchen...").
- Para inserir elemento de OUTRA imagem: coloque as duas lado a lado, janela cobre ambas + contexto, prompt no padrão **"On the left, <elemento detalhado>. On the right, <cena alvo com o elemento>"**. Use o botão **Describe** para gerar descrição precisa de imagens enviadas antes de fundir prompts.
- Variação de detalhe (cor de cabelo etc.): re-rodar Magic Fill com o prompt original MODIFICADO só naquele atributo.
- Texto integrado à cena (ex.: escrito na areia): Text tool → texto totalmente preto → **Remix com image weight 100** (converte texto em imagem) → máscara no alvo → Magic Fill: "the same text in the same style, roughly written in the sand...".
- Extend: ajuste a janela para fora do frame + prompt descrevendo o que preenche; mantenha luz coerente com o original.
- Dica oficial: sinônimos/rephrasing mudam muito o resultado; input de alta qualidade; modificações simples funcionam melhor.

## 5. Ideogram 4.5 — Precise Edit (multi-turn) ⭐ o modo principal de edição fina

Lançado 30/set/2026 como "o modelo de edição mais preciso". Resolve o problema histórico: editar parte sem estragar o resto.

**Padrão de prompt (oficial + testado):**
```
<uma mudança, resultado descrito>. Keep everything else exactly the same.
```
Ex.: `Change the date line to "Fridays in August · 6–11 pm". Keep everything else exactly the same.`
Texto novo entre aspas; diga qual elemento existente ele substitui ("Replace the headline NIGHT MARKET with ... in the same font, colour and position").

**Edit Precision:**
| Modo | O que faz | Quando usar |
|---|---|---|
| **High** | Precise Edit: copia da fonte os pixels que a edição não mudou (~91% byte-idêntico após 1 turno; 96% intacto após 3) | **Qualquer edição em que você vai construir em cima**; cadeias multi-turn |
| **Regular** | Redesenha o frame inteiro (0,3% idêntico) | Quando quer mudar tamanho/proporção de saída — único modo que muda size |
| High/masked | exigem **Image Size = Auto** | — |

**Mask (quando a mudança é grande / substituição):**
- Preto = área a editar; branco = preservar; **mesmo WxH da imagem fonte**; deve conter as duas cores.
- Ao substituir elemento (ex.: headline maior): cubra o elemento antigo INTEIRO **com margem** — senão sobram traços ("MRCHÉ" com restos de "NIGHT" dentro do MA).
- Abaixo da mask, ~93–99,9% dos pixels ficam idênticos.

**Referências:** até 4 imagens de referência na edição; personagem referenciado se mantém (consistência confirmada em testes).

**Limites práticos (API):**
- Seed existe e torna runs repetíveis **no mesmo tier de qualidade** — tranque o tier (Very Low/Low/Medium/High) antes de refinar.
- Tipo de tipografia é seguido "mais solto" — refine com a mask sobre o bloco de texto.
- 2K nativo; imagens grandes demais são reduzidas (Auto mantém proporção).
- Mask: max 25MB (JPEG/PNG/WEBP). Request com mask aceita **no máximo 3 outras imagens-fonte** (1 fonte + mask + 3 refs).

## 6. Sem API 4.5 — fallbacks HOSTED (não prometer checkpoint local)

- O **4.0 regenera a imagem inteira** em toda chamada de geração — mas a API hospedada TEM edição: **`v1/edit`** (até 10 imagens, `seed` presente) e **`v2 remix` do 4.0** (upload de imagem + prompt lido como instrução de edição).
- **Máscara/inpaint hosted:** documentada no **generate do 4.5** (parâmetro `mask`); não documentada no v1/edit.
- **Não prometa checkpoint local de "Ideogram 3.0 Edit" sem verificação** — pesos locais confirmados do Ideogram: só 4.0 T2I. Para 4.0 local, a edição realista é inpainting genérico no ComfyUI (mask + prompt da região), não um "3.0 Edit" dedicado.
- Roteamento: "trocar só o céu/placa mantendo o resto" → 4.5 High+mask (API) · sem API 4.5 → v1/edit ou remix 4.0 (hosted) · "recompor a cena com controle" → 4.0/4.5 JSON loop.
## 7. Anti-padrões de edição

- "Remove the watermark" → tende a re-renderizar; "clean white background" + reroll; idealmente gere a versão limpa direto.
- Múltiplas mudanças num turno (4.5) → passes separados; no Krea Annotate, múltiplas regiões numa passada são suportadas.
- Re-descrever elementos estáveis → repintura.
- Substituir texto com mask apertada → traços sobrando (margem!).
- Editar em Regular esperando preservação → use High.
