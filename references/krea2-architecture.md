# Arquitetura de prompt — Krea 2

## 1. Filosofia

Krea 2 é um modelo "direção de arte em prosa". O prompt ideal é um **parágrafo denso e legível**, não uma lista de tags. Escreva como se estivesse dirigindo uma equipe de arte: sujeito, ação, cenário, luz, mood, referência estética, notas de composição.

## 2. Esqueleto K2-SCENE (usar só os módulos relevantes)

```
[Medium]              watercolor illustration / 35mm photograph / 3D render / risograph print…
[Subject hierarchy]   <sujeito principal> <atributos ligados a ele por pronome/aposto> <ação>
[Appearance]          idade, etnia, cabelo, roupa (texturas!), marcas
[Pose/interaction]    o que faz, com o quê, mão em quê
[Camera/composition]  ângulo, distância, lente, profundidade de campo, enquadramento
[Environment/spatial] cenário + 2–3 camadas de profundidade (frente/meio/fundo)
[Lighting]            FONTE + DIREÇÃO + QUALIDADE (o atributo mais sensível do modelo)
[Color system]        texturas/materiais nomeados > adjetivos de cor
[Style/production]    referência estética legível por humano ("in the style of a 1980s field guide plate")
[Typography/positive constraints]  texto entre aspas; exclusões como instrução positiva
```

Regra de concordância: cada atributo colado ao sujeito que ele descreve. "the woman wearing the red coat" — não solte "red coat" no fim do parágrafo.

## 3. Dois regimes de comprimento

| Regime | Como | Quando |
|---|---|---|
| **Exploração** | 1 frase vaga de propósito: "a cat riding a bicycle" | Rodadas iniciais como pesquisa de direção; varrer 2–3 resultados e escolher universo |
| **Controle** | 1–2 parágrafos densos, gramática completa | Briefing fechado, trabalho de cliente, composição específica |

Não existe meio-termo útil: ou vagueie de propósito, ou controle de propósito.

## 4. Iluminação — fórmula

`[fonte] + [direção] + [qualidade]` — exemplos:
- "low golden sun through a window from camera-left, soft falloff"
- "single soft key light from the upper left, gentle shadow wrap"
- "flat overcast daylight, minimal shadow"
- "practical neon from behind, hazy bloom"

## 5. Style Reference (hosted)

- Até 4 imagens de referência, slider 0–100% cada.
- Escala prática: **20%** = sutil ("cheiro" do estilo sobre foto real) · **50%** = equilibrado · **80%** = referência domina · **>80–90%** = o estilo sobrescreve o SUJEITO (quebra).
- Quanto mais referências, maior a chance de blend inesperado: 1 referência forte costuma vencer 4 medianas.
- Prompt acompanha: descreva o SUJEITO/CONTEÚDO e deixe a referência carregar o estilo — não descreva o estilo no prompt E na referência (briga de condicionamento).

## 6. Moodboard

- Sem limite de imagens; clustering + LLM extrai *taste profile* (keywords + avoids).
- Use prompt mínimo ("a frog") e deixe o board definir universo, atitude e anti-exemplos (avoids) — depois aplique "avoids" como positive constraints nas próximas gerações.

## 7. LoRAs oficiais (trigger phrases)

- Cada LoRA tem uma **trigger phrase** que frequentemente não tem relação com o nome do arquivo (ex.: LoRA "Darkbrush" → trigger `monochrome ink wash style`; "Softwatercolor" → `art deco watercolor style`). Sempre confira a trigger no card do LoRA.
- No prompt, fale do **CONTEÚDO**, não do estilo — deixe o LoRA carregar o estilo. Prompt descrevendo o mesmo estilo do LoRA luta com o LoRA.
- Medium tende a render melhor estilos artísticos; Large para fotorrealismo/raw.

## 8. Anti-padrões (detalhes em failure-repair.md)

- Tags soltas e pesos `(x:1.3)`; adjetivos vazios ("beautiful", "modern"); negative prompt carregado; texto sem aspas; descrição de estilo redundante com referência anexada.
