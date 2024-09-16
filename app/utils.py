
def model_to_dict(model, *exclude_fields):
    return {
        column.name: getattr(model, column.name)
        for column in model.__table__.columns
        if column.name not in exclude_fields
    }
