import unittest
from tests.test_employee_management import TestEmployeeManagement

if __name__ == "__main__":
    # Create a test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestEmployeeManagement)
    
    # Run the test suite
    unittest.TextTestRunner(verbosity=2).run(test_suite)