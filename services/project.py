from models.project import Project
from flask import jsonify


class ProjectService:

    def get_all_project(self):
        projects = Project.query.all()
        project_dicts = [project.to_dict() for project in projects]
        return jsonify(project_dicts)
