---
name: handoff
description: "Use em troca de responsabilidade, interrupção de sessão, mudança de agente, incidente ou conclusão de fase para preservar estado e próximos passos."
---
# Handoff curto, completo e retomável

## Quando usar
Passagem Líder→DEV, DEV→Reviewer, Reviewer→DEV, QA→Líder, Sustentação→Líder ou handoff após falha/interrupção.

## Procedimento
1. Identifique `projeto`, `task_id`, remetente, destinatário, branch/commit/PR, ambiente e autorização vigente.
2. Declare objetivo, aceite e exclusões **sem mudar conteúdo original**.
3. Registre trabalho realmente realizado (links, paths e comandos com resultados), não planos apresentados como fatos.
4. Diga o estado atual com semântica exata: `em_execucao`, `pronto_review`, `bloqueado`, `falhou`, etc.
5. Separe riscos confirmados, hipóteses e itens ainda não verificados.
6. Transmita uma próxima ação executável e como provar sua conclusão. Quando houver operação externa, informe idempotência/status e se é seguro repetir.
7. Sanitizar dados, suprimir credenciais e não espalhar contexto de outro projeto.

## Modelo
- `De → Para / projeto / task_id`
- `Objetivo e aceite`
- `Estado / artefatos`
- `Verificações e resultados`
- `Riscos / pendências / aprovações`
- `Próxima ação`

## Falhas
Sem acesso ao estado, não fabrique links, SHAs ou resultados. Indique `não verificado` e quem pode confirmar. Sem mecanismo de persistência, recomende registrar no issue/arquivo do projeto, não prometer memória durável do chat.
