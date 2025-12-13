# Engineering Note  
## Retry como Feedback — Erro não é Falha, é Sinal

Data: 2025-12-13  
Contexto: openai-mastery-24  
Categoria: AI Systems / Engineering Notes  

---

Introdução

Em sistemas tradicionais, retry costuma ser tratado como um mal necessário:
- algo falhou
- tenta de novo
- espera que funcione

Quando aplicado dessa forma a LLMs, retry vira:
- tentativa cega
- aumento de custo
- fonte de comportamento imprevisível

Este texto documenta uma mudança importante de modelo mental:
retry não como exceção,
mas como **mecanismo explícito de feedback**.

---

O erro clássico: retry como sorte

A forma mais comum (e perigosa) de usar retry com LLMs é:

- o modelo erra
- a chamada é repetida
- nada muda
- o resultado depende de sorte

Esse tipo de retry:
- não ensina nada ao modelo
- não aumenta confiabilidade
- apenas consome tokens

Pior: cria a ilusão de robustez.

---

Por que LLMs erram de forma previsível

Um ponto fundamental é entender que:
LLMs não erram aleatoriamente.

Eles erram porque:
- o contrato não ficou claro
- a instrução conflita com restrições
- há ambiguidade estrutural
- faltam limites explícitos

Isso significa que, na maioria dos casos,
o erro contém informação útil.

Ignorar essa informação é desperdiçar sinal.

---

Retry como feedback dirigido

Quando um sistema possui:
- um contrato explícito
- validação semântica
- erros bem classificados

o retry pode ser usado de forma muito mais poderosa.

Em vez de:
“Tente novamente”

o sistema diz:
- onde o contrato foi violado
- qual campo está errado
- o que precisa ser corrigido
- o que é proibido

O modelo não tenta de novo.
Ele **corrige**.

---

O papel da validação no retry inteligente

Retry sem validação é ruído.

A validação fornece:
- o diagnóstico exato
- o ponto de correção
- o limite do aceitável

Sem validação, o sistema não sabe:
- por que errou
- se a correção funcionou
- quando parar de tentar

Retry inteligente só existe quando:
erro é detectável
e correção é verificável.

---

Retry precisa ser limitado

Um ponto crítico: retry infinito é bug.

Sistemas confiáveis precisam de:
- número máximo de tentativas
- comportamento determinístico
- falha explícita quando não há convergência

No Projeto 03, isso se materializa como:
- max_retries pequeno
- mensagens corretivas claras
- retorno de erro estruturado se necessário

Isso protege o sistema de:
- loops infinitos
- custos imprevisíveis
- comportamentos erráticos

---

Retry muda a relação com o modelo

Quando retry vira feedback:
- o modelo deixa de ser imprevisível
- erros deixam de ser “azar”
- comportamento passa a convergir

O sistema assume o papel ativo.
O modelo passa a operar dentro de limites claros.

Essa inversão é fundamental.

---

Retry como parte do contrato implícito

Um insight importante é que:
retry também é parte do contrato.

O modelo aprende implicitamente que:
- violações serão detectadas
- correções serão exigidas
- o resultado final precisa convergir

Mesmo sem “memória”, esse feedback em tempo de execução
altera o comportamento de forma local e controlada.

---

Quando retry não deve ser usado

Nem todo erro deve gerar retry.

Exemplos:
- falta de permissão
- erro de autenticação
- falhas de infraestrutura
- inputs inválidos do usuário

Retry inteligente é específico para:
- erros semânticos
- violações de contrato
- inconsistências corrigíveis

Misturar esses casos gera confusão.

---

Insight central

O insight central deste artigo é:

Retry não é um pedido de desculpas ao sistema.  
É uma conversa técnica com o modelo.

Quando bem usado:
- aumenta confiabilidade
- reduz variância
- transforma erro em aprendizado controlado

Quando mal usado:
- mascara problemas
- aumenta custo
- cria sistemas frágeis

---

Conclusão

Tratar retry como feedback muda profundamente
a forma de projetar sistemas com LLMs.

Erro deixa de ser exceção.
Passa a ser sinal.

E sistemas que sabem interpretar sinais
são sistemas que escalam.
