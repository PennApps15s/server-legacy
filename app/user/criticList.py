from app import db
from app.user.models import User
from app.review.models import Review

import json

columns = ['id', 'name', '"criticPublication"', 'average_review', 'sharedCount', 'diffCount']

def get_critics(user, reviews):
    print str(user), str(reviews)

    likes = [
        "11720",
        "49821",
        "22007",
        "30922",
        "50981",
        "13800",
        "13341"
    ]
    dislikes = [
        "28075",
        "31379",
        "44391",
        "45418"
    ]
    
    sql = """
            SELECT """ +', '.join(columns)+ """, sharedCount-diffCount as netScore from users
            inner join
                (
                    SELECT "userId", COUNT(*) as sharedCount FROM reviews
                    LEFT JOIN users ON "userId" = users.id
                    WHERE ("movieId" in ("""+', '.join(likes)+""") AND "metacriticScore" > 70) OR ("movieId" in ("""+', '.join(dislikes)+""") AND "metacriticScore" < 40)
                    GROUP BY "userId"
                ) sharedReviews
            on sharedReviews."userId" = users.id
            inner join
                (
                    SELECT "userId", COUNT(*) as diffCount FROM reviews
                    LEFT JOIN users ON "userId" = users.id
                    WHERE ("movieId" in ("""+', '.join(likes)+""") AND "metacriticScore" < 30) OR ("movieId" in ("""+', '.join(dislikes)+""") AND "metacriticScore" > 70)
                    GROUP BY "userId"
                ) diffReviews
            on diffReviews."userId" = users.id
            ORDER BY netScore DESC
            LIMIT 10
        """
    print sql
    columns.append("netScore")

    result = []
    for row in db.engine.execute(sql):
        data = {}
        for i, cell in enumerate(row):
            data[ columns[i].replace('"', '') ] = cell
        result.append(data)
    return result
