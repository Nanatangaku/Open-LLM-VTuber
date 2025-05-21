import re
import requests


from loguru import logger
from .tts_interface import TTSInterface


class openai_tts(TTSInterface):
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini-tts", 
        voice: str = "alloy",
        speed: float = 1.0,
        media_type: str = "wav",       
        instructions: str = None,        
    ):
        self.api_key = api_key
        self.model = model
        self.voice = voice
        self.speed = speed
        self.media_type = media_type
        self.instructions = instructions  
        self.api_url = "https://api.openai.com/v1/audio/speech"

    def generate_audio(self, text, file_name_no_ext=None):
        file_name = self.generate_cache_file_name(file_name_no_ext, self.media_type)
        cleaned_text = re.sub(r"\[.*?\]", "", text)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "input": cleaned_text,
            "voice": self.voice,
            "speed": self.speed,
            "response_format": self.media_type  
        }


        if self.instructions:
            data["instructions"] = self.instructions

        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=120
            )

            if response.status_code == 200:
                with open(file_name, "wb") as audio_file:
                    audio_file.write(response.content)
                return file_name
            else:
                logger.critical(f"OpenAI TTS Error: {response.status_code}, {response.text}")
                return None

        except Exception as e:
            logger.critical(f"OpenAI TTS Request Failed: {str(e)}")
            return None