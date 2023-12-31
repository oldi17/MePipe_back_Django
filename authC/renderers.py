import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        status_code = data.get('status_code', None)

        if not status_code:
            return json.dumps({
                'user': data
            })
        
        return super(UserJSONRenderer, self).render(data)