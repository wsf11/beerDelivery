# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
import urllib.request
import json
import requests
from .forms import LoginForm, SignUpForm, TripForm, TripCreate, OrderForm, OrderCreate, SearchForm
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import datetime
from elasticsearch import Elasticsearch
from django.utils.timezone import utc

def login_required(fun):
	def wrap(request,*args,**kwargs):
		try: 
			auth = request.COOKIES.get('auth')
			name = request.COOKIES.get('name')
			data = {'auth':auth, 'name':name}
			endpoint = "http://exp-api:8000/checkAuth/"

			req = requests.post(endpoint, data = data)
			# next = reverse("index")
			# return HttpResponseRedirect(next)
			message = (req.content).decode()
			data2 = json.loads(message)
			# name = data['name']
			# age = data['age']
			# username = data['username']
			if 'status' in data2 and data2['status'] == 200:
			    return fun(request,*args,**kwargs)
			else:
				return HttpResponseRedirect("/login/")

		except: 
			return HttpResponseRedirect("/login/")
	return wrap

def index(request):
	try:
		auth = request.COOKIES.get('auth')
		name = request.COOKIES.get('name')
		# auth_time = request.COOKIES.get('auth_time')
		# person = Person.object.get(pk=auth.user_id)
		return render(request, 'index.html', context={'username': name, 'auth': auth})

	except:
		return render(request, 'index.html', context={})

@login_required
def getPerson(request,pk = None):
	try: 
		auth = request.COOKIES.get('auth')
		endpoint = "http://exp-api:8000/person/" + str(pk)
		req = urllib.request.Request(endpoint)
		response = urllib.request.urlopen(req).read().decode('utf-8')
		data = json.loads(response)
		name = data['name']
		age = data['age']
		return render(request,'person_detail_view.html',context={'name':name,'age':age,'auth':auth})
	except: 
		obj = 'Person'
		return render(request,'no_exist.html',context={'object':obj,'auth':auth})

@login_required
def getOrder(request,pk = None):
	try:
		auth = request.COOKIES.get('auth')
		endpoint = "http://exp-api:8000/order/" + str(pk)
		req = urllib.request.Request(endpoint)
		response = urllib.request.urlopen(req).read().decode('utf-8')
		data = json.loads(response)
		buyer = data['buyer']
		item = data['item']
		trip = data['order_trip']
		return render(request,'order_detail_view.html',context={'buyer':buyer,'item':item,'auth':auth,'order_trip':trip})
	except: 
		obj = 'Order'
		return render(request,'no_exist.html',context={'object':obj,'auth':auth})

@login_required
def getTrip(request,pk = None,name=None):
	try:
		auth = request.COOKIES.get('auth')
		name = request.COOKIES.get('name')
		endpoint = "http://exp-api:8000/trip/" + str(pk) + '/' + str(name)
		req = urllib.request.Request(endpoint)
		response = urllib.request.urlopen(req).read().decode('utf-8')
		data = json.loads(response)
		runner = data['runner']
		store = data['store']
		time_created = data['time']
		active = data['active']

		orders = data['orders']

		url = str(name) + "/endTrip"

		rec_trips = data['rec_trips']
		return render(request,'trip_detail_view.html',context={'runner':runner,'store':store,'time_created':time_created,'active':active,'auth':auth, 'url':url, 'name':name,'orders':orders,'rec_trips':rec_trips})
	except: 
		# obj = 'Trip'
		return render(request,'no_exist.html',context={'object':obj,'auth':auth})

@login_required
def getBeer(request,pk = None):
	try:
		auth = request.COOKIES.get('auth')
		endpoint = "http://exp-api:8000/beer/" + str(pk)
		req = urllib.request.Request(endpoint)
		response = urllib.request.urlopen(req).read().decode('utf-8')
		data = json.loads(response)
		name = data['name']
		size = data['size']
		price = data['price']
		beer_type = data['beer_type']
		bottle_type = data['bottle_type']
		return render(request,'beer_detail_view.html',context={'name':name,'age':size,'price':price,'bottle_type':bottle_type,'beer_type':beer_type,'auth':auth})
	except: 
		obj = 'Beer'
		return render(request,'no_exist.html',context={'object':obj,'auth':auth})

@login_required
def getStore(request,pk = None):
	try:
		auth = request.COOKIES.get('auth')
		endpoint = "http://exp-api:8000/store/" + str(pk)
		req = urllib.request.Request(endpoint)
		response = urllib.request.urlopen(req).read().decode('utf-8')
		data = json.loads(response)
		name = data['name']
		location = data['location']
		inventory = data['inventory']
		return render(request,'store_detail_view.html',context={'name':name,'location':location,'inventory':inventory,'auth':auth})
	except: 
		obj = 'Store'
		return render(request,'no_exist.html',context={'object':obj,'auth':auth})

