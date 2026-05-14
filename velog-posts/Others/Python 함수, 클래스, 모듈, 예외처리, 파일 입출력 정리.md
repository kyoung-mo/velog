<hr />
<h2 id="목차">목차</h2>
<ul>
<li><a href="https://api.velog.io/rss/@mommers#%ED%95%A8%EC%88%98-function">함수 (Function)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%ED%81%B4%EB%9E%98%EC%8A%A4-class">클래스 (Class)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%AA%A8%EB%93%88-module">모듈 (Module)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%98%88%EC%99%B8%EC%B2%98%EB%A6%AC-exception-handling">예외처리 (Exception Handling)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%ED%8C%8C%EC%9D%BC-%EC%9E%85%EC%B6%9C%EB%A0%A5-file-io">파일 입출력 (File I/O)</a></li>
</ul>
<hr />
<h2 id="함수-function">함수 (Function)</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e83a5436-ce8a-4944-995b-3e7b9bb84224/image.png" /></p>
<h3 id="내장함수">내장함수</h3>
<p>파이썬에는 별도의 import 없이 바로 사용할 수 있는 내장함수들이 있습니다. </p>
<pre><code class="language-python">L = [1, 2, 4, 6, 8, 7, 10]

len(L)     # 7   — 길이
max(L)     # 10  — 최댓값
min(L)     # 1   — 최솟값
sum(L)     # 38  — 합계
sorted(L)  # [1, 2, 4, 6, 7, 8, 10]  — 정렬된 새 리스트 반환</code></pre>
<p><code>sorted()</code>와 <code>sort()</code>는 헷갈리기 쉬운데, 차이를 구분하면 다음과 같습니다.</p>
<table>
<thead>
<tr>
<th></th>
<th><code>sorted(L)</code></th>
<th><code>L.sort()</code></th>
</tr>
</thead>
<tbody><tr>
<td>원본 변경</td>
<td>❌ (새 리스트 반환)</td>
<td>✅ (원본 직접 변경)</td>
</tr>
<tr>
<td>반환값</td>
<td>정렬된 새 리스트</td>
<td><code>None</code></td>
</tr>
</tbody></table>
<pre><code class="language-python">L = [1, 2, 4, 6, 8, 7, 10]

L2 = sorted(L)   # L은 그대로, L2에 정렬 결과 저장
L.sort()         # L 자체가 정렬됨

list(reversed(L))  # 역순으로 뒤집은 새 리스트 반환</code></pre>
<p>리스트뿐 아니라 <strong>튜플과 집합</strong>에도 <code>len</code>, <code>max</code>, <code>min</code>, <code>sum</code>, <code>sorted</code>를 동일하게 사용할 수 있습니다.</p>
<hr />
<h3 id="사용자-정의-함수">사용자 정의 함수</h3>
<pre><code class="language-python">def 함수명(매개변수):
    수행문
    return 반환값</code></pre>
<pre><code class="language-python">def find_max(a, b):
    if a &gt; b:
        return a
    else:
        return b

find_max(20, 10)   # 20</code></pre>
<p>여러 값을 동시에 반환할 경우 <strong>튜플</strong>로 묶여서 반환됩니다.</p>
<pre><code class="language-python">def add_multiply(a, b):
    return a + b, a * b   # 튜플로 반환

m, n = add_multiply(10, 20)
print(m, n)   # 30 200</code></pre>
<p>반환 자료형은 튜플, 리스트, 딕셔너리 등 자유롭게 선택할 수 있습니다.</p>
<pre><code class="language-python">def func(x):
    return (x*2, x*4, x*6)    # 튜플 반환
    return [x*2, x*4, x*6]    # 리스트 반환
    return {'r1': x*2, 'r2': x*4}  # 딕셔너리 반환</code></pre>
<hr />
<h3 id="기본값-매개변수">기본값 매개변수</h3>
<p>매개변수에 기본값을 지정하면 인수를 생략했을 때 기본값이 사용됩니다.</p>
<pre><code class="language-python">def para_func(x1, x2, x3=0):
    return x1 + x2 + x3

