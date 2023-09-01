import json

from rest_framework.renderers import JSONRenderer


class CreatorJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        status_code = data.get('status_code', None)

        if not status_code:
            data.pop('id', None)
            data.pop('user_id', None)
            return json.dumps({
                'creator': data
            })
        
        return super(CreatorJSONRenderer, self).render(data)