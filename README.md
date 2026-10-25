# agents_skill_soul

Biblioteca em português brasileiro para uma equipe de engenharia de software com **seis papéis**, orquestrada no OpenMausBot e reutilizável em outros harnesses.

## Equipe
| Papel | Decide / entrega | Não faz |
| --- | --- | --- |
| Líder técnico / PO | Prioridades, tickets, delegação, integração e status | Fingir execução ou substituir revisão independente |
| Arquiteto | Entrevista, requisitos, alternativas, ADR e desenho enxuto | Codificar por padrão ou decidir escopo de produto pelo dono |
| DEV | Menor implementação completa, manutenção e testes próximos do código | Expandir escopo e fazer deploy unilateral |
| Code Reviewer | Revisão independente de riscos do diff e parecer | Aprovar o próprio trabalho ou inventar evidência |
| QA | Cenários de aceite, testes, regressão e parecer de release | Confundir lint com teste ou aprovar sem execução |
| Sustentação | Diagnóstico, observabilidade, incidentes e runbooks | Fazer mudanças destrutivas sem autorização |

Comece por [Instalação no OpenMaus](docs/INSTALACAO.md), [Contrato entre agentes](governanca/CONTRATOS.md), [Segurança](governanca/SEGURANCA.md) e [Fontes e decisões](governanca/FONTES.md).

## Estrutura
- `agentes/<papel>/SOUL.md`: identidade e decisões fundamentais, pronta para as instruções permanentes do bot;
- `agentes/<papel>/AGENTS.md`: manual de execução e saída do papel, para consulta/uso em projetos;
- `skills/<slug>/SKILL.md`: procedimentos autocontidos, com YAML de descoberta e sem dependências executáveis ocultas;
- `governanca/`: regras transversais e contratos de handoff;
- `openmausbot/team.yaml`: manifesto declarativo v1 para `openmausbot team apply`;
- `docs/AVALIACAO.md`: testes de aceitação antes do uso real.

## Premissas
Português nas interações e artefatos; nomes técnicos e interfaces de código mantidos no idioma da ferramenta. Não existe stack compulsória para todos os projetos: Python, PostgreSQL, Docker e GitHub Actions são preferências usuais, a verificar em cada repositório. Sem fluxos de deploy/restart/migração automáticos no pacote.

**Importante:** arquivos `AGENTS.md` e `SOUL.md` não são mágicos: o OpenMaus carrega `soul`, `brief` e `skills` indicados no manifesto; os `AGENTS.md` específicos devem ser lidos explicitamente quando houver workspace disponível. Permissões, acesso SSH, ferramentas, tarefas programadas e delegação real dependem do runtime.

O arquivo `arquiteto_senior.md` da raiz foi preservado como **legado de referência**. Ele menciona scripts e referências que não estão neste repositório: não os trate como ferramentas instaladas.

## Estado
Versão inicial para revisão. Nenhum teste contra a instância real da VPS foi realizado a partir desta biblioteca. Execute dry-run e avaliação antes de ativar rotinas ou permitir ações em produção.

## V2 — ferramentas executáveis e Black

A biblioteca agora contém `tools/agentkit.py`, testes unitários, contratos JSON, EditorConfig, `pyproject.toml` e GitHub Actions. Consulte [ferramentas executáveis](docs/FERRAMENTAS_EXECUTAVEIS.md) para comandos, limites e instalação. O Black é padrão de código **Python** (4 espaços, 88 colunas por padrão) nos novos projetos; para legados, adoção incremental sem refatoração massiva incidental. Não alcança linguagens não Python. Sem acesso real ao checkout e interpretador no OpenMaus, os scripts **não** rodam automaticamente.