para_func(10, 20)       # 30  (x3 생략 → 기본값 0 사용)
para_func(10, 20, 30)   # 60</code></pre>
<hr />
<h3 id="가변-매개변수">가변 매개변수</h3>
<p>인수의 개수가 가변적일 때는 <code>*</code> 또는 <code>**</code>를 사용합니다.</p>
<pre><code class="language-python"># *args — 튜플 형태로 받음
def para_func(*para):
    result = 0
    for num in para:
        result += num
    return result

para_func(10, 20)        # 30
para_func(10, 20, 30)    # 60</code></pre>
<pre><code class="language-python"># **kwargs — 딕셔너리 형태로 받음
def print_dic(**persons):
    for k in persons.keys():
        print(f'{k} : {persons[k]}')

print_dic(소녀시대=7, 블랙핑크=4, 트와이스=9)</code></pre>
<p><code>*args</code> 뒤에 오는 일반 매개변수는 반드시 <strong>키워드 인수</strong>로 호출해야 합니다.</p>
<pre><code class="language-python">def print_args(*argv, argc):
    for i in range(argc):
        print(argv[i])

print_args('파이썬', '연습', '문제', argc=3)   # argc= 로 명시 필요</code></pre>
<hr />
<h3 id="람다-함수-lambda">람다 함수 (Lambda)</h3>
<p><code>lambda</code>는 이름 없는 익명 함수로, 간단한 함수를 한 줄로 표현할 때 사용합니다.</p>
<pre><code class="language-python"># 일반 함수
def add(x, y):
    return x + y

# 람다 함수
lambda x, y: x + y</code></pre>
<p><code>map()</code>과 <code>filter()</code>와 함께 사용하면 강력합니다.</p>
<pre><code class="language-python"># map() — 리스트의 각 요소에 함수 적용
a = [1, 2, 3, 4]
b = [10, 20, 30, 40]
list(map(lambda x, y: x + y, a, b))   # [11, 22, 33, 44]

X = [1, 3, 6]
list(map(lambda a: a * a, X))   # [1, 9, 36]</code></pre>
<pre><code class="language-python"># filter() — 조건을 만족하는 요소만 추출
list(filter(lambda x: x % 2 == 1, range(11)))   # [1, 3, 5, 7, 9]</code></pre>
<hr />
<h3 id="유용한-문자열-메서드">유용한 문자열 메서드</h3>
<pre><code class="language-python">name = 'kang'
name.upper()        # 'KANG'  — 대문자
name.lower()        # 'kang'  — 소문자
name.islower()      # True    — 소문자 여부 확인
name.isupper()      # False

d = 'hello world'
d.capitalize()   # 'Hello world'  — 첫 글자만 대문자
d.title()        # 'Hello World'  — 단어마다 첫 글자 대문자</code></pre>
<pre><code class="language-python"># join() — 리스트를 문자열로 합치기
name = ['kang', 'Kim', 'Yang']
'-'.join(name)   # 'kang-Kim-Yang'

# split() — 문자열을 리스트로 쪼개기
'kang kim yang'.split()        # ['kang', 'kim', 'yang']
'2019/10/16'.split('/')        # ['2019', '10', '16']</code></pre>
<hr />
<h2 id="클래스-class">클래스 (Class)</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/66553c94-ca62-42ea-b1fb-d335326fc558/image.png" /></p>
<h3 id="클래스-선언과-객체-생성">클래스 선언과 객체 생성</h3>
<p>클래스는 데이터(속성)와 기능(메서드)을 하나로 묶는 틀입니다.<br /><code>__init__</code>은 객체가 생성될 때 자동으로 호출되는 <strong>생성자</strong>입니다.</p>
<pre><code class="language-python">class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(self.name, 'is barking')

# 객체 생성
x = Dog('Happy', 5)
x.bark()   # Happy is barking
print(x.name, 'is', x.age, 'years old')</code></pre>
<p>실용적인 예시입니다.</p>
<pre><code class="language-python">class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def drive(self, distance):
        self.odometer_reading += distance
        return f&quot;Driving {distance} kilometers.&quot;

