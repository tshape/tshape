from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView


class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


# @require_http_methods(['GET', 'POST'])
class IndexView(TemplateView):

    template_name = 'index.html'
