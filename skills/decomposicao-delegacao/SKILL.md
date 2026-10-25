---
name: decomposicao-delegacao
description: "Use para transformar uma demanda aprovada em tarefas com dependências, responsáveis, isolamento, gates e evidências; não invoque subagentes inexistentes."
---
# Planejamento e delegação real

## Entrada
Spec aprovada (ou tarefa clara), projeto, estado e restrições de ambiente, papéis disponíveis no runtime e limites de gasto/tempo.

## Passos
1. Classifique porte e risco. Trabalho curto/local pode ir direto a DEV com testes e revisão proporcionais; não crie burocracia.
2. Defina vertical mínima entregável e aceite verificável. Separe implementação, dados, integração, testes e rollout apenas quando necessários.
3. Para cada tarefa, registre ID, objetivo, artefato, área de escrita, branch/worktree, dependências, riscos, evidências, condição de pronto e responsável.
4. Desenhe grafo de dependências, paralelize **somente** ramos independentes; não permita dois agentes editando mesmos arquivos/mesma branch sem acordo explícito.
5. Decida quando pedir Arquiteto, Reviewer, QA ou Sustentação conforme risco. Auth, dados, migrações e produção exigem maior rigor.
6. Ao delegar, passe contrato completo e links, não logs enormes. Utilize função nativa de coordenação apenas se realmente disponível (`coordinate_bots` ou equivalente).
7. Acompanhe entregas pelo artefato e evidências. Para falha/timeout, determine se efeito externo ocorreu antes de retry. Limite ciclos improdutivos e escale bloqueios.
8. Nunca libere merge/deploy só porque DEV e QA disseram “feito”.

## Saída
Backlog mínimo ordenado e status por tarefa: proprietário, pronto para iniciar, em curso, bloqueado ou aguardando gate.

## Não fazer
Delegar a papéis imaginários, prometer execução assíncrona sem runtime, autoaprovar trabalho delegado, serializar tarefas independentes sem motivo, gerar dezenas de tickets para uma pequena correção.
