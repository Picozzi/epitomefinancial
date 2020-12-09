from django.shortcuts import render
from django.http import JsonResponse
from .models import Security, Account
import pandas as pd
from .api_utils import create_stock_table, create_sector_information, chart_colour_picker, portfolio_value_chart, get_all_user_account_security
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

def home (request):
    return render(request, 'portfolio_viewer/home.html')

@login_required
def dashboard(request):

    current_user = request.user
    query = get_all_user_account_security(current_user)
    security_queryset = Security.objects.filter(query).values()
    
    df = pd.DataFrame(security_queryset)

    tickers = df['ticker_symbol'].tolist()
    share_count = df['num_shares'].tolist()

    if request.method == 'POST':
        route = request.POST.get('dataset')
        date_val, data_arr = portfolio_value_chart(route, tickers, share_count)

        response = {
            'date_val' : date_val,
            'data_arr' : data_arr,
            'PortViewCol' : chart_colour_picker(len(tickers)),
            'tickers' : tickers
        }

        return JsonResponse(response)

    sector_labels, sector_data = create_sector_information(tickers)

    df_subset, total = create_stock_table(tickers, df)

    df_subset = df_subset.rename(columns={'ticker_symbol': 'Symbol', 'companyName': 'Name', 'latestPrice' : 'Price', 'changePercent' : '% Change', 'change' : 'Change',
    'num_shares' : 'Shares', 'purchase_price' : 'Purchase Price', 'Total_Initial_Cost': 'Total Cost', 'Current_Value_Adjusted_Shares' : 'Market Value', 
    'Security_Overall_Gain' : 'Gain', 'Change_Adjusted_Shares' : 'Day\'s Gain', 'Security_Overall_Return_Percentage' : 'Return (%)'})

    date_val, data_arr = portfolio_value_chart('1m', tickers, share_count)

    context = {
        'PerformanceTodayNum' : round(total.Change_Adjusted_Shares,2),
        'PerformanceTodayPercent' : round((total.Change_Adjusted_Shares/total.Previous_Close_Adjusted_Shares) * 100, 2),
        'OverallReturnNum' : round(total.Security_Overall_Gain, 2),
        'OverallReturnPercent' : round((total.Security_Overall_Gain/total.Total_Initial_Cost) * 100,2),
        'PortfolioCost' : round(total.Total_Initial_Cost,2),
        'PortfolioValue' : round(total.Current_Value_Adjusted_Shares,2),
        'MainTable' : df_subset.to_html(classes=["table table-hover table-striped text-center table-bordered"], table_id="main_table"),
        'SectorPieLabels' : sector_labels,
        'SectorPieData' : sector_data,
        'SectorPieColours' : chart_colour_picker(len(sector_data)),
        'default_date_val' : date_val,
        'default_data_arr' : data_arr,
        'default_PortViewCol' : chart_colour_picker(len(tickers)),
        'default_tickers' : tickers
    }

    return render(request, 'portfolio_viewer/dashboard.html', context)

class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['name', 'account_type', 'brokerage', 'cash_balance']
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class AccountListView(ListView):
    model = Account
    context_object_name = 'accounts'

    def get_queryset (self):
        user = self.request.user
        return Account.objects.filter(owner = user).order_by('name')

class AccountDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Account

    def test_func(self):
        account = self.get_object()
        if self.request.user == account.owner:
            return True
        return False

class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Account
    fields = ['name', 'account_type', 'brokerage', 'cash_balance']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        account = self.get_object()
        if self.request.user == account.owner:
            return True
        return False

class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Account
    success_url = '/account/'
    def test_func(self):
        account = self.get_object()
        if self.request.user == account.owner:
            return True
        return False

class SecurityCreateView(LoginRequiredMixin, CreateView):
    model = Security
    fields = ['name', 'ticker_symbol', 'num_shares', 'security_type', 'date_of_purchase', 'purchase_price', 'account']
    
class SecurityListView(LoginRequiredMixin, ListView):
    model = Security
    context_object_name = 'securities'

    def get_queryset(self):
        user = self.request.user
        query = get_all_user_account_security(user)
        return Security.objects.filter(query).order_by('account', '-date_of_purchase')

class SecurityDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Security

    def test_func(self):
        security = self.get_object()
        if self.request.user == security.account.owner:
            return True
        return False

class SecurityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Security
    fields = ['name', 'ticker_symbol', 'num_shares', 'security_type', 'date_of_purchase', 'purchase_price', 'account']
    
    def test_func(self):
        security = self.get_object()
        if self.request.user == security.account.owner:
            return True
        return False

class SecurityDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Security
    success_url = '/security/'
    def test_func(self):
        security = self.get_object()
        if self.request.user == security.account.owner:
            return True
        return False