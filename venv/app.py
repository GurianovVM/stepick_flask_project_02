from flask import Flask, render_template, request
import json

with open('./static/goals.json', 'r') as f:
    goals = json.load(f)

with open('./static/teachers.json', 'r') as f:
    teachers = json.load(f)

week = {'mon': 'Понедельник', 'tue': 'Вторник', 'wed': 'Среда', 'thu': 'Четверг', 'fri': 'Пятница', 'sat': 'Суббота', 'sun': 'Воскресенье'}

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
    return render_template('profile.html', teacher=teacher, week=week, goals=goals)

@app.route('/request/')
def render_request():
    return render_template('request.html')

@app.route('/request_done/')
def render_request_done():
    return render_template('request_done.html')

@app.route('/booking_done/', methods=['POST'])
def form_booking():
    booking = {'client_day': request.form.get('clientWeekday'),
                'client_time': request.form.get('clientTime'),
                'teacher_id': request.form.get('clientTeacher'),
                'client_name': request.form.get('clientName'),
                'client_phone': request.form.get('clientPhone')}
    with open('booking.jsonlines', 'a', encoding='utf-8') as f:
        json.dump(booking, f)
        f.write('\n')
    client_week_day = ''
    for i in week:
        if booking['client_day'] == i:
            client_week_day = week[i]
    return render_template('booking_done.html', name=booking['client_name'], day=client_week_day, hour=booking['client_time'], phone=booking['client_phone'])

@app.route('/booking/<id_teacher>/<day>/<time>/')
def render_booking(id_teacher, day, time):
    teacher = {}
    for i in range(len(teachers)):
        if int(id_teacher) == teachers[i]['id']:
            teacher = teachers[i]
    form = """<form action="booking_done" class="card mb-3" method="POST">
          <div class="card-body text-center pt-5">
            <img src="{{ teacher.picture }}" class="mb-3" width="95" alt="">
            <h2 class="h5 card-title mt-2 mb-2">{{teacher.name}}</h2>
            <p class="my-1">Запись на пробный урок</p>
            <p class="my-1">{%for i,j in week.items()%}{%if day == i%}{{j}}{%endif%}{%endfor%}, {{hour}}:00</p>
          </div>
          <hr />
          <div class="card-body mx-3">
              <div class="row">
                  <input class="form-control" type="hidden" name="clientWeekday" value="{{day}}">
                  <input class="form-control" type="hidden" name="clientTime" value="{{hour}}">
                  <input class="form-control" type="hidden" name="clientTeacher" value="{{teacher.id}}">
              </div>

            <label class="mb-1 mt-2" for="clientName">Вас зовут</label>
            <input class="form-control" type="text" name="clientName" id="clientName">

            <label class="mb-1 mt-2" for="clientPhone">Ваш телефон</label>
            <input class="form-control" type="tel"  name="clientPhone" id="clientPhone">

            <input type="submit" class="btn btn-primary btn-block mt-4" value="Записаться на пробный урок">

          </div>
        </form>"""
    return render_template('booking.html', teacher=teacher, day=day, hour=time, week=week)

@app.route('/booking_done/')
def render_booking_done():
    return render_template('booking_done.html')

if __name__ == '__main__':
    app.run(debug=True)
