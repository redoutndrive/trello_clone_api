from django.http import Http404, QueryDict
from django.db.models import Q
from rest_framework import permissions, status, generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from api.serializers import *


class Cards(APIView):
    parser_classes = (JSONParser,)

    def get_record(self, unique_number):
        try:
            return Card.objects.get(uniqueNumber=unique_number)
        except Card.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        data = Card.objects.all()
        serializer = CardSerializer(data, many=True)
        return Response(serializer.data)

    def put(self, request, format=None):
        # print(request.user, request.password)
        try:
            unique_number = request.data['uniqueNumber']
        except KeyError:
            return Response({'missing field': 'uniqueNumber'}, status=status.HTTP_400_BAD_REQUEST)

        record = self.get_record(unique_number)
        serializer = CardSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = CardSerializer(data=request.data)
        # serializer = CardSerializer(data=request.query_params)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            unique_number = request.data['uniqueNumber']
        except KeyError:
            return Response({'missing field': 'uniqueNumber'}, status=status.HTTP_400_BAD_REQUEST)

        record = self.get_record(unique_number)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Comments(APIView):

    def get(self, request, format=None):
        data = Comment.objects.all()
        serializer = CommentSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        # serializer = CardSerializer(data=request.query_params)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):

    def get_record(self, comment_id):
        try:
            return Comment.objects.get(id=comment_id)
        except Card.DoesNotExist:
            raise Http404

    def get(self, request, comment_id):
        data = self.get_record(comment_id)
        serializer = CommentSerializer(data)
        return Response(serializer.data)

    def delete(self, request, comment_id):
        record = self.get_record(comment_id)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CardComments(APIView):

    def get_record(self, cardid):
        try:
            return Comment.objects.filter(reference_card=cardid)
        except Card.DoesNotExist:
            raise Http404

    def get(self, request, cardid):
        data = self.get_record(cardid)
        serializer = CommentSerializer(data, many=True)
        return Response(serializer.data)


class CardDetails(APIView):
    parser_classes = (JSONParser,)

    def get_record(self, cardid):
        try:
            return Card.objects.get(uniqueNumber=cardid)
        except Card.DoesNotExist:
            raise Http404

    def get(self, request, cardid, format=None):
        record = self.get_record(cardid)
        serializer = CardSerializer(record)
        return Response(serializer.data)


class Boards(APIView):
    parser_classes = (JSONParser,)

    def get_record(self, boardId):
        try:
            return Board.objects.get(id=boardId)
        except Board.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        data = Board.objects.filter(Q(owner=self.request.user) | Q(public_access=True))
        serializer = BoardSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            boardId = request.data['id']
        except KeyError:
            return Response({'missing field': 'id'}, status=status.HTTP_400_BAD_REQUEST)

        record = self.get_record(boardId)
        serializer = BoardSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            boardId = request.data['id']
        except KeyError:
            return Response({'missing field': 'id'}, status=status.HTTP_400_BAD_REQUEST)

        record = self.get_record(boardId)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Tables(APIView):
    parser_classes = (JSONParser,)

    def get_record(self, table_id):
        try:
            return Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        data = Table.objects.all()
        serializer = TableSerializer(data, many=True)
        return Response(serializer.data)

    def put(self, request, format=None):
        try:
            id = request.data['id']
        except KeyError:
            return Response({'missing field': 'id'}, status=status.HTTP_400_BAD_REQUEST)

        record = self.get_record(id)
        serializer = TableSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            id = request.data['id']
        except KeyError:
            return Response({'missing field': 'id'}, status=status.HTTP_400_BAD_REQUEST)

        record = self.get_record(id)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BoardTables(APIView):
    parser_classes = (JSONParser,)

    def get(self, request, id, format=None):
        records = Table.objects.filter(boardID=id)
        serializer = TableSerializer(records, many=True)
        return Response(serializer.data)


class ArchiveCards(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get(self, request, format=None):
        records = Card.objects.filter(archiveStatus=True)
        serializer = CardSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request, cardid, format=None):
        # params = dict(request.query_params)
        try:
            record = Card.objects.get(uniqueNumber=cardid)
            # print(record.title, record.archiveStatus)
            record.archiveStatus = True
            record.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            # print(e)
            return Response({'Exception': e}, status=status.HTTP_400_BAD_REQUEST)


class TableContents(APIView):
    parser_classes = (JSONParser,)

    def get(self, request, tableid, format=None):
        records = Card.objects.filter(tableID=tableid, archiveStatus=False)
        serializer = CardSerializer(records, many=True)
        return Response(serializer.data)


class UserList(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSignUp(APIView):

    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)

    def post(self, request):
        # print(request.data['username'], request.data['email'], request.data['password'])
        try:
            User.objects.create_user(request.data['username'], request.data['email'], request.data['password'])
        except Exception as e:
            return Response({'Server exception': str(e.__cause__)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)
