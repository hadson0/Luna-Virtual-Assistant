import pickle


class Task:
    def __init__(self, title, status=False):
        self.name = title
        self.status = status

    def __str__(self):
        return f"{self.name} ({'Concluída' if self.status else 'Pendente'})"


class TaskList:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task_title):
        self.tasks = [task for task in self.tasks if task.title != task_title]

    def mark_done(self, task_title):
        for task in self.tasks:
            if task.title == task_title:
                task.status = True

    def __str__(self):
        return f'{self.name} ({len(self.tasks)} tarefas)\n' + '\n'.join(
            [str(task) for task in self.tasks]
        )


class TaskManager:
    def __init__(self):
        self.__lists = {}

    def save_lists(self, lists, file_name='task_lists.pickle'):
        with open(file_name, 'wb') as f:
            pickle.dump(lists, f)

    def load_lists(self, file_name='task_lists.pickle'):
        try:
            with open(file_name, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def add_list(self, list_name):
        self.__lists[list_name] = TaskList(list_name)
        return f"Lista '{list_name}' adicionada."

    def remove_list(self, list_name):
        self.__lists.pop(list_name, None)
        return f"Lista '{list_name}' removida."

    def show_lists(self):
        for list_name in self.__lists:
            print(list_name)

    def show_list(self, list_name):
        task_list = self.__lists.get(list_name)
        if task_list:
            return task_list
        return f"Lista '{list_name}' não encontrada."

    def add_task(self, list_name, task_title):
        task_list = self.__lists.get(list_name)
        if task_list:
            task_list.add_task(Task(task_title))
            return f"Tarefa '{task_title}' adicionada."
        return f"Lista '{list_name}' não encontrada."

    def remove_task(self, list_name, task_title):
        task_list = self.__lists.get(list_name)
        if task_list:
            task_list.remove_task(task_title)
            return f"Tarefa '{task_title}' removida."
        return f"Lista '{list_name}' não encontrada."

    def mark_done(self, list_name, task_title):
        task_list = self.__lists.get(list_name)
        if task_list:
            task_list.mark_done(task_title)
            return f"Tarefa '{task_title}' concluída."
        return f"Lista '{list_name}' não encontrada."
