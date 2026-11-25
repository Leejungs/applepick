from marshmallow import Schema, fields, validate


class RequestNotificationSchema(Schema):
    email = fields.Email(required=True, metadata={"description": "유저 이메일"})
    product = fields.Str(required=True, metadata={"description": "등록할 상품 키 (예: iPhone 15 Pro)"})
    price = fields.Int(required=True, validate=validate.Range(min=0), metadata={"description": "지정가 (원)"})
