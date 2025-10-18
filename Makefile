# Makefile for automated terraform deployement
.PHONY: all build test clean
# Running 'make all' will build requirements, then follow terrafom steps, then run tests, then clean
all: build requirements terraform_step1 terraform_step2 terraform_step3 unit_tests pep8tests Safety clean 

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
	pytest -vvvrp

pep8tests: 
	@echo "Running PEP8 compliance tests..."
	pytest --cov=. --cov-report=term-missing && flake8 ."

safety: 
	@echo "Running Safety tests..."
	safety scan

clean:
	@echo "Cleaning up..."
	# put your clean commands here

# Makefile for automated terraform deployement
Requirements: pip install requirements.txt
RunRequirements: Requirements

UnitTests: pytest -vvvrp
RunUnitTests: make UnitTests

PEP8Tests: pytest --cov=. --cov-report=term-missing && flake8 ."
RunPEP8Tests: make PEP8Tests

Safety: safety scan
RunSafetyTest: Safety

TfInit: cd terraform && terraform init || terraform init -reconfigure
TfPlan: terraform plan
TfApply: terraform apply
RunTf: TfInit TfPlan TfApply
