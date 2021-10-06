from pywebio import *
from pywebio.output import *
from pywebio.input import *
from pywebio.pin import *

def tempConvert():
    conversion = input_group("Temperature Converter", [
    input("Temperature", name="temp"),
    radio("Convert to: ", options=["Celcius", "Fahrenheit"], value="Celcius", inline=True, required=True, name="converter")
    ])

    with put_loading(shape="border", color="dark"):
        converter = conversion.get("converter")

        if converter == "Celcius":
            put_text(conversion.get("temp"), "°C is", round(9/5*int(conversion.get("temp"))+32,2), "°F")

        elif converter == "Fahrenheit":
            put_text(conversion.get("temp"), "°F is", round(5/9*(int(conversion.get("temp"))-32),2), "°C")

    session.hold()