@login_required
def getAllPeople(request, pk = None):
	auth = request.COOKIES.get('auth')
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
	return render(request, 'people.html', context={'full_list':full_list,'auth':auth})

@login_required
def getAllBeers(request, pk = None):
	auth = request.COOKIES.get('auth')
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
	return render(request, 'beers.html', context={'full_list':full_list,'auth':auth})

def getAllBeersList():
	endpoint = "http://exp-api:8000/beer/all"
	req = urllib.request.Request(endpoint)
	response = urllib.request.urlopen(req).read().decode('utf-8')
	data = json.loads(response)	
	new_list = data
	full_list = []
	for keys in new_list:
		endpoint2 = "http://exp-api:8000/beer/" + str(keys)
		req2 = urllib.request.Request(endpoint2)
		response2 = urllib.request.urlopen(req2).read().decode('utf-8')
		data2 = json.loads(response2)
		name = data2['name']
		full_list.append(name)
	choices = ()
	for values in full_list:
		tup = (str(values), str(values))
		choices = choices + (tup,)
	return choices

@login_required
def getAllStores(request, pk = None):
	auth = request.COOKIES.get('auth')
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
	return render(request, 'stores.html', context={'full_list':full_list,'auth':auth})

def getAllStoresList():
	endpoint = "http://exp-api:8000/store/all"
	req = urllib.request.Request(endpoint)
	response = urllib.request.urlopen(req).read().decode('utf-8')
	data = json.loads(response)	
	new_list = data
	full_list = []
	for keys in new_list:
		endpoint2 = "http://exp-api:8000/store/" + str(keys)
		req2 = urllib.request.Request(endpoint2)
		response2 = urllib.request.urlopen(req2).read().decode('utf-8')
		data2 = json.loads(response2)
		name = data2['name']
		full_list.append(name)
	choices = ()
	for values in full_list:
		tup = (str(values), str(values))
		choices = choices + (tup,)
	return choices

@login_required
def getAllTrips(request, pk = None):
	auth = request.COOKIES.get('auth')
	nameToken = request.COOKIES.get('name')
	endpoint = "http://exp-api:8000/trip/all"
	req = urllib.request.Request(endpoint)
	response = urllib.request.urlopen(req).read().decode('utf-8')
	data = json.loads(response)	
	new_list = data
	full_list = {}
	for keys in new_list:
		endpoint2 = "http://exp-api:8000/trip2/" + str(keys)
		req2 = urllib.request.Request(endpoint2)
		response2 = urllib.request.urlopen(req2).read().decode('utf-8')
		data2 = json.loads(response2)
		name = data2['runner']
		full_list[keys] = name
	return render(request, 'trips.html', context={'full_list':full_list,'auth':auth,'name':nameToken})



@login_required
def getMyTrips(request, pk = None):
	auth = request.COOKIES.get('auth')
	nameToken = request.COOKIES.get('name')
	endpoint = "http://exp-api:8000/trip/all"
	req = urllib.request.Request(endpoint)
	response = urllib.request.urlopen(req).read().decode('utf-8')
	data = json.loads(response)	
	new_list = data
	full_list = {}
	for keys in new_list:
		endpoint2 = "http://exp-api:8000/trip2/" + str(keys)
		# endpoint2 = "http://exp-api:8000/trip/" + str(keys) + '/' + str(nameToken)
		req2 = urllib.request.Request(endpoint2)
		response2 = urllib.request.urlopen(req2).read().decode('utf-8')
		data2 = json.loads(response2)
		name = data2['runner']
		if nameToken == name:
			full_list[keys] = name
	return render(request, 'trips.html', context={'full_list':full_list,'auth':auth, 'name':nameToken})

@login_required
def getActiveTrips(request, pk = None):
	auth = request.COOKIES.get('auth')
	nameToken = request.COOKIES.get('name')
	endpoint = "http://exp-api:8000/trip/all"
	req = urllib.request.Request(endpoint)
	response = urllib.request.urlopen(req).read().decode('utf-8')
	data = json.loads(response)	
	new_list = data
	full_list = {}
	for keys in new_list:
		# endpoint2 = "http://exp-api:8000/trip/" + str(keys)  + '/' + str(nameToken)
		endpoint2 = "http://exp-api:8000/trip2/" + str(keys)
		req2 = urllib.request.Request(endpoint2)
		response2 = urllib.request.urlopen(req2).read().decode('utf-8')
		data2 = json.loads(response2)
		name = data2['runner']
		active = data2['active']
		if active == True:
			full_list[keys] = name
	return render(request, 'trips.html', context={'full_list':full_list,'auth':auth, 'name':nameToken})

