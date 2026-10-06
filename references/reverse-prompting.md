# Reverse-prompting (image → prompt)

## 1. Quando usar

- Usuário enviou uma imagem e quer "o prompt disso".
- Quer recriar a imagem com variação controlada.
- Quer converter o estilo da imagem para outro modelo.

## 2. System prompt do analista (adaptação livre, pt-BR)

Use este system prompt para a etapa de análise:

```
Você é um diretor de arte especializado em engenharia reversa de imagens.
Ao receber uma imagem, desconstrua-a em um relatório estruturado com:

1. SUJEITO — hierarquia completa (principal → secundário), atributos ligados
   ao sujeito certo, ação, interações.
2. CÂMERA/COMPOSIÇÃO — ângulo, distância, lente provável, profundidade de
   campo, enquadramento, regra de terços/centralização.
3. AMBIENTE — camadas de profundidade (frente/meio/fundo), materiais.
4. LUZ — fonte, direção, qualidade, cor da luz, sombras (dura/macia).
5. COR — paleta aproximada (liste hex quando possível), relação de contraste.
6. ESTILO/MEDIUM — fotografia (filme/sensor/lente) OU arte (movimento,
   medium, superfície, qualidade de linha). NUNCA ambos.
7. TEXTOS — transcreva TODO texto visível, exatamente, com aspas.
8. TIPOGRAFIA — lettering, peso, material do texto.
9. ATRIBUTOS ÚNICOS — os 3–5 detalhes que mais identificam a imagem.
10. RESTRIÇÕES — o que NÃO pode mudar numa recriação.

Seja específico (vocabulário de material > adjetivo). Não use "beautiful",
"stunning", "masterpiece". Descreva apenas o que é verificável na imagem.
```

## 3. Da análise ao prompt

**Para Krea 2**: funda os itens 1–9 em 1–2 parágrafos densos de prosa (K2-SCENE, ver krea2-architecture.md). Textos do item 7 vão entre aspas no lugar certo da frase.

**Para Ideogram 4**: mapeie direto para o JSON (ideogram4-json.md):
- itens 6 → `style_description` (photo XOR art_style)
- itens 2–3 → `compositional_destruction` (background + elements com bbox)
- itens 5 → `color_palette` (hex)
- itens 7–8 → `text` por elemento

**Variação controlada**: escolha exatamente UMA dimensão para alterar (luz, paleta, ângulo, estilo) e mantenha as outras travadas.

## 4. Notas

- Não invente detalhes que não estão na imagem; marque incertezas como "aprox.".
- Para mood/atmosphere, descreva o mecanismo ("haze from backlight", "grain from high ISO") em vez do sentimento.
- O repositório oficial krea-ai/krea-2 (docs/expansion.txt) e a página do Krea-2-Turbo no Hugging Face publicam system prompts de expansão/reverse — bons referenciais de tom, mas escreva o seu próprio em vez de copiar.
