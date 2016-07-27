import cfscrape
from pokemon_spider import PokemonSpider

scraper = cfscrape.create_scraper()
print('Warming up')
pokemon_spider = PokemonSpider(scraper)
scraper.get(pokemon_spider.base_url)
print('Searching...')
pokemon_spider.fetch()