my_car = Car(&quot;KIA&quot;, &quot;Sorento&quot;, 2025)
print(my_car.drive(100))   # Driving 100 kilometers.</code></pre>
<hr />
<h3 id="생성자와-소멸자">생성자와 소멸자</h3>
<p><code>__del__</code>은 객체가 메모리에서 삭제될 때 호출되는 <strong>소멸자</strong>입니다.</p>
<pre><code class="language-python">class Resource:
    def __init__(self, name):
        self.name = name
        print(f&quot;Resource {name} created&quot;)

    def __del__(self):
        print(f&quot;Resource {self.name} cleaned up&quot;)

r = Resource(&quot;DB Connection&quot;)   # Resource DB Connection created
del r                            # Resource DB Connection cleaned up</code></pre>
<blockquote>
<p>변수에 저장하지 않고 객체를 생성하면 즉시 소멸자가 실행됩니다.</p>
</blockquote>
<hr />
<h3 id="self의-이해">self의 이해</h3>
<p><code>self</code>는 인스턴스 자기 자신을 가리키는 참조입니다.<br />메서드를 호출할 때 파이썬이 자동으로 첫 번째 인수로 넘겨줍니다.</p>
<pre><code class="language-python">class SelfTest:
    def function2(self):
        print(id(self))   # 인스턴스의 메모리 주소

f = SelfTest()
print(id(f))      # f의 메모리 주소
f.function2()     # 동일한 주소가 출력됨</code></pre>
<p><code>f.function2()</code>는 내부적으로 <code>SelfTest.function2(f)</code>와 동일합니다.</p>
<hr />
<h3 id="클래스-변수-vs-인스턴스-변수">클래스 변수 vs 인스턴스 변수</h3>
<table>
<thead>
<tr>
<th></th>
<th>클래스 변수</th>
<th>인스턴스 변수</th>
</tr>
</thead>
<tbody><tr>
<td>선언 위치</td>
<td>클래스 내부 (메서드 밖)</td>
<td><code>__init__</code> 안에서 <code>self.변수명</code></td>
</tr>
<tr>
<td>공유 여부</td>
<td><strong>모든 인스턴스 공유</strong></td>
<td>인스턴스마다 독립적</td>
</tr>
<tr>
<td>접근 방법</td>
<td><code>클래스명.변수명</code></td>
<td><code>self.변수명</code></td>
</tr>
</tbody></table>
<pre><code class="language-python">class Warehouse:
    stock_num = 0   # 클래스 변수 — 공유

    def __init__(self, name):
        self.name = name          # 인스턴스 변수
        Warehouse.stock_num += 1  # 클래스 변수 증가

    def __del__(self):
        Warehouse.stock_num -= 1

user1 = Warehouse('Kim')
user2 = Warehouse('Park')

print(Warehouse.stock_num)   # 2  — 두 인스턴스가 공유
print(user1.stock_num)       # 2
print(user2.stock_num)       # 2</code></pre>
<hr />
<h2 id="모듈-module">모듈 (Module)</h2>
<p>모듈은 함수, 클래스, 변수 등을 담아둔 <code>.py</code> 파일입니다.<br /><code>import</code>를 통해 불러와 재사용할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f0ce82e3-7651-4136-a6dc-71363c9730c2/image.png" /></p>
<h3 id="import-방식-3가지">import 방식 3가지</h3>
<pre><code class="language-python"># 방법 1 — 모듈 전체 import
import calculator
calculator.plus(10, 20)

# 방법 2 — 별칭(alias) 지정
import calculator as c
c.plus(5, 4)

# 방법 3 — 특정 함수만 import
from calculator import minus
minus(10, 5)

# 전체 함수 import (권장하지 않음 — 이름 충돌 위험)
from calculator import *
multiply(3, 5)</code></pre>
<hr />
<h3 id="사용자-정의-모듈-만들기">사용자 정의 모듈 만들기</h3>
<p>Jupyter Notebook에서는 <code>%%writefile</code> 매직커맨드로 <code>.py</code> 파일을 바로 만들 수 있습니다.</p>
<pre><code class="language-python">%%writefile calculator.py

def plus(x, y):
    return x + y
def minus(x, y):
    return x - y
def multiply(x, y):
    return x * y
def divide(x, y):
    return x / y</code></pre>
