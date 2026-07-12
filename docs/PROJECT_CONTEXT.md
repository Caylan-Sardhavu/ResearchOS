# ResearchOS Project Context

> **Project:** ResearchOS — The Autonomous AI Research Laboratory  
> **Purpose:** Canonical source of truth for continuing development  
> **Status:** Active development  
> **Original context:** AMD Developer Hackathon  
> **Last updated:** July 2026

This document contains the architecture, implementation status, development history, design decisions, current workflow, known issues, and roadmap for ResearchOS.

A developer or future ChatGPT instance should be able to read this file and continue development without requiring the user to repeat previous discussions.

---

# Table of Contents

1. Project Overview
2. Project Goals and Objectives
3. Hackathon Context and Requirements
4. Architectural Principles
5. Overall System Architecture
6. Technology Stack
7. Repository and Folder Structure
8. Backend Architecture
9. Frontend Architecture
10. Agent System
11. Research Workflow
12. Memory and Notebook System
13. Evidence Collection Pipeline
14. Literature Review Pipeline
15. Research Gap Detection
16. Report Generation
17. API Endpoints
18. Data Models and Schemas
19. External APIs and Integrations
20. AMD-Specific Features
21. Environment Setup
22. Running the Project
23. Testing Workflow
24. Coding Conventions
25. Current Implementation Status
26. Completed Features
27. Partially Completed Features
28. Planned Features
29. Known Bugs and Current Issues
30. Design Decisions
31. Important Discussions and Decisions
32. Development History
33. Current TODO List
34. Current Working State
35. Immediate Next Steps
36. Long-Term Roadmap
37. Repository File Reference
38. Engineering Playbook
39. Architecture Decision Records
40. Lessons Learned

# 1. Project Overview

## Project Name

ResearchOS

Alternative descriptive name:

> The Autonomous AI Research Laboratory

ResearchOS is an AI-powered multi-agent research system that automatically performs literature investigations from a natural-language research question.

Unlike traditional search engines or single-LLM assistants, ResearchOS is designed around a team of specialized AI agents coordinated by a Research Director.

Each investigation is treated as an autonomous research project.

The system:

- understands the question
- recalls previous investigations
- creates an investigation strategy
- assembles specialist AI agents
- retrieves evidence
- analyzes papers
- compares literature
- identifies research gaps
- writes an evidence-grounded report
- stores the investigation for future reuse

The long-term vision is to create an "AI Research Operating System" rather than another chatbot.

---

# 2. Vision

ResearchOS should eventually feel like working alongside a team of professional researchers.

Instead of asking:

> "Summarize these papers"

the user should be able to ask:

> "Find an unexplored research direction in AMD GPU inference optimization."

ResearchOS should determine:

- which experts are needed
- where evidence exists
- where evidence is weak
- where literature disagrees
- which experiments should be performed
- what novel research questions exist

Eventually the system should function more like a research collaborator than a search tool.

---

# 3. Project Goals

Primary goals:

• Autonomous research planning

• Dynamic multi-agent collaboration

• Evidence-grounded reasoning

• Academic literature analysis

• Cross-paper synthesis

• Research gap discovery

• Automatic report generation

• Persistent research notebook

• Reusable investigations

---

Secondary goals

The system should eventually recommend:

- new research directions

- proposed experiments

- publication venues

- novelty estimates

- confidence estimates

- peer-review style criticism

---

# 4. Hackathon Context

This project was originally developed for the AMD Developer Hackathon.

Important constraints influenced architecture.

## Time constraints

Initially only approximately two weeks.

Later reduced to only a few hours.

Finally extended by one additional day.

Because of this:

Several large ideas were intentionally postponed.

Examples:

❌ Vector databases

❌ LangGraph

❌ Distributed agents

❌ Long-term autonomous evolution

❌ Kubernetes deployment

Instead development focused on producing an impressive end-to-end demonstration.

---

# 5. High-Level Architecture

The complete workflow is:

User

↓

Research Director

↓

Research Planner

↓

Evidence Retrieval

↓

Paper Ranking

↓

Paper Analysis

↓

Literature Review

↓

Research Gap Detection

↓

Report Writer

↓

Notebook Memory

↓

Frontend Dashboard

Every stage has a single responsibility.

Every stage can be independently upgraded.

Whenever possible:

Fireworks AI performs reasoning.

Deterministic Python logic acts as fallback.

---

# 6. Design Philosophy

Several architectural principles have guided every implementation decision.

## Principle 1

Evidence before generation.

ResearchOS should never invent evidence.

Evidence must always be collected first.

---

## Principle 2

AI should reason.

Python should orchestrate.

The deterministic backend should coordinate work while Fireworks performs reasoning.

---

## Principle 3

Every AI component requires a deterministic fallback.

If Fireworks:

fails

times out

returns invalid JSON

becomes unavailable

ResearchOS should still function.

Only quality should degrade.

Never availability.

---

## Principle 4

Notebook memory comes first.

Every investigation begins by checking previous research.

ResearchOS should leverage its own knowledge before searching externally.

---

## Principle 5

Agents should be modular.

Each agent performs one responsibility.

This makes the system easier to improve independently.

---

## Principle 6

Reports should always be evidence grounded.

The Report Writer must use retrieved evidence.

It should never fabricate papers.

---

## Principle 7

Every stage should be independently testable.

Every service should be testable without running the entire workflow.

---

# 7. Overall Architecture

ResearchOS consists of three major systems.

Frontend

↓

Backend

↓

External AI and Literature Services

---

Frontend

Next.js

TypeScript

TailwindCSS

Responsible only for:

User interaction

Visualization

Notebook browsing

Timeline

Report viewing

---

Backend

FastAPI

Python

Coordinates the entire workflow.

Contains:

Director

Planner

Evidence retrieval

Analysis

Notebook

Report Writer

Fireworks integration

---

External Services

Fireworks AI

arXiv

Semantic Scholar

Future:

CrossRef

OpenAlex

PubMed

---

# 8. Technology Stack

Frontend

Next.js

TypeScript

React

TailwindCSS

---

Backend

Python 3.12

FastAPI

Pydantic

HTTPX

AsyncIO

OpenAI SDK (configured for Fireworks API)

---

AI

Fireworks AI

Current production model:

DeepSeek V4 Flash

Fireworks is accessed using its OpenAI-compatible endpoint.

---

Research Sources

arXiv

Semantic Scholar

Future:

CrossRef

OpenAlex

PubMed

---

Development

VS Code

Git

GitHub

uv

Uvicorn

---

# 9. Repository Structure

Current project layout (simplified)

researchos/

apps/

backend/

app/

agents/

api/

core/

knowledge/

models/

services/

workflows/

main.py

frontend/

app/

components/

public/

README.md

---

Backend responsibilities

agents/

Agent orchestration.

services/

Business logic.

knowledge/

Notebook memory.

models/

Pydantic models.

workflows/

Research pipeline.

core/

Configuration.

api/

FastAPI routes.

---

Frontend responsibilities

components/

Reusable UI.

page.tsx

Main dashboard.

Sidebar

Notebook history.

ResultsTabs

Tabbed report display.

Timeline

Live investigation progress.

Hero

Landing section.

SearchPanel

Research query input.

---

# 10. Current User Experience

The intended user experience is:

Open ResearchOS

↓

Enter research question

↓

Watch live investigation timeline

↓

Observe selected AI agents

↓

Review evidence

↓

Inspect synthesized research gaps

↓

Read complete report

↓

Automatically save investigation

↓

Reuse investigation later

The experience is intended to feel closer to supervising an autonomous research team than chatting with a single assistant.

---

# 11. Current AI Workflow (High Level)

1.

Director

↓

2.

Planner

↓

3.

Evidence Collection

↓

4.

Ranking

↓

5.

Paper Analysis

↓

6.

Literature Review

↓

7.

Gap Detection

↓

8.

Report Writer

↓

9.

Notebook Save

↓

10.

Frontend Display

Each of these stages will be documented individually in later sections of this document.

# 12. Backend Architecture

## Overview

The backend is the orchestration engine of ResearchOS.

