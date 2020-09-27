from django.shortcuts import render, get_object_or_404
from .models import Movie


def home(request):
    all_rows = Movie.objects.all()
    movies = [
        all_rows.filter(title=item["title"]).last()
        for item in Movie.objects.values("title")
        .distinct()
        .order_by("rating")
        .reverse()
    ]
    return render(request, "movies/home.html", {"movies": movies})


def detail(request, movie_pk):
    detail = get_object_or_404(Movie, pk=movie_pk)
    return render(request, "movies/detail.html", {"detail": detail})

