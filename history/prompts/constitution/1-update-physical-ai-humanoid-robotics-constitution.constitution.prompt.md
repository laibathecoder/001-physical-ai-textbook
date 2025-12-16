---
id: 1
title: Update-Physical-AI-Humanoid-Robotics-Constitution
stage: constitution
date: 2025-12-14
surface: agent
model: Claude Sonnet 4.5
feature: Physical AI & Humanoid Robotics textbook
branch: master
user: User
command: /sp.constitution
labels: [constitution, textbook, robotics, ai]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```
Project: Physical AI & Humanoid Robotics — Technical Textbook
Output Medium: Docusaurus-based book + PDF export via Spec-Kit Plus
Tools: Gemini CLI, Claude Code, Spec-Kit Plus

Core Principles

1. Source Accuracy
   - All technical definitions, scientific claims, and historical facts must be verified
     from primary or peer-reviewed sources.
   - No speculative or unverified information.

2. Clarity & Pedagogical Structure
   - Writing must be suitable for an academic audience with a computer science background.
   - Explanations must be layered: Concept → Example → Technical Detail → Citation.

3. Reproducibility
   - All processes, algorithms, architectures, and robotics mechanisms must be
     described with reproducible steps or diagrams.
   - Code snippets must be functional and tested.

4. Rigor
   - Prefer peer-reviewed articles, IEEE papers, ACM publications, reputable books,
     and official documentation.


Quality & Citation Standards

1. Citation Style: APA 7th Edition
2. Minimum Sources:
   - At least 15 **credible** sources
   - Minimum **50% peer-reviewed**
3. Plagiarism Tolerance: 0% before submission
4. Writing Quality:
   - Maintain Flesch-Kincaid Grade Level 10–12 (clear academic English)
5. Fact Verification:
   - Each factual claim must include an inline citation
   - All data must be cross-referenced before final export


Format Constraints

- Word Count: 5,000–7,000 words
- Book Structure:
  - Introduction
  - Core Chapters (3–5)
  - Technical Diagrams / Code (where relevant)
  - Summary & Future Work
  - Reference Section
- Output Formats:
  - Docusaurus website
  - PDF with embedded APA citations (Spec-Kit Plus)

Success Criteria

- All claims are fully traceable with APA citations
- Zero plagiarism on final PDF export
- Content passes scientific fact-checking
- High clarity for CS/Robotics students
- Book builds successfully in Docusaurus and deploys to GitHub Pages
- AI tools (Gemini + Claude Code) follow this constitution consistently

End of Constitution
```

## Response snapshot

The project constitution was successfully updated for the Physical AI & Humanoid Robotics textbook project. The new constitution includes 4 core principles: Source Accuracy, Clarity & Pedagogical Structure, Reproducibility, and Rigor. It also includes sections on Quality & Citation Standards, Format & Output Constraints, Success Criteria, Development Workflow, and Governance.

## Outcome

- ✅ Impact: Updated project constitution with academic-focused principles for robotics textbook
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with new constitution
- 🔁 Next prompts: Continue with textbook development following new constitution
- 🧠 Reflection: Constitution now properly reflects academic rigor requirements for technical textbook

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Begin textbook development following new constitution