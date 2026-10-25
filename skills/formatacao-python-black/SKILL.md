---
name: formatacao-python-black
description: "Use sempre que um agente escrever, revisar, testar ou preparar commit/PR com código Python; padroniza indentação e formatação pelo Black."
---
# Formatação Python obrigatória com Black

## Regra de equipe
Em todos os projetos Python, **Black é o formatador-padrão**: indentação de 4 espaços (não tabulações), quebras e aspas regidas pelo Black, linha-alvo de 88 caracteres por padrão. Isso não cobre JavaScript, TypeScript ou outras linguagens.

- Para **projetos novos**, inclua `[tool.black]` em `pyproject.toml` com `line-length = 88`, .editorconfig com 4 espaços nos arquivos Python, dependência de desenvolvimento Black fixada e `black --check` no CI.
- Para **projetos existentes**, inspecione versão Python, configuração `pyproject.toml`, formatter/CI já implantados e a extensão do diff. Não reformate todo o legado em PR funcional. Migração global requer tarefa/PR separado e aprovação.
- Se já houver regra Black específica do projeto (ex.: 100 colunas), **não a sobreponha silenciosamente**. Registre divergência e proponha padronização consciente.
- Não fixe Python alvo em toda a organização: use versão exigida por cada projeto. Evite `--preview` e `--unstable` como padrão.
- Use `black` para código Python; mantenha outras linguagens nos formatadores de cada ecossistema.

## Comandos
1. Verificar a ferramenta: `python -m black --version`; se ausente, instale no ambiente de desenvolvimento permitido, conforme dependências do projeto, e nunca altere produção só por formatação.
2. Prévia segura: `python -m black --check --diff caminho/do/arquivo.py`.
3. Formatar arquivos Python modificados, quando autorizado: `python -m black caminho/do/arquivo.py`.
4. No repositório desta biblioteca, use `python tools/agentkit.py black .` (checagem) e `python tools/agentkit.py black . --changed-base main` (somente arquivos Python alterados em commits desde main).
5. Em CI, `python -m black --check .` apenas se o repositório inteiro já adota o padrão; em migração gradual, limitar caminhos.

## Gates por papel
- **Arquiteto:** recomendar Black na especificação de projeto novo, sem iniciar reformatação.
- **Tech Lead/PO:** incluir formatador e impacto no aceite/CI; impedir PR que misture formatação massiva e bugfix sem justificativa.
- **DEV:** formatar somente Python alterado, antes de entregar.
- **Reviewer:** exigir evidência do `black --check` para arquivos Python tocados, sem privilegiar estilo sobre bugs.
- **QA:** conferir job no commit correto; Black verde **não** prova que testes passaram.
- **Sustentação:** ao criar scripts Python novos em trabalho autorizado, seguir Black; nunca reformatar código em produção.

## Falhas
Black ausente = checagem NÃO EXECUTADA, nunca PASSOU. Erro do Black não autoriza bypass de CI. Se versão fixada divergir da do projeto, documente. Não edite áreas fora do escopo para obter resultado verde.

Fonte: https://github.com/psf/black — licença MIT; comandos conforme documentação oficial.
