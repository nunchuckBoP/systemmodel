from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from pinchart.models import Pinchart

class cBaseCreateView(CreateView):
    success_url = ''
    headline = ''
    parent = ''
    parent_model = Pinchart
    template_name = 'pinchart/base_form.html'
    def get_success_url(self) -> str:
        _pk = self.kwargs.get('pk')
        if _pk is None:
            return reverse_lazy(self.success_url)
        else:
            return reverse_lazy(self.success_url, kwargs={'pk':_pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _pk = self.kwargs.get('pk')
        _parent_object = get_object_or_404(self.parent_model, pk=_pk)
        form = self.form_class(initial={self.parent:_pk})

        context['headline'] = self.headline
        context['form'] = form
        context['parent'] = self.parent.title()
        context['parent_object'] = _parent_object
        return context

class cBaseUpateView(UpdateView):
    success_url = ''
    headline = ''
    template_name = 'pinchart/base_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = self.headline
        return context