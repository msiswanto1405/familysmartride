from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'ride/home.html')

def grabspecial(request):
    return render(request, 'ride/grabspecial.html')

def loading(request):
    return render(request, 'ride/loading.html')

def driverfound(request):
    return render(request, 'ride/driverfound.html')

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        # Handle file upload logic here
    return render(request, 'ride/upload.html')

