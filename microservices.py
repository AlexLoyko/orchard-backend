from flask import Flask, Response, request
from db import DBsession, Restaurant, Inspection
from sqlalchemy import desc, asc, and_, or_
from assign_data_to_fieldnames import assign_data_to_fieldnames

app = Flask(__name__)


@app.route('/best-places', methods=['GET'])
def best_places():
    cuisine = request.args.get('cuisine', default='thai', type=str)
    session = DBsession()
    most_recent_best = session.query(Restaurant.id, Restaurant.name,         \
                                     Restaurant.building, Restaurant.street, \
                                     Restaurant.boro, Restaurant.cuisine,    \
                                     Inspection.rest_id, Inspection.grade,   \
                                     Inspection.grade_date)                  \
                              .join(Inspection, Restaurant.id == Inspection.rest_id) \
                              .filter(Restaurant.cuisine.contains(cuisine.upper())) \
                              .filter(and_(and_(Inspection.score >= 0, Inspection.score <= 27, or_(Inspection.grade == 'A', Inspection.grade == 'B')))) \
                              .order_by(desc(Inspection.grade_date))              \
                              .order_by(asc(Inspection.score))                     \
                              .distinct()   \
                              .limit(10)    \
                              .all()

    res = assign_data_to_fieldnames(most_recent_best)
    session.close()
    return Response(res, mimetype='application/json')

app.run(host='0.0.0.0')
