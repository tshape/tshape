# from django.shortcuts import render
# from django.template import RequestContext


def assign_attrs(attr_map, obj):
    for key, value in attr_map.items():
        if not hasattr(obj, key):
            raise AttributeError
        setattr(obj, key, value)
    return obj

# def render_response(req, *args, **kwargs):
#     kwargs['context_instance'] = RequestContext(req)
#     return render(*args, **kwargs)


# def render_to(template_name):
#     def renderer(func):
#         def wrapper(request, *args, **kw):
#             output = func(request, *args, **kw)
#             if not isinstance(output, dict):
#                 return output
#             return render(request, template_name, output)
#         return wrapper
#     return renderer


# class PKContextMixin(object):

#     def get_context_data(self, *args, **kwargs):
#         context = super(
#             PKContextMixin, self).get_context_data(*args, **kwargs)
#         context.update(self.kwargs)
#         return context


class MultiSerializerViewSetMixin(object):

    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        Thanks gonz: http://stackoverflow.com/a/22922156/11440

        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(
                MultiSerializerViewSetMixin, self).get_serializer_class()
