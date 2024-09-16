from app.exceptions.base_exception import BaseExceptions


class BadParametersPassed(BaseExceptions):
    status_code: int = 400
    detail: str = "Данные неправильно сформированы или не соответствуют требованиям"


class UserNotExistOrInvalid(BaseExceptions):
    status_code: int = 401
    detail: str = "Пользователь не существует или некорректен"


class NotEnoughRights(BaseExceptions):
    status_code: int = 403
    detail: str = "Недостаточно прав для выполнения действия"


class OrganizationNotFound(BaseExceptions):
    status_code: int = 404
    detail: str = "Организация не существует"


class TenderOrBidNotFound(BaseExceptions):
    status_code: int = 404
    detail: str = "Тендер или предложение не найдено"


class TenderNotFound(BaseExceptions):
    status_code: int = 404
    detail: str = "Тендер не найден"


class TenderOrVersionNotFound(BaseExceptions):
    status_code: int = 404
    detail: str = "Тендер или версия не найдены"


class BidNotFound(BaseExceptions):
    status_code: int = 404
    detail: str = "Предложение не найдено"


class BidOrVersionNotFound(BaseExceptions):
    status_code: int = 404
    detail: str = "Предложение или версия не найдены"
