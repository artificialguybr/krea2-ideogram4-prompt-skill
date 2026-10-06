# Falhas: diagnóstico e reparo

## 1. Guard rails — padrões proibidos na skill (converter automaticamente)

| Entrada do usuário | Converter para |
|---|---|
| `masterpiece, best quality, 8k, ultra detailed, sharp focus` | Descrição visual concreta do acabamento desejado |
| `(red dress:1.3)` | "the oxblood red dress" + restatement ("her crimson dress") |
| `negative prompt: deformed hands, extra fingers, watermark, text` | Positive constraints: "anatomically natural hands, two hands, clean background" |
| "make it beautiful/modern/artistic" | Mover/material/luz/era específicos |
| "no blur, high detail" | "crisp edge contrast, fine visible grain/texture" |

## 2. Tabela de sintoma → causa → reparo

| Sintoma | Causa provável | Reparo |
|---|---|---|
| Imagem desmonta ao usar peso | Weighting de embedding shoveia o conditioning inteiro | Remover pesos; restatement |
| Elementos do fim sumiram | Prompt >80–90 palavras (Ideogram) | Migrar para JSON |
| `photo`+`art_style` juntos | Fork de comportamento | Escolher um |
| Ideogram rejeita JSON | Schema inválido (ordem/snake_case) | Validar com scripts/validate_ideogram4_json.py |
| Texto erra letra | >4 palavras / texto tarde / sem aspas | typography.md |
| Style-ref engoliu o sujeito | Força >80–90% | 40–60% |
| Duas refs brigam | 4 refs medianas | 1 ref forte |
| Edit Identity: double picture | `grounding_px` >768 | Baixar para 384–512 |
| Edit Identity: rostos derretem (2 pessoas) | Deriva cruzada | Encadear inserções individuais |
| Edit Identity: remoção re-renderiza | Limitação conhecida | Reroll/rephrase; Raw/CFG 3 |
| Edit mudou imagem inteira (Ideogram) | 4.0 regenera tudo | Roteiar para 3.0 Edit |
| Plain text bloqueado (local) | Falso-positivo do filtro | Tentar JSON |
| Magic Prompt alterou meu texto | Expansão reescreve | Desligar (app) ou ir de JSON |
| Corpo cortado em 16:9 | Aspect inadequado | 2:3 / 9:16 |
| Composição genérica | Adjetivos vazios | Substantivos de material + luz nomeada |
| Inconsistência entre gerações | Espera de seed (não existe no 4.0) | JSON loop; criar "negative prompt" textual de variantes |

## 3. Fluxo de reparo (modo `repair` da skill)

1. Identifique o módulo quebrado (só ELE muda na próxima geração).
2. Reescreva só esse módulo com vocabulário mais específico.
3. Se for Krea 2: ajuste creativity (baixa) ou style-ref strength.
4. Se for Ideogram 4: edite um campo do JSON e reenvie.
5. Reporte: hipótese de causa → mudança aplicada → próxima variável se falhar de novo.
6. Após 2 falhas na mesma dimensão, mude de estratégia (ex.: prosa → JSON; ref → descrição; edit → regenerate).

## 4. Limitações honestas a comunicar ao usuário

- Ideogram 4: sem seed; texto longo imperfeito; edição local = 3.0 Edit.
- Krea 2 edit: remoção e outfit-swap parciais; >2MP duplica; 2 pessoas derivam.
- Nenhum dos dois reproduz pixel a pixel — consistência ≠ clonagem.
