# Removes old build files, builds new ones and uploads them to pypi
all:	test docs fix_number clean build upload git

test:
	python .test.py

docs:
	rm docs/*html
	pdocs3 --html smamp
	mv html/smamp/*.html docs/
	rm -r html

clean:
	rm -rf build dist smamp.egg-info

fix_number:
	python .update_version.py

build:
	python setup.py sdist bdist_wheel

upload:
	python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/* -p unsave_pw_saved_in_plaintext_CdR2amJDlY -u lukaselflein

git:
	git pull
	git add .
	git commit -m 'auto update'
	git push


