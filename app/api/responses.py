from app.exceptions.exceptions import (
    BadParametersPassed,
    UserNotExistOrInvalid,
    NotEnoughRights,
    OrganizationNotFound,
    TenderOrBidNotFound,
    TenderNotFound,
    TenderOrVersionNotFound,
    BidNotFound,
    BidOrVersionNotFound
)


error400 = {
    "description": BadParametersPassed.detail,
    "content": {
        "application/json": {
            "example": {
                "detail": BadParametersPassed.detail
            }
        }
    }
}

error401 = {
    "description": UserNotExistOrInvalid.detail,
    "content": {
        "application/json": {
            "example": {
                "detail": UserNotExistOrInvalid.detail
            }
        }
    }
}

error403 = {
    "description": NotEnoughRights.detail,
    "content": {
        "application/json": {
            "example": {
                "detail": NotEnoughRights.detail
            }
        }
    }
}

error404_organization_not_found = {
    "description": OrganizationNotFound.detail,
    "content": {
        "application/json": {
            "example": {
                "detail": OrganizationNotFound.detail
            }
        }
    }
}

error404_tender_or_bid_not_found = {
    "description": TenderOrBidNotFound.detail,
    "content": {
        "application/json": {
            "example": {
                "detail": TenderOrBidNotFound.detail
            }
        }
    }
}

error404_tender_not_found = {
    "description": TenderNotFound.detail,
    "content": {
        "application/json": {
            "example": {
                "detail": TenderNotFound.detail
            }
        }
    }
}

error404_tender_or_version_not_found = {
    "description": TenderOrVersionNotFound.detail,
    "content": {
        "application/json": {
            "example": {
                "detail": TenderOrVersionNotFound.detail
            }
        }
    }
}

error404_bid_not_found = {
    "description": BidNotFound.detail,
    "content": {
        "application/json": {
            "example": {
                "detail": BidNotFound.detail
            }
        }
    }
}

error404_bid_or_version_not_found = {
    "description": BidOrVersionNotFound.detail,
    "content": {
        "application/json": {
            "example": {
                "detail": BidOrVersionNotFound.detail
            }
        }
    }
}

error422 = {
    "description": "Ошибка валидации",
    "content": {
        "application/json": {
            "example": {
                "detail": [
                    {"loc": ["string", 0],
                     "msg": "string",
                     "type": "string"}
                ]
            }
        }
    }
}

error500 = {
    "description": "Сервер не готов обрабатывать запросы, если ответ статусом 500 или любой другой, кроме 200."
}
