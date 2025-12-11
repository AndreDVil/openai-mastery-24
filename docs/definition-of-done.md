# Definition of Done (DoD) – openai-mastery-24  
**Versão oficial do HQ CENTRAL**

Este documento define os critérios mínimos para considerar qualquer um dos 24 projetos como **completamente concluído** dentro da trilha openai-mastery-24.

Ele garante consistência, profissionalismo e rastreabilidade ao longo de todo o repositório.

---

## ✅ 1. Estrutura obrigatória do projeto

Cada projeto deve conter:

```
projects/XX-name/
  README.md
  skills-report.md
  demo/
    (pelo menos um demo)
```

---

## ✅ 2. README.md completo

O README deve seguir **integralmente** o template oficial definido no *Documentation Style Guide*:

1. Overview  
2. Objectives  
3. OpenAI Features Explored  
4. Architecture  
5. How to Run  
6. Results & Examples  
7. Skills Developed  
8. Future Improvements  

O README deve estar claro, conciso, em inglês, com trechos executáveis quando aplicável.

---

## ✅ 3. Skills Report preenchido

O arquivo `skills-report.md` deve seguir o template oficial e conter:

- lista de habilidades adquiridas  
- caixas de seleção concluídas  
- evidências de proficiência  
- reflexão sobre limitações e próximos passos  

O objetivo é demonstrar **aprendizado real**, não apenas funcionamento técnico.

---

## ✅ 4. Pelo menos um demo funcional

Local obrigatório:

```
projects/XX-name/demo/
```

Formatos aceitos conforme *Demo Guidelines*:

- Jupyter Notebook  
- CLI transcript  
- GIF/screenshot sequence  
- Vídeo curto  
- Arquivo markdown com execução real  

Checklist de demo:

- [x] demonstração real da aplicação  
- [x] fluxo completo  
- [x] reprodutível  
- [x] explicação descritiva  
- [x] dentro da pasta `/demo`  

---

## ✅ 5. Branch de projeto + PR obrigatório

Fluxo conforme *Git Rules*:

### 1. Criar branch do projeto:
```
git switch -c projectXX
```

### 2. Se necessário, criar feature branches:
```
projectXX/feature-<nome>
```

### 3. O PR deve conter:
- título padronizado  
- resumo  
- mudanças  
- como rodar  
- validações/testes  
- checklist de conformidade  

### 4. O PR deve ser aprovado e feito merge para `main`.

### 5. Após merge:
- apagar branch local  
- apagar branch remoto  

---

## ✅ 6. Código estável, organizado e documentado

O código deve:

- conter funções claras  
- possuir docstrings  
- evitar hardcodes de keys  
- ser executável por terceiros  
- respeitar a estrutura do projeto  

O objetivo é desenvolver maturidade real de engenharia.

---

## ✅ 7. Atualização do CERTIFICATE.md

Após concluir o projeto:

- marcar “Completed”  
- adicionar data  
- adicionar link para README  
- adicionar link para demo  
- registrar principais competências  

O arquivo CERTIFICATE.md é a trilha auditável do progresso.

---

## ✅ 8. Toda verificação final deve passar pelo HQ CENTRAL

Antes de considerar um projeto concluído:

- Verificar consistência  
- Confirmar aderência a todos os itens  
- Confirmar alinhamento com os padrões globais  



## ✅ 9. OpenAI SDK compliance

- All code must use the OpenAI Python SDK 2.9.0.
- The unified `OpenAI()` client must be used (`from openai import OpenAI; client = OpenAI()`).
- Legacy 1.x-style calls (e.g. `responses.create`, `output_text`, old clients) are not allowed.
- The README must mention the SDK version explicitly.
---

Somente então o projeto é oficialmente marcado como **DONE**.

# ✔ Conclusão

Um projeto só está finalizado quando atende **todos** os critérios acima.  
Se faltar qualquer item, o HQ CENTRAL considera o projeto **pendente**.

