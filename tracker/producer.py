from cassandra.cluster import Cluster
from faker import Faker
import random
import time
from datetime import datetime

EVENT_TYPES = ['click', 'view', 'login', 'logout', 'purchase']
fake = Faker()

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('user_tracking')

def generate_event(user_id):
    event_type = random.choice(EVENT_TYPES)
    details = fake.sentence()
    now = datetime.utcnow()
    return user_id, now, event_type, details

def insert_event(user_id):
    user_id, now, event_type, details = generate_event(user_id)
    session.execute("""
        INSERT INTO user_events (user_id, event_time, event_type, details)
        VALUES (%s, %s, %s, %s)
    """, (user_id, now, event_type, details))
    print(f"{user_id} - {event_type} at {now}")

if __name__ == "__main__":
    # Simulate 10 events with random user IDs - comment out if needed
    for _ in range(10):  
        insert_event(fake.uuid4())
        time.sleep(1)
    
    # Simulate user activity for the same user - comment out if needed
    """ user_id = fake.uuid4()
    for _ in range(10):
        insert_event(user_id)
        time.sleep(1) """
