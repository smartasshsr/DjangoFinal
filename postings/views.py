from django.shortcuts import render, redirect, get_object_or_404
from .models import Posting, Comment
from .forms import PostingForm, CommentForm
# [코드 작성] django.contrib.auth.decorators 에서 login_required 데코레이션 가져오기

# [코드 작성] django.views.decorators.http 에서 require_POST 데코레이션 가져오기

# Paginator 가져오기
from django.core.paginator import Paginator
# get_user_model 가져오기
from django.contrib.auth import get_user_model

# Create your views here.
def default_posting():
    # 포스팅 객체가 하나도 경우
    if Posting.objects.all().count() == 0:
        # (admin 계정이 있다는 가정하에) admin 유저 불러오기
        # [코드 수정] createsuperuser시 사용자 이름을 admin으로 만들지 않았다면 'admin' 대신 본인 계정의 username을 문자열로 넣어주기
        user_admin = get_object_or_404(get_user_model(), username='admin')
        # 작성자가 admin인 게시글 300개 생성
        for i in range(1, 301):
            Posting.objects.create(
                title = f'연습용 데이터({i})입니다.',
                content = f'{i}번 글입니다.',
                author = user_admin
            )

def index(request):
    default_posting()
    return render(request, 'postings/index.html')

def posting_list(request):
    # [코드 수정] 페이지네이션
    postings = Posting.objects.all()
    context = {
        'postings': postings,
    }
    return render(request, 'postings/posting_list.html', context)

def posting_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            posting_form = PostingForm(request.POST)
            
            if posting_form.is_valid():
                posting_form = posting_form.save(commit=False)
                posting_form.author = request.user
                posting_form.save()
                return redirect('postings:posting_list')
        else:
            posting_form = PostingForm()
        
        context = {
            'posting_type': '글쓰기',
            'posting_form': posting_form,
        }
        return render(request, 'postings/posting_form.html', context)
    return redirect('accounts:login')

def posting_detail(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.posting = posting
            comment_form.author = request.user
            comment_form.save()
            return redirect('postings:posting_detail', posting_id)
    else :
        comment_form = CommentForm()
    
    comments = posting.comment_list.all()

    context = {
        'posting': posting,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'postings/posting_detail.html', context)

# [코드 작성] login_required 데코레이션 추가

def posting_update(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    if posting.author == request.user:
        if request.method == 'POST':
            posting_form = PostingForm(request.POST, instance=posting)

            if posting_form.is_valid():
                posting_form.save()
                return redirect('postings:posting_detail', posting_id)
        else:
            posting_form = PostingForm(instance=posting)

        context = {
            'posting_type': '글수정',
            'posting': posting,
            'posting_form': posting_form,
        }
        return render(request, 'postings/posting_form.html', context)
    return redirect('postings:posting_detail', posting_id)

# [코드 작성] login_required 데코레이션 추가

# [코드 작성] require_POST 데코레이션 추가

def posting_delete(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    # [미션] 글(posting) 작성자(author)가 로그인한 사람(request.user)과 같을 경우에만 글 삭제가 가능하도록 조건문 작성
    # [미션] True를 지우고 작성
    if True:
        posting.delete()
        return redirect('postings:posting_list')
    # [미션] posting_id에 해당하는 페이지로 redirect
    return 

# [코드 작성] login_required 데코레이션 추가

# [코드 작성] require_POST 데코레이션 추가

def comment_delete(request, posting_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # [미션] 댓글(comment) 작성자(author)가 로그인한 사람(request.user)과 같을 경우에만 댓글 삭제가 가능하도록 조건문 작성
    # [미션] True를 지우고 작성
    if True:
        comment.delete()
    return redirect('postings:posting_detail', posting_id)
