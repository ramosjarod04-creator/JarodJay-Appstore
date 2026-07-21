from django.shortcuts import render, redirect, get_object_or_404
from .models import Application
from .forms import ApplicationForm

def app_list(val_request):
    apps = Application.objects.all().order_by('-uploaded_at')
    return render(val_request, 'core/index.html', {'apps': apps})

def upload_app(val_request):
    if val_request.method == 'POST':
        form = ApplicationForm(val_request.POST, val_request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            
            # Capture the direct Cloudinary URL from the hidden frontend input field
            file_url = val_request.POST.get('file_url')
            if file_url:
                app.file = file_url
                
            app.save()
            return redirect('app_list')
    else:
        form = ApplicationForm()
    return render(val_request, 'core/upload.html', {'form': form})

# Delete view
def delete_app(val_request, pk):
    app = get_object_or_404(Application, pk=pk)
    if app.file:
        app.file.delete(save=False)
    app.delete()
    return redirect('app_list')