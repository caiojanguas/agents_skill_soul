# Padrão de formatação nos projetos

## Python: Black em todos os projetos
Fonte: [psf/black](https://github.com/psf/black); documentação [uso e configuração](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html).

- **Indentação**: 4 espaços, não tabulações;
- **Comprimento-alvo**: 88 caracteres, configurado no `pyproject.toml` de novos projetos;
- **Versão**: Black `26.10.0` para a validação compartilhada (fixada e publicada em outubro de 2026);
- **Modo seguro**: `python -m black --check --diff .` sem mutações;
- **Aplicação**: `python -m black src/arquivo.py` **somente** quando alteração de arquivos é autorizada.

Black **não** formata SQL, YAML, TypeScript, JavaScript ou outras linguagens. Para elas, o projeto deve definir formatter próprio, e `.editorconfig` garante requisitos elementares de whitespace.

## Padrão centralizado no GitHub
O arquivo [black-reusable.yml](../.github/workflows/black-reusable.yml) é um workflow reutilizável de GitHub Actions. Ele executa Black fixado a `26.10.0` e bloqueia o CI se encontrar código fora do padrão. Uma aplicação externa pode ter um job pequeno que chama o workflow, conforme [template](../templates/python/github-workflow-example.yml).

**Antes de usar**, faça merge deste PR na branch principal (após revisão), escolha uma referência SHA ou tag controlada para a chamada e confira se a política de Actions do repositório consumidor permite workflow reutilizável externo. O template possui placeholder e **não pode ser aplicado literalmente**.

### Projeto Python novo
1. Adapte `templates/python/.editorconfig` e adicione a seção de `templates/python/pyproject.toml` ao `pyproject.toml` real.
2. Inclua Black na ferramenta de dependências de desenvolvimento do projeto, com versão compatível com a organização.
3. Copie o workflow de exemplo, substitua o placeholder pela referência revisada.
4. Rode `python -m black --check --diff .` e os testes do projeto; nenhum job de formatação substitui pytest.
5. Abra PR normal; não faça push direto em main ou aplique em produção.

### Projeto Python legado
1. Confirme se há outra regra de formatação e o que Black reformata em `--check --diff`.
2. Adote Black em arquivos novos e alterados. Não crie PR gigante de mudança cosmética junto de bugfix.
3. Para ativar checagem de todo o repo (`check_path: "."`), **primeiro** faça migração separada e revise o diff; antes disso, usar caminho de escopo **já migrado**, como `src/novo_modulo`, se houver.
4. Fixe a versão em cada projeto ou use a verificação reutilizável central e mantenha rastreabilidade da política.
5. Só considere o rollout completo após CI verde e review.

## Papéis e responsabilidade
- Arquiteto: Black no projeto Python novo, sem reformatar legado.
- Líder/PO: tarefa de adoção específica, CI e regressão, sem confundir estilo com funcionalidade.
- DEV: formata apenas o código dentro do escopo.
- Reviewer: fiscaliza evidência de `--check` sem opiniões pessoais de estilo.
- QA: valida no SHA correspondente; Black verde não equivale a testes passando.
- Sustentação: não instala nem roda formatter diretamente em produção.

## Limite da centralização
Adicionar a skill e o workflow **neste** repositório não altera outros projetos automaticamente. Para garantir o padrão no GitHub de cada aplicação, é preciso instalar a chamada reutilizável no respectivo repo e manter as configurações de Python coerentes. Sem isso o comportamento segue dependendo da iniciativa do agente.
