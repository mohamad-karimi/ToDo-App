from django.views.generic import ListView, CreateView, UpdateView, View
from .models import Tasks
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from .forms import TodoForm


# Create your views here.
class IndexView(LoginRequiredMixin, ListView):
    """
    Displays a list of todo tasks belonging to the current user.

    Only authenticated users can access this view.
    """

    template_name = "todo/index.html"
    context_object_name = "tasks"

    def get_queryset(self):
        """
        Returns only the todo items created by the logged-in user.
        """

        return Tasks.objects.filter(user=self.request.user)


class TodoCreateView(LoginRequiredMixin, CreateView):
    """
    Handles creating a new todo task.

    The newly created todo item is automatically assigned
    to the currently authenticated user.
    """

    model = Tasks
    form_class = TodoForm
    success_url = reverse_lazy("todo:index")

    def form_valid(self, form):
        """
        Assigns the current user before saving the todo object.
        """

        form.instance.user = self.request.user
        return super().form_valid(form)


class TodoEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Handles updating an existing todo task.

    Users can only edit their own todo items.
    """

    model = Tasks
    form_class = TodoForm
    template_name = "todo/update.html"
    success_url = reverse_lazy("todo:index")

    def test_func(self):
        """
        Shoe the 403 to user ask a task that wasnt for it
        """
        todo = self.get_object()
        return todo.user == self.request.user


class TodoComplete(LoginRequiredMixin, View):
    """
    Marks a todo task as completed.

    This view updates the completion status of a selected todo item.
    """

    model = Tasks
    success_url = reverse_lazy("todo:index")

    def get(self, request, *args, **kwargs):
        """
        Finds the requested todo item and marks it as completed.
        """

        object = Tasks.objects.get(id=kwargs.get("pk"))
        object.completed = True
        object.save()
        return redirect(self.success_url)


class TodoNotComplete(LoginRequiredMixin, View):
    """
    Marks a todo task as NOt completed.

    This view updates the completion status of a selected todo item.
    """

    model = Tasks
    success_url = reverse_lazy("todo:index")

    def get(self, request, *args, **kwargs):
        """
        Finds the requested todo item and marks it as not completed.
        """

        object = Tasks.objects.get(id=kwargs.get("pk"))
        object.completed = False
        object.save()
        return redirect(self.success_url)


class TodoDeleteView(LoginRequiredMixin, View):
    """
    Deletes a todo task owned by the current user.

    The deletion is handled through a POST request to prevent
    accidental removals.
    """

    def post(self, request, *args, **kwargs):
        """
        Deletes the selected todo item and redirects back to the index page.
        """

        todo = get_object_or_404(
            Tasks, pk=kwargs.get("pk"), user=request.user
        )

        todo.delete()

        return redirect(reverse_lazy("todo:index"))
