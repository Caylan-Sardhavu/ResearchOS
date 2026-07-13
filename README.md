# ResearchOS

> **The Autonomous AI Research Laboratory**
>
> ResearchOS is a multi-agent AI research platform that autonomously plans investigations, retrieves scientific literature, synthesizes evidence, identifies research gaps, and generates evidence-grounded research reports.

Built for the **AMD Developer Hackathon: ACT II**.

---

# Overview

Academic research is becoming increasingly difficult due to the exponential growth of scientific publications. Researchers spend significant time:

- Searching for relevant papers
- Comparing conflicting findings
- Identifying research gaps
- Writing literature reviews
- Planning future research

ResearchOS automates this workflow using a team of specialized AI agents that collaborate to produce structured, evidence-grounded research investigations.

Instead of simply answering questions, ResearchOS performs a complete research investigation.

---

# Features

### Multi-Agent Research Workflow

ResearchOS dynamically assembles specialized agents depending on the research question.

Current agents include:

- Research Director
- Research Planner
- Literature Review Agent
- Evidence Retrieval Agent
- Research Gap Detector
- Report Writer

---

### Academic Literature Retrieval

Retrieves evidence from:

- arXiv
- Semantic Scholar

Each paper is ranked according to relevance before synthesis.

---

### Literature Review

Automatically performs cross-paper analysis including:

- Common findings
- Conflicting evidence
- Emerging topics
- Shared limitations

---

### Research Gap Detection

ResearchOS identifies evidence-grounded research gaps by comparing multiple papers instead of relying on a single source.

Generated gaps include:

- Missing benchmark comparisons
- Underexplored methodologies
- Evaluation weaknesses
- Future research opportunities

---

### AI Report Generation

Produces professional research reports containing:

- Executive Summary
- Literature Review
- Comparative Analysis
- Research Gaps
- Future Research Directions
- References

Reports are generated using Fireworks AI with deterministic fallbacks when required.

---

### Persistent Research Notebook

Completed investigations are stored locally.

Users can revisit previous investigations without repeating the entire workflow.

---

# System Architecture

```text
                    User Research Question
                             │
                             ▼
                    Research Director
                             │
                             ▼
                    Research Planner
                             │
                             ▼
               Evidence Retrieval Pipeline
             (arXiv + Semantic Scholar)
                             │
                             ▼
                   Paper Ranking Engine
                             │
                             ▼
                  Literature Review Agent
                             │
                             ▼
                 Research Gap Detection
                             │
                             ▼
                    AI Report Writer
                             │
                             ▼
                  Persistent Notebook
```

---

# Workflow

1. User submits a research question.
2. Research Director selects the required agents.
3. Planner decomposes the investigation.
4. Evidence is retrieved from academic databases.
5. Papers are ranked.
6. Literature review is generated.
7. Research gaps are detected.
8. AI generates a research report.
9. Investigation is saved to notebook memory.

---

# Technology Stack

## Backend

- Python
- FastAPI
- Uvicorn

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

## AI

- Fireworks AI

## Research Sources

- arXiv API
- Semantic Scholar API

## Infrastructure

- Docker
- Docker Compose

---

# Project Structure

```text
researchos/

├── apps/
│   ├── backend/
│   └── frontend/
│
├── docs/
│
├── infra/
│
├── packages/
│
├── docker-compose.yml
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/Caylan-Sardhavu/ResearchOS
cd ResearchOS
```

---

## Backend

```bash
cd apps/backend

uv sync

uv run uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd apps/frontend

npm install

npm run dev
```

---

# Docker

Create a root `.env` file:

```env
USE_FIREWORKS=true

FIREWORKS_API_KEY=YOUR_KEY

FIREWORKS_MODEL=YOUR_MODEL

NEXT_PUBLIC_API_URL=http://localhost:8000
```

Then run:

```bash
docker compose up --build
```

---

# Usage

1. Open

```
http://localhost:3000
```

2. Enter a research question.

Example:

```
Investigate recent research on retrieval-augmented generation (RAG) systems for large language models. Compare retrieval strategies, evaluation methodologies, benchmark results, identify evidence-grounded research gaps, and recommend future research directions.
```

3. ResearchOS will automatically:

- retrieve literature
- rank papers
- synthesize findings
- identify research gaps
- generate an AI research report
- save the investigation

---

# Example Output

ResearchOS generates reports including:

- Executive Summary
- Research Objective
- Literature Review
- Comparative Analysis
- Research Gaps
- Future Research Directions
- References

---

# Future Work

- PDF full-text retrieval
- Citation graph analysis
- Multi-agent debate
- Local vector database
- Collaborative research workspaces
- AMD GPU benchmarking integration

---

# Team

Developed for the **AMD Developer Hackathon: ACT II**.

---

# License

MIT License