It is responsible for transforming a natural language research question into an evidence-grounded research report.

Unlike traditional REST APIs, the backend behaves more like a workflow engine.

Each stage performs exactly one responsibility before passing structured data to the next stage.

The backend intentionally separates:

- orchestration
- reasoning
- evidence retrieval
- report generation

This architecture makes every stage independently replaceable and testable.

---

# Backend Layer Responsibilities

The backend is organized into the following layers.

```

API

↓

Workflow

↓

Services

↓

Models

↓

Knowledge

↓

External APIs

```

---

# API Layer

Purpose

Expose REST endpoints to the frontend.

The API layer contains almost no business logic.

Responsibilities:

• Receive requests

• Validate input

• Invoke workflow

• Return structured responses

Files

```

app/api/

```

Future

Authentication and streaming endpoints may eventually live here.

---

# Workflow Layer

Purpose

Coordinates the entire investigation.

The workflow does **not** perform reasoning itself.

Instead it invokes specialist services in order.

Current implementation

```

ResearchWorkflow

```

File

```

app/workflows/research_graph.py

```

Responsibilities

1.

Receive question.

↓

2.

Director planning.

↓

3.

Planner.

↓

4.

Evidence retrieval.

↓

5.

Ranking.

↓

6.

Paper analysis.

↓

7.

Literature review.

↓

8.

Gap detection.

↓

9.

Report writing.

↓

10.

Notebook save.

↓

11.

Return API response.

The workflow should remain deterministic.

Only specialist services should use Fireworks.

---

# Service Layer

Every service performs one responsibility.

Services communicate using Pydantic models.

Current services

Research Director

Planner

Evidence

Ranking

Paper Summarizer

Literature Review

Gap Detector

Report Writer

Fireworks

Notebook

Each service is documented below.

---

# 13. Research Director

Purpose

Acts as the "Chief Scientist" of ResearchOS.

The Director decides how the investigation should begin.

Responsibilities

• Inspect question

• Estimate complexity

• Search notebook

• Select specialist agents

• Generate director notes

• Decide whether AI or fallback planning was used

Inputs

Natural language question

Outputs

ResearchResponse

Contains

complexity

selected_agents

notebook_matches

director_notes

ai_used

Current implementation

Initially rule-based.

Later upgraded with Fireworks.

If Fireworks fails

↓

Falls back to deterministic agent selection.

Important design decision

The Director should NEVER retrieve papers.

The Director only plans.

Future improvements

Dynamic agent creation

Budget estimation

Reasoning depth estimation

Agent dependency graphs

---

# 14. Planner Service

Purpose

Convert a broad research question into a structured investigation.

Current outputs

Objective

Subquestions

Search queries

Example

Question

```

Research gaps in transformer inference optimization for AMD GPUs

```

Planner produces

Objective

↓

Investigate transformer inference optimization on AMD GPUs

Subquestions

↓

Which AMD GPUs?

Which benchmarks?

What optimization methods?

What limitations?

Search Queries

↓

AMD GPU performance

Transformer inference

ROCm optimization

LLM inference AMD GPU

Fireworks Upgrade

Originally deterministic.

Now uses Fireworks when available.

Fallback

Keyword rules.

Files

```

services/planner.py

```

Future

Recursive decomposition

Automatic search refinement

Query expansion

---

# 15. Evidence Service

Purpose

Collect research papers.

Sources

Current

arXiv

Semantic Scholar

Future

OpenAlex

CrossRef

PubMed

IEEE

ACM

Responsibilities

Perform multiple searches.

Merge papers.

Remove duplicates.

Return standardized Paper objects.

Evidence Service NEVER summarizes papers.

It only retrieves.

Files

```

services/evidence.py

```

Dependencies

arxiv.py

semantic_scholar.py

Future

Parallel retrieval

Citation graph expansion

Open-access PDF download

---

# 16. Ranking Service

Purpose

Determine which retrieved papers are most relevant.

Current implementation

Deterministic scoring.

Factors

Keyword overlap

Title similarity

Summary similarity

Returns

Ranked papers.

Future

Fireworks semantic ranking.

Embedding similarity.

Cross-paper importance.

---

# 17. Paper Summarizer

Purpose

Transform each paper into structured knowledge.

Output model

PaperAnalysis

Contains

paper_title

key_findings

limitations

research_gaps

confidence

Current implementation

Rule-based extraction.

Future

Fireworks paper reasoning.

Expected improvements

Better limitation detection.

Method extraction.

Experimental setup extraction.

Dataset extraction.

Metric extraction.

---

# 18. Literature Review Service

Purpose

Compare papers.

Unlike the Paper Summarizer,

this service reasons across papers.

Responsibilities

Identify

Common findings

Repeated limitations

Emerging topics

Cross-paper gaps

Confidence

Current implementation

Deterministic aggregation.

Recently began Fireworks integration.

Architecture

Fireworks

↓

Structured synthesis

↓

Fallback

↓

Original aggregation logic

Known issue

Large JSON responses from Fireworks occasionally become malformed or truncated.

Current strategy

Maintain deterministic fallback.

Future strategy

Generate structured Markdown instead of JSON to improve reliability.

---

# 19. Gap Detector

Purpose

Identify research opportunities.

Current implementation

Aggregates paper-level research gaps.

Future implementation

Fireworks cross-paper reasoning.

Target outputs

Missing experiments

Missing benchmarks

Repeated limitations

Contradictions

Novel opportunities

Long-term goal

Gap Detector becomes the primary innovation engine of ResearchOS.

---

# 20. Report Writer

Purpose

Generate the final research report.

Current implementation

Fireworks-powered.

Fallback

Markdown template.

Current report sections

Executive Summary

Research Objective

Current Literature

Key Findings

Comparative Analysis

Research Gaps

Future Directions

Known improvement

Frontend currently renders raw markdown.

Planned improvement

Render report as professional research paper cards.

Future sections

Evidence Matrix

Consensus

Contradictions

Confidence

Suggested Experiments

---

# 21. Fireworks Service

Purpose

Provide a centralized interface for every AI call.

Important design principle

No service communicates directly with Fireworks.

Everything goes through

FireworksService

Advantages

Centralized configuration

Consistent error handling

Single API key

Shared timeout

Shared model

Shared fallback behavior

Current model

DeepSeek V4 Flash

Architecture

Service

↓

FireworksService

↓

OpenAI SDK

↓

Fireworks Endpoint

Fallback philosophy

Every AI failure returns structured data.

Never crashes workflow.

Known issue

Models occasionally return invalid JSON.

Current mitigation

Validation

JSON extraction

Fallback

Future improvements

Retry mechanism

Streaming

Function calling

Structured outputs

---

# 22. Notebook System

Purpose

Persistent memory.

Every completed investigation is stored.

Current stored information

Question

Summary

Research gaps

Selected agents

Paper titles

Full report

Timestamp

Current storage

JSON

Future

SQLite

PostgreSQL

Vector search

Notebook-first philosophy

Every investigation begins with notebook search before evidence retrieval.

---

# 23. Current Backend Pipeline

Current execution order

User Question

↓

Research Director

↓

Planner

↓

Evidence Retrieval

↓

Ranking

↓

Paper Summarizer

↓

Literature Review

↓

Gap Detector

↓

Report Writer

↓

Notebook Save

↓

Frontend Response

Every stage produces structured models.

No stage directly manipulates frontend data.

This separation was intentional to keep the workflow modular, testable, and easy to evolve.

# 24. Frontend Architecture

## Overview

The frontend is the visual interface of ResearchOS.

Unlike a traditional CRUD application, the frontend is designed to make the user feel like they are supervising an autonomous AI research laboratory.

Every visual component exists to reinforce that illusion.

Instead of simply displaying results, the interface visualizes the investigation process.

Primary goals:

• feel futuristic

• emphasize AI collaboration

• visualize investigation progress

• make reports easy to consume

• encourage repeated investigations

The frontend intentionally separates presentation from business logic.

All research logic remains inside the backend.

---

# Technology

Framework

Next.js

Language

TypeScript

UI

React

Styling

TailwindCSS

Communication

REST API

Current backend endpoint

http://127.0.0.1:8000

