import os
from flask import Flask, request, render_template
from subprocess import Popen, PIPE

app = Flask(__name__)


def analyze(source):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
    process = Popen(['python2', main_path],
                    stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate(source)
    return (stdout, True) if process.returncode == 0 else (stderr, False)


def format_output(output):
    mapping = {}
    for line in output.splitlines():
        line_number = int(line.split()[0].split(':')[1])
        line_text = line[line.index(' ')+1:]
        mapping[line_number] = (mapping[line_number] + '; ' + line_text
                                if line_number in mapping else line_text)
    if len(mapping) == 0:
        return 'No errors'
    else:
        result = ''
        max_line = max(mapping.keys())
        for i in range(1, max_line + 1):
            result += mapping.get(i, '') + '\r\n'
        return result


@app.route('/process', methods=['POST'])
def html():
    source = request.form.get('source')
    output, success = analyze(source)
    return format_output(output) if success else (output, 400)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
