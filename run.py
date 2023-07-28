import yaml
from playwright.sync_api import sync_playwright
from time import sleep
import pyaml
import pytest

# with open('data.yaml', 'r') as f:
#     r = yaml.safe_load(f)
#
#     print(r['Cases'])
#     for cases in r['Cases']:
#         for case in cases['cases']:
#             print(case)



class Test_case():
    with open('data.yaml', 'r') as f:
        r = yaml.safe_load(f)
        print(r)

    def setup_class(self):
        self.browser = sync_playwright().start().chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        return {'browser': self.browser, 'context': self.context, 'page': self.page}

    def step(self, case):
        print(case)
        self.page.__getattribute__(case['method'])(*list(case.values())[3:-1])

    def swith_page(self, case):
        with self.context.expect_page() as new_page_info:
            print(case)
            self.page.__getattribute__(case['method'])(*list(case.values())[3:-1])
        global new_page
        new_page = new_page_info.value
    def new_page(self, case):
        print(case)
        new_page.__getattribute__(case['method'])(*list(case.values())[3:-1])


    def run(self, Cases):
        for case in Cases['cases']:
            if case['page'] == 1:
                self.step(case)
            elif case['page'] == 2:
                self.swith_page(case)
            else:
                self.new_page(case)
            sleep(3)

    @pytest.mark.parametrize('Cases', r['Cases'])
    def test_run(self, Cases):
        self.run(Cases)


