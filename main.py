import requests
from datetime import datetime
from win10toast import ToastNotifier
import pyttsx3
import threading

def get_match_data():
    return requests.get(
        url="https://temporeal.lance.com.br/storage/matches/copa-do-mundo-2022-28-11-2022-brasilxsuica.json"
    ).json()

engine = pyttsx3.init()
toaster = ToastNotifier()

last_update = None
while True:
    match_data = get_match_data()

    narrations = match_data['match']['narrations']
    last_narration = narrations[len(narrations)-1]
    last_narration_time = datetime.strptime(last_narration['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')

    if(not last_update) or (last_narration_time > last_update):
        last_update = last_narration_time
        last_narration_moment = narrations[len(narrations)-1]['moment']
        last_narration_text = narrations[len(narrations)-1]['text']
        print(f', \n, \n, \n{last_narration_moment}" - {last_narration_text}')
        toaster.show_toast("Jogos da Copa: ", f',{last_narration_moment}" - {last_narration_text}', threaded=True, icon_path=None, duration=10)
        engine.say(f',{last_narration_moment}" - {last_narration_text}')
        engine.runAndWait()