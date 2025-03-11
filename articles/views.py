# articles/views.py
# views.py
from rest_framework import viewsets
from .models import Article, Paragraph
from .serializers import ArticleSerializer, ParagraphSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'  # 🔥 Now Django will look up articles by slug

class ParagraphViewSet(viewsets.ModelViewSet):
    queryset = Paragraph.objects.all()
    serializer_class = ParagraphSerializer

