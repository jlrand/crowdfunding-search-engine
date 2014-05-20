# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from crowdsearch.models import Kickitems, Kickrewards, KickitemsFilterSet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max
from datetime import datetime
from django.core.cache import cache

from endless_pagination.decorators import page_template

@page_template('crowdsearch/project_list.html')  # just add this decorator
def index(request, template='crowdsearch/search.html', sort_criteria='-backers', extra_context=None):
	kickitems = KickitemsFilterSet(request.GET, queryset=Kickitems.objects.all())
	#kickitems = Kickitems.objects.all().order_by(sort_criteria)
	kickitems.header = 'Projects View'
	kickitems.current_time = datetime.now()
	
	context = {'kickitems': kickitems, 'page_template': 'crowdsearch/project_list.html',}
	if extra_context is not None:
		context.update(extra_context)
	return render_to_response(
		template, context, context_instance=RequestContext(request))

# def index(request, sort_criteria = '-pledge'):
# 	#kickitems_list = Kickitems.objects.order_by(sort_criteria)
# 	categories_list = Kickitems.objects.values('parent_category').distinct()
# 	
# 	kickitems = KickitemsFilterSet(request.GET, queryset=Kickitems.objects.all().order_by(sort_criteria))
# 	## pagination
# 
# 	kickitems.header = 'Projects View'
# 	kickitems.current_time = datetime.datetime.now()
# 
# 	return render_to_response('crowdsearch/base.html', {"kickitems": kickitems, "categories_list": categories_list},
# context_instance=RequestContext(request))

def home(request, template='crowdsearch/home.html', sort_criteria='-backers', extra_context=None):
	now = datetime.now
	new_tech = Kickitems.objects.filter(parent_category='technology').filter(end_time__gte=now()).order_by('-backers')[:4]
	under_20 = Kickitems.objects.filter(get_it_pledge_amount__lte=20).filter(end_time__gte=now()).order_by('-backers')[:4]
	most_funded = Kickitems.objects.filter(funded=1).order_by('-pledge')[:4]
	
	context = {'under_20': under_20, 'new_tech':new_tech, 'most_funded':most_funded, 'page_template': 'crowdsearch/home.html',}
	if extra_context is not None:
		context.update(extra_context)
	return render_to_response(
		template, context, context_instance=RequestContext(request))
	
def rewardsview(request, category= 'none', sort_by = 'highrollers'):
	#get all the categories so we can build a menu
	categories_list = Kickitems.objects.values('parent_category').distinct()
	
	#Figure out how we're going to be ordering the results
	if sort_by == 'backers':
	    sort_by = ['-reward_backers']
	elif sort_by == 'dollars':
		sort_by = ['-reward_times_backers']
	elif sort_by == 'highrollers':
		sort_by = ['-reward_amount','-reward_backers']
		page_title = 'Who is well connected'
	else:
		sort_by = ['-reward_text']

	#Get all the Projects along with the Reward with the highest number of backers
	kickitems = Kickitems.objects.annotate(biggest_reward_amount=Max('rewards__reward_backers'))
	#Get only the rewards that were the highest for each project
	kickitems_list = Kickrewards.objects.filter(reward_backers__in=[b.biggest_reward_amount for b in kickitems]).extra(
		select={'reward_times_backers':'reward_amount * reward_backers'},
		order_by=(sort_by)
		)
	# Filter to show only rewards with at least 1 backer
	kickitems_list = kickitems_list.filter(reward_backers__gte=1)
	
	# Filter again by category if we were passed one
	if category != 'none':
		kickitems_list = kickitems_list.filter(kickitem__parent_category=category)
				
	# pagination
	paginator = Paginator((list(kickitems_list)), 8) # Show 25 contacts per page

	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		kickitems = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		kickitems = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		kickitems = paginator.page(paginator.num_pages)
	
	#assign the name of the page and the active category
	kickitems.header = page_title
	kickitems.activecat = category
	
	#send it all to the Reward View template
	return render_to_response('crowdsearch/rewardview.html', {"kickitems": kickitems, "categories_list": categories_list})
		

def mostbackers(request, category= 'none'):
	categories_list = Kickitems.objects.values('parent_category').distinct()
	if category != 'none':
		kickitems_list = Kickitems.objects.filter(parent_category=category).order_by('-backers')
	else:
		kickitems_list = Kickitems.objects.order_by('-backers')
	
	## pagination
	paginator = Paginator(kickitems_list, 8) # Show 25 contacts per page

	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		kickitems = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		kickitems = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		kickitems = paginator.page(paginator.num_pages)
	
		
	kickitems.header = 'Most Backers'
	kickitems.activecat = category
	
	return render_to_response('crowdsearch/index.html', {"kickitems": kickitems, "categories_list": categories_list})
	

