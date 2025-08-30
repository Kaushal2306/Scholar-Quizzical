import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from serpapi import GoogleSearch
import json
import requests
from bs4 import BeautifulSoup
import re

# Load environment variables
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

# Gemini summarizer
def summarize_long(text: str, explanation_ip: str, length_ip: str) -> str:
    if not text:
        return ""
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""Summarize the following text into {length_ip}, for {explanation_ip}.
Keep it simple and concise.

Text: {text[:8000]}
Notes:"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Error summarizing with Gemini: " + str(e)

# ----------------- NEW FEATURES -----------------

# Generate question bank and flashcards
def generate_qa_flashcards(text: str, num_questions: int):
    if not text:
        return {}, {}
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""
From the following text, create:
1. A question bank of {num_questions} short-answer questions.
2. A set of {num_questions} flashcards, each with a term on one side and its definition on the other.

Format the output as a JSON object with two keys: "questions" (an array of objects with "question" and "answer" keys) and "flashcards" (an array of objects with "term" and "definition" keys).

Text: {text[:8000]}
JSON:
"""
    try:
        response = model.generate_content(prompt)
        json_output = response.text.strip().replace('```json', '').replace('```', '')
        data = json.loads(json_output)
        return data.get("questions", []), data.get("flashcards", [])
    except Exception as e:
        st.error(f"Error generating Q&A and flashcards: {e}")
        return [], []

# Generate a practice quiz
def generate_quiz(text: str, num_questions: int):
    if not text:
        return []
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""
From the following text, create a multiple-choice practice quiz with {num_questions} questions.
Each question should have a unique question ID, the question text, 4 options (labeled A, B, C, D), and the correct answer.

Format the output as a JSON array of objects, where each object represents one question.
Example structure:
[
  {{
    "id": 1,
    "question": "What is the capital of France?",
    "options": {{ "A": "Berlin", "B": "Paris", "C": "Madrid", "D": "Rome" }},
    "answer": "B"
  }}
]

Text: {text[:8000]}
JSON:
"""
    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        json_match = re.search(r'```json\s*(.*?)\s*```', raw_text, re.DOTALL)
        if json_match:
            json_output = json_match.group(1)
        else:
            json_output = raw_text
        quiz_data = json.loads(json_output)
        return quiz_data
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON from Gemini. Please try again. Details: {e}")
        st.markdown(f"**Problematic Output:**\n```\n{raw_text}\n```")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return []

# Function to scrape a webpage for content
def scrape_webpage_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text.strip()
    except Exception as e:
        st.warning(f"Could not scrape the webpage: {e}")
        return ""

# Fetch Google Scholar papers
def fetch_papers(query):
    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": SERPAPI_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("organic_results", [])

# Streamlit UI
st.title("📘 Scholar Summarizer with Gemini")

query = st.text_input("Enter your topic (Google Scholar Search):", "Integration in Calculus")

explanation_ip = st.selectbox('Select explanation type', ('Basic Explanation', 'Detailed Explanation', 'Real-world Applications', 'Best Practices', 'Common Challenges'))
length_ip = st.selectbox('Select response length', ('Short (1-2 sentences)', 'Medium (1-2 paragraphs)', 'Long (Detailed explanation)'))
num_questions = st.number_input('Number of questions/flashcards to generate:', min_value=1, max_value=10, value=5)

if st.button("Search Papers"):
    if not SERPAPI_KEY:
        st.error("⚠️ SERPAPI_KEY not found. Please add it to .env")
    else:
        papers = fetch_papers(query)
        if not papers:
            st.warning("No papers found. Try another topic.")
        else:
            st.session_state["papers"] = papers
            st.session_state.pop("selected_paper_link", None)
            st.session_state.pop("content_to_process", None) # Clear old content

