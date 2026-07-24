import unittest

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    def test_package_imports(self) -> None:
        self.assertTrue(callable(emotion_detector))

    def test_detects_joy(self) -> None:
        result = emotion_detector("I am happy and excited today")
        self.assertEqual(result["dominant_emotion"], "joy")

    def test_detects_anger(self) -> None:
        result = emotion_detector("I am angry and furious")
        self.assertEqual(result["dominant_emotion"], "anger")

    def test_detects_disgust(self) -> None:
        result = emotion_detector("I feel disgusted and revolted")
        self.assertEqual(result["dominant_emotion"], "disgust")

    def test_detects_sadness(self) -> None:
        result = emotion_detector("I am sad and depressed")
        self.assertEqual(result["dominant_emotion"], "sadness")

    def test_detects_fear(self) -> None:
        result = emotion_detector("I am afraid and terrified")
        self.assertEqual(result["dominant_emotion"], "fear")

    def test_blank_input(self) -> None:
        result = emotion_detector("   ")
        self.assertIsNone(result["anger"])
        self.assertIsNone(result["dominant_emotion"])


if __name__ == "__main__":
    unittest.main()
