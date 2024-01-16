from .models import Category


def category_list_variables(request):
    category_list = Category.objects.all()
    context = {'category_list': category_list}
    return context
