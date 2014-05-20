from django.db import models
import datetime
import django_filters



# Create your models here.
	
class Kickitems(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300L, blank=True)
    url = models.CharField(max_length=200L, blank=True)
    imageurl = models.CharField(max_length=200L, unique=True, blank=True)
    smallimageurl = models.CharField(max_length=200L, unique=True, blank=True)
    thumbimageurl = models.CharField(max_length=200L, unique=True, blank=True)
    location = models.CharField(max_length=45L, blank=True)
    parent_category = models.CharField(db_index=True, max_length=45L, blank=True)
    backers = models.IntegerField(db_index=True)
    average_reward = models.IntegerField()
    percent_funded = models.IntegerField()
    funded = models.BooleanField(db_index=True)
    funding_period = models.CharField(max_length=200L, blank=True)
    category = models.CharField(max_length=45L, blank=True)
    currency = models.CharField(max_length=20L, blank=True)
    pledge = models.DecimalField(db_index=True, null=True, max_digits=12, decimal_places=2, blank=True)
    get_it_pledge_amount = models.DecimalField(db_index=True, null=True, max_digits=12, decimal_places=2, blank=True)
    goal = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    site = models.CharField(max_length=200L, blank=True)
    short_description = models.CharField(max_length=400L, blank=True)
    search_text = models.CharField(max_length=1000L, blank=True)
    get_it_reward_id = models.IntegerField()
    def currency_stem(self):
		if self.currency == "CAD":
			return "CAD"
		if self.currency == "AUD":
			return "AUD"
		if self.currency == "NZD":
			return "NZD"
		else:
			return ""
    def currency_symbol(self):
		if self.currency == "USD":
			return "$"
		if self.currency == "CAD":
			return "$"
		if self.currency == "GBP":
			return "&pound;"
		if self.currency == "EUR":
			return "&euro;"
		if self.currency == "AUD":
			return "$"
		if self.currency == "NZD":
			return "$"
    def is_active(self):
        return self.end_time > datetime.datetime.now()
    def is_funded(self):
        return self.pledge >= self.goal
    def days_left(self):
		a = self.end_time
		b = datetime.datetime.now()
		delta = a - b
		if delta.days > 0:
			if delta.days > 1:
				return str(delta.days) + " days"
			else:
				return str(delta.days) + " day"
		if delta.seconds/3600 >= 1:
			if delta.seconds/3600 > 1:
				return str(delta.seconds/3600) + " hours"
			else:
				return str(delta.seconds/3600) + " hour"
		else:
			if delta.seconds > 60:
				return str(delta.seconds/60) + " minutes"
			else:
				return str(delta.seconds) + " seconds"
    class Meta:
        db_table = 'kickitems'
        verbose_name_plural = 'kickitems'
    def __unicode__(self):
        return self.name
    def get_most_popular_reward(self):
       	return Kickrewards.objects.get(pk=self.get_it_reward_id)

class Kickrewards(models.Model):
    id = models.IntegerField(primary_key=True)
    reward_amount = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)
    reward_text = models.CharField(max_length=300L, blank=True)
    reward_backers = models.CharField(max_length=45L, blank=True)
    kickitem = models.ForeignKey(Kickitems, db_column='kickitem', related_name='rewards')
    class Meta:
        db_table = 'kickrewards'
        verbose_name_plural = 'kickrewards'
    
    def __unicode__(self):
        return self.reward_text
        
    def _total_reward_dollars(self):
       return self.reward_amount * self.reward_backers
    total_reward_dollars = property(_total_reward_dollars)
    


class KickitemsFilterSet(django_filters.FilterSet):
	# FILTER_CHOICES = (
