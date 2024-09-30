import unittest
from src.Functions.image_detection import check_image_presence

class TestImageDetection(unittest.TestCase):
    def test_check_image_presence(self):
        # You might need to mock the actual image detection
        # and just test the function's logic
        result = check_image_presence("path/to/test/image.png")
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
