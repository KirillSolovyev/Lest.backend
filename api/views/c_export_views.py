from rest_framework.views import APIView
from rest_framework.response import Response


class ExportCView(APIView):
    def post(self, request):
        print(request.data)

    def get(self, request):
        return Response({"status": "OK"})
