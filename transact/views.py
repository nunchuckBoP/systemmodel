from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
import transact.models as models
from django.urls import reverse_lazy

# Create your views here.
class TransactionListView(ListView):
    model = models.Transaction

class TransactionUpdateView(UpdateView):
    model = models.Transaction
    success_url = reverse_lazy('transaction-list')

class TransactionDeleteView(DeleteView):
    model = models.Transaction
    success_url = reverse_lazy('transaction-list')
