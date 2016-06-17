from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('profiles/index.html')
    return HttpResponse(template.render(request))

def skillsets(request):
    template = loader.get_template('profiles/skillsets.html')
    return HttpResponse(template.render(request))

def skill(request):
    template = loader.get_template('profiles/skill.html')
    return HttpResponse(template.render(request))
