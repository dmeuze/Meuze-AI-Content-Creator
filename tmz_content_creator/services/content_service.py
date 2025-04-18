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
                6. Engagement and impact
                7. Originality and creativity
                
                Provide clear, numbered suggestions that can be directly implemented.
                Be critical and thorough in your analysis.
                Focus on making the content more concise and impactful.""",
                
                'improve': """You are a professional content editor with expertise in creating compelling content.
                Your task is to significantly improve the content based on the provided suggestions.
                
                Follow these steps:
                1. Carefully read the original content
                2. Review each suggestion thoroughly
                3. Make substantial improvements while maintaining the core message
                4. Enhance the content by:
                   - Making it more concise and focused
                   - Removing redundant information
                   - Strengthening the main points
                   - Using more precise language
                   - Improving the logical flow
                   - Adding relevant examples or analogies
                5. Ensure the improved version is noticeably better than the original
                
                Return only the improved content, without any explanations or notes.
                Make sure the improvements are significant and meaningful.
                Focus on quality over quantity."""
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
                6. Betrokkenheid en impact
                7. Originaliteit en creativiteit
                
                Geef duidelijke, genummerde suggesties die direct kunnen worden geïmplementeerd.
                Wees kritisch en grondig in je analyse.
                Focus op het maken van de content bondiger en impactvoller.""",
                
                'improve': """Je bent een professionele content editor met expertise in het maken van boeiende content.
                Je taak is om de content significant te verbeteren op basis van de gegeven suggesties.
                
                Volg deze stappen:
                1. Lees de originele content zorgvuldig
                2. Bekijk elke suggestie grondig
                3. Maak substantiële verbeteringen terwijl je de kernboodschap behoudt
                4. Verbeter de content door:
                   - Het bondiger en gerichter te maken
                   - Overbodige informatie te verwijderen
                   - De hoofdpunten te versterken
                   - Preciezere taal te gebruiken
                   - De logische flow te verbeteren
                   - Relevante voorbeelden of analogieën toe te voegen
                5. Zorg ervoor dat de verbeterde versie merkbaar beter is dan het origineel
                
                Geef alleen de verbeterde content terug, zonder uitleg of notities.
                Zorg ervoor dat de verbeteringen significant en betekenisvol zijn.
                Focus op kwaliteit boven kwantiteit."""
            }
        }

    def create_content(self, user_prompt: str, language: str = "en", improve_again: bool = False, previous_content: dict = None, history: list = None) -> dict:
        """Create content based on user prompt with improvement history."""
        try:
            # Get the appropriate system prompts based on language
            system_prompt = self.system_prompts[language]["create"]
            review_prompt = self.system_prompts[language]["review"]
            improve_prompt = self.system_prompts[language]["improve"]

            # Step 1: Generate initial content or use existing content for improvement
            if not improve_again:
                original_content = self.openai_service.create_completion(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt
                )
            else:
                original_content = previous_content.get('original', user_prompt)

            # Step 2: Review the content
            review_prompt_text = f"""Content to review:
{original_content}

Previous improvements (if any):
{history[-1]['improvements'] if history else 'None'}

Please provide specific, actionable suggestions for improvement. Be thorough and critical in your analysis."""
            
            suggestions = self.openai_service.create_completion(
                system_prompt=review_prompt,
                user_prompt=review_prompt_text
            )

            # Step 3: Improve the content
            improvement_prompt_text = f"""Original content:
{original_content}

Suggestions for improvement:
{suggestions}

Previous improvements (if any):
{history[-1]['improvements'] if history else 'None'}

Please significantly improve the content based on these suggestions while maintaining the original message and tone.
Make sure the improvements are substantial and meaningful. Focus on:
1. Making the content more engaging and impactful
2. Improving the structure and flow
3. Adding more vivid examples or analogies
4. Strengthening the opening and closing
5. Using more compelling language
6. Ensuring clear transitions between ideas"""
            
            improved_content = self.openai_service.create_completion(
                system_prompt=improve_prompt,
                user_prompt=improvement_prompt_text
            )

            # Create or update history
            if not history:
                history = []
            
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