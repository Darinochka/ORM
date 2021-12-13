from saegly import *


conn = SqliteDatabase('chinook.sqlite')

class BaseModel(Model):
    database = conn  # соединение с базой

# Определяем модель исполнителя
class Artist(BaseModel):
    artist_id = IntegerField(column_name='ArtistId')
    name = TextField(column_name='Name')

    table_name = 'Artist'

class Tracks(BaseModel):
    track_id = IntegerField(column_name='TrackId')
    name = TextField(column_name="Name")
    album_id = IntegerField(column_name="AlbumId")
    media_types = IntegerField(column_name="MediaTypeId")
    genre_id = IntegerField(column_name="GenreId")
    composer = TextField(column_name="Composer")
    milliseconds = IntegerField(column_name="Milliseconds")
    bytes_ = IntegerField(column_name="Bytes")
    unit_price = FloatField(column_name="UnitPrice")
    table_name = 'Track'


def main():

    print('SELECT ArtistId, Name FROM Artist')
    assert(Artist.select() == Artist.select("ArtistId", "Name"))
    print(Artist.select())

    print('SELECT ArtistId FROM Artist')
    assert(Artist.select("ArtistId") == Artist.artist_id)
    print(Artist.artist_id)

    print('SELECT TrackId, Name, AlbumId FROM Track WHERE AlbumId = 4')
    print(Tracks.select(Tracks.album_id == 4))

    # INSERT INTO Tracks VALUES (323423, "Монетка", '12')
    lsp = Artist.create(artist_id=343224, name="LSP")
    assert(lsp.name == 'LSP')

    dirty = Artist(artist_id=23434, name="Gryaz")
    assert(dirty.artist_id == 23434)
    dirty.save()
    
    # DELETE
    dirty.delete_instance()

    print('DELETE FROM Tracks WHERE album_id = 3')
    print(Tracks.select(Tracks.album_id == 3))
    print(Tracks.delete(Tracks.album_id == 3))

    # ERRORS
    try:
        k = Artist(artist_id="345", name=4)
    except TypeError:
        print("Ошибка")
    
    conn.close()

if __name__ == "__main__":
    main()