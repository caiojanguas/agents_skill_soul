---
name: descoberta-requisitos
description: "Use para entrevistar o dono sobre ideia nova ou demanda ambígua e produzir especificação aprovada; evite em tarefas triviais já delimitadas."
---
# Descoberta de requisitos por entrevista

## Acionar quando
Objetivo ou aceite indefinido, mudanças novas com trade-offs, restrições desconhecidas ou pedido explícito de entrevista. Não acionar para bug com repro/escopo e aceite claros.

## Entradas
Pedido original; projeto/repo e documentação existentes; decisões históricas acessíveis; prazo, restrições e responsável pela aprovação. **Primeiro inspecione fatos acessíveis**; não pergunte ao humano por dados encontrados no código.

## Procedimento
1. Reescreva em uma frase o resultado desejado, sem inferir arquitetura.
2. Identifique as lacunas que poderiam mudar o produto ou impedir aceitação: motivo, usuário, comportamento, limite, dados, acessos, implantação, tolerância a falhas.
3. Escolha profundidade pelo risco: rápida (até 3 perguntas), padrão (até 8), profunda (até 15). São limites, não metas; não fabrique perguntas extras.
4. Faça **uma pergunta por turno**. Ataque primeiro o ponto de maior incerteza; dê sugestão e trade-off quando isso ajudar. Registre resposta e premissa. Evite “você prefere A ou B?” sem explicar consequência.
5. Para iniciativa importante, desafie ao menos uma premissa: por que precisa existir? solução atual? o que acontece se não fizermos?
6. Pare quando houver decisão suficiente para especificar, ou quando atingir limite e restarem pendências explícitas. Pontuações de ambiguidade são heurísticas, nunca garantia.
7. Produza documento com: resumo do problema, resultado/valor, usuários, requisitos, restrições, fora do escopo, decisões tomadas, alternativas rejeitadas, riscos, aceite em cenários observáveis, perguntas pendentes com dono, autorização necessária.
8. Apresente síntese para revisão. Só salve em `docs/specs/YYYY-MM-DD-slug.md` de projeto acessível **com permissão**; salvar não implica commitar, publicar issue ou iniciar implementação.

## Saída
Especificação acionável ou registro de bloqueio com exatamente a decisão que falta. Handoff ao Líder/Arquiteto.

## Falhas
Se o usuário pedir execução imediata com requisito suficiente, não imponha entrevista. Se faltar acesso ao repo, diga o que não verificou. Nunca acrescente respostas fictícias em nome do dono.
