from venv import create
from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import glob
import os
from wtforms.validators import InputRequired
import json
import re

# Defines a custom class to handle malware STIX objects
class StixMalware:
    def __init__(self, type, spec_version, id, created, modified, name, description, malware_types, is_family, kill_chain_phases):
        self.type = type
        self.spec_version = spec_version
        self.id = id
        self.created = created
        self.modified = modified
        self.name = name
        self.description = description
        self.malware_types = malware_types
        self.is_family = is_family
        self.kill_chain_phases = kill_chain_phases

    def __str__(self):
        return f"Malware(type='{self.type}', spec_version={self.spec_version}, id={self.id}, created={self.created}, modified={self.modified}, name = {self.name}, description = {self.description}, malware_types = {self.malware_types}, is_family = {self.is_family}, kill_chain_phases = {self.kill_chain_phases})"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])





def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                  app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))  # Then save the file
        os.chdir("/Users/rohiteagala/python_projects/STIX/static/files")
        f = open("STIX.json")
        data = json.load(f)

        indicator_object = data['objects'][0]

        ioString = str(indicator_object)

        malware_object = data['objects'][1]

        moString = str(malware_object)

        relationship_object = data['objects'][2]

        roString = str(relationship_object)

        return ioString + moString + roString

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
