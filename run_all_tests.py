import unittest

# 모든 테스트 자동 발견
loader = unittest.TestLoader()
suite = loader.discover("tests", pattern="test_*.py")

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
