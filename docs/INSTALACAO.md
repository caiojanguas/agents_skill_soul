# Instalação e adaptação ao OpenMausBot

## Escolha do caminho
**Opção A — com CLI disponível na VPS:** o manifesto `openmausbot/team.yaml` descreve equipe, Chief of Staff, instruções e skills em arquivos. Trabalhe sobre checkout local **confiável** desse repositório, não apenas a URL GitHub. O comando do projeto upstream é `openmausbot team apply`, sujeito à versão instalada.

1. Confira a versão e ajuda do `openmausbot` presente no servidor/container; não confunda app desktop com CLI disponibilizada no PATH.
2. Coloque este repositório no filesystem acessível ao comando, com os caminhos relativos preservados. Faça backup/export da configuração existente pelo mecanismo da sua versão antes de aplicar.
3. Verifique na UI que só existe o Chief desejado e que não há nomes duplicados; o manifesto **não** usa `prune`.
4. Execute a partir da raiz: `openmausbot team apply openmausbot/team.yaml --dry-run`. Analise cada criação/alteração.
5. Se for seguro, execute `openmausbot team apply openmausbot/team.yaml`. Isso **modifica bots na instância**, não faça no escuro.
6. Na UI, confirme nomes, time, souls, skills ligadas, `Ask`, provedores, computador/working folder e ferramentas. Habilite somente conexões exigidas pelo trabalho.
7. Execute as avaliações em `docs/AVALIACAO.md` com projeto não produtivo e verifique as permissões **na prática** antes de ampliar autonomia.

**Opção B — sem CLI compatível:** crie os seis bots na interface, marque apenas o Líder como Chief of Staff, copie cada `agentes/<papel>/SOUL.md` nas instruções permanentes, use `governanca/BRIEF.md` como instruções compartilhadas do time e adicione as `SKILL.md` correspondentes na área Skills, ativando-as por papel. `AGENTS.md` é manual complementar, não é lido automaticamente por essa ação.

## Precauções da versão
- Documentação upstream consultada: [CLI / team apply](https://github.com/milind-soni/OpenMausBot/blob/main/docs/headless-cli.md), [níveis de aprovação](https://github.com/milind-soni/OpenMausBot/blob/main/docs/approval-levels.md), [compartilhamento](https://github.com/milind-soni/OpenMausBot/blob/main/docs/team-sharing.md).
- Manifesto omite modelos, `cwd`, engines/chaves e dispositivos: são dependentes do host, seus caminhos e seus provedores; não configurem valores fictícios.
- O upstream informa que novas contas podem iniciar com `Full access`; o YAML fixa `approval: ask`, mas **confirme no bot e em delegações**. O nível do Chief pode se propagar. Proteger produção na infraestrutura continua necessário.
- As skills de um pacote exportado podem vir desligadas; `team apply` permite `enabled: true` no manifesto, mas só a instância efetiva confirma resultado.
- Nome do perfil, room e bot são identidades no runtime. Se já existem bots com o mesmo nome, `team apply` pode atualizá-los — examine o dry-run.
- O `--dry-run` não comprova que o modelo seguirá as instruções; só antecipa alterações na configuração.
- Arquivo YAML declarativo é distinto do formato Markdown de distribuição por Template/Import. Não assuma que são intercambiáveis.

## Agentes por projeto
Cada repositório de aplicação define seu próprio `AGENTS.md` com stack detectada, comandos reais de build/teste, arquitetura atual, interfaces, convenções, ambientes, definições de pronto, pastas vedadas e acessos permitidos. **Não substitua esses fatos com defaults da biblioteca.**

Antes do primeiro trabalho de cada sessão, o bot deve ler esse contexto. Quando o OpenMaus não montar automaticamente arquivos auxiliares de papéis, mande-os como contexto ou inclua no workspace acessível.

## Não executar automaticamente
Este pacote não cria cron, monitoramento, backups, GitHub secrets, deploys, tokens, webhooks nem acesso por SSH. Automação de sustentação e permissões de escrita em produção exigem desenho e aprovação separados.

## V2 — scripts e Black não entram automaticamente no bot
O compartilhamento padrão de skills distribui texto `SKILL.md`, mas **não** os executáveis auxiliares. Para executar `tools/agentkit.py` e Black, disponibilize uma cópia confiável deste repositório no computador/workspace do bot (sem dar acesso amplo à produção) e instale o ambiente Python correto. Ver `docs/FERRAMENTAS_EXECUTAVEIS.md`. Não habilite `full access` só para rodar formatação.
