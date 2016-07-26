import json
import datetime
import time
import random
import pyglet
import os
import copy
from configparser import ConfigParser
from data import names, postcode
from time import sleep

class PokemonSpider():
    min_interval = 3
    max_interval = 15
    base_url = 'https://pokevision.com/'
    found_list = []

    # get config
    path = os.getcwd()
    configfile = os.path.join(
        path,
        '{}.cfg'.format(os.environ.get('ENVIRONMENT', 'dev'))
    )
    config = ConfigParser(allow_no_value=True)
    config.optionxform = str

    # get sound
    fullpath = os.path.join(path, '6856.wav')
    sound = pyglet.media.load(fullpath, streaming=False)
    player = pyglet.media.Player()

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
                interval = random.uniform( self.min_interval, self.max_interval)

                new_url = '%s/map/data/%f/%f' % \
                          (self.base_url, latlon[0]+lat_adjust, latlon[1]+lon_adjust)
                # print("%s: %s" % (self.get_time_string(), new_url))
                content = self.scraper.get(new_url).content
                self.parse(content)
                sleep(int(interval))

    def check(self, poke):
        self.config.read(self.configfile)
        candidates = self.get_targets('missing') + \
                     self.get_targets('fav') + \
                     self.get_targets('lucky')
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
        except Exception:
            print('%s: unknown error' % self.get_time_string())
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

            # keep found_list short, throw the first 50 if excess 100
            if len(self.found_list) > 100:
                self.found_list = self.found_list[50:]

            self.found_list.append(r['longitude'])

    def prepare_data(self):
        data = self.my_data()
        random.shuffle(data)
        my_dict = {}
        for d in data:
            my_dict[d['code']] = (d['lat'], d['lon'])
        return my_dict

    def get_targets(self, category):
        return json.loads( self.config.get('target', category) )

    def get_time_string(self):
        return datetime.datetime.fromtimestamp(
            time.time()
        ).strftime('%H:%M:%S')

    def my_data(self):
        return postcode

    def get_name(self, number):
        return names.get(number)
