from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .forms import Complaint_form,CreateUserForm,Student_form,Feedback_form
from .models import Complaint,Feedback,Student,Hod
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from .decorators import is_student_decorator,is_hod_decorator
from .filters import ProductFilter
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.db.models import Q


# Create your views here.
@login_required(login_url='/login')
def home(request):
        return render(request,'home.html')

@login_required(login_url='/login')
@is_student_decorator
def addcomplaint(request):
        form = Complaint_form()
        comp_success =""

        if request.method == 'POST':
                form = Complaint_form(request.POST)
        if form.is_valid():
                f1 = form.save(commit=False)
                f1.owner = request.user
                f1.save()
                form = Complaint_form()
                comp_success ="Success"
        context = {'form':form,'comp_success':comp_success}
        return render(request,'kk.html',context)

def registerPage(request):
        form = CreateUserForm()
        stu_form = Student_form()
        success =""
        if request.method == 'POST':
                form = CreateUserForm(request.POST)
                stu_form = Student_form(request.POST)
                if form.is_valid() and stu_form.is_valid():
                        user = form.save()
                        student = stu_form.save(commit = False)
                        student.user = user
                        student.save()
                        form = CreateUserForm()
                        stu_form = Student_form()
                        success = "Registered Successfully.Go to Login Page."
        context = {'form':form,'stu_form':stu_form,'success':success}                
        return render(request,'register.html',context)
        
def loginPage(request):
        if request.method == 'POST':
                
                username = request.POST.get('username')
                password = request.POST.get('password')

                user = authenticate(username=username,password=password)

                if user is not None:
                        login(request, user)
                        try:
                                c_user = Student.objects.get(user=request.user)
                        except Student.DoesNotExist:
                                c_user = None
                        if c_user is None:

                                try:
                                        c_user = Hod.objects.get(user=request.user)
                                except Hod.DoesNotExist:
                                        c_user = None
                        request.session['role'] = c_user._meta.object_name
                        return redirect('home')
                else:
                        messages.info(request, 'Incorrect Username or Password')

        return render(request,'login.html')
        

def logoutUser(request):
        request.session.flush()
        logout(request)
        return redirect('login')
        

@login_required(login_url='/login')
@is_hod_decorator
def detail(request):
       
        coms = Complaint.objects.all()#.exclude(status = 'RJ')
        f = ProductFilter(request.GET, queryset=coms)
        coms = f.qs
        coms = enumerate(coms,start = 1)
        return render(request,'detail.html',{'coms':coms,'f':f}) 
@login_required(login_url='/login')
def detailed(request, id):
        if id:
                ob = Complaint.objects.get(pk=id)
                return render(request,'detailed.html',{'ob':ob})
@login_required(login_url='/login')
def delete(request, id):
        if id:
                ob = Complaint.objects.get(pk=id)
                ob.delete()
                return HttpResponseRedirect(reverse('detail'))

@login_required(login_url='/login')
def profile(request):
        form = CreateUserForm(instance = request.user)
        stu_form = Student_form(instance = request.user)
        success =""
        if request.method == 'POST':
                form = CreateUserForm(request.POST,instance = request.user)
                stu_form = Student_form(request.POST,instance = request.user)
                if form.is_valid() and stu_form.is_valid():
                        user = form.save()
                        student = stu_form.save(commit = False)
                        student.user = user
                        student.save()
        
        return render(request,'profile.html',{'form':form,'stu_form':stu_form})
