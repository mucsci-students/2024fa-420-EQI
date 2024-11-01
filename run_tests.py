import pytest
import coverage

def run_tests():
    # Start coverage analysis
    cov = coverage.Coverage()
    cov.start()

    # Run pytest with arguments to produce an XML report
    result = pytest.main(["--cov=TESTING", "--cov-report=xml"])

    # Stop and save coverage data
    cov.stop()
    cov.save()

    # Exit with the same code as pytest to signal success/failure
    exit(result)

if __name__ == "__main__":
    run_tests()
