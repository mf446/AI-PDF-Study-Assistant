SUMMARY_PROMPT = """
Summarize the uploaded PDF into well-organized study notes.
Use headings and bullet points.
"""

MCQ_PROMPT = """
Generate 10 multiple-choice questions based on the uploaded PDF.

Each question should have:
- A, B, C, D options
- Correct answer
- Short explanation
"""

FLASHCARD_PROMPT = """
Create study flashcards.

Format:

Front:
...

Back:
...
"""

EXAM_PROMPT = """
Create concise exam revision notes.

Highlight:
- Key definitions
- Important concepts
- Things likely to appear in exams
"""