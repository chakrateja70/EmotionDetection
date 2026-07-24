"""Emotion detection utilities using IBM Watson NLP with a local fallback."""
from __future__ import annotations

import re
from typing import Any, Dict

try:
    from ibm_watson import NaturalLanguageUnderstandingV1
    from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
    IBM_WATSON_AVAILABLE = True
except Exception:
    NaturalLanguageUnderstandingV1 = None  # type: ignore[assignment]
    Features = None  # type: ignore[assignment]
    EmotionOptions = None  # type: ignore[assignment]
    IBM_WATSON_AVAILABLE = False

EMOTION_KEYWORDS = {
    "joy": ["happy", "excited", "glad", "joy", "delighted", "thrilled", "cheerful"],
    "sadness": ["sad", "unhappy", "upset", "depressed", "down", "sorrow"],
    "anger": ["angry", "furious", "annoyed", "hate", "rage", "irate"],
    "fear": ["afraid", "scared", "fearful", "terrified", "nervous", "anxious"],
    "disgust": ["disgusted", "gross", "revolted", "nauseated", "repulsed"],
}


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _local_emotion_analysis(text: str) -> Dict[str, Any]:
    normalized = _normalize_text(text)
    scores = {emotion: 0.0 for emotion in EMOTION_KEYWORDS}

    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in normalized:
                scores[emotion] += 1.0

    if sum(scores.values()) == 0:
        scores = {emotion: 1.0 for emotion in scores}

    total = sum(scores.values())
    normalized_scores = {emotion: round(value / total, 2) for emotion, value in scores.items()}
    top_emotion = max(normalized_scores, key=normalized_scores.get)

    return {
        "status_code": 200,
        "emotion": top_emotion,
        "scores": normalized_scores,
        "source": "local",
    }


def emotion_detector(text: str, api_key: str = None, url: str = None) -> Dict[str, Any]:
    if not isinstance(text, str) or not text.strip():
        return {
            "status_code": 400,
            "message": "Invalid input: text cannot be blank.",
        }

    if IBM_WATSON_AVAILABLE and api_key and url:
        try:
            nlu = NaturalLanguageUnderstandingV1(
                version="2023-08-01",
                iam_apikey=api_key,
                url=url,
            )
            response = nlu.analyze(
                text=text,
                features=Features(emotion=EmotionOptions()),
            ).get_result()
            emotion_scores = response["emotion"]["document"]["emotion"]
            top_emotion = max(emotion_scores, key=emotion_scores.get)
            return {
                "status_code": 200,
                "emotion": top_emotion,
                "scores": {k: round(v, 4) for k, v in emotion_scores.items()},
                "source": "watson",
            }
        except Exception as error:
            return {
                "status_code": 400,
                "message": "Watson NLP analysis failed.",
                "details": str(error),
            }

    return _local_emotion_analysis(text)


def format_emotion_output(emotion_result: Dict[str, Any]) -> Dict[str, Any]:
    if emotion_result.get("status_code") != 200:
        return emotion_result

    return {
        "status_code": 200,
        "emotion": emotion_result["emotion"],
        "scores": emotion_result["scores"],
        "source": emotion_result.get("source", "unknown"),
    }
