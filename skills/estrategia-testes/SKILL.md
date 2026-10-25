---
name: estrategia-testes
description: "Use quando QA precisar derivar cenários de aceite, executá-los conforme risco e fornecer parecer baseado em observações."
---
# QA com evidência e economia

## Entrada
Spec e aceite, commit preciso, ambiente/sandbox, comandos reais, serviços envolvidos, dados fictícios e restrições.

## Passos
1. Crie uma matriz `cenário | risco | pré-condição | ação | esperado | evidência | estado`. Priorize o caminho feliz essencial, negativos, segurança e risco de regressão.
2. Para bugfix, reproduza sintoma antes se possível, execute após correção, avalie teste de regressão.
3. Defina nível de teste por risco: unitário para lógica; integração para DB/API e transação; E2E para fluxo real; carga apenas com requisito e ambiente apropriado.
4. Projete massa controlada, isolamento transacional e limpeza segura; não usar dados reais de produção sem autorização.
5. Execute testes no commit e ambiente identificados; registre comando/exit code e falhas. Confirme que testes desabilitados ou `skip` não escondem resultado.
6. Classifique defeitos reproduzíveis e envie ao DEV; dúvidas de aceite ao Líder/PO.
7. Repita somente cenários impactados e regressão proporcional após fix, a menos que risco maior peça suíte completa.
8. Reporte `APROVADO PARA DECISÃO DE RELEASE`, `REPROVADO` ou `INCONCLUSIVO` e risco residual.

## Não afirmar
Teste estático ou especificação não provam execução. Pipeline antigo não vale para commit novo. Não declare porcentagem de cobertura sem medição.

## Saída
Matriz curta com PASSOU/FALHOU/NÃO EXECUTADO/BLOQUEADO, evidências e recomendação.
