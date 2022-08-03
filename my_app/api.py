from my_app.models import db, User, Tracker, Log
from flask_restful import Resource, marshal_with,fields,reqparse
from my_app.validation import NotFoundError,BusinessValidationError, TrackerValidationError, LogValidationError

user_output_fields={
  "user_id":fields.Integer,
  "username":fields.String,
  "email":fields.String,
  "target":fields.Integer
}
new_user_parser=reqparse.RequestParser()
new_user_parser.add_argument('username')
new_user_parser.add_argument('email')
new_user_parser.add_argument('target')

update_user_parser=reqparse.RequestParser()
update_user_parser.add_argument('email')
update_user_parser.add_argument('target')

class UserAPI(Resource):
  @marshal_with(user_output_fields)
  def get(self,username):
    user = User.query.filter_by(username=username).first()  #try-catch 
    if user:
      return user
    else:
      return NotFoundError(status_code=404)

  @marshal_with(user_output_fields)
  def delete(self,username):
    user = User.query.filter_by(username=username).first()  #try-catch 
    if user is None:
      return NotFoundError(status_code=404)
    trackers=Tracker.query.filter_by(owner=user.id).first()
    if trackers :
      raise BusinessValidationError(status_code=400,error_code="BE1005",error_message="cant delete as there are trackers associated with user")
    db.session.delete(user)
    db.session.commit()
    return '',200
  
  @marshal_with(user_output_fields)
  def put(self,username):
    args=update_user_parser.parse_args()
    upd_email=args.get("email",None)
    upd_target=args.get("target",None)
    if upd_email is None:
      raise BusinessValidationError(status_code=400,error_code="BE1002",error_message="email is required")
    if "@" not in upd_email :
      raise BusinessValidationError(status_code=400,error_code="BE1003",error_message="Invalid email")
    user_e=User.query.filter_by(User.email==upd_email).first()
    if user_e:
      raise BusinessValidationError(status_code=400,error_code="BE1006",error_message="Dulpicate email")
    user=User.query.filter_by(username=username).first()
    if user is None:
      raise BusinessValidationError(status_code=400,error_code="BE1001",error_message="username is required")
    user.target=upd_target
    user.email=upd_email
    db.session.commit()
    return '',200
    
  @marshal_with(user_output_fields)  
  def post(self):
    args=new_user_parser.parse_args()
    username=args.get("username",None)
    email=args.get("email",None)
    target=args.get("target",None)
    if username is None:
      raise BusinessValidationError(status_code=400,error_code="BE1001",error_message="username is required")
    if email is None:
      raise BusinessValidationError(status_code=400,error_code="BE1002",error_message="email is required")
    if "@" not in email :
      raise BusinessValidationError(status_code=400,error_code="BE1003",error_message="Invalid email")
    user=User.query.filter( (User.username==username) | (User.email==email)).first()
    if user:
      raise BusinessValidationError(status_code=400,error_code="BE1004",error_message="User already exists")
    user_e=User.query.filter_by(User.email==email).first()
    if user_e:
      raise BusinessValidationError(status_code=400,error_code="BE1006",error_message="Dulpicate email")
    new_user=User(username=username,email=email,target=target)
    db.session.add(new_user)
    db.session.commit()
    return new_user,201
    
tracker_output_fields={
    "id":fields.Integer,
    "name":fields.String,
    "description":fields.String,
    "type":fields.String,
    "owner":fields.Integer,
    "choices":fields.String
}

new_tracker_parser=reqparse.RequestParser()
new_tracker_parser.add_argument('name')
new_tracker_parser.add_argument('description')
new_tracker_parser.add_argument('type')
new_tracker_parser.add_argument('owner')
new_tracker_parser.add_argument('choices')

upd_tracker_parser=reqparse.RequestParser()
upd_tracker_parser.add_argument('description')
upd_tracker_parser.add_argument('type')
upd_tracker_parser.add_argument('owner')
upd_tracker_parser.add_argument('choices')

