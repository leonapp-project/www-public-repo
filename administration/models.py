from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string


class FixedCharField(models.CharField):
    def db_type(self, connection):
        varchar: str = super().db_type(connection)
        char: str = varchar.replace('varchar', 'char')
        return char


class Transaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, null=False, blank=False)
    date_purchased = models.DateTimeField(auto_now_add=True)
    ticket_type = models.CharField(max_length=16)
    block_code = FixedCharField(
        max_length=16, ###############################################
        unique=True,  # REMEMBER TO CALL THIS IN TRY-EXCEPT TO HANDLE THAT
        # default=get_random_string(length=17)
    )

    class Meta:
        # managed = False
        db_table = 'acquisti'
