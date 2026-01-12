from rest_framework.throttling import UserRateThrottle

class TenCallsPerMinute(UserRateThrottle):
    rate = '10/minute'

class FiveCallsPerMinute(UserRateThrottle):
    rate = '5/minute'

class TwoCallsPerMinute(UserRateThrottle):
    rate = '2/minute'