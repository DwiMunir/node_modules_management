import os
import subprocess
import shutil

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def list_top_level_node_modules(start_path='.'):
    node_modules_dirs = []
    for root, dirs, files in os.walk(start_path):
        if 'node_modules' in dirs:
            node_modules_path = root
            # Check if this node_modules is within another node_modules directory
            if not any('node_modules' in part for part in root.split(os.sep)):
                node_modules_dirs.append(node_modules_path)
                # Skip walking into this node_modules directory
                dirs.remove('node_modules')
    return node_modules_dirs

def delete_node_modules(node_modules_path):
    try:
        shutil.rmtree(node_modules_path)
        print(style.GREEN+f"Deleted: {node_modules_path}"+style.RESET)
    except subprocess.CalledProcessError as e:
        print(f"Failed to delete {node_modules_path}: {e}")

def reinstall_node_modules(project_path):
    try:
        yarn_lock_path = os.path.join(project_path, 'yarn.lock')
        pnpm_lock_path = os.path.join(project_path, 'pnpm-lock.yaml')
        if os.path.exists(yarn_lock_path):
            subprocess.run(['yarn', 'install'], cwd=project_path, check=True)
            print(f"Reinstalled node_modules in: {project_path}")
        elif os.path.exists(pnpm_lock_path):
            subprocess.run(['pnpm', 'install'], cwd=project_path, check=True)
            print(f"Reinstalled node_modules in: {project_path}")
        else :
          subprocess.run(['npm', 'install'], cwd=project_path, check=True)
          print(f"Reinstalled node_modules in: {project_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to reinstall node_modules in {project_path}: {e}")

def list_top_level_existing_packages(start_path='.'):
    # get all the directories in the start_path with existing package.json
    existing_packages = []
    for root, dirs, files in os.walk(start_path):
      if 'package.json' in files:
        package_json_path = root
        # Check if this package.json is within another node_modules directory
        if not any('node_modules' in part for part in root.split(os.sep)):
          existing_packages.append(package_json_path)
    return existing_packages

def set_path(start_path):
    node_modules_dirs = list_top_level_node_modules(start_path)
    
    print("\n\nFound node_modules directories:")
    if not node_modules_dirs:
        print(style.RED +"\nNo node_modules directories found.\n"+style.RESET)
    else:
      for idx, dir in enumerate(node_modules_dirs):
          print(f"{idx + 1}. {dir}")
      print("\n")
    return node_modules_dirs

def main():
    is_exit = False
    start_path = input("Enter the start path to search for node_modules: ")
    node_modules_dirs = set_path(start_path)

    while not is_exit:
      print(style.BLUE + "List of command: \n1. delete all node_modules\n2. reinstall all node_modules\n3. list available node_modules\n4. reinstall one\n5. delete one\n6. change path\n7. list ready to reinstall\n8. size of all node_modules\n9. exit\n" + style.RESET)
      action = input("Enter your choice : ").strip().lower()

      if action == '1':
          for dir in node_modules_dirs:
              delete_node_modules(dir)
              node_modules_dirs.remove(dir)
      elif action == '2':
          for dir in node_modules_dirs:
              project_path = os.path.dirname(dir)
              reinstall_node_modules(project_path)
      elif action == '3':
          node_modules_dirs = set_path(start_path)
          print("\nHere are the node_modules directories listed:\n")
          if not node_modules_dirs:
              print("\nNo node_modules directories found.\n")
          else:
            for idx, dir in enumerate(node_modules_dirs):
              print(f"{idx + 1}. {dir}")
      elif action == '4':
          idx = int(input("Enter the index of the node_modules directory to reinstall: ")) - 1
          project_path = node_modules_dirs[idx]
          reinstall_node_modules(project_path)
      elif action == '5':
          idx = int(input("Enter the index of the node_modules directory to delete: ")) - 1
          delete_node_modules(node_modules_dirs[idx])
          node_modules_dirs.pop(idx)
      elif action == '6':
          new_path = input("Enter the new start path to search for node_modules: ")
          node_modules_dirs = set_path(new_path)
      elif action == '7':
          node_modules_dirs = list_top_level_existing_packages(start_path)
          print("\nHere are the ready reinstall node_modules directories listed:\n")
          if not node_modules_dirs:
              print("\nNo node_modules directories found.\n")
          else:
            for idx, dir in enumerate(node_modules_dirs):
              print(f"{idx + 1}. {dir}")
            print("\n")
      elif action == '8':
          print("\nHere are the sizes of all node_modules directories:\n")
          total_size = 0
          for dir in node_modules_dirs:
            size = sum(os.path.getsize(os.path.join(dir, f)) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)))
            total_size += size
            if size < 1024:
              print(f"Size of {dir}:"+style.GREEN+f" {size:.2f} KB"+style.RESET)
            elif size < 1024 * 1024:
              print(f"Size of {dir}:"+style.GREEN+f" {size / 1024:.2f} MB"+style.RESET)
            else:
              print(f"Size of {dir}:"+style.GREEN+f" {size / 1024 / 1024:.2f} GB"+style.RESET)

          if total_size < 1024 * 1024:
            print(style.YELLOW+f"Total size of all node_modules: {total_size / 1024:.2f} MB"+style.RESET)
          else:
            print(style.YELLOW+f"Total size of all node_modules: {total_size / 1024 / 1024:.2f} GB"+style.RESET)
          print("\n")
      elif action == '9':
          is_exit = True
      else:
          print("No action taken.")
      
if __name__ == "__main__":
    main()
