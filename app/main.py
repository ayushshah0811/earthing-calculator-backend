from fastapi import FastAPI, HTTPException
from app.model import EarthingInput, EarthingOutput
from app.calculations import calculate_earthing
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Earthing Calculation Engine",
    version="1.0",
    description="Internal company tool for IS 3043 earthing calculations",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all origins (OK for internal tool)
    allow_credentials=True,
    allow_methods=["*"],        # allow POST, GET, etc.
    allow_headers=["*"],        # allow all headers
)

@app.post("/calculate", response_model=EarthingOutput)
def calculate(input_data: EarthingInput):
    try:
        return calculate_earthing(input_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
