from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.


def home(request):
    # return HttpResponse("Hello, Django!")
    print(request.build_absolute_uri())  # optional
    return render(
        request,
        'pmiot/hello.html'
    )
