import csv
import pandas as pd
import pdb
import django
import psycopg2
import re
import os
import glob
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')

django.setup()
from cms.models import *


class CsvImport():
    def shape(self, target_file):
        def f1(x): return re.sub(',', '', x)
        def f2(y): return re.sub('[^0-9|.]+', '', y)
        def f3(z): return float(re.sub('--', '0', z))
        def f4(z): return float(re.sub('', '0', z))
        with open(target_file, 'r') as f:
            datas = pd.read_csv(f, skiprows=[0, 1, 2], names=(
                'value', 'order', 'prefec', 'total', 'per', 'hensa'))
            print(len(datas.value))
            print(target_file)
            if (len(datas.value) != 49):
                print("not")
                print(target_file)
                with open("../tmp/lost.txt", 'a') as f:
                    save_name = target_file + "\n"
                    f.write(save_name)
                return False
            try:
                datas.total = datas.total.apply(f1)
            except:
                pass
            try:
                datas.total = datas.total.apply(f2)
            except:
                pass
            try:
                datas.per = datas.per.apply(f1)
                datas.per = datas.per.apply(f2)
            except:
                datas.hensa = datas.per

            category = target_file.split('/')[1]
            # datas.order = datas.order.apply(f3)
            # pdb.set_trace()
            # datas.total = datas.total.apply(f3)
            # datas.per = datas.per.apply(f3)
            # datas.hensa = datas.hensa.apply(f3)
            file_name = re.sub('.csv', '', target_file.split('/')[-1])
            for i, data in enumerate(datas.iterrows()):
                # object毎に必要なデータをfilter
                #category_id = Category.objects.filter(categories=category)
                #statics_id = Deviation.objects.filter(data_name=file_name)
                # orderprefec_id = Prefecture.objects.filter(
                #    prefecture=data[1].prefec)
                category_id = Category.objects.get(categories=category)
                statics_id = Deviation.objects.get(data_name=file_name)
                orderprefec_id = Prefecture.objects.get(
                    prefecture=data[1].prefec)
                if i >= 46:
                    break
                if len(data[1].total) == 0:
                    save_data1 = f4(data[1].total)
                else:
                    save_data1 = f3(data[1].total)
                if len(str(data[1].per)) == 0:
                    save_data2 = f4(data[1].per)
                else:
                    save_data2 = f3(str(data[1].per))
                if len(str(data[1].hensa)) == 0:
                    save_hensa = f4(data[1].hensa)
                else:
                    save_hensa = f3(str(data[1].hensa))
                # pdb.set_trace()
                #Sample.objects.create(cate_id=category_id, data_id=statics_id)
                Alldata.objects.create(
                    cate_id=category_id, static_id=statics_id, order_id=orderprefec_id,
                    data1=save_data1, data2=save_data2, hensa=save_hensa)
                # print(data[1].prefec, category_id, statics_id, orderprefec_id,
                #      save_data1, save_data2, save_hensa)
# f1 = lambda x : re.sub(',','.',x)
# lamda x : re.sub('','',x)


hoge = CsvImport()

files = os.listdir("../")
remove_list = ['__pycache__', 'myapp', '.vscode', 'env', '.git', 'tmp']
for target in remove_list:
    files.remove(target)
files_file = [f for f in files if os.path.isdir(os.path.join("../", f))]
for dirs in files_file:
    #dirs = "コンビニ"
    csvfiles = os.listdir("../"+dirs)
    for csvfile in csvfiles:
        fullpath = "../" + dirs + "/" + csvfile
        # print(fullpath)
        #fullpath = "../アルコール/アルコール消費量2016年.csv"
        hoge.shape(fullpath)
        # pdb.set_trace()
    print("ok")
    # pdb.set_trace()
