add_function
====

### 追加関数
+ sin関数(sin)
+ 2次関数(quad)
+ ステップ関数(step)

### モデル
+ (SP) カラム数    : 4048
+ (SP) カラム発火数: 40(1%)
+ (TP) 1カラム当たりのセル数: 32

### 結果
+ 平均正解率
  + 他の関数との交点が多いsin関数は正解率が低くなる. 文脈よりも入力に依存しているということか?
  + なぜか, flatの正解率も凄く低くなる.

  | function_type | accuracy_rate |
  | -----         | -----         |
  | flat          | 0.831         |
  | plus          | 0.815         |
  | minus         | 0.943         |
  | sin           | 0.715         |
  | step          | 0.822         |
  | quad          | 0.889         |

+ 入力毎正解率
  + sin
    ![4048_40_32_sin.png](docs/images/4048_40_32_sin.png)
  + flat
    ![4048_40_32_flat.png](docs/images/4048_40_32_flat.png)
