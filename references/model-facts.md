# Fatos de modelo — Krea 2 × Ideogram 4.0/4.5

> Síntese da pesquisa (repo oficial ideogram-oss/ideogram4, blog técnico do Ideogram 4.0, docs/changelog Krea, guias runware/fuser/morphic). Confirme na doc oficial se algo parecer desatualizado.

## 1. Krea 2 — o que importa para prompting

- **12.9B** single-stream DiT (28 blocos, width 6144, GQA, learned output gate, per-head QK-norm, RoPE 3-eixos); encoder de texto **Qwen3-VL com agregação multi-camada**; VAE Qwen Image. Anunciado 12/mai/2026; relatório técnico 23/jun/2026.
- **RAW = checkpoint NÃO destilado** (para fine-tuning/LoRA e variedade); **Turbo = destilado** (8 passos, ~2s). **Resoluções por checkpoint (README oficial do krea-ai/krea-2): RAW treinado até ~1K; Turbo de 1K a 2K.** Não force 2K no RAW; no Turbo, iterar em 1K e renderizar em 2K é o workflow documentado; upscale continua sendo etapa separada.
- VRAM aproximada do Turbo: bf16 16 GB · fp8 10–12 GB · nvfp4 8 GB.
- Licença: **Krea 2 Community License** — uso comercial OK para indivíduos/pequenos times; cláusula enterprise (~50+ assentos exige acordo). Leia a licença para trabalho de cliente.
- **Aesthetic-first por design**: o modelo privilegia exploração estética sobre aderência literal (style refs/moodboards são o forte; composição precisa é o fraco). Briefing rígido → Ideogram JSON.
- **Prosa natural > tags.** O encoder entende gramática, possessivos, contagens e relações espaciais. Não dá boost por `masterpiece, 8k`.
- **Nomeie o MEDIUM primeiro** — é o maior knob de estilo: "35mm film photograph, fine grain" implica fotorealismo sem dizer "photorealistic"; "gouache painting" trava a superfície.
- Ordem = ênfase (front-loading). Restatement = ênfase. Textura/material > cor abstrata. Iluminação: fonte + direção + qualidade.
- Exclusões como instrução positiva; negative prompt carregado reduz qualidade.

## 2. Variantes Krea 2 (NÃO misturar parâmetros)

| Variante | Steps | CFG | Notas |
|---|---|---|---|
| **RAW** (open) | 52 | 3.5 | Não destilado; LoRA/pesquisa; lento em GPU mid-range; treinado até ~1K |
| **Turbo** (open) | 8 | 0 | ~2s; `mu 1.15`; negative pode não afetar; treinado de 1K a 2K |
| **krea-2/medium** (hosted/API) | — | — | Ilustração/artístico |
| **krea-2/large** (hosted/API) | — | — | Fotorrealismo |
| **krea-2/medium-turbo** (hosted/API) | — | — | Velocidade |

- **Generative Sliders (API, nas 3 variantes hosted)**: `intensity` (quão estilizado), `complexity` (densidade), `movement` (energia de pose/câmera) — inteiros **−100 a 100**, 0 = neutro; não mudam custo; combinam com style transfer e moodboards. Mais o modo **Creativity** (quanto o Krea expande/interpreta o prompt antes de gerar — análogo ao Magic Prompt do Ideogram).
- Workflow clássico: **acerte o prompt no Turbo** (barato/rápido), depois render no Medium/Large. Seed mantém a "faixa" entre variantes, mas o frame muda.
- Resolução nativa ~1024px (RAW); Turbo gera de 1K a 2K; 4K segue no roadmap → upscale é etapa separada (grátis até 2K no plano free). Aspectos: 1:1, 4:3, 3:4, 16:9, 9:16, 21:9, 3:2, 2:3. Defina o aspecto ANTES de gerar.
- **Krea 2 LoRAs**: criação disponível para todos; trigger phrases não-óbvias (verificar no card do LoRA). Prompt fala de CONTEÚDO, não de estilo.
- **Krea hospeda Ideogram 4.0 nativo** (2K, JSON prompts, ótimo texto) — alternativa quando o usuário não quer sair do app Krea.
- **Krea 1 (o modelo anterior)** ainda é a escolha para: fotorrealismo máximo, geração nativa até 4K, e o style transfer clássico com slider de influência. Krea 2 Turbo = iteração barata (2 units); Krea 1 = 8 units; ChatGPT Image pode chegar a 183 units — confira o custo no seletor.
- Plataforma Krea: 100 units/dia no free; seletor de modelo com **Auto** (roteia o prompt pro modelo adequado); aba **Enhance** (background removal, relighting, detail enhancement) e aba **Edit** (inpainting por região); botão "reuse parameters" para batch consistente.
- **Real-time canvas** (<50 ms) é pipeline separado do Krea 2 standard (~15 s) — não confunda os dois.
- Krea 2 ≠ FLUX.1 Krea [dev]. Comunidade mantém variantes do encoder Qwen3VL "abliterated" com menos recusas (workflow local, fora do escopo oficial).

## 3. Ideogram 4.0 — o que importa

