nupic_function_recognition
====

## 目的
+ nupicのnetwork apiを使って, 関数の分類をする.

## 目次
### 概要
+ 時系列データ( y=f(x) )を入力し, そのデータを作成した関数を判別するタスクを解く.
+ nupicのnetwrok apiを使い, 入力が(x, y), 出力が関数確率(softmax関数みたいな感じ)となるnetwork(encoder, spacial pooler, temporal pooler)を作成する. このnetworkに対して, ある関数の出力f(x)をx=1からx=100まで入力する. 判別を行うclassifierには, 教師データとして関数の種類を入力する. これを繰り返し学習を行う. これにより, (x,y)の時系列データから関数fを判別できるnetworkができる.
+ このnetworkは, たとえ同じ入力であっても, それまで入力された内容からどの関数であるかを判別できる. 例えば, 単調増加(y=x)と単調減少(y=100-x)について考えてみると, (x,y)=(50, 50)は単調増加/単調減少どちらの関数にも当てはまるので, (x,y)のみではその値が単調増加から得られたものか単調減少から得られたものかを判別することは出来ない. しかし, このnetworkでは, x=50以前の入力も考慮されるので関数を判別することができる.
+ [nupic](https://github.com/numenta/nupic)をインストールする必要がある.

### 単層
+ [実行結果](docs/single.md) 
  + 典型的なモデルで, 判別できるかどうか試す.
  + 1カ所以外は判別できている状態となった.
+ [パラメータ調査](docs/parameter.md)
  + パラメータを変更し影響を調べる.
  + カラム数は, 入力を十分表現できる数があればよい.
  + カラム中発火数は, 文脈の判別に影響する. おそらく1~2%が妥当.
  + カラム中のセル数は, 文脈の判別に影響する. 大きい方が良いが時間かかる.
+ [関数増加](docs/add_function.md)
  + 判別する関数を増加させて, 判別できるか試す.
  + sin関数の分類を上手く行えていない.


### 多層
+ [直列層](docs/series_layer.md)
  + 同じ層を2つ重ねる.
  + 交点以外での正解率は上がるが, 交点周辺での正解率は下がる.
+ [並列層](docs/parallel_layer.md) 
  + 同じencoderから2つの異なる層でSDRを作り, その2つを統合する層を作る.
  + 同じ層を繋いだ場合, 直列層とほぼ同じ結果となった.
  + 異なる層を繋いだ場合, 多少結果が良くなった.
+ [層別学習](docs/unit_learning.md)
  + 1層づつ学習させると結果が良くなる.
  + 直列層, 並列層どちらでも同様の結果がでた.
  + sinの分離も出来るようになった.


### 汎化
+ [汎化](docs/generalization.md) 未まとめ
  + sinの周期などを変更した場合に分離出来るか確認する.
  + sensorを分離した場合, 良く判別できる気がする.

### 備考
+ CLAって分類に使うものなのか?
  + CLAはそもそも, オンラインで数ステップ先の結果を予測するものだから, ここでやっているように教師あり学習させる使い方は, 適切でないかも.
+ 普通にnupic使ったらこんなエラーがでた.
  + encoderにVectorEncoderOPFを使ったせい.
  + [nupic/issues/727](https://github.com/numenta/nupic/issues/727) にも上がっていたが, VectorEncoderOPF自体が不完全ぽいので, issue上げた人と同じ対応をした. VectorEncoderOPF使うべきでは無さそう.
```
  File "/Library/Python/2.7/site-packages/nupic-0.1.0-py2.7.egg/nupic/regions/RecordSensor.py", line 296, in compute
      outputs['sourceOut'][:] = self.encoder.getScalars(data)
      ValueError: could not broadcast input array from shape (2) into shape (1)
```

---

## CLA White Paper
+ 多分これ読んでないと何してるかよくわからんと思う.
+ [CLA White Paper](http://numenta.org/cla-white-paper.html)

## Install
+ だいたいここの通りにやればできた.
+ [nupic](https://github.com/numenta/nupic)

## tutorial
+ [nupic_tutorials](https://github.com/kokukuma/nupic_tutorials#network_api)
+ [nupic](https://github.com/numenta/nupic/tree/master/examples/network)

