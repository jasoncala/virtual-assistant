import speech_recognition as sr 
import os 
from gtts import gTTS 
import datetime 
import warnings
import calendar 
import random
import wikipedia

#Ignoring warning messages
warnings.filterwarnings('ignore')

#Record audio and convert to string
def recordAudio():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print('Say Something!')
		audio = r.listen(source)
	data = ''
	try:
		data = r.recognize_google(audio)
		print('You said: '+data)
	except sr.UnknownValueError:
		print('Google Speech Recognition could not understand the audio, unknown error')
	except sr.RequestError as e:
		print('Request results from Googles Speech Recognition service error '+e)

	return data

#Convert text to audio (virtual assistant response)
def assistantResponse(text):
	print(text)
	myobj = gTTS(text = text, lang = 'en', slow = False)
	myobj.save('assistant_response.mp3')
	os.system('start assistant_response.mp3')

#Wake word
def wakeWord(text):
	WAKE_WORDS = ['hey babushka', 'hey vee', 'hey computer', 'a computer']
	text = text.lower()

	for phrase in WAKE_WORDS:
		if phrase in text:
			return True
	return False

#Give current date
def getDate():
	month_names = ['January', 'February', 'March', 'April', 'May','June',
	'July', 'August', 'September', 'October', 'November', 'December']
	ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th',
	'9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th',
	'18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', 
	'27th', '28th', '29th', '30th', '31st']

	now = datetime.datetime.now()
	my_date = datetime.datetime.today()
	weekday = calendar.day_name[my_date.weekday()]
	monthNum = now.month 
	dayNum = now.day 

	return 'Today is '+weekday+' '+ month_names[monthNum-1] + ' the ' + ordinalNumbers[dayNum-1]+'.'

#Return greeting
def greeting(text):
	GREETING_INPUTS = ['hi', 'hey', 'whats poppin', 'hello', 'whats crackalackin']
	GREETING_RESPONSES = ['howdy', 'whats good', 'hey there muchacho']
	for word in text.split():
		if word.lower() in GREETING_INPUTS:
			return random.choice(GREETING_RESPONSES) +'.'
	return ''

#Get name from text (if they ask what something is)
def getKnowledge(text):
	wordList = text.split()
	for i in range(0, len(wordList)):
		if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'what' and wordList[i+1].lower() == 'is':
			return wordList[i+2] + ' ' + wordList[i+3]
		elif i + 1 <= len(wordList) and wordList[i].lower() == 'what' and wordList[i+1].lower() == 'is':
			print('test')
			return wordList[i+2] + ' '
	return 'Mystery'

def main():
	while True:
		text = recordAudio()
		response = ''

		# Check for wake word
		if(wakeWord(text) == True):
			response = response + greeting(text)

			if('date' in text):
				get_date = getDate()
				response = response + ' ' + get_date

			if('time' in text):
				now = datetime.datetime.now()
				m = ''
				if now.hour >= 12:
					m = 'p.m'
					hour = now.hour - 12
				else:
					m = 'a.m'
					hour = now.hour 
				if now.minute < 10:
					minute = '0' + str(now.minute)
				else:
					minute = str(now.minute)
				response = response + ' ' + 'It is '+str(hour)+ ':'+minute+' '+m+' .'

			if('what is' in text):
				topic = getKnowledge(text)
				wiki = wikipedia.summary(topic, sentences=2)
				response = response + ' ' + wiki

			assistantResponse(response)


if __name__ == '__main__':
	main()
