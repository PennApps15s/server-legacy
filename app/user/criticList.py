from app import db
from app.user.models import User
from app.review.models import Review

import json

columns = ['id', 'name', '"criticPublication"', 'average_review', 'sharedCount', 'diffCount']

upp_border = 60
low_border = 40

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
            SELECT """ +', '.join(columns)+ """,
            CAST(1.4 as float)*sharedCount-diffCount as netScore
            FROM users
            INNER JOIN
                (
                    SELECT "userId", COUNT(*) as sharedCount FROM reviews
                    LEFT JOIN users ON "userId" = users.id
                    WHERE ("movieId" in ("""+', '.join(likes)+""") AND "metacriticScore" > """+str(upp_border)+""") OR ("movieId" in ("""+', '.join(dislikes)+""") AND "metacriticScore" < """+str(low_border)+""")
                    GROUP BY "userId"
                ) sharedReviews
            on sharedReviews."userId" = users.id
            INNER JOIN
                (
                    SELECT "userId", COUNT(*) as diffCount FROM reviews
                    LEFT JOIN users ON "userId" = users.id
                    WHERE ("movieId" in ("""+', '.join(likes)+""") AND "metacriticScore" < """+str(low_border)+""") OR ("movieId" in ("""+', '.join(dislikes)+""") AND "metacriticScore" > """+str(upp_border)+""")
                    GROUP BY "userId"
                ) diffReviews
            ON diffReviews."userId" = users.id
            ORDER BY netScore DESC
            LIMIT 100
        """
    columns.append("netScore")

    result = []
    for row in db.engine.execute(sql):
        data = {}
        for i, cell in enumerate(row):
            data[ columns[i].replace('"', '') ] = cell
        result.append(data)

    scoreTotal = 0
    count = 0
    for critic in result:
        scoreTotal += critic['netScore']
        count += 1

    averageScore = float(scoreTotal) / float(count)
    print "Average Score", averageScore
    for i, critic in enumerate(result):
        result[i]['adjustedScore'] = float(critic['netScore']-averageScore)/abs(averageScore)

    return sorted(result, key=lambda k: -1 * k['adjustedScore'])[:10]
