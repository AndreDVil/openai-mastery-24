# Engineering Note  
## LLMs Orientados a Contratos — Por que Prompts Não São Suficientes

**Data:** 2025-12-13  
**Contexto:** openai-mastery-24  
**Categoria:** AI Systems / Engineering Notes  

---

## Introdução

Grande parte do uso atual de LLMs ainda é guiada por uma lógica implícita:

> “Se eu escrever um prompt bom o suficiente, o modelo vai se comportar bem.”

Essa lógica funciona para:
- exploração
- prototipagem
- uso manual

Ela **não funciona** para sistemas.

Este texto documenta o ponto em que fica claro que,
para qualquer aplicação séria,
**prompts não são contratos**.

---

## O problema fundamental dos prompts

Prompts são:
- instruções
- sugestões
- contexto

Mas **não são garantias**.

Mesmo prompts longos, bem escritos e detalhados:
- podem ser ignorados parcialmente
- podem ser interpretados de forma ambígua
- não têm mecanismos nativos de validação

Em outras palavras:
> um prompt pode *pedir*  
> mas não pode *exigir*

Isso é aceitável quando o output é texto livre.  
Não é aceitável quando o output alimenta sistemas.

---

## Sistemas precisam de contratos, não de expectativas

Em engenharia de software tradicional:
- APIs têm contratos
- funções têm tipos
- bancos têm schemas
- integrações falham quando o contrato é violado

Quando um LLM entra no sistema, nada disso desaparece.

O erro comum é tratar o modelo como:
> “um humano muito bom digitando rápido”

O modelo correto é:
> **um componente não determinístico que precisa ser limitado**

E limitar, em engenharia, significa **contratar**.

---

## O que é um contrato em sistemas baseados em LLMs

Um contrato não é apenas “responder em JSON”.

Um contrato define:
- **quais campos existem**
- **quais campos são obrigatórios**
- **quais tipos são aceitos**
- **quais valores são válidos**
- **o que é proibido**

No Projeto 03, isso se materializou como:
- um JSON explícito
- sem campos opcionais
- sem propriedades extras
- com enum, ranges e versionamento

Isso transforma o modelo em:
> um produtor de dados com responsabilidade clara

---

## JSON Mode ajuda, mas não resolve

JSON Mode é uma **ferramenta sintática**.

Ele ajuda a garantir que:
- o output seja um objeto JSON
- não haja texto fora da estrutura

Mas JSON Mode **não sabe**:
- se o campo está faltando
- se o tipo está errado
- se o valor faz sentido
- se o contrato foi violado semanticamente

Confiar apenas em JSON Mode é confundir:
> **formato** com **significado**

Contratos vivem no nível semântico.

---

## O papel do system prompt em contratos

O system prompt não é o contrato.
Ele é a **declaração do contrato**.

Sua função é:
- explicar as regras ao modelo
- reforçar o que é proibido
- alinhar expectativas

Mas o system prompt **não valida nada**.

Ele atua antes da execução.
O contrato precisa ser verificado depois.

Essa separação é importante:
- prompt = governança
- validação = controle

---

## O momento em que o modelo deixa de ser “criativo”

Ao adotar contratos, algo interessante acontece:
- a criatividade do modelo diminui
- a utilidade do modelo aumenta

Isso não é uma perda.
É uma troca consciente.

Para sistemas:
- previsibilidade > criatividade
- correção > eloquência
- consistência > originalidade

Criatividade pode existir **dentro do contrato**,
não fora dele.

---

## Contratos permitem retry inteligente

Um efeito colateral positivo de contratos explícitos
é a possibilidade de **retry informativo**.

Quando o sistema sabe:
- exatamente o que está errado
- exatamente onde o contrato foi violado

o retry deixa de ser tentativa cega
e passa a ser **feedback dirigido**.

O modelo não “tenta de novo”.
Ele **corrige**.

Isso só é possível quando o contrato existe.

---

## Implicação prática importante

Sem contratos:
- agentes são frágeis
- tool calling vira gamble
- RAG quebra silenciosamente
- erros se propagam

Com contratos:
- falhas são detectáveis
- correções são possíveis
- limites são claros
- sistemas escalam com menos risco

---

## Insight central

O insight mais importante deste artigo é simples, mas profundo:

> **Prompts orientam comportamento.  
> Contratos definem limites.**

E sistemas vivem de limites bem definidos.

---

## Conclusão

Tratar LLMs como sistemas orientados a contratos
não é excesso de rigor.
É pré-requisito para confiabilidade.

JSON Mode é uma ferramenta útil.
System prompts são necessários.
Mas nenhum deles substitui um contrato explícito
validado pelo sistema.

A partir do momento em que contratos entram em cena,
LLMs deixam de ser experimentais
e passam a ser componentes de engenharia.
