from django.shortcuts import get_object_or_404, render, redirect, reverse

from utils.translation import localize_attr_name
from .models import Board, Committee, CommitteeMembership


def committee_index(request):
    """Overview of committees"""

    committees = Committee.active_committees.all().order_by(
        localize_attr_name('name'))

    return render(request, 'activemembers/committee_index.html',
                  {'committees': committees})


def committee_detail(request, id):
    """View the details of a committee"""
    committee = get_object_or_404(Committee, pk=id)

    members = []
    memberships = (CommitteeMembership
                   .active_memberships
                   .filter(committee=committee)
                   .prefetch_related('member__committeemembership_set'))
    for membership in memberships:
        member = membership.member
        member.chair = membership.chair
        member.committee_since = membership.initial_connected_membership.since
        members.append(member)  # list comprehension would be more pythonic?

    members.sort(key=lambda x: x.committee_since)

    return render(request, 'activemembers/committee_detail.html',
                  {'committee': committee,
                   'members': members})


def board_index(request):
    boards = Board.objects.all()

    return render(request,
                  'activemembers/board_index.html',
                  {'boards': boards})


def board_detail(request, year):
    """View the details of a board"""
    since, until = year.split('-')
    board = get_object_or_404(Board, since__year=since, until__year=until)
    members = []
    memberships = (CommitteeMembership
                   .objects
                   .filter(committee=board)
                   .prefetch_related('member'))

    for membership in memberships:
        member = membership.member
        member.chair = membership.chair
        member.role = membership.role
        members.append(member)  # list comprehension would be more pythonic?

    return render(request, 'activemembers/board_detail.html',
                  {'board': board,
                   'members': members})


def current_board(request):
    try:
        board = Board.objects.order_by('-since')[0]
    except IndexError:
        return redirect(reverse('activemembers:boards'))
    return redirect(board.get_absolute_url())
