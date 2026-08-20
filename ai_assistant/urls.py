from django.urls import path
from . import views
app_name="ai_assistant"
urlpatterns = [
    path("chat/", views.chat,name="ai_chat"),
    path("chat_page/", views.chat_page,name="chat_page"),
]
