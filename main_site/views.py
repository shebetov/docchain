from django.shortcuts import render


def home(request):
    return render(request, 'main_site/home.html')

def registration(request):
    return render(request, 'main_site/registration.html')

def about_organization(request):
    return render(request, 'main_site/about_organization.html')

def about_docchain(request):
    return render(request, 'main_site/about_docchain.html')

def contact(request):
    return render(request, 'main_site/contact.html')