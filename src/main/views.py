from django.shortcuts import render
from .forms import ContactForm
from django.core.mail import send_mail

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
    sent = False
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            subject = f"{username} sent a contact message! email: {email}"
            msg = form.cleaned_data.get('message')
            send_mail(subject, msg, 'admin@blog.com', ['miclemabasie3@gmail.com']) 
            sent = True
        else:
            print(form.errors)
    form = ContactForm()

    context = {
        'title': 'This is the Contact Page',
        'form': form,
        'sent': sent,
    }
    
    return render(request, 'main/contact.html', context)