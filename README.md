# ResearchOS

> **The Autonomous AI Research Laboratory**

ResearchOS is a multi-agent AI research platform that transforms a natural-language research question into an evidence-grounded investigation.

It plans the investigation, retrieves academic papers from arXiv, ranks evidence, analyzes literature, identifies research gaps, generates a structured report, and saves completed investigations in persistent notebook memory.

Built for the **AMD Developer Hackathon: ACT II**.

---

## Overview

Researchers often spend significant time:

- searching for relevant papers
- comparing findings across studies
- identifying limitations and contradictions
- discovering research gaps
- planning future experiments
- writing literature reviews

ResearchOS automates this workflow using a team of specialized AI agents coordinated by a central Research Director.

Instead of returning a single chatbot response, ResearchOS performs a complete research investigation.

---

## Core Features

### Multi-Agent Research Workflow

ResearchOS uses specialized agents with separate responsibilities:

- **Research Director** — analyzes the question, estimates complexity, checks notebook memory, and selects specialist agents
- **Research Planner** — creates an objective, subquestions, and search queries
- **Literature Specialist** — retrieves academic papers from arXiv
- **Evidence Synthesizer** — compares findings and limitations across papers
- **Research Gap Detector** — identifies underexplored research opportunities
- **Report Writer** — produces a structured, evidence-grounded research report

---

### arXiv Evidence Retrieval

ResearchOS searches arXiv for relevant academic papers.

The evidence pipeline:

1. runs multiple search queries
2. normalizes paper metadata
3. removes duplicates
4. ranks papers by relevance
5. passes the strongest evidence to downstream analysis

---

### Cross-Paper Literature Analysis

ResearchOS analyzes multiple papers together rather than summarizing them independently.

The system identifies:

- common findings
- repeated limitations
- emerging themes
- conflicting evidence
- missing evaluations
- possible future research directions

---

### Research Gap Detection

ResearchOS generates specific research opportunities based on the retrieved literature.

Examples include:

- missing benchmark comparisons
- inconsistent evaluation methodologies
- underexplored optimization strategies
- absent hardware-specific studies
- unresolved methodological contradictions
- missing datasets or experiments

---

### Evidence-Grounded Reports

ResearchOS produces structured Markdown reports with sections such as:

- Executive Summary
- Research Objective
- Identified Research Gaps
- Current State of the Literature
- Key Findings
- Comparative Analysis
- Future Research Directions
- Limitations
- References

Reports are generated using Fireworks AI.

Every AI-powered stage includes deterministic fallback behavior so the system can continue functioning if an external model fails or returns invalid output.

---

### Persistent Research Notebook

Completed investigations are stored in notebook memory.

Users can:

- revisit previous investigations
- reopen saved reports
- inspect prior research gaps
- review selected agents
- avoid repeating the same investigation

The current notebook implementation uses local JSON storage.

---

### Live Investigation Timeline

The frontend visualizes the research process as it happens:

- Research Director
- Planning Investigation
- Collecting Evidence
- Analyzing Literature
- Writing Report
- Investigation Complete

This makes the system feel like an autonomous research laboratory rather than a standard chatbot.

---

## System Architecture

```text
User Research Question
        |
        v
Research Director
        |
        v
Research Planner
        |
        v
Notebook Memory Lookup
        |
        v
arXiv Evidence Retrieval
        |
        v
Paper Ranking
        |
        v
Paper Analysis
        |
        v
Literature Review
        |
        v
Research Gap Detection
        |
        v
Fireworks Report Writer
        |
        v
Notebook Save
        |
        v
Frontend Results Dashboard
```

---

## Research Workflow

1. The user submits a research question.
2. The Research Director analyzes the question.
3. Previous notebook investigations are checked.
4. The Planner creates an investigation strategy.
5. arXiv papers are retrieved.
6. Papers are deduplicated and ranked.
7. Individual papers are analyzed.
8. Cross-paper findings and limitations are synthesized.
9. Research gaps are identified.
10. Fireworks AI generates the final report.
11. The investigation is saved to notebook memory.
12. The frontend displays results in dedicated tabs.

---

## Frontend

The ResearchOS frontend is designed to feel like an autonomous research laboratory.

Current interface features include:

- futuristic dark-purple research UI
- investigation timeline
- dynamic agent cards
- evidence cards
- research gap cards
- formatted research reports
- notebook history
- saved investigation replay
- backend system status

---

## Technology Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- React Markdown
- Remark GFM

### Backend

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- HTTPX
- AsyncIO

### AI

- Fireworks AI
- OpenAI-compatible Fireworks API

### Research Source

- arXiv API

### Infrastructure

- Docker
- Docker Compose
- uv
- GitHub

---

## Project Structure

