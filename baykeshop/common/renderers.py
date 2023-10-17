from rest_framework import renderers
from rest_framework.utils.serializer_helpers import ReturnList
from django.core.serializers.json import DjangoJSONEncoder


class JSONRenderer(renderers.JSONRenderer):
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return super().render(data, accepted_media_type, renderer_context)
    

class TemplateHTMLRenderer(renderers.TemplateHTMLRenderer):
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, ReturnList):
            data = {"results": data}
        return super().render(data, accepted_media_type, renderer_context)