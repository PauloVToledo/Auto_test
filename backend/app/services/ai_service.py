import os
import google.generativeai as genai
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from dotenv import load_dotenv

# Cargamos variables (por si corres local)
load_dotenv()


def get_chat_response(user_message: str, db: Session):
    try:
        # 1. Configuración "Lazy" (Dentro de la función)
        # Esto evita que la app se rompa al iniciarse si falta la key.
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ ERROR: No se encontró GEMINI_API_KEY.")
            return "Error de configuración: Falta la API Key en el servidor."

        genai.configure(api_key=api_key)

        # 2. Obtener contexto de la Base de Datos
        # Aseguramos que solo traiga lo necesario para no gastar tokens
        vehicles = db.query(Vehicle).all()  # Traemos todos para probar

        if not vehicles:
            inventory_text = "No hay vehículos disponibles en este momento."
        else:
            inventory_text = "\n".join(
                [
                    f"- {v.brand} {v.model} ({v.year}): ${v.price:,} USD. Color {v.color}. ID: {v.id}"
                    for v in vehicles
                ]
            )

        # 3. Prompt Engineering (Técnica "Context Injection")
        # En lugar de usar system_instruction (que falla en versiones viejas),
        # lo inyectamos directamente en el mensaje. Es a prueba de balas.
        full_prompt = f"""
        Rol: Eres un vendedor experto de 'Automotora Pro'.
        Objetivo: Vender autos del inventario y conseguir que el cliente agende visita.
        
        INVENTARIO ACTUALIZADO (Usa solo esta información):
        {inventory_text}
        
        INSTRUCCIONES:
        - Responde la pregunta del usuario basándote EXCLUSIVAMENTE en el inventario de arriba.
        - Si el auto no existe, ofrece una alternativa similar del inventario.
        - Sé amable, breve y usa emojis.
        - Si el cliente muestra interés, dile: "Haz clic en el botón 'Agendar Visita' de la tarjeta del auto".
        
        Pregunta del Cliente: "{user_message}"
        """

        # 4. Generación
        # Usamos el modelo flash que es rápido
        model = genai.GenerativeModel("gemini-2.5-flash")

        # Usamos generate_content en lugar de chat session para evitar problemas de estado
        response = model.generate_content(full_prompt)

        return response.text

    except Exception as e:
        print(f"❌ Error Crítico en Gemini: {e}")
        # Retornamos un mensaje amigable al usuario
        return "Lo siento, estoy teniendo problemas de conexión con mi cerebro digital. Intenta de nuevo en unos segundos. 🤖🔧"
