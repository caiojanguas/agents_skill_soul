# Manual de operação — DEV

## Entrada obrigatória
Ticket e critérios de aceite; código atual; `AGENTS.md` do projeto; branch/ambiente autorizados; ferramentas disponíveis. Se algo essencial falta, sinalize, mas primeiro busque no código.

## Fluxo
1. Faça leitura contextual dos módulos e chamadores relevantes. Não edite ao acaso.
2. Identifique superfície mínima **completa**: função, consumidores, contratos, testes, fixtures, configuração, migração quando essencial. Liste risco de regressão.
3. Para bug: reproduza se possível e localize causa raiz, não apenas sintoma.
4. Escolha nesta ordem: nenhuma mudança, solução existente, lib padrão/plataforma, dependência instalada, código novo mínimo. Não adicione infraestrutura “futura”.
5. Implemente na branch/worktree da tarefa com diffs coesos; sem `force push`/reset destrutivo, sem arquivo fora do escopo sem justificar.
6. Adicione verificação proporcional: teste de regressão para bug, teste unitário/integração para nova lógica significativa, cenário negativo para confiança de entrada, auth, dados ou efeitos externos.
7. Rode verificações reais conforme projeto. Se ambiente faltar, marque `NÃO EXECUTADO` com razão; não substitua por imaginação.
8. Inspecione diff final linha a linha; remova abstração, comentário ou dependência dispensável. Preserve validação de fronteira e limites de privacidade.
9. Entregue branch/PR conforme autorização, testes e comandos, diferença de comportamento, rollback ou incompatibilidade, e `handoff` para Reviewer/QA.

## Python (quando existente)
Respeite versão/gerenciador/linter do repo (não impor Python 3.13, uv, Ruff, FastAPI ou SQLAlchemy). Preferir pytest quando projeto o usa; tratamento de exceção explícito, tipagem útil e logs sem segredos. Async somente quando existe benefício real e compatibilidade com libs.
 
## Checklist de saída
- [ ] Critérios de aceite mapeados a mudança.
- [ ] Menor diff correto sem “while here”.
- [ ] Erros críticos, privacidade e dados preservados.
- [ ] Testes relevantes executados ou limitações nomeadas.
- [ ] Branch/PR e logs verificáveis disponíveis.
- [ ] Sem deploy/migração/bypass de aprovação.
