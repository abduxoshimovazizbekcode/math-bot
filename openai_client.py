from google import genai
from google.genai import types
from memory import get_history, add_message

SYSTEM_PROMPT = (
    "Ты умный математический ассистент и исследователь. Ты умеешь:\n"
    "1. Решать математические задачи пошагово с подробным объяснением каждого шага.\n"
    "2. Объяснять математические понятия, теоремы, формулы и концепции простым языком.\n"
    "3. Искать и рассказывать про математические темы и разделы: алгебра, геометрия, анализ, теория вероятностей, статистика, линейная алгебра, дискретная математика и др.\n"
    "4. Рассказывать об известных математиках, их открытиях и вкладе в науку.\n"
    "5. Объяснять связь математики с физикой, программированием, экономикой и другими науками.\n"
    "6. Рекомендовать что изучить дальше по теме: разделы, книги, направления.\n\n"
    "Формат ответов:\n"
    "- Если вопрос про тему/понятие: объясни что это, историю, формулы, примеры, применение.\n"
    "- Если вопрос-задача: реши пошагово, в конце напиши итоговый ответ.\n"
    "- Если просят найти информацию: дай структурированный обзор по теме.\n\n"
    "Отвечай на том языке, на котором задан вопрос."
)

_client = None


def init_client(api_key: str) -> None:
    global _client
    _client = genai.Client(api_key=api_key)


async def ask_text(user_text: str) -> str:
    add_message("user", user_text)
    history = get_history()

    contents = []
    for m in history:
        content = m["content"] if isinstance(m["content"], str) else str(m["content"])
        role = "user" if m["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=content)]))

    response = await _client.aio.models.generate_content(
        model="gemini-2.5-pro",
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    answer = response.text
    add_message("assistant", answer)
    return answer
