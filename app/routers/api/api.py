import shutil
from os import getenv, path
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable

import openai
from fastapi import APIRouter, Request, Depends, Response
from fastapi import UploadFile
from fastapi.templating import Jinja2Templates
from keras.models import load_model
from keras.utils import get_file, load_img, img_to_array
from numpy import argmax, max, array
from sqlalchemy.orm import Session
from starlette import status
from tensorflow import expand_dims, nn

from app.database.database import get_db
from app.utils.dependencies import get_api_version

openai.organization = "org-fIGpo6HM0J4nPzVJXFf7q0RW"
openai.api_key = getenv("OPENAI_API_KEY")
openai.Model.list()

router = APIRouter(prefix=get_api_version(), tags=["Predicting Model"], include_in_schema=True)

templates = Jinja2Templates(directory="templates")

model_dir = Path(path.join(path.dirname(__file__), '../..', 'database/tensor_model/SNAPI_model.h5'))

model = load_model(model_dir)
predictions = array(
    ['apple', 'banana', 'beetroot', 'bell pepper', 'cabbage', 'capsicum', 'carrot', 'cauliflower', 'chilli pepper',
     'corn', 'cucumber', 'eggplant', 'garlic', 'ginger', 'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce', 'mango',
     'onion', 'orange', 'paprika', 'pear', 'peas', 'pineapple', 'pomegranate', 'potato', 'raddish', 'soy beans',
     'spinach', 'sweetcorn', 'sweetpotato', 'tomato', 'turnip', 'watermelon'])


class ImageNotRecognizedException(Exception):
    pass


@router.post("/predict", name="api.predict", status_code=200)
async def predict_image(request: Request, image_file: UploadFile, db: Session = Depends(get_db),
                        response: Response = 200):
    if image_file == '':
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": "No Image supplied"}

    try:
        image_link = save_upload_file_tmp(image_file)
        image_path = get_file(fname=image_link, origin=image_link)
        print(image_path)
        img = load_img(image_path, target_size=(180, 180))

        img_array = expand_dims(img_to_array(img=img), 0)
        prediction = model.predict(img_array)
        score = nn.softmax(prediction[0])

        class_prediction = predictions[argmax(score)]
        model_score = round(max(score) * 100, 2)
        if model_score < 80:
            raise ImageNotRecognizedException('Image not recognized')
        description = generate_description(f"{class_prediction}")
        print(description)
        head, body, note = description.split('```')
        trim_body = body[body.rfind('=') + 2:]
        return {"detection": class_prediction, "detail": eval(trim_body), "notes": note}
    except ImageNotRecognizedException as ex:
        # copy image to unrecognized foldr
        # store dataset item, under unrecognized dataset
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {
            'detail': {
                'msg': 'Failed to analyze image. Please try a different angle or or taking it under lit conditions.'}
        }


def generate_description(input_):
    messages = [{"role": "user",
                 "content": """Give me nutritional facts of a' \n"""},
                {"role": "user", "content": f"{input_}. Format the output to a python dict"}]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = completion.choices[0].message.content
    return reply


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


def handle_upload_file(
        upload_file: UploadFile, handler: Callable[[Path], None]
) -> None:
    tmp_path = save_upload_file_tmp(upload_file)
    try:
        handler(tmp_path)
    finally:
        tmp_path.unlink()
