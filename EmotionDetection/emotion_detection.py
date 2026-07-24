"""Emotion detection helper using Watson NLP endpoint and fallback logic."""
import re
from typing import Any, Dict

import requests

EMOTION_KEYWORDS = {
    "joy": [
        "happy",
        "excited",
        "glad",
        "joy",
        "delighted",
        "thrilled",
        "cheerful",
    ],
    "sadness": [
        "sad",
        "unhappy",
        "upset",
        "depressed",
        "down",
        "sorrow",
    ],
    "anger": [
        "angry",
        "furious",
        "annoyed",
        "mad",
        "hate",
        "rage",
        "irate",
    ],
    "fear": [
        "afraid",
        "scared",
        "fearful",
        "terrified",
        "nervous",
        "anxious",
    ],
    "disgust": [
        "disgusted",
        "gross",
        "revolted",
        "nauseated",
        "repulsed",
    ],
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
    normalized_scores = {
        emotion: round(value / total, 2)
        for emotion, value in scores.items()
    }
    dominant_emotion = max(normalized_scores, key=normalized_scores.get)

    return {
        "anger": normalized_scores["anger"],
        "disgust": normalized_scores["disgust"],
        "fear": normalized_scores["fear"],
        "joy": normalized_scores["joy"],
        "sadness": normalized_scores["sadness"],
        "dominant_emotion": dominant_emotion,
    }


def emotion_detector(text_to_analyse: str) -> Dict[str, Any]:
    if not isinstance(text_to_analyse, str) or not text_to_analyse.strip():
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    payload = {"raw_document": {"text": text_to_analyse}}

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        response_json = response.json()
        emotions = response_json["emotionPredictions"][0]["emotion"]
        dominant_emotion = max(emotions, key=emotions.get)
        return {
            "anger": emotions["anger"],
            "disgust": emotions["disgust"],
            "fear": emotions["fear"],
            "joy": emotions["joy"],
            "sadness": emotions["sadness"],
            "dominant_emotion": dominant_emotion,
        }
    except (requests.RequestException, ValueError, KeyError):
        return _local_emotion_analysis(text_to_analyse)


def format_emotion_output(emotion_result: Dict[str, Any]) -> Dict[str, Any]:
    return emotion_result