---

# Frontend Philosophy

Several design decisions were made throughout development.

## The interface should feel alive.

Rather than waiting silently for a report...

ResearchOS shows:

Director thinking

↓

Planner working

↓

Evidence collection

↓

Gap detection

↓

Report generation

This dramatically improves perceived intelligence.

---

## The report should not appear instantly.

Even if the backend responds quickly,

the investigation timeline intentionally continues for a short period.

Reason:

Users trust systems more when they can observe reasoning steps.

Timeline duration is intentionally slower than the backend.

---

## Results are organized by task rather than raw JSON.

Instead of one large response,

ResearchOS separates information into tabs.

Overview

Agents

Evidence

Research Gaps

Report

This mirrors the workflow of a real research investigation.

---

# Main Page

File

app/page.tsx

Purpose

Acts as the main orchestration layer for the frontend.

Responsibilities

Maintain application state.

Invoke backend.

Display notebook.

Display timeline.

Display results.

Current state variables

Question

Loading state

Current investigation

Notebook investigation

Timeline stage

Errors

Notebook refresh key

This file intentionally contains almost no business logic.

It coordinates components.

---

# Hero Component

Purpose

Landing section.

Introduces ResearchOS.

Communicates identity.

Current design

ResearchOS logo

Large heading

Subtitle

Dark futuristic appearance

Visual goal

Immediately communicate

"This is not a chatbot."

---

# Universe Visual

Purpose

Decorative.

Appears in top-right.

Design

Purple orbital system

Stars

Glowing nucleus

Concentric orbit rings

Reason

ResearchOS should feel like a research operating system.

Not another dashboard.

This visual was inspired by scientific visualization rather than enterprise software.

---

# Search Panel

Purpose

Accept user research question.

Current controls

Question textbox

Start Investigation button

Loading indicator

Responsibilities

Input validation.

Disable repeated requests.

Trigger backend.

No AI logic exists here.

---

# Investigation Timeline

Purpose

Visualize autonomous investigation.

Current stages

Research Director

↓

Planning Investigation

↓

Collecting Evidence

↓

Analyzing Literature

↓

Writing Report

↓

Investigation Complete

Each stage activates sequentially.

Timeline intentionally progresses slightly slower than backend completion.

Reason

Creates perception of intelligent work.

Future improvements

Streaming updates.

Agent-specific messages.

Live evidence counts.

---

# Sidebar

Purpose

Persistent navigation.

Current sections

Home

Director

Agents

Evidence

Notebook

Reports

Research History

System Status

Notebook history loads automatically.

Each investigation becomes immediately available.

System status displays backend readiness.

Future improvements

Recent AI activity.

Notebook search.

Folders.

Pinned investigations.

---

# Results Tabs

Purpose

Separate different investigation outputs.

Current tabs

Overview

Agents

Evidence

Research Gaps

Report

Reason

Allows users to inspect specific stages individually.

Much cleaner than one scrolling page.

---

# Overview Tab

Purpose

High-level investigation summary.

Current cards

Complexity

Papers Found

AI Used

Research Director Notes

Notebook Matches

Future additions

Confidence score

Investigation duration

Evidence strength

Consensus indicator

---

# Agents Tab

Purpose

Explain why specialist agents were selected.

Current display

Agent name

Department

Role

Description

Future improvements

Agent avatars

Live thinking

Conversation between agents

Execution times

AI confidence

---

# Evidence Tab

Purpose

Display strongest retrieved papers.

Current information

Title

Year

Source

Relevance score

Summary

Paper link

Future improvements

Citation counts

PDF preview

Methodology extraction

Datasets

Evidence strength

---

# Research Gaps Tab

Purpose

Display synthesized research opportunities.

Current implementation

Attempts to extract

## Identified Research Gaps

from report.

If successful

↓

Displays AI Synthesized badge.

Otherwise

↓

Displays fallback gaps.

Current card design

Opportunity number

Research opportunity

Hover animation

Purple glow

Future improvements

Criticality

Impact score

Novelty score

Suggested experiments

---

# Report Tab

Current implementation

Displays markdown inside a formatted container.

Current issue

Raw markdown feels less professional.

Planned redesign

Render each report section individually.

Executive Summary

↓

Objective

↓

Literature Landscape

↓

Evidence Matrix

↓

Consensus

↓

Research Gaps

↓

Future Work

↓

Advisor Recommendations

Expected improvement

One of the largest visual improvements remaining.

---

# Notebook Viewer

Purpose

Allow previous investigations to be reopened.

Current workflow

Sidebar

↓

Notebook Entry

↓

Load from backend

↓

Display identical tabs

Notebook investigations remain read-only.

This prevents accidental modification of previous work.

Future improvements

Search

Rename

Delete

Tags

Folders

Similarity search

---

# Research Gap Extraction

Current implementation

The frontend parses the report.

Searches for

## Identified Research Gaps

Extracts bullet items.

Displays cards.

Reason

Allows AI-generated gaps to appear without changing backend schema.

Fallback

If section missing

↓

Uses backend research_gaps field.

---

# Current UX Flow

Landing Page

↓

Enter Question

↓

Press Start Investigation

↓

Timeline Animates

↓

Backend Completes

↓

Timeline Finishes

↓

Results Tabs Appear

↓

Investigation Saved

↓

Notebook Updated

---

# Design Language

Dark

Purple

Scientific

Minimal

No bright enterprise colors.

Visual inspiration

Scientific visualization

Astronomy

Laboratories

Research environments

Not corporate dashboards.

---

# Current Frontend Components

Hero

Sidebar

SearchPanel

InvestigationTimeline

ResultsTabs

UniverseVisual

ResearchGapsPanel

NotebookViewer (integrated into page.tsx)

Future components

EvidenceMatrix

ConsensusCard

AdvisorCard

PeerReviewCard

ConfidenceGauge

AgentConversation

CitationViewer

PDFExportButton

---

# Frontend / Backend Communication

Current communication

REST

POST

/research

↓

Returns

Director

Plan

Papers

Analyses

Review

Research Gaps

Report

GET

/notebook

↓

Returns notebook history

GET

/notebook/{id}

↓

Returns complete saved investigation

All communication uses JSON.

No frontend component performs research reasoning.

Reasoning remains entirely inside backend services.

# 25. AI Agent System

## Philosophy

ResearchOS is intentionally designed as a **multi-agent research system** rather than a single LLM application.

The long-term vision is that every investigation should resemble a team of researchers collaborating under the supervision of a principal investigator.

Instead of one model answering everything, ResearchOS decomposes the research process into specialized responsibilities.

The user should feel as though they are directing an autonomous research laboratory.

---

# Agent Architecture

Every investigation follows the same high-level structure.

```

User

↓

Research Director

↓

Planner

↓

Evidence Collection

↓

Evidence Analysis

↓

Literature Review

↓

Research Gap Detection

↓

Report Writer

↓

Notebook Memory

```

Each stage is represented by a specialist AI agent.

Some agents are already implemented.

Others are planned for future releases.

---

# Design Principles

Every agent follows the same rules.

## Single Responsibility

Each agent should perform one task only.

Examples

Planner

↓

Creates plans.

NOT reports.

Report Writer

↓

Writes reports.

NOT retrieve evidence.

Gap Detector

↓

Discovers research opportunities.

NOT summarize literature.

This keeps prompts simple and makes each component independently replaceable.

---

## Structured Communication

Agents communicate using structured Pydantic models.

Agents never exchange raw markdown unless explicitly required.

Example

Planner

↓

ResearchPlan

↓

Evidence Service

↓

Paper[]

↓

Summarizer

↓

PaperAnalysis[]

↓

Literature Review

↓

LiteratureReview

↓

Report Writer

---

## Evidence Grounding

Agents are prohibited from inventing evidence.

Every conclusion must originate from:

retrieved papers

↓

paper analyses

↓

cross-paper synthesis

No agent should fabricate:

citations

benchmark results

paper titles

statistics

---

## Fireworks First

Whenever reasoning is required:

Fireworks performs reasoning.

Python performs orchestration.

Every AI agent must include a deterministic fallback.

---

