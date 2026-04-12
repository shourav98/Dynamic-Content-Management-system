from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from .models import Category, ContentItem, ExplanatoryLink, ExpandableSection, ArticleContent


def index(request):
    """Main landing page showing top-level categories."""
    root_categories = Category.objects.filter(parent=None).prefetch_related(
        'subcategories', 'contents', 'expandable_sections', 'articles', 'explanatory_links'
    )
    # Use first category as featured, or show all
    featured_category = root_categories.first()
    context = {
        'root_categories': root_categories,
        'featured_category': featured_category,
    }
    return render(request, 'cms/index.html', context)


def category_detail(request, slug):
    """Detail page for a specific category."""
    category = get_object_or_404(Category, slug=slug)
    subcategories = category.subcategories.prefetch_related(
        'contents', 'expandable_sections', 'articles', 'explanatory_links'
    )
    context = {
        'category': category,
        'subcategories': subcategories,
        'root_categories': Category.objects.filter(parent=None),
    }
    return render(request, 'cms/category_detail.html', context)


@require_GET
def content_modal(request, pk):
    """Return partial HTML for the content modal (AJAX)."""
    item = get_object_or_404(ContentItem, pk=pk)
    return render(request, 'cms/partials/content_modal.html', {'item': item})


@require_GET
def explanation_modal(request, pk):
    """Return partial HTML for an explanatory link modal (AJAX)."""
    link = get_object_or_404(ExplanatoryLink, pk=pk)
    return render(request, 'cms/partials/explanation_modal.html', {'link': link})


@require_GET
def api_content(request, pk):
    """JSON API fallback for content item."""
    item = get_object_or_404(ContentItem, pk=pk)
    data = {
        'id': item.pk,
        'title': item.title,
        'content_type': item.content_type,
        'is_premium': item.is_premium,
    }
    if item.content_type == 'text':
        data['text_content'] = item.text_content
    elif item.content_type == 'image' and item.image:
        data['image_url'] = item.image.url
    elif item.content_type == 'audio' and item.audio_file:
        data['audio_url'] = item.audio_file.url
    elif item.content_type == 'video' and item.video_file:
        data['video_url'] = item.video_file.url
    elif item.content_type == 'youtube':
        data['embed_url'] = item.get_embed_url()
    return JsonResponse(data)
