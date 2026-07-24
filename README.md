# Final Project: Emotion Detection

**Project Name:** Final Project - Embedded AI (oaqjp-final-project-emb-ai)

## Description

This repository contains the **Final Project** for the course, an **Emotion Detector** application built using the Watson NLP library (via the Watson Emotion Predict API). The application analyzes a given piece of text and returns the scores for five emotions — anger, disgust, fear, joy, and sadness — along with the dominant (highest-scoring) emotion.

## Project Structure

```
oaqjp-final-project-emb-ai/
├── EmotionDetection/
│   ├── __init__.py
│   └── emotion_detection.py
├── static/
├── templates/
│   └── index.html
├── server.py
├── test_emotion_detection.py
└── README.md
```

## Features

- Sends text to the Watson NLP Emotion Predict API and parses the response.
- Returns a dictionary with scores for `anger`, `disgust`, `fear`, `joy`, and `sadness`, plus the `dominant_emotion`.
- Handles blank/invalid input with a status code of 400.
- Packaged as a proper Python package (`EmotionDetection`) with unit tests.
- Deployed as a Flask web application with a `/emotionDetector` endpoint and a simple web interface.
- Includes static code analysis (pylint) to ensure code quality.

## How to Run

1. Install dependencies:
   ```
   pip install requests flask
   ```

2. Run the server:
   ```
   python3 server.py
   ```

3. Open the app in your browser at:
   ```
   http://localhost:5000
   ```

4. Enter text in the input field and submit to see the detected emotions.

## Running Tests

```
python3 -m unittest test_emotion_detection.py
```

## Running Static Code Analysis

```
pylint server.py
```

## Author

Final Project submission for the AI Application Development course — Emotion Detector application.