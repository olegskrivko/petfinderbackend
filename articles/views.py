# articles/views.py
# views.py
from rest_framework import viewsets
from .models import Article, Paragraph
from .serializers import ArticleSerializer, ParagraphSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'  # 🔥 Now Django will look up articles by slug

class ParagraphViewSet(viewsets.ModelViewSet):
    queryset = Paragraph.objects.all()
    serializer_class = ParagraphSerializer
