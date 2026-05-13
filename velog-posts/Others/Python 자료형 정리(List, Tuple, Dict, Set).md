<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/add291c7-9e47-43ed-a087-23928756f2bb/image.png" /></p>
<blockquote>
<p>Python의 핵심 복합 자료형 4가지와 심화 문법을 정리한 글입니다.</p>
</blockquote>
<hr />
<h2 id="목차">목차</h2>
<ul>
<li><a href="https://api.velog.io/rss/@mommers#%EB%A6%AC%EC%8A%A4%ED%8A%B8-list">리스트 (List)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%ED%8A%9C%ED%94%8C-tuple">튜플 (Tuple)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%94%95%EC%85%94%EB%84%88%EB%A6%AC-dictionary">딕셔너리 (Dictionary)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%A7%91%ED%95%A9-set">집합 (Set)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%8B%AC%ED%99%94--%EC%BB%B4%ED%94%84%EB%A6%AC%ED%97%A8%EC%85%98--zip--%EB%B3%B5%EC%82%AC">심화 — 컴프리헨션 / zip / 복사</a></li>
</ul>
<hr />
<h2 id="리스트-list">리스트 (List)</h2>
<p>리스트는 여러 값을 순서대로 저장하는 자료형입니다.<br />대괄호 <code>[]</code>로 감싸며, <strong>다양한 타입을 하나의 리스트에 담을 수 있습니다.</strong></p>
<pre><code class="language-python">a = [1, 2, 3, 4, 5]
b = ['life', 'is', 'too', 'short']
c = [1, 2, 'life', 'is']          # 혼합 타입도 가능
d = [1, 2, ['life', 'is']]        # 리스트 안에 리스트도 가능</code></pre>
<h3 id="인덱싱과-슬라이싱">인덱싱과 슬라이싱</h3>
<p>문자열과 동일하게 인덱싱, 슬라이싱을 사용할 수 있습니다.</p>
<pre><code class="language-python">a = [1, 2, 3, 4, 5]

a[0]      # 1
a[-1]     # 5  (뒤에서 첫 번째)
a[1:-1]   # [2, 3, 4]
a[3:]     # [4, 5]</code></pre>
<p>리스트 안에 리스트가 있는 경우, 인덱싱을 두 번 사용합니다.</p>
<pre><code class="language-python">d = [1, 2, ['life', 'is', ['too', 'short']]]

d[2]          # ['life', 'is', ['too', 'short']]
d[2][2]       # ['too', 'short']
d[-1][-1][-1] # 'short'</code></pre>
<h3 id="리스트-연산">리스트 연산</h3>
<pre><code class="language-python">x = [1, 3, 5, 7, 9]
y = [2, 4, 6, 8]

x + y     # [1, 3, 5, 7, 9, 2, 4, 6, 8]  — 두 리스트를 연결
x * 3     # [1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9]  — 반복

7 in x    # True
8 in x    # False
4 not in x  # True</code></pre>
<h3 id="주요-메서드">주요 메서드</h3>
<table>
<thead>
<tr>
<th>메서드</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><code>append(x)</code></td>
<td>맨 뒤에 요소 추가</td>
</tr>
<tr>
<td><code>extend([x])</code></td>
<td>맨 뒤에 다른 리스트 추가</td>
</tr>
<tr>
<td><code>insert(i, x)</code></td>
<td>인덱스 i 위치에 x 삽입</td>
</tr>
<tr>
<td><code>remove(x)</code></td>
<td>첫 번째로 나오는 x 삭제</td>
</tr>
<tr>
<td><code>pop(i)</code></td>
<td>인덱스 i의 요소를 꺼내고 삭제 (기본: 마지막)</td>
</tr>
<tr>
<td><code>index(x)</code></td>
<td>x의 인덱스 반환</td>
</tr>
<tr>
<td><code>count(x)</code></td>
<td>x의 개수 반환</td>
</tr>
<tr>
<td><code>sort()</code></td>
<td>오름차순 정렬 (원본 변경)</td>
</tr>
<tr>
<td><code>sort(reverse=True)</code></td>
<td>내림차순 정렬</td>
</tr>
<tr>
<td><code>reverse()</code></td>
<td>순서를 역으로 뒤집기</td>
</tr>
<tr>
<td><code>clear()</code></td>
<td>모든 요소 삭제</td>
</tr>
<tr>
<td><code>copy()</code></td>
<td>리스트 복사</td>
</tr>
</tbody></table>
<pre><code class="language-python">z = [1, 4, 6, 8]
z.append(9)            # [1, 4, 6, 8, 9]
z.insert(1, 99)        # [1, 99, 4, 6, 8, 9]
z.remove(99)           # [1, 4, 6, 8, 9]
z.pop()                # 9 반환 후 삭제

