from rest_framework import serializers
from .models import KanjiMeaning, WordMeaning, WordExample, Comment, Reading

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
        model = WordExample
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = '__all__'