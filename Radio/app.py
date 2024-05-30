import asyncio
import json
import time
from os import listdir
from os.path import isfile, join
from pathlib import Path
from random import randint
from typing import Generator

import uvicorn
from fastapi import Body, status, HTTPException
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import StreamingResponse

from Radio.util.dataTransmitter import DataTransmitter, Publisher
from Radio.dataProcessing.equalizerData import Equalizer
from Radio.dataProcessing.radioFrequency import Frequencies, RadioFrequency
from Radio.db.db import Database
from Radio.util.util import get_project_root

app = FastAPI()
db = Database()
data_transmitter: DataTransmitter = DataTransmitter()
publisher: Publisher = Publisher()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/stream/volume")
async def websocket_volume(websocket: WebSocket):
    await websocket.accept()
    try:
        volume_old = None
        while True:
            volume = db.get_volume()
            if volume_old != volume:
                volume_old = volume
                volume_data = json.dumps({"volume": volume})
                await websocket.send_text(volume_data)
            await asyncio.sleep(1)  # Simulate data sent every second using asyncio compatible sleep
    except Exception:
        print("WebSocket disconnected")
        await websocket.close()

@app.post("/volume")
async def set_volume(volume: dict):
    data_transmitter.send({"volume": int(volume["volume"])})
    return {"message": "Volume set successfully"}

@app.websocket("/stream/equalizer")
async def websocket_equalizer(websocket: WebSocket):
    await websocket.accept()
    try:
        equalizer_old: Equalizer = Equalizer()
        equalizer_data = json.dumps(equalizer_old.to_dict())
        await websocket.send_text(equalizer_data)
        while True:
            equalizer: Equalizer = db.get_equalizer()
            if equalizer_old != equalizer:
                equalizer_old.from_list(equalizer.to_list())
                equalizer_data = json.dumps(equalizer.to_dict())
                await websocket.send_text(equalizer_data)
            await asyncio.sleep(1)  # Simulate data sent every second using asyncio compatible sleep
    except Exception:
        await websocket.close()

@app.post("/equalizer")
async def set_equalizer(equalizer_data: dict):
    equalizer = Equalizer()
    equalizer.from_dict(equalizer_data)
    publisher.publish(f'equalizer:{str(equalizer.to_list())}')
    return {"message": "Equalizer set successfully"}

@app.websocket("/stream/frequency_values")
async def websocket_frequency_values(websocket: WebSocket):
    await websocket.accept()
    try:
        frequency_old = {}
        while True:
            frequency = db.get_frequency_values()
            if frequency_old != frequency:
                frequency_old = frequency.copy()  # Create a copy of frequency
                frequency_data = json.dumps(frequency)
                await websocket.send_text(frequency_data)
            await asyncio.sleep(0.01)  # Simulate data sent every second using asyncio compatible sleep
    except Exception:
        await websocket.close()

@app.post("/frequency")
async def set_frequency(frequency: dict):
    data_transmitter.send({"frequency": {"name": frequency["name"], "value": int(frequency["value"])}})
    return {"message": "Frequency set successfully"}

@app.post("/re_active")
async def set_re_active(active: dict):
    # TODO: Implement the necessary operations to set the re_active
    db.replace_re_active(active["active"])
    return {"message": "Radio active status set successfully"}

@app.websocket("/stream/radio_frequency")
async def websocket_radio_frequency(websocket: WebSocket):
    await websocket.accept()
    try:
        frequency_old = RadioFrequency()
        while True:
            frequency = db.get_radio_frequency()
            if frequency_old != frequency:
                frequency_old = RadioFrequency(name=frequency.name, minimum=frequency.minimum,
                                               maximum=frequency.maximum, radio_name=frequency.radio_name,
                                               radio_url=frequency.radio_url, radio_name_re=frequency.radio_name_re,
                                               radio_url_re=frequency.radio_url_re, re_active=frequency.re_active)
                frequency_data = json.dumps(frequency.to_dict())
                await websocket.send_text(frequency_data)
            await asyncio.sleep(1)  # Simulate data sent every second using asyncio compatible sleep
    except Exception as e:
        await websocket.close()


@app.get("/buttons/")
async def get_buttons_settings():
    path_settings = get_project_root() / 'data/settings.json'
    with open(path_settings.resolve()) as f:
        settings = json.load(f)
    buttons = []
    for name, button_settings in settings["buttons"].items():
        if button_settings["active"]:
            buttons.append({"name": name, "reversed": button_settings["reversed"],
                             "type": button_settings["action"]["type"], "state": False})
    return buttons

@app.post("/button")
async def set_button(button: dict):
    data_transmitter.send({"button": {"name": button["name"], "value": button["value"]}})
    # Perform the necessary operations to set the button
    return {"message": "Button set successfully"}

@app.websocket("/stream/buttons")
async def websocket_buttons(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            buttons = db.get_buttons_data()
            await websocket.send_text(json.dumps(buttons))
            await asyncio.sleep(1)  # Simulate data sent every second using asyncio compatible sleep
    except Exception:
        await websocket.close()

@app.get("/frequency_names")
async def get_frequency_names():
    path_settings = get_project_root() / 'data/settings.json'
    with open(path_settings.resolve()) as f:
        settings = json.load(f)
    frequency_names = []
    for name, analog_item in settings["analog"]["sensors"].items():
        if analog_item["is_frequency"] and analog_item["on"]:
            frequency_names.append({name: {"min": analog_item["min"], "max": analog_item["max"]}})
    return frequency_names


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
