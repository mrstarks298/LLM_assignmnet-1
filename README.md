# College Chatbot Project

## Overview

This project is a **College Chatbot** that leverages **Machine Learning**, **Natural Language Processing**, and **Retrieval-Augmented Generation (RAG)** techniques to answer user queries about *Sitare University*. The chatbot integrates a **PostgreSQL** database for storing question embeddings, the **Groq API** for enhancing responses, and a **Flask** web interface for user interaction.

## Features

1. **Question Similarity Search**:
   * Embeddings generated using `SentenceTransformer`
   * Questions are matched based on cosine similarity using PostgreSQL's vector operations

2. **Enhanced Response Generation**:
   * Answers are enhanced using the **Groq API** with the `llama3-8b-8192` model for detailed responses

3. **Greeting Handling**:
   * Recognizes user greetings like "hello", "hi", etc., and provides a friendly response

4. **Web Interface**:
   * Flask-powered interface for question answering used HTML, CSS and little JS
     

5. **Error Logging**:
   * Comprehensive logging for debugging and tracking issues

6. **Issue Reporting**:
   * Users can  give  feedback with responses for continuous improvement by usning thumbs down.

## Prerequisites

* **Python 3.9+**
* PostgreSQL database
* Groq API key
* Flask
* Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/college-chatbot.git
   cd college-chatbot
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL database:
   * Crea.te a new database
   * and run the notebook mention in reposetory

5. Set up environment variables:
   * Create a `.env` file in the project root
   * Add your Groq API key:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```



## Running the Application

```bash
flask run
```

## API Endpoints

* `/ask` - Submit a question

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## Contact

Your Name - Saurabh_Agrahari (saurabhagrahariiitjee2022@gmail.com)


## Acknowledgements

* [SentenceTransformer](https://www.sbert.net/)
* [Groq API](https://console.groq.com/)
* [Flask](https://flask.palletsprojects.com/)
* [PostgreSQL](https://www.postgresql.org/)
