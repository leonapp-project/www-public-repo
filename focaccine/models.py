from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from scan.models import Scanner
from core.models import User
from administration.models import Transaction

class FixedCharField(models.CharField):
    def db_type(self, connection):
        varchar: str = super().db_type(connection)
        char: str = varchar.replace('varchar', 'char')
        return char


# class User(AbstractUser):
#     CLASS_SECTION_CHOICES = [
#         ("sca", "Scientifico A"),
#         ("scb", "Scientifico B"),
#         ("scc", "Scientifico C"),
#         ("cla", "Classico"),
#         ("spo", "Sportivo")
#     ]

#     CLASS_NUMBER_CHOICES = [
#         ("1", "Prima"),
#         ("2", "Seconda"),
#         ("3", "Terza"),
#         ("4", "Quarta"),
#         ("5", "Quinta")
#     ]

#     class_number = FixedCharField(
#         max_length=1,
#         choices=CLASS_NUMBER_CHOICES,
#         blank=True,
#         default=""
#     )

#     class_section = FixedCharField(
#         max_length=3,
#         choices=CLASS_SECTION_CHOICES,
#         blank=True,
#         default=""
#     )

#     # define the custom permissions
#     # related to User.
#     class Meta:
#         permissions = (
#             ("can_buy_tickets", "Has the authorization to buy focaccine"),
#         )


class Ticket(models.Model):
    # An Open ticket is defined as a ticket assigned to a redeemer.
    # A Pending ticket is not yet solved but is waiting on information from the requester before working on it further.
    # An On-hold ticket is waiting for information or action from someone other than the requester.
    # A Used ticket is a ticket that has been solved.
    STATUS_CHOICES = [
        ("OPEN", "Unused"),
        ("PEND", "Pending"),
        ("HOLD", "On-hold"),
        ("USED", "Used")
    ]

    TYPE_CHOICES = [
        ("FOCACCINA", "Focaccina"),
        ("PRANZO", "Pranzo"),
        ("CENA", "Cena"),
        ("ALTRO", "Altro")
    ]

    # The ticket's unique code
    ticket_code = FixedCharField(
        max_length=16, #####################
        unique=True,  # REMEMBER TO CALL THIS IN TRY-EXCEPT TO HANDLE THAT
        # default=get_random_string(length=17)
    )

    # The date the ticket has been created
    date_created = models.DateTimeField(auto_now_add=True)

    # The status of the ticket
    status = FixedCharField(
        max_length=4,
        choices=STATUS_CHOICES,
        default="OPEN"
    )

    # The date the ticket has been used
    date_used = models.DateTimeField(default=None, null=True)

    type = models.CharField(
        max_length=16,
        choices=TYPE_CHOICES,
        default="FOCACCINA"
    )

    # The user of the ticket
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)

    block_code = models.ForeignKey(Transaction, on_delete=models.PROTECT, null=False, blank=False, to_field="block_code")
    # transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, null=False, blank=False)

    # The scanner who scanned the ticket
    scanner = models.ForeignKey(Scanner, on_delete=models.PROTECT, null=True, blank=False)

    def save(self, *args, **kwargs):
        if not self.ticket_code:
            self.ticket_code = get_random_string(16)  ##################
        super().save(*args, **kwargs)

    class Meta:
        db_table = "tickets"
