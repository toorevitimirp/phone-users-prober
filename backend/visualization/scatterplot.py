import json
import matplotlib.pyplot as plt
from flask import request
from flask_cors import cross_origin

from etl.data_utils import load_data
from visualization import visual


@visual.route('/scatter', methods=['POST'])
@cross_origin()
def scatter_plot():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        collection = json_data['collection']
        x1 = json_data['feature1']
        x2 = json_data['feature2']

        data_all = load_data(collection)

        grouped = data_all.groupby('label')
        label1_df = grouped.get_group(1)
        label0_df = grouped.get_group(0)
        ax = label0_df.plot.scatter(figsize=(10, 8), x=x1, y=x2, color='b', marker='x', label='label=0')
        label1_df.plot.scatter(figsize=(10, 8), x=x1, y=x2, color='r', marker='+', label='label=1', ax=ax)

        from io import BytesIO
        fig_file = BytesIO()
        plt.savefig(fig_file, format='png')
        fig_file.seek(0)  # rewind to beginning of file
        import base64
        scatter_png = base64.b64encode(fig_file.getvalue())
        return scatter_png