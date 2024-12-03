from fastapi import APIRouter, File, UploadFile
from code.utils.serve_model import read_imagefile, predict

router = APIRouter()

@router.post("/invocations")
async def read_item(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return {"code": 429, "message": "Image must be jpg or png format!", "data": {}}
    image = read_imagefile(await file.read())
    prediction, score = predict(image)
    return {"code": 200, "message": "OK", "data": {"prediction": prediction, "confidence": f"{float(score):.6f}%"}}