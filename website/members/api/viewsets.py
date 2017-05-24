import copy
from datetime import datetime

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework import permissions

from members.api.serializers import MemberBirthdaySerializer, MemberSerializer
from members.models import Member


class MemberViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Member.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MemberSerializer

    def _get_birthdays(self, member, start, end):
        birthdays = []

        start_year = max(start.year, member.birthday.year)
        for year in range(start_year, end.year + 1):
            bday = copy.deepcopy(member)
            try:
                bday.birthday = bday.birthday.replace(year=year)
            except ValueError as e:
                if bday.birthday.month == 2 and bday.birthday.day == 29:
                    bday.birthday = bday.birthday.replace(year=year, day=28)
                else:
                    raise e
            if start.date() <= bday.birthday <= end.date():
                birthdays.append(bday)

        return birthdays

    @list_route()
    def birthdays(self, request):
        try:
            start = timezone.make_aware(
                datetime.strptime(request.query_params['start'], '%Y-%m-%d')
            )
            end = timezone.make_aware(
                datetime.strptime(request.query_params['end'], '%Y-%m-%d')
            )
        except:
            raise ParseError(detail='start or end query parameters invalid')

        queryset = (
            Member
            .active_members
            .with_birthdays_in_range(start, end)
            .filter(show_birthday=True)
        )

        all_birthdays = [
            self._get_birthdays(m, start, end)
            for m in queryset.all()
        ]
        birthdays = [x for sublist in all_birthdays for x in sublist]

        serializer = MemberBirthdaySerializer(birthdays, many=True)
        return Response(serializer.data)

    @list_route()
    def info(self, request):
        serializer = MemberSerializer(request.user.member)

        return Response(serializer.data)
