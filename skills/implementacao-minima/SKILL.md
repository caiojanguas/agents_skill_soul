---
name: implementacao-minima
description: "Use em implementação, bugfix ou revisão quando o objetivo for a menor mudança completa e verificável, sem sobreengenharia nem redução de segurança."
---
# Implementação mínima — engenharia enxuta

## Regra-mãe
Minimizar **complexidade total e superfície de risco**, não apenas linhas. Código curto inseguro ou incompleto é pior que o diff ligeiramente maior e correto.

## Antes de codificar
1. Leia ticket, aceite, AGENTS.md do projeto, módulos afetados, chamadores e testes. Faça inventário da superfície mínima completa.
2. Pergunte na ordem:
   - Isso precisa existir para o requisito?
   - O projeto já tem função, módulo ou padrão que resolve?
   - A biblioteca padrão ou plataforma oferecem solução?
   - Uma dependência **já instalada** oferece solução?
   - Só então, qual é o código novo mínimo?
3. Se demandar dependência, migração, serviço, configuração ou abstração não prevista, explicite custo e reavalie antes de introduzir.
4. Para bug, investigue causa e crie/verifique reprodução quando possível.

## Durante
- Faça diff pequeno e coeso; evite renomeações cosméticas e “while here”.
- Atualize chamadas, testes/fixtures e contratos necessários ao funcionamento. Não esqueça consumidores em busca de menos linhas.
- Proteja limites de confiança, erros críticos, consistência, acessibilidade e privacidade.
- Antes de criar wrapper, genericidade, flag e opção, peça caso concreto. Código claro é mais importante que encurtamento artificial.
- Teste novo caminho não trivial e regressão relevante. Não adicione snapshot gigante para falsificar qualidade.

## Antes de entregar
Passe cada linha do diff pela pergunta “é exigida pelo comportamento ou segurança?”. Remova extra. Registre o que deliberadamente **não** fez e por quê; se dívida foi aceita, diga gatilho que justificaria melhoria.

## Saída
Mudanças e justificativas, testes com comando/resultado, limites e riscos, branch/PR (se feito) e entrega ao Reviewer.

## Erros
Nunca retirar validação de entrada, tratamento de perda de dados, autorização ou teste crítico sob pretexto de minimalismo. Se não consegue executar teste, diga `não executado`.
