import psycopg2
import json
from datetime import datetime, timedelta
import pytz

def main()->None:
  db_conn = connect_to_db()
  # create our tables
  create_tables(db_conn)
  # read our data
  with open('example_fit.json', 'r') as json_file:
    training = json.load(json_file)
  # upload activity
  upload_swim(training)
  # check result
  db_cur = db_conn.cursor()
  result = db_cur.execute('SELECT COUNT(*) FROM lengths;')
  print("We inserted", result, "legnths!")
  print("Congratiolations, you did it!")

def connect_to_db():
  conn = psycopg2.connect(
    host="database",
    database="postgres",
    user="postgres",
    password="supersicher"
  )
  return conn

def create_tables(db_conn) -> None:
  create_statements = ""
  with open("setup.sql", "r") as setup:
    create_statements = setup.read()
  db_cur = db_conn.cursor()
  db_cur.execute(create_statements)
  db_conn.commit()
  db_cur.close()

def upload_swim(training: dict)->None:
  """upload a swimming training"""
  training_data = training['data']
  message_map = map_training_data(training_data)
  db_conn = connect_to_db()
  db_cur = db_conn.cursor()
  training_id = upload_activity(db_cur, training_data[message_map['activity'][0]])
  session_lap_info = upload_swim_sessions(db_cur, training_data[message_map['session'][0]], training_id)
  laps_with_timestamp = upload_swim_laps(db_cur, training_data, message_map['lap'], session_lap_info)
  upload_swim_lengths(db_cur, training_data, message_map['length'])
  # do not commit earlier, since everything depends on each other
  db_conn.commit()
  db_cur.close()
  db_conn.close()

def upload_swim_sessions(db_cur, session_info: dict, training_id: int) -> list[list[int]]:
  """Upload a swimming session"""
  session_data = session_info['data']
  print('You did', len(session_data), "sessions")
  # collect session id with first_lap_index and num_laps
  session_lap_info = []
  for session in session_data:
    sql = "INSERT INTO swimming_sessions (training_id,"
    values = ") VALUES (" + str(training_id) + ','
    for column in session[1:]:
      for key, value in column.items():
        if not key_in_swim_session(key):
          continue
        sql += key + ','
        if "timestamp" in key or key in ['start_time']:
          values += "'" + str(convert_garmin_timestamp(int(value['value']))) + "'"
        else:
          values += value['value']
        values += ','
    sql = sql[:-1]
    sql += values[:-1] + ') RETURNING session_id, first_lap_index, num_laps;'
    db_cur.execute(sql)
    result = db_cur.fetchone()
    session_lap_info.append(result)
  return session_lap_info

def upload_swim_laps(db_cur, training_data: dict, lap_data_indicies: list[int], session_lap_info: list[tuple] ) -> list[list[int, str]]:
  """
  Upload laps for swimming
  """
  activity_results = []
  for index, session_info in enumerate(session_lap_info):
    last_lap_index = session_info[1] + session_info[2] - 1
    session_lap_data = training_data[lap_data_indicies[index]]
    session_result = []
    for lap in session_lap_data['data']:
      sql = "INSERT INTO swimming_laps (session_id,"
      values = ") VALUES (" + str(session_info[0]) + ','
      for column in lap[1:]:
        for key, value in column.items():
          if not key_in_swim_lap(key):
            continue
          sql += key + ','
          if "timestamp" in key or key == 'start_time':
            values += "'" + str(convert_garmin_timestamp(int(value['value']))) + "'"
          else:
            values += value['value']
          values += ','
      sql = sql[:-1]
      sql += values[:-1] + ') RETURNING lap_id, timestamp;'
      db_cur.execute(sql)
      result = db_cur.fetchone()
      session_result.append(result)
    activity_results.append(session_result)
  return activity_results

