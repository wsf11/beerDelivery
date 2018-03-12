# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
import urllib.request
import json

def index(request):
	# req = urllib.request.Request('http://exp-api:8000/index/')
	# response = urllib.request.urlopen(req).read().decode('utf-8')
	# data = json.loads(response)
	# string = "HERE--- " + req
	return render(request, 'index.html', context={})

def getPerson(request,pk = None):
	try: 
		endpoint = "http://exp-api:8000/person/" + str(pk)
		req = urllib.request.Request(endpoint)
		response = urllib.request.urlopen(req).read().decode('utf-8')
		data = json.loads(response)
		name = data['name']
		age = data['age']
		return render(request,'person_detail_view.html',context={'name':name,'age':age})
	except: 
		obj = 'Person'
		return render(request,'no_exist.html',context={'object':obj})

def getOrder(request,pk = None):
	try:
		endpoint = "http://exp-api:8000/order/" + str(pk)
		req = urllib.request.Request(endpoint)
		response = urllib.request.urlopen(req).read().decode('utf-8')
		data = json.loads(response)
		buyer = data['buyer']
		item = data['item']
		return render(request,'order_detail_view.html',context={'buyer':buyer,'item':item})
	except: 
		obj = 'Order'
		return render(request,'no_exist.html',context={'object':obj})

def getTrip(request,pk = None):
	try:
		endpoint = "http://exp-api:8000/trip/" + str(pk)
		req = urllib.request.Request(endpoint)
		response = urllib.request.urlopen(req).read().decode('utf-8')
		data = json.loads(response)
		runner = data['runner']
		store = data['store']
		time_created = data['time']
		active = data['active']
		return render(request,'trip_detail_view.html',context={'runner':runner,'store':store,'time_created':time_created,'active':active,})
	except: 
		obj = 'Trip'
		return render(request,'no_exist.html',context={'object':obj})

def getBeer(request,pk = None):
	try:
		endpoint = "http://exp-api:8000/beer/" + str(pk)
		req = urllib.request.Request(endpoint)
		response = urllib.request.urlopen(req).read().decode('utf-8')
		data = json.loads(response)
		name = data['name']
		size = data['size']
		price = data['price']
		beer_type = data['beer_type']
		bottle_type = data['bottle_type']
		return render(request,'beer_detail_view.html',context={'name':name,'age':size,'price':price,'bottle_type':bottle_type,'beer_type':beer_type})
	except: 
		obj = 'Beer'
		return render(request,'no_exist.html',context={'object':obj})

def getStore(request,pk = None):
	try:
		endpoint = "http://exp-api:8000/store/" + str(pk)
		req = urllib.request.Request(endpoint)
		response = urllib.request.urlopen(req).read().decode('utf-8')
		data = json.loads(response)
		name = data['name']
		location = data['location']
		inventory = data['inventory']
		return render(request,'store_detail_view.html',context={'name':name,'location':location,'inventory':inventory})
	except: 
		obj = 'Store'
		return render(request,'no_exist.html',context={'object':obj})


def getAllPeople(request, pk = None):
	endpoint = "http://exp-api:8000/person/all"
	req = urllib.request.Request(endpoint)
	response = urllib.request.urlopen(req).read().decode('utf-8')
	data = json.loads(response)	
	new_list = data
	full_list = {}
	for keys in new_list:
		endpoint2 = "http://exp-api:8000/person/" + str(keys)
		req2 = urllib.request.Request(endpoint2)
		response2 = urllib.request.urlopen(req2).read().decode('utf-8')
		data2 = json.loads(response2)
		name = data2['name']
		full_list[name] = keys
	return render(request, 'people.html', context={'full_list':full_list})

def getAllBeers(request, pk = None):
	endpoint = "http://exp-api:8000/beer/all"
	req = urllib.request.Request(endpoint)
	response = urllib.request.urlopen(req).read().decode('utf-8')
	data = json.loads(response)	
	new_list = data
	full_list = {}
	for keys in new_list:
		endpoint2 = "http://exp-api:8000/beer/" + str(keys)
		req2 = urllib.request.Request(endpoint2)
		response2 = urllib.request.urlopen(req2).read().decode('utf-8')
		data2 = json.loads(response2)
		name = data2['name']
		full_list[name] = keys
	return render(request, 'beers.html', context={'full_list':full_list})

def getAllStores(request, pk = None):
	endpoint = "http://exp-api:8000/store/all"
	req = urllib.request.Request(endpoint)
	response = urllib.request.urlopen(req).read().decode('utf-8')
	data = json.loads(response)	
	new_list = data
	full_list = {}
	for keys in new_list:
		endpoint2 = "http://exp-api:8000/store/" + str(keys)
		req2 = urllib.request.Request(endpoint2)
		response2 = urllib.request.urlopen(req2).read().decode('utf-8')
		data2 = json.loads(response2)
		name = data2['name']
		full_list[name] = keys
	return render(request, 'stores.html', context={'full_list':full_list})

def getAllTrips(request, pk = None):
	endpoint = "http://exp-api:8000/trip/all"
	req = urllib.request.Request(endpoint)
	response = urllib.request.urlopen(req).read().decode('utf-8')
	data = json.loads(response)	
	new_list = data
	full_list = {}
	for keys in new_list:
		endpoint2 = "http://exp-api:8000/trip/" + str(keys)
		req2 = urllib.request.Request(endpoint2)
		response2 = urllib.request.urlopen(req2).read().decode('utf-8')
		data2 = json.loads(response2)
		name = data2['runner']
		full_list[name] = keys
	return render(request, 'trips.html', context={'full_list':full_list})

def getAllOrders(request, pk = None):
	endpoint = "http://exp-api:8000/order/all"
	req = urllib.request.Request(endpoint)
	response = urllib.request.urlopen(req).read().decode('utf-8')
	data = json.loads(response)	
	new_list = data
	full_list = {}
	for keys in new_list:
		endpoint2 = "http://exp-api:8000/order/" + str(keys)
		req2 = urllib.request.Request(endpoint2)
		response2 = urllib.request.urlopen(req2).read().decode('utf-8')
		data2 = json.loads(response2)
		name = data2['order']
		full_list[name] = keys
	return render(request, 'orders.html', context={'full_list':full_list})






