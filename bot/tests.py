import os
import unittest
from unittest.mock import MagicMock, patch

from handlers.downloader import Downloader, PlatformDetector


class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.downloader = Downloader()

    def test_download_invalid_platform(self):
        with self.assertRaises(ValueError):
            self.downloader.download("InvalidPlatform", "https://bbc.com/news", "testfile")


class TestPlatformDetector(unittest.TestCase):
    def setUp(self):
        self.detector = PlatformDetector()

    def test_detect_platform(self):
        self.assertEqual(self.detector.detect_platform("https://www.youtube.com/watch?v=example"), "YouTube")
        self.assertEqual(self.detector.detect_platform("https://x.com/example"), "X")
        self.assertEqual(self.detector.detect_platform("https://www.tiktok.com/@example/video/123"), "TikTok")
        self.assertEqual(self.detector.detect_platform("https://www.instagram.com/reel/example"), "Instagram")
        self.assertEqual(self.detector.detect_platform("https://www.pinterest.com/pin/example"), "Pinterest")
        self.assertEqual(self.detector.detect_platform("https://open.spotify.com/track/example"), "Spotify")
        self.assertEqual(self.detector.detect_platform("https://bbc.com/news"), "unsupported")


if __name__ == "__main__":
    unittest.main()
