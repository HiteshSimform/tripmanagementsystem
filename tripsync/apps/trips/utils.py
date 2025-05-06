# from django.db import connection


# def get_total_trip_participants(trip_id):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT get_total_trip_participants(%s);", [trip_id])
#         result = cursor.fetchone()
#     return result[0] if result else 0

from django.db import connection

def get_total_trip_participants_proc(trip_id):
    with connection.cursor() as cursor:
        cursor.execute("CALL get_total_trip_participants_proc(%s, %s)", [trip_id, None])
        result = cursor.fetchone()
    return result[0] if result else 0

