from app.movie.models import Movie
from app import db

with open('db_imports/omdb.txt') as f:
    lines = f.readlines()
    COLUMNS = lines.pop(0).replace('\r', '').replace('\n', '').split('\t')
    # for line in lines:
    line = lines[0].replace('\r', '').replace('\n', '')
    cols = line.split('\t')
    data = {}
    for i, col in enumerate(cols):
        data[COLUMNS[i]] = col
    print data

    movie = Movie(**data)
    db.session.add(movie)

    db.session.commit()

