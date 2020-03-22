from flask import Flask, render_template, request
import json, random

with open('./static/goals.json', 'r') as f:
    goals = json.load(f)

with open('./static/teachers.json', 'r') as f:
    teachers = json.load(f)

week = {'mon': 'Понедельник', 'tue': 'Вторник', 'wed': 'Среда', 'thu': 'Четверг', 'fri': 'Пятница', 'sat': 'Суббота', 'sun': 'Воскресенье'}

app = Flask(__name__)

@app.route('/')
def render_main():
    temp_list = sorted(random.sample(range(1, 11), 6))

    teacher = []
    for i in temp_list:
        teacher.append(teachers[i])
    return render_template('index.html', goals=goals, teacher=teacher)

@app.route('/goals/<goal>/')
def render_goal(goal):
    goal_teacher = []
    for teacher in teachers:
        temp_list = teacher['goals']
        for i in temp_list:
            if i == goal:
                goal_teacher.append(teacher)

    for i in goals:
        if i == goal:
            goal = goals[i]
    return render_template('goal.html', goal=goal, teachers=goal_teacher)

@app.route('/profiles/<id_teacher>/')
def render_profiles(id_teacher):
    teacher = {}
    for i in range(len(teachers)):
        if int(id_teacher) == teachers[i]['id']:
            teacher = teachers[i]
    return render_template('profile.html', teacher=teacher, week=week, goals=goals)

@app.route('/request/')
def render_request():
    form = """<form action="/request_done/" class="card mb-5" method="POST">
        <div class="card-body text-center pt-5">
          <h1 class="h3 card-title mt-4 mb-2">Подбор преподавателя</h1>
          <p class="px-5">Напишите, чего вам нужно и&nbsp;мы&nbsp;подберем отличных&nbsp;ребят</p>
        </div>
        <hr>
        <div class="card-body mx-3">
          <div class="row">
            <div class="col">
              <p>Какая цель занятий?</p>
              <div class="form-check ">
                <input type="radio" class="form-check-input" name="goal" value="travel" id="goal1" checked>
                <label class="form-check-label" for="goal1">
                  Для путешествий
                </label> 
              </div>
              <div class="form-check ">
                <input type="radio" class="form-check-input" name="goal" value="learn" id="goal2">
                <label class="form-check-label" for="goal2">
                  Для школы
                </label>
              </div>
              <div class="form-check ">
                <input type="radio" class="form-check-input" name="goal" value="work" id="goal3">
                <label class="form-check-label" for="goal2">
                  Для работы
                </label>
              </div>
              <div class="form-check ">
                <input type="radio" class="form-check-input" name="goal" value="move" id="goal4">
                <label class="form-check-label" for="goal2">
                  Для переезда
                </label>
              </div>
            </div>
            <div class="col">
              <p>Сколько времени есть?</p>
              <div class="form-check">
                <input type="radio" class="form-check-input" name="time" value="1-2" id="time1">
                <label class="form-check-label" for="time1">
                  1-2 часа в&nbsp;неделю
                </label> 
              </div>
              <div class="form-check">
                <input type="radio" class="form-check-input" name="time" value="3-5" id="time2">
                <label class="form-check-label" for="time2">
                  3-5 часов в&nbsp;неделю
                </label>
              </div>
              <div class="form-check">
                <input type="radio" class="form-check-input" name="time" value="5-7" id="time3" checked>
                <label class="form-check-label" for="time3">
                  5-7 часов в&nbsp;неделю
                </label> 
              </div>
              <div class="form-check">
                <input type="radio" class="form-check-input" name="time" value="7-10" id="time4">
                <label class="form-check-label" for="time4">
                  7-10 часов в&nbsp;неделю
                </label>
              </div>
            </div>
          </div>
        </div>
        <hr>
        <div class="card-body mx-3">
          <label class="mb-1 mt-2">Вас зовут</label>
          <input class="form-control" type="text" placeholder="ФИО" name = "request_name">
          <label class="mb-1 mt-2">Ваш телефон</label>
          <input class="form-control" type="text" placeholder="+7. . ." name = "request_phone">
          <input type="submit" class="btn btn-primary mt-4 mb-2" value="Найдите мне преподавателя">
        </div>
      </form>"""
    return render_template('request.html')

@app.route('/request_done/', methods=['POST'])
def render_request_done():
    requests = {'client_goal': request.form.get('goal'),
                'client_time': request.form.get('time'),
                'client_name': request.form.get('request_name'),
                'client_phone': request.form.get('request_phone')}
    with open('request.jsonlines', 'a', encoding='utf-8') as f:
        json.dump(requests, f, ensure_ascii=False)
        f.write('\n')
    return render_template('request_done.html')

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

if __name__ == '__main__':
    app.run(debug=True)
