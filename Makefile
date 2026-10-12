.PHONY: install run test api frontend bonus headed report allure allure-serve clean

install:
	python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && python -m playwright install chromium

test:
	behave

api:
	behave --tags=@api

frontend:
	behave --tags=@frontend

bonus:
	behave --tags=@bonus

headed:
	HEADLESS=false SLOW_MO=300 behave --tags=@frontend

report:
	behave -f html -o reports/report.html

run:
	python run_tests.py

allure:
	python run_tests.py --somente-relatorio

allure-serve:
	python run_tests.py --somente-relatorio --servidor

clean:
	rm -rf reports
