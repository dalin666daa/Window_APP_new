class TestsManager:
    def __init__(self):
        self.tests = []

    def add_test(self, test_info):
        self.tests.append(test_info)

    def get_tests(self):
        return self.tests
