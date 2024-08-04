from models.segment import Segment
from database import db

class SegmentService:
    @staticmethod
    def get_all_segments():
        return Segment.query.all()

    @staticmethod
    def get_segment_by_id(segment_id):
        return Segment.query.get(segment_id)

    @staticmethod
    def create_segment(name, project_id, sum_of_hc_of_lines):
        new_segment = Segment(name=name, project_id=project_id, sum_of_hc_of_lines=sum_of_hc_of_lines)
        db.session.add(new_segment)
        db.session.commit()
        return new_segment

    @staticmethod
    def update_segment(segment_id, name=None, project_id=None, sum_of_hc_of_lines=None):
        segment = Segment.query.get(segment_id)
        if segment is None:
            return None
        if name:
            segment.name = name
        if project_id:
            segment.project_id = project_id
        if sum_of_hc_of_lines:
            segment.sum_of_hc_of_lines = sum_of_hc_of_lines
        db.session.commit()
        return segment

    @staticmethod
    def delete_segment(segment_id):
        segment = Segment.query.get(segment_id)
        if segment:
            db.session.delete(segment)
            db.session.commit()
            return True
        return False
