# Falhas: diagnóstico e reparo

## 1. Guard rails — padrões proibidos (converter automaticamente)

| Entrada do usuário | Converter para |
|---|---|
| `masterpiece, best quality, 8k, ultra detailed, sharp focus` | Descrição visual concreta do acabamento |
| `(red dress:1.3)` | "the oxblood red dress" + restatement |
| `negative prompt: deformed hands, watermark, text` | Positive constraints ("anatomically natural hands, clean background, no other text") |
| "make it beautiful/modern/artistic" | Movimento/material/luz/era específicos |
| `{"object": ..., "description": ...}` (JSON Ideogram) | `{"type": "obj", "desc": ...}` — schema canônico |
| `#1b1b2f` / `#fff` (hex) | `#1B1B2F` — MAIÚSCULO, 6 dígitos |
| `"text": "\"HELLO\""` (aspas dentro do valor) | `"text": "HELLO"` — literal, sem aspas internas |

## 2. Tabela de sintoma → causa → reparo

| Sintoma | Causa provável | Reparo |
|---|---|---|
| Imagem desmonta ao usar peso | Weighting de embedding | Remover pesos; restatement |
| Elementos do fim sumiram | Prompt >80–90 palavras (Ideogram) | Migrar para JSON |
| `photo`+`art_style` juntos | Fork de comportamento | Escolher UM (strings, não objetos) |
| Warning do CaptionVerifier | Ordem de chaves / chave desconhecida | ideogram4-json §3 + validator |
| Hex rejeitado | Minúsculo ou shorthand | `#RRGGBB` maiúsculo |
| Plain text não funciona local | Pesos locais exigem JSON/Magic Prompt | ideogram4-json §1 |
| Ideogram bloqueia prompt benigno | Falso-positivo do safety filter em plain text | Tentar JSON |
| Case do texto alterado | Expand/Magic Prompt ON | Desligar (OFF mantém wording) |
| Letra trocada | >4 palavras / texto tarde / sem aspas | typography.md |
| Traços do texto antigo após troca | Mask sem margem | Mask cobrindo o bloco antigo inteiro + margem |
| Cor/textura deriva após edições | Edit Precision Regular | High (Auto size) |
| Edit redesenhou tudo | Regular / modelo errado | 4.5 High; ou edição hosted (v1/edit / remix 4.0) |
| Segunda ref de edição ignorada | ref_boost baixo (Krea) / sem ref (Ideogram) | `ref_boost_b` / 4.5 aceita até 4 refs |
| "Double picture" no Identity Edit | `grounding_px` >768 | 384–512 |
| Rostos derretem (2 pessoas, Krea) | Deriva cruzada | Encadear inserções individuais |
| Remoção re-renderiza | Limitação conhecida | Reroll; Raw/CFG 3; ou 4.5 High |
| Style-ref engoliu o sujeito | Strength >80–90% | 40–60% |
| Toda geração muda de estilo (Krea) | Sem medium | Medium primeiro |
| Stock photo genérica | "photorealistic" vago | Câmera + artefatos |
| Inconsistência entre gerações | Espera de seed (4.0 não tem) | JSON loop; 4.5 tem seed |
| Turbo ≠ Medium | Modelos diferentes | Esperado; settle no Turbo, render no Medium |
| Geração "mushy" (Krea) | Duas ações competindo / zero luz | Uma ação + fonte de luz (krea2-architecture §3) |
| Magic Fill alterou meu prompt otimizado | Magic Prompt ligado no Canvas | Desligar (docs oficiais recomendam OFF) |
| Rostos/mãos irreconhecíveis no Canvas | Janela grande = poucos pixels por rosto | Upscale 2× primeiro; janela < metade; re-fill |
| Texto borrado após truque de integração | Janela ~2× maior que o original | Minimizar janela; reduzir ref pela metade; upscale final |
| Prompt denso ignorado (Krea) | Aesthetic-first por design | `creativity` baixa; sliders; ou Ideogram JSON |
| Uso comercial em cliente | Licença | Krea 2 Community License: OK indivíduos/pequenos times; enterprise ~50+ assentos precisa acordo |

## 3. Fluxo de reparo (modo `repair` da skill)

1. Identifique o módulo quebrado (só ELE muda na próxima geração).
2. Reescreva só esse módulo com vocabulário mais específico.
3. Krea 2: ajuste sliders (intensity/complexity/movement) antes do texto; depois creativity; depois style-ref strength.
4. Ideogram: edite um campo do JSON e reenvie (4.0) ou faça um turno de Precise Edit (4.5).
5. Reporte: hipótese → mudança → próxima variável se falhar.
6. Após 2 falhas na mesma dimensão, troque de estratégia (prosa → JSON; ref → descrição; edit → regenerate; Regular → High).

## 4. Limitações honestas a comunicar

- Ideogram 4.0: v2 tem seed; texto longo imperfeito; edição = 4.5 (API, com mask) ou fallbacks hosted (v1/edit, remix).
- Ideogram 4.5: hosted (pesos "em breve"); tier de qualidade trava detalhes de tipografia; Regular redesenha tudo.
- Krea 2 edit: remoção/outfit-swap parciais; >2MP duplica; 2 pessoas derivam; texto longo é ponto fraco (use Ideogram/Seedream no app Krea).
- Nenhum dos dois reproduz pixel a pixel — consistência ≠ clonagem.
