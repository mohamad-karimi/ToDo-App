from django.views.generic import ListView, CreateView, UpdateView, View
from .models import Todo
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from .forms import TodoForm

# Create your views here.
class IndexView(LoginRequiredMixin, ListView):
    '''
    This class for show the list of the todo
    '''
    template_name = "todo/index.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Todo.objects.all()

class TodoCreateView(LoginRequiredMixin, CreateView):
    """
    This claad for create a new todo with form
    """
    model = Todo
    form_class = TodoForm
    success_url = reverse_lazy("todo:index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class TodoEditView(LoginRequiredMixin, UpdateView):
    '''
    This class use for edit the todo
    '''
    model = Todo
    form_class = TodoForm
    template_name = "todo/update.html"
    success_url = reverse_lazy("todo:index")

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

class TodoComplete(LoginRequiredMixin, View):
    '''
    This class usr for complete the todo
    '''
    model = Todo
    success_url = reverse_lazy("todo:index")

    def get(self, request, *args, **kwargs):
        object = Todo.objects.get(id=kwargs.get("pk"))
        object.completed = True
        object.save()
        return redirect(self.success_url)
    
class TodoDeleteView(LoginRequiredMixin, View):
    '''
    This class for delete the todo
    '''
    def post(self, request, *args, **kwargs):
        todo = get_object_or_404(
            Todo,
            pk=kwargs.get("pk"),
            user=request.user
        )

        todo.delete()

        return redirect(reverse_lazy("todo:index"))