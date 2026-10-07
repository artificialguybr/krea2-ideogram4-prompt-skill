# Instalação

Estrutura:
```
krea2-ideogram4-prompt-skill/
├── SKILL.md
├── references/
│   ├── model-facts.md          (Krea 2 variantes/sliders · Ideogram 4.0/4.5)
│   ├── krea2-architecture.md   (medium primeiro · K2-SCENE · sliders · workflow)
│   ├── ideogram4-json.md       (schema canônico ideogram-oss/ideogram4)
│   ├── editing.md              (Krea Edit/Identity · Canvas · 4.5 Precise Edit · 3.0 Edit fallback)
│   ├── typography.md
│   ├── reverse-prompting.md    (inclui fluxo MCP describe_image oficial)
│   ├── failure-repair.md
│   └── genre-presets.md
└── scripts/
    └── validate_ideogram4_json.py
```

## Instalação
Copie a pasta inteira para o diretório de skills do seu agente (`~/.kimi/skills/`, `~/.claude/skills/`, `.codex/skills/`). SKILL.md carrega sob demanda; referências são lidas lazy — mantenha caminhos relativos.

## Validador
```bash
python scripts/validate_ideogram4_json.py meu_prompt.json
```

## Complementos oficiais conhecidos
- Ideogram publica a skill `/ideogram-prompt` (Claude Code) — `curl -fLo ~/.claude/skills/ideogram-prompt/SKILL.md --create-dirs https://ideogram.ai/skills/ideogram-prompt/SKILL.md` (fluxo MCP: describe → extract → apply).
- `krea2-prompt-suite` (GitHub AI-KSK) — modos avançados (evaluate, node-system, batch) compatíveis com esta skill.
- MCP oficial do Ideogram: `generate_image`, `describe_image`, `remix_image`.

## Manutenção
- Fontes primárias: github.com/ideogram-oss/ideogram4 (docs/prompting.md — schema canônico), github.com/krea-ai/krea-2 (docs/prompting.md, docs/expansion.txt), krea.ai/docs/changelog, docs.ideogram.ai, ideogram.ai/blog.
- Schema e parâmetros mudam entre versões — o validator cobre o schema 4.0/4.5 conhecido até out/2026.

## Changelog da skill
- v4 (out/2026, revisão pós-validação): corrige seed por endpoint (v2 do 4.0 ACEITA seed; negative_prompt não existe em 4.0/4.5; v1 legado = confirmar na doc); resoluções por checkpoint conforme README oficial (RAW ~1K, Turbo 1K–2K); documenta remix do 4.0 (v2) e v1/edit como fallbacks hosted; marca Identity Edit como adapter não-oficial (exige ComfyUI-Krea2Edit); adiciona matriz de interfaces; "uma mudança por turno" vira estratégia de debug (Krea Annotate aceita múltiplas regiões); tetos de 80/4 palavras e medium-first viram conselhos condicionais; remove INSTALL.md do contexto de leitura da skill.
- v3 (out/2026): corrige specs do Krea 2 (12.9B, RAW = não destilado); tabela completa das 9 trigger phrases de LoRA; diagnóstico "mushy = duas ações/zero luz"; aprofunda Canvas (prompt de cena inteira vs. uma-mudança do 4.5, orçamento fixo de pixels, upscale-first, padrão "On the left/On the right", Describe, truque texto→Remix→Fill, Magic Prompt OFF); limites de API do 4.5 (mask ≤25MB, ≤3 refs com mask); notas de plataforma Krea (units, Krea 1 vs 2, Auto router, Enhance/Edit, licença Community).
- v2 (out/2026): corrige schema do Ideogram para o canônico (`type`/`desc`, `medium`, hex maiúsculo, ordens de chave por caminho photo/art_style, `text` literal); adiciona Ideogram 4.5 (Precise Edit, masks, multi-turn, seed, tiers), Generative Sliders do Krea 2, regra "medium primeiro", workflow Turbo→Medium, roteamento de edição atualizado.
- v1: versão inicial.
