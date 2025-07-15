from flask import Flask, render_template, request, jsonify
from mpin_analyzer import MPINAnalyzer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    mpin = data.get('mpin', '')
    pin_length = len(mpin)
    
    if pin_length not in (4, 6):
        return jsonify({
            'valid': False,
            'strength': 'INVALID',
            'reasons': ['INVALID_LENGTH']
        })
    
    analyzer = MPINAnalyzer(pin_length)
    demographics = data.get('demographics', {})
    
    # Clean date formats
    for field in ['user_dob', 'spouse_dob', 'anniversary']:
        if field in demographics:
            demographics[field] = ''.join(c for c in demographics[field] if c.isdigit())
    
    result = analyzer.analyze(mpin, demographics)
    return jsonify(result)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    pin_length = data.get('pin_length', 4)
    
    if pin_length not in (4, 6):
        return jsonify({'error': 'Invalid PIN length'}), 400
    
    analyzer = MPINAnalyzer(pin_length)
    pin = analyzer.generate_strong_pin()
    return jsonify({'pin': pin})

if __name__ == '__main__':
    app.run(debug=True)