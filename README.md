# AI App Compiler

## Overview

AI App Compiler is a compiler-inspired application generation pipeline that converts natural language product requirements into structured, validated, execution-aware application configurations.

Instead of relying on a single prompt to generate an entire application, the system decomposes the process into multiple deterministic stages including intent extraction, architecture planning, schema generation, validation, repair, and runtime simulation.

The goal of the project is to improve:
- reliability
- structural consistency
- controllability
- execution awareness
- robustness against ambiguous or contradictory prompts

---

## Key Features

- Multi-stage AI pipeline architecture
- Structured deterministic JSON-style outputs
- Automatic schema generation
- Cross-layer validation
- Runtime execution preview
- Role-based authorization generation
- Contradiction normalization
- Ambiguity handling
- Repair-aware architecture generation
- Metrics tracking and evaluation

---

## Pipeline Architecture

```text
Natural Language Prompt
→ Intent Extraction
→ Architecture Planning
→ Database Schema Generation
→ API Schema Generation
→ UI Schema Generation
→ Validation Engine
→ Repair Layer
→ Runtime Simulation / Executable Preview
```

---

## System Components

### 1. Intent Extraction

Extracts:
- app type
- entities
- roles
- features
- assumptions

### 2. Architecture Planning

Builds:
- entities
- pages
- routes
- component structures
- business rules

### 3. Schema Generation

Generates:
- database schema
- REST API schema
- UI schema
- authorization rules

### 4. Validation Engine

Checks:
- entity consistency
- API/UI alignment
- role validity
- schema completeness
- field mappings

### 5. Repair Layer

Automatically normalizes:
- contradictory prompts
- missing requirements
- unsafe authorization logic
- incomplete structures

### 6. Runtime Simulation

Generates:
- executable preview
- runtime HTML simulation
- component visualization

---

## Example Capabilities

The system can generate application structures for:
- CRM systems
- Ecommerce platforms
- Hospital systems
- Inventory systems
- Learning platforms
- Booking systems
- Admin dashboards
- Analytics systems

---

## Reliability & Robustness

The system was evaluated on:
- normal prompts
- ambiguous prompts
- contradictory prompts
- incomplete requirements
- authorization conflicts

### Evaluation Results

- Total prompts tested: 20
- Successful generations: 20/20
- Validation failures: 0
- Average repair attempts: 0
- Low-latency generation (< 6 ms)

Detailed evaluation results are available in:

```text
evaluation_results.md
```

---

## Observed Strengths

- Stable structured output generation
- Strong schema consistency
- Reliable CRUD architecture generation
- Safe authorization defaults
- Deterministic output behavior
- Execution-aware runtime simulation
- Robust ambiguity handling

---

## Known Limitations

- Some specialized domains are generalized into reusable CRUD abstractions.
- Contradictory requirements are normalized into deployable structures instead of rejected.
- Guest-only analytics and advanced policy logic are simplified into authenticated defaults.
- Real payment gateway integrations are not implemented.

---

## Tech Stack

### Backend
- Python
- FastAPI
- Pydantic
- Uvicorn

### Frontend
- Streamlit

### Core Concepts
- Structured generation pipelines
- Validation systems
- Compiler-inspired architecture
- Runtime simulation
- Deterministic schema generation

---

## Project Structure

```text
ai_app_compiler/
│
├── app/
│   ├── main.py
│   ├── pipeline.py
│   ├── models.py
│   ├── validator.py
│
├── streamlit_app.py
├── requirements.txt
├── evaluation_results.md
├── README.md
└── screenshots/
```

---

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Backend

```bash
uvicorn app.main:app --reload
```

### 3. Start Frontend

```bash
streamlit run streamlit_app.py
```

---

## Future Improvements

- Real LLM integration
- Dynamic domain ontology mapping
- Smarter contradiction detection
- Advanced repair planning
- Multi-agent generation pipeline
- Deployment-aware infrastructure generation
- Real executable code generation

---

## Project Goal

This project focuses on demonstrating:
- system thinking
- reliable AI orchestration
- structured generation pipelines
- controllable outputs
- execution-aware architecture generation

rather than only surface-level UI generation.