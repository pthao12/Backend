import os
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import azure.cognitiveservices.speech as speechsdk

def record_audio(request):
    return render(request, 'audio_app/record.html')

@csrf_exempt
def upload_audio(request):
    if request.method == 'GET':
        # Return keys
        return JsonResponse({'key': settings.AZURE_SPEECH_KEY, 'region': settings.AZURE_SERVICE_REGION})
    if request.method == 'POST' and request.FILES['audioFile']:
        audio_file = request.FILES['audioFile']
        file_path = default_storage.save('uploads/' + audio_file.name, audio_file)
        absolute_file_path = os.path.join(settings.MEDIA_ROOT, file_path)

        # Set up Azure Speech SDK
        speech_key = settings.AZURE_SPEECH_KEY
        service_region = settings.AZURE_SERVICE_REGION

        # Log the key and region
        print(f"Key: {speech_key}")
        print(f"Region: {service_region}")

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        audio_input = speechsdk.AudioConfig(filename=absolute_file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

        # Perform speech recognition
        result = speech_recognizer.recognize_once()
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            text = result.text
        else:
            text = "Error recognizing speech"

        return JsonResponse({'transcription': text})

    return JsonResponse({'error': 'Invalid request'}, status=400)
