from enum import Enum


class ErrorCode(Enum):
    INCOMPLETE_DATA = "incomplete_data"
    INVALID_DATA = "invalid_data"
    INVALID_OTP = "invalid_otp"
    INVALID_CREDENTIALS = "invalid_credentials"
    PHONE_ALREADY_VERIFIED = "phone_already_verified"
    PHONE_HAS_NO_VERIFY_REQUEST = "phone_has_no_verify_request"
    USER_ALREADY_EXIST = "user_already_exist"
    USER_NOT_REGISTERED = "user_not_registered"
