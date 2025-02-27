import os
import shutil
from settings import BASE_DIR


class FileManager:
    def __init__(self, dir):
        self.base_dir = os.path.abspath(dir)
        self.current_dir = self.base_dir

    # 1.	Создание папки (с указанием имени);
    def create_folder(self, folder_name):
        folder_path = os.path.join(self.current_dir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"folder '{folder_name}' created.")
            return
        print(f"folder '{folder_name}' already exists!")

    # 2.	Удаление папки по имени;
    def delete_folder(self, folder_name):
        folder_path = os.path.join(self.current_dir, folder_name)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(f"folder '{folder_name}' deleted.")
            return
        print(f"folder '{folder_name}' does not exist!")

    # 3.	Перемещение между папками (в пределах рабочей папки) - заход в папку по имени, выход на уровень вверх;
    def change_directory(self, folder_name):
        if folder_name == "up":
            self.current_dir = os.path.dirname(self.current_dir)  #####################################
            print(f"moved to the folder: {self.current_dir}")
            return

        new_dir = os.path.join(self.current_dir, folder_name)
        if os.path.exists(new_dir) and os.path.isdir(new_dir):
            self.current_dir = new_dir
            print(f"Перешли в папку: {self.current_dir}")
            return
        print(f"folder '{folder_name}' does not exist!")

    # 4.	Создание пустых файлов с указанием имени;
    def create_file(self, file_name):
        file_path = os.path.join(self.current_dir, file_name)
        if not os.path.exists(file_path):  # если файла еще не существует
            with open(file_path, 'w') as f:
                pass
            print(f"file '{file_name}' created.")
            return
        print(f"file '{file_name}' already exists!")

    # 5.	Запись текста в файл (если текст какой-то существует, то происходит перезапись);
    def write_to_file(self, file_name, text):
        file_path = os.path.join(self.current_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(text)
            print(f"text is written to the file '{file_name}'.")
            return
        print(f"file '{file_name}' does not exist!")

    # 6.	Просмотр содержимого текстового файла;
    def read_file(self, file_name):
        file_path = os.path.join(self.current_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                print(f.read())
            return
        print(f"file '{file_name}' does not exist!")

    # 7.	Удаление файлов по имени;
    def delete_file(self, file_name):
        file_path = os.path.join(self.current_dir, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"file '{file_name}' deleted.")
            return
        print(f"file '{file_name}' does not exist!")

    # 8.	Копирование файлов из одной папки в другую;
    def copy_file(self, file_name, destination_folder):
        src_path = os.path.join(self.current_dir, file_name)
        dest_path = os.path.join(self.current_dir, destination_folder, file_name)
        if os.path.exists(src_path):
            shutil.copy(src_path, dest_path)
            print(f"file '{file_name}' copied to the folder '{destination_folder}'.")
            return
        print(f"file '{file_name}' does not exist!")

    # 9.	Перемещение файлов;
    def move_file(self, file_name, destination_folder):
        src_path = os.path.join(self.current_dir, file_name)
        dest_path = os.path.join(self.current_dir, destination_folder, file_name)
        if os.path.exists(src_path):
            shutil.move(src_path, dest_path)
            print(f"file '{file_name}' moved to the folder '{destination_folder}'.")
            return
        print(f"file '{file_name}' does not exist!")

    # 10.	Переименование файлов.
    def rename_file(self, old_name, new_name):
        old_path = os.path.join(self.current_dir, old_name)
        new_path = os.path.join(self.current_dir, new_name)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f"file '{old_name}' renamed, new name: '{new_name}'.")
            return
        print(f"file '{old_name}' does not exist!")


def main():
    fmanager = FileManager(BASE_DIR)

    while True:
        print(f"\ncurrent directory: {fmanager.current_dir}")
        print("  createFr (folder_name)")
        print("  deleteFr (folder_name)")
        print("  changeDir (dir_name / up)")
        print("  createFl (file_name)")
        print("  writeFl (file_name, text)")
        print("  readFl (file_name)")
        print("  deleteFl (file_name)")
        print("  copyFl (file_name, destination_dir)")
        print("  moveFl (file_name, destination_dir)")
        print("  renameFl (old_name, new_name)")
        print("  q")

        command = input(">").strip().split()
        if not command:
            continue
        cmd = command[0]  # сама команда
        args = command[1:]  # аргументы команды (если есть)

        if cmd == "createFr" and len(args) == 1:
            fmanager.create_folder(args[0])
        elif cmd == "deleteFr" and len(args) == 1:
            fmanager.delete_folder(args[0])
        elif cmd == "changeDir" and len(args) == 1:
            fmanager.change_directory(args[0])
        elif cmd == "createFl" and len(args) == 1:
            fmanager.create_file(args[0])
        elif cmd == "writeFl" and len(args) >= 2:
            fmanager.write_to_file(args[0], ' '.join(args[1:]))
        elif cmd == "readFl" and len(args) == 1:
            fmanager.read_file(args[0])
        elif cmd == "deleteFl" and len(args) == 1:
            fmanager.delete_file(args[0])
        elif cmd == "copyFl" and len(args) == 2:
            fmanager.copy_file(args[0], args[1])
        elif cmd == "moveFl" and len(args) == 2:
            fmanager.move_file(args[0], args[1])
        elif cmd == "renameFl" and len(args) == 2:
            fmanager.rename_file(args[0], args[1])
        elif cmd == "q":
            break
        else:
            print("wrong instruction!")


if __name__ == "__main__":
    main()