<p>클래스도 동일하게 모듈로 저장할 수 있습니다.</p>
<pre><code class="language-python">%%writefile pet.py

class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(self.name, 'is barking')</code></pre>
<hr />
<h3 id="모듈-탐색-순서">모듈 탐색 순서</h3>
<p><code>import</code>를 실행하면 파이썬은 다음 순서로 모듈을 찾습니다.</p>
<ol>
<li>현재 디렉토리</li>
<li>환경변수 <code>PYTHONPATH</code>에 지정된 경로</li>
<li>Python 설치 경로 및 라이브러리 경로</li>
</ol>
<p>탐색 경로는 <code>sys.path</code>로 확인할 수 있으며, 경로를 추가할 수도 있습니다.</p>
<pre><code class="language-python">import sys
print(sys.path)   # 현재 탐색 경로 목록 확인

sys.path.append('/원하는/경로')   # 경로 추가</code></pre>
<hr />
<h2 id="예외처리-exception-handling">예외처리 (Exception Handling)</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/26915853-ad8a-4d6d-bb35-1444b8362887/image.png" /></p>
<h3 id="주요-에러-종류">주요 에러 종류</h3>
<table>
<thead>
<tr>
<th>에러</th>
<th>발생 상황</th>
</tr>
</thead>
<tbody><tr>
<td><code>SyntaxError</code></td>
<td>문법 오류 (따옴표 미종료 등)</td>
</tr>
<tr>
<td><code>NameError</code></td>
<td>정의되지 않은 변수 사용</td>
</tr>
<tr>
<td><code>TypeError</code></td>
<td>타입 불일치 연산 (<code>int + str</code>)</td>
</tr>
<tr>
<td><code>ZeroDivisionError</code></td>
<td>0으로 나누기</td>
</tr>
<tr>
<td><code>IndexError</code></td>
<td>리스트 범위를 벗어난 인덱스</td>
</tr>
<tr>
<td><code>ValueError</code></td>
<td>값이 유효하지 않을 때</td>
</tr>
</tbody></table>
<pre><code class="language-python">print(x)          # NameError  — x가 정의되지 않음
1 + 'A'           # TypeError
10 / 0            # ZeroDivisionError
[1,2,3][5]        # IndexError</code></pre>
<hr />
<h3 id="try--except--else--finally">try / except / else / finally</h3>
<pre><code class="language-python">try:
    c = a / b
except ZeroDivisionError:
    print('Cannot divide by 0')</code></pre>
<p>여러 예외를 한 번에 처리하거나 예외 정보를 출력할 수도 있습니다.</p>
<pre><code class="language-python">try:
    c = a / b
    print(L[3])
except Exception as err:
    print(f'예외가 발생했습니다.({err})')
else:
    print('에러 없이 정상 실행됨')
finally:
    print('에러 여부와 관계없이 항상 실행됨')</code></pre>
<ul>
<li><code>except</code> : 에러 발생 시 실행</li>
<li><code>else</code> : 에러가 없을 때 실행</li>
<li><code>finally</code> : 에러 여부와 무관하게 <strong>항상</strong> 실행</li>
</ul>
<p>실용 예시 — 문자열에서 특정 단어 위치를 모두 찾을 때 <code>try-except</code>로 루프를 제어합니다.</p>
<pre><code class="language-python">myStr = '파이썬은 재미있어요. 파이썬 공부 열심히 할래요'
postList = []
index = 0

while True:
    try:
        index = myStr.index('파이썬', index)
        postList.append(index)
        index += 1
    except:
        break

