from flask import Flask, render_template, request, redirect, Response
from werkzeug.utils import secure_filename

from utils.pdf_reader import extract_text
from utils.ai import ask_ai
from utils.chunker import split_text
from utils.embeddings import create_embeddings, create_query_embedding
from utils.vector_db import store_chunks, search

import os
import markdown
import re


app = Flask(__name__)


# ==========================
# Configuration
# ==========================

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Make sure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================
# Global Variables
# ==========================

pdf_text = ""

pdf_chunks = []

chat_history = []


# ==========================
# Home Route
# ==========================

@app.route("/", methods=["GET", "POST"])
def home():

    global pdf_text
    global chat_history
    global pdf_chunks

    message = ""


    # ==========================================================
    # POST REQUEST
    # ==========================================================

    if request.method == "POST":


        # ======================================================
        # UPLOAD PDF
        # ======================================================

        if "pdf" in request.files:

            file = request.files["pdf"]


            if file and file.filename != "":

                filename = secure_filename(
                    file.filename
                )


                file_path = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )


                file.save(file_path)


                # ----------------------------------------------
                # Extract PDF text
                # ----------------------------------------------

                pdf_text = extract_text(
                    file_path
                )


                # ----------------------------------------------
                # Split PDF into chunks
                # ----------------------------------------------

                pdf_chunks = split_text(
                    pdf_text
                )

                print(
                    "TOTAL PDF CHUNKS:",
                    len(pdf_chunks)
                )


                # ----------------------------------------------
                # Create embeddings
                # ----------------------------------------------

                embeddings = create_embeddings(
                    pdf_chunks
                )


                # ----------------------------------------------
                # Store chunks in vector database
                # ----------------------------------------------

                store_chunks(
                    pdf_chunks,
                    embeddings
                )


                # ----------------------------------------------
                # Clear previous chat
                # ----------------------------------------------

                chat_history.clear()


                message = (
                    f"{filename} uploaded successfully!"
                )


        # ======================================================
        # STUDY TOOLS
        # ======================================================

        elif "tool" in request.form:

            if not pdf_text:

                message = (
                    "Please upload a PDF first."
                )


            else:

                tool = request.form["tool"]


                print(
                    "TOOL RECEIVED:",
                    tool
                )


                # ==================================================
                # SUMMARY
                # ==================================================

                if tool == "summary":

                    print(
                        "SUMMARY BRANCH STARTED"
                    )


                    # Store summaries from each part
                    all_summaries = []


                    # Smaller batches = lower memory usage
                    batch_size = 5


                    # ----------------------------------------------
                    # Summarize PDF in batches
                    # ----------------------------------------------

                    for start in range(
                        0,
                        len(pdf_chunks),
                        batch_size
                    ):

                        current_chunks = pdf_chunks[
                            start:start + batch_size
                        ]


                        context = "\n\n".join(
                            current_chunks
                        )


                        question = """
                        Summarize this section of the PDF.

                        Requirements:

                        - Identify the most important concepts.
                        - Explain important ideas clearly.
                        - Use headings where appropriate.
                        - Use bullet points.
                        - Include important definitions and facts.
                        - Keep the summary concise.
                        - Do not add information that is not in the PDF.
                        """


                        section_number = (
                            start // batch_size + 1
                        )


                        print(
                            f"Summarizing PDF section "
                            f"{section_number}"
                        )


                        answer = ask_ai(
                            question,
                            context
                        )


                        # ------------------------------------------
                        # Check AI response
                        # ------------------------------------------

                        if (
                            not answer
                            or answer.startswith("⚠️")
                            or answer.startswith("❌")
                            or answer.startswith("⏳")
                        ):

                            message = (
                                f"The AI could not summarize "
                                f"PDF section {section_number}."
                            )

                            break


                        # ------------------------------------------
                        # Store section summary
                        # ------------------------------------------

                        all_summaries.append(
                            answer
                        )


                    # ----------------------------------------------
                    # Create final summary
                    # ----------------------------------------------

                    if all_summaries:

                        print(
                            "CREATING FINAL SUMMARY"
                        )


                        # Combine smaller summaries
                        combined_summary = (
                            "\n\n".join(
                                all_summaries
                            )
                        )


                        final_question = """
                        Create a concise final study summary
                        using ONLY the section summaries provided.

                        Requirements:

                        - Organize information using clear headings.
                        - Use bullet points.
                        - Include important definitions.
                        - Include important facts and concepts.
                        - Remove repeated information.
                        - Keep the final summary concise.
                        - Do not add information that is not
                          contained in the section summaries.
                        """


                        final_answer = ask_ai(
                            final_question,
                            combined_summary
                        )


                        # ------------------------------------------
                        # Check final response
                        # ------------------------------------------

                        if (
                            not final_answer
                            or final_answer.startswith("⚠️")
                            or final_answer.startswith("❌")
                            or final_answer.startswith("⏳")
                        ):

                            message = (
                                "The AI could not create "
                                "the final summary."
                            )


                        else:

                            answer_html = markdown.markdown(
                                final_answer,
                                extensions=[
                                    "fenced_code",
                                    "tables"
                                ]
                            )


                            chat_history.append({
                                "question": "Full PDF Summary",
                                "answer": final_answer,
                                "answer_html": answer_html
                            })


                            print(
                                "SUMMARY COMPLETED"
                            )


                # ==================================================
                # FLASHCARDS
                # ==================================================

                elif tool == "flashcards":

                    print(
                        "FLASHCARD BRANCH STARTED"
                    )


                    question = """
                    Create 10 study flashcards from the uploaded PDF.

                    Follow this EXACT format for every flashcard:

                    FLASHCARD 1
                    FRONT: Question or term
                    BACK: Answer or explanation

                    FLASHCARD 2
                    FRONT: Question or term
                    BACK: Answer or explanation

                    Continue until you have created 10 flashcards.

                    Requirements:

                    - Base every flashcard only on the uploaded PDF.
                    - Cover different important sections.
                    - Keep the front concise.
                    - Make the back clear and educational.
                    - Do not add extra text before or after the flashcards.
                    """


                    # Retrieve chunks for flashcards
                    top_k = 5


                    query_embedding = (
                        create_query_embedding(
                            question
                        )
                    )


                    relevant_chunks = search(
                        query_embedding,
                        top_k=top_k
                    )


                    context = "\n\n".join(
                        relevant_chunks
                    )


                    answer = ask_ai(
                        question,
                        context
                    )


                    print(
                        "FLASHCARD AI RESPONSE RECEIVED"
                    )


                    # ------------------------------------------
                    # Check AI response
                    # ------------------------------------------

                    if (
                        not answer
                        or answer.startswith("⚠️")
                        or answer.startswith("❌")
                        or answer.startswith("⏳")
                    ):

                        message = (
                            "The AI could not generate "
                            "flashcards."
                        )


                    else:

                        answer_html = markdown.markdown(
                            answer,
                            extensions=[
                                "fenced_code",
                                "tables"
                            ]
                        )


                        chat_history.append({
                            "question": "10 Flashcards",
                            "answer": answer,
                            "answer_html": answer_html
                        })


                # ==================================================
                # EXPLAIN
                # ==================================================

                elif tool == "explain":

                    print(
                        "EXPLAIN BRANCH STARTED"
                    )


                    top_k = 8


                    question = """
                    Explain the main concepts from this PDF
                    in simple words.

                    Use examples where possible.

                    Requirements:

                    - Cover the important concepts.
                    - Use headings.
                    - Use bullet points where appropriate.
                    - Keep the explanation easy for students
                      to understand.
                    """


                    query_embedding = (
                        create_query_embedding(
                            question
                        )
                    )


                    relevant_chunks = search(
                        query_embedding,
                        top_k=top_k
                    )


                    context = "\n\n".join(
                        relevant_chunks
                    )


                    answer = ask_ai(
                        question,
                        context
                    )


                    print(
                        "EXPLAIN AI RESPONSE RECEIVED"
                    )


                    # ------------------------------------------
                    # Check AI response
                    # ------------------------------------------

                    if (
                        not answer
                        or answer.startswith("⚠️")
                        or answer.startswith("❌")
                        or answer.startswith("⏳")
                    ):

                        message = (
                            "The AI could not explain "
                            "the PDF."
                        )


                    else:

                        answer_html = markdown.markdown(
                            answer,
                            extensions=[
                                "fenced_code",
                                "tables"
                            ]
                        )


                        chat_history.append({
                            "question": "Explain PDF",
                            "answer": answer,
                            "answer_html": answer_html
                        })


                # ==================================================
                # EXAM NOTES
                # ==================================================

                elif tool == "exam_notes":

                    print(
                        "EXAM NOTES BRANCH STARTED"
                    )


                    top_k = 15


                    question = """
                    Create concise exam revision notes.

                    Include:

                    - Definitions
                    - Key concepts
                    - Important facts
                    - Things students should memorize

                    Use clear headings and bullet points.
                    """


                    query_embedding = (
                        create_query_embedding(
                            question
                        )
                    )


                    relevant_chunks = search(
                        query_embedding,
                        top_k=top_k
                    )


                    context = "\n\n".join(
                        relevant_chunks
                    )


                    answer = ask_ai(
                        question,
                        context
                    )


                    print(
                        "EXAM NOTES AI RESPONSE RECEIVED"
                    )


                    # ------------------------------------------
                    # Check AI response
                    # ------------------------------------------

                    if (
                        not answer
                        or answer.startswith("⚠️")
                        or answer.startswith("❌")
                        or answer.startswith("⏳")
                    ):

                        message = (
                            "The AI could not generate "
                            "exam notes."
                        )


                    else:

                        answer_html = markdown.markdown(
                            answer,
                            extensions=[
                                "fenced_code",
                                "tables"
                            ]
                        )


                        chat_history.append({
                            "question": "Exam Revision Notes",
                            "answer": answer,
                            "answer_html": answer_html
                        })


                # ==================================================
                # MCQ GENERATOR
                # ==================================================

                elif tool == "mcq":

                    print(
                        "MCQ BRANCH STARTED"
                    )


                    number = int(
                        request.form["mcq_number"]
                    )


                    level = request.form[
                        "mcq_level"
                    ]


                    # Generate MCQs in batches
                    batch_size = 10


                    all_answers = []


                    # Keep track of previous questions
                    previous_questions = []


                    # ----------------------------------------------
                    # Generate MCQs batch by batch
                    # ----------------------------------------------

                    for start in range(
                        0,
                        number,
                        batch_size
                    ):

                        current_batch = min(
                            batch_size,
                            number - start
                        )


                        previous_text = (
                            "\n".join(
                                previous_questions
                            )
                        )


                        question = f"""
                        Generate exactly {current_batch}
                        multiple-choice questions from
                        the provided PDF context.

                        Difficulty level:
                        {level}

                        This is batch
                        {start // batch_size + 1}.

                        Requirements:

                        - Generate exactly {current_batch} questions.
                        - Each question must have 4 options:
                          A)
                          B)
                          C)
                          D)
                        - Clearly show the correct answer.
                        - Give a short explanation after each answer.
                        - Cover different sections of the PDF.
                        - Avoid repeating questions.
                        - Make every question different
                          from the previous questions.

                        Previous questions already generated:

                        {previous_text}

                        Do not include questions that are
                        duplicates or very similar to the
                        previous questions.
                        """


                        # ------------------------------------------
                        # Create embedding
                        # ------------------------------------------

                        query_embedding = (
                            create_query_embedding(
                                question
                            )
                        )


                        # ------------------------------------------
                        # Retrieve PDF chunks
                        # ------------------------------------------

                        relevant_chunks = search(
                            query_embedding,
                            top_k=5
                        )


                        context = "\n\n".join(
                            relevant_chunks
                        )


                        # ------------------------------------------
                        # Ask AI
                        # ------------------------------------------

                        answer = ask_ai(
                            question,
                            context
                        )


                        print(
                            "MCQ AI RESPONSE RECEIVED"
                        )


                        print(
                            answer[:200]
                            if answer
                            else "EMPTY ANSWER"
                        )


                        # ------------------------------------------
                        # Check response
                        # ------------------------------------------

                        if (
                            not answer
                            or answer.startswith("⚠️")
                            or answer.startswith("❌")
                            or answer.startswith("⏳")
                        ):

                            message = (
                                f"The AI could not generate "
                                f"batch "
                                f"{start // batch_size + 1}. "
                                f"Please try again."
                            )


                            break


                        # ------------------------------------------
                        # Save batch
                        # ------------------------------------------

                        all_answers.append(
                            answer
                        )


                        # ------------------------------------------
                        # Save generated questions
                        # for duplicate prevention
                        # ------------------------------------------

                        previous_questions.append(
                            answer
                        )


                    # ----------------------------------------------
                    # Combine MCQ batches
                    # ----------------------------------------------

                    if all_answers:

                        combined_answer = (
                            "\n\n".join(
                                all_answers
                            )
                        )


                        answer_html = markdown.markdown(
                            combined_answer,
                            extensions=[
                                "fenced_code",
                                "tables"
                            ]
                        )


                        chat_history.append({
                            "question": (
                                f"{number} {level} MCQs"
                            ),
                            "answer": combined_answer,
                            "answer_html": answer_html
                        })


                        print(
                            "MCQ GENERATION COMPLETED"
                        )


        # ======================================================
        # MANUAL QUESTIONS
        # ======================================================

        elif "question" in request.form:

            question = request.form[
                "question"
            ].strip()


            if not pdf_text:

                message = (
                    "Please upload a PDF first."
                )


            elif question:

                query_embedding = (
                    create_query_embedding(
                        question
                    )
                )


                relevant_chunks = search(
                    query_embedding,
                    top_k=10
                )


                context = "\n\n".join(
                    relevant_chunks
                )


                answer = ask_ai(
                    question,
                    context
                )


                answer_html = markdown.markdown(
                    answer,
                    extensions=[
                        "fenced_code",
                        "tables"
                    ]
                )


                chat_history.append({
                    "question": question,
                    "answer": answer,
                    "answer_html": answer_html
                })


    # ==========================================================
    # DISPLAY PAGE
    # ==========================================================

    return render_template(
        "index.html",
        message=message,
        chat_history=chat_history
    )


# ==============================================================
# CLEAR CHAT
# ==============================================================

@app.route("/clear-chat")
def clear_chat():

    chat_history.clear()

    return redirect("/")


# ==============================================================
# DOWNLOAD ANSWER
# ==============================================================

@app.route("/download/<int:index>")
def download_answer(index):

    if (
        index < 0
        or index >= len(chat_history)
    ):

        return "Answer not found", 404


    answer = chat_history[index]["answer"]


    # Convert Markdown to HTML
    html = markdown.markdown(
        answer
    )


    # Remove HTML tags
    clean_text = re.sub(
        "<[^>]+>",
        "",
        html
    )


    return Response(
        clean_text,
        mimetype="text/plain",
        headers={
            "Content-Disposition":
                f"attachment; filename=answer_{index + 1}.txt"
        }
    )


# ==============================================================
# RUN APPLICATION
# ==============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )