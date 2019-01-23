from group import models


# Line Group
def get_line_group_by_line_id(line_id):
    result = models.LineGroup.objects.filter(
        line_id=line_id
    ).first()

    return result


def get_line_groups_by_group_id(group_id):
    results = models.LineGroup.objects.filter(
        group_id=group_id
    )

    return results


def add_line_group(to_insert):
    result = models.LineGroup.objects.create(**to_insert)

    return result
