
pip:
	pip install -U -r requirements.txt

test:
	py.test -svx

lint:
	flake8 tunneler
	flake8 tests

clean:
	git clean -fXd
	find . -name \*.pyc -delete
	rm -rf .cache

testpublish:
	python setup.py register -r https://testpypi.python.org/pypi
	python setup.py sdist bdist_wheel --universal upload -r https://testpypi.python.org/pypi

publish:
	python setup.py register
	python setup.py sdist bdist_wheel --universal upload
