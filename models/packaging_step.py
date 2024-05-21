from database import db

class PackagingStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pre_fix = db.Column(db.String(50))
    field_id = db.Column(db.Integer, db.ForeignKey('field.id'))  # Define the foreign key
    status = db.Column(db.Integer, default=0)
    description = db.Column(db.String(150))
    packaging_process_id = db.Column(db.Integer, db.ForeignKey('packaging_process.id'))
    img = db.Column(db.String(200))
    order = db.Column(db.Integer)

    def __init__(self, pre_fix, field, status, description, packaging_process_id, img, order):
        self.pre_fix = pre_fix
        self.field = field
        self.status = status
        self.description = description
        self.packaging_process_id = packaging_process_id
        self.img = img
        self.order = order

    def to_dict(self):
        return {
            'id': self.id,
            'pre_fix': self.pre_fix,
            'field': self.field,
            'status': self.status,
            'description': self.description,
            'packaging_process_id': self.packaging_process_id,
            'img': self.img,
            'order': self.order
        }
