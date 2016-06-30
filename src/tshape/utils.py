from django.shortcuts import render
from django.template import RequestContext


def render_response(req, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(req)
    return render(*args, **kwargs)


def render_to(template_name):
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if not isinstance(output, dict):
                return output
            return render(request, template_name, output)
        return wrapper
    return renderer


class PKContextMixin(object):

    def get_context_data(self, *args, **kwargs):
        context = super(PKContextMixin, self).get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        return context
