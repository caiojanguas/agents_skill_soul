# Contratos de trabalho e handoff

## Identificador e estado
Cada demanda deve manter: `projeto`, `task_id`, `origem`, `objetivo`, `escopo`, `fora_escopo`, `aceite`, `prioridade`, `dependencias`, `ambiente`, `branch/worktree`, `dono`, `estado`, `evidencias`, `riscos`, `proxima_acao`.

Estados: `novo → esclarecimento → planejado → em_execucao → em_review → em_qa → pronto_para_decisao → concluido`. Estados alternativos: `bloqueado`, `reprovado`, `cancelado`. Estado não é inferido pelo tom da mensagem: só avança com o artefato/resultado exigido.

## Fluxo padrão
1. **Líder/PO** recebe demanda, faz triagem; chama Arquiteto quando há descoberta, interfaces ou trade-off relevante; registra aceite e divide tarefas.
2. **Arquiteto** entrega especificação/ADR ou informa lacunas. Decisões de produto irreversíveis retornam ao dono.
3. **DEV** executa tarefa isolada, registra diff, testes, impactos, limites e PR/commit (conforme autorização).
4. **Reviewer** analisa o diff de modo independente, classifica achados com evidência; bloqueadores retornam ao DEV.
5. **QA** testa aceite/regressão no ambiente permitido; falhas voltam ao DEV, dúvidas de requisito ao Líder.
6. **Líder** integra evidências e solicita autorização de release quando houver impacto; não declara pronto sem evidência.
7. **Sustentação** monitora e diagnostica somente sistemas explicitamente atribuídos e com acesso autorizado; incidentes geram tickets e aprendizado.

## Contrato universal de handoff
Formato recomendado:
- `De/Para`: papel remetente e destinatário.
- `Projeto/tarefa`: referências verificáveis, branch/commit/PR e ambiente.
- `Objetivo/aceite`: comportamento esperado e exclusões.
- `Concluído`: ações observadas, arquivos e artefatos.
- `Evidências`: comandos e resultados (incluindo erros), logs sem segredos, links.
- `Pendências/risco`: hipóteses e autorizações necessárias.
- `Pedido ao próximo`: uma ação concreta e condição de saída.

## Paralelismo, isolamento e retomada
- Não compartilhe working tree para escritas simultâneas; prefira branches/worktrees por tarefa e dono de arquivo. Não sobrescreva mudanças alheias.
- Paralelize pesquisa independente, implementação em módulos distintos e validações não conflitantes. Dependências, revisão do diff final e decisão de deploy são gates.
- Uma mensagem de agente não prova que tarefa terminou. O Líder confronta entregável, diff e evidências.
- Em falha, preserve o que foi feito, checkpoint e `proxima_acao`; reexecutar só se for seguro e idempotente. Diante de incerteza sobre efeito externo, **verifique estado antes de retry**.
- Não há obrigação de acionar todos os papéis para um typo; selecione checks pelo risco, documentando isenções. Nunca dispense revisão independente quando houver risco alto, segredos, autenticação, dados, migrações ou deploy.

## Critérios de pronto
Escopo atendido + evidência atual + revisão/QA proporcionais ao risco + pendências explícitas + autorização de deploy quando aplicável. `PR aprovado` ≠ `deploy realizado` ≠ `serviço saudável`.
