import os
import subprocess

from source.utils.variables import STREAM_BACKGROUND_PATH

# extra data
icon_path = os.path.join('.', 'source', 'gui', 'images', 'app_icon.ico')
# we need to add this manually: https://github.com/ultralytics/ultralytics/tree/main/ultralytics
ultralytics = os.path.join('.', 'dev_setup', 'exe_gen_extra_files', 'ultralytics')
runs = os.path.join('.', 'runs')  # yolo detection models
main_script = os.path.join('.', 'main.py')

pyinstaller_cmd = [
    'pyinstaller',
    '--noconfirm',
    '--onefile',
    '--windowed',
    '--icon', f'{icon_path}',
    '--name', "Traffic Surveillance",
    '--add-data', f'{ultralytics};ultralytics/',
    '--add-data', f'{runs};runs/',
    '--add-data', f'{STREAM_BACKGROUND_PATH};.',
    '--distpath', os.path.join(os.getcwd(), 'dist'),
    f'{main_script}'
]

subprocess.run(pyinstaller_cmd, shell=True)
