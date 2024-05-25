# from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
# from django.shortcuts import redirect
# from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Case, When, Value, IntegerField
from django.utils.crypto import get_random_string
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin  # , UserPassesTestMixin
from .models import Ticket
from administration.models import Transaction
from core.models import User


# from django.db.models import Count
# from core.models import User


# class FocaccineIndexView(LoginRequiredMixin, TemplateView):
#     template_name = 'focaccine/index.html'


class FocaccineIndexView(LoginRequiredMixin, CreateView):  # keep, add LoginRequiredMixin
    model = Ticket
    fields = []  # no fields needed since values are predetermined
    template_name = 'focaccine/index.html'
    success_url = '/focaccine/'

    def form_valid(self, form):
        # # Create a list of 10 Ticket objects with the user set to the current user
        # tickets = [
        #     Ticket(
        #         user=self.request.user,
        #         ticket_code=get_random_string(17),
        #     ) for _ in range(10)
        # ]
        # # Create all the tickets in a single query
        # Ticket.objects.bulk_create(tickets)

        # ADD THE TRANSACTION TO DATABASE TABLE TO BE CREATED

        with transaction.atomic():
            # Create a Transaction with the same block_code for the created tickets
            new_transaction = Transaction.objects.create(
                user=self.request.user,
                ticket_type="FOCACCINA",
                block_code=get_random_string(16),
            )

            tickets = [
                Ticket(
                    user=self.request.user,
                    ticket_code=get_random_string(16),
                    block_code=new_transaction,
                ) for _ in range(10)
            ]

            Ticket.objects.bulk_create(tickets)

        # Redirect the user
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        number_of_tickets = self.request.user.ticket_set.filter(status="OPEN").count()

        context['number_of_tickets'] = number_of_tickets

        if number_of_tickets:
            context['ticket_code'] = Ticket.objects.filter(user=self.request.user, status="OPEN")[0].ticket_code

        return context


class FocaccineTicketQRCodeView(LoginRequiredMixin, TemplateView):  # keep, add LoginRequiredMixin
    template_name = 'focaccine/ticket_qrcode.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the first ticket of the current user
        try:
            context['ticket_code'] = Ticket.objects.filter(user=self.request.user, status="OPEN")[0].ticket_code
        except IndexError:
            raise Http404()

        return context


class TicketHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'focaccine/ticket_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['unused_tickets'] = Ticket.objects.filter(user=user, status='OPEN')
        context['used_tickets'] = Ticket.objects.filter(user=user, status='USED')
        context['pending_tickets'] = Ticket.objects.exclude(status__in=['OPEN', 'USED'])
        context['tab_names'] = {
            'unused': "Disponibili",
            'used': "Utilizzati",
            'pending': "In attesa"
        }
        return context


# class TicketList(ListView):
#     model = Ticket
#     # template_name = 'ticket_list.html'
#     context_object_name = 'tickets'  # This is the context name that the template will use, default would have been object_list

#     # def get_queryset(self):
#     #     return Ticket.objects.filter(user=self.request.user)
#     def get_queryset(self):
#         # We create a custom order, setting 'OPEN' status as the highest priority
#         ordering = Case(
#             When(status='USED', then=Value(1)),
#             When(status='OPEN', then=Value(0)),
#             default=Value(2),
#             output_field=IntegerField()
#         )
#         # Now we filter the user's tickets and order by the custom ordering and then by date
#         return Ticket.objects.filter(user=self.request.user).annotate(custom_order=ordering).order_by('custom_order', 'date_created')


# FOLLOWING VIEWS ARE TO BE REMOVED

class TicketBuy(CreateView):  # LOGIN REQUIRED # not needed?
    model = Ticket
    fields = []  # no fields needed since values are predetermined
    template_name_suffix = '_buy'
    success_url = '/focaccine/'

    # def get_initial(self):
    #     return {
    #         'user': self.request.user
    #     }

    def form_valid(self, form):
        # for i in range(10):
        #     ticket = self.model(**form.cleaned_data)
        #     ticket.pk = None
        #     ticket.save()

        # Create a list of 10 Ticket objects with the user set to the current user
        # tickets = [
        #     Ticket(
        #         user=self.request.user,
        #         ticket_code=get_random_string(17),
        #     ) for _ in range(10)
        # ]
        # Create all the tickets in a single query
        # Ticket.objects.bulk_create(tickets)

        # ADD THE TRANSACTION TO DATABASE TABLE TO BE CREATED
        # Use a transaction to ensure atomicity of ticket and transaction creation
        # with transaction.atomic():
        # Create all the tickets in a single query
        # Ticket.objects.bulk_create(tickets)

        # Create a Transaction with the same block_code for the created tickets
        new_transaction = Transaction.objects.create(
            user=self.request.user,
            ticket_type="FOCACCINA",  # Set the appropriate ticket type
            # block_code=get_random_string(17),  # Generate the block code for the Transaction
        )

        for _ in range(10):  ##################################
            Ticket.objects.create(user=self.request.user, ticket_code=get_random_string(16),
                                  transaction=new_transaction)

        # tickets = [
        #     Ticket(
        #         user=self.request.user,
        #         ticket_code=get_random_string(17),
        #         transaction=new_transaction,
        #     ) for _ in range(10)
        # ]
        #
        # Ticket.objects.bulk_create(tickets)

        # Update the block_code for the created tickets to match the Transaction's block_code
        # Ticket.objects.filter(block_code=transaction.block_code).update(block_code=transaction.block_code)

        # Redirect the user
        return HttpResponseRedirect(self.success_url)


class TicketDetailView(DetailView):  # not needed?
    model = Ticket

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

# def custom_404(request, exception):
#    return render(request, '404.html', {'exception': exception}, status=404)
