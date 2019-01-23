from bot import db_manager
from line_api import service


def repost(event):
    # Get line group belongs group
    line_id = event.source.group_id
    line_group = db_manager.get_line_group_by_line_id(line_id)
    if not line_group:
        return

    # Get line group index
    group_index = get_index_from_name(line_group.name)

    # Get group member info
    member_id = event.source.user_id
    member_info = service.get_group_member_profile(line_id, member_id)
    member_name = member_info.display_name

    # Compose repost message
    message = '{index}組 【{name}】 {message}'.format(
        index=group_index,
        name=member_name,
        message=event.message.text
    )

    # Get all other line groups
    line_groups = db_manager.get_line_groups_by_group_id(line_group.group_id)

    # Repost to other line groups
    for group in line_groups:
        if group.id != line_group.id:
            service.push_text_message(group.line_id, message)


def add_line_group_to_repost(event, group_name):
    line_id = event.source.group_id

    # Get group by group_name
    group = db_manager.get_group_by_group_name(group_name)
    if not group_name:
        service.push_text_message(line_id, '查無群組名稱')
        return

    # check if added
    line_group = db_manager.get_line_group_by_line_id(line_id)
    if line_group:
        group = db_manager.get_group(line_group.group_id)
        service.push_text_message(line_id, '此群組已加入{}轉貼'.format(group.name))
        return

    # Add line group
    to_insert = {
        'name': 'test',
        'line_id': line_id,
        'group_id': group.id
    }
    line_group = db_manager.add_line_group(to_insert)
    if not line_group:
        service.push_text_message(line_id, '新增群組錯誤')
        return

    service.push_text_message(
        line_id, '新增『{}』至{}'.format(line_group.name, group.name)
    )


def get_index_from_name(name):
    pos = name.find('組')

    if pos - 1 < 0:
        return 'A'

    return name[pos-1]
