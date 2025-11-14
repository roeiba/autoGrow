---
trigger: manual
project: AI-Optimized Project Template
version: 2.0.1
last_updated: 2025-11-11
---

# Project Guidelines for AI Agents

## Purpose

This document provides comprehensive guidelines for AI coding assistants working on this project. It defines the project structure, development workflows, quality standards, and best practices that ensure consistent, high-quality contributions.

You are in **generation mode**. Your job is to:
1. Read `PROJECT_BRIEF.md` to understand requirements
2. Generate the complete project structure
3. Create all necessary code, documentation, and configuration
4. Follow the guidelines below while generating
5. Don't generate more than what is required. 
6. Do not create empty files or folders. Create only the files and folders that are required.

## Project Structure

### Directory Overview

#### `/` - Project Root Directory
Contains all applications folder organized by platform or function:

- **Independent Apps**: `backend/`, `frontend/`, `mobile/`, `web/`, `portal/`, `marketing/`, `sales/`, `admin/`, `api-gateway/`, `creative/`
- **Shared Code**: `shared/` - Common libraries, types, and utilities

**Key Principles**:
- Each app has its own `.agents/README.md` with app-specific guidelines
- Each app is fully self-contained and has its own `tests/` directory for unit and integration tests
- Apps are independently deployable with isolated dependencies
- Technology choices can differ between apps
- CI and CD handled under .github/ folder

- **`docs/`** - Technical documentation, user guides, API specs, processes
- **`docs/knowledge_base/`** - Business context, domain knowledge, requirements, research
- **`docs/architecture/`** - System design, ADRs, diagrams, patterns, security

