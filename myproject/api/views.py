# api/views.py
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decouple import config

CHATBOT_API = config('CHATBOT_API', default='default')
CHATBOT_URL = config('CHATBOT_URL', default='default')

client = openai.OpenAI(api_key=CHATBOT_API, base_url=CHATBOT_URL)

@csrf_exempt
def chat(request):
    if request.method == 'GET':
        return JsonResponse({"error": "Please send a POST request"})
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        print(response.choices[0].message.content)
        return JsonResponse({"response": response.choices[0].message.content})