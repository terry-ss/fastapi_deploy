# 簡易なウェブアプリケーション
学習済みのONNXファイル（best.onnxの名前を付く。また、画像のサイズとONNXモデルの入力サイズが同じとする）をwebapp/に置き、`python start_serve.py`でプログラムを起動し、ブラウザ（edgeなど）で index.html を開いて画像のアップロードしてから、モデル推論結果のデモを表示します。

* 依頼(requirements.txt)
```
fastapi==0.95.1
numpy==1.23.5
onnx==1.13.1
onnxruntime==1.14.1
onnxsim==0.4.0
opencv-python==4.7.0.72
uvicorn==0.21.1
```
