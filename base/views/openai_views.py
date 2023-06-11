from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from dotenv import load_dotenv
import openai
from django.http import HttpResponse
import time
from pytube import YouTube
import re
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
    try:
        # wait 3 seconds and send "happy"
        link = request.query_params.get('url')
        open_ai_key = request.headers.get('x-openai-api-key')
        openai.api_key = open_ai_key

        def youtube_audio_downloader(link):
            if "youtube.com" not in link:
                print("Please enter a valid YouTube URL")
                return False
            yt = YouTube(link)
            # check if the video is valid
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
                    print('Done!')

            else:
                with open(audio_file, 'rb') as f:
                    print("Transcribing Started ...", end='')
                    transcript = openai.Audio.transcribe('whisper-1', f)
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
            Text{transcript}
            
            Add a title to the summary.
            Your summary should be informative and factual, covering the most important aspects if the topic.
            Use BULLET POINTS if possible'''

            print("Summarizing Started....", end=" ")

            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': prompt}
                ],
                max_tokens=2024,
                temperature=1

            )

            #  delete the file
            print('Done!')
            r = response['choices'][0]['message']['content']
            os.remove(transcript_filename)
            return r

        downloaded_audio_file = youtube_audio_downloader(link)
        transcribed_file = transcribe(downloaded_audio_file, not_english=False)
        summary = summarize(transcribed_file)
        return Response(summary)
    except Exception as error:
        print(error)
        return Response({
            'error': 'Something wrong happen, plz make sure your open ai key is valid'
        }, status=400)
