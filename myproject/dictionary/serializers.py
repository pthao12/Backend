from rest_framework import serializers
from .models import KanjiMeaning, WordMeaning, Example, Comment

class KanjiSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanjiMeaning
        fields = '__all__'

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordMeaning
        fields = '__all__'

class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'