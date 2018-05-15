.PHONY: clean
clean:
	rm -rf `find . -name "__pycache__"`
	rm -rf .eggs/ build/ dist/

.PHONY: build
build: clean
	python3 setup.py py2app
	open ./dist/

.PHONY: run
run:
	clear && python3 urstatus/app.py