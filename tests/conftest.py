import pytest
from .util import load_mockup


@pytest.fixture
def brawlers_html():
    return load_mockup("brawlers.html")


@pytest.fixture
def brawler_html():
    return load_mockup("brawler.html")
