from django.shortcuts import render


def home(request):
    context = {
        'title': 'this is my site'
    }
    
    return render(request, 'main/home.html', context)



def about(request):
    context = {
        'title': 'This is the About page'
    }
    
    return render(request, 'main/about.html', context)


def contact(request):
    context = {
        'title': 'This is the Contact Page'
    }
    
    return render(request, 'main/contact.html', context)