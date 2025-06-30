from flask import Blueprint, jsonify
from backend.database import excel_manager
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/api/analytics/alerts_weekly', methods=['GET'])
def alerts_weekly():
    alerts = excel_manager.read_all_alerts() or []
    # Use 'timestamp' field, extract date part (YYYY-MM-DD)
    today = datetime.today().date()
    week_ago = today - timedelta(days=6)
    # Count alerts per day for the last 7 days
    counts = {}
    for i in range(7):
        day = week_ago + timedelta(days=i)
        counts[day.strftime('%Y-%m-%d')] = 0
    for alert in alerts:
        ts = alert.get('timestamp')
        if ts:
            try:
                # Support both ISO and date-only
                d = datetime.fromisoformat(str(ts)[:10]).date() if 'T' in str(ts) else datetime.strptime(str(ts)[:10], '%Y-%m-%d').date()
                if week_ago <= d <= today:
                    counts[d.strftime('%Y-%m-%d')] += 1
            except Exception:
                continue
    # Return as list of {date, count}
    result = [{'date': d, 'count': counts[d]} for d in sorted(counts.keys())]
    return jsonify({'weekly_alerts': result})
