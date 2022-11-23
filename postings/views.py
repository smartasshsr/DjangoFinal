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
    # Posting 객체들을 'date'기준으로 역순으로 정렬
    postings = Posting.objects.order_by('date').reverse()
    # 정렬된 postings의 전체 개수 저장
    postings_num = postings.count()

    # Paginator를 이용하여 postings 객체를 10개씩 가져오기
    paginator = Paginator(postings, 10)
    # GET 방식으로 url중 ?page의 value값을 받아옴
    page = request.GET.get('page')
    # page가 선택되지 않았을 경우에는 '1'로 설정
    if page == None:
        page = '1'

    # 화면에 보여질 페이지 개수 설정
    count = 5
    # 현재 보여지는 페이지를 정수형으로 변환
    recent_page = int(page)
    
    # 마지막 페이지 번호 계산
    last_page = postings_num // 10
    if postings_num % 10 != 0:
        last_page + 1
    
    # '이전' 버튼을 눌렀을 때 이동할 페이지 번호 계산
    previous_page = ((recent_page-1)//count)*count
    # '이전' 버튼을 눌렀을 때 이동 가능 여부 저장
    move_previous = True
    if previous_page < count:
        move_previous = False
    
    # '다음' 버튼을 눌렀을 때 이동할 페이지 번호 계산
    next_page = ((recent_page-1)//count+1)*count+1
    # '다음' 버튼을 눌렀을 때 이동 가능 여부 저장
    move_next = True
    if next_page > last_page:
        move_next = False
    
    # 현재 페이지에서 이동 가능한 첫 페이지 번호 계산
    start_page = previous_page+1
    # 현재 페이지에서 이동 가능한 마지막 페이지 번호 계산
    end_page = next_page-1
    if end_page > last_page:
        end_page = last_page

    # 현재 페이지에서 이동 가능한 페이지 범위를 리스트로 저장
    page_range = list(range(start_page, end_page+1))
    # page에 해당하는 글 10개 저장
    page_postings = paginator.get_page(page)

    # 현재 페이지에서 보여지는 첫 번째 게시글 번호 저장
    page_postings_start_index = postings_num-(recent_page-1)*10

    context = {
        'last_page': last_page,
        'previous_page': previous_page,
        'move_previous': move_previous,
        'next_page': next_page,
        'move_next': move_next,
        'start_page': start_page,
        'end_page': end_page,
        'page_range': page_range,
        'page_postings': page_postings,
        'page_postings_start_index': page_postings_start_index,
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