```text
researchos/
├── apps/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── agents/
│   │   │   ├── api/
│   │   │   ├── core/
│   │   │   ├── knowledge/
│   │   │   ├── models/
│   │   │   ├── services/
│   │   │   ├── workflows/
│   │   │   └── main.py
│   │   ├── Dockerfile
│   │   └── pyproject.toml
│   │
│   └── frontend/
│       ├── app/
│       ├── components/
│       ├── public/
│       ├── Dockerfile
│       └── package.json
│
├── docs/
├── infra/
├── packages/
├── scripts/
├── docker-compose.yml
└── README.md
```

---

## Run with Docker

### 1. Clone the repository

```bash
git clone https://github.com/Caylan-Sardhavu/ResearchOS.git
cd ResearchOS
```

### 2. Create the root environment file

Create a file named `.env` in the repository root:

```env
USE_FIREWORKS=true
FIREWORKS_API_KEY=your_fireworks_api_key
FIREWORKS_MODEL=your_fireworks_model_id
FIREWORKS_BASE_URL=https://api.fireworks.ai/inference/v1
FIREWORKS_MAX_TOKENS=3200
FIREWORKS_TEMPERATURE=0.2
FIREWORKS_TIMEOUT_SECONDS=120
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Do not commit the real `.env` file.

### 3. Build and start ResearchOS

```bash
docker compose up --build
```

### 4. Open the application

Frontend:

```text
http://localhost:3000
```

Backend health:

```text
http://localhost:8000/health
```

Backend API docs:

```text
http://localhost:8000/docs
```

### 5. Stop the application

```bash
docker compose down
```

---

## Run Locally Without Docker

### Backend

```bash
cd apps/backend
uv sync
uv run uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

### Frontend

Open a second terminal:

```bash
cd apps/frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:3000
```

Create `apps/frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Example Research Question

```text
Investigate recent research on retrieval-augmented generation systems for large language models. Compare retrieval strategies, evaluation methodologies, and benchmark results across the retrieved papers. Identify four specific evidence-grounded research gaps and recommend realistic future experiments.
```

---

## Example AMD-Focused Question

```text
Identify the most important unresolved research gaps in efficient transformer inference on AMD GPUs. Compare optimization strategies, evaluation methodologies, hardware constraints, and reported bottlenecks across the retrieved literature. Propose four realistic future experiments for AMD MI300X or ROCm-based systems.
```

---

## API Endpoints

### Health Check

```http
GET /health
```

### Run a Research Investigation

```http
POST /research
```

Example request:

```json
{
  "question": "What are the most important unresolved research gaps in retrieval-augmented generation?"
}
```

### Notebook History

```http
GET /notebook
```

### Load a Saved Investigation

```http
GET /notebook/{id}
```

---

## Reliability Design

ResearchOS follows a graceful-degradation architecture.

Every AI-powered component has deterministic fallback behavior.

If Fireworks:

- times out
- becomes unavailable
- returns invalid JSON
- returns incomplete output

ResearchOS continues using deterministic Python logic.

This reduces quality gracefully without stopping the investigation.

---

## AMD Relevance

ResearchOS was developed for the AMD Developer Hackathon: ACT II.

The system supports research questions involving:

- AMD Instinct GPUs
- AMD MI300X
- ROCm
- transformer inference
- GPU performance optimization
- hardware benchmarking
- kernel auto-tuning
- performance portability

ResearchOS is domain-independent, but its planning and research workflows can support AMD-focused technical investigations.

---

## Current Limitations

- Evidence retrieval currently uses arXiv only.
- Analysis relies primarily on titles and abstracts.
- Notebook storage currently uses JSON.
- Full-text PDF analysis is not yet implemented.
- Research quality depends on the relevance of retrieved papers.
- Some Fireworks responses may use deterministic fallback behavior.

---

## Future Work

- full-text PDF retrieval and analysis
- OpenAlex integration
- Semantic Scholar integration
- citation graph analysis
- interactive citations
- research confidence scoring
- AI Research Advisor
- AI Research Critic
- experiment design agent
- SQLite or PostgreSQL notebook storage
- vector similarity search
- live streaming workflow updates
- AMD ROCm benchmark integration
- publication-ready PDF export

---

## Design Principles

1. Evidence before generation
2. Python orchestrates; AI reasons
3. Every AI stage has a deterministic fallback
4. Notebook memory is checked before retrieval
5. Every agent has one responsibility
6. Reports must remain evidence-grounded
7. Never fabricate citations
8. Every stage should be independently testable

---

## Team

Developed by:

- Caylan Sardhavu
- ResearchOS Team

Built for the **AMD Developer Hackathon: ACT II**.

---

## License

This project is available under the MIT License.