from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from dotenv import load_dotenv
import openai


load_dotenv()
@api_view(['GET'])
def getOpenAi(request):
    
    # with open('openai_key.txt', 'r') as f:
    #     api_key = f.read().strip('\n')
    #     assert api_key.startswith('sk-'), "Please enter a valid OpenAI API key"


    openai.api_key = os.getenv('OPENAI_API_KEY')


    def gpt_classify_sentiment(prompt, emotions):
        system_promote= f'''You are an emotionally intelligent assistant.
        Classify the sentiment of the user's text with ONLY ONE OF THE FOLLOWING EMOTIONS: {emotions}.
        After classifying the text, response with the emotions ONLY. '''
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": 'system', "content": system_promote},{"role": "user", "content": prompt}],
            max_tokens=20,
            temperature=0,

        )

        r= response['choices'][0].message.content
        if r == '':
            return 'N/A'
        return r




    prompt = "After reviewing your course, I will say the truth. I am not satisfied with the course. I was learning at the beginning, but later I was wasting my time"
    emotions = "happy, sad, angry, neutral"
    result = gpt_classify_sentiment(prompt=prompt,emotions=emotions)
    # return 
    return Response(result)

