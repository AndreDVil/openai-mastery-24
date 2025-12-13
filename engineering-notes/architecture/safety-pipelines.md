# Architecture Note  
## Safety Pipelines em Sistemas com LLMs — Defesa em Profundidade

Data: 2025-12-13  
Contexto: openai-mastery-24  
Categoria: Architecture / AI Systems  

---

Introdução

Quando sistemas baseados em LLMs falham, raramente falham por um único motivo.
Eles falham porque **não existem camadas suficientes entre o modelo e o mundo real**.

Este artigo consolida uma ideia central que emerge naturalmente
ao longo dos Projetos 01 a 03:

Sistemas confiáveis com LLMs não dependem de uma única técnica,
mas de **pipelines de segurança em camadas**.

Essa abordagem não é nova em engenharia.
Ela apenas foi esquecida quando LLMs entraram em cena.

---

O problema da confiança direta no modelo

Um erro comum em sistemas com LLMs é a confiança direta:

- confiar no prompt
- confiar no JSON Mode
- confiar “no bom comportamento” do modelo
- confiar que “na prática funciona”

Esse tipo de confiança funciona:
- em demos
- em protótipos
- em uso manual

Ela falha quando:
- o sistema cresce
- o input varia
- o custo do erro aumenta

Confiar diretamente no modelo é um antipadrão arquitetural.

---

Defesa em profundidade: um conceito clássico

Em sistemas críticos (segurança, finanças, aviação),
existe um princípio bem estabelecido:

Nenhuma camada isolada é suficiente.

A confiabilidade surge da sobreposição de camadas independentes,
cada uma tratando uma classe diferente de falhas.

Esse princípio se aplica perfeitamente a LLMs.

---

O Safety Pipeline aplicado a LLMs

Um safety pipeline para LLMs pode ser entendido como
uma sequência explícita de responsabilidades:

1. Governança de comportamento  
2. Enforcement de formato  
3. Verificação estrutural  
4. Validação semântica  
5. Correção controlada  
6. Falha explícita

Cada camada reduz risco.
Nenhuma camada resolve tudo sozinha.

---

Camada 1 — System Prompt (Governança)

A primeira camada é o system prompt.

Seu papel é:
- declarar regras explícitas
- proibir comportamentos indesejados
- alinhar expectativas

Ele atua como prevenção.
Não como garantia.

Um bom system prompt reduz a taxa de erro,
mas não pode ser a única linha de defesa.

---

Camada 2 — Enforced Output Format (JSON Mode)

A segunda camada força a forma do output.

JSON Mode:
- elimina texto solto
- reduz ambiguidade
- facilita parsing

Mas ele não entende significado.
Ele apenas garante forma.

Confiar apenas nesta camada é insuficiente.

---

Camada 3 — Parsing Estrutural

Parsing manual (ex: json.loads) é a primeira barreira real.

Ela responde a perguntas simples:
- isso é JSON?
- a estrutura é válida?

Aqui, erros deixam de ser subjetivos
e passam a ser técnicos.

---

Camada 4 — Validação Semântica (Schema)

Esta é a camada mais importante.

Ela valida:
- campos obrigatórios
- tipos corretos
- valores permitidos
- limites numéricos
- versionamento

É aqui que o sistema realmente assume controle.

Sem esta camada:
- não há contrato
- não há confiabilidade
- não há base para retry inteligente

---

Camada 5 — Correção Controlada (Retry)

Quando validação falha,
o sistema não “tenta de novo”.

Ele:
- explica o erro
- aponta a violação
- exige correção

Retry vira feedback.
Erro vira sinal.

Essa camada transforma comportamento não determinístico
em convergência controlada.

---

Camada 6 — Falha Explícita

Por fim, todo pipeline precisa saber falhar.

Quando:
- retries se esgotam
- erros não são corrigíveis
- o input é inválido

o sistema deve:
- falhar de forma explícita
- retornar erro estruturado
- não mascarar problemas

Falhar claramente é parte da segurança.

---

Por que esse pipeline funciona

Porque cada camada:
- trata um tipo diferente de risco
- não depende da camada anterior
- reduz impacto de falhas residuais

O sistema não “confia” no modelo.
Ele o **contém**.

---

O erro de tentar simplificar demais

Um antipadrão comum é tentar remover camadas:

- “JSON Mode já resolve”
- “O prompt está bom”
- “Nunca deu problema”

Essas frases funcionam até o dia
em que deixam de funcionar.

Pipelines existem justamente para o dia ruim,
não para o dia bom.

---

Insight central

O insight central deste artigo é:

LLMs não devem ser confiáveis.  
Devem ser **controláveis**.

Controle emerge de arquitetura,
não de instrução.

---

Conclusão

Safety pipelines não são burocracia.
São a condição mínima para usar LLMs
em sistemas que importam.

A partir do momento em que esse pipeline existe,
LLMs deixam de ser um risco inevitável
e passam a ser um componente útil,
limitado e governado.

Esse é o ponto em que IA deixa de ser experimento
e passa a ser engenharia.
