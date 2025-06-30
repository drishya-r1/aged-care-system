@feedback_bp.route('/api/feedback/all', methods=['GET'])
def get_all_feedback():
    import pandas as pd
    import os
    FEEDBACK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/feedback.xlsx')
    if os.path.exists(FEEDBACK_FILE):
        df = pd.read_excel(FEEDBACK_FILE)
        feedback_list = df.fillna('').to_dict(orient='records')
        return jsonify({'feedback': feedback_list})
    else:
        return jsonify({'feedback': []})
