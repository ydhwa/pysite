from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, '_bs/main/index.html')


def handler404(request, *args, **argv):
    response = render(request, "error/404.html", {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, "error/500.html", {})
    response.status_code = 500
    return response