@login_required(login_url='/login')
def feedback(request, id):

        try:
                feed = Feedback.objects.get(comp_id_id = id)    
        except Feedback.DoesNotExist:
                feed = None
        ob = Complaint.objects.get(pk=id)
        if feed:
                form = Feedback_form(instance = feed)
        else:
                form = Feedback_form()
               # context = {'form':form}
               #return render(request,'feedback.html',context)
               # if request.method == 'POST' and id:
                    #    form = Feedback_form(request.POST,instance = feed)
                     #   if form.is_valid():
                       #         ob = Complaint.objects.get(pk=id)
                       #         f1 = form.save(commit=False)
                       #         f1.comp_id = ob
                       #         f1.save()
                       #         return HttpResponseRedirect(reverse('detailed',args=[id]))
        #form = Feedback_form()
        if request.method == 'POST' and id:
                if feed:
                        form = Feedback_form(request.POST,instance = feed)
                else:
                        form =Feedback_form(request.POST)
                if form.is_valid():
                        ob = Complaint.objects.get(pk=id)
                        f1 = form.save(commit=False)
                        f1.comp_id = ob
                        f1.save()
                        return HttpResponseRedirect(reverse('detailed',args=[id]))


        context = {'form':form}
        return render(request,'feedback.html',context)



@login_required(login_url='/login')
def changestatus(request, id):
        if id:
                ob = Complaint.objects.get(pk=id)
                if ob.status == 'PN':
                        ob.status = 'SO'
                else:
                        ob.status = 'PN'
                ob.save()        
                return HttpResponseRedirect(reverse('detailed',args=[id]))
@login_required(login_url='/login')
def mycomplaint(request):
        coms = Complaint.objects.all().filter(owner_id = request.user.id)
        coms = enumerate(coms,start = 1)
        return render(request,'mycomplaint.html',{'coms':coms}) 
@login_required(login_url='/login')
def reject(request, id):
        if id:
                ob = Complaint.objects.get(pk=id)
                ob.status = 'RJ'
                ob.save()        
                return HttpResponseRedirect(reverse('detail'))
@login_required(login_url='/login')               
def mydetailed(request, id):
        if id:
                try:
                        feed = Feedback.objects.get(comp_id_id = id)    
                except Feedback.DoesNotExist:
                        feed = None
                ob = Complaint.objects.get(pk=id)
                return render(request,'mydetailed.html',{'ob':ob,'feed':feed})
@login_required(login_url='/login')
def reopen(request, id):
        if id:
                try:
                        ob = Complaint.objects.get(pk=id)
                except Complaint.DoesNotExist:
                        ob = None
                form = Complaint_form(instance = ob)
                comp_success =""
                if request.method == 'POST':
                        form = Complaint_form(request.POST, instance = ob)
                if form.is_valid():
                        form.save()
                        ob.status = 'PN'
                        ob.save()
                        comp_success ="Success"
                        return render(request,'kk.html',{'comp_success':comp_success})
                        
                context = {'form':form}
                return render(request,'kk.html',context)




def ppdf(request):

        start_date="2022-03-05"
        end_date="2021-04-03"
        all_objects = Complaint.objects.filter(c_date__range=(start_date, end_date)).values_list('id','status','branch__branch','category__category')
        all_objects = [(id, replace_status(status), branch__name,category) for id, status, branch__name,category in all_objects]
        table_data = [['Id','Status','Branch','Category' ]] + list(all_objects)


        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)

        elements = []

    # Create a table with the data.
        table = Table(table_data,colWidths=[75, 140])
        table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        elements.append(table)

        doc.build(elements)

        return response
def replace_status(status):
        name_mapping = {
        'PN': 'Pending',
        'RJ': 'Rejected',
        'SO': 'Solved',
        # add more name mappings as needed
    }
        return name_mapping.get(status, status)


