import base64
from io import BytesIO
import cv2
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
import onnxruntime as ort
from PIL import Image
from pydantic import BaseModel

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- init ---
MODEL_PATH = "multi_digit_model.onnx"
session = ort.InferenceSession(MODEL_PATH)
input_name = session.get_inputs()[0].name

# PTS
PTS_NOISE_MASK = np.array([[0, 24], [0, 0], [51, 0]], dtype=np.int32)


# --- Preproccesing Pipeline ---
def preprocess_image(img_bytes: bytes) -> np.ndarray:
    """
    """
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Invalid image content")

    # Grayscale conversion & dynamic masking
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = np.where((gray >= 247), 255, 0).astype(np.uint8)  # tolerance=8 (255-8=247)
    blurred_image = cv2.GaussianBlur(mask, (3, 3), 0)

    # Polygon mask for background noise removal
    cv2.fillPoly(blurred_image, [PTS_NOISE_MASK], color=0)

    # ONNX Tensor preparation (PIL image scaling)
    pil_img = Image.fromarray(blurred_image).resize((160, 70))

    # Normalization: Standardizing to [-1, 1] range
    img_array = np.array(pil_img, dtype=np.float32) / 255.0
    img_array = (img_array - 0.5) / 0.5

    # Expand dimensions for NCHW [1, 1, 70, 160] format
    return np.expand_dims(img_array, axis=(0, 1))


# --- Schema & Output ---
class CaptchaRequest(BaseModel):
    image_base64: str


class StandardResponse(BaseModel):
    success: bool
    result: str | None = None
    error: str | None = None


# --- Custom Exception Handlers ---
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "result": None, "error": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "result": None,
            "error": "Invalid payload. Pass a valid 'image_base64' string.",
        },
    )


# --- Main Endpoint ---
@app.post("/predict", response_model=StandardResponse)
def predict_captcha(data: CaptchaRequest):
    b64_string = data.image_base64
    if "," in b64_string:
        b64_string = b64_string.split(",")[1]

    # Base64 Decode (From Request)
    try:
        img_bytes = base64.b64decode(b64_string, validate=True)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Base64 string format.",
        )

    # Preprocessing and Inference
    try:
        input_data = preprocess_image(img_bytes)
        outputs = session.run(None, {input_name: input_data})

        # 4 digit argmax
        d1 = np.argmax(outputs[0], axis=1)[0]
        d2 = np.argmax(outputs[1], axis=1)[0]
        d3 = np.argmax(outputs[2], axis=1)[0]
        d4 = np.argmax(outputs[3], axis=1)[0]

        captcha_code = f"{d1}{d2}{d3}{d4}"

        return {"success": True, "result": captcha_code, "error": None}

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Decoded data is not a valid image.",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model failed to process the image tensor.",
        )
