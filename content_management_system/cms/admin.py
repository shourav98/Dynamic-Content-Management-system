from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Category, ContentItem, ExplanatoryLink, ExpandableSection, ArticleContent


class ContentItemInline(admin.StackedInline):
    model = ContentItem
    extra = 1
    fields = [
        'content_type', 'title', 'order', 'is_premium',
        'text_content', 'image', 'audio_file', 'video_file', 'youtube_url'
    ]


class ExplanatoryLinkInline(admin.StackedInline):
    model = ExplanatoryLink
    extra = 1
    fk_name = 'category'
    fields = ['trigger_text', 'explanation_title', 'explanation_text', 'explanation_image', 'is_premium']


class ExpandableSectionInline(admin.StackedInline):
    model = ExpandableSection
    extra = 1
    fields = ['title', 'body', 'order', 'is_open_by_default']


class ArticleContentInline(admin.StackedInline):
    model = ArticleContent
    extra = 1
    fields = ['title', 'body', 'order', 'is_premium']


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'slug', 'is_premium', 'order')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_premium',)
    search_fields = ('name',)
    inlines = [
        ContentItemInline,
        ExplanatoryLinkInline,
        ExpandableSectionInline,
        ArticleContentInline,
    ]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'parent', 'description', 'order')
        }),
        ('Settings', {
            'fields': ('is_premium',)
        }),
    )


@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'category', 'is_premium', 'order', 'created_at')
    list_filter = ('content_type', 'is_premium', 'category')
    search_fields = ('title',)
    ordering = ('category', 'order')

    fieldsets = (
        ('Basic Info', {
            'fields': ('category', 'content_type', 'title', 'order', 'is_premium')
        }),
        ('Text Content (Rich Editor)', {
            'fields': ('text_content',),
            'classes': ('collapse',),
        }),
        ('Media Files', {
            'fields': ('image', 'audio_file', 'video_file', 'youtube_url'),
            'classes': ('collapse',),
        }),
    )


@admin.register(ExplanatoryLink)
class ExplanatoryLinkAdmin(admin.ModelAdmin):
    list_display = ('trigger_text', 'category', 'content_item', 'is_premium')
    list_filter = ('is_premium',)
    search_fields = ('trigger_text', 'explanation_title')


@admin.register(ExpandableSection)
class ExpandableSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'is_open_by_default')
    list_filter = ('category',)
    ordering = ('category', 'order')


@admin.register(ArticleContent)
class ArticleContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'is_premium', 'created_at')
    list_filter = ('is_premium', 'category')
    search_fields = ('title',)
