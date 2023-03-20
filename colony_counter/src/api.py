import io
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from  src.main import Predict, Count_vis
from fastapi import FastAPI, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, StreamingResponse

app = FastAPI()
# allow communication from all frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def save_file_tmp(file) -> Path :
    """takes in a file and saves it temporarily and
    returns the path of the file
    """
    suffix = Path(file.filename).suffix
    try:
         with NamedTemporaryFile(delete=False, suffix=suffix) as temp_img_file:
            # copy file recieved and store it temporarily
            shutil.copyfileobj(file.file, temp_img_file)
            # get path of stored
            temp_img_path = Path(temp_img_file.name)
    finally:
        file.file.close()
    return temp_img_path

@app.get('/', response_class=PlainTextResponse)
def root():
    return 'Welcome to the root api \n Go to /colonies/ endpoint '

@app.post('/colony/')
def count(file:UploadFile):
    img_path = save_file_tmp(file)
    try:
        image = str(img_path)
        pred_image, colonies = Count_vis(Predict(image), image)

        buffer_bytes = io.BytesIO()# bytes array
        pred_image.save(buffer_bytes, format= 'JPEG')# save image to bytes array

        image_headers = {'1-number-of-colonies': str(colonies)}

        return Response(content=buffer_bytes.getvalue(), headers=image_headers, media_type="image/jpg")
    finally:
        img_path.unlink()
