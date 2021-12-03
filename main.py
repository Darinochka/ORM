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


srh = Artist(artist_id=1223224531, name="Mika")
srh.name = 'Karina'
print(srh.name)
print(srh.artist_id)
srh.save()
alish = Artist.create(artist_id=32423942394, name='KAlisher')

print(alish.name)
print(alish.artist_id)

artists = Artist.select('Name', 'ArtistId')
print(artists)

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