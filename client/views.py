from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.views.generic import TemplateView
from .forms import ClientForm, VisitCreateForm
from .models import Client, Visit


class ClientListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Client
    template_name = 'client/client_list.html'

    def queryset(self):
        return Client.objects.filter(author=self.request.user).order_by('-pk')


class ClientDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Client
    template_name = 'client/client_detail.html'


class ClientCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:create_done')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(ClientCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        client_name_list = []
        context = super().get_context_data(**kwargs)
        client_data = Client.objects.filter(author=self.request.user)
        for client in client_data:
            client_name_list.append(client.client_name)
        context["client_name_list"] = client_name_list
        return context

@login_required
def create_done(request):
    return render(request, 'client/create_done.html')


@login_required
def create_visit(request, pk):
    if request.method == 'POST':
        form = VisitCreateForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.client = get_object_or_404(Client, pk=pk)
            visit.save()
            return redirect('client:client_detail', pk=pk)
    else:
        form = VisitCreateForm()
    context = {
        'form': form,
    }
    return render(request, 'client/client_visit_form.html', context)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:update_done')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(ClientUpdateView, self).form_valid(form)

@login_required
def update_done(request):
    return render(request, 'client/update_done.html')


@login_required
def update_visit(request, pk):
    visit = get_object_or_404(Visit, id=pk)
    if request.method == 'POST':
        form = VisitCreateForm(request.POST)
        if form.is_valid():
            visit.visit_date = form.cleaned_data['visit_date']
            visit.menu = form.cleaned_data['menu']
            visit.save()
            return redirect('client:client_detail', pk=visit.client.id)
    else:
        form = VisitCreateForm({
            'visit_date': visit.visit_date,
            'menu': visit.menu,
        })
    context = {
        'form': form,
    }
    return render(request, 'client/client_visit_form.html', context)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Client
    success_url = reverse_lazy('client:delete_done')

@login_required
def delete_done(request):
    return render(request, 'client/delete_done.html')


@login_required
def delete_visit(request, pk):
    visit = get_object_or_404(Visit, id=pk)
    if request.method == 'POST':
        visit.delete()
        return redirect('client:client_detail', pk=visit.client.id)
    else:
        context = {
            'visit': visit,
        }
        return render(request, 'client/client_visit_confirm_delete.html', context)