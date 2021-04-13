from typing import List
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
import pinchart.models as models

# Create your views here.
class PinchartListView(ListView):
    model = models.Pinchart

class PinchartUpdateView(UpdateView):
    model = models.Pinchart
    success_url = reverse_lazy('pinchart-list')

class PinchartDeleteView(DeleteView):
    model = models.Pinchart
    success_url = reverse_lazy('pinchart-list')

class WordListView(ListView):
    model = models.Word

class WordUpdateView(UpdateView):
    model = models.Word
    success_url = reverse_lazy('word-list')

class WordDeleteView(DeleteView):
    model = models.Word
    success_url = reverse_lazy('word-list')

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