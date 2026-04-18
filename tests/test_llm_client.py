import os
import unittest

from aibeyin.llm_client import LLMClient


class LLMClientTests(unittest.TestCase):
    def test_openrouter_defaults(self):
        client = LLMClient({"provider": "openrouter"})
        self.assertEqual(client.provider, "openrouter")
        self.assertEqual(client.api_key_env, "OPENROUTER_API_KEY")
        self.assertEqual(client.base_url, "https://openrouter.ai/api/v1/chat/completions")

    def test_azure_root_is_normalized(self):
        client = LLMClient(
            {
                "provider": "azure_openai",
                "base_url": "https://example.openai.azure.com/openai/v1/",
            }
        )
        self.assertEqual(
            client._azure_resource_root(client.base_url),
            "https://example.openai.azure.com",
        )

    def test_env_backed_model_resolution(self):
        os.environ["AIBEYIN_TEST_DEPLOYMENT"] = "gpt-4o-mini-prod"
        client = LLMClient(
            {
                "provider": "azure_openai",
                "primary_model_env": "AIBEYIN_TEST_DEPLOYMENT",
            }
        )
        self.assertEqual(client.primary_model, "gpt-4o-mini-prod")


if __name__ == "__main__":
    unittest.main()
