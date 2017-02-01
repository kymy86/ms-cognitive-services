"""
test run with
python -m unittest tests.test_speech
"""
import unittest
import socket
from ms_services.speechttpservice import SpeechHttpService

class NetworkMock():

    @staticmethod
    def disable_network():
        def guarded(*args, **kwargs):
            raise RuntimeError('No internet connection')
        socket.socket = guarded

    @staticmethod
    def enable_network():
        def guarded(*args, **kwargs):
            return socket.SocketType(*args, **kwargs)
        socket.socket = guarded

class SpeechTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.speech_client = SpeechHttpService('<your-api-key-here>')

    def test_audio_recognition(self):
        res = self.speech_client.get_response('tests/test_data/track.wav')
        self.assertEqual(res, 'computer')

    def test_audio_with_diff_locale(self):
        self.speech_client.locale = "IT-it"
        res = self.speech_client.get_response('tests/test_data/track.wav')
        self.assertNotEqual(res, 'computer')

    def test_audio_negative_recognition(self):
        res = self.speech_client.get_response('tests/test_data/track.wav')
        self.assertNotEqual(res, 'foo')

    def test_audio_no_network(self):
        NetworkMock.disable_network()
        with self.assertRaises(RuntimeError):
            res = self.speech_client.get_response('tests/test_data/track.wav')
        NetworkMock.enable_network()


if __name__ == '__main__':
    unittest.main()
