from tmz_content_creator.services.openai_service import OpenAIService

class ContentService:
    def __init__(self, openai_service):
        self.openai_service = openai_service

    def create_content(self, user_prompt, language='en'):
        # Define language-specific system prompts
        system_prompts = {
            'en': """You are a professional content creator. 
            Create engaging and informative content in English based on the user's prompt.
            Make sure to write in English and maintain a professional tone.""",
            
            'nl': """Je bent een professionele content creator. 
            Maak boeiende en informatieve content in het Nederlands op basis van de prompt van de gebruiker.
            Zorg ervoor dat je in het Nederlands schrijft en een professionele toon aanhoudt."""
        }

        # Get the appropriate system prompt based on language
        system_prompt = system_prompts.get(language, system_prompts['en'])

        # Add language instruction to user prompt
        if language == 'nl':
            user_prompt = f"Schrijf in het Nederlands: {user_prompt}"
        else:
            user_prompt = f"Write in English: {user_prompt}"

        # Create the content using the OpenAI service
        response = self.openai_service.create_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

        return response 