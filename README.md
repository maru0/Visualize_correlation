# Visualize correlation
* ユーザにカテゴリを複数選択させる
* 選択されたカテゴリに従って、k-meansを利用して県をクラスタリング
* クラスタリングした結果を地図上に可視化
* 可視化結果から県ごとの相関を知ることができる


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