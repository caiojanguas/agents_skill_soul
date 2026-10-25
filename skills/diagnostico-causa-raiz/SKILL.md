---
name: diagnostico-causa-raiz
description: "Use para bugs, falhas de testes, integrações e incidentes quando é necessário localizar a causa antes de propor correção."
---
# Diagnóstico sistemático de causa raiz

## Procedimento
1. Descreva sintoma e impacto, quando começou, frequência, ambiente, versão/commit e comportamento esperado x observado.
2. Colete mensagem de erro e linha do tempo sem segredos; reproduza de modo controlado, se possível.
3. Inspecione mudanças recentes, dependências e exemplos similares que funcionam.
4. Trace entrada e saída entre componentes para localizar a primeira divergência. Faça hipóteses explícitas e ordenadas por plausibilidade e custo do teste.
5. Escolha verificação **não destrutiva** que discrimine hipóteses; execute somente se ferramenta/autorização disponível.
6. Separe raiz confirmada, causa provável e correlação. Se inconclusivo, peça informação mínima para diferenciar.
7. Para correção, proponha diff mínimo, teste de regressão e risco/rollback; em produção, apenas sugira até receber autorização.
8. Valide o sintoma original após correção e confira efeitos secundários, não apenas health geral.

## Anti-intuições
- Retry cego pode duplicar efeitos externos.
- Restart pode esconder evidência e não corrigir causa.
- Ausência de exceção não prova persistência correta.
- Erro de permissão não se resolve automaticamente ampliando privilégios.

## Saída
Evidências, hipótese/certeza, confirmação ou lacuna, próximo experimento, solução proposta, gate e responsável.

## Quando interromper
Sem permissões, dados sensíveis ou risco de perda: pare, sanitize e escale. Não invente teste de produção.
