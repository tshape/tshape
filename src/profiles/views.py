from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('profiles/index.html')
    context = {
        'latest_question_list': "test",
    }
    return HttpResponse(template.render(context, request))
