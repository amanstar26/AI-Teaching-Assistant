import ollama
import re

def parse_flashcards(text):

    cards = []

    # Remove markdown stars
    text = text.replace("**", "")

    # Normalize separators
    text = text.replace("---", "\n")

    # Match Q/A pairs
    qa_matches = re.findall(
        r"Q:\s*(.*?)\s*A:\s*(.*?)(?=\n\s*Q:|$)",
        text,
        re.DOTALL | re.IGNORECASE
    )

    for q, a in qa_matches:

        cards.append({
            "question": q.strip(),
            "answer": a.strip()
        })

    return cards

def generate_answer(question, context, mode="hybrid"):

    if mode == "document":

        prompt = f"""
        Answer ONLY from the document.

        If information is not found say:

        'Not found in the uploaded document.'

        CONTEXT:
        {context}

        QUESTION:
        {question}
        """

    elif mode == "ai":

        prompt = f"""
        Answer using your own knowledge.

        QUESTION:
        {question}
        """

    else:

        prompt = f"""
        Answer using the document first.

        Then provide:

        Additional AI Explanation

        CONTEXT:
        {context}

        QUESTION:
        {question}
        """
    
    print("\nSending question to qwen...")
    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    print("Response received")
    return response["message"]["content"]

def generate_question_paper(context):

    prompt = f"""
Generate a school examination question paper.

Use ONLY the provided context.

Create:

SECTION A
10 MCQs

SECTION B
5 Short Answer Questions

SECTION C
2 Long Answer Questions

Do NOT provide answers.

CONTEXT:
{context}
"""
    print("Requesting question paper from qwen...")
    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    print("Response received")
    return response["message"]["content"]

def generate_flashcards(context):

    prompt = f"""
    Generate exactly 10 flashcards.

    VERY IMPORTANT:

    Return ONLY this format:

    Q: Question 1
    A: Answer 1

    Q: Question 2
    A: Answer 2

    Q: Question 3
    A: Answer 3

    Rules:
    - Exactly 10 flashcards
    - Every question must start with Q:
    - Every answer must start with A:
    - No numbering
    - No markdown
    - No headings
    - No explanations
    - No intro text
    - No summary

    CONTEXT:
    {context}
    """
    print("\nRequesting flashcards from qwen...")
    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    print("Response Received")

    return response["message"]["content"]

def generate_study_plan(context):

    prompt = f"""
You are an expert teacher.

Create a student-friendly study plan.

The study plan MUST contain:

# Chapter Overview
Brief summary of the chapter.

# Learning Objectives
What students should learn.

# Important Concepts
Explain the most important concepts.

# Day-wise Study Plan

For each day provide:

Topic
Key Concepts
Important Facts
Quick Notes
Practice Questions

# Revision Plan

# Exam Tips

# Most Important Questions

Use simple language suitable for school students.

CONTEXT:
{context}
"""

    print("Generating Study Plan...")

    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]

def generate_ppt_content(context):

    prompt = f"""
    Create exactly 10 PowerPoint slides.

    STRICT FORMAT:

    SLIDE 1
    TITLE: Chapter Overview

    POINTS:
    - point 1
    - point 2
    - point 3

    SLIDE 2
    TITLE: Important Concepts

    POINTS:
    - point 1
    - point 2

    Rules:
    - Exactly 10 slides
    - Maximum 5 bullet points per slide
    - Maximum 15 words per bullet
    - No markdown
    - No ###
    - No **
    - No explanations outside slides

    CONTEXT:
    {context}
    """
    print("Generating PPT Content")
    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )
    print("Got the PPT Points")
    return response["message"]["content"]