# Policy-to-Rules Converter — POC

> Takes unstructured billing/coding policy text and uses an LLM to produce a plain-language summary, structured machine-readable rules as JSON, and a check that applies those rules to a sample claim.

---

## Overview

This proof of concept demonstrates an end-to-end pipeline for converting raw payer/coding policy documents into actionable, machine-readable rules:

1. **Ingest** — accept raw policy text (paste or file upload)
2. **Summarize** — produce a concise plain-language summary via an LLM
3. **Extract Rules** — emit a validated JSON rule set (structured with Pydantic)
4. **Check Claim** — apply the extracted rules against a sample claim and return a pass/fail result with rationale

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | Python · FastAPI |
| Data Validation | Pydantic |
| LLM | Anthropic API (Claude) |
| Frontend | Minimal HTML/JS (no framework) |

---

## Setup

1. **Copy the example env file** and add your Anthropic API key:

   ```bash
   cp .env.example .env
   ```

2. Open `.env` and set your key:

   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

3. **Never commit `.env`** — it is listed in `.gitignore` and will not be tracked by Git.  
   Only `.env.example` (which contains no real secrets) is committed to the repository.

---

## How to Run

> _Setup and run instructions will be added once the source code is in place._

```bash
# placeholder
pip install -r requirements.txt
uvicorn poc.main:app --reload
```

---

## Repository Structure

```
policy-to-rules-poc/
├── poc/                  # All POC source code and sample data
│   └── samples/          # Sample policy text files for testing
├── report/               # Written report (Word doc, added later)
├── slides/               # PowerPoint presentation (added later)
├── video/                # Demo video recording (added later)
├── resume/               # Resume PDF (added later)
└── README.md
```

---

## Deliverables

- [Written Report](./report/) — detailed write-up of approach, findings, and results
- [Slide Deck](./slides/) — presentation summarizing the POC
- [Demo Video](./video/) — screen-recorded walkthrough of the running application
- [Resume](./resume/) — candidate resume PDF
