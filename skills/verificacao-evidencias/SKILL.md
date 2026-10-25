---
name: verificacao-evidencias
description: "Use antes de declarar trabalho concluído, teste aprovado, PR revisado, deploy realizado ou incidente resolvido; requer evidência atual."
---
# Verificação antes de declarar sucesso

## Regra
**Nenhuma afirmação de conclusão sem evidência adequada ao que se afirma.**

## Processo
1. Escreva a afirmação pretendida: “teste passou”, “bug corrigido”, “PR aberto”, “serviço saudável”.
2. Defina a prova adequada: comando e exit code/testes, diff, GitHub URL/SHA, comparação de sintoma, healthcheck e logs, respectivamente.
3. Execute/verifique a prova atual **se ferramenta e autorização permitirem**.
4. Leia resultado completo pertinente, falhas e escopo testado; compare com aceite.
5. Declare apenas o nível de evidência suportado, com local, commit/ambiente e limitações.
6. Quando houver erro ou ausência de executor, use `FALHOU`, `NÃO EXECUTADO` ou `INCONCLUSIVO`, nunca “deve estar bom”.

## Exemplos
- Linter verde ≠ testes passando.
- PR criado ≠ review aprovado.
- Diff revisado estaticamente ≠ código executado.
- Deploy iniciado ≠ release concluído.
- Healthcheck HTTP 200 ≠ resultado correto em todo o fluxo.
- “Agente confirmou” ≠ mudança inspecionada.
- Backups existentes ≠ restauração comprovada.

## Saída
Tabela pequena `afirmação | prova | resultado | limitação` quando houver várias. Para mudança trivial, uma frase pode bastar.

## Proibições
Inventar comandos, métricas, prints, logs ou resultados. Testes realizados em commit anterior não validam um diff novo.
