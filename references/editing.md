# Modos de EDIÇÃO — Krea (app + Identity Edit) × Ideogram (Canvas + 3.0 Edit)

## 1. Princípios universais de prompt de edição

1. **Descreva o RESULTADO, não a operação.** "She wears the black bodysuit" ✔ — "replace her dress with a bodysuit" ✘. O modelo deduz o que mudar.
2. **Nunca escreva a palavra "reference"** no prompt. Anexe a imagem e nomeie a coisa normalmente ("the black bodysuit"); falar em "referência" confunde o grounding.
3. **Uma mudança por instrução.** Encadeie edições em passes sucessivos.
4. **Não re-descreva o que deve ficar.** Preservação é o default; nomear cabelo/rua/cor de fundo só convida o modelo a repintá-los.
5. **Presente, terceira pessoa**: "She wears…", "The car is now red…" — combina com o jeito que o modelo foi treinado.
6. Se o resultado escorregar: ajuste os **dials** antes de inflar o prompt com mais palavras.

## 2. Krea app — Edit (Change Region / Annotate / Expand / Relight)

- Linguagem natural simples, zero sintaxe especial.
- **Annotate**: marque várias regiões, cada uma com prompt próprio (e até imagem própria), e gere **uma única vez** — evita artefatos de passes sequenciais.
- Crop/Expand: descreva o que preenche a área nova.
- Relight: descreva a nova luz (fonte+direção+qualidade), não o objeto.
- Ordem mental: selecionar → descrever resultado → gerar → avaliar 1 variável por vez.

## 3. Krea 2 Identity Edit (LoRA, app/ComfyUI) — re-stage, face swap, try-on

**Wiring (ComfyUI):**
- Fluxo base (RAW ou Turbo) → nó Krea2IdentityEdit (cond poz + cond neg) → sampler.
- **Cond negativa precisa da MESMA imagem com prompt vazio** ("keep the image"). Prompt vazio = preservar.
- Ordem fixa de inputs em cena+pessoa: **cena = imagem 1, pessoa = imagem 2**. Inverter degrada muito.
- Vocabulário de edição: "edit", "inpaint", "outpaint" (termos que o LoRA entende; "swap"/"replace" funcionam pior).

**Dials:**

| Dial | O que faz | Faixa útil |
|---|---|---|
| `grounding_px` | Quão literalmente o modelo prende na imagem | 384–768 (acima disso: "double picture") |
| `ref_boost` | Fidelidade da referência | ~4 = forte; >10 quebra remoções; <1 solta identidade |
| `ref_boost_a` / `ref_boost_b` | Força por imagem de referência | subir se a 2ª imagem for ignorada |
| steps | ~8 favorece composição; ~12+ favorece detalhe facial | 8–12 |

**Limitações honestas:**
- **2 pessoas juntas**: roupas se mantêm, mas rostos derivam um pro outro → encadear inserções de pessoa única.
- **>2MP**: duplicação/sangramento → gerar em ≤2MP (1–1.5MP) e upscale depois.
- **Remoção de objeto**: funciona mas não é confiável — às vezes re-renderiza em vez de deletar; reroll/rephrase; recipe Raw/CFG 3 ajuda.
- **Troca de roupa no corpo**: parcialmente confiável; cenário simples ajuda.
- Troubleshooting: "double picture" → baixar `grounding_px`; identidade escorregando → subir `ref_boost`; composição travada → subir steps; segunda ref ignorada → `ref_boost_b`.

**Template de instrução:**
```
She wears the black bodysuit.        ← resultado, 1 mudança
[anexar: imagem da pessoa, imagem da bodysuit]
grounding_px ~512 · ref_boost ~4 · 8–12 steps
```

## 4. Ideogram Canvas — Magic Fill (inpaint) & Extend (outpaint)

- Selecione a região; **ajuste a janela de geração** (dá pra zoomar e regenerar detalhe em alta resolução local).
- Prompt descreve **só a região editada**, no presente: "moss growing between the cobblestones, damp and overcast light".
- Extend: arraste a janela para o lado novo e descreva o que aparece; mantenha descrição de luz consistente com a imagem original.

## 5. Roteamento crítico: edição local preserva o resto?

- **Ideogram 4.0 regenera a imagem inteira** em toda chamada — mesmo com JSON editado, tudo fora do elemento tocado desloca.
- Para editar 1 região e preservar o resto: **Ideogram 3.0 Edit** (envie imagem + mask + prompt + seed).
- Regra da skill: usuário quer "trocar só o céu/fundamento/placa mantendo o resto igual" → 3.0 Edit. Quer "recompor/variar a cena com controle" → 4.0 JSON loop.

## 6. Anti-padrões de edição

- "Remove the watermark/logo" → o modelo tende a re-renderizar em vez de limpar; tente "clean white background" + reroll, e gere a versão limpa direto quando possível.
- Múltiplas mudanças numa frase ("change her dress to red AND make it night AND add rain") → faça em passes.
- Re-descrever elementos estáveis → repintura indesejada.
- Pedir "mantenha tudo igual e mude só X" com prompt longo → descreva só X.
