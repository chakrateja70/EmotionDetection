from EmotionDetection import emotion_detector, format_emotion_output


def test_package_imports() -> None:
    assert callable(emotion_detector)


def test_emotion_detector_returns_valid_format() -> None:
    result = emotion_detector("I feel happy and joyful today")
    formatted = format_emotion_output(result)

    assert formatted["status_code"] == 200
    assert isinstance(formatted["emotion"], str)
    assert "scores" in formatted
    assert formatted["emotion"] in formatted["scores"]
    score_values = formatted["scores"].values()
    assert all(isinstance(value, float) for value in score_values)


def test_emotion_detector_blank_input() -> None:
    result = emotion_detector("   ")
    assert result["status_code"] == 400
    assert "Invalid input" in result["message"]


def test_format_emotion_output_returns_error_as_is() -> None:
    error = {"status_code": 400, "message": "Invalid input"}
    assert format_emotion_output(error) == error
