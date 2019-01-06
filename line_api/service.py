import os

from linebot import (
    LineBotApi
)
from linebot.models import (
    TextSendMessage
)

AccessToken = os.environ.get('ChannelAccessToken', '')

line_bot_api = LineBotApi(AccessToken)


def push_text_message(line_id, message):
    line_bot_api.push_message(
        line_id, TextSendMessage(text=message)
    )


def reply_text_message(reply_token, message):
    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(text=message)
    )


def get_group_member_profile(group_id, member_id):
    profile = line_bot_api.get_group_member_profile(group_id, member_id)

    return profile