def getAllTripsList():
	endpoint = "http://exp-api:8000/trip/all"
	req = urllib.request.Request(endpoint)
	response = urllib.request.urlopen(req).read().decode('utf-8')
	data = json.loads(response)	
	new_list = data
	full_list = []
	for keys in new_list:
		endpoint2 = "http://exp-api:8000/trip2/" + str(keys)
		req2 = urllib.request.Request(endpoint2)
		response2 = urllib.request.urlopen(req2).read().decode('utf-8')
		data2 = json.loads(response2)
		name = data2['runner']
		# full_list[keys] = name
		active = data2['active']
		trip_id = data2['trip_id']
		if active == True:
			full_list.append(trip_id)
		choices = ()
		for values in full_list:
			tup = (str(values), str(values))
			choices = choices + (tup,)
	return choices

@login_required
def getAllOrders(request, pk = None):
	auth = request.COOKIES.get('auth')
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
		name = data2['buyer']
		full_list[keys] = name
	return render(request, 'orders.html', context={'full_list':full_list,'auth':auth})

@login_required
def getMyOrders(request, pk = None):
	auth = request.COOKIES.get('auth')
	name = request.COOKIES.get('name')
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
		buyer = data2['buyer']
		if name == buyer:
			full_list[keys] = buyer
	return render(request, 'orders.html', context={'full_list':full_list,'auth':auth})


@login_required
def createTrip(request):
	name = request.COOKIES.get('name')
	auth = request.COOKIES.get('auth')
	next = reverse('index')
	# CHOICES = (("Food Lion","Food Lion"), ("Kroger", "Kroger"))
	CHOICES = getAllStoresList()
	if not auth:
		response = HttpResponseRedirect(next)
	if request.method == 'GET':
		form = TripForm(allStores = CHOICES)
		return render(request, 'tripForm.html', {'form': form,'auth':auth})
	form2 = TripCreate(store = request.POST['store'])
	#if form2.is_valid():
	try:
			data = request.POST.copy()
			data['name'] = name
			store = data['store']
			# name = name
			endpoint = "http://exp-api:8000/createTrip/"
			req = requests.post(endpoint, data = data)
			status = req.status_code
			message = (req.content).decode()
			resp = json.loads(message)
			if resp['status'] != 200:
				form = TripForm(allStores = CHOICES)
				error = resp['error']
				return render(request,'tripForm.html',{'form':form,'error':resp['status'],'auth':auth})

			response = HttpResponseRedirect(next)
			return response
			# request.method = "GET"
			# return getTrip(request, pk = data['pk'])
	except:
		return render(request, 'tripForm.html', context={'error': message,'auth':auth})
	#return render(request, 'tripForm.html', context={'error': 'Pete is dead!'})

@login_required
#@old_cookie_logout
def createOrder(request, pk = None):
	try:
		name = request.COOKIES.get('name')
		auth = request.COOKIES.get('auth')
		next = reverse('index')
		BEER_CHOICES = getAllBeersList()
		TRIP_CHOICES = getAllTripsList()
		if not auth:
			response = HttpResponseRedirect(next)
		if request.method == 'GET':
			form = OrderForm(allBeers = BEER_CHOICES, allTrips = TRIP_CHOICES)
			return render(request, 'orderForm.html', {'form':form,'auth':auth})
		form2 = OrderCreate(beer = request.POST['beer'],trip = request.POST['trip'])
	except:
		return render(request, 'orderForm.html', context={'error': TRIP_CHOICES})
	try:
		data = request.POST.copy()
		data['name'] = name
		beer = data['beer']
		trip = data['trip']
		data['trip_id'] = trip 
		endpoint = "http://exp-api:8000/createOrder/"

		req = requests.post(endpoint, data = data)
		status = req.status_code
		message = (req.content).decode()
		resp = json.loads(message)
		if resp['status'] != 200:
			form = OrderForm(allStores = CHOICES)
			error = resp['error']
			return render(request,'orderForm.html',{'form':form,'error':resp['status'],'auth':auth})

		response = HttpResponseRedirect(next)
		return response
		# request.method = "GET"
		# return getTrip(request, pk = data['pk'])
	except:
		return render(request, 'orderForm.html', context={'error': data})



