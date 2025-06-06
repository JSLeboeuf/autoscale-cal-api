 from flask import Flask, request, jsonify
  from flask_cors import CORS
  import requests
  import os
  from datetime import datetime

  app = Flask(__name__)
  CORS(app)

  CAL_API_KEY = os.environ.get('CAL_API_KEY', 'cal_live_e7f24f1eab131ba927de8e70b8912da1')
  CAL_EVENT_TYPE_ID = os.environ.get('CAL_EVENT_TYPE_ID', '2575862')

  @app.route('/')
  def home():
      return jsonify({'message': 'Autoscale AI running'})

  @app.route('/health')
  def health():
      return jsonify({'status': 'healthy'})

  @app.route('/check-availability', methods=['POST'])
  def check_availability():
      try:
          data = request.json
          response = requests.get(
              "https://api.cal.com/v1/availability",
              params={
                  'eventTypeId': CAL_EVENT_TYPE_ID,
                  'startTime': data.get('dateFrom'),
                  'endTime': data.get('dateTo')
              },
              headers={'Authorization': f'Bearer {CAL_API_KEY}'}
          )

          slots = response.json().get('slots', [])[:5]
          formatted = []
          for slot in slots:
              dt = datetime.fromisoformat(slot['time'].replace('Z', '+00:00'))
              formatted.append({
                  'datetime': slot['time'],
                  'display': dt.strftime('%A, %B %d at %I:%M %p')
              })

          return jsonify({
              'success': True,
              'slots': formatted,
              'message': f"I have {len(formatted)} slots available."
          })
      except:
          return jsonify({
              'success': False,
              'message': "Let me send you: cal.com/autoscaleai/ai-demo"
          })

  @app.route('/create-booking', methods=['POST'])
  def create_booking():
      try:
          data = request.json
          response = requests.post(
              'https://api.cal.com/v1/bookings',
              json={
                  'eventTypeId': int(CAL_EVENT_TYPE_ID),
                  'start': data['datetime'],
                  'responses': {
                      'name': data['name'],
                      'email': data['email'],
                      'phone': data.get('phone', '')
                  },
                  'timeZone': 'America/New_York'
              },
              headers={'Authorization': f'Bearer {CAL_API_KEY}'}
          )

          return jsonify({
              'success': True,
              'message': f"Demo booked! Check {data['email']}"
          })
      except:
          return jsonify({
              'success': False,
              'message': "Use: cal.com/autoscaleai/ai-demo"
          })

  if __name__ == '__main__':
      port = int(os.environ.get('PORT', 8080))
      app.run(host='0.0.0.0', port=port)
