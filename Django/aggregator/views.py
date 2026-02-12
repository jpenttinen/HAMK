from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import NewsSourceForm
from .models import NewsSource
from .services import fetch_news_for_sources


def dashboard(request):
    sources = NewsSource.objects.filter(is_active=True)
    source_feeds = fetch_news_for_sources(sources)

    return render(
        request,
        'aggregator/dashboard.html',
        {
            'source_feeds': source_feeds,
            'active_sources_count': sources.count(),
            'total_sources_count': NewsSource.objects.count(),
        },
    )


def source_list(request):
    if request.method == 'POST':
        form = NewsSourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'News source added.')
            return redirect('aggregator:source_list')
    else:
        form = NewsSourceForm()

    return render(
        request,
        'aggregator/source_list.html',
        {
            'form': form,
            'sources': NewsSource.objects.all(),
        },
    )


def source_edit(request, pk: int):
    source = get_object_or_404(NewsSource, pk=pk)

    if request.method == 'POST':
        form = NewsSourceForm(request.POST, instance=source)
        if form.is_valid():
            form.save()
            messages.success(request, 'News source updated.')
            return redirect('aggregator:source_list')
    else:
        form = NewsSourceForm(instance=source)

    return render(
        request,
        'aggregator/source_form.html',
        {
            'form': form,
            'source': source,
        },
    )


@require_POST
def source_delete(request, pk: int):
    source = get_object_or_404(NewsSource, pk=pk)
    source.delete()
    messages.success(request, f'News source "{source.name}" deleted.')
    return redirect('aggregator:source_list')