def ipdf(request):

    # Create a response object with PDF mimetype
        response = HttpResponse(content_type='application/pdf')

    # Set the filename
        response['Content-Disposition'] = 'filename="table.pdf"'

    # Create a PDF object
        pdf = SimpleDocTemplate(response, pagesize=letter)

    # Create a table with headings and data
        start_date="2023-02-19"
        end_date="2023-02-20"
        all_objects = Complaint.objects.filter(c_date__range=(start_date, end_date)).values_list('id','status','branch__branch','category__category','c_date')
        all_objects = [(id, replace_status(status), branch__name,category,c_date) for id, status, branch__name,category,c_date in all_objects]
        table_data = [['Id','Status','Branch','Category','Date' ]] + list(all_objects)
        table = Table(table_data, hAlign='CENTER',colWidths=[65, 140])
        table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
    # Create a paragraph with a heading
    
        style = getSampleStyleSheet()['Heading1']
        heading = '<h1>ComplaintReport</h1>'
        h = Paragraph(heading, style)

    # Create a paragraph with a sentence
        style = getSampleStyleSheet()['Normal']
        name = "John"
        age = 30
        sentence = "My name is {} and I'm {} years old.".format(name, age)
        p = Paragraph(sentence, style)

    # Add the heading, table, and sentence to the PDF object
        elements = [h, table, p]

    # Build the PDF document
        pdf.build(elements)

    # Return the response with PDF content
        return response






def pdf(request):
        start_date=request.GET.get('start_date')
        end_date=request.GET.get('end_date')


    # Create a response object with PDF mimetype
        response = HttpResponse(content_type='application/pdf')

    # Set the filename
        response['Content-Disposition'] = 'filename="table.pdf"'

    # Create a PDF object
        pdf = SimpleDocTemplate(response, pagesize=letter)

    # Create a table with headings and data
        all_objects = Complaint.objects.filter(c_date__range=(start_date, end_date)).values_list('id', 'status', 'branch__branch', 'category__category', 'c_date')
        all_objects = [(id, replace_status(status), branch__name, category, c_date) for id, status, branch__name, category, c_date in all_objects]
        table_data = [['Id', 'Status', 'Branch', 'Category', 'Date']] + list(all_objects)
        table = Table(table_data, hAlign='CENTER', colWidths=[65, 140])
        table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

    # Create a paragraph with a heading
        style1 = ParagraphStyle(name='CenteredHeading1', parent=getSampleStyleSheet()['Heading1'], alignment=TA_CENTER)
        heading = '<h1>ComplaintReport</h1>'
        h = Paragraph(heading, style1)

    # Create a paragraph with a sentence
        sentence_style = ParagraphStyle(
        name='LargeSentence',
        parent=getSampleStyleSheet()['Normal'],
        fontSize=16,
        leading=24
        )
        total =  Complaint.objects.filter(c_date__range=(start_date, end_date)).count()
        sentence = "Total Complaints in this period : {}".format(total)
        p1 = Paragraph(sentence, sentence_style)

        solved =  Complaint.objects.filter(Q(c_date__range=(start_date, end_date))&Q(status='SO')).count()
        sentence = "Total Complaints solved in this period : {}".format(solved)
        p2 = Paragraph(sentence, sentence_style)

        reject =  Complaint.objects.filter(Q(c_date__range=(start_date, end_date))&Q(status='RJ')).count()
        sentence = "Total Complaints rejected in this period : {}".format(reject)
        p3 = Paragraph(sentence, sentence_style)

        pending =  Complaint.objects.filter(Q(c_date__range=(start_date, end_date))&Q(status='PN')).count()
        sentence = "Total Complaints pending in this period : {}".format(pending)
        p4 = Paragraph(sentence, sentence_style)

    # Add a Spacer element with a height of 0.5 inches (or any desired value) between the Paragraph and Table elements
  
        elements = [h]
        elements.append(Spacer(1, 0.2*inch))
        elements.append(table)

    # Add a line break
        elements.append(Spacer(1, 0.2*inch))
        elements.append(p1)
        elements.append(Spacer(1, 0.2*inch))
        elements.append(p2)
        elements.append(Spacer(1, 0.2*inch))
        elements.append(p3)
        elements.append(Spacer(1, 0.2*inch))
        elements.append(p4)
        

    # Build the PDF document
        pdf.build(elements)

    # Return the response with PDF content
        return response

    # Add the heading, sentence, Spacer
