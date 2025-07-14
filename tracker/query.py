from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('user_tracking')

def get_user_events(user_id, limit=5):
    rows = session.execute("""
        SELECT * FROM user_events WHERE user_id = %s LIMIT %s
    """, (user_id, limit))
    for row in rows:
        print(row)

# Replace with actual UUID used in producer.py
get_user_events('some-uuid-here')
