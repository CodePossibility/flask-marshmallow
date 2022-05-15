from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
import copy


app = Flask(__name__)
ma = Marshmallow(app)

project_status = ['CREATED', 'PROGRESS', 'CLOSED']
project_size = ['SMALL', 'MEDIUM', 'LARGE']

class ProjectResponseSchema(Schema):
    ProjectId = fields.Integer()
    Name = fields.Str()

class AddProjectRequestSchema(Schema):
    Name = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    Status = fields.Str(required=True, validate=validate.OneOf(project_status))
    NoOfUsers = fields.Integer(required=True)
    Size = fields.Str(required=True, validate=validate.OneOf(project_size))
    Memory = fields.Integer(required=True)

    @validates("NoOfUsers")
    def validate_NoOfUsers(self, value):
        if value < 10 or value > 20:
            raise ValidationError("NoOfUsers should be between 10 and 20")

    @validates_schema
    def validate_size_memory(self, data, **kwargs):
        errors_dict = {}
        if data['Size'] == 'SMALL' and (data['Memory'] < 0 or data['Memory'] > 100):
            # raise ValidationError('For "SMALL" size, Memory should be between 0 and 100')
            errors_dict['Memory'] = 'For "SMALL" size, Memory should be between 0 and 100'
        elif data['Size'] == 'MEDIUM' and (data['Memory'] < 100 or data['Memory'] > 200):
            # raise ValidationError('For "MEDIUM" size, Memory should be between 100 and 200')
            errors_dict['Memory'] = 'For "MEDIUM" size, Memory should be between 100 and 200'

        raise ValidationError(errors_dict)


@app.route('/project', methods=['GET', 'POST'])
def project():

    if request.method == 'GET':
        project_response_dict = {
            'ProjectId': 1,
            'Name': 'Bangalore Phase 1'
        }
        
        return ProjectResponseSchema().dump(project_response_dict)
    elif request.method == 'POST':
        errors = AddProjectRequestSchema().validate(request.json)
        
        if errors:
            return errors, 422

        # load will do both validation and loading
        project_request_dict = AddProjectRequestSchema().load(request.json)

        project_response_dict = copy.deepcopy(project_request_dict)

        return project_response_dict


if __name__ == '__main__':
    app.run(debug=True)