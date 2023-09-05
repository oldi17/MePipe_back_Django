import json

from rest_framework.renderers import JSONRenderer


class CommentJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        status_code = data.get('status_code', None)

        if not status_code:
            return json.dumps({
                'comment': data
            })
        
        return super(CommentJSONRenderer, self).render(data)