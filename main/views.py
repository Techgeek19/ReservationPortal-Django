from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Table, Booking
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect) 
from .forms import AvailabilityForm, BookingForm
from .booking_functions.availability import check_availability

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        # main = Note.objects.filter(user=request.user).order_by('-updated_at')[:10]
        # all_main = Note.objects.filter(user=request.user).order_by('-updated_at')
        # paginator = Paginator(all_main, 15)

        # if request.method == 'POST':
        #     form = AddNoteForm(request.POST)
        #     if form.is_valid():
        #         form_data = form.save(commit=False)
        #         form_data.user = request.user
        #         form_data.save()
        #         # Without this next line the tags won't be saved.
        #         form.save_m2m()
        #         form = AddNoteForm()
        #         messages.success(request, 'Note added successfully!')
        #         return redirect('main')
        # else:
        #     form = AddNoteForm()
        # context = {
        #     'main': main,
        #     'all_main': all_main,
        #     'add_note_form': form,
        # }
        return HttpResponseRedirect("/table_list") 
    else:
        return render(request, 'index.html')


def TableListView(request):
    table = Table.objects.all()[0]
    table_categories = dict(table.TABLE_CATEGORIES)
    table_values = table_categories.values()
    table_list = []

    for table_category in table_categories:
        table = table_categories.get(table_category)
        table_url = reverse('main:TableDetailView', kwargs={
                           'category': table_category})

        table_list.append((table, table_url))
        # print(table_list)
    context = {
        "table_list": table_list,
    }
    return render(request, 'table_list_view.html', context)


class BookingListView(ListView):
    model = Booking
    template_name = "booking_list_view.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list
    
    # def get_context_data(self, **kwargs):
    #     table = table.objects.all()[0]
    #     table_categories = dict(table.table_CATEGORIES)
    #     context = super().get_context_data(**kwargs)
    #     context


class TableDetailView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        form = AvailabilityForm()
        table_list = Table.objects.filter(category=category)

        if len(table_list) > 0:
            table = table_list[0]
            table_category = dict(table.TABLE_CATEGORIES).get(table.category, None)
            context = {
                'table_category': table_category,
                'form': form,
            }
            return render(request, 'table_detail_view.html', context)
        else:
            return HttpResponse('Category does not exist')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        table_list = Table.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_tables = []
        for table in table_list:
            if check_availability(table, data['check_in'], data['check_out']):
                available_tables.append(table)

        if len(available_tables) > 0:
            table = available_tables[0]
            booking = Booking.objects.create(
                user=self.request.user,
                table=table,
                check_in=data['check_in'],
                check_out=data['check_out']
            )
            booking.save()
            return HttpResponseRedirect('/booking_list')
        else:
            return HttpResponse('All of this category of tables are booked!! Try another one')
        

def update_view(request, id): 
    context ={} 
    obj = get_object_or_404(Booking, id = id) 
    form = BookingForm(request.POST or None, instance = obj) 
    if form.is_valid(): 
        form.save() 
        return HttpResponseRedirect("/booking_list") 
    context["form"] = form 
    return render(request, "booking_edit_view.html", context) 


class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('main:BookingListView')