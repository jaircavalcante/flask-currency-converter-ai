from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from src.services.converter import convert, ConversionError

ui_bp = Blueprint('ui', __name__)

@ui_bp.route('/')
def index():
    return render_template('index.html')

@ui_bp.route('/convert', methods=['POST'])
def do_convert():
    data = request.form or request.get_json() or {}
    amount = data.get('amount')
    source = data.get('source')
    target = data.get('target')
    try:
        result = convert(amount, source, target)
    except ConversionError as e:
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify({'error': str(e)}), 400
        return render_template('index.html', error=str(e))

    # If JSON requested
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify(result)

    return render_template('results.html', result=result)

@ui_bp.route('/currencies')
def currencies():
    from config import SUPPORTED_CURRENCIES
    arr = [{'code': c, 'name': c} for c in SUPPORTED_CURRENCIES]
    return jsonify({'currencies': arr})

@ui_bp.route('/rates')
def rates():
    source = request.args.get('source')
    target = request.args.get('target')
    if not source or not target:
        return jsonify({'error': 'source and target required'}), 400
    try:
        from src.services.rate_provider import fetch_rate
        info = fetch_rate(source.upper(), target.upper())
        return jsonify({
            'source': source.upper(),
            'target': target.upper(),
            'rate': info['rate'],
            'isFromCache': info['is_from_cache'],
            'rateTimestamp': info['rate_timestamp'],
            'cachedAt': info['cached_at']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 503
