from flask import Flask, render_template
import json

with open('./static/goals.json', 'r') as f:
    goals = json.load(f)

with open('./static/teachers.json', 'r') as f:
    teachers = json.load(f)

app = Flask(__name__)

@app.route('/')
def render_main():
    return render_template('index.html')

@app.route('/goals/<goal>/')
def render_goal(goal):
    return render_template('goal.html')

@app.route('/profiles/<id_teacher>/')
def render_profiles(id_teacher):
    teacher = {}
    for i in range(len(teachers)):
        if int(id_teacher) == teachers[i]['id']:
            teacher = teachers[i]

    week = {'mon': 'Понедельник', 'tue': 'Вторник', 'wed': 'Среда', 'thu': 'Четверг', 'fri': 'Пятница', 'sat': 'Суббота', 'sun': 'Воскресенье'}
    return render_template('profile.html', teacher=teacher, week=week, goals=goals)

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
