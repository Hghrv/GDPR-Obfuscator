# Makefile for automated terraform deployement
.PHONY: project build requirements terraform_step1 terraform_step2 terraform_step3 unit_tests pep8tests Safety clean 
# Running 'make all' will build requirements, then follow terrafom steps, then run tests, then clean
project: build requirements terraform_step1 terraform_step2 terraform_step3 unit_tests pep8tests Safety clean 

build:
	@echo "Building project..."
	python venv venv -m && source venv/bin/activate && export PYTHONPATH=$pwd

requirements: 
	@echo "Installng project requirements"
	pip install requirements.txt
	
terraform_step1: 
	@echo "Initialising modules..."
	cd terraform && terraform init || terraform init -reconfigure

terraform_step2:
	@echo "Running a terraform plan for required resources and permisions..."
	terraform plan

terraform_step3:
@echo "Deploying Lambda handler resources to AWS..."
	terraform apply

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