# Current Agents

---

# Research Director

Status

Implemented

Purpose

Acts as the principal investigator.

The Director is responsible for deciding how an investigation should begin.

Responsibilities

Inspect question.

Estimate complexity.

Search notebook.

Select specialist agents.

Generate director notes.

Determine AI/fallback status.

Inputs

Research question.

Notebook history.

Outputs

ResearchResponse

Current implementation

Fireworks-powered.

Fallback

Rule-based agent selection.

Example responsibilities

Question

```

Research gaps in AMD transformer inference

```

Director decides

Planner

Evidence Synthesizer

Benchmark Analyst

Gap Detector

Writer

Future improvements

Budget estimation.

Reasoning depth estimation.

Dynamic agent creation.

Agent dependency graphs.

---

# Research Planner

Status

Implemented

Purpose

Convert an ambiguous question into a structured investigation.

Outputs

Objective.

Subquestions.

Search queries.

Example

Question

↓

Investigate AMD transformer optimization.

Planner produces

Objective

↓

Investigate transformer inference optimization.

Subquestions

↓

Which AMD GPUs?

↓

Which benchmarks?

↓

Which optimization methods?

↓

Which research gaps?

Search queries

↓

AMD GPU performance

↓

Transformer inference

↓

ROCm optimization

↓

LLM inference AMD GPU

Fireworks

Used.

Fallback

Keyword rules.

Future improvements

Recursive planning.

Hierarchical decomposition.

Automatic query refinement.

---

# Literature Specialist

Status

Implemented

Purpose

Acquire academic evidence.

Current implementation

Evidence Service.

Searches

arXiv

Semantic Scholar

Outputs

Paper objects.

Responsibilities

Retrieve papers.

Normalize metadata.

Merge duplicates.

Return standardized evidence.

Future

CrossRef.

OpenAlex.

PubMed.

IEEE.

ACM.

---

# Evidence Synthesizer

Status

Partially implemented.

Purpose

Transform individual papers into collective knowledge.

Current workflow

Paper

↓

PaperAnalysis

↓

LiteratureReview

Current outputs

Common findings.

Repeated limitations.

Emerging topics.

Research gaps.

Confidence.

Future Fireworks version

Consensus.

Contradictions.

Strong evidence.

Weak evidence.

Emerging trends.

Evidence confidence.

Reason

This becomes the knowledge foundation for every later agent.

---

# Benchmark Analyst

Status

Implemented through Director selection.

Purpose

Interpret hardware benchmarking papers.

Responsibilities

Identify benchmark methodologies.

Interpret performance claims.

Compare GPU evaluations.

Highlight benchmarking limitations.

Current implementation

Mostly represented through prompts.

Future

Dedicated Fireworks reasoning stage.

Outputs

Benchmark comparison.

Benchmark reliability.

Missing benchmarks.

Performance conclusions.

---

# Research Gap Detector

Status

Implemented.

Purpose

Identify opportunities for future research.

Current implementation

Aggregates

paper-level gaps

↓

limitations

↓

future work

Outputs

Research gaps.

Future implementation

Fireworks synthesis across all evidence.

Future outputs

Missing experiments.

Missing datasets.

Contradictions.

Unexplored topics.

Novel research opportunities.

Expected impact

One of the core innovations of ResearchOS.

---

# Report Writer

Status

Implemented.

Purpose

Generate final research report.

Inputs

ResearchPlan.

LiteratureReview.

Research gaps.

Ranked papers.

Outputs

Markdown report.

Current sections

Executive Summary.

Objective.

Current Literature.

Key Findings.

Comparative Analysis.

Research Gaps.

Future Work.

Current implementation

Fireworks.

Fallback

Template generation.

Future

Professional report rendering.

Evidence matrix.

Citation references.

---

# Notebook Memory

Status

Implemented.

Purpose

Persistent institutional memory.

Responsibilities

Store investigations.

Search previous work.

Avoid duplicate investigations.

Outputs

Notebook entries.

Future

Vector similarity.

Embeddings.

Semantic notebook search.

Automatic recommendation.

---

# Planned Agents

---

# Research Advisor

Status

Planned.

Priority

Highest.

Purpose

Recommend new research projects.

Inputs

Final report.

Research gaps.

Evidence.

Outputs

Suggested project.

Novel research question.

Experiments.

Publication venues.

Novelty estimate.

Difficulty estimate.

Example

Suggested Project

↓

Memory-Efficient FlashAttention Kernels for MI300X

Novelty

High

Experiments

3

Venue

MLSys

Reason

Transforms ResearchOS from summarizer into research collaborator.

---

# Research Critic

Status

Planned.

Purpose

Critique ResearchOS's own report.

Prompt

Act as a peer reviewer.

Identify

Weak evidence.

Unsupported claims.

Missing citations.

Missing experiments.

Outputs

Strengths.

Weaknesses.

Missing evidence.

Overall confidence.

Reason

Self-critique significantly improves trustworthiness.

---

# Evidence Confidence Agent

Status

Planned.

Purpose

Estimate confidence in conclusions.

Inputs

Evidence.

Literature review.

Outputs

Confidence percentage.

Reasoning.

Factors

Agreement.

Evidence quantity.

Publication recency.

Methodological diversity.

Contradictions.

---

# Experiment Designer

Status

Planned.

Purpose

Recommend experiments.

Outputs

Experiment title.

Methodology.

Dataset.

Metrics.

Expected outcome.

Reason

Helps researchers move directly into experimentation.

---

# Citation Manager

Status

Planned.

Purpose

Link report statements to supporting papers.

Outputs

Interactive citations.

Evidence traceability.

Reason

Increase transparency.

Reduce hallucination.

---

# Agent Communication

Agents never communicate directly.

Instead

Research Director

↓

Planner

↓

Evidence Service

↓

Summarizer

↓

Literature Review

↓

Gap Detector

↓

Report Writer

Each stage receives structured models.

Each stage produces structured models.

Advantages

Easy testing.

Easy replacement.

Low coupling.

Future distributed execution.

---

# Fireworks Integration Philosophy

Every reasoning-heavy agent should eventually use Fireworks.

Current

Director

Planner

Report Writer

Research Gaps

Partial Literature Review

Future

Evidence Synthesizer

Advisor

Critic

Experiment Designer

Confidence Engine

No AI stage should ever crash the workflow.

Every stage must provide deterministic fallback behavior.

---

# Long-Term Vision

The long-term objective is for ResearchOS to evolve into an autonomous AI research laboratory.

Future investigations should resemble conversations between specialist researchers.

Example

Research Planner

↓

"We need additional benchmark evidence."

Benchmark Analyst

↓

"Only MI300X is sufficiently represented."

Gap Detector

↓

"I've identified four unexplored optimization strategies."

Research Advisor

↓

"I recommend investigating FlashAttention kernels for ROCm."

Report Writer

↓

"Compiling final publication-ready report."

Rather than presenting a single AI response, the system should expose the reasoning process of multiple collaborating specialists.

This collaborative model is considered one of the defining architectural principles of ResearchOS.

# 26. API Architecture

## Overview

ResearchOS exposes a small REST API.

The frontend is intentionally thin and communicates only through these endpoints.

All endpoints return JSON.

Business logic never exists inside the API layer.

---

# POST /research

## Purpose

Runs a complete autonomous research investigation.

This is the primary endpoint of ResearchOS.

---

### Request

```json
{
  "question": "Identify recent research gaps in transformer inference optimization for AMD GPUs."
}
```

---

### Internal Workflow

POST /research

↓

ResearchWorkflow.run()

↓

Research Director

↓

Planner

↓

Evidence Retrieval

↓

Ranking

↓

Paper Analysis

↓

Literature Review

↓

Gap Detection

↓

Report Writer

↓

Notebook Save

↓

Response

---

### Response

The response currently contains

Director

Research Plan

Paper count

Top papers

Paper analyses

Literature review

Research gaps

Report

Example

```json
{
  "question": "...",

  "director": {
    "complexity": "medium",
    "selected_agents": [],
    "notebook_matches": [],
    "notes": [],
    "ai_used": true
  },

  "research_plan": {},

  "papers_found": 5,

  "top_papers": [],

  "paper_analyses": [],

  "literature_review": {},

  "research_gaps": [],

  "report": "# Research Report..."
}
```

