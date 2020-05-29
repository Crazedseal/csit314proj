import requests
from enum import Enum
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

class Operation(Enum):
    SINGLE = 0
    AND = 1
    OR = 2
    EXCLUDE = 3

# bing class="sb_count"
#x = requests.get('https://www.bing.com/search', params = {"q": "wikipedia"})

class SearchContext(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def get_element_type(self):
        pass

    @abstractmethod
    def get_selector_type(self):
        pass

    @abstractmethod
    def get_selector(self):
        pass

    @abstractmethod
    def get_url(self):
        pass

    @abstractmethod
    def get_param(self):
        pass

    @abstractmethod
    def parse_result_into_value(self, result):
        pass


class BingContext(SearchContext):
    def get_element_type(self):
        return 'span'

    def get_selector_type(self):
        return 'class'

    def get_selector(self):
        return 'sb_count'

    def get_url(self):
        return 'https://www.bing.com/search'

    def get_param(self):
        return 'q'

    def parse_result_into_value(self, result):
        r_pipe = result.replace('<span class="sb_count">', '')
        r_pipe = r_pipe.replace(' results</span>', '')
        r_pipe = r_pipe.replace(',', '')
        r_pipe = int(r_pipe)
        return r_pipe

class KeywordTest:
    searchWord = ""
    altWord = ""
    result = {}
    def __init__(self, search, alt, s_context):
        self.SearchWord = search
        self.AltWord = alt
        self.context = s_context
        return

    def do_single(self):
        single_page = requests.get(self.context.get_url(), params = {self.context.get_param(): self.searchWord})
        soup = BeautifulSoup(single_page.text)
        s_result = soup.find(self.context.get_element_type(),{self.context.context.get_selector_type():self.context.get_selector()})
        result[Operation.SINGLE] = self.context.parse_result_into_value(s_result)
        return

    
    def do_search(self):
        do_single()
        return

# Module Testing
def test_bing_context():
    b_context = BingContext()
    assert b_context
    assert b_context.get_element_type() == 'span'
    assert b_context.get_selector_type() == 'class'
    assert b_context.get_selector() == 'sb_count'
    assert b_context.parse_result_into_value('<span class="sb_count">565,000,000 results</span>') == 565000000
    return

# Running
if __name__ == "__main__":
    test_bing_context()
