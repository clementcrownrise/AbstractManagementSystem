from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm
from django.contrib  import messages
from .models import Article, ArticleReviewer, Comment
from accounts.models import Account
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string




# Create your views here.
def create_abstract(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            #i need to send a mail here for a successful abstract creation

            mail_subject = 'Abstract Submission Notification'
            message = render_to_string('article/abstractSubmissionEmail.html',{
                'article':article,
            })
            to_email = article.user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            #below email will go to the faculty head 
            mail_subject_to_admin = 'Abstract Submission Notification'
            message_to_admin = render_to_string('article/abstractSubmissionEmailFacultyHead.html',{
                'article':article,
            })
            
            faculty = article.user.faculty_id
            facultyheademail = Account.objects.filter(
                faculty_id=faculty, user_type ='admin').values_list('email',flat=True)
            facultyheademail = facultyheademail.first()
            send_email_to_admin = EmailMessage(mail_subject_to_admin, message_to_admin, to=[facultyheademail])
            send_email_to_admin.send()

            messages.success(request, 'Abstract Submitted Successfully')
            return redirect('dashboard')


    else:
        form = ArticleForm()


    context ={'form':form}
    return render(request, 'article/create_abstract.html', context)


def view_abstract(request, id):
    #print(id)
    revieweremails = []
    
    user = request.user

    if user.user_type == 'candidate':

        article = get_object_or_404(Article, id=id, user=request.user)
        

    elif user.user_type == 'reviewer':
        #article = get_object_or_404(Article, id=id, user__faculty = request.user.faculty)
        assigment = get_object_or_404(ArticleReviewer, article_id = id, reviewer = request.user)
        article = assigment.article

    elif user.user_type == 'admin':
        #I only get the reviewers of the logged in Admin user faculty
        revieweremails = Account.objects.filter(
            faculty = request.user.faculty, user_type = 'reviewer').values_list('id', 'email')
        article = get_object_or_404(Article, id=id, user__faculty = request.user.faculty)
    else:
        messages.error(request, 'You can NOT view an article you do not own')
        return redirect('dashboard')
    comments = article.comments.all().order_by('-created_at')
    #i need to get all currently assigned reviewers
    assigned_reviewers = ArticleReviewer.objects.filter(article=article).select_related('reviewer')
    context={
        'article':article,
        'revieweremails':revieweremails,
        'comments':comments,
        'assigned_reviewers':assigned_reviewers,
    }
    
    return render(request, 'article/view_abstract.html', context)



def assign_reviewer(request,pk):
    #return HttpResponse( 'I am getting here')
    article  = Article.objects.get(id=pk)
    if request.method == 'POST':
        reviewer_id = request.POST.get('reviewer')
        if not reviewer_id:
            messages.error(request, "Failure: No reviewer was selected.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        #check if the revieer is already assigned 
        already_assigned = ArticleReviewer.objects.filter(
            article=article, 
            reviewer_id=reviewer_id
        ).exists()
        
        if not already_assigned:

            assignment = ArticleReviewer.objects.create(
                article = article,
                reviewer_id = reviewer_id
            )
            #I need to send a message to send a mail to the reviewer
            mail_subject = 'Abstract Assignment Notification'
            message = render_to_string('article/ReviewerAssignmentEmail.html',{
                'article':article,
            })
            to_email = assignment.reviewer.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
        
            messages.success(request,'Reviewer has been assigned successfully')
        #print(reviewer_id,article)
        else:
            messages.error(request, 'Error adding a reviewer, This reviewer is already added to this Abstract')

    return redirect(request.META.get('HTTP_REFERER','/'))


#adminComment
def admin_comment(request,pk):
    article = Article.objects.get(id=pk)
    if request.method =='POST':
        print('I am getting here')
        status = request.POST.get('status', 'NONE')
        comment = request.POST.get('comment')
        saved_comment = Comment.objects.create(
            article = article,
            status = status,
            comment = comment,
            user = request.user
        )
        if saved_comment:
            #I need to send a mail to all the users in this article

            mail_subject = 'Abstract Update Notification'
            message = render_to_string('article/commentNotification.html',{
                'article':article,
            })
            emails =set()
            #candidate's email
            if request.user.email != article.user.email:
                emails.add(article.user.email)
            #faculty chairman email
            if request.user.user_type != 'admin':
                emails.update(Account.objects.filter(
                    faculty=article.user.faculty,
                    user_type ='admin'
                ).values_list('email',flat=True))
            #reviewer's email
            emails.update(
                ArticleReviewer.objects.filter(article=article).values_list(
                    'reviewer__email', flat=True)
            )
            send_email = EmailMessage(mail_subject, message, to=list(emails))
            #print(emails)
            send_email.send()

            messages.success(request, 'Your comment was saved successfully')
        else:
            messages.error(request, 'Messages could not be saved')

    return redirect(request.META.get('HTTP_REFERER', '/'))



def remove_reviewer(request, article_id, reviewer_id):
    ArticleReviewer.objects.filter(
        article_id=article_id,
        reviewer_id = reviewer_id
    ).delete()  
    messages.error(request, 'The reviewer has been removed succefully')
    return redirect(request.META.get('HTTP_REFERER', '/'))