# --- NEW LOGIC STARTS HERE ---
if "papers" in st.session_state:
    papers = st.session_state["papers"]
    paper_titles = [p["title"] for p in papers]
    
    # Use a unique key for the selectbox to avoid a potential bug
    selected_title = st.selectbox("Choose a paper to work with:", paper_titles, key="paper_selector")

    if selected_title:
        paper = next(p for p in papers if p["title"] == selected_title)
        link = paper.get("link", "#")
        snippet = paper.get("snippet", "")
        st.write("🔗 [Link to Paper](" + link + ")")
        st.write("**Snippet:**", snippet)
        
        # This is where the core logic begins to differ
        if st.button("Get Content from Link"):
            with st.spinner("Retrieving full content from link..."):
                full_content = scrape_webpage_content(link)
                if full_content:
                    st.session_state["content_to_process"] = full_content
                    st.success("Content successfully retrieved!")
                else:
                    st.warning("Could not retrieve full content. Using the snippet instead.")
                    st.session_state["content_to_process"] = snippet
        
        # Only display the generation buttons if a content has been processed
        if "content_to_process" in st.session_state and st.session_state["content_to_process"]:
            st.markdown("---")
            text_to_process = st.session_state["content_to_process"]

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Generate Summary"):
                    with st.spinner("Generating summary..."):
                        summary = summarize_long(text_to_process, explanation_ip, length_ip)
                        st.session_state["summary_display"] = summary
            
            with col2:
                if st.button("Generate Q&A & Flashcards"):
                    with st.spinner("Generating Q&A and flashcards..."):
                        questions, flashcards = generate_qa_flashcards(text_to_process, num_questions)
                        st.session_state["questions_display"] = questions
                        st.session_state["flashcards_display"] = flashcards

            with col3:
                if st.button("Generate Practice Quiz"):
                    with st.spinner("Generating quiz..."):
                        quiz_data = generate_quiz(text_to_process, num_questions)
                        st.session_state["quiz_display"] = quiz_data
        
            # ... (rest of your display logic remains the same below this point)
            
            if "summary_display" in st.session_state:
                st.subheader("📑 Summarized Notes")
                st.write(st.session_state["summary_display"])
                # Note: Do not use `del` immediately after displaying. It can cause re-rendering issues.
            
            if "questions_display" in st.session_state and st.session_state["questions_display"]:
                num_q_bank = len(st.session_state["questions_display"])
                st.subheader(f"❓ Question Bank ({num_q_bank} Questions)")
                for q in st.session_state["questions_display"]:
                    with st.expander(f"Question: {q.get('question', 'N/A')}"):
                        st.write(f"**Answer:** {q.get('answer', 'N/A')}")

            if "flashcards_display" in st.session_state and st.session_state["flashcards_display"]:
                num_flashcards = len(st.session_state["flashcards_display"])
                st.subheader(f"🃏 Flashcards ({num_flashcards} Cards)")
                for card in st.session_state["flashcards_display"]:
                    with st.expander(f"Term: {card.get('term', 'N/A')}"):
                        st.write(f"**Definition:** {card.get('definition', 'N/A')}")

            if "quiz_display" in st.session_state and st.session_state["quiz_display"]:
                # ... (your existing quiz display and form logic)
                num_quiz_questions = len(st.session_state["quiz_display"])
                st.subheader(f"📝 Practice Quiz ({num_quiz_questions} Questions)")
                
                # Define a constant for the skip option
                SKIP_OPTION_VALUE = "➡️ Skip"

                with st.form("quiz_form"):
                    for i, q in enumerate(st.session_state["quiz_display"]):
                        st.markdown(f"**Q{i+1}:** {q.get('question', 'N/A')}")
                        
                        options = q.get("options", {})
                        if options:
                            skip_key = f"skip_q_{i}"
                            options[skip_key] = SKIP_OPTION_VALUE
                            
                            user_answer = st.radio(
                                "Choose an option:", 
                                options.values(), 
                                key=f"quiz_q_{i}"
                            )
                            
                            for key, value in options.items():
                                if value == user_answer:
                                    st.session_state[f"user_answer_{i}"] = key
                                    break
                        else:
                            st.warning(f"No options found for question {i+1}. Skipping.")
                    
                    submit_button = st.form_submit_button("Submit Quiz")
                
                if submit_button:
                    score = 0
                    total_attempted = 0
                    for i, q in enumerate(st.session_state["quiz_display"]):
                        if f"user_answer_{i}" in st.session_state:
                            user_answer_key = st.session_state[f"user_answer_{i}"]
                            skip_key = f"skip_q_{i}"

                            if user_answer_key == skip_key:
                                st.markdown(f"**Q{i+1}:** Skipped. ⏭️ The correct answer was **{q['answer']}**.")
                            else:
                                total_attempted += 1
                                if user_answer_key == q["answer"]:
                                    st.markdown(f"**Q{i+1}:** Correct! ✅")
                                    score += 1
                                else:
                                    st.markdown(f"**Q{i+1}:** Incorrect. ❌ The correct answer was **{q['answer']}**.")
                        else:
                            st.markdown(f"**Q{i+1}:** (No answer submitted) The correct answer was **{q['answer']}**.")
                    
                    st.success(f"You scored {score} out of {total_attempted} attempted questions.")
                    
                    # To prevent the quiz from showing again on reruns
                    del st.session_state["quiz_display"]
                    
        # This else block will only run if there are papers, but no content has been processed yet.
        else:
            st.info("Please click 'Get Content from Link' to retrieve the full text before generating study materials.")

# This final else block only runs on the very first load or if no papers were found.
else:

    st.info("Start by searching for a topic and clicking 'Search Papers'.")

    st.info("Start by searching for a topic and clicking 'Search Papers'.")