class TrackerAPI(Resource):
  @marshal_with(tracker_output_fields)
  def get(self,name):
    tracker = Tracker.query.filter_by(name=name).first()  #try-catch 
    if tracker:
      return tracker
    else:
      return NotFoundError(status_code=404)

  @marshal_with(tracker_output_fields)  
  def post(self):
    args=new_tracker_parser.parse_args()
    name=args.get("name",None)
    description=args.get("description",None)
    type=args.get("type",None)
    owner=args.get("owner",None)
    choices=args.get("choices",None)
    
    if name is None:
      raise TrackerValidationError(status_code=400,error_code="T001",error_message="tracker name is required")
    if type is None:
      raise TrackerValidationError(status_code=400,error_code="T002",error_message="tracker type is required")
    if owner is None:
      raise TrackerValidationError(status_code=400,error_code="T003",error_message="associated user id required")
    user=User.query.all()
    if owner not in user.id:
      raise TrackerValidationError(status_code=400,error_code="T004",error_message="Invalid user")
    tracker=Tracker.query.filter( (Tracker.name==name) & (Tracker.type==type)).first()
    if tracker:
      raise TrackerValidationError(status_code=400,error_code="T005",error_message="Tracker already exists")
    new_tracker=Tracker(name=name,description=description,type=type,owner=owner,choices=choices)
    db.session.add(new_tracker)
    db.session.commit()
    return new_tracker,201

  @marshal_with(tracker_output_fields)
  def delete(self,name):
    tracker=Tracker.query.filter_by(name=name).first()
    if tracker is None:
      return NotFoundError(status_code=404)
    logs=Log.query.filter_by(tracker_id=tracker.id).first()
    if logs :
      raise LogValidationError(status_code=400,error_code="L005",error_message="cant delete as there are log associated with tracker")
    db.session.delete(tracker)
    db.session.commit()
    return '',200

  @marshal_with(tracker_output_fields)  
  def put(self,name):
    args=new_tracker_parser.parse_args()
    upd_description=args.get("description",None)
    upd_type=args.get("type",None)
    upd_choices=args.get("choices",None)
    
    if upd_type is None:
      raise TrackerValidationError(status_code=400,error_code="T002",error_message="tracker type is required")
    tracker=Tracker.query.filter( (Tracker.name==name) & (Tracker.type==upd_type)).first()
    if tracker:
      raise TrackerValidationError(status_code=400,error_code="T004",error_message="Tracker already exists")
    tracker=Tracker.query.filter_by(name=name).first()
    tracker.description=upd_description
    tracker.type=upd_type,
    tracker.choices=upd_choices
    db.session.commit()
    return '',200


log_output_fields={
    "id":fields.Integer,
    "name":fields.String,
    "value":fields.Integer,
    "description":fields.String,
    "type":fields.String,
    "owner":fields.Integer,
    "choices":fields.String
}

new_log_parser=reqparse.RequestParser()
new_log_parser.add_argument('value')
new_log_parser.add_argument('note')
new_log_parser.add_argument('user_id')
new_log_parser.add_argument('tracker_id')
new_log_parser.add_argument('timestamp')

upd_log_parser=reqparse.RequestParser()
upd_log_parser.add_argument('value')
upd_log_parser.add_argument('note')
upd_log_parser.add_argument('timestamp')

class LogAPI(Resource):    
  @marshal_with(log_output_fields)
  def get(self,tracker_id,log_id):
    tracker = Tracker.query.filter_by(id=tracker_id).first()  #try-catch 
    if tracker:
      log = Log.query.filter_by(id=log_id).first()  #try-catch 
      if log :
        return log
      else:
        return NotFoundError(status_code=404)
    else:
      return NotFoundError(status_code=404)
      
  @marshal_with(log_output_fields)  
  def post(self,tracker_id):
    args=new_log_parser.parse_args()
    value=args.get("value",None)
    note=args.get("note",None)
    timestamp=args.get("timestamp",None)
    
    if value is None:
      raise TrackerValidationError(status_code=400,error_code="L001",error_message="value required")
    if timestamp is None:
      raise TrackerValidationError(status_code=400,error_code="T002",error_message="timestamp required")
    tracker=Tracker.query.filter_by(id=tracker_id).first()
    if tracker is None:
      raise TrackerValidationError(status_code=400,error_code="T002",error_message="tracker doesnt exists")
    logs=Log.query.filter_by((timestamp==timestamp)&(value==value)).first()
    if logs : raise LogValidationError(status_code=400,error_code="T002",error_message="log already exits")
    #check timestamp format
    tracker=Tracker.query.filter_by(id=tracker_id).first()
    new_log=Log(value=value,timestamp=timestamp,note=note,user_id=tracker.owner,tracker_id=tracker.id)
    db.session.add(new_log)
    db.session.commit()
    return new_log,201

  @marshal_with(log_output_fields)
  def delete(self,tracker_id,log_id):
    tracker=Tracker.query.filter_by(id=tracker_id).first()
    if tracker is None:
      return NotFoundError(status_code=404)
    logs=Log.query.filter_by(id=log_id).first()
    if logs is None :
      raise LogValidationError(status_code=400,error_code="L005",error_message="log not found")
    db.session.delete(logs)
    db.session.commit()
    return '',200

  @marshal_with(log_output_fields)  
  def put(self,tracker_id,log_id):
    args=new_tracker_parser.parse_args()
    value=args.get("value",None)
    note=args.get("note",None)
    timestamp=args.get("timestamp",None)
    
    if value is None:
      raise TrackerValidationError(status_code=400,error_code="L001",error_message="value required")
    if timestamp is None:
      raise TrackerValidationError(status_code=400,error_code="T002",error_message="timestamp required")
    tracker=Tracker.query.filter_by(id=tracker_id).first()
    if tracker is None:
      raise TrackerValidationError(status_code=400,error_code="T002",error_message="tracker doesnt exists")
    logs=Log.query.filter_by((timestamp==timestamp)&(value==value)).first()
    if logs : raise LogValidationError(status_code=400,error_code="T002",error_message="log already exits")
    log=Log.query.filter_by(id-log_id).first()
    log.value=value
    log.timestamp=timestamp
    log.note=note
    db.session.commit()
    return '',200