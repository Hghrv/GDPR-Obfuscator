
# Makefile for automated terraform deployement
.PHONY: project build requirements unit_tests pep8tests Safety clean 
# Running 'make all' will build requirements, then follow terrafom steps, then run tests, then clean
project: build requirements unit_tests safety pep8tests  clean 

build:
	@echo "Building project..."
	python -m venv venv
	@echo "Activating virtual environment..."
	. venv/bin/activate 
	@echo "Exporting pythonpath..."
	export PYTHONPATH=$(PWD)
requirements: 
	@echo "Installng project requirements"
	pip install -r requirements.txt
	
unit_tests:
	@echo "Running unit-tests with pytest modules..."
	pytest -vvvrp

safety: 
	@echo "Running Safety tests..."
	safety scan

pep8tests: 
	@echo "Running PEP8 compliance tests..."
	pytest --cov=. --cov-report=term-missing && flake8 .

clean:
	@echo "Cleaning up..."
	rm -f *.o my_executable