def mostfunded(request, category = 'none'):
	categories_list = Kickitems.objects.values('parent_category').distinct()
	if category != 'none':
		kickitems_list = Kickitems.objects.filter(parent_category=category).order_by('-pledge')
	else:
		kickitems_list = Kickitems.objects.order_by('-pledge')
	
	## pagination
	paginator = Paginator(kickitems_list, 8) # Show 25 contacts per page

	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		kickitems = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		kickitems = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		kickitems = paginator.page(paginator.num_pages)
		
	kickitems.header = 'Most Funded'
	kickitems.activecat = category
	
	return render_to_response('crowdsearch/index.html', {"kickitems": kickitems, "categories_list": categories_list})

def mostpopularrewards(request, category= 'none'):
	categories_list = Kickitems.objects.values('parent_category').distinct()
	if category != 'none':
		kickitems_list = Kickrewards.objects.filter(kickitem__parent_category=category).extra(
		select={'multiple':'reward_amount*reward_backers'},
		order_by=('-multiple',)
		)
	else:		
		kickitems = Kickitems.objects.annotate(biggest_reward_amount=Max('rewards__reward_backers')) 
		kickitems_list = Kickrewards.objects.filter(reward_backers__in=[b.biggest_reward_amount for b in kickitems]).extra(
		select={'reward_times_backers':'reward_amount * reward_backers'},
		order_by=('-reward_times_backers',)
		)
		
		
	# pagination
	paginator = Paginator((list(kickitems_list)), 8) # Show 25 contacts per page

	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		kickitems = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		kickitems = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		kickitems = paginator.page(paginator.num_pages)
	
		
	kickitems.header = 'Highest Earning Rewards'
	kickitems.activecat = category
	
	return render_to_response('crowdsearch/rewardview.html', {"kickitems": kickitems, "categories_list": categories_list})

def mostbackedrewards(request, category= 'none'):
	categories_list = Kickitems.objects.values('parent_category').distinct()
	if category != 'none':
		kickitems_list = Kickrewards.objects.filter(kickitem__parent_category=category).extra(
		select={'multiple':'reward_amount*reward_backers'},
		order_by=('-multiple',)
		)
	else:		
		kickitems = Kickitems.objects.annotate(biggest_reward_amount=Max('rewards__reward_backers')) 
		kickitems_list = Kickrewards.objects.filter(reward_backers__in=[b.biggest_reward_amount for b in kickitems]).extra(
		select={'reward_times_backers':'reward_amount * reward_backers'},
		order_by=('-reward_backers',)
		)
		
	# pagination
	paginator = Paginator((list(kickitems_list)), 8) # Show 25 contacts per page

	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		kickitems = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		kickitems = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		kickitems = paginator.page(paginator.num_pages)
	
		
	kickitems.header = 'Most Backed Rewards'
	kickitems.activecat = category
	
	return render_to_response('crowdsearch/rewardview.html', {"kickitems": kickitems, "categories_list": categories_list})
	#return HttpResponse(kickitems[0].kickitem)

def highrollers(request, category= 'none'):
	categories_list = Kickitems.objects.values('parent_category').distinct()
	if category != 'none':
		kickitems_list = Kickrewards.objects.filter(kickitem__parent_category=category).extra(
		select={'multiple':'reward_amount*reward_backers'},
		order_by=('-multiple',)
		)
	else:		
		kickitems = Kickitems.objects.annotate(biggest_reward_amount=Max('rewards__reward_backers')) 
		kickitems_list = Kickrewards.objects.filter(reward_backers__in=[b.biggest_reward_amount for b in kickitems]).extra(
		select={'reward_times_backers':'reward_amount * reward_backers'},
		order_by=('-reward_amount','-reward_backers',)
		)
		
		
	# pagination
	paginator = Paginator((list(kickitems_list)), 8) # Show 25 contacts per page

	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		kickitems = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		kickitems = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		kickitems = paginator.page(paginator.num_pages)
	
		
	kickitems.header = "Who is well connected?"
	kickitems.activecat = category
	
	return render_to_response('crowdsearch/rewardview.html', {"kickitems": kickitems, "categories_list": categories_list})

def mostexpensive(request, category = 'none'):
	categories_list = Kickitems.objects.values('parent_category').distinct()
	if category != 'none':
		kickitems_list = Kickitems.objects.filter(parent_category=category).extra(
		select={'divisor':'pledge/backers'},
		order_by=('-divisor',)
		)
	else:
		kickitems_list = Kickitems.objects.extra(
		select={'divisor':'pledge/backers'},
		order_by=('-divisor',)
		)
		
		
	## pagination
	paginator = Paginator(kickitems_list, 8) # Show 25 contacts per page

	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		kickitems = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		kickitems = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		kickitems = paginator.page(paginator.num_pages)
	
		
	kickitems.header = 'Highest Average Donations'
	kickitems.activecat = category
	
	return render_to_response('crowdsearch/averagereward.html', {"kickitems": kickitems, "categories_list": categories_list})