i = [2, 5, 7, 1, 9]
i.sort()               # [1, 2, 5, 7, 9]
i.sort(reverse=True)   # [9, 7, 5, 2, 1]</code></pre>
<h3 id="리스트-복사-주의사항">리스트 복사 주의사항</h3>
<p><code>=</code>로 대입하면 같은 메모리를 가리키는 <strong>참조 복사</strong>가 됩니다.<br />한쪽을 바꾸면 다른 쪽도 바뀌기 때문에 주의가 필요합니다.</p>
<pre><code class="language-python">e = [1, 3, 5, 7, 9]
f = e           # 참조 복사 — 같은 메모리

f[2] = 200
print(f)   # [1, 3, 200, 7, 9]
print(e)   # [1, 3, 200, 7, 9]  ← 원본도 바뀜!</code></pre>
<p>독립적인 복사를 원한다면 <code>copy()</code> 또는 슬라이싱 <code>[:]</code>을 사용합니다.</p>
<pre><code class="language-python">g = [2, 4, 6, 8]
h = g.copy()    # 독립 복사
# 또는
h = g[:]

h[2] = 200
print(g)   # [2, 4, 6, 8]  ← 원본 유지
print(h)   # [2, 4, 200, 8]</code></pre>
<blockquote>
<p><code>=</code> 대입은 복사가 아닌 <strong>참조</strong>임을 반드시 기억해야 합니다.</p>
</blockquote>
<hr />
<h2 id="튜플-tuple">튜플 (Tuple)</h2>
<p>튜플은 리스트와 유사하지만 <strong>값을 변경할 수 없는 (immutable)</strong> 자료형입니다.<br />소괄호 <code>()</code>로 감쌉니다.</p>
<pre><code class="language-python">a = (1, 3, 5, 7, 9)
b = (2, 4, 6, 8)</code></pre>
<h3 id="기본-연산">기본 연산</h3>
<p>리스트와 동일하게 인덱싱, 슬라이싱, 연산을 사용할 수 있습니다.</p>
<pre><code class="language-python">a[0]      # 1
a[:3]     # (1, 3, 5)  ← 슬라이싱 결과도 튜플
a + b     # (1, 3, 5, 7, 9, 2, 4, 6, 8)
a * 3     # 반복
5 in a    # True
len(a)    # 5</code></pre>
<h3 id="주요-메서드-1">주요 메서드</h3>
<p>튜플은 값 변경이 불가하기 때문에 사용 가능한 메서드가 매우 제한적입니다.</p>
<pre><code class="language-python">d = (2, 4, 3, 7, 5, 2, 9)

d.count(2)   # 2  — 값 2의 개수
d.index(2)   # 0  — 값 2의 첫 번째 인덱스
d.index(9)   # 6</code></pre>
<h3 id="원소가-1개인-튜플">원소가 1개인 튜플</h3>
<p>소괄호만으로는 튜플이 되지 않습니다. <strong>반드시 쉼표를 붙여야 합니다.</strong></p>
<pre><code class="language-python">e = (1)
type(e)   # int  ← 튜플이 아님!

