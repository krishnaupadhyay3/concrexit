from django.conf import settings
from django.utils import timezone

from activemembers.models import CommitteeMembership, Mentorship, Board
from members.models import Member
from utils.snippets import datetime_to_lectureyear


def get_automatic_lists():
    memberships = (CommitteeMembership.active_memberships
                   .filter(committee__board=None)
                   .filter(chair=True)
                   .prefetch_related('member'))
    committee_chairs = [x.member for x in memberships] + [
        Member(email='intern@thalia.nu')
    ]

    active_committee_memberships = (CommitteeMembership.active_memberships
                                    .exclude(committee__board__is_board=True)
                                    .prefetch_related('member'))
    active_members = [x.member for x in active_committee_memberships]

    lectureyear = datetime_to_lectureyear(timezone.now())
    # Change to next lecture year after December
    if 0 < timezone.now().month < 9:
        lectureyear += 1
    active_mentorships = Mentorship.objects.filter(
        year=lectureyear)
    mentors = [x.member for x in active_mentorships]

    lists = []

    lists += _create_automatic_list(
        ['leden', 'members'], '[THALIA]',
        Member.all_with_membership('member'), True, True, True)
    lists += _create_automatic_list(
        ['begunstigers', 'supporters'], '[THALIA]', Member.all_with_membership(
            'supporter'), multilingual=True)
    lists += _create_automatic_list(
        ['ereleden', 'honorary'], '[THALIA]', Member.all_with_membership(
            'honorary'), multilingual=True)
    lists += _create_automatic_list(
        ['mentors'], '[THALIA] [MENTORS]', mentors, moderated=False)
    lists += _create_automatic_list(
        ['activemembers'], '[THALIA] [COMMITTEES]',
        active_members)
    lists += _create_automatic_list(
        ['commissievoorzitters', 'committeechairs'], '[THALIA] [CHAIRS]',
        committee_chairs, moderated=False)
    lists += _create_automatic_list(
        ['optin'], '[THALIA] [OPTIN]', Member.current_members.filter(
            profile__receive_optin=True),
        multilingual=True)

    for year in range(Board.objects.earliest('since').since.year, lectureyear):
        board = Board.objects.get(since__year=year)
        if board is not None:
            lists += _create_automatic_list(
                ['bestuur'
                 + str(board.since.year)[-2:] + str(board.until.year)[-2:],
                 'board'
                 + str(board.since.year)[-2:] + str(board.until.year)[-2:]],
                '',
                [x.member for x in CommitteeMembership.objects
                    .filter(committee=board).prefetch_related('member')],
                archived=False, moderated=False, multilingual=False
            )

    return lists


def _create_automatic_list(names, prefix, members,
                           archived=True, moderated=True, multilingual=False):
    data = {
        'names': names,
        'prefix': prefix,
        'archived': archived,
        'moderated': moderated,
    }

    if multilingual:
        data['addresses'] = [member.email for member in members]
        yield data  # this is the complete list, e.g. leden@
        for language in settings.LANGUAGES:
            localized_data = data.copy()
            localized_data['addresses'] = [
                member.email for member in members
                if member.profile.language == language[0]]
            localized_data['names'] = [
                '{}-{}'.format(n, language[0]) for n in names]
            yield localized_data  # these are localized lists, e.g. leden-nl@
    else:
        data['addresses'] = [member.email for member in members]
        yield data
