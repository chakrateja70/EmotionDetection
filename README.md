# Emotion Detector

A small Flask-based Emotion Detector application using IBM Watson NLP when available, with a local fallback.

## Files

- `EmotionDetection/emotion_detection.py` - emotion detection logic and output formatting
- `EmotionDetection/__init__.py` - package entrypoint importing the application module
- `server.py` - Flask web deployment and static analysis helper
- `test_emotion_detection.py` - unit tests for emotion detection
- `requirements.txt` - development dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Run unit tests

```bash
pytest
```

## Run the web server

```bash
python server.py
```

## Run static analysis

```bash
python server.py --lint
```
