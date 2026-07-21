import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Application
from .forms import ApplicationForm

def app_list(val_request):
    apps = Application.objects.all().order_by('-uploaded_at')
    return render(val_request, 'core/index.html', {'apps': apps})

@csrf_exempt
def upload_app(val_request):
    if val_request.method == 'POST':
        # Strictly process JSON data payloads coming from the client-side Cloudinary widget script
        try:
            if val_request.content_type == 'application/json':
                data = json.loads(val_request.body)
            else:
                data = val_request.POST

            name = data.get('name')
            version = data.get('version')
            description = data.get('description')
            file_url = data.get('file_url')

            if not name or not file_url:
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

            Application.objects.create(
                name=name,
                version=version,
                description=description,
                file=file_url
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return render(val_request, 'core/upload.html')

def delete_app(val_request, pk):
    app = get_object_or_404(Application, pk=pk)
    # Safely delete the database record without throwing storage file errors on Cloudinary string URLs
    app.delete()
    return redirect('app_list')