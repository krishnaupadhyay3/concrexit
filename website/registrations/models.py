import uuid

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers, validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from members.models import Membership, Profile
from registrations import emails
from thaliawebsite.settings import settings


class Entry(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), default=timezone.now)

    STATUS_CONFIRM = 'confirm'
    STATUS_REVIEW = 'review'
    STATUS_REJECTED = 'rejected'
    STATUS_ACCEPTED = 'accepted'

    STATUS_TYPE = (
        (STATUS_CONFIRM, _('Awaiting email confirmation')),
        (STATUS_REVIEW, _('Ready for review')),
        (STATUS_REJECTED, _('Rejected')),
        (STATUS_ACCEPTED, _('Accepted')),
    )

    status = models.CharField(
        verbose_name=_('status'),
        choices=STATUS_TYPE,
        max_length=20,
        default='confirm',
    )

    MEMBERSHIP_YEAR = 'year'
    MEMBERSHIP_STUDY = 'study'

    MEMBERSHIP_LENGTHS = (
        (MEMBERSHIP_YEAR, _('One year')),
        (MEMBERSHIP_STUDY, _('Until graduation')),
    )

    length = models.CharField(
        verbose_name=_('membership length'),
        choices=MEMBERSHIP_LENGTHS,
        max_length=20,
    )

    MEMBERSHIP_TYPES = [m for m in Membership.MEMBERSHIP_TYPES
                        if m[0] != Membership.HONORARY]

    membership_type = models.CharField(
        verbose_name=_('membership type'),
        choices=MEMBERSHIP_TYPES,
        max_length=40,
        default=Membership.MEMBER,
    )

    remarks = models.TextField(
        _('remarks'),
        blank=True,
        null=True,
    )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if (self.status != self.STATUS_ACCEPTED and
                self.status != self.STATUS_REJECTED):
            self.updated_at = timezone.now()

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        try:
            return self.registration.__str__()
        except Registration.DoesNotExist:
            pass
        try:
            return self.renewal.__str__()
        except Renewal.DoesNotExist:
            pass
        return super().__str__()

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        permissions = (
            ('review_entries', _("Review registration and renewal entries")),
        )


class Registration(Entry):

    # ---- Personal information -----

    username = models.CharField(
        _('Username'),
        max_length=150,
        blank=True,
        null=True,
        help_text=_('Enter value to override the auto-generated username '
                    '(e.g. if it is not unique)')
    )

    first_name = models.CharField(
        _('First name'),
        max_length=30,
        blank=False,
    )

    last_name = models.CharField(
        _('Last name'),
        max_length=200,
        blank=False,
    )

    birthday = models.DateField(
        verbose_name=_('birthday'),
        blank=False,
    )

    language = models.CharField(
        verbose_name=_('language'),
        max_length=5,
        choices=settings.LANGUAGES,
        default='nl',
    )

    # ---- Contact information -----

    email = models.EmailField(
        _('Email address'),
        blank=False,
    )

    phone_number = models.CharField(
        max_length=20,
        verbose_name=_('phone number'),
        validators=[validators.RegexValidator(
            regex=r'^\+?\d+$',
            message=_('please enter a valid phone number'),
        )],
        blank=False,
    )

    # ---- University information -----

    student_number = models.CharField(
        verbose_name=_('student number'),
        max_length=8,
        validators=[validators.RegexValidator(
            regex=r'(s\d{7}|[ezu]\d{6,7})',
            message=_('enter a valid student- or e/z/u-number.'))],
        blank=True,
        null=True,
    )

    programme = models.CharField(
        max_length=20,
        choices=Profile.PROGRAMME_CHOICES,
        verbose_name=_('study programme'),
        blank=True,
        null=True,
    )

    starting_year = models.IntegerField(
        verbose_name=_('starting year'),
        blank=True,
        null=True,
    )

    # ---- Address information -----

    address_street = models.CharField(
        max_length=100,
        validators=[validators.RegexValidator(
            regex=r'^.+ \d+.*',
            message=_('include the house number'),
        )],
        verbose_name=_('street and house number'),
        blank=False,
    )

    address_street2 = models.CharField(
        max_length=100,
        verbose_name=_('second address line'),
        blank=True,
        null=True,
    )

    address_postal_code = models.CharField(
        max_length=10,
        verbose_name=_('postal code'),
        blank=False,
    )

    address_city = models.CharField(
        max_length=40,
        verbose_name=_('city'),
        blank=False,
    )

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip().encode('utf-8')

    def clean(self):
        super().clean()
        errors = {}

        if get_user_model().objects.filter(email=self.email).exists():
            errors.update({
                'email': _('A user with that email address already exists.')})

        if (self.student_number is not None and (
                Profile.objects.filter(
                    student_number=self.student_number).exists()
            or
                Registration.objects.filter(student_number=self.student_number)
                .exclude(pk=self.pk).exists())):
            errors.update({
                'student_number':
                    _('A user with that student number already exists.')})

        if self.username is not None and get_user_model().objects.filter(
                username=self.username).exists():
            errors.update({
                'username': _('A user with that username already exists.')})

        if (self.starting_year is None and
                self.membership_type is not Membership.SUPPORTER):
            errors.update({
                'username': _('This field is required.')})

        if (self.programme is None and
                self.membership_type is not Membership.SUPPORTER):
            errors.update({
                'programme': _('This field is required.')})

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        send_confirm_email = self.pk is None
        super().save(*args, **kwargs)
        if send_confirm_email:
            emails.send_registration_email_confirmation(self)

    def __str__(self):
        return '{} {} ({})'.format(self.first_name, self.last_name, self.email)

    class Meta:
        verbose_name = _('registation')
        verbose_name_plural = _('registrations')


