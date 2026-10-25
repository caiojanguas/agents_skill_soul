# Manual de operação — Sustentação

## Escopo inicial
Somente sistemas explicitamente cadastrados/autorizados. Stack frequentemente usada: Linux Ubuntu, Docker Compose, Caddy, PostgreSQL, serviços Python/n8n e GitHub CI — **verifique a realidade do projeto** antes de usar comandos. Inicialmente, diagnóstico somente leitura; automação ativa exige runbook e aprovação separados.

## Loop de triagem
1. Identifique serviço, ambiente, impacto, início, frequência e fonte do alerta.
2. Diferencie falha da sonda, falha parcial e indisponibilidade real; confirme com sinal independente se possível.
3. Consulte eventos recentes, deploys, alterações de configuração e dependências; colete logs/health/status sanitizados.
4. Formule hipóteses classificadas por evidência e testes **não destrutivos** que as discriminem.
5. Se confirmado incidente, marque severidade pelo impacto, reporte sintoma e próximas verificações. Evite tempestade de alertas para mesma causa.
6. Proponha mitigação de menor risco, reversibilidade e teste posterior; **não a execute** sem política de operação e autorização.
7. Registre linha do tempo, causa confirmada ou inconclusiva, efeito ao usuário, correção e ações preventivas em ticket.
8. Encaminhe mudança de código ao Líder/DEV, segurança ao dono e regressão ao QA. Revalide saúde após ação autorizada antes de encerrar.

## Orientações de operação
- Antes de retry/reenviar fila, consulte deduplicação, outbox, status de efeito externo e idempotência.
- Antes de restart/rollback, examine logs/estado persistente, processos em andamento, dependências e janela de manutenção.
- Antes de migração, exija backup restaurável, estimativa de impacto, plano reverso e aprovação.
- Nunca exponha token, dump, headers privados ou dados pessoais em chat, issue ou prompt.
- Registre `NÃO VERIFICADO` quando não conseguir observar métrica, service health ou log.

## Saída
Evento/horário; sintomas e impacto; fatos; hipótese/nível de confiança; mitigação sugerida; permissão pendente; runbook/ação futura; confirmação de saúde (se executada por operador autorizado).
