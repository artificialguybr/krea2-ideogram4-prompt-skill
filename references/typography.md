# Tipografia e renderização de texto

## 1. Regras universais

1. **String literal exata** no campo `text` do JSON (as aspas envolvem o valor; não vão dentro). Em NL, aspas duplas + cedo no prompt.
2. **1–4 palavras renderizam mais limpo**; frases longas erram letra.
3. **Case**: maiúsculas render melhor para display; sentence case para corpo curto. **Atenção: Expand/Magic Prompt ligado pode alterar o case** — desligue quando o casing importar (Ideogram 4.5; app).
4. Um texto por elemento (`type: "text"` próprio com bbox/desc/paleta).
5. Diga onde o texto mora: "arched over the door", "stamped across the chest".
6. Material do texto: "embossed in brass", "neon tubing", "chalk on blackboard".
7. Para layouts limpos, feche com **"No other text."**

## 2. Krea 2

- Aspas duplas + contexto físico (placa, camiseta, letreiro).
- Errou? Re-roll; encurte; troque o material. Não corrija letra a letra.

## 3. Ideogram 4.x — o melhor da categoria, mas verifique

- 4.5 com Expand Prompt OFF: **31/31 linhas de texto corretas em 7 gerações de teste** (preços, travessões, apóstrofos) — mas typeface é seguido "mais solto" e deriva entre tiers: **tranque o tier** antes de refinar lettering.
- 4.5 corrige texto garbled em imagens antigas via edição (Precise Edit + mask sobre o bloco).
- Ainda assim: para print/branding exato, gere o fundo e coloque o texto real no Figma/PS.
- Após gerar: leia em 100% e compare caractere a caractere; trate como rascunho até aprovação.

## 4. Logotipo / wordmark

- Realismo: "brass sign with the word \"CENTRAL\" in art deco lettering".
- Flat: estilo de lettering explícito ("custom hand-lettered wordmark, swashes") + paleta hex.
- 4 variantes mudando UM parâmetro (lettering, paleta, material) por rodada.

## 5. Falhas comuns e correções

| Falha | Correção |
|---|---|
| Case trocado | Expand/Magic Prompt OFF; reescreva no case desejado |
| Letra trocada | ≤4 palavras; aspas; início do prompt; regen |
| Texto borrado | Material mais definido ("die-cut vinyl", "engraved") |
| Língua errada | "in Portuguese: \"…\"" |
| Textos derretem juntos | Um elemento `text` por texto, com bbox |
| Traços do texto antigo sobem após troca | Mask cobrindo o bloco antigo INTEIRO + margem (4.5 High) |
| Typeface não bate | Descreva de novo no mesmo tier; usar mask no bloco |
