from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
#db.create_all()

class JobModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    job_description = db.Column(db.String(200), nullable=False)
    emstatus = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Job(job_title = {job_title}, company = {company}, location = {location}, rating = {rating}, job_description = {job_description}, emstatus = {emstatus})"


job_put_args = reqparse.RequestParser()
job_put_args.add_argument("job_title", type=str, help="Name of the job is required", required=True)
job_put_args.add_argument("company", type=str, help="Name of the company is required", required=True)
job_put_args.add_argument("location", type=str, help="job place is required", required=True)
job_put_args.add_argument("rating", type=int, help="job place is required", required=True)
job_put_args.add_argument("job_description", type=str, help="job place is required", required=True)
job_put_args.add_argument("emstatus", type=str, help="number of hiring is required", required=True)

job_update_args = reqparse.RequestParser()
job_update_args.add_argument("job_title", type=str, help="Name of the job is required")
job_update_args.add_argument("company", type=str, help="Name of the company is required")
job_update_args.add_argument("location", type=str, help="job place is required")
job_update_args.add_argument("rating", type=int, help="job place is required")
job_update_args.add_argument("job_description", type=str, help="job place is required")
job_update_args.add_argument("emstatus", type=str, help="number of hiring is required")


resource_fields = {
    'id': fields.Integer,
    'job_title': fields.String,
    'company': fields.String,
    'location': fields.String,
    'rating': fields.Integer,
    'job_description': fields.String,
    'emstatus': fields.String
}


class Job(Resource):
    @marshal_with(resource_fields)
    def get(self, job_id):
        result = JobModel.query.filter_by(id=job_id).first()
        if not result:
            abort(404, message="cannot find job")
        return result
    
    @marshal_with(resource_fields)
    def put(self, job_id):
        args = job_put_args.parse_args()
        result = JobModel.query.filter_by(job_title='job_title', company='company').first()
        if result:
            abort(409, message="job id taken...")
        else:
            job = JobModel(id=job_id, job_title=args['job_title'], company=args['company'], location=args['location'], rating=args['rating'], job_description=args['job_description'], emstatus=args['emstatus'])
            db.session.add(job)
            db.session.commit()
            return job, 201 

    @marshal_with(resource_fields)
    def patch(self, job_id):
        args = job_update_args.parse_args()
        result = JobModel.query.filter_by(id=job_id).first()
        if not result:
            abort(404, message="job doesn't exist, cannot update")

        if args['job_title']:
            result.job_title = args['job_title']
        if args['company']:
            result.company = args['company']
        if args['location']:
            result.location = args['location']
        if args['rating']:
            result.rating = args['rating']
        if args['job_description']:
            result.job_description = args['job_description']
        if args['emstatus']:
            result.emstatus = args['emstatus']

        db.session.commit()
        
        return result

    @marshal_with(resource_fields)
    def delete(self, job_id):
        args = job_update_args.parse_args()
        result = JobModel.query.filter_by(id=job_id).first()
        if not result:
            abort(404, message="job doesn't exist")
        
        db.session.delete(result)
        db.session.commit()
        return '', 204

#api.add_resource(Helloworld, "/helloworld/<string:name>")

api.add_resource(Job, "/job/<int:job_id>")

if __name__ == "__main__":
    app.run(debug=False)