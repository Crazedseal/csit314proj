import requests
from enum import Enum
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import random

class Operation(Enum):
    SINGLE = 0
    AND = 1
    OR = 2
    EXCLUDE = 3

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
    
    @abstractmethod
    def get_header(self):
        pass


class BingContext(SearchContext):
    def __init__(self, header):
        self.header = header
    
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

    def get_header(self):
        return self.header

    def parse_result_into_value(self, result):
        r_pipe = result.replace(' results', '')
        r_pipe = r_pipe.replace(',', '')
        r_pipe = int(r_pipe)
        return r_pipe

class KeywordTest:
    searchWord = ""
    altWord = ""
    result = {}
    cancel = False
    def __init__(self, search, alt, s_context):
        self.searchWord = search
        self.altWord = alt
        self.context = s_context
        self.result = { }
        self.cancel = False
        return

    def do_single_search(self):
        single_page = requests.get(self.context.get_url(), params = {self.context.get_param(): self.searchWord},
                                   headers = self.context.get_header())
        soup = BeautifulSoup(single_page.text, 'html.parser')
        s_result = soup.find(self.context.get_element_type(),{self.context.get_selector_type():self.context.get_selector()})
        if (s_result == None):
            self.cancel = True
            print("Fail [" + self.searchWord + "] on single search")
            return
        self.result[Operation.SINGLE] = self.context.parse_result_into_value(s_result.text)
        return

    def do_and_search(self):
        and_page = requests.get(self.context.get_url(), params = {self.context.get_param(): self.searchWord + " " + self.altWord},
                                headers = self.context.get_header())
        soup = BeautifulSoup(and_page.text, 'html.parser')
        s_result = soup.find(self.context.get_element_type(),{self.context.get_selector_type():self.context.get_selector()})
        if (s_result == None):
            self.cancel = True
            print("Fail [" + self.searchWord + "] on and search")
            return
        self.result[Operation.AND] = self.context.parse_result_into_value(s_result.text)
        return

    def do_or_search(self):
        or_page = requests.get(self.context.get_url(), params = {self.context.get_param(): self.searchWord + " | " + self.altWord},
                               headers = self.context.get_header())
        soup = BeautifulSoup(or_page.text, 'html.parser')
        s_result = soup.find(self.context.get_element_type(),{self.context.get_selector_type():self.context.get_selector()})
        if (s_result == None):
            self.cancel = True
            print("Fail [" + self.searchWord + "] on or search")
            return
        self.result[Operation.OR] = self.context.parse_result_into_value(s_result.text)
        return

    def do_exclude_search(self):
        exclude_page = requests.get(self.context.get_url(), params = {self.context.get_param(): self.searchWord + " -" + self.altWord},
                                    headers = self.context.get_header())
        soup = BeautifulSoup(exclude_page.text, 'html.parser')
        s_result = soup.find(self.context.get_element_type(),{self.context.get_selector_type():self.context.get_selector()})
        if (s_result == None):
            self.cancel = True
            print("Fail [" + self.searchWord + "] on exclude search")
            return
        self.result[Operation.EXCLUDE] = self.context.parse_result_into_value(s_result.text)
        return

    def do_search(self):
        self.do_single_search()
        if self.cancel:
            return
        self.do_and_search()
        if self.cancel:
            return
        self.do_or_search()
        if self.cancel:
            return
        self.do_exclude_search()
        return
    

def get_word_list(filename):
    file = open(filename, "r")
    word_list = []
    for line in file:
        word_list.append(line.strip())

    return word_list

# Module Testing
def test_bing_context():
    b_context = BingContext()
    assert b_context
    assert b_context.get_element_type() == 'span'
    assert b_context.get_selector_type() == 'class'
    assert b_context.get_selector() == 'sb_count'
    assert b_context.parse_result_into_value('565,000,000 results') == 565000000
    return

def test_word_list_load():
    words = get_word_list('google-10000-english-usa-no-swears-medium.txt')
    assert words

# Running
if __name__ == "__main__":
    # Grab these from your browser?
    
    run_count = 0
    # Run count input prompt
    while True:
        run_count = -1
        try:
            run_count = int(input('run count: '))
            if (run_count > 0):
                break
        except:
            print('Ensure that the number you input is a positive non-zero integer!')


    print('Run Count selected -> ' + str(run_count))

    
    word_list_file = ""
    # Word List file prompt
    while True:
        print("Enter the word file name below or default for google-10000-english-usa-no-swears-medium.txt")
        word_list_file_hold = input('word file: ')
        if (word_list_file_hold == "default"):
            word_list_file = 'google-10000-english-usa-no-swears-medium.txt'
            break
        try:
            fOp = open(word_list_file_hold, "r")
            assert fOp
            fOp.close()
            word_list_file = word_list_file_hold
            break
        except:
            print('Ensure that the file exists and can be read!')
            
        
    # Input for cookie and Agent
    cookie = input('cookie: ')
    agent = input('agent: ')
    header = { 'user-agent': agent, 'cookie': cookie }
    # Result breakdown data structure.
    result_breakdown = { Operation.AND: { 'success': 0, 'fail': 0 }, Operation.OR: { 'success': 0, 'fail': 0 }, Operation.EXCLUDE: { 'success': 0, 'fail': 0 } }
    
    #test_bing_context()
    # Construct a BingContext
    bingContext = BingContext(header)
    word_list = get_word_list(word_list_file)
    word_set = { }

    # Test if the word list is sufficient size for the run count.
    if (len(word_list)/2 < run_count):
        print('Amount of words in word set ' + str(len(word_list)) + ' insufficient for run count ' + str(run_count))
        assert len(word_list)/2 > run_count


    # Begin testing.
    keywordTests = []
    for num in range(0, run_count):
        rand = random.randint(0, len(word_list)-1) # Get a random word.
        print(num)
        counter = 0
        # Select our first word.
        while rand in word_set:
            rand = random.randint(0, len(word_list)-1)
            counter = counter + 1
            if counter > 10000: 
                break
        
        # Select our second word.
        altrand = random.randint(0, len(word_list)-1)
        while (altrand == num) or (altrand in word_set):
            altrand = random.randint(0, len(word_list)-1)

        # Do the test.
        currentTest = KeywordTest(word_list[rand], word_list[altrand], bingContext)
        currentTest.do_search()

        # Print for both debugging and proper runtime purposes.
        print(currentTest.__dict__)
        
        if not currentTest.cancel:
            # If the test was not cancelled, conduct analysis of current result.
            if (currentTest.result[Operation.AND] > currentTest.result[Operation.SINGLE]):
                result_breakdown[Operation.AND]['fail'] += 1
            else:
                result_breakdown[Operation.AND]['success'] += 1

            if (currentTest.result[Operation.OR] > currentTest.result[Operation.SINGLE]):
                result_breakdown[Operation.OR]['success'] += 1
            else:
                result_breakdown[Operation.OR]['fail'] += 1

            if (currentTest.result[Operation.EXCLUDE] > currentTest.result[Operation.SINGLE]):
                result_breakdown[Operation.EXCLUDE]['fail'] += 1
            else:
                result_breakdown[Operation.EXCLUDE]['success'] += 1

        keywordTests.append(currentTest)
        # Print our current result breakdown.
        print(result_breakdown)

    with open('output.txt', mode='w') as f_out:
        assert f_out
        for test in keywordTests:
            f_out.write(str(test.__dict__) + '\n')

        f_out.write(str(result_breakdown) + '\n')
    
    # Program is over. However this is to keep the window open.    
    input('Press Enter to Exit.')
            
            

        
        
        
