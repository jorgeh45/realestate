from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.syndication.views import Feed
from realestate.listing.models import Listing
from realestate.listing.forms import SearchForm, ContactForm
from constance import config


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        recentp = Listing.objects.active().order_by('-created_at')[:config.RECENTLY_ADDED]
        form = SearchForm()
        context['recent'] = recentp
        context['form'] = form
        return context


class ContactView(FormView):
    template_name = 'home/contact-us.html'
    form_class = ContactForm
    success_url = reverse_lazy('thank-you')

    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)


class ListingFeed(Feed):
    title = "Recent Listing"
    link = "/rss/"
    description = "Recent Listing"

    def items(self):
        return Listing.objects.order_by('-last_modified')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
