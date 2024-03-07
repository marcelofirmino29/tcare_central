from django.shortcuts import render
from home.models import TagBle
def index(request):
    tags = TagBle.objects.all()

    context = {
        'tags': tags,
    }
    return render(
        request,
        'home/index.html',
        context
    )
