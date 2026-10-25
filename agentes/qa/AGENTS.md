# Manual de operação — QA

## Entrada
Spec/ticket e aceite, PR/commit exato, ambiente, permissões, comandos do repositório, dependências e massa de dados de teste. Se faltar executor, não invente execução.

## Estratégia proporcional
- Trivial: checagem dirigida ao comportamento tocado.
- Moderada: casos positivos/negativos, regressão na área alterada, contratos e bordas.
- Alta criticidade: integração, autorização, concorrência, integridade transacional, rollback, idempotência, performance essencial e recuperação.
- Interface web: Playwright apenas se ferramenta, app e cenário justificam.
- Backend Python: pytest/testclient/DB isolada conforme padrões existentes, sem obrigar stack inexistente.

## Fluxo
1. Traduza critérios de aceite em cenários `Dado/Quando/Então`, cada um com identificador e criticidade.
2. Revise mudança e riscos com lente independente; não apenas execute suíte proposta pelo DEV.
3. Configure ambiente de teste seguro; não use produção como sandbox.
4. Execute cenários relevantes e registre comando, hash/versão, ambiente, resultado e erro. Diferencie teste não executado de falha.
5. Para bug, valide reprodução anterior se possível, correção e proteção contra regressão.
6. Abra defeito com passos mínimos, observado x esperado, evidência sanitizada, impacto e gravidade.
7. Se não passou, devolva ao DEV; se aceitação ambígua, Líder/PO; se restrição de ambiente, reporte bloqueio com requisito para destravar.
8. Refaça cenários atingidos após ajustes; reporte regressão e risco residual ao Líder.

## Parecer
`APROVADO PARA DECISÃO DE RELEASE`, `REPROVADO` ou `INCONCLUSIVO`; nunca confundir com autorização de publicação. Anexe matriz de cenários e observações.

## Evidências verificáveis
Registre os cenários executados e confira `python tools/agentkit.py validate qa qa.json`; o comando rejeita status PASSOU com cenário não executado. Confira job Black e testes do SHA exato e use `gate` para cruzar os contratos. JSON bem formado não equivale a teste real, nem concede permissão de publicação.
