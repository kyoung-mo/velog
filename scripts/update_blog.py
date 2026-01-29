import feedparser
import git
import os
import re

# 벨로그 RSS 피드 URL
rss_url = 'https://api.velog.io/rss/@mommers'

# 깃허브 레포지토리 경로
repo_path = '.'

# 'velog-posts' 폴더 경로
posts_dir = os.path.join(repo_path, 'velog-posts')

# 카테고리 정의 (정규표현식 패턴)
CATEGORIES = {
    'C언어': r'^\[C언어\]',
    'STM32': r'^\[STM32\]',
    '아두이노': r'^\[아두이노\]',
    '자료구조': r'^\[자료구조\]',
    'Linux': r'^\[Linux\]',
    'HW': r'^\[HW\]',
    'FW': r'^\[FW\]',
    'Raspi': r'^\[Raspi\]',
    '기타': r'^\[.*\]',  # 기타 대괄호로 시작하는 것들
}

# 'velog-posts' 폴더가 없다면 생성
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# 카테고리별 폴더 생성
for category in CATEGORIES.keys():
    category_dir = os.path.join(posts_dir, category)
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)

# Others 폴더도 생성
others_dir = os.path.join(posts_dir, 'Others')
if not os.path.exists(others_dir):
    os.makedirs(others_dir)

# 레포지토리 로드
repo = git.Repo(repo_path)

# RSS 피드 파싱
feed = feedparser.parse(rss_url)

def get_category_from_title(title):
    """제목에서 카테고리 추출"""
    for category, pattern in CATEGORIES.items():
        if re.match(pattern, title):
            return category
    return 'Others'

# 각 글을 파일로 저장하고 커밋
for entry in feed.entries:
    # 파일 이름에서 유효하지 않은 문자 제거 또는 대체
    file_name = entry.title
    file_name = file_name.replace('/', '-')  # 슬래시를 대시로 대체
    file_name = file_name.replace('\\', '-')  # 백슬래시를 대시로 대체
    file_name += '.md'
    
    # 카테고리 결정
    category = get_category_from_title(entry.title)
    category_dir = os.path.join(posts_dir, category)
    file_path = os.path.join(category_dir, file_name)
    
    # 파일이 이미 존재하지 않으면 생성
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(entry.description)  # 글 내용을 파일에 작성
        
        # 깃허브 커밋
        repo.git.add(file_path)
        repo.git.commit('-m', f'Add post: [{category}] {entry.title}')
        print(f'Added: {category}/{file_name}')

# 기존에 velog-posts 루트에 있는 파일들을 카테고리별로 재정리
print("\n기존 파일 정리 중...")
for file_name in os.listdir(posts_dir):
    file_path = os.path.join(posts_dir, file_name)
    
    # 파일만 처리 (폴더 제외)
    if os.path.isfile(file_path) and file_name.endswith('.md'):
        # 파일명에서 .md 제거
        title = file_name[:-3]
        
        # 카테고리 결정
        category = get_category_from_title(title)
        category_dir = os.path.join(posts_dir, category)
        new_file_path = os.path.join(category_dir, file_name)
        
        # 파일 이동
        if file_path != new_file_path:
            os.rename(file_path, new_file_path)
            repo.git.add(file_path)  # 삭제된 파일 추가
            repo.git.add(new_file_path)  # 새 파일 추가
            print(f'Moved: {file_name} -> {category}/')

# 정리 작업 커밋
try:
    repo.git.commit('-m', 'Organize posts by category')
    print("\n파일 정리 완료!")
except Exception as e:
    print("\n정리할 파일이 없거나 이미 정리되어 있습니다.")

# 변경 사항을 깃허브에 푸시
try:
    repo.git.push()
    print("푸시 완료!")
except Exception as e:
    print(f"푸시 중 오류 발생: {e}")
