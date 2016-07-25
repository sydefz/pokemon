import scrapy
import json
import datetime
import time
import random
import pyglet
import logging
import os
import copy
from data import names, postcode
from time import sleep

class PokemonSpider():
    min_interval = interval = 10
    base_url = 'https://pokevision.com/'
    path = os.getcwd()
    fullpath = os.path.join(path, '6856.wav')
    sound = pyglet.media.load(fullpath, streaming=False)
    player = pyglet.media.Player()
    found_list = []

    def __init__(self, scraper):
        self.scraper = scraper

    def fetch(self):
        original_dict = self.prepare_data()
        # repeat scan all sydney suburbs
        for i in range(9999):
            my_dict = copy.copy(original_dict)
            # randomly pass 20 items on each scan
            for _ in range(20):
                key = random.choice(list(my_dict))
                my_dict.pop( key )

            for _ in range(len(my_dict)):
                latlon = my_dict.pop( random.choice(list(my_dict)) )
                lat_adjust = random.uniform(-0.0125, 0.0125)
                lon_adjust = random.uniform(-0.0125, 0.0125)
                
                new_url = '%s/map/data/%f/%f' % \
                          (self.base_url, latlon[0]+lat_adjust, latlon[1]+lon_adjust)
                print("%s: %s" % (self.get_time_string(), new_url))
                content = self.scraper.get(new_url).content
                self.parse(content)
                sleep(self.interval)
                # yield scrapy.Request(response.urljoin(new_url), self.parse_titles)

    def check(self, poke):
        candidates = self.get_fav() + self.get_missing() + self.get_impossible()
        if poke['pokemonId'] in candidates and poke['is_alive']:
            if poke['expiration_time'] - 300 > time.time():
                return True
        return False

    def parse(self, content):
        try:
            rawdata = content.decode("ascii")
            data = json.loads(rawdata)
        except UnicodeDecodeError:
            print('%s: invalid response' % self.get_time_string())
            return

        result = [p for p in data['pokemon'] if self.check(p)]

        for r in result:
            # id is not unique, uid is not unique
            # fine... longitude must be unique
            if r['longitude'] in self.found_list:
                continue
            
            self.player.pause()
            self.player.delete()
            self.player.queue(self.sound)
            self.player.play()

            wanted = {'#': r['pokemonId'], 'lat': r['latitude'], 'lon': r['longitude']}
            print('%s: Found #%d %s, lat %f and lon %f, despawn in %d sec' % \
                  (
                    self.get_time_string(),
                    r['pokemonId'],
                    self.get_name(r['pokemonId']),
                    r['latitude'],
                    r['longitude'],
                    r['expiration_time'] - time.time()
                  )
              )

            # keep found_list short, throw the first 5 if excess 10
            if len(self.found_list) > 10:
                self.found_list = self.found_list[5:]

            self.found_list.append(r['longitude'])
            # yield wanted

    def prepare_data(self):
        data = self.my_data()
        random.shuffle(data)
        my_dict = {}
        for d in data:
            my_dict[d['code']] = (d['lat'], d['lon'])
        return my_dict

    def get_missing(self):
        return [68, 76, 89, 94, 141]

    def get_fav(self):
        return [143, 134, 149, 131, 76, 9]
        # 80

    def get_impossible(self):
        return [150, 151, 144, 145, 146, 132, 128, 83]
        # 122

    def get_time_string(self):
        return datetime.datetime.fromtimestamp(
            time.time()
        ).strftime('%H:%M:%S')

    def my_data(self):
        return postcode

    def get_name(self, number):
        return names.get(number)