def upload_swim_lengths(db_cur, training_data: dict, lengths_indices: list[int]) -> None:
  """Upload lengths fro a swimming session"""
  for lengths_block_index in lengths_indices:
    lengths_block_data = training_data[lengths_block_index]['data']
    for lengths_row_data in lengths_block_data:
      sql = "INSERT INTO length (lap_id,"
      values = ""
      start_time = ""
      for column in lengths_row_data[1:]:
        for key, value in column.items():
          if not key_in_swim_lengths(key):
            continue
          sql += key + ','
          if "timestamp" in key or key == 'start_time':
            values += "'" + str(convert_garmin_timestamp(int(value['value']))) + "'"
            if key == 'start_time':
              start_time = "'" + str(convert_garmin_timestamp(int(value['value']))) + "'"
          else:
            values += value['value']
          values += ','
      sql = sql[:-1]
      sql += ") VALUES ((SELECT lap_id FROM swimming_laps WHERE start_time <=" + start_time + \
              "AND timestamp > " + start_time + ")," + values[:-1] + ");"
      db_cur.execute(sql)

def map_training_data(training_data: list[dict]) -> dict[str, list[int]]:
  """map message-types to list-position(s)"""
  message_map = {}
  # message_types can repeat themselfes
  for index, message in enumerate(training_data):
    message_type = message['definition']['message_type']
    if message_type in message_map.keys():
      message_map[message_type].append(index)
    else:
      message_map.update({message_type: [index]})
  return message_map

def upload_activity(db_cur, activity_info: dict) -> int:
  """The acticity-data is the same for all types of training"""
  activity_data = activity_info['data']
  if len(activity_data) != 1:
    print("More than one activity row")
  sql = "INSERT INTO activities (user_id,"
  values = ") VALUES (1,"
  for column in activity_data[0][1:]:
    for key, value in column.items():
      sql += key + ','
      if "timestamp" in key:
        values += "'" + str(convert_garmin_timestamp(int(value['value']))) + "'"
      else:
        values += value['value']
      values += ','
  sql = sql[:-1]
  sql += values[:-1] + ') RETURNING training_id;'
  db_cur.execute(sql)
  result = db_cur.fetchone()
  return result[0]

def convert_garmin_timestamp(garmin_timestamp: int) -> datetime:
  """Garmins timestamp counts the seconds since the 31.12.1989."""

  tz_utc = pytz.timezone('utc')
  tz_berlin = pytz.timezone('Europe/Berlin')
  garmin_base = datetime(1989, 12, 31, tzinfo=tz_utc)
  actual_stamp = garmin_base + timedelta(seconds=garmin_timestamp)
  actual_stamp = actual_stamp.astimezone(tz_berlin)
  return actual_stamp

def key_in_swim_session(key: str) -> bool:
  keys = [
    "timestamp",
    "start_time",
    "total_elapsed_time",
    "total_timer_time",
    "total_distance",
    "total_strokes",
    "message_index",
    "total_calories",
    "avg_speed",
    "max_speed",
    "first_lap_index",
    "num_laps",
    "num_lengths",
    "avg_stroke_distance",
    "pool_length",
    "num_active_lengths",
    "event",
    "event_type",
    "sport",
    "sub_sport",
    "avg_cadence",
    "trigger",
    "pool_length_unit"
  ]
  return key in keys

def key_in_swim_lap(key: str) -> bool:
  keys = [
    "timestamp",
    "start_time",
    "total_elapsed_time",
    "total_timer_time",
    "total_distance",
    "total_strokes",
    "message_index",
    "total_calories",
    "avg_speed",
    "max_speed",
    "num_lengths",
    "first_length_index",
    "avg_stroke_distance",
    "num_active_lengths",
    "event",
    "event_type",
    "avg_cadence",
    "lap_trigger",
    "sport",
    "swim_stroke",
    "sub_sport"
  ]
  return key in keys

def key_in_swim_lengths(key: str)->bool:
  keys=[
    "timestamp",
    "start_time",
    "total_elapsed_time",
    "total_timer_time",
    "message_index",
    "total_strokes",
    "avg_speed",
    "total_calories",
    "event",
    "event_type",
    "swim_stroke",
    "avg_swimming_cadence",
    "length_type"
  ]
  return key in keys