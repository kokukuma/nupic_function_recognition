nupic_function_recognition
====

## 目的
+ nupicのnetwork apiを使って, 関数の分類をする.

## 目次
### 概要
+ 時系列データ( y=f(x) )を入力し, そのデータを作成した関数を判別するタスクを解く.
+ nupicのnetwrok apiを使い, 入力が(x, y), 出力が関数確率(softmax関数みたいな感じ)となるnetworkを作成する. このnetworkに対して, ある関数の出力f(x)をx=1からx=100まで入力する. これにより, (x,y)の時系列データから関数fを判別できるnetworkができる.
+ このnetworkは, たとえ同じ入力であっても, それまで入力された内容からどの関数であるかを判別できる. 例えば, 単調増加(y=x)と単調減少(y=100-x)について考えてみると, (x,y)=(50, 50)は単調増加/単調減少どちらの関数にも当てはまるので, (x,y)のみではその値が単調増加から得られたものか単調減少から得られたものかを判別することは出来ない. しかし, このnetworkでは, x=50以前の入力も考慮されるので関数を判別することができる.

### １層
+ 対象関数
  + 定数(const)     : y = 50
  + 単調増加(plus)  : y = x
  + 単調減少(minus) : y = 100-x
+ 評価指標
  + 
+ 結果
  + 
+ パラメータ調査
  + SPのカラム数
  + SPのカラム発火割合
  + TPのセル数

### 多層
+ 構造
  + 1-1-1 構造
  + 3-1 構造(同一encoder)
  + 3-1 構造(別encoder)
+ 結果
  + 1-1-1 構造
  + 3-1 構造(同一encoder)
  + 3-1 構造(別encoder)

### 関数増加
+ 追加関数
  + sin関数(sin)       :
  + 2次関数(quad)      :
  + ステップ関数(step) :

+ 

---

## CLA White Paper
+ 多分これ読んでないと何してるかよくわからんと思う.
+ [CLA White Paper](http://numenta.org/cla-white-paper.html)

## Install
+ だいたいここの通りにやればできた.
+ [nupic](https://github.com/numenta/nupic )

## tutorial
+ [nupic_tutorials](https://github.com/kokukuma/nupic_tutorials#network_api)
+ [nupic](https://github.com/numenta/nupic/tree/master/examples/network)

