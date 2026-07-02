# ResearchOS Architecture

ResearchOS is an autonomous multi-agent AI research lab.

The system takes a user research question and coordinates multiple specialist agents to:

1. Plan the investigation
2. Retrieve relevant research sources
3. Extract claims and evidence
4. Detect contradictions
5. Build a knowledge map
6. Identify research gaps
7. Generate hypotheses
8. Write a cited research report

## Core Components

- Frontend: Next.js
- Backend: FastAPI
- Agent Orchestration: LangGraph
- LLM Provider: Fireworks AI
- Vector Database: Qdrant
- Relational Database: PostgreSQL
- Cache / Queue: Redis
- Deployment: Docker Compose

## Initial Agent Team

- Research Director
- Literature Search Agent
- Evidence Extraction Agent
- Skeptic Agent
- Research Gap Agent
- Hypothesis Agent
- Citation Verifier
- Report Writer