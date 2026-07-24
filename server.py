from __future__ import annotations

import argparse
import subprocess
from typing import Any, Dict

from flask import Flask, jsonify, request
from EmotionDetection import emotion_detector, format_emotion_output

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home() -> Any:
    return jsonify({"message": "Emotion Detector is running."}), 200


@app.route("/predict", methods=["POST"])
def predict() -> Any:
    if request.is_json:
        payload = request.get_json(silent=True)
    else:
        payload = request.form.to_dict()

    if payload is None:
        payload = {}

    if isinstance(payload, dict):
        text = payload.get("text", "")
    else:
        text = ""

    if not isinstance(text, str) or not text.strip():
        return jsonify(
            {"status_code": 400, "message": "Text input cannot be blank."},
        ), 400

    result = emotion_detector(text)
    formatted = format_emotion_output(result)

    if formatted.get("status_code") != 200:
        return jsonify(formatted), 400
    return jsonify(formatted), 200


def run_static_analysis() -> Dict[str, Any]:
    files = [
        "server.py",
        "EmotionDetection/emotion_detection.py",
        "test_emotion_detection.py",
    ]
    try:
        completed = subprocess.run(
            ["pycodestyle", *files],
            capture_output=True,
            text=True,
            check=True,
        )
        return {
            "status_code": 0,
            "message": "Static code analysis passed with no issues.",
        }
    except FileNotFoundError:
        return {
            "status_code": 1,
            "message": "pycodestyle is not installed.",
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
