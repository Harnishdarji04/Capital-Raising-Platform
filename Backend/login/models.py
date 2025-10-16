from django.db import models

class Info(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=50, default='investor')

    def _str_(self):
        return self.firstname


class Documents(models.Model):
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='logos/')
    industry = models.CharField(max_length=100)
    company_origin = models.CharField(max_length=100)
    year_founded = models.DateField()
    description = models.TextField()
    problem_solution = models.TextField()
    competitive_advantage = models.TextField()
    funding_goal = models.FloatField()
    valuation = models.FloatField()
    equity_offered = models.FloatField()
    funding_deadline = models.DateField()
    min_investment = models.FloatField()
    risk_factors = models.TextField(blank=True)
    revenue_2023 = models.FloatField(blank=True, null=True)
    profit_2023 = models.FloatField(blank=True, null=True)
    assets_2023 = models.FloatField(blank=True, null=True)
    revenue_2022 = models.FloatField(blank=True, null=True)
    profit_2022 = models.FloatField(blank=True, null=True)
    assets_2022 = models.FloatField(blank=True, null=True)
    revenue_2021 = models.FloatField(blank=True, null=True)
    profit_2021 = models.FloatField(blank=True, null=True)
    assets_2021 = models.FloatField(blank=True, null=True)

    pitch_deck = models.FileField(upload_to='documents/')
    financial_statements = models.FileField(upload_to='documents/')
    legal_documents = models.FileField(upload_to='documents/', blank=True, null=True)
    additional_materials = models.FileField(upload_to='documents/', blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.company_name


class Invest(models.Model):
    user = models.ForeignKey(Info, on_delete=models.CASCADE, null=True, blank=True)

    # Investor details
    firstname = models.CharField(max_length=100,null=True)
    lastname = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True)
    companyname=models.CharField(max_length=255,null=True)
    company_logo = models.ImageField(upload_to='logos/',null=True)
    industry=models.CharField(max_length=50,null=True)
    amount=models.FloatField(null=True)
    equity=models.FloatField(null=True)
    valuation = models.FloatField(null=True)
    method = models.CharField(max_length=100,null=True)
    # Link to selected company
    company = models.ForeignKey('Documents', on_delete=models.CASCADE,null=True)

    # Uploaded documents
    pitch_deck = models.FileField(upload_to='pitch_decks/',null=True)
    financial_statements = models.FileField(upload_to='financials/',null=True)
    legal_documents = models.FileField(upload_to='legal_docs/',null=True)
    additional_materials = models.FileField(upload_to='extras/', blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.firstname} {self.lastname} - {self.company.name}"