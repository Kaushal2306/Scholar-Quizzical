# 📘 Scholar Summarizer with Gemini

A **Streamlit-based AI-powered tool** that helps students, researchers, and learners **summarize academic papers, generate flashcards, question banks, and practice quizzes** using **Google Gemini** and **SerpApi**.

---

## 🔹 Features

1. **Google Scholar Integration**
   - Search academic papers by topic directly within the app.
   - Fetch paper titles, snippets, and links for easy access.

2. **Content Summarization**
   - Summarizes selected paper content using **Gemini AI**.
   - Options for explanation types:  
     - Basic Explanation  
     - Detailed Explanation  
     - Real-world Applications  
     - Best Practices  
     - Common Challenges  
   - Options for response length: Short, Medium, or Long.

3. **Question Bank & Flashcards Generation**
   - Automatically generates a set of **short-answer questions** from the content.  
   - Creates **flashcards** with terms and definitions for quick revision.  

4. **Practice Quiz**
   - Generates a **multiple-choice quiz** with options and correct answers.  
   - Includes a **Skip option** for questions you want to skip.  
   - Evaluates answers and shows the score of attempted questions.

5. **Webpage Scraping**
   - Retrieve full content from paper links if available.  
   - Falls back to snippet if the full content cannot be retrieved.

---

## 🔹 Technologies Used

- **Python 3.10+**
- **Streamlit** – for the interactive web interface.
- **Google Gemini API** – for summarization, Q&A, and flashcards.
- **SerpApi** – for Google Scholar search integration.
- **BeautifulSoup & Requests** – for web scraping.
- **dotenv** – to manage API keys securely.

---

## 🔹 Setup and Run Instructions

1.Clone the repository**
git clone https://github.com/Kaushal2306/Scholar-Quizzical.git
cd Scholar-Quizzical
2.Create a virtual environment and activate it
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate

3.Install dependencies 
pip install -r requirements.txt

4.Set up environment variables
Create a .env file in the project root:
GEMINI_API_KEY=your_gemini_api_key
SERPAPI_API_KEY=your_serpapi_api_key

5.Run the app
streamlit run app.py

🔹 How to Use

Enter a topic for Google Scholar search.

Select a paper from the fetched list.

Retrieve full content from the paper link (optional).

Choose options for summarization: explanation type and length.

Generate: Summary, Question Bank & Flashcards, Practice Quiz.

Attempt the quiz and get your score for attempted questions.

🔹 Example Output

Summary: Concise notes from the paper.

Questions & Flashcards: Interactive expanders for easy revision.

Quiz: Multiple-choice questions with immediate feedback and scoring.

🔹 Future Improvements

Support for more AI models for better summarization.

Add PDF upload for offline paper summarization.

Include image-based flashcards for visual learning.

🔹 License

MIT License

🔹 Author

Kaushal Amara – B.Tech CSE (AI & ML), SRM Institute
GitHub: Kaushal2306
