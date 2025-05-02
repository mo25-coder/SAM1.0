from django.shortcuts import render
from django.http import JsonResponse
from .models import ChatMessage
import requests, uuid, markdown
from django.views.decorators.csrf import csrf_exempt
import json

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "YOUR_API_KEY"

def get_session_id(request):
    if "session_id" not in request.session:
        request.session["session_id"] = str(uuid.uuid4())
    return request.session["session_id"]

def index(request):
    session_id = get_session_id(request)
    messages = ChatMessage.objects.filter(session_id=session_id).order_by("id")
    formatted_messages = [
        {"role": msg.role, "content": markdown.markdown(msg.content)} for msg in messages
    ]
    return render(request, "chatapp/index.html", {"messages": formatted_messages})

@csrf_exempt
def chat_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_input = data.get("user_input", "")
        session_id = get_session_id(request)

        # Save user message
        ChatMessage.objects.create(session_id=session_id, role="user", content=user_input)

        # Prepare messages for API
        messages = list(ChatMessage.objects.filter(session_id=session_id).values("role", "content"))
        messages.append({"role": "user", "content": user_input})

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept-Charset": "UTF-8"
        }

        body = {
            "model": "mistralai/mistral-small-3.1-24b-instruct:free",
            "messages": messages
        }

        try:
            res = requests.post(API_URL, headers=headers, json=body)
            result = res.json()
            assistant_response = result["choices"][0]["message"]["content"]
        except Exception as e:
            assistant_response = f"⚠️ Error: {str(e)}"

        # Save assistant response
        ChatMessage.objects.create(session_id=session_id, role="assistant", content=assistant_response)

        return JsonResponse({"response": markdown.markdown(assistant_response)})
