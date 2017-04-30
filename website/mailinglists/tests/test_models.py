from django.core.exceptions import ValidationError
from django.test import TestCase

from mailinglists.models import MailingList, ListAlias


class MailingListTest(TestCase):
    """Tests mailing lists"""

    @classmethod
    def setUpTestData(cls):
        cls.mailinglist = MailingList.objects.create(
            name="mailtest",
        )

    def setUp(self):
        self.mailinglist.refresh_from_db()

    def test_clean_works(self):
        self.mailinglist.clean()

    def test_no_alias_duplicates(self):
        listalias = ListAlias(
            alias="mailtest",
            mailinglist=self.mailinglist
        )

        with self.assertRaises(ValidationError):
            listalias.clean()

        listalias.alias = "mailalias"
        listalias.clean()


class ListAliasTest(TestCase):
    """Tests list aliases"""

    @classmethod
    def setUpTestData(cls):
        cls.mailinglist = MailingList.objects.create(
            name="mailtest",
        )
        cls.listalias = ListAlias.objects.create(
            alias="mailalias",
            mailinglist=cls.mailinglist
        )

    def setUp(self):
        self.mailinglist.refresh_from_db()
        self.listalias.refresh_from_db()

    def test_clean_works(self):
        self.listalias.clean()

    def test_no_mailinglist_duplicates(self):
        m1 = MailingList(
            name="mailalias"
        )

        with self.assertRaises(ValidationError):
            m1.clean()

        m1.name = "mailtest2"
        m1.clean()
