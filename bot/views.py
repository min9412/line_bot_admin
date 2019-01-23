import os
import logging

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import (
    HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
)
from linebot import (
    WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)

from line_api import service as line_service
from line_group_admin import db_manager

logger = logging.getLogger(__name__)

ChannelSecret = os.environ.get('ChannelSecret', '')

parser = WebhookParser(ChannelSecret)


@csrf_exempt
@require_http_methods(['POST'])
def callback(request):
    body = request.body.decode('utf-8')
    signature = request.META['HTTP_X_LINE_SIGNATURE']

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        return HttpResponseForbidden()
    except LineBotApiError:
        return HttpResponseBadRequest()

    for event in events:
        # logger.info('event:{}\n{}'.format(type(event), event))
        print('event:{}\n{}'.format(type(event), event))

        if event.type == 'message':

            message = event.message
            if message.type == 'text':

                # Repost
                if event.source.type is "group":
                    repost(event)
        elif event.type == 'join':
            join_group(event)

    return HttpResponse()


def repost(event):
    group_id = event.source.group_id

    from_group = db_manager.get_group_by_line_id(group_id)
    emba_group_name = from_group.emba_group_name
    groups = db_manager.get_groups_by_emba_group_name(emba_group_name)

    user_name = ''
    if event.source.user_id:
        member_id = event.source.user_id
        profile = line_service.get_group_member_profile(group_id, member_id)
        user_name = profile.display_name

    message = "{index} 【{name}】 {message}".format(
        index=from_group.line_group_name,
        name=user_name,
        message=event.message.text
    )

    for group in groups:
        line_id = group.line_group_id
        if line_id != group_id:
            line_service.push_text_message(line_id, message)


def join_group(event):
    group_id = event.source.group_id

    message = '群組 ID: %s' % group_id

    to_insert = {
        'line_group_name': '',
        'emba_group_name': '',
        'created_by': 'line_bot'
    }

    result = db_manager.get_or_create_group(group_id, to_insert)
    line_service.push_text_message(group_id, message)
