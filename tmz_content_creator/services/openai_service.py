from openai import OpenAI
from tmz_content_creator.config.config import Config

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.MODEL_NAME
        self.system_prompt = Config.SYSTEM_PROMPT

    def generate_content(self, user_prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in OpenAI service: {str(e)}")
            return None 