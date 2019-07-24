# Visualize correlation
* ユーザにカテゴリを複数選択させる
* 選択されたカテゴリに従って、k-meansを利用して県をクラスタリング
* クラスタリングした結果を地図上に可視化
* 可視化結果から県ごとの相関を知ることができる

## Demonstration
* カテゴリ選択画面
    ![カテゴリ選択画面](https://user-images.githubusercontent.com/33250779/61775811-9b630100-ae34-11e9-8043-63745478685a.png)

* 地図可視化画面
    ![地図可視化画面](https://user-images.githubusercontent.com/33250779/61775366-c8fb7a80-ae33-11e9-8ff2-59f7de5aa851.png)



## Data
* とどラン(https://todo-ran.com/)
* カテゴリの全データを取得


## k-means
* カテゴリ情報を基に、県をクラスタに分割
* クラスタ数は5で固定
* 自動クラスタ決定は今後行う予定


## Technology
* Django(ver:2.2.3)
    * システムの作成に使用
* scikit-learn(ver:0.21.2)
    * k-meansに使用
* folium(ver:0.9.1)
    * 地図の可視化に使用