@csrf_exempt
# @logout_required
def login(request, pk = None):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			try:
				data = request.POST.copy()
				username = data['username']
				endpoint = "http://exp-api:8000/login/"
				req = requests.post(endpoint, data=data)
				status = req.status_code
				message = (req.content).decode()
				resp = json.loads(message)
				if resp['status'] != 200:
					form = LoginForm()
					error = resp['error']
					return render(request,'login.html',{'form':form,'error':resp})

				next = reverse('index')
				if 'next' in form:
					next = form.cleaned_data.get('next')

				response = HttpResponseRedirect(next)
				response.set_cookie("auth",resp['auth'])
				response.set_cookie("name",resp['name'])

				return response

			except: 
				error = 'Invalid User Credentials'
				return render(request,'login.html',{'form':form,'error':error})
	else:
		form = LoginForm()

	return render(request,'login.html',{'form':form})

@csrf_exempt
# @logout_required
def signup(request, pk = None):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			try:
				error = 1
				data = request.POST.copy()
				username = data['username']
				error = 4
				endpoint = "http://exp-api:8000/signup/"
				req = requests.post(endpoint, data = data)
				status = req.status_code
				error = 5
				message = (req.content).decode()
				error = message
				resp = json.loads(message)
				error = 2
				if resp['status'] != 200:
					form = SignUpForm()
					error = resp['error']
					return render(request,'signup.html',{'form':form,'error':error})

				next = reverse('index')
				error = 3
				if 'next' in form:
					next = form.cleaned_data.get('next')

				response = HttpResponseRedirect(next)
				response.set_cookie("auth",resp['auth'])
				response.set_cookie("name",resp['name'])

				return response

			except: 
				# error = 'User already exists. Please try another username.'
				return render(request,'signup.html',{'form':form,'error':error})
	else:
		form = SignUpForm()
		return render(request,'signup.html',{'form':form})

@csrf_exempt
@login_required
def logout(request):
	next = reverse('login')
	response = HttpResponseRedirect(next)
	data = {}
	auth_cookie = request.COOKIES.get('auth')
	data['auth_cookie'] = auth_cookie
	endpoint = "http://exp-api:8000/logout/"
	req = requests.post(endpoint, data = data)
	status = req.status_code
	message = (req.content).decode()
	resp = json.loads(message)
	if resp['status'] != 200:
		error = resp['error']
		return render(request,'index.html',{'error':message})

	response = HttpResponseRedirect(next)
	response.delete_cookie('auth')
	response.delete_cookie('name')
	return response

@csrf_exempt
@login_required
def EndTrip(request,pk = None, name=None):
	try:
		obj = 1
		auth = request.COOKIES.get('auth')
		name = request.COOKIES.get('name')
		obj = 2
		endpoint = "http://exp-api:8000/trip/" + str(pk) + '/' + str(name) + "/endTrip"
		obj = 5
		req = urllib.request.Request(endpoint)
		obj = 6
		response = urllib.request.urlopen(req).read().decode('utf-8')
		obj = 3
		data = json.loads(response)
		obj = 4
		runner = data['runner']
		store = data['store']
		time_created = data['time']
		active = data['active']
		return render(request,'trip_detail_view.html',context={'runner':runner,'store':store,'time_created':time_created,'active':active,'auth':auth})
	except: 
		# obj = 'Trip'
		return render(request,'no_exist.html',context={'object':obj,'auth':auth})

@csrf_exempt
def search(request):
	if request.method == 'POST':
		auth = request.COOKIES.get('auth')
		form = SearchForm(request.POST)
		if True:
			try:
				data = request.POST.copy()
				query = data['all']
				search_field = data['search']
				endpoint = "http://exp-api:8000/search/"
				req = requests.post(endpoint, data = data)
				status = req.status_code
				message = (req.content).decode()
				resp = json.loads(message)
				if 'error'  not in resp:
					if search_field == "Trip":
						info = resp['search']
						# trip_id = info['trip_id']
						# url = "/trip/"+ str(trip_id)
						return render(request, 'search_trips.html', context={'full_list':info, 'auth':auth})

						# return HttpResponseRedirect(url)
					elif search_field == "Order":
						info = resp['search']
						# order_id = info['order_id']
						# url = "/order/"+ str(order_id)
						# return HttpResponseRedirect(url)
						return render(request, 'search_orders.html', context={'full_list':info, 'auth':auth})
					else:
						info = resp['search']
						# person_id = info['person_id']
						# url = "/person/"+ str(person_id)
						# return HttpResponseRedirect(url)
						return render(request, 'search_people.html', context={'full_list':info, 'auth':auth})
				else:
					if search_field == "Trip":
						obj = 'Trip'
					elif search_field == "Order":
						obj = 'Order'
					else:
						obj = 'Person'
					return render(request,'no_exist.html',context={'object':obj,'auth':auth})
			except:
				try:
					return render(request, 'index.html', context={'error': resp['error']})
				except:
					return render(request, 'index.html', context={'error': 'Empty Kafka', 'auth':auth})

		else:
			return render(request, 'index.html', context={'error': request.POST})