---

# GET /notebook

Purpose

Return notebook history.

Used by Sidebar.

Returns

```json
{
  "entries": [
    {
      "id": "...",
      "question": "...",
      "created_at": "..."
    }
  ]
}
```

---

# GET /notebook/{id}

Purpose

Load one complete investigation.

Returns

Question

Summary

Report

Research gaps

Selected agents

Paper titles

Timestamp

Frontend displays the notebook using the exact same UI as live investigations.

---

# GET /health

Purpose

Backend health check.

Response

```json
{
  "status": "ok"
}
```

Used during development.

---

# API Philosophy

Endpoints should remain extremely small.

The workflow owns orchestration.

Services own logic.

The API only translates HTTP into workflow calls.

---

# 27. Data Models

ResearchOS uses Pydantic extensively.

Models represent communication contracts between services.

---

# ResearchPlan

Purpose

Structured investigation plan.

Fields

Objective

Subquestions

Search queries

Produced by

Planner

Consumed by

Evidence Service

Report Writer

---

# Paper

Purpose

Normalized representation of a research paper.

Fields

Title

Authors

Summary

Published date

URL

PDF URL

Source

Relevance score

Produced by

Evidence Service

Consumed by

Ranking

Summarizer

Report Writer

Frontend

---

# PaperAnalysis

Purpose

Structured analysis of one paper.

Fields

paper_title

key_findings

limitations

research_gaps

confidence

Produced by

Paper Summarizer

Consumed by

Literature Review

Gap Detector

---

# LiteratureReview

Purpose

Cross-paper reasoning.

Fields

common_findings

common_limitations

emerging_topics

possible_research_gaps

confidence

Produced by

Literature Review Service

Consumed by

Report Writer

Future

Research Advisor

Research Critic

---

# ResearchResponse

Purpose

Director output.

Contains

Complexity

Notebook matches

Selected agents

Research plan

Director notes

AI used

Produced by

Research Director

Consumed by

Workflow

Frontend

---

# NotebookEntry

Purpose

Persistent memory.

Fields

id

question

summary

research_gaps

selected_agents

paper_titles

report

created_at

Produced by

Notebook

Consumed by

Sidebar

Notebook Viewer

---

# AgentProfile

Purpose

Represents one AI specialist.

Fields

Name

Department

Role

Description

Produced by

Research Director

Consumed by

Frontend

---

# 28. Fireworks Integration

## Overview

Fireworks is the primary reasoning engine.

Python orchestrates.

Fireworks reasons.

---

Current model

DeepSeek V4 Flash

Previous models used

Llama 3.1 8B

DeepSeek V3

Reason for migration

DeepSeek V4 Flash demonstrated

better reasoning

better markdown

better reports

more reliable JSON

while remaining inexpensive.

---

# Fireworks Service

Centralized wrapper.

No service directly calls Fireworks.

Advantages

Shared timeout

Shared model

Shared retries

Shared error handling

Shared configuration

---

Configuration

.env

contains

API key

Model

Timeout

Temperature

Max tokens

Base URL

---

Current AI Services

Research Director

Planner

Report Writer

Research Gaps

Partial Literature Review

---

Planned AI Services

Evidence Synthesizer

Research Advisor

Research Critic

Confidence Engine

Experiment Designer

---

# Prompt Engineering Philosophy

Every prompt follows the same rules.

Return structured output.

Never fabricate evidence.

Use supplied context only.

No unsupported claims.

Concise.

Professional tone.

Every AI stage should produce deterministic outputs when given identical evidence.

---

# JSON Reliability

Large JSON occasionally becomes malformed.

Current mitigation

Validation

Regex cleanup

Fallback

Future

OpenAI structured outputs

Function calling

Markdown parsing

---

# Fallback Philosophy

Every Fireworks failure must return

```python
{
    "success": False,
    "message": "...",
    "response": None
}
```

The caller then falls back.

No exception should escape into the workflow.

---

# 29. Notebook Storage and API Integration

Purpose

Persistent institutional memory.

ResearchOS remembers previous investigations.

Current storage

JSON

Reason

Hackathon simplicity.

Future

SQLite

Vector database

Semantic retrieval

---

Notebook Workflow

Investigation finishes

↓

Notebook.save()

↓

Sidebar refreshes

↓

User can reopen investigation

↓

Notebook Viewer displays previous report

---

Current Stored Data

Question

Summary

Research gaps

Selected agents

Paper titles

Report

Timestamp

---

Future Notebook Features

Similarity search

Automatic recommendations

Folders

Tags

Delete

Rename

Version history

Embedding search

---

# 30. External Integrations

Current

Fireworks

arXiv

Semantic Scholar

---

Future

OpenAlex

CrossRef

PubMed

IEEE Xplore

ACM Digital Library

GitHub Papers

Google Scholar (if legally permissible)

---

# AMD-Specific Integration

ResearchOS is designed to support any domain.

However,

the original hackathon centered on AMD.

Current AMD-aware behavior

Planner expands AMD queries.

Benchmark Analyst recognizes

AMD

ROCm

MI300

Inference

GPU

Report Writer understands AMD context.

Gap Detector highlights AMD-specific research opportunities.

Future

ROCm documentation

AMD benchmark datasets

AMD optimization guides

Hardware comparison dashboards


# 31. Development History

This section documents the evolution of ResearchOS in chronological order.

Understanding *why* decisions were made is just as important as understanding the code itself.

---

## Phase 1 — Initial Concept

ResearchOS began as an AMD Developer Hackathon project.

The original objective was to build an AI-powered research assistant capable of helping researchers identify research gaps.

Very early in development it became clear that another chatbot would not stand out in a hackathon.

The decision was therefore made to build an **Autonomous AI Research Laboratory** rather than a conversational assistant.

This architectural decision influenced every later component.

---

## Phase 2 — Multi-Agent Architecture

Several possible architectures were discussed.

Options included:

- Single LLM pipeline
- LangGraph
- CrewAI
- Fully autonomous evolving agents
- Deterministic orchestration

The final decision was:

- deterministic Python workflow
- specialist AI agents
- Fireworks performs reasoning
- Python performs orchestration

Reasons

- Easier debugging
- More reliable
- Better hackathon stability
- Easier to demonstrate
- Easier to extend

---

## Phase 3 — Research Workflow

The first complete workflow became

Question

↓

Planner

↓

Evidence

↓

Summaries

↓

Research Gaps

↓

Report

This proved functional but felt too linear.

The Research Director was then introduced.

The Director became responsible for

- notebook lookup
- complexity estimation
- agent selection
- investigation planning

This transformed ResearchOS into a multi-agent system.

---

## Phase 4 — Notebook Memory

Originally every investigation was independent.

This felt unrealistic.

Notebook memory was added.

Every completed investigation is now stored.

Every future investigation first searches previous work.

Reason

Researchers build upon previous investigations.

ResearchOS should behave the same way.

---

## Phase 5 — Frontend Evolution

The original frontend was a simple form and response.

It evolved into a research dashboard.

Major additions

Sidebar

Notebook History

Results Tabs

Investigation Timeline

Universe Visual

Research Gap Cards

Notebook Viewer

This dramatically improved the perceived intelligence of the system.

---

## Phase 6 — Fireworks Integration Analysis

Initially every service used deterministic Python.

Fireworks was introduced incrementally.

Order

Research Director

↓

Planner

↓

Report Writer

↓

Research Gap Synthesis

↓

Partial Literature Review

The philosophy became

Python orchestrates

↓

Fireworks reasons

↓

Python validates

↓

Fallback if necessary

---

## Phase 7 — AI Research Gaps

Originally the frontend displayed simple extracted gaps.

This looked weak.

The report already contained significantly better AI-generated gaps.

A frontend parser was created.

The UI now extracts

## Identified Research Gaps

from the report.

The cards therefore display the AI synthesis instead of the fallback list whenever possible.

This became one of the largest improvements to perceived quality.

---

## Phase 8 — Current Direction

