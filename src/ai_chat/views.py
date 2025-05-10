from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import PyPDF2
import g4f


@login_required
def analyze_resume(request: HttpRequest):
    ai_response = None

    if request.method == 'POST' and request.FILES.get('pdf_file'):
        try:
            # Чтение PDF
            pdf = PyPDF2.PdfReader(request.FILES['pdf_file'])
            text = "\n".join([page.extract_text() for page in pdf.pages])

            # Промт для AI
            prompt = (
                "Ты — карьерный консультант и технический эксперт в сфере IT. "
                "Твоя задача — проанализировать резюме IT-специалиста (разработчика) и дать краткие, но полезные рекомендации по улучшению.\n\n"
                "Проверь следующее:\n"
                "- Насколько резюме понятно, структурировано и легко читается.\n"
                "- Видно ли в нём позиционирование: на кого претендует кандидат.\n"
                "- Подходит ли содержание под роль разработчика: навыки, стек, достижения, релевантный опыт.\n"
                "- Есть ли технические или смысловые слабые места.\n\n"
                "Ответь строго по структуре:\n\n"
                "1. Краткая оценка резюме в 1–2 предложениях.\n"
                "(Общее впечатление, насколько оно профессионально и понятно).\n\n"
                "2. Слабые стороны (до 3 пунктов):\n"
                "(Например: неясное позиционирование, отсутствуют ключевые технологии, слабое оформление проектов и т.д.)\n\n"
                "3. Что улучшить (3–5 конкретных рекомендаций):\n"
                "(Переформулировать, добавить, изменить — с фокусом на цели кандидата).\n\n"
                "4. Какие навыки/технологии стоит прокачать:\n"
                "(Например: Docker, TypeScript, системное проектирование, английский язык и т.п.)\n\n"
                "Форматируй ответ чётко и лаконично, используй списки. "
                "Никакого вступления или благодарностей — только аналитика."
                "Если ты понимаешь, ты читаешь не резюме, а что-то другое, тогда выведи краткий ответ - ЭТО НЕ РЕЗЮМЕ!\n\n"
                f"Текст резюме:\n{text}"
            )

            # Запрос к AI
            response = g4f.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )

            ai_response = response.strip()

        except Exception as e:
            ai_response = f"Ошибка: {str(e)}"

    return render(request, 'ai_chat/analyze.html', {'response': ai_response})
