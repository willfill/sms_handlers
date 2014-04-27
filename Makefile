.PHONY: deps clean assets

deps:
	pip install -r requirements.pip

assets:
	./manage.py collectstatic --noinput

clean:
	find . -type f -name "*.py[co]" -delete
