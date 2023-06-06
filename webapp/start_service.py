from collections import defaultdict
import sys 

import uvicorn
import numpy as np
import cv2
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import onnxruntime as ort

app = FastAPI()

# CORSミドルウェアの追加
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "null"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ラベルの名前と推論モデルをローダ
labeldict=defaultdict(int)
types=["タイプ1","タイプ2"]
for i,t in enumerate(types):
    labeldict[i]=t
    
try:
    session = ort.InferenceSession("best.onnx")
except Exception as E:
    sys.exit("モデルをロット失敗")


# 典型的な推論部分
def predict(image):
    image=np.transpose(image, (2, 0, 1))
    image=image[None].astype(np.float32)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    out = session.run([output_name], {input_name: image})
    out=np.argmax(out[0].squeeze())
    result=labeldict[out]   
    return result

# 画像を受け取り、推論を行うエンドポイントを定義
@app.post("/predict")
async def predict_image( image_data: UploadFile = File(...)):
    content_type = image_data.content_type
    if not content_type.startswith("image/"):
        return {"error": "ファイルは画像ではありません"}
    file_bytes = await image_data.read()
    nparr = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = predict(image)
    return {"result": result}

if __name__ == "__main__":
    uvicorn.run("start_service:app", host="127.0.0.1", port=8000, reload=True)
