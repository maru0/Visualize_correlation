import glob
import django
import sys
import os
import re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')

django.setup()
from cms.models import *


# DJANGO_SETTINGS_MODULEにプロジェクトのsettings.pyのを指定します。

files = os.listdir("../")
remove_list = ['__pycache__', 'myapp', '.vscode', 'env', '.git']
for target in remove_list:
    files.remove(target)
files_file = [f for f in files if os.path.isdir(os.path.join("../", f))]

for dirs in files_file:
    csvfiles = os.listdir("../"+dirs)
    Category.objects.create(categories=dirs)
    for csvfile in csvfiles:
        csvfile = re.sub('.csv', '', csvfile)
        Deviation.objects.create(data_name=csvfile)
    # csvfiles = [f for f in csvfiles if os.path.isfile(
    #    os.path.join("../"+csvfiles, f))]
