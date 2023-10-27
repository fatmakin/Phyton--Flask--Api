from flask import Flask, request, jsonify

app = Flask(__name__)

# Örnek veri seti
data = [
    {"main.uploaded_variation": "variation_1", "main.existing_variation": "existing_1", "main.symbol": "symbol_1", "main.af_vcf": 0.2, "main.dp": 30, "details2.dann_score": 3.5, "links.mondo": "link1", "links.pheno_pubmed": "link2", "details2.provean": "detail1"},
    {"main.uploaded_variation": "variation_2", "main.existing_variation": "existing_2", "main.symbol": "symbol_2", "main.af_vcf": 0.4, "main.dp": 25, "details2.dann_score": 2.5, "links.mondo": "link3", "links.pheno_pubmed": "link4", "details2.provean": "detail2"},
    # Ek veri satırları buraya eklenebilir
]

@app.route('/assignment/query', methods=['GET', 'POST'])
def query_records():
    if request.method == 'GET':
        try:
            page = int(request.args.get('page', 1))
            page_size = int(request.args.get('page_size', 10))

            filters = request.args.to_dict()
            ordering = []

            filtered_data = data
            for column, value in filters.items():
                filtered_data = [d for d in filtered_data if d.get(column) == value]

            start = (page - 1) * page_size
            end = start + page_size
            paginated_data = filtered_data[start:end]

            return jsonify({
                "page": page,
                "page_size": page_size,
                "count": len(filtered_data),
                "results": paginated_data
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 400

    elif request.method == 'POST':
        try:
            page = int(request.args.get('page', 1))
            page_size = int(request.args.get('page_size', 10))

            request_data = request.get_json()

            filters = request_data.get('filters', {})
            ordering = request_data.get('ordering', [])

            filtered_data = data
            for column, value in filters.items():
                filtered_data = [d for d in filtered_data if d.get(column) == value]

            for order in ordering:
                column = next(iter(order))
                direction = order[column]
                reverse = direction == "DESC"
                filtered_data = sorted(filtered_data, key=lambda k: k[column], reverse=reverse)

            start = (page - 1) * page_size
            end = start + page_size
            paginated_data = filtered_data[start:end]

            return jsonify({
                "page": page,
                "page_size": page_size,
                "count": len(filtered_data),
                "results": paginated_data
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
