from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def render_main():
    return render_template('index.html')

@app.route('/goals/<goal>/')
def render_goal(goal):
    return render_template('goal.html')

@app.route('/profiles/<id_teacher>/')
def render_profiles(id_teacher):
    return render_template('profile.html')

@app.route('/request/')
def render_request():
    return render_template('request.html')

@app.route('/request_done/')
def render_request_done():
    return render_template('request_done.html')

@app.route('/booking/<id_teacher>/<day>/<time>/')
def render_booking(id_teacher, day, time):
    return render_template('booking.html')

@app.route('/booking_done/')
def render_booking_done():
    return render_template('booking_done.html')

if __name__ == '__main__':
    app.run(debug=True)
