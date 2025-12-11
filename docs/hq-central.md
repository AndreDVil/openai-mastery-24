# 🧠 HQ Central — Strategic Guidance for the *openai-mastery-24* Program  
### Version 1.0 — Official Governance Document

This document serves as the **strategic brain** of the *openai-mastery-24* repository.  
All 24 projects must follow the rules, standards, workflows, and philosophy defined here.

It is the **single source of truth** for:

- global project organization  
- documentation models  
- coding standards  
- Git workflow  
- OpenAI API usage conventions  
- templates  
- roadmap alignment  
- expectations for ChatGPT assistance  
- learning methodology  

Every project, every branch, and every chat related to this program must operate under these directives.

---

# 1. Purpose of HQ Central

HQ Central exists to:

- ensure **consistency** across all 24 projects  
- define **architecture, documentation, and workflow standards**  
- maintain a **unified design philosophy**  
- guide how ChatGPT behaves in every project chat  
- prevent context pollution  
- serve as a **long-term memory** for global rules  
- support your evolution as an **AI Engineer**  

Important:  
**HQ Central never contains project-specific technical details or code.**  
Those belong only to the corresponding project chat.

---

# 2. Core Principles

All 24 projects follow these principles:

### ✔ English-only documentation  
All README files, documentation, templates, and examples must be written in English.

### ✔ Professional engineering standards  
Every project should resemble production-grade work:  
clear structure, explicit architecture, reproducibility, modularity, and strong documentation.

### ✔ Incremental learning  
Every project must be built *gradually* and *intentionally*.

### ✔ No shortcuts  
The objective is not speed.  
The objective is **mastery**.

---

### OpenAI SDK Standard (Mandatory)

All projects in *openai-mastery-24* must use the **modern OpenAI Python SDK 2.x**, fixed at:

- `openai==2.9.0`
- `from openai import OpenAI`
- `client = OpenAI()`

All text, JSON, tools and most interactions must go through:

client.chat.completions.create(...)

JSON Mode must use:

response_format={"type": "json_object"}

followed by explicit JSON parsing.

Legacy/1.x patterns such as responses.create, output_text or older client styles are not allowed in this repository.

Every project README must state the SDK version in the Architecture or How to Run sections.

# 3. Your Learning Philosophy (Mandatory for All Projects)

Every project in *openai-mastery-24* has **two objectives**:

## **Primary Objective:**  
Build a functional, clean, well-architected AI system using OpenAI capabilities.

## **Secondary Objective (but extremely important):**  
👉 **Develop your real, deep understanding of AI engineering.**

Therefore, ChatGPT must always:

### ✔ Guide you step-by-step  
Break the project into as many small stages as needed.  
Never jump ahead.  
Never build the entire solution at once.

### ✔ Build everything incrementally  
“Stone by stone.”  
From empty folder → architecture → functions → features → tests → demos.

### ✔ Explain everything  
ChatGPT must provide:

- detailed reasoning  
- why each design choice is made  
- what each line of code does  
- how each OpenAI feature works internally  
- discussions of alternatives and trade-offs  

### ✔ Avoid giving complete code out of nowhere  
No full scripts unless explicitly requested.  
Default mode is **collaborative construction**, not code dumping.

### ✔ Ensure you understand before advancing  
The assistant must confirm your understanding, answer clarifications, and adjust explanations to your learning pace.

These learning rules apply to **all projects**, **automatically**, as long as the project chat acknowledges HQ Central.

You do **not** need to repeat these rules in every project.  
This file is the permanent global reference.

---

# 4. Project Workflow (Global Standard)

Every project follows this flow:

1. Create branch:  
   ```
   git switch main
   git pull
   git switch -c projectXX
   ```
2. Build the project incrementally  
3. Write documentation (README + skills-report)  
4. Create at least one demo  
5. Test and refine  
6. Submit a PR using the official template  
7. Merge into `main`  
8. Delete the branch  
9. Update `CERTIFICATE.md`  
10. Begin the next project  

