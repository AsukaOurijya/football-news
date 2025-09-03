from django.shortcuts import render

# Create your views here.

def show_main(request):
    context ={
        'npm' : '2406431510',
        'name' : 'Muhammad Azka Awliya',
        'class' : 'PBP C'
    }

    return render(request, "main.html", context)