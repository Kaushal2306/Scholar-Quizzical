# 📚 Scholar Quizzical: Your AI-Powered Study Assistant

## About the Project

**Scholar Quizzical** is an AI-powered web application designed to help students, researchers, and lifelong learners transform dense academic content into personalized, actionable study materials. By leveraging the power of **Google's Gemini API**, this tool streamlines the process of learning by providing instant summaries, custom quizzes, and interactive flashcards.

The application's core workflow is simple and efficient: you find an academic paper on **Google Scholar**, and Scholar Quizzical takes care of the rest, turning raw text into effective study aids.

## ✨ Features

  * **Intelligent Summaries**: Quickly grasp the main concepts of any academic paper with AI-generated summaries.
  * **Custom Quizzes**: Test your knowledge with a practice quiz featuring multiple-choice questions. A "Skip" option allows you to deselect an answer if you're unsure.
  * **Interactive Flashcards**: Memorize key terms and definitions with a set of easy-to-use flashcards.
  * **Google Scholar Integration**: Search for and retrieve academic paper snippets and full-text content directly within the app using **SerpApi**.
  * **User-Friendly Interface**: A clean and intuitive UI, built with **Streamlit**, makes studying an engaging and efficient experience.

## ⚙️ How to Run Locally

### Prerequisites

  * Python 3.8+
  * A **Gemini API Key** from Google AI Studio.
  * A **SerpApi Key** from SerpApi.

### Setup Steps

1.  **Clone the Repository**:

    ```bash
    git clone <your_repository_url>
    cd <your_repository_folder>
    ```

2.  **Create a Virtual Environment** (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Required Packages**:

    ```bash
    pip install -r requirements.txt
    ```

    *Note: The `requirements.txt` file should contain all necessary libraries from your code, such as `streamlit`, `google-generativeai`, `serpapi`, `requests`, and `beautifulsoup4`.*

4.  **Configure API Keys**:
    Create a file named `.env` in the project root directory and add your API keys:

    ```
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    SERPAPI_API_KEY="YOUR_SERPAPI_API_KEY"
    ```

5.  **Run the Application**:

    ```bash
    streamlit run app.py
    ```

    The application will open in your web browser.

## 🚀 Future Enhancements

  * **Document Upload**: Allow users to upload their own lecture notes, PDFs, or other documents to generate personalized study materials.
  * **Progress Tracking**: Implement a feature to track quiz scores and study progress over time.
  * **User Accounts**: Add a login system to save user-specific data and a study history.
  * **Advanced AI Features**: Explore using LangChain for more complex RAG (Retrieval-Augmented Generation) applications to answer questions about the documents.

## 🤝 Contributing

Contributions are welcome\! If you have ideas for new features, bug fixes, or improvements, please open an issue or submit a pull request.

-----

### **License**

This project is licensed under the MIT License - see the `LICENSE` file for details.
