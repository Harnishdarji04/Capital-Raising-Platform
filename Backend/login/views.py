from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Info,Documents,Invest
# from .models import Profile  # Assuming you have a Profile model for userType
# Create your views here.
email1=''
password=''
def home(request):
    return render(request,'home.html')
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        email1=str(email)
        password=str(password)
        try:
            user = Info.objects.get(email=email, password=password)
            # Store email in session
            request.session['email'] = user.email
            request.session['lastname'] = user.lastname
            request.session['ustype'] = user.usertype
            request.session['password'] = user.password
            return redirect('dashboard')  # this is your dashboard view name
        except Info.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password'})

    return render(request,'login.html')
@csrf_exempt
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        user_type = request.POST.get('userType')

        # Validation checks
        if not all([first_name, last_name, email, password, confirm_password, user_type]):
            messages.error(request, "All fields are required.")
            return render(request, 'register.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if Info.objects.filter(email=email).exists():
            n= "Email is already registered."
            return render(request, 'register.html',{'n':n})
        # Create user and profile
        try:
            data=Info(firstname=first_name,lastname=last_name,email=email,password=password,usertype=user_type)
            data.save()
            return redirect('login')
        except Exception as e:
            messages.error(request, "Something went wrong: " + str(e))
            return render(request, 'register.html')
    return render(request, 'register.html')
def dashboard(request):
    # email=request.GET.get('email')
    # lastname=request.GET.get('lastname')
    # return render(request,'finaldashboard.html',{'email':email,'lastname':})
    email = request.session.get('email')
    lastname = request.session.get('lastname')
    ustype = request.session.get('ustype')
    hs=Invest.objects.filter(email=email)
    if not email:
        return redirect('login')  # session expired or not logged in
    return render(request,'pdashboard.html',{'email': email,'lastname':lastname,'ustype':ustype,'hs':hs})
def profile(request):
    email=request.session.get('email')
    lastname = request.session.get('lastname')
    ustype = request.session.get('ustype')
    return render(request,'user-profile.html',{'lastname':lastname,'ustype':ustype})


def projectdashboard(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        location = request.POST.get('location')
        search_query = request.POST.get('search')  # the text input
        lastname = request.session.get('lastname')
        ustype = request.session.get('ustype')
        # You can now use these to filter your data
        print("Industry:", category)
        print("Location:", location)
        print("Search:", search_query)

        # Example: filter Company model (if exists)
        companies = Documents.objects.all()
        if search_query:
            companies = companies.filter(company_name__icontains=search_query)
        if category:
            companies = companies.filter(industry=category)
        if location:
            companies = companies.filter(company_origin=location)

        return render(request, 'projectlistings.html', {'lastname':lastname,'ustype':ustype,'company': companies})
    else:
        lastname = request.session.get('lastname')
        ustype = request.session.get('ustype')
        company=Documents.objects.all() 
        return render(request,'projectlistings.html',{'lastname':lastname,'ustype':ustype,'company':company})



def submitcompany(request):
    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        # form = DocumentForm(request.POST, request.FILES)
        # if form.is_valid():
        #     form.save()
        risk_list = request.POST.getlist('risk_factors')
        risk_combined = ','.join(risk_list)
        company_name=data['company_name']
        company_logo=files.get('image')
        industry=data['industry']
        industry_other=data.get('company_origin')
        company_origin=data['company_origin']
        year_founded=data['year_founded']
        description=data['description']
        problem_solution=data['problem_solution']
        competitive_advantage=data['competitive_advantage']
        funding_goal=data['funding_goal']
        valuation=data['valuation']
        equity_offered=data['equity_offered']
        funding_deadline=data['funding_deadline']
        min_investment=data['min_investment']
        risk_factors=risk_combined
        risk_other_specify=data.get('risk_other_specify')
        revenue_2023=data.get('revenue_2023')
        profit_2023=data.get('profit_2023')
        assets_2023=data.get('assets_2023')
        revenue_2022=data.get('revenue_2022')
        profit_2022=data.get('profit_2022')
        assets_2022=data.get('assets_2022')
        revenue_2021=data.get('revenue_2021')
        profit_2021=data.get('profit_2021')
        assets_2021=data.get('assets_2021')
        pitch_deck=files.get('pitch_deck')
        financial_statements=request.FILES.get('financial')
        legal_documents=files.get('legal')
        additional_materials=files.get('additional')
        app = Documents(
            company_name=company_name,
            company_logo= company_logo,
            industry=industry,
            company_origin=company_origin,
            year_founded=year_founded,
            description=description,
            problem_solution=problem_solution,
            competitive_advantage=competitive_advantage,
            funding_goal=funding_goal,
            valuation=valuation,
            equity_offered=equity_offered,
            funding_deadline=funding_deadline,
            min_investment=min_investment,
            risk_factors=risk_factors,

            revenue_2023=revenue_2023,
            profit_2023=profit_2023,
            assets_2023=assets_2023,
            revenue_2022=revenue_2022,
            profit_2022=profit_2022,
            assets_2022= assets_2022,
            revenue_2021=revenue_2021,
            profit_2021=profit_2021,
            assets_2021=assets_2021,

            pitch_deck=pitch_deck,
            financial_statements= financial_statements,
            legal_documents=legal_documents,
            additional_materials=additional_materials,
        )
        app.save()
        return redirect('pdashboard')
    return render(request, 'form.html')

def companydetail(request,id):
    lastname = request.session.get('lastname')
    ustype = request.session.get('ustype')
    details=get_object_or_404(Documents,pk=id)
    request.session['cname']=details.company_name
    request.session['cimage']=details.company_logo.url
    request.session['invest']=details.equity_offered
    request.session['funding']=details.funding_goal
    request.session['industry']=details.industry
    if request.method=='post':
        return redirect('invest')
    return render(request,'companydetails.html',{'detail':details,'lastname':lastname,'ustype':ustype})


def invest(request):
    cname=request.session.get('cname')
    lastname = request.session.get('lastname')
    info=Documents.objects.get(company_name=cname)
    return render(request,'investmentpage.html',{'info':info,'lastname':lastname})

def history(request):
    company_id = request.POST.get('company_id')
    info = get_object_or_404(Documents, pk=company_id)

    # Save selected company in session for current user
    request.session['selected_company_id'] = company_id

    lastname = request.session.get('lastname')
    inf = Info.objects.get(lastname=lastname)
    fname = inf.firstname
    cd = request.POST.get('payment_method')

    # Check if user has already invested in this company
    already_invested = Invest.objects.filter(
        lastname=lastname,
        companyname=info.company_name
    ).exists()

    if not already_invested:
        # Save investment entry
        data = Invest(
            firstname=fname,
            lastname=lastname,
            email=inf.email,
            companyname=info.company_name,
            company_logo=info.company_logo,
            industry=info.industry,
            amount=info.funding_goal,
            equity=info.equity_offered,
            valuation=info.valuation,
            method=cd,
            pitch_deck=info.pitch_deck,
            financial_statements=info.financial_statements,
            legal_documents=info.legal_documents,
            additional_materials=info.additional_materials
        )
        data.save()
        return render(request, 'payment.html', {
        'info': info,
        'method': cd,
        })
    else:
        return render(request, 'payment.html', {
        'info': info,
        'method': cd,
        })
def investments(request):
    lastname = request.session.get('lastname')
    email = request.session.get('email')
    hs=Invest.objects.filter(email=email)
    ustype = request.session.get('ustype')
    return render(request, 'pipage.html', {'details': hs, 'lastname':lastname,'ustype':ustype})

def network(request):
    return render(request,'coming-soon.html')