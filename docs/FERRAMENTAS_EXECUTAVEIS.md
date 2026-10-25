# Ferramentas executáveis da equipe — V2

## O que é realmente determinístico
Esta biblioteca combina **instruções em Markdown** com `tools/agentkit.py`, um utilitário **Python com biblioteca padrão**, sem credenciais e sem necessidade de LLM. Os comandos validam estrutura e fatos locais; eles **não** atestam intenção de produto, qualidade semântica, autorização humana, autenticidade de artefatos ou estado de produção.

| Comando | Quem usa | Faz | Não faz |
| --- | --- | --- | --- |
| `inspect` | Arquiteto / DEV / Reviewer | Analisa AST de imports Python e relata ciclos locais, gera Mermaid opcional | Não detecta topologia real, imports dinâmicos, contratos distribuídos |
| `validate spec/plan/handoff/review/qa/ci` | Líder / todos | Confere chaves, tipos, estados, integridade de dependências, riscos declarados | Não confirma evidência de fato nem substitui julgamento |
| `scope` | DEV / Reviewer | Compara caminhos alterados em `base...HEAD` com padrões aprovados | Não inspeciona diff não comitado, nem prova correção |
| `black` | DEV / Reviewer / QA / Líder | Invoca Black em modo de checagem, por padrão sem editar | Não testa lógica, não formata outras linguagens |
| `gate` | Líder / QA | Bloqueia inconsistências entre review, QA e CI (SHA, estado, papéis distintos) | Nunca autoriza merge, deploy ou substitui verificação de CI real |

## Execução
A partir de checkout local confiável (com Python >=3.10 disponível):

```sh
python tools/agentkit.py inspect /caminho/projeto-python
python tools/agentkit.py inspect /caminho/projeto-python --mermaid
python tools/agentkit.py validate plan exemplos/plan.json
python tools/agentkit.py scope /caminho/projeto --base main --allow "src/*.py" --allow "tests/**"
python tools/agentkit.py black /caminho/projeto --changed-base main
python tools/agentkit.py gate exemplos
```

As evidências em `exemplos/` são **fictícias**, apenas para exercitar a estrutura. O status `READY_FOR_HUMAN_DECISION` nunca é autorização nem prova de que a CI referenciada foi executada de verdade. Não use exemplos no deploy.

**Black:** `python -m pip install -r requirements-dev.txt` instala a versão fixada para este repositório. Em cada projeto real, fixe Black em suas dependências de desenvolvimento e configure `[tool.black]` adequadamente. `python tools/agentkit.py black PROJETO --apply` é a única opção de `agentkit` que **altera arquivos**; exige opção explícita, e deve ser executada somente após aprovar o escopo. Sem `--apply`, retorna código de erro se arquivo exige formatação ou Black está ausente.

## Integração com OpenMaus
**Ponto central:** o formato de compartilhamento de bots importa o texto `SKILL.md`, não scripts e dependências auxiliares. O manifesto `team.yaml` aponta para as skills, mas **não** copia automaticamente `tools/agentkit.py` ao workspace de execução de cada agente.

Para utilizar os comandos, monte/clonE (de forma controlada) este repositório no ambiente de trabalho que o bot de fato consegue acessar e instale a versão de Black no ambiente de desenvolvimento. Verifique `cwd`, isolamento, acesso aos repositórios-alvo, presença do Python e política de shell. Se um agente só tiver acesso ao chat, as skills servem como procedimento, mas os scripts ficam **indisponíveis**, e isso deve ser reportado explicitamente. Não conceda acesso à VPS de produção apenas para disponibilizar scripts: use cópias de trabalho isoladas.

## Procedimentos verificáveis por papel
- Arquiteto: `inspect` + exame humano do grafo → design/spec. Citar limitações da análise estática.
- Tech Lead/PO: `validate spec` e `validate plan` antes de distribuir; `gate` ao fechar entrega.
- DEV: `scope` e `black` (se Python), testes reais do projeto e `validate handoff`.
- Reviewer: confere hash/diff e `validate review`, não confia no JSON declarado sem comparar com GitHub.
- QA: executa testes do projeto; reporta `validate qa` com resultados de execução e depois `gate`.
- Sustentação: `validate handoff` para incidentes e `inspect` para entender código, jamais rodar ferramentas no host de produção sem autorização.

## Black como padrão entre projetos
- **Projetos Python novos:** 4 espaços, Black estável, 88 colunas, `pyproject.toml`, `.editorconfig` e job `--check`.
- **Projetos Python existentes:** adotar Black para novo código e arquivos alterados, sem deixar um bugfix disparar formatação massiva; migração integral em PR separado.
- **GitHub CI:** formatador deve ser verificado no **commit atual**. Qualquer exceção deve estar explícita no projeto.
- **Outras linguagens:** Black não suporta JS/TS, Go, SQL etc.; seus formatadores devem ser escolhidos por stack.

## Inventário das fontes executáveis examinadas
- [Senior Architect](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/senior-architect/scripts): três programas Python extensos para diagramas, dependências e avaliação. **Não foram copiados**. Em especial, o indicador de acoplamento e a inferência por nomes são heurísticos; optamos por reimplementar escopo menor com AST, testes e limitações explícitas. Sem execução dos programas terceiros.
- [ECC](https://github.com/affaan-m/ECC/tree/main/scripts): scripts de CLI, instalação, hooks, orchestration, observabilidade e CI, acoplados ao projeto ECC. Não importados; instalar o ECC inteiro seria complexidade/risco adicional.
- [Ponytail](https://github.com/DietrichGebert/ponytail): regras e plugins, porém a skill principal contém essencialmente procedimento textual. Incorporamos o método, não hooks globais.
- [Agency Agents](https://github.com/msitarzewski/agency-agents): descrições e métodos dos papéis, sem runtime necessário para suas personas. Reescrevemos os contratos.
- [Black](https://github.com/psf/black): ferramenta concreta de formatação Python com `--check` e `--diff`. Usamos o software como dependência de desenvolvimento, não copiamos seu código.
- [OpenMausBot](https://github.com/milind-soni/OpenMausBot/blob/main/docs/team-sharing.md): runtime, permissões e limites de transferência de skills. Configuração precisa ser validada na versão instalada.

## Qualidade do pacote
O workflow `.github/workflows/agentkit-ci.yml` instala Black de versão fixada, executa `unittest` em Python 3.11 e 3.13, verifica `black --check` e valida os exemplos JSON. CI do repositório comprova apenas estes checks. Ainda são necessários testes end-to-end dos seis bots no OpenMaus e validação de permissões na VPS. Nenhum segredo, deploy ou acesso à VPS está presente neste pacote.
