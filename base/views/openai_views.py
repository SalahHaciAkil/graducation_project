from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from dotenv import load_dotenv
import openai
from pytube import YouTube
import re
import requests
import json
import time
load_dotenv()


@api_view(['GET'])
def analyzeUserEmotions(request):
    try:
        emotions = request.query_params.get('emotions')
        prompt = request.query_params.get('prompt')
        open_ai_key = request.headers.get('x-openai-api-key')

        def gpt_classify_sentiment(prompt, emotions):
            openai.api_key = open_ai_key
            system_promote = f'''You are an emotionally intelligent assistant.
            Classify the sentiment of the user's text with ONLY ONE OF THE FOLLOWING EMOTIONS: {emotions}.
            After classifying the text, response with the emotions ONLY. '''

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": 'system', "content": system_promote},
                          {"role": "user", "content": prompt}],
                max_tokens=20,
                temperature=0,

            )

            r = response['choices'][0].message.content
            if r == '':
                return 'N/A'
            return r

        result = gpt_classify_sentiment(prompt=prompt, emotions=emotions)
        return Response(result)
    except Exception as error:
        print(error)
        # set the response status code to 500
        return Response({
            'error': 'Something wrong happen, plz make sure your open ai key is valid'
        }, status=400)


@api_view(['GET'])
def summarizeYoutubeVideo(request):
    link = request.query_params.get('url')
    open_ai_key = request.headers.get('x-openai-api-key')
    openai.api_key = open_ai_key
    try:
        openai.Engine.retrieve('davinci')
    except Exception as error:
        print(error)
        return Response({
            'error': 'Something wrong happen, plz make sure your open ai key is valid'
        }, status=400)

    def youtube_audio_downloader(link):
        if "youtube.com" not in link:
            print("Please enter a valid YouTube URL")
            return False

        yt = YouTube(link)
        if yt == None:
            print("Please enter a valid YouTube URL")
            return False
        print(f'Title of the video: {yt.title}')
        print(f'Length of the video: {yt.length} seconds')

        audio_stream = yt.streams.filter(only_audio=True).first()
        download_result = audio_stream.download()

        if (os.path.exists(download_result)):
            print("File downloaded successfully")
        else:
            print("Some error occurred")
            return False

        basename = os.path.basename(download_result)

        name, extension = os.path.splitext(basename)
        audio_file = re.sub('\s+', '-',  name)
        complete_audio_path = f'{audio_file}.mp3'
        os.rename(download_result, complete_audio_path)
        return complete_audio_path

    def transcribe(audio_file, not_english=False):
        if not os.path.exists(audio_file):
            print(f'The following file doensn not exist: {audio_file}')
            return False

        if not_english:
            with open(audio_file, 'rb') as f:
                print("Translating non-English audio to English ...", end='')
                transcript = openai.Audio.translate('whisper-1', f)
                print(transcript)
                print('Done!')

        else:
            with open(audio_file, 'rb') as f:
                print("Transcribing Started ...", end='')
                transcript = openai.Audio.transcribe('whisper-1', f)
                print(transcript)
                print('Done!')

        name, extension = os.path.splitext(audio_file)
        transcript_filename = f'transcript-{name}.txt'
        with open(transcript_filename, 'w') as f:
            f.write(transcript['text'])

        #  delete the file
        os.remove(audio_file)
        return transcript_filename

    def summarize(transcript_filename):
        if not os.path.exists(transcript_filename):
            print("The transcript file doesn't exist!")
            return False

        with open(transcript_filename) as f:
            transcript = f.read()

        system_prompt = "Act as Expert one who can summarize any topic"
        prompt = f'''Create a summary of the following text.
            Text : {transcript}'''

        print("Summarizing Started....", end=" ")
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ],


        )
        os.remove(transcript_filename)
        print('Done!')
        r = response['choices'][0]['message']['content']
        return r

    downloaded_audio_file = youtube_audio_downloader(link)
    if not downloaded_audio_file:
        return Response({
            'error': 'plz make sure your youtube link is valid'
        }, status=400)
    transcribed_file = transcribe(downloaded_audio_file, not_english=False)
    if not transcribed_file:
        return Response({
            'error': 'Something wrong happen, plz make sure your open ai key is valid'
        }, status=400)
    summary = summarize(transcribed_file)
    if not summary:
        return Response({
            'error': 'Something wrong happen, plz make sure your open ai key is valid'
        }, status=400)
    return Response(summary)


@api_view(['GET'])
def bitcoinPriceAnalysis(request):

    query = request.query_params.get('query')
    open_ai_key = request.headers.get('x-openai-api-key')
    openai.api_key = open_ai_key

    url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/history"
    querystring = {
        "referenceCurrencyUuid": "yhjMzLPhuIDl", "timePeriod": "7d"}
    headers = {
        "X-RapidAPI-Key": "a617d6467dmshac84323ce581a72p11caa9jsn1adf8bbcbd47",
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    JSONResult = json.loads(response.text)
    history = JSONResult["data"]["history"]
    prices = []
    for change in history:
        prices.append(change["price"])

    pricesList = ','.join(prices)
    chatGPTPrompt = f"""
    Hey there ChatGPT! Could you provide a brief analysis based on the recent Bitcoin prices over the last seven days, also {query}, I'll share the price data with you, and I'd love to hear your insights on what this could mean for the cryptocurrency market. Thanks in advance for your help! price list: 
    """ + pricesList

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in the field of cryptocurrency and able to give a great analysis of the recent Bitcoin prices and you can suggest whether to buy or not."
             },
            {"role": "user", "content": chatGPTPrompt}
        ],
        max_tokens=400,

    )
    return Response(completion.choices[0].message.content)


@api_view(['GET'])
def create_meals(request):
    # ingredients, kcal, type_of_meal
    ingredients = request.query_params.get('ingredients')
    kcal = request.query_params.get('kcal')
    type_of_meal = request.query_params.get('type_of_meal')
    open_ai_key = request.headers.get('x-openai-api-key')
    openai.api_key = open_ai_key

    prompt = f'''Create a healthy daily {type_of_meal} meal plan for breakfast, lunch, and dinner based on the following ingredients: {ingredients}.
     Explain each recipe.
     The total daily intake of kcal should be below {kcal}.
     Assign a suggestive an concise name for each meal.
     Your answer should end with all the suggested titles like that:
     'Titles: 
     - title_1
     - title_2
     - title-3
     '''

    system_promote = 'You are an Expert and talented cook.'
    messages = [
        {"role": 'system', "content": system_promote},
        {"role": 'user', "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=1,
        max_tokens=1024,
        n=1

    )
    r = response['choices'][0].message.content
    return Response(r)
