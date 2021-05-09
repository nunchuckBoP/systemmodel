from typing import ContextManager, List, Sequence
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import ListView, UpdateView, DeleteView, RedirectView
from django.views.generic.edit import CreateView
import pinchart.models as models
import pinchart.forms as forms
from core.views import cBaseCreateView, cBaseUpateView


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
    ]
    banner_text = "Edit Pinchart"

class PinchartDeleteView(DeleteView):
    model = models.Pinchart
    success_url = reverse_lazy('pinchart-list')
    
class WordListView(ListView):
    """
        Word List - Filtered by pinchart
    """
    model = models.Word
    template_name = "pinchart/word_list.html"

    def get_parent(self):
        parent_pinchart = get_object_or_404(models.Pinchart, pk=self.kwargs.get('pk'))
        return parent_pinchart

    def get_queryset(self):
        return models.Word.objects.filter(pinchart=self.get_parent()).order_by('group')

    def get_context_data(self, **kwargs):
        context = super(WordListView, self).get_context_data(**kwargs)
        context['parent_object'] = self.get_parent()
        return context

class WordCreateView(CreateView):
    model = models.Word
    form_class = forms.WordForm
    success_url = 'word-list'
    template_name = 'pinchart/word_form.html'

    def get_success_url(self):
       return reverse_lazy(self.success_url, kwargs={'pk':self.get_parent_object().pk})

    def get_parent_object(self):
        parent_pk = self.kwargs.get('pk')
        parent = get_object_or_404(models.Pinchart, pk=parent_pk)
        return parent

    def get_initial(self):
        initial = super(WordCreateView, self).get_initial()
        parent = self.get_parent_object()
        initial.update({'pinchart':parent})
        return initial

    def get_context_data(self, **kwargs):
        context = super(WordCreateView, self).get_context_data(**kwargs)
        context['headline'] = "Create Pinchart Data Word"
        context['parent'] = 'Pinchart'
        context['parent_object'] = self.get_parent_object()
        return context

class WordUpdateView(UpdateView):
    model = models.Word
    success_url = 'word-list'
    template_name = 'pinchart/word_form.html'
    form_class = forms.WordForm

    def get_context_data(self, **kwargs):
        context = super(WordUpdateView, self).get_context_data(**kwargs)
        context['headline'] = 'Edit Pinchart Data Word'
        context['parent'] = 'Pinchart'
        context['parent_object'] = context['object'].pinchart
        return context

    def get_success_url(self):
        _pk = self.kwargs.get('pk')
        object = get_object_or_404(models.Word, pk=_pk)
        return reverse_lazy('word-list', kwargs={'pk':object.pinchart.pk})

class WordDeleteView(DeleteView):
    model = models.Word
    success_url = reverse_lazy('word-list')

    def get_success_url(self):
        object = get_object_or_404(models.Word, pk=self.kwargs.get('pk'))
        pinchart = object.pinchart
        return reverse_lazy('word-list', kwargs={'pk':pinchart.pk})

class BitDescriptionListView(ListView):
    model = models.BitDescription

    def get_parent(self):
        parent = get_object_or_404(models.Word, pk=self.kwargs.get('pk'))
        return parent

    def get_queryset(self):
        return models.BitDescription.objects.filter(word=self.get_parent()).order_by('bit')

    def get_context_data(self, **kwargs):
        context = super(BitDescriptionListView, self).get_context_data(**kwargs)
        context['parent_object'] = self.get_parent()
        return context
        
class BitDescriptionUpdateView(UpdateView):
    model = models.BitDescription
    template_name = "pinchart/bitdescription_form.html"
    sucess_url = "bitdescription-list"
    form_class = forms.BitDescriptionForm

    def get_success_url(self):
        object = get_object_or_404(models.BitDescription, pk=self.kwargs.get('pk'))
        return reverse_lazy(self.success_url, kwargs={'pk':object.word.pk})

    def get_context_data(self, **kwargs):
        context = super(BitDescriptionUpdateView, self).get_context_data(**kwargs)
        context['headline'] = 'Edit Pinchart Bit Description for Word'
        context['parent'] = 'Word'
        context['parent_object'] = context['object'].word
        return context

class BitDescriptionCreateView(CreateView):
    model = models.BitDescription
    template_name = 'pinchart/bitdescription_form.html'
    success_url = 'bitdescription-list'
    form_class = forms.BitDescriptionForm

    def get_success_url(self):
        return reverse_lazy(self.success_url, kwargs={'pk':self.get_parent_object().pk})

    def get_parent_object(self):
        parent_pk = self.kwargs.get('pk')
        parent = get_object_or_404(models.Word, pk=parent_pk)
        return parent

    def get_initial(self):
        initial = super(BitDescriptionCreateView, self).get_initial()
        parent = self.get_parent_object()
        initial.update({'word':parent})
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = "Create Bit Description for Word"
        context['parent'] = 'Word'
        context['parent_object'] = self.get_parent_object()
        return context

class SequenceListView(ListView):
    model = models.Sequence

    def get_context_data(self, **kwargs):
        context = super(SequenceListView, self).get_context_data(**kwargs)
        pinchart = get_object_or_404(models.Pinchart, pk=self.kwargs.get('pk'))
        context['parent_object'] = pinchart
        return context

    def get_queryset(self):
        pinchart_pk = self.kwargs.get('pk')
        pinchart = get_object_or_404(models.Pinchart, pk=pinchart_pk)
        return models.Sequence.objects.filter(pinchart=pinchart).order_by('name')

class SequenceUpdateView(UpdateView):
    model = models.Sequence
    success_url = reverse_lazy('sequence-list')
    form_class = forms.SequenceForm
    
    def get_context_data(self, **kwargs):
        context = super(SequenceUpdateView, self).get_context_data(**kwargs)
        context['parent'] = 'Pinchart'
        context['parent_object'] = context['object'].pinchart
        return context

    def get_success_url(self):
        _pk = self.kwargs.get('pk')
        object = get_object_or_404(models.Sequence, pk=_pk)
        return reverse_lazy('sequence-list', kwargs={'pk':object.pinchart.pk})

class SequenceDeleteView(DeleteView):
    model = models.Sequence
    success_url = reverse_lazy('sequence-list')

class StepListView(ListView):
    model = models.Step
    
    def get_context_data(self, **kwargs):
        
        # gets the sequence from the primary key
        sequence = get_object_or_404(models.Sequence, pk=self.kwargs.get('pk'))

        # gets the steps for the sequence
        steps = models.Step.objects.filter(sequence=sequence).order_by('number')

        context = {
            'object_list':steps,
            'parent_object':sequence,
        }

        return context
        
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