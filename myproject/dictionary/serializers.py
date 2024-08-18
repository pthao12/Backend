from rest_framework import serializers
from .models import KanjiMeaning, WordMeaning, MaziiWordExampleReturnType

class KanjiSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanjiMeaning
        fields = '__all__'

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordMeaning
        fields = '__all__'

class MaziiWordExampleReturnTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaziiWordExampleReturnType
        fields = '__all__'