The project is now shifting from

"research summarization"

towards

"research collaboration."

Future agents will recommend research rather than merely summarize it.

---

# 32. Current Implementation Status

## Fully Implemented

Research Director

Planner

Evidence Retrieval

Paper Ranking

Paper Summarization

Notebook Memory

Report Writer

Research Gap Extraction

Sidebar

Notebook Viewer

Timeline

Results Tabs

Universe Visual

Fireworks Integration

---

## Mostly Complete

Literature Review

Current implementation

Deterministic aggregation.

Partial Fireworks integration.

Known issue

Large JSON occasionally becomes malformed.

Current decision

Keep deterministic fallback.

Future direction

Markdown synthesis instead of JSON.

---

## Partially Implemented

Benchmark Analyst

Exists primarily as an agent selection and prompt concept.

Future

Dedicated reasoning stage.

---

Research Gap Detector

Current

Aggregates paper-level gaps.

Future

Cross-paper AI reasoning.

---

Fireworks

Integrated successfully.

Current production model

DeepSeek V4 Flash.

Reason

Excellent quality.

Low cost.

Reliable responses.

---

# 33. Known Bugs

## Literature Review JSON

Occasionally Fireworks returns malformed JSON.

Current workaround

Validation

↓

Fallback

Planned solution

Generate structured markdown rather than JSON.

---

## Raw Markdown Report

Current report is displayed inside

<pre>

This works but does not look publication quality.

Planned

Professional report renderer.

---

## Large Reports

Very long reports can exceed comfortable reading length.

Future

Collapsible sections.

---

## Notebook

Currently JSON.

Will eventually become SQLite.

---

# 34. Major Design Decisions

## Dynamic Agent Selection

Chosen instead of static pipelines.

Reason

Different investigations require different expertise.

---

## Deterministic Fallbacks

Every AI stage has deterministic fallback.

Reason

Reliability.

Hackathon robustness.

---

## Fireworks Instead of Multiple APIs

One centralized reasoning engine.

Simplifies prompts.

Simplifies configuration.

---

## Notebook Before Retrieval

Research should begin with existing knowledge.

Avoid duplicate work.

---

## Backend Owns Reasoning

Frontend never performs research logic.

Reason

Maintainability.

---

## AI Reports are Evidence Grounded

Reports are generated only after evidence retrieval.

No fabricated citations.

---

# 35. Current TODO List

Highest priority

□ Professional report renderer

□ AI Research Advisor

□ AI Research Critic

□ AI Evidence Synthesizer

Medium priority

□ Confidence Engine

□ Evidence Matrix

□ Interactive citations

□ PDF export

□ Experiment Designer

Lower priority

□ SQLite notebook

□ Semantic notebook search

□ Streaming investigation updates

□ Agent conversations

□ OpenAlex integration

---

# 36. Immediate Next Steps

Development should continue in the following order.

---

## 1. AI Evidence Synthesizer

Purpose

Compare papers.

Find consensus.

Find contradictions.

Identify strongest evidence.

Detect weak evidence.

Current status

Partially implemented.

Needs redesign to favor Markdown synthesis over large JSON.

---

## 2. Beautiful Report Renderer

Current report is raw markdown.

Replace with

Executive Summary card

↓

Objective card

↓

Literature Landscape

↓

Evidence Matrix

↓

Consensus

↓

Research Gaps

↓

Future Directions

↓

Advisor

Expected impact

Largest UI improvement remaining.

---

## 3. Research Advisor

New Fireworks agent.

Input

Final report.

Output

Suggested research project.

Novel research question.

Experiments.

Publication venues.

Novelty.

Difficulty.

This transforms ResearchOS into a research collaborator.

---

## 4. Research Critic

New Fireworks agent.

Acts as peer reviewer.

Outputs

Strengths

Weaknesses

Missing evidence

Missing citations

Future work

---

## 5. Confidence Engine

Produces

Research Confidence

based on

paper count

agreement

recency

contradictions

evidence quality

---

# 37. Long-Term Vision

ResearchOS should ultimately become an autonomous AI research operating system.

The desired workflow is

Question

↓

Research Director

↓

Planner

↓

Evidence Specialists

↓

Benchmark Analyst

↓

Literature Synthesizer

↓

Gap Detector

↓

Research Advisor

↓

Research Critic

↓

Publication-Ready Report

↓

Notebook Memory

↓

Future Investigations

The user should feel like they are supervising an entire AI research laboratory rather than interacting with a single chatbot.

---

# 38. Architectural Principles (Canonical)

These principles should guide all future development.

1. Evidence before generation.

2. Python orchestrates; AI reasons.

3. Every AI stage has a deterministic fallback.

4. Notebook memory comes before retrieval.

5. Every agent has one responsibility.

6. Reports must be evidence-grounded.

7. Never fabricate citations.

8. Every stage should be independently testable.

9. Prefer structured models over free-form text.

10. Optimize for researcher productivity rather than chatbot conversation.

---

# 39. Current Working State (End of This Conversation)

At the conclusion of this development session, ResearchOS includes:

- Multi-agent orchestration led by an AI Research Director.
- Fireworks-powered Research Director, Planner, Report Writer, and Research Gap synthesis.
- Dynamic agent selection with deterministic fallback.
- Evidence retrieval from arXiv and Semantic Scholar.
- Paper ranking and structured paper analysis.
- Literature review with deterministic aggregation and experimental Fireworks integration.
- AI-generated research reports with evidence-grounded content.
- Frontend extraction and display of AI-generated research gaps.
- Persistent notebook memory with investigation history and report replay.
- Live investigation timeline and modern, research-focused UI.

The immediate next engineering milestone is to evolve ResearchOS from an AI-powered summarizer into an AI research collaborator by implementing the Evidence Synthesizer, Research Advisor, Research Critic, and a publication-quality report renderer.

---

# End of PROJECT_CONTEXT.md

This document is intended to be the authoritative engineering reference for ResearchOS. Future development should preserve the architectural principles documented above while extending the agent ecosystem and maintaining evidence-grounded reasoning.

# Appendix A — Complete Repository Reference

This appendix documents every important file in the repository.

For each file we describe

- Purpose
- Responsibilities
- Dependencies
- Used By
- Important Notes
- Future Improvements

This section should always be updated whenever new files are added.

---

# Repository Overview

```
researchos/

apps/

    backend/

        app/

            agents/

            api/

            core/

            knowledge/

            models/

            services/

            workflows/

        tests/

    frontend/

        app/

        components/

        public/
```

---

# Backend Files

---

## app/main.py

Purpose

Application entry point.

Responsibilities

- Create FastAPI application.
- Register routes.
- Configure middleware.
- Start backend.

Dependencies

FastAPI

api/routes.py

Used By

Entire backend.

Future

Authentication middleware.

Rate limiting.

---

## app/api/routes.py

Purpose

Expose REST API.

Current Endpoints

GET /health

POST /research

GET /notebook

GET /notebook/{id}

Responsibilities

Validate requests.

Call ResearchWorkflow.

Return JSON.

Should Never

Contain business logic.

---

# app/workflows/research_graph.py

Purpose

Master orchestration engine.

Responsibilities

Coordinate every research stage.

Current workflow

Director

↓

Planner

↓

Evidence

↓

Ranking

↓

Paper Analysis

↓

Literature Review

↓

Gap Detection

↓

Report Writer

↓

Notebook

Dependencies

Every service.

Future

Streaming execution.

Parallel execution.

Agent messaging.

---

# app/agents/director.py

Purpose

Research Director.

Responsibilities

Question analysis.

Notebook lookup.

Complexity estimation.

Agent selection.

Director notes.

AI orchestration.

Dependencies

Planner

Notebook

Fireworks

Outputs

ResearchResponse.

Future

Dynamic agents.

Budget estimation.

Recursive planning.

---

# app/services/planner.py

Purpose

Planner agent.

Responsibilities

Generate

Objective

Subquestions

Search queries

Dependencies

Fireworks

ResearchPlan

Future

Recursive planning.

Automatic refinement.

---

# app/services/evidence.py

Purpose

Evidence retrieval coordinator.

