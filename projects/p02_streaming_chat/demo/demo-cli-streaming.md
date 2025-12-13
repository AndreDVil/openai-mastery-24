# Demo — Project 02 · Streaming Chat Client (stateless)

This document shows a real CLI session using the Project 02 – Streaming Chat Client.
The focus is on:
- streaming behavior (token-by-token output)
- basic commands
- latency summary


============================================================
1. Command Used
============================================================

python projects/p02_streaming_chat/streaming_chat.py \
  --model gpt-4o-mini \
  --temperature 0.7 \
  --top_p 1.0 \
  --max-output-tokens 256 \
  --system "You are a helpful assistant. Answer in Brazilian Portuguese."


============================================================
2. Session Transcript (simplified)
============================================================

----- Startup -----

────────────────────────────────────────────────────────────
Project 02 · Streaming Chat Client (stateless)
────────────────────────────────────────────────────────────
Model: gpt-4o-mini
Temperature: 0.7 · top_p: 1.0
Max output tokens: 256
System prompt: You are a helpful assistant. Answer in Brazilian Portuguese.
Commands: /help · /config · /exit



----- 1st Question -----

You: O que é streaming de respostas em modelos de IA?

Assistant (streaming...):

Streaming de respostas é um modo de interação em que o modelo
não envia a resposta inteira de uma vez. Em vez disso, ele vai
enviando pequenos fragmentos de texto, token por token, conforme
a resposta é gerada. Isso permite que você comece a ler a saída
mais rápido, melhora a experiência do usuário e ajuda a perceber
que o modelo está ativo e processando sua pergunta.

  (first token: 0.418s · total: 1.937s)



----- 2nd Question -----

You: Quais são as principais vantagens técnicas do streaming em relação à resposta tradicional?

Assistant (streaming...):

Do ponto de vista técnico, o streaming oferece algumas vantagens
importantes em relação ao modo tradicional de resposta:

1. Latência percebida menor: o usuário vê algo na tela muito antes
   da resposta completa estar pronta.
2. Feedback contínuo: é possível detectar mais facilmente se a
   resposta está indo na direção certa e, se necessário, interromper.
3. Melhor experiência em respostas longas: grandes blocos de texto
   deixam de “aparecer do nada” e passam a ser exibidos de forma
   incremental.
4. Integração com interfaces reativas: aplicações em tempo real,
   dashboards e CLIs podem atualizar a UI à medida que os tokens
   chegam, criando experiências mais ricas.

  (first token: 0.452s · total: 2.381s)



----- /config Command -----

You: /config

--- Current Configuration ---
Model: gpt-4o-mini
Temperature: 0.7
top_p: 1.0
Max output tokens: 256
System prompt: You are a helpful assistant. Answer in Brazilian Portuguese.
Colors enabled: True
--- End of config ---



----- Empty Input -----

You:

Empty input. Type a message or '/exit'.



----- 3rd Question -----

You: Me dê um exemplo simples de caso de uso de streaming em linha de comando.

Assistant (streaming...):

Um exemplo simples é exatamente este tipo de cliente de linha de
comando: você faz uma pergunta, e o modelo vai respondendo em tempo
real. Isso é útil quando:

- Você faz perguntas longas ou complexas.
- Quer acompanhar o raciocínio do modelo conforme ele escreve.
- Precisa de sensação de responsividade, mesmo em conexões lentas.

Ferramentas de debug, chat de suporte, assistentes para desenvolvedores
e painéis de monitoramento podem se beneficiar bastante do streaming.

  (first token: 0.365s · total: 1.742s)



----- Exit -----

You: /exit
Goodbye!



============================================================
3. Notes
============================================================

- The client is stateless: each message is independent.
- Streaming uses response.output_text.delta events.
- Latency information is printed after each streamed response.
- Logs are saved under logs/project02-streaming-<timestamp>.log.

End of demo.

