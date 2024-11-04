# weather of a city (temp and conditions)

import requests
import random
import asyncio

async def weather(message):
    try:
        list_for_how_to_give_weather = [1, 1, 1, 2]

        city_for_temperature = message.content[9:]

        api_key = ""

        result = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city_for_temperature}&appid={api_key}")

        not_parsed_weather = result.json()['weather'][0]
        weather = not_parsed_weather.get('main')
        description = not_parsed_weather.get('description')

        temp_k = result.json()['main'].get('temp')
        temp_c = round(int(temp_k) - 273.15)
        temp_f = round((temp_c * 9 / 5) + 32)

        city_name = result.json()['name']

        choice_of_how_to_give_weather = random.choice(list_for_how_to_give_weather)

        if choice_of_how_to_give_weather == 1:
            await asyncio.sleep(0.25)
            await message.channel.send(
                f"There is/are **{weather}({description})** in {city_name} with a temperature of {temp_c} degrees C  /  {temp_f} degrees F")

        elif choice_of_how_to_give_weather == 2:
            await asyncio.sleep(0.25)
            await message.channel.send("Why don't you stick your head out the window!?")
            await asyncio.sleep(1.5)
            await message.channel.send(
                f"anyways there is/are **{weather}({description})** in {city_name} with a temperature of {temp_c} degrees C  /  {temp_f} degrees F")

    except KeyError:
        # error when the city inputted is invalid
        await message.channel.send("Uh oh. Looks like the city you mentioned is invalid. Please try again.")
