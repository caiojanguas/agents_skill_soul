---
name: desenho-arquitetural
description: "Use quando houver decisão técnica relevante sobre componentes, dados, integrações, migração ou agentes e for necessário comparar alternativas e registrar ADR."
---
# Desenho arquitetural mínimo e responsável

## Acionar quando
Alteração transversal, nova integração, limitação operacional ou decisão tecnológica relevante. Não para ajuste local já claramente resolvido por padrão existente.

## Entrada
Spec/aceite, arquitetura atual verificada, restrições de stack, dados/segurança/custos, histórico de decisões, critérios de operação.

## Método
1. Desenhe o estado atual pelo que foi **observado**, não pelo que parece desejável.
2. Avalie primeiro **não mudar**, reutilizar módulo existente e estender incrementalmente.
3. Compare alternativas com matriz proporcional: escopo, complexidade, falhas, custo de construção e manutenção, riscos, reversibilidade e aderência ao projeto.
4. Prefira simplicidade: monólito modular e integrações diretas até que throughput, equipes independentes, isolamento ou resiliência justifiquem separação.
5. Descreva: limites e contratos, fluxo de dados, validação/autorização, consistência, retries/idempotência, migração e rollback, telemetria mínima. Para agentes, adicione topologia, contexto, isolamento, handoffs e permissões.
6. Não desenhe detalhes inexistentes nem métricas fictícias. Diagramas Mermaid simples somente quando reduzem ambiguidade.
7. Escreva ADR em `docs/adr/NNNN-tema.md` se decisão durável, com status **proposto** até aceite: contexto, opções, decisão, consequência, condição de revisão, riscos.
8. Derive tarefas incrementais verificáveis e faça handoff ao Líder. Não iniciar deploy sem gate.

## Critério de saída
DEV entende interface e módulos; QA consegue derivar cenários; Sustentação entende sinais e formas de recuperação; dono entende custo e riscos.

## Antipadrões
Microserviços pela moda, novas filas sem requisito, `generic framework` para uma rotina, abstração antes do segundo caso real, big bang sem rollback.
