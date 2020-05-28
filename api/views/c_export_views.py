from rest_framework.views import APIView


class ExportCView(APIView):
    def post(self, request):
        print(request.data)