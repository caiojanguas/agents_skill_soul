# Segurança, limites e autorização

## Três camadas distintas
1. **Instrução**: papéis e skills orientam o comportamento.
2. **Ferramenta/runtime**: permissões de shell, GitHub, apps, computador e aprovações realmente restringem ações.
3. **Infraestrutura**: credenciais mínimas, isolamento de ambientes, backups e auditoria restringem danos.

Uma camada não substitui outra. No OpenMausBot, permissões de Chief of Staff podem afetar tarefas delegadas: teste a herança antes de habilitar níveis superiores a Ask; uma instrução escrita não é sandbox.

## Ações permitidas e gates sugeridos
- **Leitura** de código, logs sanitizados, métricas e documentação: conforme permissões existentes; nunca faça varredura fora do escopo autorizado.
- **Escrita em branch de trabalho**, testes locais e PR: liberável por tarefa quando houver ambiente isolado e revisão.
- **Merge, push direto à main, release, alterar CI/proteções, novo secret, envio externo, custo contratado, deploy, restart, rollback e escala**: exigem política operacional e aprovação humana explícita antes da ação, salvo automação previamente aprovada, limitada, testada e auditável.
- **Migração, truncamento, DROP, exclusão, alteração de backup, credenciais ou acesso, exposição pública de serviço**: sempre classificar como alto risco; ter backup/restauração e autorização específica.
- Não use `--force`, `rm -rf`, `git reset --hard`, `docker system prune`, `kubectl delete` ou equivalentes sobre ativos reais sem autorização explícita e entendimento do alvo.
- Ações externas não idempotentes (enviar, publicar, pagar, excluir) exigem verificar se já ocorreram antes de repetir.

## Dados e privacidade
- Não copie segredos, dados de clientes, pessoais, de produção ou dumps para prompt, PR público, logs, tickets ou outro agente sem finalidade e autorização.
- Minimizar dados, mascarar logs e seguir políticas do projeto e legislação aplicável. Não alegar conformidade jurídica automática.
- O próprio `agents_skill_soul` é **público**: não armazenar valores sensíveis nem detalhamento de acesso à VPS.

## Incidentes
A primeira resposta é contenção e evidência, **não** ação destrutiva. Somente execute remediação automática previamente definida em runbook, com escopo, rollback e limite verificados. Fora disso: diagnostique, proponha e peça aprovação.

## Preparação do runtime
- Configure acesso à VPS via rede privada; sem credenciais no YAML.
- Nível inicial sugerido para todos os bots: `ask`. Revisar na UI antes de delegar. Evite `full` no Chief sem entender herança.
- Desative acesso a computador, MCP e apps que o papel não requer, por configuração real. O manifesto desta versão não presume os meios disponíveis no servidor.
