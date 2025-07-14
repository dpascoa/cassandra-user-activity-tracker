CREATE KEYSPACE IF NOT EXISTS user_tracking
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

USE user_tracking;

CREATE TABLE IF NOT EXISTS user_events (
    user_id TEXT,
    event_time TIMESTAMP,
    event_type TEXT,
    details TEXT,
    PRIMARY KEY (user_id, event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);
