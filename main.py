import tkinter as tk
import time
from pip._vendor import requests as rq
from PIL import Image, ImageTk
from math import ceil
from variables import *
import simplenote

def clock_update():
    up_row = time.strftime('%a %H:%M:%S')
    down_row = time.strftime('%d %b %Y')
    clock_ctr = up_row + '\n' + down_row
    clock.config(text=clock_ctr, foreground='white', background='black', font=60)
    clock.after(200,clock_update)

def weather_update():
    wether_res = rq.get(W_HTTPS, params={'q': CITY_NAME, 'units':'metric', 'appid': W_API_KEY})
    data = wether_res.json()
    temp = str(data['main']['temp']) + ' ' + chr(0x00b0) + 'C'
    icon = data['weather'][0]['icon']    
    match icon:
        case '01d':
            w_path = "./weather_icons/png/01d.png"
        case '01n':
            w_path = "./weather_icons/png/01n.png"
        case '02d':
            w_path = "./weather_icons/png/02d.png"
        case '02n':
            w_path = "./weather_icons/png/02n.png"
        case '03d' | '03n':
            w_path = "./weather_icons/png/03d.png"
        case '04d' | '04n':
            w_path = "./weather_icons/png/04d.png"
        case '09d' | '09n':
            w_path = "./weather_icons/png/09d.png"
        case '10d':
            w_path = "./weather_icons/png/10d.png"
        case '10n':
            w_path = "./weather_icons/png/10n.png"
        case '11d' | '11n':
            w_path = "./weather_icons/png/11d.png"
        case '13d' | '13n':
            w_path = "./weather_icons/png/13d.png"
        case '50d' | '50n':
            w_path = "./weather_icons/png/50d.png"

    w_img.config(file=w_path)
    w_temp.config(text=temp, foreground='white', background='black', font=70)
    w_temp.after(1800000,weather_update)

def traffic_update():
    now = time.strftime('%Y-%m-%dT%H:%M')
    traffic_res = rq.get(T_HTTPS, params={'origins': WP0, 'destinations': WP1, 'travelMode': 'driving', 'startTime' : now, 'key': M_API_KEY})
    data = traffic_res.json()
    duration = float(data["resourceSets"][0]['resources'][0]['results'][0]['travelDuration'])
    duration = ceil(duration)
    distance = float(data["resourceSets"][0]['resources'][0]['results'][0]['travelDistance'])
    distance = round(distance, 1)
    map_res = rq.get(M_HTTPS, params={'wp.0': WP0 + ';66;H', 'wp.1': WP1 + ';64;W', 'optimize' : 'timeWithTraffic', 'key': M_API_KEY}, stream = True)
    map_pil = Image.open(map_res.raw)
    map_tk = ImageTk.PhotoImage(map_pil)
    map_label.config(image=map_tk, text=f'{duration} min   {distance} km', compound='bottom', foreground='white', background='black', font=70)
    map_label.image = map_tk
    map_label.after(1800000, traffic_update)

def simplenote_update():
    sn = simplenote.Simplenote(SN_LOGIN, SN_PASSWORD)
    all = sn.get_note_list(data=True, tags=[])
    notes = ''
    
    for each in all:
        if isinstance(each,int) == True:
            continue
        else:
            for i in each:
                if i['deleted'] == True:
                    continue
                else:
                    notes += i['content'] + '\n'

    simplenote_label.config(text=notes, justify='left', foreground='white', background='black', font=90)
    simplenote_label.after(3600000, simplenote_update)

root = tk.Tk()
root.attributes('-fullscreen', True)
root.config(background='black')
root.bind('<Escape>', lambda e: root.destroy())
f = tk.Frame(root, background='black')

# simplenote

simplenote_label = tk.Label(root)
simplenote_label.pack(side=tk.LEFT, expand=1, fill=tk.Y, anchor=tk.W)
simplenote_update()

#clock

clock = tk.Label(root)
clock.pack(side=tk.LEFT, expand=1, anchor=tk.NW)
clock_update()

f.pack(side=tk.TOP)

#weather

w_img = tk.PhotoImage()
w_logo = tk.Label(f, image=w_img, background='black')
w_logo.pack(expand=1, anchor=tk.NE, side=tk.RIGHT)
w_temp = tk.Label(f)
w_temp.pack(expand=1, anchor=tk.NE, side=tk.RIGHT)
weather_update()

#map(with traffic layer)

map_label = tk.Label(root)
map_label.pack(expand=1, anchor=tk.SE, side=tk.BOTTOM)
traffic_update()

root.mainloop()