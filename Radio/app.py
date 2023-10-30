import json
from os import listdir
from os.path import isfile, join
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
import uvicorn
from Radio.radioFrequency import Frequencies, RadioFrequency
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


@app.post("/frequencies/test")
async def test_frequencies(frequencies_data: list = Body(), response: Response = 200):
    name = frequencies_data[0]
    frequencies_data.pop(0)
    frequencies_data = frequency_dict_to_list(frequencies_data)
    print("START TEST")
    try:
        frequency = Frequencies()
        frequency.load_frequencies(frequencies_data)
        result = frequency.test_radio_frequencies()
    except Exception as error:
        print(error)
        response.status_code = 404
        return "Wrong data"
    print("result:")
    print(result)
    response.status_code = 200
    return result

@app.post("/frequency/test/")
async def test_frequencies(url: dict):
    frequency = RadioFrequency()
    frequency.radio_url = url["url"]
    if frequency.test_radio_frequency() == 1:
        return True
    else:
        return False


def save_in_file(file_path: Path, data):
    with open(file_path.resolve(), "w") as file_handler:
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
