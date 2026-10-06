# Tipografia e renderização de texto

## 1. Regras universais

1. **Aspas duplas sempre**: "OPEN LATE", "Café Central".
2. **Cedo no prompt** — os dois modelos pesam mais o início. No Ideogram, o melhor lugar é a seção do sujeito principal.
3. **1–4 palavras renderizam mais limpo**; frases longas erram letra com frequência.
4. **Maiúsculas** tendem a render melhor que sentence case para display; sentence case funciona bem em corpo de texto curto (pôster, packaging).
5. Uma instância de texto por elemento; cada texto tem sua região/elemento próprio (no Ideogram: um objeto de `text` por elemento, com bbox).
6. Diga onde o texto mora: "arched over the door", "stamped across the chest", "small caption at the bottom".
7. Combine com material: "embossed in brass", "printed in cracked screenprint ink", "neon tubing".

## 2. Krea 2

- Aspas duplas + contexto físico do texto (placa, camiseta, letreiro neon).
- Se errar: re-rolar; encurtar o texto; trocar o material descrito. Não tente "corrigir letra por letra" no prompt — regenere.

## 3. Ideogram 4

- Melhor modelo da categoria para texto, mas **não é perfeito**: se a exatidão for obrigatória (print, branding), gere o fundo e coloque o texto real no Figma/Photoshop.
- No JSON: `text` com a string exata entre aspas + `bbox` + `art_style` (mesmo que "pareça foto de um pôster" — print/graphic = art_style).
- Muitos elementos de texto: um `elements[]` por texto, com suas paletas.
- Após gerar: leia a imagem em 100% e compare caractere a caractere; trate como rascunho até aprovação.

## 4. Logotipo / wordmark

- Peça como objeto físico quando quiser realismo: "brass sign with the word \"CENTRAL\" in art deco lettering".
- Para wordmark flat: estilo explícito de lettering ("custom hand-lettered wordmark, swashes") + paleta em hex.
- Gere 4 variantes mudando UM parâmetro (lettering, paleta, material) por rodada.

## 5. Falhas comuns e correções

| Falha | Correção |
|---|---|
| Letra trocada | Encurtar para ≤4 palavras; aspas; mover para início; regen |
| Texto borrado | Material mais definido ("die-cut vinyl", "engraved") |
| Texto em língua errada | Especificar idioma: "in Portuguese: \"…\"" |
| Múltiplos textos derretem | Separar em elementos/regiões distintos |
