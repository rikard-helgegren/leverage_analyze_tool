
all: src/compiled_code info_run

debug: src/compiled_code debug_run

info: src/compiled_code info_run

trace: src/compiled_code trace_run

clean:
	rm -rf src/compiled_code

src/compiled_code:
	mkdir src/compiled_code
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$0/model
	python3 src/setup.py

run:
	python3 leverage_analysis_tool.py

debug_run:
	python3 leverage_analysis_tool.py debug

info_run:
	python3 leverage_analysis_tool.py info

trace_run:
	python3 leverage_analysis_tool.py trace

test: pytest cpp_test

pytest:
	pytest -v tests/set_path_for_import.py tests/

pytest_debug:
	pytest --pdb -v tests/set_path_for_import.py tests/

cpp_test:
	g++  -std=c++11 tests/runAllCppTests.cpp -o tests.out && ./tests.out

install:
	sudo apt install python3-pip
	sudo pip install pytest
	apt install xsel
	apt install xclip

	pip install -r requirements.txt