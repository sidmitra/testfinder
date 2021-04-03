# testfinder - Find tests easier

Command-line tool to find, print all the test cases in a project.


- Find your test methods, class names faster.
- Integrate with other search/filtering/autocomplete tools like bash, grep, fzf.
- Defaults to pytest test invocation syntax.
  -- Other invocation syntax like Django coming soon!

## Install

```shell
pip install testfinder
```

## Usage

```shell
cd <project-root>
testfinder
```

### with fzf
*fzf* is an interactive Unix filter for command-line that can be used with any list and supports fuzzy searches.

- Install [fzf](https://github.com/junegunn/fzf#installation)


- Run pytest and find your test

```bash
pytest $(testfinder | fzf)
```

[![asciicast](https://asciinema.org/a/UxajDsBmyQc0imiiCGzaXd7e8.svg)](https://asciinema.org/a/UxajDsBmyQc0imiiCGzaXd7e8)

# How does it work?
In Python the files containing tests usually have the following naming conventions:

- `tests.py`
- `test_*.py`
- `*_test.py`
- `tests/__init__.py`

It enumerates all the files above, and discovers all the test cases in those files with a few simple regexes.
