import requests, re
import json
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Scraper
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models import Value, FloatField

class ScraperAPI(View):
    def get(self, *args, **kwargs):
      scrapper_list = list(Scraper.objects.values().annotate(value=Value('0', output_field=FloatField())))
      content = requests.get('https://coinmarketcap.com/')
      for item in scrapper_list:
        p = re.compile(r'<a href="/currencies/'+item['currency'].lower().replace(" ","-")+'/markets/" class="cmc-link">(.*?)</a>')
        result = p.findall(content.text)
        value = 0
        if result :
          value = result[0].replace('$','')
        item['value']=value
        
      print(scrapper_list)
      return JsonResponse({"scrapers": scrapper_list}, safe=False)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
      return super(ScraperAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
      data = request.body.decode('utf8')
      data = json.loads(data)
      try:
        new_scrapper = Scraper(currency=data["currency"], frequency=data["frequency"])
        new_scrapper.save()
        return JsonResponse( model_to_dict(new_scrapper), safe=False)
      except:
        return JsonResponse({"error": "dato no valido"}, safe=False)

    def put(self, request, *args, **kwargs):
      data = request.body.decode('utf8')
      data = json.loads(data)
      pk = data["id"]
      try:
        new_scrapper = Scraper.objects.get(pk=pk)
        data_key = list(data.keys())
        for key in data_key:
          if key == "frequency":
            new_scrapper.frequency = data[key]
        new_scrapper.save()
        return JsonResponse({"msg": "Scraper updated"}, safe=False)
      except:
        return JsonResponse({"error": "Dato no valido"}, safe=False)        

    def delete(self, request, *args, **kwargs):
      data = request.body.decode('utf8')
      data = json.loads(data)
      pk = data["id"]
      try:
        new_scrapper = Scraper.objects.get(pk=pk)
        new_scrapper.delete()
        return JsonResponse({"msg": "Scraper deleted"}, safe=False)
      except:
        return JsonResponse({"error": "Primary Key no valido"}, safe=False)  
