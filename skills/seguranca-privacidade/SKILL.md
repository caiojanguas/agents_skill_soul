---
name: seguranca-privacidade
description: "Use para mudanças que lidam com autenticação, autorização, segredos, dados pessoais, serviços expostos ou integrações externas."
---
# Segurança e privacidade aplicada ao mínimo necessário

## Quando ativar
Autenticação, API pública, acesso remoto, token, conexão de app, dado pessoal, pagamento/envio externo, logs, integrações e modelo RAG com dados internos.

## Procedimento
1. Liste fronteiras de confiança, dados tratados, finalidade e onde entram, persistem, trafegam e aparecem em logs.
2. Confira autorização por recurso e ator, não apenas presença de login. Negar por padrão até permissão explícita.
3. Minimize coleta, exposição e retenção. Use dados de teste e mascaramento; nunca leve segredos para chat/PR público.
4. Revise validação de entrada, queries parametrizadas, path traversal, chamadas externas, SSRF, redirecionamento, credenciais, dependências e abuso de retry.
5. Verifique autorização operacional: prompt de agente não libera acesso; só runtime/infra controla ferramentas, ambientes e aprovações.
6. Para mudança com risco, proponha teste negativo e revisão de rollback. Não afirme conformidade com LGPD sem análise do caso.
7. Registre risco residual, mitigação mínima, evidência e aprovação pendente.

## Saída
Mapa curto de ameaça, achados priorizados e ações verificáveis. Evite implantar scanner, framework, criptografia caseira ou infraestrutura sem necessidade.
