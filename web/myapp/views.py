# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
import urllib.request
import json
import requests
from .forms import LoginForm, SignUpForm, TripForm, TripCreate, OrderForm, OrderCreate
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

def login_required(fun):
	def wrap(request,*args,**kwargs):
		try: 
			auth = request.COOKIES.get('auth')
			name = request.COOKIES.get('name')
			data = {'auth':auth, 'name':name}
			endpoint = "http://exp-api:8000/checkAuth/"
			req = requests.post(endpoint, data = data)
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
		# person = Person.object.get(pk=auth.user_id)
		return render(request, 'index.html', context={'username': name, 'auth': auth})

	except:
		return render(request, 'index.html', context={})

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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
		full_list[keys] = name
	return render(request, 'trips.html', context={'full_list':full_list})

@login_required
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
		return render(request, 'tripForm.html', {'form': form})
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
				return render(request,'tripForm.html',{'form':form,'error':resp['status']})

			response = HttpResponseRedirect(next)
			return response
			# request.method = "GET"
			# return getTrip(request, pk = data['pk'])
	except:
		return render(request, 'tripForm.html', context={'error': "No post"})
	#return render(request, 'tripForm.html', context={'error': 'Pete is dead!'})

@login_required
def createOrder(request, pk = None):
	name = request.COOKIES.get('name')
	auth = request.COOKIES.get('auth')
	next = reverse('index')
	CHOICES = getAllBeersList()
	if not auth:
		response = HttpResponseRedirect(next)
	if request.method == 'GET':
		form = OrderForm(allBeers = CHOICES)
		return render(request, 'orderForm.html', {'form':form})
	form2 = OrderCreate(beer = request.POST['beer'])
	try:
		data = request.POST.copy()
		data['name'] = name
		beer = data['beer']
		endpoint = "http://exp-api:8000/createOrder/"
		req = requests.post(endpoint, data = data)
		status = req.status_code
		message = (req.content).decode()
		resp = json.loads(message)


		if resp['status'] != 200:
			form = OrderForm(allStores = CHOICES)
			error = resp['error']
			return render(request,'orderForm.html',{'form':form,'error':resp['status']})

		response = HttpResponseRedirect(next)
		return response
		# request.method = "GET"
		# return getTrip(request, pk = data['pk'])
	except:
		return render(request, 'orderForm.html', context={'error': message})



@csrf_exempt
def login(request, pk = None):
	# try:
	# 	auth = request.COOKIES.get('auth')
	# 	name = request.COOKIES.get('name')
	# 	if auth:
	# 		next = reverse('index')
	# 		response = HttpResponseRedirect(next)

	# 	return response

	# except auth.DoesNotExist:
	# 	return None

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
def signup(request, pk = None):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			try:
				data = request.POST.copy()
				username = data['username']
				endpoint = "http://exp-api:8000/signup/"
				req = requests.post(endpoint, data = data)
				status = req.status_code
				message = (req.content).decode()
				resp = json.loads(message)
				if resp['status'] != 200:
					form = SignUpForm()
					error = resp['error']
					return render(request,'signup.html',{'form':form,'error':error})

				next = reverse('index')
				if 'next' in form:
					next = form.cleaned_data.get('next')

				response = HttpResponseRedirect(next)
				response.set_cookie("auth",resp['auth'])
				response.set_cookie("name",resp['name'])

				return response

			except: 
				error = 'User already exists. Please try another username.'
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



