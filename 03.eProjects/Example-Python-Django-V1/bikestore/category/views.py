from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse
from .models import Category

#entry point
#URL: /categories
def categories(request):
    categories = Category.objects.all().values()
    template = loader.get_template('main.html')
    context = {
        'categories': categories,
    }
    # có thể dùng HttpResponse
    return HttpResponse(template.render(context, request))

#URL: /categories/details/:id
def details(request, id):
    categories = get_object_or_404(Category, pk=id)
    context = {
        'categories': categories,
    }
    # có thể dùng trực tiếp hàm render
    return render(request, "details.html", context)
