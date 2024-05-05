import json
import time
from os import listdir
from os.path import isfile, join
from pathlib import Path
from typing import Generator

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body, status, HTTPException
import uvicorn
from starlette.responses import StreamingResponse

from Radio.dataProcessing.radioFrequency import Frequencies, RadioFrequency
from Radio.util.util import get_project_root

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/frequencies/{name}")
async def frequencies(name):
    name = name.lower()
    return Frequencies(file_name=f"freq_{name}.json").frequencies


def frequency_dict_to_list(frequency_dict: dict):
    list_data = []
    for frequency in frequency_dict:
        list_data.append([
            frequency["name"], frequency["minimum"], frequency["maximum"],
            frequency["radio_name"], frequency["radio_url"], frequency["radio_name_re"],
            frequency["radio_url_re"], frequency["re_active"]]
        )
    return list_data


@app.get("/frequencyNames")
async def get_frequency_names():
    return get_frequency_names()


def get_frequency_names():
    freq_files = get_freq_files()
    freq_names = []
    for file_name in freq_files:
        freq_names.append(file_name.replace("freq_", "").replace(".json", ""))
    return freq_names


def get_freq_files():
    path_data = get_project_root() / 'data'
    freq_files = [f for f in listdir(path_data) if isfile(join(path_data, f)) and f.startswith("freq")]
    return freq_files


def load_settings() -> dict:
    path_settings = get_project_root() / 'data/settings.json'
    with open(path_settings.resolve()) as f:
        settings = json.load(f)
    return settings


@app.post("/frequencies")
async def save_frequencies(frequencies_data: list = Body(), response: Response = 200):
    name = frequencies_data[0]
    frequencies_data.pop(0)
    frequencies_data = frequency_dict_to_list(frequencies_data)
    try:
        frequency = Frequencies()
        frequency.load_frequencies(frequencies_data)
    except Exception as error:
        print(error)
        response.status_code = 404
        return "Wrong data"
    save_in_file(file_path=get_project_root() / f'data/freq_{name.lower()}.json', data=frequency.to_list())
    response.status_code = 200
    return True


@app.post("/frequencies/test2")
async def test_frequencies(frequencies_data: list = Body(), response: Response = 200):
    name = frequencies_data[0]
    frequencies_data.pop(0)
    frequencies_data = frequency_dict_to_list(frequencies_data)
    print("START TEST")
    start = time.time()
    try:
        frequency = Frequencies()
        frequency.load_frequencies(frequencies_data)
        result = frequency.test_radio_frequencies()
    except Exception as error:
        print(error)
        response.status_code = 404
        return "Wrong data"
    end = time.time()
    print(f"duration: {end - start}")
    print("result:")
    print(result)
    response.status_code = 200
    return result


@app.post("/frequencies/test")
async def get_image_file(frequencies_data: list = Body(), response: Response = 200):
    name = frequencies_data[0]
    frequencies_data.pop(0)
    frequencies_data = frequency_dict_to_list(frequencies_data)
    frequencies_obj = Frequencies()
    frequencies_obj.load_frequencies(frequencies_data)
    print("START TEST")
    try:
        return StreamingResponse(
            content=test_all_frequencies(frequencies_obj),
            media_type='application/json'
        )
    except Exception as error:
        raise HTTPException(detail=error.__str__(), status_code=status.HTTP_404_NOT_FOUND)


def test_all_frequencies(frequencies_obj: Frequencies) -> Generator:
    for frequency in frequencies_obj.frequencies:
        yield json.dumps([frequency.radio_url, frequency.test_radio_frequency(),
                          frequency.radio_url_re, frequency.test_radio_frequency(test_re=True)])


@app.post("/frequency/test/")
async def test_frequencies(url: dict):
    frequency = RadioFrequency()
    frequency.radio_url = url["url"]
    if frequency.test_radio_frequency() == 1:
        return True
    else:
        return False


@app.post("/frequency/testWithRe/")
async def test_frequencies(url: dict):
    frequency = RadioFrequency()
    frequency.radio_url = url["url"]
    frequency.radio_url_re = url["url_re"]
    if url["url"]:
        if frequency.test_radio_frequency() == 1:
            url_state = True
        else:
            url_state = False
    else:
        url_state = None
    if url["url_re"]:
        if frequency.test_radio_frequency(True) == 1:
            url_state_re = True
        else:
            url_state_re = False
    else:
        url_state_re = None
    return url_state, url_state_re


def save_in_file(file_path: Path, data):
    for item in data:
        print(item)
    with open(file_path.resolve(), "w", encoding='utf-8', ) as file_handler:
        json.dump(data, file_handler, indent=4)


def run():
    origins = ['http://localhost:3000', 'http://127.0.0.1:3000']

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(app, host="127.0.0.1", port=8000)


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
