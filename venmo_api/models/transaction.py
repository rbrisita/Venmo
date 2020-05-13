from venmo_api import string_to_timestamp
from venmo_api import User
from venmo_api import get_phone_model_from_json
from venmo_api import JSONSchema


class Transaction(object):

    def __init__(self, story_id, payment_id, date_completed, date_created,
                 date_updated, payment_type, audience, status,
                 note, device_used, actor, target):

        super().__init__()

        self.id = story_id
        self.payment_id = payment_id

        self.date_completed = date_completed
        self.date_created = date_created
        self.date_updated = date_updated

        self.payment_type = payment_type
        self.audience = audience
        self.status = status

        self.note = note
        self.device_used = device_used

        self.actor = actor
        self.target = target

    @classmethod
    def from_json(cls, json):

        # Skip money transfers to/from bank accounts
        if json.get("transfer"):
            return None

        parser = JSONSchema.transaction(json)
        date_created = string_to_timestamp(parser.get_date_created())
        date_updated = string_to_timestamp(parser.get_date_updated())
        date_completed = string_to_timestamp(parser.get_date_completed())

        target = User.from_json(json=parser.get_target())
        actor = User.from_json(json=parser.get_actor())
        device_used = get_phone_model_from_json(parser.get_actor_app())

        return cls(story_id=parser.get_story_id(),
                   payment_id=parser.get_payment_id(),
                   date_completed=date_completed,
                   date_created=date_created,
                   date_updated=date_updated,
                   payment_type=parser.get_type(),
                   audience=parser.get_audience(),
                   status=parser.get_status(),
                   note=parser.get_story_note(),
                   device_used=device_used,
                   actor=actor,
                   target=target)

    def __str__(self):

        return f'story_id: {self.id}, payment_id: {self.payment_id}, date_completed: {self.date_completed},' \
            f'date_created: {self.date_created}, date_updated: {self.date_updated},' \
            f' payment_type: {self.payment_type},' \
            f'audience: {self.audience}, status: {self.status}, note: {self.note}, device_used: {self.device_used},\n' \
            f'actor_user: {self.actor},\n' \
            f'target_user: {self.target}\n'
