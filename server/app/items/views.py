from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Item


class ItemCreateView(CreateView):
    pass


class ItemListView(ListView):
    pass


class ItemDetailView(DetailView):
    pass


class ItemUpdateView(UpdateView):
    pass


class ItemDeleteView(DeleteView):
    pass
