# Data Model: Physical AI & Humanoid Robotics Textbook

## Entities Overview

Based on the feature specification, this textbook project involves content-based entities rather than traditional data models. The following entities represent the core concepts and components of the textbook.

## Entity: Textbook Content
- **Description**: The main content structure of the textbook
- **Components**:
  - Title: Physical AI & Humanoid Robotics Textbook
  - Chapters: 6 main chapters (Intro, Physical AI, ROS2, Simulation, Isaac, VLA, Capstone)
  - Sections: Modular sections within each chapter
  - Learning objectives: Specific goals for each section
  - Content type: Conceptual, technical, practical, or reference material
- **Validation rules**: Must adhere to Flesch-Kincaid Grade Level 10-12
- **Relationships**: Contains multiple Code Examples, Diagrams, and Citations

## Entity: Code Example
- **Description**: Reproducible code implementations referenced in the textbook
- **Attributes**:
  - ID: Unique identifier for the example
  - Language: Python, URDF, Launch files, etc.
  - Category: ROS2, Isaac, Simulation, etc.
  - Complexity level: Beginner, Intermediate, Advanced
  - Associated chapter: Which chapter the example belongs to
  - File path: Location in src/examples/
- **Validation rules**: Must be tested and functional in appropriate environment
- **Relationships**: Referenced by one or more Textbook Content sections

## Entity: Diagram
- **Description**: Visual elements supporting the textbook content
- **Attributes**:
  - ID: Unique identifier for the diagram
  - Type: Architecture, Flowchart, Schematic, etc.
  - Associated chapter: Which chapter the diagram belongs to
  - File path: Location in static/img/
  - Description: Alt text and explanation
- **Validation rules**: Must be clear, accurate, and pedagogically effective
- **Relationships**: Referenced by one or more Textbook Content sections

## Entity: Citation
- **Description**: Academic and reference sources used in the textbook
- **Attributes**:
  - ID: Unique identifier for the citation
  - Type: Academic paper, Technical documentation, Book, Website
  - APA format: Properly formatted citation string
  - Peer reviewed: Boolean indicating if peer-reviewed
  - URL: Link to source (if applicable)
  - Associated content: Which content sections reference this citation
- **Validation rules**: Must follow APA 7th edition format, minimum 50% must be peer-reviewed
- **Relationships**: Referenced by one or more Textbook Content sections

## Entity: Chapter
- **Description**: Major sections of the textbook
- **Attributes**:
  - Title: Chapter title
  - Number: Sequential chapter number
  - Word count: Number of words in the chapter
  - Learning objectives: Specific goals for the chapter
  - Prerequisites: What knowledge is required before reading
  - Associated concepts: Key concepts covered in the chapter
- **Validation rules**: Must support independent learning while building on previous chapters
- **Relationships**: Contains multiple Sections, Code Examples, Diagrams, and Citations

## Entity: Section
- **Description**: Subdivisions within chapters
- **Attributes**:
  - Title: Section title
  - Content type: Conceptual, technical detail, example, or summary
  - Associated chapter: Which chapter contains this section
  - Learning objectives: Specific goals for the section
  - Difficulty level: Beginner, Intermediate, Advanced
- **Validation rules**: Must follow Concept → Example → Technical Detail → Citation structure
- **Relationships**: Part of one Chapter, may reference other Sections

## Entity: Learning Objective
- **Description**: Specific goals for student learning
- **Attributes**:
  - ID: Unique identifier for the objective
  - Text: Clear statement of what the student should learn
  - Associated chapter/section: Where the objective is addressed
  - Assessment method: How the objective will be validated
  - Priority: P1 (essential), P2 (important), P3 (nice-to-have)
- **Validation rules**: Must be measurable and achievable
- **Relationships**: Connected to specific Chapter or Section entities

## State Transitions

### Content Creation Workflow
1. **Draft**: Content is initially created with placeholder information
2. **Research**: Content is enhanced with verified sources and citations
3. **Review**: Content is reviewed for technical accuracy and pedagogical effectiveness
4. **Validate**: Content is tested for readability, citation standards, and code functionality
5. **Approve**: Content is approved for inclusion in the textbook
6. **Publish**: Content is included in the final textbook output

### Validation Gates
- Each entity must pass specific validation checks before advancing to the next state
- Citations must be verified as peer-reviewed when required
- Code examples must be tested and confirmed functional
- Content must meet readability standards (Grade Level 10-12)
- All claims must have proper citations