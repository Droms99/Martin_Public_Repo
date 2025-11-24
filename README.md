Testing with copilot
====================

Summary
-------
This repository contains a small finance utility (`finance.py`) and a test suite (`test_finance.py`) used to validate its functions. I created a set of 15 unit tests grouped into three test classes to cover the three public functions: `calculate_compound_interest`, `calculate_annuity_payment`, and `calculate_internal_rate_of_return`.

What I did
----------
- Added 15 unit tests in `test_finance.py` (5 tests per class) to exercise normal inputs, boundary cases and unexpected inputs.
- Refactored tests to reuse shared data via class-scoped pytest fixtures (reduces duplication and clarifies setup/teardown).
- Adjusted one assertion (IRR test) to validate correctness by checking the resulting NPV rather than a single hard-coded numeric root — this makes the test robust to numerical differences while still ensuring correctness.
- Ran the full test suite with coverage and confirmed 100% coverage for `finance.py`.

Challenges and how they were solved
----------------------------------
During the task I iteratively improved the tests to make them robust and maintainable. Highlights from the conversation and work:

- Initially I wrote a simple set of tests and ran them. One IRR test failed because it compared the computed rate to a single expected numeric value; the implementation's Newton–Raphson result differed slightly. To solve this I changed the test to assert that the Net Present Value (NPV) at the computed IRR is approximately zero — this verifies correctness without depending on a specific numeric root.

- I added class-level setup/teardown logic. At first I used `setup_class` / `teardown_class` methods, then converted to pytest fixtures (`@pytest.fixture(scope="class")`) with `autouse=True` injection so tests could access shared data through `self`. Fixtures provide better integration with pytest and are more flexible for future reuse.

- I kept the tests strict where behavior is well-defined (for example, `ZeroDivisionError` for zero periods) and allowed numeric tolerance for floating-point comparisons using `pytest.approx`.

These improvements were made across several iterations to keep the test count at 15 while increasing robustness and coverage.

Final metrics
-------------
- Unit tests created: 15
- Coverage for `finance.py`: 100% (statements and branches)

How to run the tests and coverage
---------------------------------
1. (Optional) create and activate a virtual environment.
2. Install requirements and tools:

```cmd
python -m pip install -r requirements.txt
python -m pip install coverage
```

3. Run tests with pytest:

```cmd
python -m pytest -q
```

4. Run coverage and generate a report and HTML output:

```cmd
python -m coverage run -m pytest
python -m coverage report -m
python -m coverage html
```

Open `htmlcov/index.html` in your browser to see the HTML coverage report.

Notes and next steps
--------------------
- If you prefer fixtures over class-level injection, I can convert tests to use shared fixtures directly as function arguments and add parametrized tests to reduce duplication while keeping the total tests at 15.
- I can also add a short `Makefile` or `scripts` section in this README to simplify running tests and coverage for other contributors.

If you want, I can commit these changes and generate the `coverage html` output here and attach the `htmlcov` directory snapshot.

