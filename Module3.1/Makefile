# Makefile

# Define variables for country name, start date, and end date
COUNTRY_NAME := $(shell read -p "Enter country name: " COUNTRY_NAME; echo $$COUNTRY_NAME)
START_DATE := $(shell read -p "Enter start date (DD-MM-YYYY): " START_DATE; echo $$START_DATE)
END_DATE := $(shell read -p "Enter end date (DD-MM-YYYY): " END_DATE; echo $$END_DATE)

query2:
	python3 mapper2.py "$(COUNTRY_NAME)" "$(START_DATE)" "$(END_DATE)" | python3 combiner2.py | python3 reducer2.py

query1:
	python3 mapper1.py "$(COUNTRY_NAME)" | python3 reducer1.py
