import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
import uvicorn
from Radio.radioFrequency import KurzFrequencies, LangFrequencies, MittelFrequencies, UKWFrequencies
from Radio.util.util import get_project_root

# from Radio.gpio.button import RadioButtonsRaspi

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/frequencies/{name}")
async def frequencies(name):
    if name == "Lang":
        return LangFrequencies().frequencies
    elif name == "Mittel":
        return MittelFrequencies().frequencies
    elif name == "Kurz":
        return KurzFrequencies().frequencies
    elif name == "UKW":
        return UKWFrequencies().frequencies
    else:
        return {}


def frequency_dict_to_list(frequency_dict: dict):
    list_data = []
    for frequency in frequency_dict:
        if "radio_url_re" in frequency:
            list_data.append([
                frequency["name"], frequency["minimum"], frequency["maximum"],
                frequency["radio_name"], frequency["radio_url"], frequency["radio_url_re"]]
            )
        else:
            list_data.append([
                frequency["name"], frequency["minimum"], frequency["maximum"],
                frequency["radio_name"], frequency["radio_url"], ""]
            )
    return list_data


@app.post("/frequencies")
async def save_frequencies(frequencies_data: list = Body(), response: Response = 200):
    name = frequencies_data[0]
    frequencies_data.pop(0)
    frequencies_data = frequency_dict_to_list(frequencies_data)
    try:
        frequency = LangFrequencies()
        frequency.load_frequencies(frequencies_data)
    except Exception as error:
        print(error)
        response.status_code = 404
        return "Wrong data"
    save_in_file(file_path=get_project_root() / f'data/freq_{name.lower()}.json', data=frequency.to_list())
    response.status_code = 200
    return True


def save_in_file(file_path: Path, data):
    with open(file_path.resolve(), "w") as file_handler:
        json.dump(data, file_handler, indent=4)


@app.get("/json/")
async def json_re():
    data = [
        {
            "id": 1,
            "name": "abc",
            "username": "Bret",
            "email": "mail@mail.biz",
        }
    ]
    return data


if __name__ == "__main__":
    origins = ['http://localhost:3000', 'http://127.0.0.1:3000']

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(app, host="127.0.0.1", port=8000)
