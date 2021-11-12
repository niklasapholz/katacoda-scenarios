CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER GENERATED ALWAYS AS IDENTITY,
  name TEXT NOT NULL,
  surname TEXT NOT NULL,
  PRIMARY KEY(user_id)
);

CREATE TABLE IF NOT EXISTS activities (
  training_id INTEGER GENERATED ALWAYS AS IDENTITY,
  user_id INTEGER NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,
  total_timer_time REAL NOT NULL,
  local_timestamp TIMESTAMPTZ NOT NULL,
  num_sessions SMALLINT NOT NULL,
  type SMALLINT,
  event SMALLINT,
  event_type SMALLINT,
  PRIMARY KEY(training_id),
  CONSTRAINT fk_user
    FOREIGN KEY(user_id)
      REFERENCES users(user_id)
      ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS swimming_sessions (
  session_id INTEGER GENERATED ALWAYS AS IDENTITY,
  training_id INTEGER NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,
  start_time TIMESTAMPTZ NOT NULL,
  total_elapsed_time REAL NOT NULL,
  total_timer_time REAL NOT NULL,
  total_distance REAL NOT NULL,
  total_strokes INTEGER,
  message_index SMALLINT NOT NULL,
  total_calories SMALLINT NOT NULL,
  avg_speed REAL,
  max_speed REAL,
  first_lap_index SMALLINT NOT NULL,
  num_laps SMALLINT NOT NULL,
  num_lengths SMALLINT NOT NULL,
  avg_stroke_distance REAL NOT NULL,
  pool_length REAL NOT NULL,
  num_active_lengths SMALLINT NOT NULL,
  event SMALLINT,
  event_type SMALLINT,
  sport SMALLINT NOT NULL,
  sub_sport SMALLINT NOT NULL,
  avg_cadence SMALLINT NOT NULL,
  trigger SMALLINT,
  pool_length_unit SMALLINT NOT NULL,
  PRIMARY KEY(session_id),
  CONSTRAINT fk_swim_training
    FOREIGN KEY(training_id)
      REFERENCES activities(training_id)
      ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS swimming_laps (
  lap_id INTEGER GENERATED ALWAYS AS IDENTITY,
  session_id INTEGER NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,
  start_time TIMESTAMPTZ NOT NULL,
  total_elapsed_time REAL NOT NULL,
  total_timer_time REAL NOT NULL,
  total_distance REAL NOT NULL,
  total_strokes INTEGER,
  message_index SMALLINT NOT NULL,
  total_calories SMALLINT NOT NULL,
  avg_speed REAL,
  max_speed REAL,
  num_lengths SMALLINT NOT NULL,
  first_length_index SMALLINT NOT NULL,
  avg_stroke_distance REAL NOT NULL,
  num_active_lengths SMALLINT NOT NULL,
  event SMALLINT,
  event_type SMALLINT,
  avg_cadence SMALLINT NOT NULL,
  lap_trigger SMALLINT,
  sport SMALLINT NOT NULL,
  sub_sport SMALLINT NOT NULL,
  swim_stroke SMALLINT NOT NULL,
  PRIMARY KEY(lap_id),
  CONSTRAINT fk_swimming_session
    FOREIGN KEY(session_id)
      REFERENCES swimming_sessions(session_id)
      ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS length (
  length_id INTEGER GENERATED ALWAYS AS IDENTITY,
  lap_id INTEGER NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,
  start_time TIMESTAMPTZ NOT NULL,
  total_elapsed_time REAL NOT NULL,
  total_timer_time REAL NOT NULL,
  message_index SMALLINT NOT NULL,
  total_strokes INTEGER NOT NULL,
  avg_speed REAL NOT NULL,
  total_calories SMALLINT NOT NULL,
  event SMALLINT,
  event_type SMALLINT,
  swim_stroke SMALLINT,
  avg_swimming_cadence SMALLINT,
  length_type SMALLINT,
  PRIMARY KEY(length_id),
  CONSTRAINT fk_swimming_lap
    FOREIGN KEY(lap_id)
      REFERENCES swimming_laps(lap_id)
      ON DELETE CASCADE
);

INSERT INTO users (name, surname) VALUES ('','');
