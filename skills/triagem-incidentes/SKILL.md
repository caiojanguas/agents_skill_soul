---
name: triagem-incidentes
description: "Use em alertas de serviço, falhas operacionais e suspeitas de indisponibilidade para coletar evidências, reduzir risco e decidir escalonamento."
---
# Triagem de incidentes em produção

## Entrada
Serviço/ambiente autorizado, sinal, timestamp, impacto aparente, histórico, acesso somente leitura ou runbook aprovado.

## Procedimento
1. Determine o que falhou, para quem, desde quando e se o alerta é reproduzível. Distinga alarme falso, falha parcial e incidente ativo.
2. Cheque saúde e dependências com leitura permitida: status container, logs filtrados, healthchecks, recursos, últimos commits/deploys, DB e rede. Não publique segredos.
3. Defina severidade por impacto real; registre linha do tempo.
4. Identifique hipóteses e teste menos invasivo que as diferencie. Não atire restart ou rollback sem contexto.
5. Proponha mitigação e pré-condições: idempotência, backup e recuperação, efeitos em dados, reversibilidade, observabilidade e janela. Execute somente operação coberta por autorização/runbook.
6. Após mitigação autorizada, valide sintoma, serviço, dependências e consistência de dados; registre resultado. Caso contrário, indique `aguardando aprovação`.
7. Faça handoff ao Líder com causa confirmada/provável, ação preventiva, ticket e links. Evite incidentes duplicados/alert storm.

## Estados
`EM INVESTIGAÇÃO`, `INCIDENTE CONFIRMADO`, `MITIGAÇÃO PROPOSTA`, `AGUARDANDO APROVAÇÃO`, `RECUPERADO E VERIFICADO`, `INCONCLUSIVO`.

## Red flags
Job que envia Telegram/e-mail/pagamento pode ter efeito externo antes do crash; não reenvie sem rastrear outbox/deduplicação. Banco sem backup restaurável; não migre. Logs com segredo; sanitize.

## Saída
Resumo de impacto, evidência, hipótese, próxima ação segura, aprovação exigida e responsável. Sem metas MTTR inventadas.
