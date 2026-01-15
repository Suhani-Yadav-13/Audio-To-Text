# Audio-to-Text Converter 

# Overview -
The Audio-to-Text Converter is a Python-based desktop application that converts spoken audio into text using AI speech recognition.
It features a Tkinter GUI, user authentication, offline audio playback, and secure integration with the OpenAI Whisper API using environment variables.
This project demonstrates secure API handling, multithreading, and desktop application development in Python.

# Features - 
* Convert audio files (.wav) to text using AI
* Desktop GUI built with Tkinter
* User login & registration (SQLite database)
* Automatic audio playback & replay
* Non-blocking UI using multithreading
* Secure API key handling (no hard-coded secrets)

# Tech Stack - 
* Python
* Tkinter (GUI)
* OpenAI Whisper API
* SQLite3
* Pygame (audio playback)
* Requests
* Pillow (PIL)

# How to Run the Project - 
1️. Clone the Repository
git clone https://github.com/Suhani-Yadav-13/Audio-To-Text.git
cd Audio-To-Text

2️. Install Dependencies
pip install -r requirements.txt

3️. Set API Key (IMPORTANT)
This project does not store API keys in code.
- Permanent (Windows)
- Search → Environment Variables
- Click Environment Variables
- Under User variables → New
- Name: OPENAI_API_KEY
- Value: your API key
- Restart terminal

4️. Run the Application
python AudioToText.py

# Security Practices Used - 
* API keys stored in environment variables
* .env and secrets ignored using .gitignore
* GitHub Push Protection compliant
* No sensitive data committed to repository

# Use Cases - 
- Voice-to-text transcription
- Lecture & meeting transcription
- Accessibility support
- AI-powered desktop apps

# Future Improvements - 
*Support for multiple languages
* Real-time microphone input
* Export text to .txt / .pdf
* Improved UI design
* Error handling & logging

# Author - 
Suhani Yadav

# License - 
This project is licensed under the MIT License.

# Notes - 
If you clone this project, remember to set your own API key before running.