print('파이썬 글자 위치 --&gt;', postList)   # [0, 12]</code></pre>
<hr />
<h2 id="파일-입출력-file-io">파일 입출력 (File I/O)</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/362f9c80-a0f3-487a-bb15-62776a48b5c3/image.png" /></p>
<h3 id="파일-열기와-닫기">파일 열기와 닫기</h3>
<p><code>open(파일경로, 모드)</code>로 파일을 열고, 사용 후에는 반드시 <code>close()</code>로 닫아야 합니다.</p>
<table>
<thead>
<tr>
<th>모드</th>
<th>의미</th>
</tr>
</thead>
<tbody><tr>
<td><code>'r'</code></td>
<td>읽기 (기본값)</td>
</tr>
<tr>
<td><code>'w'</code></td>
<td>쓰기 (기존 내용 덮어씀)</td>
</tr>
<tr>
<td><code>'a'</code></td>
<td>추가 (기존 내용 뒤에 이어씀)</td>
</tr>
</tbody></table>
<pre><code class="language-python">f = open('파일명.txt', 'r')
# ... 파일 작업
f.close()</code></pre>
<p><code>with</code> 구문을 사용하면 블록이 끝날 때 자동으로 <code>close()</code>가 호출됩니다.</p>
<pre><code class="language-python">with open('파일명.txt', 'r') as f:
    data = f.read()
# 블록을 벗어나면 자동으로 닫힘</code></pre>
<blockquote>
<p><code>with</code> 구문을 사용하는 것이 더 안전하고 권장되는 방법입니다.</p>
</blockquote>
<hr />
<h3 id="파일-읽기">파일 읽기</h3>
<pre><code class="language-python">f = open('readfile.txt', 'r')

f.read()        # 파일 전체를 문자열로 반환
f.read(4)       # n바이트만 읽어서 반환
f.readline()    # 한 줄씩 읽어서 반환
f.readlines()   # 전체를 줄 단위로 나눠 리스트로 반환

f.close()</code></pre>
<p><code>for</code>문으로 한 줄씩 순차적으로 읽는 방법이 가장 많이 사용됩니다.</p>
<pre><code class="language-python">with open('readfile.txt', 'r') as f:
    for line in f:
        print(line, end='')</code></pre>
<p>파일 내용을 리스트나 딕셔너리로 파싱하는 것도 자주 사용하는 패턴입니다.</p>
<pre><code class="language-python"># 숫자가 한 줄씩 있는 파일 → 리스트로 저장
score = []
with open('scoredata.txt', 'r') as f:
    for line in f:
        score.append(int(line))

# '키 값' 형식의 파일 → 딕셔너리로 저장
d_score = {}
with open('scoredata2.txt', 'r') as f:
    for line in f:
        key, value = line.split()
        d_score[int(key)] = value</code></pre>
<hr />
<h3 id="파일-쓰기">파일 쓰기</h3>
<pre><code class="language-python"># write() — 문자열 쓰기
f = open('writefile.txt', 'w')
f.write('hello world\n')
f.write('python programming\n')
f.close()

# writelines() — 리스트를 한 번에 쓰기
f = open('writefile2.txt', 'w')
f.writelines(['hello\n', 'world\n', 'python\n'])
f.close()</code></pre>
<hr />
<h3 id="pathlib로-파일-다루기">pathlib로 파일 다루기</h3>
<p><code>pathlib</code> 모듈을 사용하면 파일 경로와 입출력을 더 간결하게 처리할 수 있습니다.</p>
<pre><code class="language-python">from pathlib import Path

path = Path('./my_favorite.txt')
contents = path.read_text()    # 파일 전체 읽기
print(contents)

# 줄 단위로 나누기
contents_list = contents.splitlines()

# 내용 추가하기 ('a' 모드)
with path.open(mode='a') as file:
    file.write('\nPython')

# 내용 덮어쓰기 ('w' 모드)
with path.open(mode='w') as file:
    file.write('\n'.join(contents_list))</code></pre>
<hr />
<h3 id="파일-존재-여부-확인--예외처리-적용">파일 존재 여부 확인 + 예외처리 적용</h3>
<pre><code class="language-python">import os

fileName = input('파일명을 입력하세요: ')

if os.path.exists(fileName):
    with open(fileName, 'r') as f:
        for line in f:
            print(line, end='')
else:
    print(f'{fileName} 파일이 없습니다')</code></pre>
<p>예외처리와 함께 사용하면 더 안전합니다.</p>
<pre><code class="language-python">fileName = input('파일명을 입력하세요: ')

try:
    with open(fileName, 'r') as f:
        for line in f:
            print(line, end='')
except Exception as err:
    print(f'예외가 발생했습니다.({err})')</code></pre>