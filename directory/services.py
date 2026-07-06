from .models import ConferenceGroup


def explicit_conference_group_exists(children):
    child_ids = set(child.id for child in children)
    if len(child_ids) < 2:
        return False

    candidate_groups = ConferenceGroup.objects.filter(
        is_active=True,
        members__id__in=child_ids,
    ).distinct()

    for group in candidate_groups:
        member_ids = set(group.members.values_list("id", flat=True))
        if child_ids.issubset(member_ids):
            return True
    return False


def children_may_conference(children):
    participants = list(children)
    if len({child.id for child in participants}) < 2:
        return True

    return explicit_conference_group_exists(participants)
