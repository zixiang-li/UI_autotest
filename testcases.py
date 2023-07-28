import pytest
# 读取用例
import yaml
from playwright.sync_api import sync_playwright
import time

f = open('testcase.yaml', mode='r')
case_dict = yaml.safe_load(f)
print(case_dict)


class Test_Console:


    def run_step(self, func, value):
        """显示每一步执行了什么关键字以及具体的参数是什么"""
        func(*value)

    def run_case(self, POCcases):

        # 获取所有的测试用例
        cases = POCcases['cases']

        try:
            # 遍历获取到的测试用例
            for case in cases:
                func = self.page.__getattribute__(case['method'])
                # 获取参数
                caselist = list(case.values())
                self.run_step(func, caselist[2:])
                print(type(caselist[2:]))


        except Exception:
            pytest.fail('用例执行失败')

    def setup_class(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        time.sleep(3)




    # 利用pytest做个参数化
    @pytest.mark.parametrize('POCcases', case_dict['loginpage'])
    def test_login(self, POCcases):
        self.run_case(POCcases)
        self.page.wait_for_timeout(3000)

    def tearDown_class(self):
        self.browser.close()
        self.playwright.stop()


