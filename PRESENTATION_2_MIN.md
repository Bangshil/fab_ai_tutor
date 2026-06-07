# FAB AI Tutor: 2-Minute Presentation Material

## Core Message

Our prototype applies multiple FAB course AI ideas to the problem of studying AI ideas under limited processing capacity. It represents course PDFs as searchable chunks, searches over them with a heuristic, aggregates candidate passages into an evidence board, and constrains outputs to course-grounded knowledge.

## 2-Minute Video Flow

### 0:00-0:20 — Problem

"The problem is that students are expected to deeply understand AI ideas, but they have limited information processing capacity. Reading every course PDF from beginning to end whenever we study is costly. So our goal is not to replace studying, but to help students find the most relevant course evidence faster."

### 0:20-0:45 — Course AI Ideas

"Our prototype uses several AI ideas from class. First, Representation: it converts PDFs into structured source, page, and text chunks. Second, Search: it treats a question as a goal and searches for promising passages. Third, Aggregation: it gathers competing candidate passages into one evidence board. It also uses a course boundary constraint so outputs stay grounded in the provided materials."

### 0:45-1:25 — Demo

"I upload the course PDFs and click Build Index. The system extracts text, chunks the documents, and creates a searchable representation. Now I ask a question, such as 'credit assignment intermediate feedback.' The system returns candidate passages, page numbers, and a search heuristic score. The aggregation summary shows how many passages and course files were combined into the evidence board."

### 1:25-1:50 — Study Modes

"The same evidence can be used in several study modes. Search mode finds relevant passages. Answer Draft mode creates a KRR-style evidence scaffold. Quiz mode turns passages into active recall questions for intermediate feedback. LLM Prompt mode prepares a prompt that constrains an external LLM to the retrieved course evidence."

### 1:50-2:00 — Closing

"In short, this is a working AI study system built from course ideas: representation, search, aggregation, interaction, and course-grounded constraints. It helps students economize on information processing while still studying the original course concepts deeply."

## Screen Recording Checklist

1. Open `fab_ai_tutor_web.html`.
2. Show the `Course AI Ideas Applied` section briefly.
3. Upload 2-3 representative course PDFs.
4. Click `Build Index from PDFs`.
5. Search for `credit assignment intermediate feedback`.
6. Point to `Aggregation Summary` and `Search heuristic score`.
7. Click `Answer Draft`, `Quiz`, and `LLM Prompt` briefly.
8. End by showing the evidence board with source pages.

## Terms to Use

- Limited information processing capacity
- Representation as source/page/text chunks
- Heuristic search
- Candidate passages
- Aggregation into an evidence board
- Course boundary constraint
- Active recall and intermediate feedback
- KRR-style evidence scaffold

## Terms to Avoid

- "Cosine similarity is our main AI idea"
- "This is a fully trained AI model"
- "This replaces reading the course notes"
- "This is a complete inference engine"