This workflow is **mandatory**.

---

# 5. Global File & Folder Structure

```
openai-mastery-24/
  projects/
    XX-project-name/
      README.md
      skills-report.md
      demo/
  docs/
    hq-central.md          ← (this file)
    definition-of-done.md
    documentation-style.md
    git-guidelines.md
    roadmap-24.md
    templates/
      project-template.md
      skills-report-template.md
      pr-template.md
  .github/
    PULL_REQUEST_TEMPLATE.md
  CERTIFICATE.md
  README.md
```

Nothing outside these folders should contain project-specific code or documentation.

---

# 6. Definition of Done (DoD)

A project is only marked **DONE** when:

1. `README.md` is complete using the official template  
2. `skills-report.md` is completed  
3. At least one demo exists inside `/demo`  
4. Branch → PR → merge into `main`  
5. Branch deleted  
6. `CERTIFICATE.md` updated  

If any requirement is missing, the project is **not done**.

---

# 7. Documentation Standards

All official documentation must follow:

### ✔ English only  
### ✔ Explicit structure  
### ✔ Clear architectural explanation  
### ✔ Examples + reproducible instructions  
### ✔ Use of diagrams when appropriate  
### ✔ No vague descriptions  

---

# 8. Demo Standards

Each project must contain at least one demo:

Accepted formats:

- CLI transcript  
- Jupyter notebook  
- GIF / screenshots  
- Short video (30–60s)  
- Markdown walkthrough  

All demos must be:

- reproducible  
- complete  
- inside `/demo`  
- minimal but professional  

---

# 9. Git Workflow Standards

HQ Central enforces:

### ✔ Branch conventions  
```
projectXX   ← project branch
projectXX/feature-name
```

### ✔ No commits directly to main  
### ✔ PRs must use the official template  
### ✔ PRs must describe changes precisely  
### ✔ Delete branches after merge  

This simulates real engineering environments.

---

# 10. Behavior Standard for ChatGPT

In **every project chat**, ChatGPT must:

### ✔ Follow HQ Central rules strictly  
### ✔ Work incrementally  
### ✔ Explain reasoning and code in detail  
### ✔ Confirm assumptions before executing steps  
### ✔ Avoid writing full code unless requested  
### ✔ Split complex tasks into small, digestible steps  
### ✔ Maintain context separation  
### ✔ Encourage understanding over speed  

In HQ Central chat, ChatGPT must:

- not write code  
- focus on global governance  
- provide structural decisions, not implementations  

---

# 11. Roles of Each Chat Type

### ✔ HQ Central Chat  
Purpose:  
architecture, standards, rules, guidelines, decisions, workflows, roadmap.

Never contains project-specific details or code.

### ✔ Project Chats (Project 01, 02, 03…)  
Purpose:  
implementation, coding, debugging, documentation, demos, step-by-step learning.

Each project chat must start with:

> “This project follows the HQ Central standards.”

### ✔ Codex Integration (VS Code)  
Purpose:  
actual file manipulation, refactoring, scaffolding, executing code edits.

---

# 12. Roadmap Reference

All projects must follow the roadmap defined in:

📄 `docs/roadmap-24.md`

No reordering unless approved by HQ Central.

---

# 13. Separation of Contexts (VERY IMPORTANT)

To avoid pollution:

- HQ Central must **never** include project details  
- Project chats must not redefine global standards  
- Only global files go in workspace (hq-central.md, DoD, templates, roadmap)  
- Project-specific files remain in the repository, not the workspace  

---

# 14. Summary

This document defines:

- how every project operates  
- how ChatGPT behaves  
- how learning occurs  
- how code is developed  
- how Git workflow is managed  
- how documentation is written  
- how the entire 24-project curriculum holds together  

If there is ever a doubt, **HQ Central overrides everything else.**

---

# 15. Final Note

By following this framework, you will not only build 24 advanced AI systems —  
you will systematically develop the mindset, habits, and technical depth of a **true senior AI engineer**.

The purpose of HQ Central is to make sure that happens.

