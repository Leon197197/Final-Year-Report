import unittest
from mailllm import MailLLM
from mailconfig import MailConfig

class Test_MailLLM(unittest.TestCase):
    def setUp(self):
        MailConfig.read_config()
        self.mailllm = MailLLM(MailConfig.dify_url,MailConfig.analysis_api_key)

    def test_ask_analysis_llm(self):
        str="Anger, Disgust, Fear, Sadness, Surprise, Anticipation, Trust, Joy, Other"
        self.assertEqual(self.mailllm.ask_analysis_llm("I'm mad at your behavior.",str),'Anger')

    def tearDown(self):
        pass
if __name__ == '__main__':
    unittest.main()