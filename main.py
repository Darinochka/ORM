# from peewee import *
from sth import *

conn = SqliteDatabase('chinook.sqlite')

class BaseModel(Model):
    database = conn  # соединение с базой, из шаблона выше

# Определяем модель исполнителя
class Artist(BaseModel):
    artist_id = IntegerField(column_name='ArtistId')
    name = TextField(column_name='Name')
    # class Meta:
    table_name = 'Artist'

class Tracks(BaseModel):
    track_id = IntegerField(column_name='TrackId')
    name = TextField(column_name="Name")
    table_name = 'Track'

# SELECT Name, ArtistID FROM Artist;
artists = Artist.select('Name', 'ArtistId')

srh = Artist(artist_id=1223224534, name="Darina")
srh.name = 'Karina'
alish = Artist.create(artist_id=234423, name='Alisher')

print(alish.name)
print(alish.artist_id)
print(srh.name)
print(srh.artist_id)

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