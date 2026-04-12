from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    description = models.TextField(blank=True)
    is_premium = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class ContentItem(models.Model):
    CONTENT_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('youtube', 'YouTube'),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='contents'
    )
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    title = models.CharField(max_length=255)
    text_content = RichTextUploadingField(blank=True, null=True, config_name='default')
    image = models.ImageField(upload_to='content/images/', blank=True, null=True)
    audio_file = models.FileField(upload_to='content/audio/', blank=True, null=True)
    video_file = models.FileField(upload_to='content/videos/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True, help_text='Full YouTube URL e.g. https://www.youtube.com/watch?v=...')
    is_premium = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Content Item'
        verbose_name_plural = 'Content Items'

    def __str__(self):
        return f"{self.get_content_type_display()} — {self.title}"

    def get_embed_url(self):
        """Convert YouTube watch URL to embed URL."""
        if self.youtube_url:
            url = self.youtube_url
            if 'watch?v=' in url:
                video_id = url.split('watch?v=')[1].split('&')[0]
                return f'https://www.youtube.com/embed/{video_id}'
            elif 'youtu.be/' in url:
                video_id = url.split('youtu.be/')[1].split('?')[0]
                return f'https://www.youtube.com/embed/{video_id}'
        return self.youtube_url


class ExplanatoryLink(models.Model):
    content_item = models.ForeignKey(
        ContentItem,
        on_delete=models.CASCADE,
        related_name='explanatory_links',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='explanatory_links',
        null=True,
        blank=True
    )
    trigger_text = models.CharField(max_length=255, help_text='The clickable word/phrase shown in text')
    explanation_title = models.CharField(max_length=255, blank=True)
    explanation_text = RichTextUploadingField(config_name='default')
    explanation_image = models.ImageField(upload_to='explanations/', blank=True, null=True)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return f"Explanation: {self.trigger_text}"


class ExpandableSection(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='expandable_sections'
    )
    title = models.CharField(max_length=255)
    body = RichTextUploadingField(config_name='default')
    order = models.PositiveIntegerField(default=0)
    is_open_by_default = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.category.name} — {self.title}"


class ArticleContent(models.Model):
    """Stores rich article/news content with embedded interactive elements."""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    title = models.CharField(max_length=255)
    body = RichTextUploadingField(config_name='default')
    order = models.PositiveIntegerField(default=0)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title