Responsibilities

Query literature sources.

Merge papers.

Remove duplicates.

Dependencies

arxiv.py

semantic_scholar.py

Outputs

Paper[]

Future

PubMed

OpenAlex

CrossRef

---

# app/services/arxiv.py

Purpose

Retrieve papers from arXiv.

Responsibilities

Search API.

Normalize metadata.

Create Paper model.

Future

PDF download.

Citation extraction.

---

# app/services/semantic_scholar.py

Purpose

Retrieve Semantic Scholar papers.

Responsibilities

API search.

Metadata normalization.

Paper conversion.

Future

Citation counts.

Influential paper detection.

---

# app/services/ranking.py

Purpose

Rank retrieved papers.

Responsibilities

Keyword similarity.

Relevance scoring.

Ordering.

Future

Embeddings.

Fireworks semantic ranking.

---

# app/services/summarizer.py

Purpose

Analyze one paper.

Output

PaperAnalysis.

Current

Rule-based.

Future

Fireworks reasoning.

Extract

Datasets

Metrics

Methods

Results

---

# app/services/literature_review.py

Purpose

Cross-paper reasoning.

Current

Deterministic.

Experimental Fireworks integration.

Responsibilities

Consensus.

Limitations.

Emerging topics.

Research gaps.

Future

Markdown synthesis.

Evidence matrix.

---

# app/services/gap_detector.py

Purpose

Aggregate research opportunities.

Current

Paper-level aggregation.

Future

Cross-paper reasoning.

Novel opportunity discovery.

---

# app/services/report_writer.py

Purpose

Generate final report.

Inputs

ResearchPlan

LiteratureReview

Research gaps

Ranked papers

Outputs

Markdown report.

Future

Publication-quality reports.

Advisor integration.

Interactive citations.

---

# app/services/fireworks.py

Purpose

Central Fireworks wrapper.

Responsibilities

Authentication.

Retries.

Timeouts.

Shared model.

Shared configuration.

Error handling.

Should Never

Contain application logic.

---

# app/core/settings.py

Purpose

Central configuration.

Contains

API keys.

Fireworks model.

Timeout.

Temperature.

Base URL.

Environment variables.

Dependencies

.env

---

# app/knowledge/notebook.py

Purpose

Persistent notebook.

Responsibilities

Save investigations.

Load history.

Load entry.

Search notebook.

Current storage

JSON.

Future

SQLite.

Vector search.

---

# Frontend Files

---

## app/page.tsx

Purpose

Main frontend controller.

Responsibilities

Manage state.

Call backend.

Display components.

Coordinate notebook.

Coordinate timeline.

Important

Contains almost all frontend orchestration.

Should avoid business logic.

---

## components/Hero.tsx

Purpose

Landing section.

Displays

ResearchOS branding.

---

## components/SearchPanel.tsx

Purpose

Accept user question.

Trigger investigation.

Display loading state.

---

## components/Sidebar.tsx

Purpose

Navigation.

Notebook history.

System status.

Loads

/notebook.

---

## components/InvestigationTimeline.tsx

Purpose

Visualize investigation progress.

Stages

Director

Planner

Evidence

Literature

Report

Completion

Future

Streaming updates.

Agent messages.

---

## components/ResultsTabs.tsx

Purpose

Switch between

Overview

Agents

Evidence

Research Gaps

Report

Future

Advisor

Critic

Evidence Matrix

---

## UniverseVisual

(Currently defined inside page.tsx)

Purpose

Decorative scientific visualization.

Future

Move into dedicated component.

---

## ResearchGapsPanel

(Currently defined inside page.tsx)

Purpose

Display AI-generated research gaps.

Logic

Extract

## Identified Research Gaps

from report.

Fallback

Backend research_gaps.

Future

Impact score.

Novelty score.

Suggested experiments.

---

# Models

---

## models/research.py

Contains

ResearchPlan

ResearchResponse

ResearchRequest

Primary workflow models.

---

## models/analysis.py

Contains

PaperAnalysis.

Produced by

Summarizer.

Consumed by

Literature Review.

---

## models/review.py

Contains

LiteratureReview.

Produced by

Literature Review.

Consumed by

Report Writer.

---

## models/paper.py

Contains

Paper.

Standard paper representation.

---

# Environment Files

---

## .env

Contains

Fireworks API key.

Fireworks model.

Timeout.

Temperature.

Never commit.

---

## pyproject.toml

Defines

Dependencies.

Project metadata.

Python version.

---

# Important Dependency Graph

```
page.tsx

↓

POST /research

↓

ResearchWorkflow

↓

Director

↓

Planner

↓

Evidence

↓

Ranking

↓

Summarizer

↓

Literature Review

↓

Gap Detector

↓

Report Writer

↓

Notebook

↓

Response

↓

Frontend Tabs
```

---

# Future Files Planned

advisor.py

Research Advisor.

critic.py

Peer Review Agent.

confidence.py

Confidence Engine.

experiment_designer.py

Experiment Generator.

citations.py

Evidence tracing.

report_renderer.py

Professional report formatting.

pdf_export.py

PDF generation.

openalex.py

OpenAlex integration.

pubmed.py

PubMed integration.

crossref.py

CrossRef integration.

---

# Repository Maintenance Rules

When adding a new feature

1.

Create one service.

2.

Create one model if needed.

3.

Update workflow.

4.

Update PROJECT_CONTEXT.md.

5.

Update this appendix.

Never bypass the workflow.

Never duplicate service responsibilities.

Keep every component modular.


# Appendix B — Engineering Playbook

This appendix documents the engineering philosophy used throughout ResearchOS.

It should be treated as the implementation guide for all future development.

Whenever new functionality is added, developers should follow these guidelines to preserve consistency across the project.

---

# Engineering Principles

## 1. Python orchestrates. AI reasons.

The backend should coordinate the workflow.

LLMs should perform reasoning.

Never move orchestration logic into prompts.

Instead

Python

↓

collects evidence

↓

builds context

↓

calls Fireworks

↓

validates output

↓

continues workflow.

---

## 2. Every AI component must have a fallback.

ResearchOS should never become unusable because an external model fails.

Every AI service must return

success

or

fallback.

Example

Director

↓

Fireworks unavailable

↓

Rule-based Director

Planner

↓

Fireworks unavailable

↓

Keyword Planner

Report Writer

↓

Fireworks unavailable

↓

Template Report

The system should degrade gracefully.

---

## 3. Every stage owns one responsibility.

Bad

Planner retrieves papers.

Good

Planner

↓

creates plan

Evidence

↓

retrieves papers

Summarizer

↓

analyzes papers

Report Writer

↓

writes report

---

## 4. Services communicate using models.

Avoid passing dictionaries whenever possible.

Preferred

ResearchPlan

Paper

PaperAnalysis

LiteratureReview

ResearchResponse

This makes the pipeline self-documenting.

---

## 5. Every service should be independently testable.

Every major service should have a standalone test.

Example

test_fireworks.py

test_director.py

test_planner.py

test_literature_review.py

test_report_writer.py

This greatly simplifies debugging.

---

## 6. Never duplicate prompts.

Every AI prompt should exist in exactly one location.

Avoid copying prompts between services.

If multiple services require similar prompts,

create helper utilities.

---

## 7. Reports should always be evidence grounded.

Never generate conclusions before evidence retrieval.

Correct order

Evidence

↓

Analysis

↓

Literature Review

↓

Report

Never

Question

↓

Report

---

# Prompt Engineering Guidelines

Every Fireworks prompt should contain

Role

↓

Objective

↓

Available evidence

↓

Required output format

↓

Restrictions

↓

Return format

Avoid vague prompts.

Always constrain the model.

Example

"You are a senior literature reviewer..."

instead of

"Summarize this."

---

# JSON Guidelines

When requesting JSON

Always provide

Exact schema

Allowed values

No markdown

No explanations

Return JSON only

Current limitation

Large JSON responses occasionally become malformed.

Future

Function calling

Structured outputs

---

# Markdown Guidelines

Reports should use

# Title

## Executive Summary

## Objective

## Literature Landscape

## Evidence Matrix

## Consensus

