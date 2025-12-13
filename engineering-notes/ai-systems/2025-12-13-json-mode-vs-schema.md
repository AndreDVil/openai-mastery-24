# Engineering Note  
## JSON Mode não é Schema — Formato, Contrato e Validação

Data: 2025-12-13  
Contexto: openai-mastery-24  
Categoria: AI Systems / Engineering Notes  

---

Introdução

Uma confusão recorrente em sistemas baseados em LLMs é tratar
JSON Mode como sinônimo de contrato.

Essa confusão leva a sistemas que:
- parecem estruturados
- funcionam em demos
- quebram silenciosamente em produção

Este texto existe para separar claramente três conceitos distintos:
- formato
- contrato
- validação

E mostrar por que misturá-los é um erro de arquitetura.

---

O que o JSON Mode realmente faz

JSON Mode é um mecanismo de enforcement sintático.

Quando ativado, ele força o modelo a:
- retornar um objeto JSON
- evitar texto fora da estrutura
- respeitar a sintaxe básica do formato

Isso é extremamente útil.
Mas é só isso.

JSON Mode não entende significado.
Ele não sabe:
- se um campo é obrigatório
- se um valor faz sentido
- se um tipo está correto
- se um contrato foi violado

JSON Mode responde à pergunta:
“Isso é JSON?”

Não à pergunta:
“Isso é o JSON certo?”

---

Formato não é contrato

Formato é a casca.
Contrato é o conteúdo.

Dois JSONs podem ser igualmente válidos sintaticamente
e completamente diferentes semanticamente.

Exemplo:

{ "confidence": "high" }

e

{ "confidence": 0.9 }

Ambos são JSON válidos.
Apenas um respeita o contrato.

Confiar em formato é assumir que:
“Se parece certo, está certo”

Essa suposição não se sustenta em sistemas reais.

---

O papel do schema

Um schema existe para responder perguntas que o JSON Mode não responde:

- Quais campos são obrigatórios?
- Campos extras são permitidos?
- Quais tipos são aceitos?
- Há enums?
- Existem limites numéricos?
- Existe versionamento?

No Projeto 03, o schema não é apenas documentação.
Ele é regra executável.

Mesmo quando implementado manualmente,
o schema representa um compromisso explícito
entre o sistema e o modelo.

---

Por que schema sem validação não adianta

Outro erro comum é:
- definir um schema
- documentá-lo
- e nunca validá-lo de verdade

Nesse cenário:
- o schema vira comentário
- o sistema “confia” que o modelo obedeceu
- erros passam despercebidos

Schema só existe de verdade quando:
o sistema falha ao ser violado

Sem validação, não há contrato.
Há apenas esperança.

---

Separando responsabilidades corretamente

Um sistema bem projetado separa claramente:

1. JSON Mode  
Responsável por:
- garantir formato JSON
- reduzir lixo textual

Não deve:
- validar significado
- garantir tipos
- aplicar regras de negócio

---

2. Schema  
Responsável por:
- definir o contrato
- documentar expectativas
- estabelecer limites claros

Não deve:
- assumir que será respeitado

---

3. Validação  
Responsável por:
- verificar o contrato
- rejeitar violações
- produzir erros explícitos

É aqui que o sistema assume controle.

---

Onde entra o system prompt

O system prompt atua antes de tudo.

Ele:
- explica o contrato ao modelo
- reforça proibições
- reduz a chance de erro

Mas ele não substitui nenhuma camada posterior.

Prompt é prevenção.
Validação é garantia.

Confundir os dois leva a sistemas frágeis.

---

O que acontece quando essas camadas se misturam

Quando formato, contrato e validação não são separados:
- erros ficam difíceis de diagnosticar
- retries viram tentativa cega
- bugs parecem aleatórios
- confiança no sistema diminui

A separação clara permite:
- debug rápido
- retry direcionado
- evolução segura do contrato
- refatorações controladas

---

Insight central

O insight principal deste artigo é simples:

JSON Mode garante forma.  
Schema define significado.  
Validação garante verdade.

Qualquer sistema que misture essas camadas
vai parecer funcionar — até não funcionar mais.

---

Conclusão

JSON Mode é uma ferramenta importante,
mas não é uma solução completa.

Sistemas confiáveis baseados em LLMs
exigem uma arquitetura explícita onde:
- formato
- contrato
- validação

são tratados como responsabilidades distintas.

Separar essas camadas não é burocracia.
É engenharia.
