import os
import re

import pyautogui
import speech_recognition as sr
from gtts import gTTS

from command_manager import CommandManager


class Assistant:
    def __init__(self, name):
        self.name = name

        self.__rec = sr.Recognizer()
        self.__mic = sr.Microphone()
        self.__cmd_manager = CommandManager()

    def listen(self):
        text = ''
        with self.__mic as source:
            speech = self.__rec.listen(source)
            self.__rec.adjust_for_ambient_noise(source)

        try:
            text = self.__rec.recognize_google(speech, language='pt-BR')

        except sr.UnknownValueError:
            print('Não consegui entender.')
        except sr.RequestError as e:
            print(f'Erro ao reconhecer a fala: {e}')

        return text

    def speak(self, text):
        if text:
            tts = gTTS(text=text, lang='pt-br', slow=False)
            tts.save('response.mp3')
            os.system('mpg123 response.mp3')
            os.remove('response.mp3')
    

    def clear_text(self, text):
        text = text.lower()
        to_remove = [
            'para mim',
            'fazendo favor',
            'por favor',
            'você pode',
            'pode me',
            'me ajudar',
            'você poderia',
            self.name.lower(),
        ]

        for phrase in to_remove:
            regex = r'\b' + re.escape(phrase) + r'\b'
            text = re.sub(regex, '', text)

        text = re.sub(' +', ' ', text).strip()

        return text

    def execute_command(self, text):
        text = self.clear_text(text)
        command, match_result = self.__cmd_manager.get_matching_command(text)

        if not command:
            self.speak('Não entendi')

        print('Comando reconhecido:', command)

        if command == 'pesquisar':
            response = self.__cmd_manager.search_google(match_result.group(2))
            self.speak(response)

        elif command == 'transcrecer':
            self.speak('Começando a transcrever...')
            self.transcribe()

        elif command in {'toggle_play_pause', 'next', 'previous', 'play_song', 'play_playlist', 'open_client'}:
            try:
                txt = match_result.group(2)
            except:
                txt = ''

            response = self.__cmd_manager.spotify_command(
                command, txt
            )
            self.speak(response)

        elif command in {'play midia', 'pause midia'}:
            response = self.__cmd_manager.media_command(command)
            self.speak(response)

        # elif command in {'adicionar lista de tarefas', 'remover lista de tarefas', 'adicionar tarefa'}:
        #     response = self.__cmd_manager.task_manager_command(command)
        #     self.speak(response)

    def transcribe(self):
        transcribing = True
        while transcribing:

            text = ' ' + self.listen()
            match = re.search(
                '(finalize|finalizar|finaliza|encerre|encerrar|encerra)',
                text.lower(),
            )

            if match:
                regex = r'\bf' + match.group() + r'\b'
                text = re.sub(regex, '.', text.strip())

                self.speak('Transcrição finalizada!')
                transcribing = False
            print('Texto transcrito:', text)
            pyautogui.typewrite(text)

    def initialize(self):
        while True:
            text = self.listen()
            if self.name in text:
                self.execute_command(text)