f = (2,)
type(f)   # tuple  ← 올바른 1개짜리 튜플</code></pre>
<h3 id="리스트와-튜플-비교">리스트와 튜플 비교</h3>
<table>
<thead>
<tr>
<th>구분</th>
<th>리스트</th>
<th>튜플</th>
</tr>
</thead>
<tbody><tr>
<td>선언</td>
<td><code>[1, 2, 3]</code></td>
<td><code>(1, 2, 3)</code></td>
</tr>
<tr>
<td>인덱싱</td>
<td>✅</td>
<td>✅</td>
</tr>
<tr>
<td>for 반복</td>
<td>✅</td>
<td>✅</td>
</tr>
<tr>
<td>값 변경</td>
<td>✅</td>
<td>❌</td>
</tr>
<tr>
<td>딕셔너리 key 사용</td>
<td>❌</td>
<td>✅</td>
</tr>
<tr>
<td>반복 속도</td>
<td>보통</td>
<td>더 빠름</td>
</tr>
</tbody></table>
<p>리스트는 <code>list()</code>로 복사하면 새 객체가 생성되지만, 튜플은 <code>tuple()</code>로 복사해도 <strong>동일한 객체를 가리킵니다.</strong></p>
<pre><code class="language-python">k1 = [1, 2, 3]
k2 = list(k1)
k2 is k1   # False  — 새 객체 생성

t1 = (1, 2, 3)
t2 = tuple(t1)
t1 is t2   # True  — 같은 객체 (튜플은 불변이므로 굳이 복사 안 함)</code></pre>
<blockquote>
<p>변경이 필요 없는 데이터는 튜플을 사용하는 것이 성능 면에서 유리합니다.</p>
</blockquote>
<hr />
<h2 id="딕셔너리-dictionary">딕셔너리 (Dictionary)</h2>
<p>딕셔너리는 <strong>키(Key): 값(Value)</strong> 쌍으로 데이터를 저장하는 자료형입니다.<br />중괄호 <code>{}</code>로 감싸며, 위치 인덱싱은 불가하고 <strong>키를 통해 값에 접근합니다.</strong></p>
<pre><code class="language-python">color = {'red': 1, 'green': 2, 'blue': 3}
studentNum = {1: 30, 2: 26, 3: 25}   # key는 정수도 가능</code></pre>
<blockquote>
<p>키는 중복될 수 없으며, 리스트는 키가 될 수 없습니다.</p>
</blockquote>
<h3 id="접근--추가--수정--삭제">접근 / 추가 / 수정 / 삭제</h3>
<pre><code class="language-python">color = {'red': 1, 'green': 2, 'blue': 3}

color['red']            # 1  — 키로 값 접근
color['yellow'] = 3     # 새 키-값 쌍 추가
color['red'] = 4        # 기존 키의 값 수정
del color['red']        # 키로 삭제</code></pre>
<h3 id="in-연산자">in 연산자</h3>
<p>딕셔너리에서 <code>in</code>은 <strong>키</strong>를 기준으로 검색합니다. 값으로는 검색되지 않습니다.</p>
<pre><code class="language-python">'red' in color    # True   — key 검색
2 in color        # False  — value는 검색 안 됨</code></pre>
<h3 id="주요-메서드-2">주요 메서드</h3>
<pre><code class="language-python">score = {'kor': 80, 'eng': 70, 'math': 90}

score.keys()    # dict_keys(['kor', 'eng', 'math'])
score.values()  # dict_values([80, 70, 90])
score.items()   # dict_items([('kor', 80), ('eng', 70), ('math', 90)])

score.get('kor')   # 80  — 키로 값 가져오기
score.clear()      # 전체 삭제</code></pre>
<p><code>update()</code>를 사용하면 다른 딕셔너리를 병합할 수 있습니다.</p>
<pre><code class="language-python">v1 = {1: 'one', 2: 'two'}
v2 = {100: 'hundred', 1000: 'thousand'}

