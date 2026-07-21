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
        if val_request.content_type == 'application/json':
            try:
                data = json.loads(val_request.body)
                Application.objects.create(
                    name=data.get('name'),
                    version=data.get('version'),
                    description=data.get('description'),
                    file=data.get('file_url')
                )
                return JsonResponse({'status': 'success'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
        form = ApplicationForm(val_request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            file_url = val_request.POST.get('file_url')
            if file_url:
                app.file = file_url
            app.save()
            return redirect('app_list')
    else:
        form = ApplicationForm()
    return render(val_request, 'core/upload.html', {'form': form})

def delete_app(val_request, pk):
    app = get_object_or_404(Application, pk=pk)
    if app.file:
        app.file.delete(save=False)
    app.delete()
    return redirect('app_list')