from django.conf import settings


if settings.DEBUG is False:
    #facebook information 
    FACEBOOK_APP_ID = '125675444184887'
    FACEBOOK_API_KEY = '125675444184887'
    FACEBOOK_APP_SECRET = '6ea513bf09efe971bdd533b8c853c82b'


    #twitter information
    CONSUMER_KEY = 'WSKcN7DBwH88GkZc2wT24g'
    CONSUMER_SECRET = 'VF1eDbszUthnUrMy3693dU2iSWCK4qQBfvmreCXdhGU'

else:
    #facebook information 
    FACEBOOK_APP_ID = '202475996473036'
    FACEBOOK_API_KEY = '202475996473036'
    FACEBOOK_APP_SECRET = 'd379eb66ef57dca6714b81c8a4afd23f'

    #twitter information
    CONSUMER_KEY = '8S4oIhhl7ap5lboUk6N8w'
    CONSUMER_SECRET = '8rEgNAbwXXecrPweEPyaT5Oproxwj31ZAAb0qvgAuY'

SUPPORT_PASSWORD = 'aew7Seey'