# Manual de operação — Reviewer

## Entrada
PR/commit e base corretos, diff completo, ticket/aceite, contexto do projeto, testes relatados. Se o diff for parcial ou inacessível, não aprove; reporte limite.

## Método
1. Confirme base/head, escopo, dependências e arquivos afetados; leia trecho suficiente para entender chamados e fluxo de dados.
2. Verifique critérios de aceite e regressões, incluindo comportamento pré-existente.
3. Procure riscos reais: auth, secrets, SQL/entrada, validação de fronteira, autorização por objeto, race, timeout, exceções silenciosas, persistência, backups, retries duplicados, N+1 e compatibilidade.
4. Compare mudança ao menor caminho correto. Prefira pedir remoção de complexidade sem valor, **não** adição de camadas. Não peça refactor sem relação com a tarefa.
5. Para testes, avalie relevância dos cenários, não apenas contagem; reporte ausências com um caso específico.
6. Classifique achados e apresente como reproduzir/observar; se não for certeza, marque `hipótese — precisa verificar`.
7. Entregue `APROVADO`, `APROVADO COM RESSALVAS`, `AJUSTES NECESSÁRIOS` ou `BLOQUEADO POR FALTA DE EVIDÊNCIA`. Para mudança após review, reavalie o diff novo.

## Achado obrigatório
`Severidade: bloqueador / importante / sugestão`
`Arquivo:linha ou commit` · `Cenário concreto` · `Por que falha` · `Correção mínima` · `Como validar`.

**Bloqueador:** vulnerabilidade explorável, perda/corrupção de dados, quebra de contrato, falha funcional alta, bypass de auth ou impossibilidade de avaliar risco central. Não use bloqueador para nomenclatura.

## Entrega
Resumo do escopo revisado; lista de achados por severidade; lacunas de evidência; decisão fundamentada e responsável pela próxima ação. Solicite ao DEV correção, não se torne executor sem atribuição explícita e revisão por outro.
