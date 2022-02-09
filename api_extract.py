''' 분류 모델 API 
학습된 모델을 다른 사람들이 사용할 수 있도록 api를 만들어 배포 '''

from PIL import Image
import torch
from torchvision import transforms

transforms_test = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

model = torch.load("./weight/model_best_epoch.pt")

'''웹 API 개방을 위해 ngrok 서비스 이용
    API 기능 제공을 위해 Flask 프레임워크 사용 '''

# 필요한 라이브러리 설치하기
import io
from flask_ngrok import run_with_ngrok
from flask import Flask, jsonify, request


# 이미지를 읽어 결과를 반환하는 함수
def get_prediction(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = transforms_test(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        _, preds = torch.max(outputs, 1)
        
        input = image.cpu().data[0]
        input = input.numpy().transpose((1, 2, 0))
        # 이미지 정규화 해제하기
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        input = std * input + mean
        input = np.clip(input, 0, 1)
        # 이미지 출력
        plt.imshow(input)
        plt.title('예측 결과: ' + class_names[preds[0]])
        plt.show()

    return class_names[preds[0]]



app = Flask(__name__)
run_with_ngrok(app)

@app.route('/', methods=['POST'])
def predict():
    if request.method == 'POST':
        # 이미지 바이트 데이터 받아오기
        file = request.files['file']
        image_bytes = file.read()

        # 분류 결과 확인 및 클라이언트에게 결과 반환
        class_name = get_prediction(image_bytes=image_bytes)
        print("결과:", {'class_name': class_name})
        return jsonify({'class_name': class_name})

if __name__ == "__main__":
    app.run()


## 사용 방식
# curl -X POST -F file=@{이미지 파일명} {Ngrok 서버 주소}

## 사용 예시
# curl -X POST -F file=@dongseok.jpg http://c4cdb8de3a35.ngrok.io/

# 참고
# https://velog.io/@qsdcfd/%EC%9B%B9-%ED%8E%98%EC%9D%B4%EC%A7%80-%EB%A7%8C%EB%93%A4%EA%B8%B0