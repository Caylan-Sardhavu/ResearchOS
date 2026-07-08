# ResearchOS Technical Blueprint

## Product Vision

ResearchOS is an autonomous AI research laboratory.

A user enters a research question. ResearchOS checks previous notebook entries, dynamically assembles a specialist research team, retrieves evidence, identifies gaps, and produces a structured research report.

## Hackathon MVP Scope

### Build Now

- FastAPI backend
- Research Director
- Dynamic team assembly
- Research Notebook memory lookup
- Fireworks-ready AI planning
- Real paper/document retrieval
- Basic research report generation
- Simple frontend dashboard

### Future Roadmap

- Continuous monitoring of new papers
- Research project evolution over time
- Full knowledge graph
- Background scheduled research updates
- Team collaboration features

## Core Backend Architecture

```text
User
  ↓
Frontend
  ↓
FastAPI API Layer
  ↓
Research Director
  ↓
Notebook Service + Planning Engine
  ↓
Specialist Agents
  ↓
Evidence Store
  ↓
Report Writer
  ↓
Research Notebook