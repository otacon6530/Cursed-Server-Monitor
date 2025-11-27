import unittest

class LoggerTestResult(unittest.TestResult):
    def __init__(self, logger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger

    def addSuccess(self, test):
        super().addSuccess(test)
        self.logger.debug("PASS: %s", test)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.logger.error("FAIL: %s\n%s", test, self._exc_info_to_string(err, test))

    def addError(self, test, err):
        super().addError(test, err)
        self.logger.error("ERROR: %s\n%s", test, self._exc_info_to_string(err, test))