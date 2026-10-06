# Instalação

Estrutura:
```
krea2-ideogram4-prompt-skill/
├── SKILL.md
├── references/
│   ├── model-facts.md
│   ├── krea2-architecture.md
│   ├── ideogram4-json.md
│   ├── editing.md
│   ├── typography.md
│   ├── reverse-prompting.md
│   ├── failure-repair.md
│   └── genre-presets.md
└── scripts/
    └── validate_ideogram4_json.py
```

## Kimi / Claude / Codex (pasta de skills do agente)
Copie a pasta inteira para o diretório de skills do seu agente (ex.: `~/.kimi/skills/`,
`~/.claude/skills/`, `.codex/skills/`). O SKILL.md é carregado sob demanda;
as referências são lidas lazy — mantenha os caminhos relativos.

## Uso do validador
```bash
python scripts/validate_ideogram4_json.py meu_prompt.json
```

## Manutenção
- Confira periodicamente: github.com/krea-ai/krea-2 (docs/prompting.md, docs/expansion.txt),
  docs.ideogram.ai, ideogram.ai/blog — parâmetros e schema mudam entre versões.
- O schema do Ideogram nesta skill é uma reconstrução da pesquisa; valide contra a doc
  oficial antes de usar em produção.
