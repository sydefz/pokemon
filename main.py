import cfscrape
from pokemon_spider import PokemonSpider


scraper = cfscrape.create_scraper()
print('Starting...')
pokemon_spider = PokemonSpider(scraper)
scraper.get(pokemon_spider.base_url)
print('Warmed up')
pokemon_spider.fetch()