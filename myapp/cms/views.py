from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from .forms import MessageForm, SignUpForm, UserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.template.context_processors import csrf
from . import forms
import pdb
from .models import Alldata, Category, Deviation, Prefecture
from django_pandas.io import read_frame
import pandas as pd
from sklearn.cluster import KMeans
from django.views import generic
import folium
import matplotlib.pyplot as plt


class Index():

    def index(request):
        # 登録のフォーム作成
        context = {
            'latest': 'ユーザ',
            'hoge': 'ページ',
        }
        return render(request, 'user.html', context)


class loginView(LoginView):
    form = forms.LoginForm
    template_name = "login.html"


class logoutView(LoginRequiredMixin, LogoutView):
    template_name = "logout.html"


class IndexView(TemplateView):
    template_name = "cms/index.html"


def index(request):
    ret = ''
    if request.method == 'POST':
        category_ids = request.POST.getlist("name")

        ret = 'OK'
        #target_df = df_statics(category_ids[0])
        for c_count, c_id in enumerate(category_ids):
            static_ids = Alldata.objects.filter(
                cate_id=c_id).distinct('static_id_id')
            for s_count, static_id in enumerate(static_ids):
                static_id = static_id.static_id_id
                if c_count == 0 and s_count == 0:
                    target_df = df_statics(c_id, static_id)
                else:
                    target_df = pd.merge(target_df, df_statics(
                        c_id, static_id), on='prefecture', how='left')
        c = {'result': category_ids, 'ret': ret}
        target_df = target_df.fillna(0)
        #target_df['prefecture_name'] = target_df['prefecture']
        # for count, pre_id in enumerate(target_df.prefecture):
        #    title = Prefecture.objects.get(id=pre_id)
        #   target_df.prefecture_name[count] = title.prefecture
        #target_df = target_df.set_index('prefecture')
        clustering(target_df)
        return render(request, 'map.html')
    else:
        userform = forms.UserForm
        categoryform = forms.CategoryForm
#        c = {'form': userform, }
        c = {'form': categoryform}
        c.update(csrf(request))
        return render(request, 'cms/user.html', c)


def df_statics(cate_id, static_id):
    contentname = Category.objects.filter(id=cate_id).get().categories
    # cate_id = Category.objects.values_list(
    #    'id', flat=True).get(categories=category)
    # static_id = Deviation.objects.values_list(
    #    'id', flat=True).get(data_name=contentname)
    contentname += str(static_id)
    csv_data = Alldata.objects.filter(
        cate_id_id=cate_id, static_id_id=static_id)
    df = read_frame(csv_data, fieldnames=[
                    'order_id_id', 'hensa'], verbose=False)
    df = df.rename(columns={'order_id_id': 'prefecture', 'hensa': contentname})
    return df


def clustering(df):
    topic_num = 5
#    df['cluster'] = KMeans(
#        n_clusters=topic_num, random_state=0).fit_predict(df[df.columns[df.columns != 'prefecture']].as_matrix())
    df['cluster'] = KMeans(
        n_clusters=topic_num, random_state=0).fit_predict(df[df.columns].as_matrix())
    japan_location = [35, 135]
    m = folium.Map(location=japan_location, zoom_start=5)
    geojson = './cms/templates/japan.geojson'
    # dfは県名とタグ情報のみをもつ
    # dfにタグ情報を追加するとよい
    scale = []
    print(df)
    scale.append([float(i) for i in range(topic_num)])
    m.choropleth(geo_data=geojson, data=df,
                 columns=['prefecture', 'cluster'],
                 key_on='feature.properties.id',
                 threshold_scale=scale[0],
                 fill_color='YlGnBu',
                 legend_name='県ごとの分類',
                 reset=True)
    m.save('./cms/templates/map.html')
    plt.figure()
    df.plot.scatter(x='cluster', y='prefecture', label='s', alpha=1.0)
    plt.savefig('hoge.png')


def testplot(request):
    return render(request, 'map.html')