- 9.3B single-stream DiT; encoder **Qwen3-VL-8B** (hidden states de 13 camadas); sampler Euler flow-matching com **CFG assimétrica** (uncond dropa tokens de texto); VAE frozen; 2.048 tokens de texto max; 256–2048px por lado.
- Treinado **exclusivamente em legendas JSON** — o JSON É o formato nativo; NL precisa passar pelo Magic Prompt.
- **Seed por geração de endpoint (não é fato do modelo):** o request **v1 legado** não expõe `seed`; o endpoint **v2 atual de geração do 4.0 ACEITA `seed`** (integer, opcional — confirmado na doc oficial). **`negative_prompt` não existe** no 4.0 v2 NEM no 4.5. Presets: `V4_QUALITY_48` (45 passos gw=7 + 3 polimento gw=3), `V4_DEFAULT_20`, `V4_TURBO_12`.
- **Edição por upload existe no 4.0 hosted:** `POST /v2/image/remix/ideogram-4` — imagem enviada + prompt lido como instrução de edição; `image_weight` 1–100; sem `image_ids` (upload direto do arquivo).
- Magic Prompt local (repo aberto): config `ideogram-4-v1` (grátis, server-side, precisa de API key Ideogram), `claude-opus-v1` / `claude-sonnet-v1` via OpenRouter; system prompts open-source no repo. (A expansão do repo aberto NÃO é idêntica à do produto hospedado.)
- **Pesos locais: plain text direto NÃO funciona** (e dispara falso-positivo de safety filter — gray screen "Image blocked"). Use Magic Prompt ou JSON.
- Transparência nativa: Background Remover gera alpha cutout (transparent generation listada para 4.0 e 3.0).

## 4. Ideogram 4.5 (30/set/2026) — o que muda

- Foco: **edição precisa multi-turn**. Reduz drift (shifts de pixel, mudança de cor, artefatos) entre turnos.
- **Edit Precision**: `High` = Precise Edit — pixels não alterados são copiados da fonte (na prática: ~91% byte-idêntico após 1 turno; 96% da metade inferior intacta após 3 turnos); `Regular` = redesenha o frame todo (0,3% idêntico após 1 turno) — mas é o único modo que muda o tamanho de saída. High e masked exigem **Image Size = Auto**.
- **Mask**: preto = área a editar, branco = preservar, MESMO WxH da imagem fonte, deve conter as duas cores. Ao substituir elemento, cubra-o inteiro **com margem**.
- Até **4 imagens de referência** na edição; consistência de personagem confirmada em testes.
- **Seed existe no 4.5** (repetível no mesmo tier de qualidade). 4 tiers: Very Low / Low / Medium / High. 2K nativo. API + plataforma; pesos abertos prometidos ("coming soon") — trate como hosted por ora.
- **Expand Prompt** (= Magic Prompt) com toggle: ON reescreve e adiciona cena (mudou CAIXA DE LETRAS em testes); OFF "keeps your wording and only converts it into a structured prompt" — use OFF para copy exata.
- Geração aceita o **mesmo JSON estruturado do 4.0**.
- Corrige texto garbled de imagens antigas em edição (testado em imagem ~10 meses mais velha).

## 6. Matriz de interfaces — nunca transferir schema entre superfícies

| Superfície | seed | negative_prompt | edição | máscara |
|---|---|---|---|---|
| Ideogram API v2 — 4.0 generate | **sim** | não | **remix** (upload de imagem) | não |
| Ideogram API v2 — 4.5 generate | **sim** | não | Precise Edit multi-turn | **sim** (`mask`) |
| Ideogram API v1 (legado) | confirmar na doc da versão | — | v1/edit (até 10 imagens) | não |
| App Ideogram / Canvas | n/a (UI) | — | Canvas (Magic Fill/Extend) | UI |
| App Krea | n/a (UI) | — | Edit / Annotate / Enhance | UI |
| ComfyUI/pesos abertos (Krea RAW/Turbo) | depende do workflow | depende (Turbo: CFG 0 ignora) | Identity Edit = adapter não-oficial | genérica (inpaint) |
| Providers terceiros (fal etc.) | **schema PRÓPRIO — sempre conferir antes** | idem | idem | idem |


Providers de terceiros expõem campos que a API direta não expõe (e vice-versa). Nada nesta tabela se transfere de uma linha para outra.

## 7. Tabela decisória — qual caminho de prompt?

| Precisa de… | Krea 2 | Ideogram 4.x |
|---|---|---|
| Exploração de estilo | Prompt curto + creativity alta | Expand/Magic Prompt ON |
| Fidelidade total ao briefing denso | Prosa densa (medium primeiro) | JSON estruturado |
| Posicionamento por coordenadas | — | JSON com `bbox` |
| Paleta exata (hex) | Materiais/cores nomeados | JSON `color_palette` (≤16 img, ≤5 elemento, MAIÚSCULO) |
| Identidade de pessoa em edição | Identity Edit LoRA **(não-oficial)** | 4.5 (até 4 refs) |
| Edição local preservando o resto | Annotate (regiões) | **4.5 Precise Edit High + mask** |
| Tipografia longa / logotipo | Aspas + material | JSON `text` por elemento; 4.5 com Expand OFF |
| Reprodutibilidade por seed | (depende da variante) | 4.0 v2 tem seed; 4.5 tem seed |
