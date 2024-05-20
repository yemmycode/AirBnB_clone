#!/usr/bin/python3
"""
W3C Validator for Holberton School

Validates HTML and CSS files using two APIs:

- https://validator.w3.org/nu/
- http://jigsaw.w3.org/css-validator/validator

Usage:

To validate a single file:

./w3c_validator.py index.html

To validate multiple files:


All errors are printed to `STDERR`.

Return:
Exit status is the number of errors found, 0 on success.

References:

https://developer.mozilla.org/en-US/
"""
import sys
import requests


def print_stdout(msg):
    """Print message to STDOUT"""
    sys.stdout.write(msg)


def print_stderr(msg):
    """Print message to STDERR"""
    sys.stderr.write(msg)


def analyze_html(file_path):
    """Analyze HTML file"""
    headers = {'Content-Type': "text/html; charset=utf-8"}
    data = open(file_path, "rb").read()
    url = "https://validator.w3.org/nu/?out=json"
    response = requests.post(url, headers=headers, data=data)
    results = []
    messages = response.json().get('messages', [])
    for message in messages:
        results.append("[{}:{}] {}".format(file_path, message['lastLine'], message['message']))
    return results


def analyze_css(file_path):
    """Analyze CSS file"""
    data = {'output': "json"}
    files = {'file': (file_path, open(file_path, 'rb'), 'text/css')}
    url = "http://jigsaw.w3.org/css-validator/validator"
    response = requests.post(url, data=data, files=files)
    results = []
    errors = response.json().get('cssvalidation', {}).get('errors', [])
    for error in errors:
        results.append("[{}:{}] {}".format(file_path, error['line'], error['message']))
    return results


def analyze(file_path):
    """Analyze a file and print the results"""
    error_count = 0
    try:
        if file_path.endswith('.css'):
            results = analyze_css(file_path)
        else:
            results = analyze_html(file_path)

        if results:
            for msg in results:
                print_stderr("{}\n".format(msg))
                error_count += 1
        else:
            print_stdout("{}: OK\n".format(file_path))

    except Exception as e:
        print_stderr("[{}] {}\n".format(e.__class__.__name__, e))
    return error_count


def files_loop():
    """Loop through each input file and analyze"""
    total_errors = 0
    for file_path in sys.argv[1:]:
        total_errors += analyze(file_path)

    return total_errors


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_stderr("Usage: w3c_validator.py file1 file2 ...\n")
        exit(1)

    # Execute tests and exit with the number of errors as the status code
    sys.exit(files_loop())

