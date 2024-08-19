from rest_framework import serializers
from .models import KanjiMeaning, WordMeaning

class KanjiSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanjiMeaning
        fields = '__all__'

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordMeaning
        fields = '__all__'