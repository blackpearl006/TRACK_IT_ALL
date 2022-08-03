from my_app import app, db, api
from flask import current_app, redirect, render_template, url_for, flash, request
from my_app.models import Tracker, User, Log
from my_app.forms import AddChoices, AddLog, AddTracker, RegisterForm, LoginForm, UpdateFormTracker, DeleteFormTracker, \
    UpdateLog, DeleteLog, UpdateProfile
from flask_login import current_user, login_user, logout_user, login_required
import datetime
import logging
logging.basicConfig(filename='debug.log',level=logging.DEBUG,format=f'%(asctime)s %(name)s %(threadName)s : %(message)s')



@app.route("/")
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    update_profile = UpdateProfile()
    if request.method == "POST":
        updated_profile = request.form.get('updated_profile')
        # print("<----------------------------",updated_tracker,"--------------------->")
        to_upd_profile = User.query.filter_by(id=updated_profile).first()
        # print(to_upd_tracker)
        if to_upd_profile:
            to_upd_profile.username = update_profile.username.data
            to_upd_profile.email = update_profile.email.data
            to_upd_profile.target = update_profile.target.data
            to_upd_profile.city = update_profile.city.data
            to_upd_profile.social = update_profile.social.data
            to_upd_profile.phone_num = update_profile.phone_num.data
            db.session.commit()
            flash("Profile updated ", category="success")
            current_app.logger.debug('Profile upadted for ' + current_user.username + ' sucessfully')
    return render_template('profile.html', update_profile=update_profile)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_page():
    update_tracker = UpdateFormTracker()
    if request.method == "POST":
        updated_tracker = request.form.get('updated_tracker')
        # print("<----------------------------",updated_tracker,"--------------------->")
        to_upd_tracker = Tracker.query.filter_by(name=updated_tracker).first()
        # print(to_upd_tracker)
        if to_upd_tracker:
            upd_name = update_tracker.name.data
            upd_desc = update_tracker.description.data
            to_upd_tracker.name = upd_name
            to_upd_tracker.description = upd_desc
            db.session.commit()
            flash("Tracker updated ", category="success")
            current_app.logger.debug('Tracker upadted for ' +current_user.username+'\'s '+to_upd_tracker.name+'sucessfully')
            to_upd_tracker.last_modified=datetime.datetime.now().strftime(format="%j")
            db.session.commit()

    delete_tracker = DeleteFormTracker()
    if request.method == "POST":
        deleted_tracker = request.form.get('deleted_tracker')
        to_del_tracker = Tracker.query.filter_by(name=deleted_tracker).first()
        if to_del_tracker:
            db.session.delete(to_del_tracker)
            db.session.commit()
            flash("Tracker deleted ", category="success")
            current_app.logger.debug('Tracker deleted for ' +current_user.username +'\'s '+to_del_tracker.name+' sucessfully')

    trackers = Tracker.query.filter_by(owner=current_user.id).all()
    tracker_len=len(trackers)
    logs = Log.query.all()
    trackers_name=[]
    log_count=[]
    for i in trackers:
        trackers_name.append(i.name)
        count=0
        for j in logs:    #for higher nuber of logs use better counting method  O(n)
            if j.tracker_id==i.id:
                count=count+1
        log_count.append(count)
    today=int(datetime.datetime.now().strftime(format="%j"))
    print
    context={'trackers': trackers, 'update_tracker': update_tracker, 
            'delete_tracker': delete_tracker,
            'log_count': log_count, 'trackers_name': trackers_name, 
            'tracker_len': tracker_len,'today':today}
    return render_template('dashboard.html', **context)
    

@app.route('/addtracker', methods=['GET', 'POST'])
@login_required
def addtracker_page():
    addTracker = AddTracker()
    if addTracker.validate_on_submit():
        tracker_type = addTracker.type.data
        tracker_name = addTracker.name.data
        new_tracker = Tracker(name=addTracker.name.data,
                              description=addTracker.description.data,
                              type=addTracker.type.data,
                              owner=current_user.id)
        db.session.add(new_tracker)
        db.session.commit()

        flash("New Tracker added ", category="success")
        current_app.logger.debug(' new Tracker added for '+ current_user.username +' sucessfully')


        tracker = Tracker.query.filter_by(name=tracker_name).first()
        tracker.last_modified=datetime.datetime.now().strftime(format="%j")
        db.session.commit()
        if tracker_type == '2':
            return redirect(url_for('choices_page', tracker_name=tracker_name))
        return redirect(url_for('dashboard_page'))

    if addTracker.errors != {}:
        for error in addTracker.errors.values():
            flash(f'ERROR: {error}', category='danger')
    return render_template('addtracker.html', addTracker=addTracker)


@app.route('/<string:tracker_name>/choices', methods=['GET', 'POST'])
def choices_page(tracker_name):
    to_add_choices = Tracker.query.filter_by(name=tracker_name).first()
    add_Choices = AddChoices()
    if request.method == "POST":
        choices = add_Choices.choices.data
        to_add_choices.choices = choices
        db.session.commit()
        flash("Multiple choice tracker created ", category="success")
        current_app.logger.debug('Tracker choices updated for ' +current_user.username+'\'s '+tracker_name+' sucessfully')
        return redirect(url_for('dashboard_page'))
    return render_template('choices.html', tracker=to_add_choices, add_Choices=add_Choices)


