import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from openai import OpenAI
import json
from dotenv import load_dotenv
import logging
from typing import Dict, Any

# Завантаження змінних середовища з файлу .env
load_dotenv()

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація клієнта OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="BizModelAI API")

# Налаштування CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # У продакшені замініть на конкретні домени
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтування статичних файлів
app.mount("/static", StaticFiles(directory="static"), name="static")

class BusinessIdea(BaseModel):
    description: str

class BusinessModelCanvas(BaseModel):
    ключові_партнерства: Dict[str, Any] = Field(...)
    ключові_види_діяльності: Dict[str, Any] = Field(...)
    ціннісні_пропозиції: Dict[str, Any] = Field(...)
    відносини_з_клієнтами: Dict[str, Any] = Field(...)
    сегменти_клієнтів: Dict[str, Any] = Field(...)
    ключові_ресурси: Dict[str, Any] = Field(...)
    канали: Dict[str, Any] = Field(...)
    структура_витрат: Dict[str, Any] = Field(...)
    потоки_доходів: Dict[str, Any] = Field(...)

class AdditionalAnalysisRequest(BaseModel):
    initial_analysis: Dict[str, Any]
    business_idea: str
def generate_business_model_canvas(idea: str):
    prompt = f"""
    Ви - експерт з бізнес-моделювання. Ваше завдання - заповнити бізнес-модель канвас на основі короткого опису бізнес-ідеї. 
    Бізнес-модель канвас складається з 9 блоків. Надайте відповідь у форматі JSON, де ключі відповідають компонентам канвасу українською мовою, а значення - це об'єкти з деталізованою інформацією:

    1. Ключові партнерства:
       - Ключові партнери
       - Постачальники
       - Ресурси, які отримуємо від партнерів
       - Діяльність, яку виконують партнери

    2. Ключові види діяльності:
       - Які ключові види діяльності вимагають наші ціннісні пропозиції?
       - Наші канали збуту?
       - Відносини з клієнтами?
       - Потоки доходів?

    3. Ціннісні пропозиції:
       - Яку цінність ми надаємо клієнту?
       - Які проблеми клієнтів ми допомагаємо вирішити?
       - Які потреби клієнтів ми задовольняємо?
       - Які набори продуктів та послуг ми пропонуємо кожному сегменту клієнтів?
       
       Характеристики:
       - Новизна
       - Продуктивність
       - Адаптація
       - "Виконання роботи"
       - Дизайн
       - Бренд/Статус
       - Ціна
       - Зниження витрат
       - Зниження ризику
       - Доступність
       - Зручність/Корисність

    4. Відносини з клієнтами:
       - Яких відносин очікують від нас клієнти з різних сегментів?
       - Які відносини ми встановили?
       - Наскільки вони інтегровані з рештою нашої бізнес-моделі?
       - Наскільки вони затратні?
       
       Приклади:
       - Персональна підтримка
       - Виділений персональний менеджер
       - Самообслуговування
       - Автоматизовані послуги
       - Спільноти
       - Співтворчість

    5. Сегменти клієнтів:
       - Для кого ми створюємо цінність?
       - Хто наші найважливіші клієнти?
       
       Масовий ринок
       Нішевий ринок
       Сегментований
       Диверсифікований
       Багатосторонні платформи

    6. Ключові ресурси:
       - Які ключові ресурси необхідні для наших ціннісних пропозицій?
       - Наших каналів збуту?
       - Відносин з клієнтами?
       - Потоків доходів?
       
       Види ресурсів:
       - Фізичні
       - Інтелектуальні (патенти на бренди, авторські права, дані)
       - Людські
       - Фінансові

    7. Канали:
       - Через які канали наші сегменти клієнтів хочуть, щоб їх досягли?
       - Як ми досягаємо їх зараз?
       - Як наші канали інтегровані?
       - Які працюють найкраще?
       - Які найбільш економічно ефективні?
       - Як ми інтегруємо їх з процедурами клієнтів?
       
       Фази каналів:
       1. Обізнаність
       2. Оцінка
       3. Купівля
       4. Доставка
       5. Післяпродажне обслуговування

    8. Структура витрат:
       - Які найважливіші витрати, притаманні нашій бізнес-моделі?
       - Які ключові ресурси найдорожчі?
       - Які ключові види діяльності найдорожчі?
       
       Ваш бізнес більше:
       - Орієнтований на витрати (найнижча структура витрат, низька цінова ціннісна пропозиція, максимальна автоматизація, широкий аутсорсинг)
       - Орієнтований на цінність (зосереджений на створенні цінності, преміальна ціннісна пропозиція)
       
       Приклади характеристик:
       - Фіксовані витрати (зарплати, оренда, комунальні послуги)
       - Змінні витрати
       - Економія на масштабі
       - Економія на обсязі

    9. Потоки доходів:
       - За яку цінність наші клієнти дійсно готові платити?
       - За що вони платять зараз?
       - Як вони платять зараз?
       - Як би вони хотіли платити?
       - Який внесок кожного потоку доходів у загальні доходи?
       
       Види:
       - Продаж активів
       - Плата за використання
       - Плата за підписку
       - Кредитування/Оренда/Лізинг
       - Ліцензування
       - Брокерські відрахування
       - Реклама
       
       Фіксована ціна:
       - Фіксований прайс-лист
       - Залежить від характеристик продукту
       - Залежить від сегменту клієнтів
       - Залежить від обсягу
       
       Динамічна ціна:
       - Переговори (торг)
       - Управління доходністю
       - Ринок реального часуоходів

    Опис бізнес-ідеї: {idea}
    
    Надайте відповідь у форматі JSON, де ключі відповідають компонентам канвасу українською мовою, а значення - це об'єкти з деталізованою інформацією згідно з описаною структурою. Не використовуйте потрійні зворотні лапки (```) у вашій відповіді.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ви - експерт з бізнес-моделювання."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        logging.info(f"Відповідь від OpenAI: {response}")
        
        # Видаляємо потрійні зворотні лапки, якщо вони є
        content = response.choices[0].message.content.strip('`')
        if content.startswith('json\n'):
            content = content[5:]  # Видаляємо 'json\n' на початку, якщо воно є
        
        result = json.loads(content)
        
        # Перевірка та корекція ключів
        correct_keys = {
            "ключові_партнерства": "Ключові партнерства",
            "ключові_види_діяльності": "Ключові види діяльності",
            "ціннісні_пропозиції": "Ціннісні пропозиції",
            "відносини_з_клієнтами": "Відносини з клієнтами",
            "сегменти_клієнтів": "Сегменти клієнтів",
            "ключові_ресурси": "Ключові ресурси",
            "канали": "Канали",
            "структура_витрат": "Структура витрат",
            "потоки_доходів": "Потоки доходів"
        }
        
        corrected_result = {}
        for correct_key, display_key in correct_keys.items():
            corrected_result[correct_key] = result.get(display_key, {})
        
        return corrected_result
    except json.JSONDecodeError as e:
        logging.error(f"Помилка при розборі JSON: {str(e)}")
        logging.error(f"Отриманий контент: {content}")
        raise
    except Exception as e:
        logging.error(f"Помилка під час виклику OpenAI: {str(e)}")
        raise

def generate_additional_analysis(initial_analysis: Dict[str, Any], business_idea: str):
    prompt = f"""
    На основі наданого початкового аналізу бізнес-моделі та бізнес-ідеї, надайте додатковий аналіз, 
    який включає наступні аспекти:
    
    1. Потенційні ризики та способи їх мінімізації
    2. Можливості для масштабування бізнесу
    3. Ключові метрики для відстеження успіху
    4. Потенційні інноваційні ідеї для розвитку бізнесу
    5. Рекомендації щодо стратегії виходу на ринок
    
    Початковий аналіз: {json.dumps(initial_analysis, ensure_ascii=False)}
    Бізнес-ідея: {business_idea}
    
    Надайте відповідь у форматі JSON з ключами для кожного аспекту.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ви - експерт з бізнес-моделювання та стратегічного аналізу."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        content = response.choices[0].message.content.strip('`')
        if content.startswith('json\n'):
            content = content[5:]
        
        result = json.loads(content)
        return result
    except Exception as e:
        logging.error(f"Помилка при генерації додаткового аналізу: {str(e)}")
        raise

@app.post("/api/analyze", response_model=BusinessModelCanvas)
async def analyze_business_idea(idea: BusinessIdea):
    try:
        canvas = generate_business_model_canvas(idea.description)
        return BusinessModelCanvas(**canvas)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Помилка при розборі відповіді від AI")
    except Exception as e:
        logging.error(f"Помилка при аналізі бізнес-ідеї: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/additional_analysis")
async def get_additional_analysis(request: AdditionalAnalysisRequest):
    try:
        additional_analysis = generate_additional_analysis(request.initial_analysis, request.business_idea)
        return additional_analysis
    except Exception as e:
        logging.error(f"Помилка при отриманні додаткового аналізу: {str(e)}")
        raise HTTPException(status_code=500, detail="Помилка при отриманні додаткового аналізу")
    
@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)