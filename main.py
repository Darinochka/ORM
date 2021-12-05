# from peewee import *
from sth import *


conn = SqliteDatabase('chinook.sqlite')

class BaseModel(Model):
    database = conn  # соединение с базой, из шаблона выше

# Определяем модель исполнителя
class Artist(BaseModel):
    artist_id = IntegerField(column_name='ArtistId')
    name = TextField(column_name='Name')

    table_name = 'Artist'

class Tracks(BaseModel):
    track_id = IntegerField(column_name='TrackId')
    name = TextField(column_name="Name")
    album_id = IntegerField(column_name="AlbumId")

    table_name = 'Track'

# print(Tracks.select())

print(Tracks.delete(Tracks.album_id == 3))
print(Tracks.select(Tracks.album_id == 3))
k = Artist.create(artist_id=341334, name='Alisher')
print(k.name)
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM Track WHERE Name = 'Balls to the Wall'")
# print(cursor.fetchall())

# SELECT Name, ArtistID FROM Artist;

# print(Artist.name)

# srh = Artist(artist_id=122324, name="Mika")
# srh.save()

# alish = Artist.create(artist_id=3242394, name='KAlisher')
# print(alish.name)

# print(alish.delete_instance())
# print(srh.delete_instance())

# tracks = Tracks.select('Name')
# print(tracks)
#INSERT INTO Artist (Name, ArtistId)
#  	VALUES ("Darina", 300), ("Karina", 304);
# Artist.insert(artist_data)
# print(artists)
# UPDATE Track SET Name = "Dima", ArtistId = 250;
# Track.update(
#     new_track={"Name": "Dima", "ArtistId": 250}
# )

# # DELETE FROM t;
# Track.delete()

# Artist.save()
# print(artists)

conn.close()