---
name: revisao-risco
description: "Use para code review independente de PR/commit, com foco em riscos demonstráveis, falhas silenciosas, contratos e cobertura dos testes."
---
# Revisão orientada a risco

## Preparação
Confirme PR/commit, base/head, ticket, aceite e arquivos tocados. Se revisão limitada, diga o limite antes do parecer.

## Passos
1. Compreenda intenção e contrato anterior. Veja diff e chamadas adjacentes necessárias para julgar o comportamento.
2. Priorize correção, auth, dados, segredos, privacidade, concorrência, timeout, retry, regressão e compatibilidade. Veja mensagens/erros sem vazamento de informação.
3. Inspecione falhas **silenciosas**: `except: pass`, fallback para valor sucesso, `continue` que perde evento, logging sem erro, outbox não atômica, ack antes da persistência, retries sem deduplicação.
4. Avalie teste que prova a falha e aceite; cobertura percentual e mocks isolados podem ocultar risco de integração.
5. Meça complexidade contra mínimo correto: removível sem perder requisito? Evite pedir novos padrões em todo PR.
6. Registre só achados verificáveis/hipóteses úteis, com posição, cenário, impacto, prioridade, sugestão mínima e modo de confirmar.
7. Decisão: `APROVADO`, `APROVADO COM RESSALVAS`, `AJUSTES NECESSÁRIOS` ou `BLOQUEADO SEM VISIBILIDADE`. Não substitui QA.

## Critério de severidade
- **Bloqueador:** quebra provável crítica, perda/corrupção, bypass de autorização, exposição sensível, mudança incompatível ou ausência de evidência essencial.
- **Importante:** erro significativo com caminho plausível ou teste crítico ausente.
- **Sugestão:** clareza, otimização ou melhoria não necessária para aceite.

## Saída
Resumo do diff inspecionado + achados completos + risco residual + decisão fundamentada e próximos passos.

## Falso positivo
Se não há prova de problema, faça pergunta de investigação ou marque hipótese; não arme bloqueio estilístico.
