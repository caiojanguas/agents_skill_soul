# Proveniência, seleção e adaptações — 25/10/2026

## Base
O levantamento `LEVANTAMENTO-PERSONAS-E-SKILLS.md` enviado pelo usuário (pesquisa de Daimon/Hermes) orientou a triagem. Ele relata curadoria de milhares de repositórios, mas **não constitui execução ou auditoria** de todos eles. Os conteúdos finais são redação própria e seletiva. A seleção não é endosso nem certificação das fontes.

## Fontes priorizadas (e extrações conceituais)
| Fonte | Uso neste pacote | Limite/adaptação |
| --- | --- | --- |
| [Superpowers](https://github.com/obra/superpowers) | Entrevista incremental, plano, debug e verificação por evidência | Sem obrigar entrevista para pedido trivial, sem instalação de hooks |
| [oh-my-codex / deep-interview](https://github.com/Yeachan-Heo/oh-my-codex) | Perguntas de escopo, pressupostos e limiar de ambiguidades | Sem caminhos `.omx`, métricas heurísticas não se tornam certeza |
| [mattpocock/skills](https://github.com/mattpocock/skills) | Confrontar premissas, transformar intenção em trabalho e handoff | Sem publicar automaticamente tickets externos |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | Menor solução **completa**, reutilização e YAGNI | Nunca reduzir validações de segurança ou testes relevantes |
| [Agency Agents](https://github.com/msitarzewski/agency-agents) | Minimal Change, Reviewer, Multi-Agent Architect, Privacy | Inspiração de papéis; linguagem personalizada, sem copiar biografias fictícias |
| [ECC](https://github.com/affaan-m/ECC) | Separação de responsabilidades, segurança e trabalho com evidência | Sem importar 71 agentes/hook global, métricas rígidas ou abstração obrigatória |
| [wshobson/agents](https://github.com/wshobson/agents) | Python, testes, observabilidade e incidentes | Skills específicas só quando stack presente |
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | Critérios de cargos, QA, sustentação, coordenação | Templates não concedem runtime nem tarefas reais |
| [Anthropic Claude Plugins](https://github.com/anthropics/claude-plugins-official) | Reviewer, falhas silenciosas e risco do diff | Parecer independente sem simular execução |
| [Anthropic Knowledge Work](https://github.com/anthropics/knowledge-work-plugins) | Desenho, incidentes, estratégia de testes | Não acoplar ao cliente Claude |
| [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | Objetivos, critérios de aceitação e recorte do MVP | PRD completo somente quando dimensão justificar |
| [OpenMausBot](https://github.com/milind-soni/OpenMausBot) | Team apply YAML, chief, skills, approvals, escalations | Interpretado pelo runtime instalado; verificar versão/CLI disponível |

Arquivos pontuais foram inspecionados em URLs pinadas no levantamento, como `python-pro`, `senior-architect`, `qa-expert`, `incident-responder`, `code-reviewer` e `verification-before-completion`. O conteúdo do pacote não inclui seus scripts ou assets. **Nenhum script de terceiros foi executado.**

## Licenças e responsabilidade
O levantamento aponta MIT em várias bibliotecas e Apache-2.0 em repositórios Anthropic. Antes de **copiar literalmente** código, scripts ou texto extenso, valide licença do arquivo e preserve avisos exigidos. Esta biblioteca parafraseia ideias gerais, acrescenta critérios próprios e referencia URLs; não incorpora scripts de terceiros.

## Exclusões intencionais
- Sem RAG, frontend, privacidade e multi-agent-architect como **agentes fixos**: são especializações/skills sob demanda.
- Sem Kubernetes/microserviços/Terraform por padrão: a operação atual é enxuta.
- Sem percentuais universais de cobertura, números de MTTR fantasiosos ou métricas sem baseline.
- Sem `to-spec` tratado como entrevistador e sem automação de publicação em issue tracker.
- Sem instalar ECC, Agency Agents, Superpowers ou Ponytail inteiro.
- Sem poder de deploy concedido por um prompt.

## Pendências empíricas
Validar na instalação real da VPS se `openmausbot team apply`, paths relativos, modelo, autorização e skills estão disponíveis e se a configuração vigente coincide com a documentação consultada (branch main da fonte em 25/10/2026).