class Renewal(Entry):
    member = models.ForeignKey(
        'members.Member',
        verbose_name=_('member'),
        blank=False,
        null=False,
    )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None:
            self.status = Entry.STATUS_REVIEW
        super().save(force_insert, force_update, using, update_fields)

    def clean(self):
        super().clean()
        errors = {}

        if Renewal.objects.filter(
                member=self.member, status=Entry.STATUS_REVIEW).exists():
            raise ValidationError(_('You already have a renewal '
                                    'request queued for review.'))

        # Invalid form for study and honorary members
        current_membership = self.member.current_membership
        if (current_membership is not None and
                current_membership.until is None):
            errors.update({
                'length': _('You currently have an active membership.'),
                'membership_type': _('You currently have'
                                     ' an active membership.'),
            })

        latest_membership = self.member.latest_membership
        hide_year_choice = not (latest_membership is not None and
                                latest_membership.until is not None and
                                (latest_membership.until -
                                 timezone.now().date()).days <= 31)

        if (self.length == Entry.MEMBERSHIP_YEAR and
                hide_year_choice):
            errors.update({
                'length': _('You cannot renew your membership at this moment.')
            })

        if (self.membership_type == Membership.SUPPORTER and
                self.length == Entry.MEMBERSHIP_STUDY):
            errors.update({
                'length': _('Supporters cannot have a membership '
                            'that lasts their entire study duration.')
            })

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return '{} {} ({})'.format(self.member.first_name,
                                   self.member.last_name,
                                   self.member.email)

    class Meta:
        verbose_name = _('renewal')
        verbose_name_plural = _('renewals')


class Payment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(_('created at'), default=timezone.now)

    CASH = 'cash_payment'
    CARD = 'card_payment'

    PAYMENT_TYPE = (
        (CASH, _('cash payment')),
        (CARD, _('card payment')),
    )

    type = models.CharField(
        choices=PAYMENT_TYPE,
        verbose_name=_('type'),
        max_length=20,
        blank=True,
        null=True,
    )

    amount = models.DecimalField(
        blank=False,
        null=False,
        decimal_places=2,
        max_digits=4,
        default=settings.MEMBERSHIP_PRICES['year']
    )

    processed = models.BooleanField(
        _('processed'),
        default=False,
    )

    processing_date = models.DateTimeField(
        _('processing date'),
        blank=True,
        null=True,
    )

    entry = models.OneToOneField(
        'registrations.Entry',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    membership = models.OneToOneField(
        'members.Membership',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.processed and not self.processing_date:
            self.processing_date = timezone.now()

        super().save(force_insert, force_update, using, update_fields)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (
            content_type.app_label, content_type.model), args=(self.id,))

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
        permissions = (
            ('process_payments', _("Process payments")),
        )