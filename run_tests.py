import pytest

def run_tests():
    # Run pytest with arguments for coverage, setting the output to XML
    result = pytest.main(["--cov=TESTING", "--cov-report=xml"])

    # Exit with the same code as pytest to signal success/failure
    exit(result)

if __name__ == "__main__":
    run_tests()
