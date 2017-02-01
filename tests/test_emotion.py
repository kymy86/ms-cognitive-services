"""
test run with
python -m unittest tests.test_emotion
"""
import unittest
import socket
from ms_services.emotionhttpservice import EmotionHttpService

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

class EmotionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = EmotionHttpService('<emotion-api-key>')

    def test_emotion_recognition(self):
        res = self.client.get_response('tests/test_data/face.jpg')
        self.assertEqual(res, 'neutral')

    def test_emotion_no_network(self):
        NetworkMock.disable_network()
        with self.assertRaises(RuntimeError):
            res = self.client.get_response('tests/test_data/face.jpg')
        NetworkMock.enable_network()



if __name__ == '__main__':
    unittest.main()