v1.update(v2)
print(v1)   # {1: 'one', 2: 'two', 100: 'hundred', 1000: 'thousand'}</code></pre>
<h3 id="참조-복사-주의">참조 복사 주의</h3>
<p>리스트와 마찬가지로 <code>=</code> 대입은 참조 복사입니다.</p>
<pre><code class="language-python">d1 = {1: 30, 2: 12, 5: 22}
d2 = d1        # 같은 메모리 참조

d2[4] = 33
print(d1)   # {1: 30, 2: 12, 5: 22, 4: 33}  ← d1도 바뀜</code></pre>
<hr />
<h2 id="집합-set">집합 (Set)</h2>
<p>집합은 <strong>순서가 없고 중복이 없는</strong> 자료형입니다.<br />중괄호 <code>{}</code>로 선언하지만, 빈 집합은 반드시 <code>set()</code>으로 만들어야 합니다.</p>
<pre><code class="language-python">ss = {2, 3, 4, 5, 9}
type(ss)   # set

ss1 = set()   # 빈 집합
ss2 = {}      # 이건 dict!  ← 주의</code></pre>
<p><code>set()</code>은 다양한 자료형으로부터 집합을 만들 수 있습니다.</p>
<pre><code class="language-python">set((1, 2, 3))           # {1, 2, 3}  — 튜플에서
set([1, 2, 3])           # {1, 2, 3}  — 리스트에서
set('abcd')              # {'a', 'b', 'c', 'd'}  — 문자열에서
set((1, 2, 3, 1, 2, 3))  # {1, 2, 3}  — 중복 자동 제거</code></pre>
<p>순서가 없기 때문에 인덱싱이 불가능합니다. 인덱싱이 필요하다면 리스트나 튜플로 변환 후 사용합니다.</p>
<h3 id="주요-메서드-3">주요 메서드</h3>
<pre><code class="language-python">ss = {2, 3, 4, 5, 9}

ss.add(8)        # {2, 3, 4, 5, 8, 9}  — 요소 추가
ss.discard(5)    # 있으면 삭제, 없어도 에러 없음
ss.remove(4)     # 있으면 삭제, 없으면 KeyError 발생
ss.pop()         # 임의 요소 하나 꺼내어 삭제
ss.clear()       # 전체 삭제</code></pre>
<h3 id="집합-연산">집합 연산</h3>
<pre><code class="language-python">a = {1, 2, 3, 4, 5, 6}
b = {4, 5, 6, 7, 8, 9}

a | b   # 합집합   {1, 2, 3, 4, 5, 6, 7, 8, 9}
a &amp; b   # 교집합   {4, 5, 6}
a - b   # 차집합   {1, 2, 3}
a ^ b   # 대칭차집합 (합집합 - 교집합)   {1, 2, 3, 7, 8, 9}</code></pre>
<p>메서드로도 동일하게 사용할 수 있습니다.</p>
<pre><code class="language-python">a.union(b)                  # 합집합
a.intersection(b)           # 교집합
a.difference(b)             # 차집합
a.symmetric_difference(b)   # 대칭차집합</code></pre>
<h3 id="활용-예시--중복-제거">활용 예시 — 중복 제거</h3>
<pre><code class="language-python">salesList = ['라면', '달걀', '도시락', '라면', '삼각김밥', '삼각김밥']
set(salesList)   # {'달걀', '도시락', '라면', '삼각김밥'}</code></pre>
<blockquote>
<p>리스트에서 중복을 제거할 때 <code>set()</code>으로 변환하는 것이 가장 간단합니다.</p>
</blockquote>
<hr />
<h2 id="심화--컴프리헨션--zip--복사">심화 — 컴프리헨션 / zip / 복사</h2>
<h3 id="리스트-컴프리헨션-list-comprehension">리스트 컴프리헨션 (List Comprehension)</h3>
<p><code>for</code>문을 리스트 안에 포함시켜 <strong>한 줄로</strong> 리스트를 생성하는 문법입니다.</p>
<pre><code>[표현식 for 항목 in 반복가능객체 if 조건문]</code></pre><p>기존 방식과 비교하면 다음과 같습니다.</p>
<pre><code class="language-python"># 기존 방식
numList = []
for num in range(1, 21):
    if num % 3 == 0:
        numList.append(num)

