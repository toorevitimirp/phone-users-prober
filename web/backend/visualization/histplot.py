import json
import matplotlib.pyplot as plt
from flask import request
from flask_cors import cross_origin

from etl.data_utils import load_data
from visualization import visual


@visual.route('/hist', methods=['POST'])
@cross_origin()
def hist_plot():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        collection = json_data['collection']
        feature = json_data['feature']

        data = load_data(collection)
        grouped = data.groupby('label')
        label1_df = grouped.get_group(1)
        label0_df = grouped.get_group(0)

        plt.figure(figsize=(10, 7))
        plt.suptitle(feature, fontsize=14)

        plt.subplot(211)
        label0_df[feature].plot(kind='hist')
        plt.xlabel('label=0')

        plt.subplot(212)
        label1_df[feature].plot(kind='hist')
        plt.xlabel('label=1')

        from io import BytesIO
        fig_file = BytesIO()
        plt.savefig(fig_file, format='png')
        fig_file.seek(0)  # rewind to beginning of file
        import base64
        hist_png = base64.b64encode(fig_file.getvalue())
        return hist_png
