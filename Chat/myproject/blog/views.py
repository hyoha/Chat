# blog/views.py
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import run_model

def blog_main(request):
    # index.html 렌더링
    return render(request, "blog/index.html")

@csrf_exempt
def blog_ask(request):
    if request.method == "POST":
        question = ""
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                question = data.get("question", "").strip()
            except Exception as e:
                return JsonResponse({"answer": f"JSON 파싱 오류: {e}"})
        else:
            question = request.POST.get("question", "").strip()

        if question:
            answer = run_model(question)
            return JsonResponse({"answer": answer})
    return JsonResponse({"answer": "질문이 없습니다."})
