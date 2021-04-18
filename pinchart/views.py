from typing import List
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
import pinchart.models as models

# Create your views here.
class PinchartListView(ListView):
    model = models.Pinchart

class PinchartCreateView(CreateView):
    model = models.Pinchart
    fields = [
        'name',
        'description',
        'controller_ipaddress',
        'controller_slot',
        'array_length',
    ]
    banner_text = "Create Pinchart"

class PinchartUpdateView(UpdateView):
    model = models.Pinchart
    success_url = reverse_lazy('pinchart-list')
    fields = [
        'name',
        'description',
        'controller_ipaddress',
        'controller_slot',
        'array_length',
    ]
    banner_text = "Edit Pinchart"

class PinchartDeleteView(DeleteView):
    model = models.Pinchart
    success_url = reverse_lazy('pinchart-list')

class WordListView(ListView):
    model = models.Word
    
class WordListFilteredView(ListView):
    """
        Word List - Filtered by pinchart
    """
    model = models.Word
    template_name = "pinchart/word_list_filtered.html"

    def get_context_data(self, **kwargs):

        # calls the super routine
        context = super(WordListFilteredView, self).get_context_data(**kwargs)

        # gets the primary key
        pk = int(self.kwargs.get('pk'))

        # gets the pinchart
        pinchart = get_object_or_404(models.Pinchart, pk=pk)

        # gets the object list
        object_list = models.Word.objects.filter(pinchart=pinchart)

        context['pinchart'] = pinchart
        context['object_list'] = object_list
        return context


class WordUpdateView(UpdateView):
    model = models.Word
    success_url = reverse_lazy('word-list')

class WordDeleteView(DeleteView):
    model = models.Word
    success_url = reverse_lazy('word-list')

class BitDescriptionListView(ListView):
    model = models.BitDescription

class BitDescriptionUpdateView(UpdateView):
    model = models.BitDescription
    fields = [
        'word',
        'bit',
        'device',
        'description'
    ]

class SequenceListView(ListView):
    models = models.Sequence

class SequenceUpdateView(UpdateView):
    models = models.Sequence
    success_url = reverse_lazy('sequence-list')

class SequenceDeleteView(DeleteView):
    models = models.Sequence
    success_url = reverse_lazy('sequence-list')

class StepListView(ListView):
    model = models.Step

class StepUpdateView(UpdateView):
    model = models.Step
    success_url = reverse_lazy('step-list')

class StepDeleteView(DeleteView):
    model = models.Step
    success_url = reverse_lazy('step-list')

class StepDataListView(ListView):
    model = models.StepData
    
class StepDataUpdateView(UpdateView):
    model = models.StepData
    success_url = reverse_lazy('stepdata-list')

class StepDataDeleteView(DeleteView):
    models = models.StepData
    success_url = reverse_lazy('stepdata-list')