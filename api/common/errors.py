from enum import Enum


class ErrorCode(Enum):
    INCOMPLETE_DATA = "incomplete_data"
    INVALID_DATA = "invalid_data"
    INVALID_OTP = "invalid_otp"
    INVALID_CREDENTIALS = "invalid_credentials"
    PHONE_ALREADY_VERIFIED = "phone_already_verified"
    PHONE_HAS_NO_VERIFY_REQUEST = "phone_has_no_verify_request"
    USER_ALREADY_EXIST = "user_already_exist"
    NO_SUCH_USER = "no_such_user"
    NOT_LOGGED_IN = "user_not_logged_in"
    NOT_FOUND = "not_found"
    STORE_NOT_FOUND = "store_not_found"
    STORE_ITEM_NOT_FOUND = "store_item_not_found"
    PRODUCT_NOT_FOUND = "product_not_found"
    NEW_PASSWORD_SAME_AS_OLD = "new_password_same_as_old"
    WEAK_PASSWORD = "weak_password"
