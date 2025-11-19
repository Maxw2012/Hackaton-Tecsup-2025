import os
from google import genai

class GeminiClient:
    """
    Cliente ALMA IA compatible con google-genai>=1.51.0
    Usa un solo string de entrada (NO roles).
    """

    MODEL = "gemini-2.5-flash-lite"

    SYSTEM_PROMPT = """
Eres ALMA IA, un asistente académico y emocional para estudiantes universitarios.

REGLAS DE COMPORTAMIENTO:
- Responde siempre en 2 a 4 líneas máximo.
- Sé empático, cálido y directo.
- Evita tecnicismos y explicaciones largas.
- Da siempre un consejo práctico.
- Si detectas estrés, primero valida la emoción.
"""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no está configurada.")

        self.client = genai.Client(api_key=api_key)

    def chat(self, user_message: str) -> str:
        """
        Envía un mensaje al modelo usando texto plano concatenado con el prompt maestro.
        """
        try:
            full_prompt = f"{self.SYSTEM_PROMPT}\n\nUsuario: {user_message}\nALMA IA:"
            
            response = self.client.models.generate_content(
                model=self.MODEL,
                contents=full_prompt
            )

            return response.text.strip()

        except Exception as e:
            return f"Error al generar respuesta: {str(e)}"
