from database import db
from models.base_model import BaseModel

class PackagingStep(BaseModel, db.Model):
    __tablename__ = 'packaging_steps'
    id = db.Column(db.Integer, primary_key=True)
    pre_fix = db.Column(db.String(50))
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id'))  # Define the foreign key
    status = db.Column(db.Integer, default=0)
    description = db.Column(db.String(150), nullable=True)
    packaging_process_id = db.Column(db.Integer, db.ForeignKey('packaging_processes.id'))
    img = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer)
    name = db.Column(db.String(100), default="")
    next_step_on_success = db.Column(db.Integer, nullable=True)
    next_step_on_failure = db.Column(db.Integer, nullable=True)
    condition = db.Column(db.Boolean, default=False)
    

    def __init__(self, pre_fix, field_id, status, description, packaging_process_id, img, order, name="", next_step_on_success=None, next_step_on_failure=None, condition=False):
        super().__init__()
        self.pre_fix = pre_fix
        self.field_id = field_id
        self.status = status
        self.description = description
        self.packaging_process_id = packaging_process_id
        self.img = img
        self.order = order
        self.name = name
        self.next_step_on_success = next_step_on_success
        self.next_step_on_failure = next_step_on_failure
        self.condition = condition

    def to_dict(self):
        return {
            'id': self.id,
            'pre_fix': self.pre_fix,
            'field_id': self.field_id,
            'status': self.status,
            'description': self.description,
            'packaging_process_id': self.packaging_process_id,
            'img': self.img,
            'order': self.order,
            'name': self.name,
            'next_step_on_success': self.next_step_on_success,
            'next_step_on_failure': self.next_step_on_failure,
            'condition': self.condition
        }
