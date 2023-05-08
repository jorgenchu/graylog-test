from flask import Flask, request, render_template
from collections import defaultdict

app = Flask(__name__)
data = defaultdict(lambda: {'numero': 0, 'macs': []})

@app.route('/graylog_alert', methods=['POST'])
def graylog_alert():
    content = request.get_json()
    source = content.get('source')
    event_type = content.get('event_type')
    macs = content.get('mac')

    if source:
        if event_type == 'sta_roam':
            data[source]['numero'] += 1
        elif event_type == 'soft_failure' and data[source]['numero'] > 0:
            data[source]['numero'] -= 1
            if macs in data[source]['macs']:
                data[source]['macs'].remove(macs)

        if macs and macs not in data[source]['macs']:
            data[source]['macs'].append(macs)


    return 'Data received successfully'

@app.route('/')
def index():
    table_rows = [
        {'source': source, 'numero': info['numero']}
        for source, info in data.items()
    ]
    sources = list(data.keys())  # Get the list of available sources
    return render_template('index.html', table_rows=table_rows, sources=sources)

@app.route('/<source>')
def source_page(source):
    macs = data[source]['macs']
    sources = list(data.keys())
    return render_template('sources.html', source=source, macs=macs)

if __name__ == '__main__':
    app.run(debug=True)
