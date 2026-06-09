from google import genai
from google.genai import types
from memory import get_history, add_message

SYSTEM_PROMPT = (
    "Ты математический помощник и преподаватель. Ты умеешь:\n"
    "1. Решать математические задачи пошагово с объяснением каждого шага.\n"
    "2. Объяснять математические понятия, теоремы и концепции простым языком.\n"
    "3. Приводить примеры из реальной жизни и области применения.\n"
    "4. Давать ссылки на темы для дальнейшего изучения (учебники, разделы математики).\n"
    "Если вопрос про понятие или теорию — объясни подробно: что это, зачем нужно, где применяется, приведи пример.\n"
    "Если вопрос-задача — реши пошагово.\n"
    "Используй понятные математические обозначения.\n"
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
