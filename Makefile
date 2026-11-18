.PHONY: test build fixtures mac-qa
test:
	python3 -m unittest discover -s tests -v
build:
	python3 tools/build_shortcuts.py
fixtures:
	python3 tools/make_fixtures.py
mac-qa:
	tools/mac_qa.sh
