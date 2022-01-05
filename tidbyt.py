#!/usr/bin/env python

import requests
import base64
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def get_hcp(ghinNum, lastName):

    urlbase = "https://api2.ghin.com/api/v1/public/login.json?"

    url = f"{urlbase}ghinNumber={ghinNum}&lastName={lastName}&remember_me=false"

    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        first_name = f"{data['golfers'][0]['FirstName']}"
        last_name = f"{data['golfers'][0]['LastName']}"
        ghin = data['golfers'][0]['GHINNumber']
        hcp = data['golfers'][0]['Value']

        return first_name, last_name, ghin, hcp


def create_image(first_name, last_name, ghin, hcp):

    in_file = "ghin.png"
    out_file = "ghin-custom.png"
     
    img = Image.open(in_file)
    draw = ImageDraw.Draw(img)

    name_font = ImageFont.load("Dina_r400-6.pil")
    hcp_font = ImageFont.load("6x13.pil")

    draw.text((2, 0), first_name.upper(), (255, 255, 255), font=name_font, align="center")
    draw.text((2, 8), last_name.upper(), (255, 255, 255), font=name_font, align="center")
    draw.text((38, 10), hcp, (255, 255, 255), font=hcp_font, anchor="mm", align="center")

    img.save(out_file)

def push_tidbyt(deviceID, token):

    with open("ghin-custom.png", "rb") as img_file:
        image = base64.b64encode(img_file.read()).decode('utf-8')

    url = f"https://api.tidbyt.com/v0/devices/{deviceID}/push"

    payload = '{\n  "image": "' + image + '",\n  "installationID": "GHIN",\n  "background": true\n}'

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token
        }

    response = requests.request("POST", url, data=payload, headers=headers)


def main():

    ghinNum = "" # GHIN Number
    lastName = "" # Your Last Name
    deviceID = "" # Tidbyt Device ID
    token = "" # Tidbyt API Token

    first_name, last_name, ghin, hcp = get_hcp(ghinNum, lastName)

    create_image(first_name, last_name, ghin, hcp)

    push_tidbyt(deviceID, token)


if __name__ == '__main__':
    main()