# 	('', 'Any'),
# 	('Art', 'Art'),
# 	('Design', 'Design'),
# 	('Technology', 'Technology'),
# 	)
	BACKER_CHOICES = (
		('', 'Any Number of Backers'),
		('50', 'Over 50 Backers'),
		('100', 'Over 100 Backers'),
		('500', 'Over 500 Backers'),
		('1000', 'Over 1,000 Backers'),
		('2000', 'Over 2,000 Backers'),
		('5000', 'Over 5,000 Backers'),
		('10000', 'Over 10,000 Backers'),
		)
	CATEGORY_CHOICES = (
		('', 'All Categories'),
		('Design', 'Design'),
		('Technology', 'Technology'),
		('Art', 'Art'),
		('Food', 'Food'),
		('Theater', 'Theater'),
		('Comics', 'Comics'),
		('Dance', 'Dance'),
		('Fashion', 'Fashion'),
		('Film & Video', 'Film & Video'),
		('Games', 'Games'),
		('Music', 'Music'),
		('Photography', 'Photography'),
		('Publishing', 'Publishing'),
		)

	PLEDGED_CHOICES = (
		('', 'Any Amount Pledged'),
		('100', 'Over $100 Pledged'),
		('500', 'Over $500 Pledged'),
		('1000', 'Over $1,000 Pledged'),
		('2000', 'Over $2,500 Pledged'),
		('5000', 'Over $5,000 Pledged'),
		('10000', 'Over $10,000 Pledged'),
		('25000', 'Over $25,000 Pledged'),
		('50000', 'Over $50,000 Pledged'),
		('100000', 'Over $100,000 Pledged'),
		('200000', 'Over $250,000 Pledged'),
		('500000', 'Over $500,000 Pledged'),
		('1000000', 'Over $1,000,000 Pledged'),
		)
	REWARD_PRICE_CHOICES = (
		('', 'All Reward Amounts'),
		('10', 'Under $10'),
		('20', 'Under $20'),
		('50', 'Under $50'),
		('100', 'Under $100'),
		('200', 'Under $200'),
		('500', 'Under $500'),
		('1000', 'Under $1,000'),
		)
	SITE_CHOICES = (
		('', 'All Sites'),
		('Kickstarter','Kickstarter'),
		('Indiegogo','Indiegogo'),
		)
	STATUS_CHOICES = (
		('', 'Any Funded Status'),
		('0', 'Unfunded Projects Only'),
		('1', 'Successfully Funded Only'),
		)
	ACTIVE_CHOICES = (
		('', 'Active or Completed'),
		('1', 'Only Active Projects'),
		('0', 'Only Completed Projects'),
		)
	get_it_pledge_amount = django_filters.RangeFilter()
	pledge = django_filters.ChoiceFilter(lookup_type='gt', choices=PLEDGED_CHOICES)
	#pledge = django_filters.RangeFilter()
	backers = django_filters.ChoiceFilter(lookup_type='gt', choices=BACKER_CHOICES)
	#backers = django_filters.RangeFilter()
	#parent_category = django_filters.AllValuesFilter()
	parent_category = django_filters.ChoiceFilter(choices = CATEGORY_CHOICES)
	site = django_filters.ChoiceFilter(choices = SITE_CHOICES)
	search_text = django_filters.CharFilter(lookup_type='search')
	funded = django_filters.ChoiceFilter(choices= STATUS_CHOICES)
	end_time = django_filters.DateRangeFilter()
	#end_time = django_filters.DateRangeFilter(widget = django_filters.widgets.LinkWidget)
	
	class Meta:
		model = Kickitems
		fields = ['search_text', 'parent_category', 'get_it_pledge_amount', 'funded', 'backers', 'pledge', 'site', 'end_time']
		order_by = (
		#('', 'Order by Relevance'),
		('-backers', 'Order by Most Popular'),
		('-pledge', 'Order by Most Funded'),
		('-percent_funded', 'Order by Percent Funded'),
		('-get_it_pledge_amount', 'Order by Price: High to Low'),
 		('get_it_pledge_amount', 'Order by Price: Low to High'),
		#('-average_reward', 'Order by Ave Pledge Desc'),
		#('average_reward', 'Order by Ave Pledge Asc'),
		#('-end_time', 'Order by Most Recent'),
		#('end_time', 'Order by Oldest First'),
		#('name', 'Order Alphabetically')
		)
		
	def __init__(self, *args, **kwargs):
		super(KickitemsFilterSet, self).__init__(*args, **kwargs)
		self.filters['get_it_pledge_amount'].label="Filter by Price Range"
		self.filters['backers'].label="Filter by Number of Backers"
		self.filters['pledge'].label="Filter by Dollars Pledged"
		self.filters['parent_category'].label="Category"
		self.filters['search_text'].label=""
		self.filters['end_time'].label="End Time"
		self.filters['funded'].label="Funded Status"
		self.filters['site'].label="Site"
		

	