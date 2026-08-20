import os
from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
from openai import OpenAI

from .policies import RUHAVA_POLICIES


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def chat(request):
    user_message = request.GET.get("message", "")

    if not user_message:
        return JsonResponse({
            "response": "Please ask me a question about Ruhava."
        })

    prompt = f"""
You are Ruhava's customer support assistant.

Answer the customer's question using ONLY the Ruhava information
provided below.

If the answer is not available in the provided information,
say that you don't have enough information and suggest contacting
Ruhava customer support.

Never invent or assume a Ruhava policy.

RUHAVA INFORMATION:
{RUHAVA_POLICIES}

CUSTOMER QUESTION:
{user_message}
"""

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )

    return JsonResponse({
        "response": response.output_text
    })

def chat_page(request):
    return render(request,"ai_chat.html")