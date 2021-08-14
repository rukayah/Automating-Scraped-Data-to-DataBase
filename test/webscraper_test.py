from pandas.core.frame import DataFrame
from src.scraper import Webscraping


def test_extract():
    data = Webscraping()
    assert len(data.extract(300,"dress")) == 300
    #assert data.extract(300,"dress") == DataFrame
