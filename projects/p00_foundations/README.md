# Project 00 — Foundations  
**OpenAI Mastery 24 — Understanding the Core Mechanics of the OpenAI API**

This project establishes the essential foundations for the entire 24-project journey.  
Here, we build a deep understanding of:

- How the OpenAI Python SDK works  
- How to authenticate and call models  
- How to inspect responses  
- How temperature and top_p influence outputs  
- How to compare models (latency, tokens, style)  
- How to estimate cost per request

This project is intentionally simple — but contains the core skills that every future project depends on.

---

## 📁 Project Structure

```
00-foundations/
│
├── foundations-demo.ipynb        # Main experiment notebook
├── demo/
│   └── foundations-demo.html     # Exported notebook (viewable demo)
│
├── README.md                     # This document
└── skills-report.md              # Summary of competencies acquired
```

---

## 📘 Notebook Blocks Overview

### Block 1 — Client Setup
- Load environment variables  
- Initialize the OpenAI Python client  
- Validate API key  

Learned:
- How the SDK is structured  
- Best practices using `.env`  
- Why a global client instance matters  

---

### Block 2 — First API Call (`responses.create`)
- Send a minimal prompt to `"gpt-4o-mini"`  
- Retrieve text via `response.output_text`  
- Inspect the raw response object  

Learned:
- Anatomy of a Response API call  
- Using `response.output_text`  
- Understanding `usage` (input/output tokens)  

---

### Block 3 — Temperature vs Top-P
- Generate outputs with varying `temperature`  
- Generate outputs with varying `top_p`  
- Understand randomness vs sampling diversity  

Learned:
- Temperature → randomness  
- Top-p → probability truncation  
- Why some prompts show small differences while others show strong effects  

---

### Block 4 — Model Comparison
Models tested:  
- `gpt-4o-mini`  
- `gpt-4o`  
- `gpt-4.1-mini`

Measured:
- Latency  
- Token usage  
- Style and length variability  

Insights from your real results:
- `4o-mini` → more verbose, sensory-rich  
- `4o` → balanced, polished, concise  
- `4.1-mini` → formal and efficient  

Learned:
- How text length affects latency and cost  
- Why model selection is a trade-off (speed × quality × price)  

---

### Block 5 — Cost Estimation
- Defined a price table  
- Computed cost per request based on real token counts  

Learned:
- How tokens map to $$$  
- How to estimate pricing for applications  
- Why smaller models are ideal for high-volume workloads  

---

## 🧪 Demo Output

A static HTML export of the notebook is included at:

```
00-foundations/demo/foundations-demo.html
```

Use this file to review or present the project quickly.

---

## 🎯 Learning Outcomes Summary

By completing Project 00, you now understand:

- OpenAI API basics  
- How responses are structured  
- What tokens, latency, and cost mean  
- How sampling parameters affect generation  
- How to compare different models empirically  
- How to build reproducible experiments in notebooks  

This foundation will be reused in **every** future project.

