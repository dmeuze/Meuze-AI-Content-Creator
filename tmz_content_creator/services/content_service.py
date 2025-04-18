from tmz_content_creator.services.openai_service import OpenAIService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ContentService:
    def __init__(self, openai_service):
        self.openai_service = openai_service
        self.system_prompts = {
            'en': {
                'create': """You are a professional content creator. 
                Create engaging and informative content in English based on the user's prompt.
                Make sure to write in English and maintain a professional tone.""",
                
                'review': """You are an AI content reviewer. 
                Analyze the content and provide specific, actionable suggestions for improvement.
                Focus on:
                1. Clarity and readability
                2. Structure and flow
                3. Tone and style
                4. Grammar and language use
                5. Content completeness
                
                Provide clear, numbered suggestions that can be directly implemented.""",
                
                'improve': """You are a professional content editor.
                Your task is to improve the content based on the provided suggestions.
                
                Follow these steps:
                1. Carefully read the original content
                2. Review each suggestion
                3. Implement the suggestions while maintaining the original message and tone
                4. Ensure the improved version addresses all suggestions
                
                Return only the improved content, without any explanations or notes."""
            },
            
            'nl': {
                'create': """Je bent een professionele content creator. 
                Maak boeiende en informatieve content in het Nederlands op basis van de prompt van de gebruiker.
                Zorg ervoor dat je in het Nederlands schrijft en een professionele toon aanhoudt.""",
                
                'review': """Je bent een AI content reviewer.
                Analyseer de content en geef specifieke, uitvoerbare suggesties voor verbetering.
                Focus op:
                1. Duidelijkheid en leesbaarheid
                2. Structuur en flow
                3. Toon en stijl
                4. Grammatica en taalgebruik
                5. Volledigheid van de content
                
                Geef duidelijke, genummerde suggesties die direct kunnen worden geïmplementeerd.""",
                
                'improve': """Je bent een professionele content editor.
                Je taak is om de content te verbeteren op basis van de gegeven suggesties.
                
                Volg deze stappen:
                1. Lees de originele content zorgvuldig
                2. Bekijk elke suggestie
                3. Implementeer de suggesties terwijl je de originele boodschap en toon behoudt
                4. Zorg ervoor dat de verbeterde versie alle suggesties adresseert
                
                Geef alleen de verbeterde content terug, zonder uitleg of notities."""
            }
        }

    def create_content(self, user_prompt: str, language: str = "en", improve_again: bool = False, previous_content: dict = None, history: list = None) -> dict:
        """Create content based on user prompt with improvement history."""
        try:
            # Get the appropriate system prompts based on language
            system_prompt = self.system_prompts[language]["create"]
            review_prompt = self.system_prompts[language]["review"]
            improve_prompt = self.system_prompts[language]["improve"]

            # Step 1: Generate initial content
            if not improve_again:
                original_content = self.openai_service.create_completion(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt
                )

                # Step 2: Review the content
                suggestions = self.openai_service.create_completion(
                    system_prompt=review_prompt,
                    user_prompt=f"Content to review:\n\n{original_content}"
                )

                # Step 3: Improve the content
                improvement_prompt = f"""Original content:
{original_content}

Suggestions for improvement:
{suggestions}

Please improve the content based on these suggestions while maintaining the original message and tone."""
                
                improved_content = self.openai_service.create_completion(
                    system_prompt=improve_prompt,
                    user_prompt=improvement_prompt
                )

                # Create initial history
                history = [{
                    "suggestions": suggestions,
                    "improvements": improved_content,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }]

            else:
                # Use previous content and history for subsequent improvements
                original_content = previous_content["original"]
                history = history or []
                
                # Review the current content
                suggestions = self.openai_service.create_completion(
                    system_prompt=review_prompt,
                    user_prompt=f"Content to review:\n\n{user_prompt}"
                )

                # Improve the content
                improvement_prompt = f"""Original content:
{user_prompt}

Suggestions for improvement:
{suggestions}

Please improve the content based on these suggestions while maintaining the original message and tone."""
                
                improved_content = self.openai_service.create_completion(
                    system_prompt=improve_prompt,
                    user_prompt=improvement_prompt
                )

                # Add to history
                history.append({
                    "suggestions": suggestions,
                    "improvements": improved_content,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            return {
                "original": original_content,
                "improved": improved_content,
                "suggestions": suggestions,
                "history": history
            }

        except Exception as e:
            logger.error(f"Error in create_content: {str(e)}")
            raise 