## Research Gaps

## Future Work

## References

Maintain consistent headings.

---

# Fireworks Usage Guidelines

Preferred temperature

0.1–0.2

Reason

Research should be deterministic.

High creativity is undesirable.

Preferred max_tokens

Depends on task

Director

400–600

Planner

600

Literature Review

1200

Report Writer

2000+

Advisor

1200

Critic

1000

---

# Backend Conventions

Service names

XService

Examples

PlannerService

EvidenceService

GapDetectorService

Workflow names

ResearchWorkflow

Models

Singular

Paper

ResearchPlan

NotebookEntry

Avoid abbreviations.

---

# Frontend Conventions

Every visual section should become a reusable component.

Avoid placing large UI blocks inside page.tsx.

Current exceptions

UniverseVisual

ResearchGapsPanel

These should eventually become separate files.

---

# Styling Conventions

Theme

Dark

Purple

Scientific

Rounded cards

Soft glows

Minimal animations

Avoid

Corporate dashboard styling.

Bright colors.

Heavy gradients.

---

# Performance Guidelines

Retrieve papers asynchronously.

Avoid repeated searches.

Cache notebook lookups.

Limit Fireworks context size.

Reuse analyses whenever possible.

---

# Error Handling

Every external API call should

Retry

↓

Validate

↓

Fallback

↓

Continue workflow

Never terminate an investigation because one service failed.

---

# Security Guidelines

Never commit

.env

API keys

Secrets

Notebook backups

Validate every external response before using it.

---

# Logging

Future versions should log

Director decisions

Planner output

Evidence count

Fireworks latency

Prompt token usage

Completion token usage

Notebook saves

These logs will help optimize both cost and performance.

---

# Cost Optimization

Fireworks should be used only for reasoning.

Avoid sending

Entire papers

Large PDFs

Duplicate context

Prefer

Structured summaries

↓

Cross-paper reasoning

↓

Report writing

This minimizes token usage.

---

# Code Review Checklist

Before merging any feature

□ Single responsibility maintained

□ Models updated

□ Workflow updated

□ Tests added

□ PROJECT_CONTEXT updated

□ Appendix updated

□ Fallback implemented

□ Prompt documented

---

# Definition of Done

A feature is considered complete only if

It works

↓

Has fallback

↓

Has tests

↓

Is documented

↓

Fits the architecture

↓

Does not duplicate responsibilities

---

# Final Vision

ResearchOS should eventually become

not

an AI chatbot

and not

a literature search engine.

Instead,

it should become

an autonomous AI research operating system capable of helping researchers discover, evaluate, critique, and propose novel scientific research.

Every architectural decision should move the project closer to that vision.

# Appendix C — Architecture Decision Record (ADR) Log

This appendix records the major architectural decisions made throughout the development of ResearchOS.

Each decision explains:

- What was decided
- Why it was decided
- Alternatives considered
- Long-term implications

These records should be updated whenever a significant architectural decision is made.

---

# ADR-001

## Decision

ResearchOS will be a multi-agent research platform rather than a single AI assistant.

---

### Why

Single-LLM applications are common and unlikely to stand out in research or hackathon settings.

A multi-agent architecture better reflects how real research teams operate, with specialists contributing different expertise.

It also allows the system to evolve incrementally by adding new agents without redesigning the entire application.

---

### Alternatives Considered

Single prompt pipeline

CrewAI

LangGraph

Fully autonomous evolving agents

---

### Outcome

Python orchestrates multiple specialist agents.

---

# ADR-002

## Decision

Python orchestrates.

Fireworks performs reasoning.

---

### Why

Python is deterministic.

LLMs are probabilistic.

Separating orchestration from reasoning makes the system easier to debug, test, and extend.

---

### Outcome

Every service owns its workflow.

Fireworks only performs reasoning.

---

# ADR-003

## Decision

Every AI stage must have a deterministic fallback.

---

### Why

Hackathon demonstrations cannot depend entirely on an external API.

Network failures, malformed JSON, or API outages should reduce quality rather than stop the system.

---

### Outcome

Every AI service returns either

AI result

or

fallback result.

No investigation should terminate because an LLM failed.

---

# ADR-004

## Decision

Notebook memory is checked before evidence retrieval.

---

### Why

Researchers rarely begin from scratch.

Previous investigations are valuable context.

Searching notebook memory first reduces duplicate work and creates continuity between investigations.

---

### Outcome

Notebook search occurs immediately after the Research Director receives a question.

---

# ADR-005

## Decision

Evidence retrieval always precedes report generation.

---

### Why

Reports should be evidence grounded.

The report writer should never invent papers, citations, or conclusions.

---

### Outcome

Pipeline order is fixed:

Evidence

↓

Analysis

↓

Literature Review

↓

Gap Detection

↓

Report

---

# ADR-006

## Decision

Use Fireworks as the primary reasoning provider.

---

### Why

Fireworks provided excellent reasoning quality while remaining affordable.

The OpenAI-compatible API allowed integration with minimal code changes.

---

### Outcome

Current production model:

DeepSeek V4 Flash

---

# ADR-007

## Decision

Display the investigation process rather than only the final answer.

---

### Why

Users trust AI systems more when they can observe intermediate reasoning steps.

The investigation timeline creates transparency and improves perceived intelligence.

---

### Outcome

Frontend includes:

Timeline

↓

Agent selection

↓

Evidence

↓

Research gaps

↓

Final report

---

# ADR-008

## Decision

Use tabbed results rather than one long report.

---

### Why

Different users consume information differently.

Some care about papers.

Others care about gaps.

Others only need the report.

Tabs make navigation significantly easier.

---

# ADR-009

## Decision

Represent research gaps as individual opportunity cards.

---

### Why

Research gaps are the primary value proposition of ResearchOS.

Presenting them as numbered opportunities emphasizes discovery rather than summarization.

---

### Outcome

Frontend extracts AI-generated gaps from the report whenever available.

---

# ADR-010

## Decision

Target general scientific research while maintaining AMD awareness.

---

### Why

The hackathon focused on AMD.

However, building an AMD-only system would severely limit future usefulness.

The architecture therefore supports any research domain while providing AMD-specific enhancements where appropriate.

---

### Outcome

Planner and Benchmark Analyst include AMD-aware behavior.

The overall platform remains domain independent.

---

# Appendix D — Lessons Learned

Throughout development, several important lessons emerged.

---

## 1. AI is strongest at synthesis, not orchestration.

LLMs excel at comparing evidence and writing reports.

They are less reliable for controlling complex workflows.

---

## 2. Structured outputs are essential.

Free-form responses quickly become difficult to validate.

Pydantic models significantly reduced bugs.

---

## 3. Large JSON outputs are fragile.

As prompts grew larger, malformed JSON became more common.

Future implementations should favor structured markdown or function calling.

---

## 4. Visual design strongly affects perceived intelligence.

The investigation timeline, notebook history, and universe visual dramatically increased the perceived sophistication of the system without changing backend capabilities.

---

## 5. Research quality depends on evidence quality.

Improving retrieval and literature synthesis yields greater gains than increasing model size alone.

---

# Appendix E — Future ResearchOS Vision

The long-term vision extends beyond a hackathon project.

Future ResearchOS versions should support:

- Autonomous literature surveillance
- Continuous notebook growth
- Multi-user collaboration
- Research project management
- Citation graph exploration
- Interactive evidence maps
- Automatic experiment design
- Publication drafting
- Reviewer-style critique
- Research funding opportunity recommendations
- Dataset discovery
- Benchmark recommendation
- Live monitoring of new publications
- Domain-specialized research teams

Ultimately, ResearchOS should function as an AI-powered research operating system that assists scientists throughout the entire research lifecycle—from the first question to publication.

---

# Document Maintenance Policy

This file is a living document.

Whenever a new feature is added, developers should consider whether the following sections require updates:

- Architecture
- Workflow
- Agent System
- Data Models
- API Reference
- Roadmap
- Repository Reference
- Architecture Decision Records

Keeping this document current ensures that future developers and future ChatGPT instances can continue development without losing project context.

# End of PROJECT_CONTEXT.md

