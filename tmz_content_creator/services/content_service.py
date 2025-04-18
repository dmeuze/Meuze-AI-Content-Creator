from tmz_content_creator.services.openai_service import OpenAIService

class ContentService:
    def __init__(self):
        self.openai_service = OpenAIService()

    def create_content(self, user_prompt):
        if not user_prompt:
            return ""

        full_prompt = f"""
You are an expert content creator focused on the following topics:
1. Topic A (customizable)
2. Prompt Engineering

Generate clear, high-quality, creative content based on the following input:

{user_prompt}

Make sure your response is well structured, professional, and useful for readers.
"""
        try:
            return self.openai_service.generate_content(full_prompt)
        except Exception as e:
            return f"An error occurred: {str(e)}" 