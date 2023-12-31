import logging
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from json.decoder import JSONDecodeError
from rest_framework.parsers import JSONParser
from rest_framework import views
from rest_framework.response import Response
from json import JSONDecodeError
from .utils.get_sentiment import get_sentiment
from .serializers import MessageSerializer
import json

"""
Receives post requests and serializes data, test whether data is list / string
and sends data to get_sentiment (where data gets analysed in batches or per string)
retreives either a list (batch) or a string with the result
neg=1.0 neu=0.0 pos=0.0 compound=-0.5423
"""

# Define a logger
logger = logging.getLogger(__name__)

class SentimentAPIView(APIView):
    # Add throttle classes to limit the rate of requests
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request):
        try:
            #clean up data
            data = JSONParser().parse(request)
            serializer = MessageSerializer(data=data)
            
            if serializer.is_valid():
                #extract message from data
                message_details = serializer.validated_data
                message = str(message_details['message'])
                batch_process = isinstance(message_details['message'], list)
                data, sentiment = get_sentiment(message, batch_process)
                # Add extra data to the response
                extra_data = {
                    'data_received' : data,
                    'result': sentiment,
                }
                response_data = {**message_details, **extra_data}
                return Response(response_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "JSON decoding error"}, status=400)
        except Exception as e:
            logger.error("An error occurred: %s", str(e))
            return Response({"result": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