@app.route('/<int:tracker_id>/log', methods=['GET', 'POST'])
@login_required
def log_page(tracker_id):
    update_log = UpdateLog()
    if request.method == "POST":
        updated_log = request.form.get('updated_log')
        to_upd_log = Log.query.filter_by(id=updated_log).first()
        if to_upd_log:
            upd_value = update_log.value.data
            upd_note = update_log.note.data
            to_upd_log.value = upd_value
            to_upd_log.note = upd_note
            db.session.commit()
            flash("Tracker Logs updated ", category="success")
            tracker=Tracker.query.filter_by(id=tracker_id).first()
            tracker.last_modified=datetime.datetime.now().strftime(format="%j")
            db.session.commit()
            current_app.logger.debug('Log upadted for ' +current_user.username+'\'s '+tracker.name+'\'s  log id :'+str(to_upd_log.id)+' sucessfully')

    delete_log = DeleteLog()
    if request.method == "POST":
        deleted_log = request.form.get('deleted_log')
        to_del_log = Log.query.filter_by(id=deleted_log).first()
        # print("here ------------")

        if to_del_log:
            db.session.delete(to_del_log)
            db.session.commit()
            flash("Log deleted ", category="success")
            current_app.logger.debug('Log upadted for ' +current_user.username+' \'s ' +  'log  sucessfully')


    tracker = Tracker.query.filter_by(id=tracker_id).first()
    logs = Log.query.filter_by(tracker_id=tracker_id).all()
    # print(logs)

    time_graph, value_graph, datetime_field, graph ,new_value_graph,choice_dict=[], [], [], {}, [],{}
    for i in logs:
        datetime_field.append(i.timestamp)
        graph[i.timestamp.strftime("%d-%m-%y :: %H:%M:%S")] = i.value
        # time_graph.append(i.timestamp.strftime("%d-%m-%y:%H:%M"))
        value_graph.append(i.value)
    # print(datetime_field)
    sort_time = sorted(datetime_field)
    
    for j in sort_time:
        time_graph.append(j.strftime("%d-%m-%y :: %H:%M:%S"))
    for j in time_graph:
        new_value_graph.append(graph[j])
    type_dict= {'1': 'line', '2': 'bar', '3': 'bar', '4': 'line', '5': 'line', '6': 'line'}
    type = type_dict[tracker.type]
    choices=None

    if tracker.type == '2':
        value_graph=[]
        choices = tracker.choices.split(',')
        choice_dict={}
        for i in range(1,len(choices)+1):
            count=0
            choice_dict[i]=choices[i-1]
            for j in logs:
                if j.value==i:count=count+1
            value_graph.append(count)

    if tracker.type == '3':
        value_graph=[]
        choices = ['YES', 'NO']
        yes,no=0,0
        for i in logs: 
            if i.value==1: yes=yes+1
            else: no=no+1
        value_graph=[yes,no]

    context = {'tracker': tracker,
               'logs': logs,
               'update_log': update_log,
               'delete_log': delete_log,
               'graph': graph,
               'sort_time': sort_time,
               'value_graph': value_graph,
               'time_graph': time_graph,
               'datetime_field': datetime_field,
               'type': type,
               'new_value_graph': new_value_graph,
               'choices': choices,
               'choice_dict': choice_dict}
    return render_template('log.html', **context)


@app.route('/<int:tracker_id>/addlog', methods=['GET', 'POST'])
@login_required
def addlog_page(tracker_id):
    addLog = AddLog()
    now = datetime.datetime.now
    tracker = Tracker.query.filter_by(id=tracker_id).first()
    if addLog.validate_on_submit():
        newlog = Log(value=addLog.value.data,
                     timestamp=addLog.timestamp.data,
                     note=addLog.note.data,
                     desc=addLog.desc.data,
                     user_id=current_user.id,
                     tracker_id=tracker_id)
        db.session.add(newlog)
        db.session.commit()
        
        tracker=Tracker.query.filter_by(id=tracker_id).first()
        tracker.last_modified=datetime.datetime.now()
        db.session.commit()
        flash("Log added ", category="success")
        current_app.logger.debug('new Log added for ' +current_user.username +'\'s ' + tracker.name+' sucessfully')
        tracker=Tracker.query.filter_by(id=tracker_id).first()
        tracker.last_modified=datetime.datetime.now().strftime(format="%j")
        db.session.commit()
        # print(last_modified_time,'last modified time')
        # print('<---------------------------->')
        return redirect(url_for('log_page', tracker_id=tracker_id))
    choices = []  # throws an error
    try:
        choices = tracker.choices.split(',')
    finally:
        context = {'addLog': addLog, 'now': now, 
                  'type1': tracker.type, 'tracker': tracker, 'choices': choices}

        return render_template('addlog.html', **context)  


@app.route('/reward', methods=['GET', 'POST'])
@login_required
def rewards_page():
    trackers = Tracker.query.filter_by(owner=current_user.id).all()
    trackers_len = len(trackers)
    context = {'trackers_len': trackers_len}
    return render_template('report.html', **context)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Sucess!! You are loged in as :{user_to_create.username}', category='success')
        return redirect(url_for('dashboard_page'))
    if form.errors != {}:
        for error in form.errors.values():
            flash(f'ERROR: {error}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if (attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data)):
            login_user(attempted_user)
            flash(f'Sucess!! You are loged in as :{attempted_user.username}', category='success')
            return redirect(url_for('dashboard_page'))
        else:
            flash(f'Username and password are not a match!!', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out", category='info')
    return redirect(url_for('home_page'))


def running():
    new_tracker = Tracker(name='Running',
                          description='Distance covered in KM',
                          type=1,
                          owner=current_user.id)
    db.session.add(new_tracker)
    db.session.commit()
    return redirect(url_for('dashboard_page'))


from my_app.api import UserAPI, TrackerAPI, LogAPI

api.add_resource(UserAPI, "/api/user/<string:username>", "/api/user")
api.add_resource(TrackerAPI, "/api/tracker/name", "/api/tracker/<string:name>")
api.add_resource(LogAPI, "/api/log/<int:tracker_id>/<int:log_id>", "/api/log/<int:tracker_id>")
