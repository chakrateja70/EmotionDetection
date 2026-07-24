"""Unit tests for the EmotionDetector application."""

import unittest

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Tests for the emotion_detector function."""
    def test_package_imports(self) -> None:
        """Ensure the emotion_detector function is importable and callable."""
        self.assertTrue(callable(emotion_detector))

    def test_detects_joy(self) -> None:
        """Detect joy from a clearly happy sentence."""
        result = emotion_detector("I am happy and excited today")
        self.assertEqual(result["dominant_emotion"], "joy")

    def test_detects_anger(self) -> None:
        """Detect anger from a clearly angry sentence."""
        result = emotion_detector("I am angry and furious")
        self.assertEqual(result["dominant_emotion"], "anger")

    def test_detects_disgust(self) -> None:
        """Detect disgust for text expressing revulsion."""
        result = emotion_detector("I feel disgusted and revolted")
        self.assertEqual(result["dominant_emotion"], "disgust")

    def test_detects_sadness(self) -> None:
        """Detect sadness for text expressing sorrow."""
        result = emotion_detector("I am sad and depressed")
        self.assertEqual(result["dominant_emotion"], "sadness")

    def test_detects_fear(self) -> None:
        """Detect fear for text expressing anxiety."""
        result = emotion_detector("I am afraid and terrified")
        self.assertEqual(result["dominant_emotion"], "fear")

    def test_blank_input(self) -> None:
        """Return None values when the input text is blank."""
        result = emotion_detector("   ")
        self.assertIsNone(result["anger"])
        self.assertIsNone(result["dominant_emotion"])


if __name__ == "__main__":
    unittest.main()
