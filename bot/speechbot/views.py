from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import openai
import speech_recognition as sr
import pyttsx3
from django.http import JsonResponse

openai.api_key = " "  # Replace with your OpenAI API key

# Initializing Text-to-Speech engine
engine = pyttsx3.init()

def get_llm_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error communicating with OpenAI: {e}"

def recognize_speech(request):
    if request.method == "POST":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        
        try:
            text = r.recognize_google(audio)
            response_text = get_llm_response(text)
            engine.say(response_text)
            engine.runAndWait()
            return JsonResponse({'text': text, 'response': response_text})
        except sr.UnknownValueError:
            return JsonResponse({'error': "Could not understand the audio"}, status=400)
        except sr.RequestError as e:
            return JsonResponse({'error': f"Request error: {e}"}, status=500)
    return JsonResponse({'error': "Invalid request method"}, status=405)

@csrf_exempt
def recognize_audio(request):
    if request.method == 'POST':
        return recognize_speech(request)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def index(request):
    return render(request, 'index.html')
