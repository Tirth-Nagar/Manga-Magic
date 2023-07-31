import os

def print_file_structure(path, indent=0):
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if entry == "venv":
            continue
        if os.path.isdir(full_path):
            print('  ' * indent + '|-- ' + entry + '/')
            print_file_structure(full_path, indent + 1)
        else:
            print('  ' * indent + '|-- ' + entry)

if __name__ == "__main__":
    current_directory = os.getcwd()
    print("Current Working Directory:", current_directory)
    print_file_structure(current_directory)
