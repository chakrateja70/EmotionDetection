"""Flask server for the Emotion Detector application."""
from __future__ import annotations

import argparse
import subprocess
from typing import Any, Dict

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home() -> Any:
    """Render the home page for text input."""
    return render_template("index.html", response=None)


@app.route("/emotionDetector", methods=["GET"])
def emotion_detector_route() -> Any:
    """Analyze emotion for the provided text query parameter."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    response = emotion_detector(text_to_analyze)
    formatted_text = (
        f"anger: {response['anger']} | "
        f"disgust: {response['disgust']} | "
        f"fear: {response['fear']} | "
        f"joy: {response['joy']} | "
        f"sadness: {response['sadness']} | "
        f"dominant_emotion: {response['dominant_emotion']}"
    )
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return formatted_text, 200
    return render_template("index.html", response=formatted_text)


def run_static_analysis() -> Dict[str, Any]:
    """Run pylint on project files and return the result."""
    files = [
        "server.py",
        "EmotionDetection/emotion_detection.py",
        "test_emotion_detection.py",
    ]
    try:
        completed = subprocess.run(
            ["pylint", *files],
            capture_output=True,
            text=True,
            check=True,
        )
        return {"status_code": 0, "message": completed.stdout.strip()}
    except FileNotFoundError:
        return {
            "status_code": 1,
            "message": "pylint is not installed.",
        }
    except subprocess.CalledProcessError as exc:
        output = exc.stdout.strip() or exc.stderr.strip()
        return {"status_code": exc.returncode, "message": output}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the Emotion Detector server or static analysis."
    )
    parser.add_argument(
        "--lint",
        action="store_true",
        help="Run static code analysis instead of starting the server.",
    )
    args = parser.parse_args()

    if args.lint:
        result = run_static_analysis()
        print(result["message"])
    else:
        app.run(host="0.0.0.0", port=5000, debug=True)
