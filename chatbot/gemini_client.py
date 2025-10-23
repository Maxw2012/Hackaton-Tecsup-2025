import os

class GeminiClient:
    """
    Cliente para interactuar con Google Gemini AI
    """
    
    def __init__(self):
        """
        Inicializa el cliente de Gemini
        """
        # Configurar la API key desde variables de entorno
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno")
            print("wawa");
        
        # Importar genai solo cuando sea necesario
        try:
            from google import genai
            from google.genai import types
            self.genai = genai
            self.types = types
            # Configurar el cliente
            self.client = genai.Client(api_key=api_key)
        except ImportError:
            raise ImportError("La librería google-genai no está instalada. Ejecuta: pip install google-genai")
    
    def generate_content(self, prompt, model="gemini-2.5-flash-lite"):
        """
        Genera contenido usando Gemini AI
        
        Args:
            prompt (str): El prompt o pregunta para el modelo
            model (str): El modelo a usar (por defecto: gemini-2.5-flash)
            
        Returns:
            str: La respuesta generada por el modelo
        """
        try:
            response = self.client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error al generar contenido: {str(e)}"
    
    def chat(self, message, model="gemini-2.5-flash-lite"):
        """
        Método simplificado para chat
        
        Args:
            message (str): El mensaje del usuario
            model (str): El modelo a usar
            
        Returns:
            str: La respuesta del chatbot
        """
        return self.generate_content(message, model)