# 컴프리헨션
numList = [num for num in range(1, 21) if num % 3 == 0]
# [3, 6, 9, 12, 15, 18]</code></pre>
<p>조건 분기(<code>if-else</code>)도 표현식 안에 사용할 수 있습니다.</p>
<pre><code class="language-python"># 3의 배수는 그대로, 아니면 0으로
numList = [num if num % 3 == 0 else 0 for num in range(1, 21)]
# [0, 0, 3, 0, 0, 6, 0, 0, 9, ...]</code></pre>
<p>2차원 리스트 초기화에도 자주 활용됩니다.</p>
<pre><code class="language-python">arr = [[0 for _ in range(5)] for _ in range(5)]
# 5×5 2차원 리스트 초기화</code></pre>
<h3 id="딕셔너리-컴프리헨션-dict-comprehension">딕셔너리 컴프리헨션 (Dict Comprehension)</h3>
<p>딕셔너리도 같은 방식으로 간결하게 작성할 수 있습니다.</p>
<pre><code class="language-python">names = ['Merry', 'John', 'Chris']
num   = [1, 2, 3]

dic = {k: v for k, v in zip(names, num)}
print(dic)   # {'Merry': 1, 'John': 2, 'Chris': 3}</code></pre>
<h3 id="zip--두-리스트-동시-순회">zip() — 두 리스트 동시 순회</h3>
<p><code>zip()</code>은 두 개 이상의 리스트를 동시에 묶어서 순회할 때 사용합니다. 길이가 다를 경우 <strong>짧은 쪽을 기준으로</strong> 묶입니다.</p>
<pre><code class="language-python">foods = ['떡볶이', '라면', '오뎅', '피자']
sides = ['단무지', '김치', '쿨피스']

for food, side in zip(foods, sides):
    print(food, '--&gt;', side)

# 떡볶이 --&gt; 단무지
# 라면 --&gt; 김치
# 오뎅 --&gt; 쿨피스</code></pre>
<p><code>zip()</code>으로 리스트나 딕셔너리로 변환하는 것도 가능합니다.</p>
<pre><code class="language-python">list(zip(foods, sides))   # [('떡볶이', '단무지'), ('라면', '김치'), ('오뎅', '쿨피스')]
dict(zip(foods, sides))   # {'떡볶이': '단무지', '라면': '김치', '오뎅': '쿨피스'}</code></pre>
<h3 id="얕은-복사-vs-깊은-복사">얕은 복사 vs 깊은 복사</h3>
<p>리스트 복사에서 <code>=</code> 대입은 참조 복사임을 앞서 설명했습니다. 독립적인 복사 방법은 세 가지가 있습니다.</p>
<pre><code class="language-python">orgList = ['떡볶이', '라면', '오뎅', '피자']

# 방법 1 — 슬라이싱
newList1 = orgList[:]

# 방법 2 — copy()
newList2 = orgList.copy()

# 방법 3 — list()
newList3 = list(orgList)</code></pre>
<p>단, 위 세 가지는 모두 <strong>얕은 복사(Shallow Copy)</strong> 입니다. 리스트 안에 리스트가 있는 경우, 내부 리스트는 여전히 참조를 공유합니다. </p>
<p>완전히 독립적인 복사가 필요하다면 <code>copy</code> 모듈의 <code>deepcopy()</code>를 사용합니다.</p>
<pre><code class="language-python">import copy

original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)

deep[0][0] = 999
print(original)   # [[1, 2], [3, 4]]  ← 원본 유지</code></pre>