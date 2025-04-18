from django.db import connection


def get_total_trip_participants(trip_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT get_total_trip_participants(%s);", [trip_id])
        result = cursor.fetchone()
    return result[0] if result else 0
