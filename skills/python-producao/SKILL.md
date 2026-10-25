---
name: python-producao
description: "Use somente em projetos Python para implementar e revisar serviços robustos respeitando versão, bibliotecas, lint e testes já adotados."
---
# Python pragmático em produção

## Pré-condições
Verificar `pyproject.toml`, `requirements*.txt`, `uv.lock`, `poetry.lock`, Dockerfile, runtime, versão Python, framework e comando de testes. **Não presumir** que a VPS Python 3.13 dita a versão do projeto.

## Procedimento
1. Identifique fluxo de entrada, validações, efeitos colaterais, contratos públicos e tipagem do módulo; preserve padrões.
2. Reuse biblioteca padrão (`pathlib`, `logging`, `dataclasses`, `contextlib` etc.) e dependências instaladas antes de buscar nova.
3. Evite `except Exception: pass`, retries sem limite, transações abertas, global mutável surpreendente, conversão silenciosa e logs com PII.
4. Em integração HTTP, cuide de timeout, tratamento de status, retry somente idempotente, rate limit, falha parcial e observabilidade proporcional.
5. Em PostgreSQL, use parâmetros, transações e migrações reversíveis conforme projeto. Nunca execute schema change em produção para testar hipótese.
6. Async só quando trabalho I/O concorrente justificar e stack suportar; não misture bloqueio síncrono no event loop.
7. Escreva testes significativos no framework **do projeto**, tipicamente pytest: positivo, negativo, fronteira, falha de integração e regressão.
8. Rode lint, testes e typecheck disponíveis no repo, sem inventar comandos. Apresente resultados e limites.

## Saída
Diff, estratégia de teste, impacto de dados, compatibilidade e rollback (quando necessário).

## Não fazer
Migrar todo projeto para FastAPI/uv/Ruff/Pydantic por preferência pessoal; exigir cobertura 80% arbitrária; adicionar métricas/logs ruidosos ou abstrações sem demanda.
