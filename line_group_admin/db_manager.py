from line_group_admin import models


def get_group_by_line_id(line_id):
    result = models.LineGroup.objects.filter(
        line_group_id=line_id
    ).first()

    return result


def get_groups_by_emba_group_name(name):
    results = models.LineGroup.objects.filter(
        emba_group_name=name
    )

    return results


def get_or_create_group(line_id, to_insert):
    result = models.LineGroup.objects.get_or_create(
        line_group_id=line_id, defaults=to_insert
    )
    return result
