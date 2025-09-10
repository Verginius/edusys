from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import AIInteraction
import json

@login_required
def ai_assistant_page(request):
    interactions = AIInteraction.objects.filter(user=request.user).order_by('timestamp')
    return render(request, 'agents/ai_assistant.html', {'interactions': interactions})

@login_required
@require_POST
def ask_ai(request):
    try:
        data = json.loads(request.body)
        query = data.get('query')
        if not query:
            return JsonResponse({'success': False, 'error': {'message': 'Query is required.'}}, status=400)

        # 在这里处理 AI 逻辑（为了简单起见，我们只返回一个固定的响应）
        response_text = f"这是对 ‘{query}’ 的响应。"

        interaction = AIInteraction.objects.create(
            user=request.user,
            query=query,
            response=response_text
        )
        return JsonResponse({'success': True, 'data': {'response': response_text, 'timestamp': interaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')}})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'message': 'Invalid JSON.'}}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': {'message': str(e)}}, status=500)

@login_required
@require_POST
def clear_ai_history(request):
    AIInteraction.objects.filter(user=request.user).delete()
    return redirect('agents:ai_assistant_page')