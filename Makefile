.PHONY: install test api frontend bonus headed report allure allure-serve clean

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

allure:
	allure generate reports/allure-results -o reports/allure-report --clean && allure open reports/allure-report

allure-serve:
	allure serve reports/allure-results

clean:
	rm -rf reports
