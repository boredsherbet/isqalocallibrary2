from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect


def index(request):
    """View function for home page of site."""
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()
    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_visits": num_visits,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, "catalog/index.html", context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = "catalog/my_books.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


class BookCreate(CreateView):
    model = Book
    fields = ["title", "author", "summary", "isbn", "genre"]


class BookUpdate(UpdateView):
    model = Book
    fields = ["title", "author", "summary", "isbn", "genre"]


class AuthorCreate(CreateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]


class AuthorUpdate(UpdateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    try:
        book.delete()
        messages.success(
            request, (f"{book.title} by {book.author.last_name} has been deleted")
        )
    except:
        messages.success(
            request,
            ("Copies exist, cannot be deleted."),
        )
    return redirect("book_list")


def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    try:
        author.delete()
        messages.success(
            request, (author.first_name + " " + author.last_name + " has been deleted")
        )
    except:
        messages.success(
            request,
            (
                author.first_name
                + " "
                + author.last_name
                + " cannot be deleted. Books exist for this author"
            ),
        )
    return redirect("author_list")
