# Final Project - Emotion Detector

Project Name: Final Project
Repository Name: `oaqjp-final-project-emb-ai`

A Flask-based Emotion Detector application that sends text to the Watson NLP endpoint and displays emotion scores in a browser interface.

## Files

- `EmotionDetection/emotion_detection.py` - emotion detection logic using the Watson NLP endpoint
- `EmotionDetection/__init__.py` - package entrypoint importing the application module
- `server.py` - Flask web deployment and static analysis helper
- `templates/index.html` - simple web interface for text analysis
- `test_emotion_detection.py` - unittest tests for emotion detection
- `requirements.txt` - development dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Run unit tests

```bash
python test_emotion_detection.py
```

## Run the web server

```bash
python server.py
```

Open http://127.0.0.1:5000/ in your browser and submit text to analyze.

## Run static analysis

```bash
python server.py --lint
```

## Important

To match the course requirement, this code should be pushed to a repository named `oaqjp-final-project-emb-ai`.
