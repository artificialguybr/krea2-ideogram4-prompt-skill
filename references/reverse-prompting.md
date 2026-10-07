# Reverse-prompting (image → prompt)

## 1. Quando usar

- Usuário enviou imagem e quer "o prompt disso" / recriar com variação / transplantar o estilo.
- Quer converter estilo de referência para outro modelo.

## 1b. Caminho nativo (Ideogram MCP)

O MCP oficial do Ideogram expõe `describe_image` — devolve o structured JSON da imagem (medium, paleta, luz, composição, grão). Fluxo "describe → extract → apply":
1. `describe_image` na(s) referência(s).
2. Sintetize uma **style recipe** compartilhada (a lógica visual comum, não a cópia).
3. Aplique a recipe a um sujeito novo via `generate_image` (NL + Magic Prompt) ou JSON direto.
4. `remix_image` para variações. A Ideogram publica uma skill oficial `/ideogram-prompt` (Claude Code) que empacota exatamente esse loop — boa referência de design.
5. O app Krea tem style refs one-click copiables na gallery — reverse-prompting social.

## 2. System prompt do analista (análise manual, ex.: só imagem, sem API)

```
Você é um diretor de arte especializado em engenharia reversa de imagens.
Desconstrua a imagem em relatório estruturado:

1. SUJEITO — hierarquia completa, atributos ligados ao sujeito certo, ação.
2. CÂMERA/COMPOSIÇÃO — ângulo, distância, lente provável, DOF, enquadramento.
3. AMBIENTE — camadas de profundidade, materiais.
4. LUZ — fonte, direção, qualidade, cor, sombras (dura/macia).
5. COR — paleta aproximada (hex), contraste.
6. ESTILO/MEDIUM — fotografia (filme/sensor/lente) OU arte (movimento, medium,
   superfície, linha). NUNCA ambos.
7. TEXTOS — transcreva TODO texto visível, exatamente (será o campo `text`).
8. TIPOGRAFIA — lettering, peso, material do texto.
9. ATRIBUTOS ÚNICOS — os 3–5 detalhes que mais identificam a imagem.
10. RESTRIÇÕES — o que NÃO pode mudar numa recriação.

Vocabulário de material > adjetivo. Sem "beautiful/stunning/masterpiece".
Descreva só o verificável; marque incertezas com "aprox.".
```

## 3. Da análise ao prompt

**Krea 2**: funda os itens em 1–2 parágrafos (K2-SCENE), MEDIUM PRIMEIRO. Textos entre aspas no lugar certo da frase.
**Ideogram**: mapeie direto para o JSON canônico — item 6 → `style_description` (photo XOR art_style + medium); 2–3 → `compositional_deconstruction` (background + elements com `type`/`desc`/`bbox`); 5 → `color_palette` MAIÚSCULA; 7–8 → elementos `type: "text"` com `text` literal.

**Variação controlada**: altere UMA dimensão (luz, paleta, ângulo, estilo); trave as demais.

## 4. Style recipe (formato curto reutilizável)

```
Medium: <...>
Palette: <3–5 hex ou nomes>
Lighting: <fonte+direção+qualidade>
Composition: <hierarquia do layout>
Texture: <grão/superfície/papel>
Signature: <o detalhe que quebra a formalidade>
```

Salve a recipe — ela é o "contrato" para regenerar o estilo em qualquer modelo.
