import json
import matplotlib.pyplot as plt
from flask import request
from flask_cors import cross_origin

from etl.data_utils import load_data
from visualization import visual


@visual.route('/pie', methods=['POST'])
@cross_origin()
def pie_plot():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        collection = json_data['collection']
        feature = json_data['feature']

        data_all = load_data(collection)
        bin_label = ['0', '1']
        df = data_all[feature].value_counts()
        size_0 = df[0]
        size_1 = df[1]
        sizes = [size_0, size_1]
        plt.figure(figsize=(10,8))
        plt.pie(sizes, labels=bin_label, autopct='%1.1f%%')
        plt.title(feature + '\nlabel=0,1')

        from io import BytesIO
        fig_file = BytesIO()
        plt.savefig(fig_file, format='png')
        fig_file.seek(0)  # rewind to beginning of file
        import base64
        pie_png = base64.b64encode(fig_file.getvalue())
        return pie_png
