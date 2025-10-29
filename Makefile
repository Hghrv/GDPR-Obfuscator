# Makefile for automated terraform deployement
.PHONY: project build requirements unit_tests pep8tests Safety clean 
# Running 'make all' will build requirements, then follow terrafom steps, then run tests, then clean
project: build requirements unit_tests pep8tests Safety clean 

build:
	@echo "Building project..."
	python venv venv -m && source venv/bin/activate && export PYTHONPATH=$pwd

requirements: 
	@echo "Installng project requirements"
	pip install -r requirements.txt
	
unit_tests:
	@echo "Running unit-tests with pytest modules..."
	cd .. || pytest -vvvrp

pep8tests: 
	@echo "Running PEP8 compliance tests..."
	pytest --cov=. --cov-report=term-missing && flake8 .

safety: 
	@echo "Running Safety tests..."
	safety scan

clean:
	@echo "Cleaning up..."
	rm -f *.o my_executable