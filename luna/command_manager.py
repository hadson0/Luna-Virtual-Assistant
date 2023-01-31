import json
import re
import subprocess
import webbrowser

from spotify import Spotify
from task_manager import TaskManager


class CommandManager:
    def __init__(self):
        # self.__task_manager = TaskManager()
        self.__spotify = Spotify()

        self.__commands = {}
        with open('commands.json', 'r', encoding='utf-8') as f:
            command_data = json.load(f)

        for command in command_data:
            self.__commands[command['name']] = re.compile(command['regex'])

    def get_matching_command(self, text):
        for command, pattern in self.__commands.items():
            match = pattern.search(text)
            if match:
                return command, match

        return None, None

    def search_google(self, text):
        webbrowser.open(f'https://www.google.com/search?q={text}')
        return f'Pesquisando {text} no Google.'

    def spotify_command(self, command, text):
        if command == 'open_client':
            self.__spotify.open_client()
            return 'Spotify aberto!'

        elif self.__spotify.is_device_avaliable():
            if text:
                response = getattr(self.__spotify, command)(text)

            response = getattr(self.__spotify, command)()

            return response

        return 'O Spotify está fechado.'

    # def task_manager_command(self, command):
    #     if command == 'adicionar lista de tarefas':
    #         return 'Ok! Qual o nome da lista?'
    #         list_name = self.listen()
    #         response = self.__task_manager.add_list(list_name)
    #         return response

    #     elif command == 'remover lista de tarefas':
    #         return 'Ok! Qual o nome da lista?'
    #         list_name = self.listen()
    #         response = self.__task_manager.remove_list(list_name)
    #         return response

    #     elif command == 'adicionar tarefa':
    #         self.__task_manager.add_task(list_name, task_name)

    def media_command(self, command):
        command = 'playerctl ' + command.split()[0]
        subprocess.call(command.split())
        return 'Ok!'
