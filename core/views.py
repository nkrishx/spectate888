from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import serializers
from .models import Match,Market,Sport,Selection
import django_filters
from rest_framework.response import Response


#Serializers
"""serializers for the model data"""
class SelectionsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Selection

class MarketsSerializer(serializers.ModelSerializer):
    selections = SelectionsSerializer(read_only=True, many=True)
    class Meta:
        fields = '__all__'
        model = Market

#Filters

class MatchFilter(django_filters.FilterSet):
    sport = django_filters.CharFilter(field_name='sport__name', lookup_expr='iexact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Match
        fields=['sport','name']
        #order_by = ['start_time']


#Views

@api_view(['GET'])
def retriveMatch(request,id):
    try:
        match = Match.objects.get(id=id)

        context_dict = {
            "id":match.id,
            "url":match.url,
            "name":match.name,
            "startTime":match.start_time.strftime("%m/%d/%Y, %H:%M:%S"),

            "sport": {
                "id":match.sport_id,
                "name":match.sport.name
            },
            "markets":MarketsSerializer(match.markets,many=True).data

        }
        return Response(context_dict)
    except Match.DoesNotExist:
        content = {'Id not found': 'Match Id not found'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

"""simgle view for handling the get request based filtering and ordering operations"""
@api_view(['GET'])
def listMatch(request,**kwargs):
    ordering_param = request.query_params.get('ordering')
    if ordering_param:
        if ordering_param.startswith('-'):
            ordering_param = '-' + ordering_param.split('-')[1]
        f = MatchFilter(request.GET, queryset=Match.objects.all().order_by(ordering_param))
        values = f.qs.values("id","url","name","start_time")
        return Response(values)
    else:
        f = MatchFilter(request.GET, queryset=Match.objects.all())
        values = f.qs.values("id","url","name","start_time")
        return Response(values)

"""view for handling the newEvent and update event type"""
@api_view(['GET','POST'])
def Event(request):
    if request.data["message_type"] == "NewEvent":
        selection_ids = []
        selections = request.data["event"]["markets"]["selections"]
        for each in selections:
            s = Selections.objects.create(**each)
            s.save()
            selection_ids.append(s)

        market = Markets()
        market.id = request.data["event"]["markets"]["id"]
        market.name = request.data["event"]["markets"]["name"]
        market.selections.add(*selection_ids)
        market.save()

        match = Match()
        match.id = request.data["event"]["id"]
        match.url = "http://127.0.0.1:8000/api/match/"+str(match.id)
        match.name = request.data["event"]["name"]
        match.start_time = datetime.strptime(request.data["event"]["startTime"], "%Y-%m-%d %H:%M")

        sport, sport_created = Sport.objects.get_or_create(id=request.data["event"]["sport"]["id"])
        if sport_created:
            sport.name = request.data["event"]["sport"]["name"]
            sport.save()

        match.sport = sport
        match.markets.add(market)
        match.save()
        return Response({"status":"success"})

    if request.data["message_type"] == "UpdateOdds":

        selections = request.data["event"]["markets"]["selections"]
        for each in selections:
            s = Selections.objects.get(id=each["id"])
            s.odds = each["odds"]
            s.save()


        return Response({"status": "success"})
