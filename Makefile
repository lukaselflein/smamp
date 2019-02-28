# Removes old build files, builds new ones and uploads them to pypi
all:	test fix_number clean build upload

test:
	python .test.py

clean:
	rm -rf build dist smamp.egg-info

fix_number:
	python .update_version.py

build:
	python setup.py sdist bdist_wheel

upload:
	python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/* -p unsave_pw_saved_in_plaintext_CdR2amJDlY -u lukaselflein
