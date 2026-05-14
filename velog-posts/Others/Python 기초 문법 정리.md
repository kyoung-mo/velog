<blockquote>
<p>AI 수업 진도를 나가면서 Python 기초 문법을 정리한 글입니다.</p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/29696287-d963-4a30-855e-4a744d927ee4/image.png" /></p>
<hr />
<h2 id="목차">목차</h2>
<ul>
<li><a href="https://api.velog.io/rss/@mommers#%EB%B3%80%EC%88%98-%EC%84%A0%EC%96%B8%EA%B3%BC-%EC%9E%90%EB%A3%8C%ED%98%95">변수 선언과 자료형</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%AC%B8%EC%9E%90%EC%97%B4-%EC%84%A0%EC%96%B8-%EC%A3%BC%EC%9D%98%EC%82%AC%ED%95%AD">문자열 선언 주의사항</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%82%B0%EC%88%A0-%EC%97%B0%EC%82%B0%EC%9E%90">산술 연산자</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%AC%B8%EC%9E%90%EC%97%B4-%EB%8B%A4%EB%A3%A8%EA%B8%B0">문자열 다루기</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%ED%91%9C%EC%A4%80-%EC%9E%85%EC%B6%9C%EB%A0%A5-%ED%95%A8%EC%88%98">표준 입출력 함수</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%A0%9C%EC%96%B4%EB%AC%B8">제어문</a></li>
</ul>
<hr />
<h2 id="변수-선언과-자료형">변수 선언과 자료형</h2>
<p>파이썬에서는 C언어와 달리 별도의 타입 선언 없이 값을 바로 대입하면 변수가 선언됩니다.</p>
<pre><code class="language-python">x = 10
name = &quot;영모&quot;
is_pass = True</code></pre>
<p>대표적인 자료형은 다음과 같습니다.</p>
<ul>
<li><strong>int</strong> : 정수 (예: 1, 42, -7)</li>
<li><strong>float</strong> : 실수 (예: 3.14, 0.5)</li>
<li><strong>str</strong> : 문자열 (예: &quot;hello&quot;, 'world')</li>
<li><strong>bool</strong> : 참/거짓 (<code>True</code> / <code>False</code>)</li>
<li><strong>list</strong> : 리스트 (예: [1, 2, 3])</li>
<li><strong>tuple</strong> : 튜플 (예: (1, 2, 3))</li>
<li><strong>dict</strong> : 딕셔너리 (예: {&quot;key&quot;: &quot;value&quot;})</li>
</ul>
<p>특히 <strong>bool 자료형</strong>이 별도로 존재한다는 점을 기억해두면 좋습니다.</p>
<hr />
<h2 id="문자열-선언-주의사항">문자열 선언 주의사항</h2>
<p>문자열은 작은따옴표(<code>'</code>) 또는 큰따옴표(<code>&quot;</code>) 모두 사용 가능합니다.<br />다만 문자열 안에 따옴표가 포함될 경우 주의가 필요합니다.</p>
<pre><code class="language-python"># SyntaxError — 작은따옴표가 중간에 있어 문자열이 중간에 끊김
'Kang's favorite food is apple'

# 해결 — 큰따옴표로 감싸기
&quot;Kang's favorite food is apple&quot;</code></pre>
<pre><code class="language-python"># SyntaxError — 큰따옴표가 중간에 있어 문자열이 중간에 끊김
'&quot;I love you&quot; he says.'

# 해결 — 작은따옴표로 감싸기
'&quot;I love you&quot; he says.'</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ab92458d-d3a2-48f3-ad41-998c36b8d843/image.png" /></p>
<blockquote>
<p>문자열 안에서 사용된 따옴표와 <strong>다른 종류의 따옴표</strong>로 전체를 감싸면 됩니다.</p>
</blockquote>
<hr />
<h2 id="산술-연산자">산술 연산자</h2>
<p>기본 사칙연산 외에 자주 사용하는 연산자 세 가지를 정리합니다.</p>
<pre><code class="language-python">x = 7
y = 3

x / y    # 2.333...  — 일반 나눗셈, 결과는 실수
x // y   # 2         — 몫만 반환 (소수점 버림)
x % y    # 1         — 나머지만 반환</code></pre>
<ul>
<li><code>/</code> : 일반 나눗셈입니다. 결과는 항상 실수(float)로 반환됩니다.</li>
<li><code>//</code> : 나눗셈의 <strong>몫</strong>만 정수로 반환합니다.</li>
<li><code>%</code> : 나눗셈의 <strong>나머지</strong>를 반환합니다. 짝홀수 판별이나 순환 인덱스 처리에 자주 사용됩니다.</li>
</ul>
<hr />
<h2 id="문자열-다루기">문자열 다루기</h2>
<h3 id="문자열-연결-concatenation">문자열 연결 (Concatenation)</h3>
<p>문자열 두 개를 <code>+</code>로 연결하면 그대로 이어붙이는 방식(concatenate)으로 처리됩니다.</p>
<pre><code class="language-python">a = 'Hello'
b = 'World'

a + b          # 'HelloWorld'
a + ' ' + b   # 'Hello World'  (공백도 문자열로 직접 넣어야 합니다)</code></pre>
<p><code>*</code> 연산자는 문자열을 반복합니다.</p>
<pre><code class="language-python">c = 'hello'
c * 3    # 'hellohellohello'</code></pre>
<p>문자열과 숫자는 <code>+</code> 연산이 불가능합니다. <code>str()</code>로 변환이 필요합니다.</p>
<pre><code class="language-python">score = 90
'I got ' + score + ' in the exam'      # TypeError!
'I got ' + str(score) + ' in the exam' # 정상 동작</code></pre>
<hr />
<h3 id="인덱싱-indexing">인덱싱 (Indexing)</h3>
<p><code>[]</code>를 사용해 문자열의 각 문자에 접근할 수 있습니다.<br />인덱스는 <strong>0부터 시작</strong>하며, 음수 인덱스로 뒤에서부터 접근하는 것도 가능합니다.</p>
<pre><code class="language-python">greeting = 'Good Morning'

greeting[0]    # 'G'
greeting[5]    # 'M'
greeting[-1]   # 'g'  (마지막 문자)
greeting[-12]  # 'G'  (뒤에서 12번째)</code></pre>
<hr />
<h3 id="슬라이싱-slicing">슬라이싱 (Slicing)</h3>
<p><code>[시작:끝:간격]</code> 형식으로 부분 문자열을 추출할 수 있습니다.<br />끝 인덱스는 결과에 포함되지 않습니다.</p>
<pre><code class="language-python">greeting = 'Good Morning'

greeting[0:4]   # 'Good'
greeting[:4]    # 'Good'    (시작 생략 → 처음부터)
greeting[5:]    # 'Morning' (끝 생략 → 끝까지)
greeting[::-1]  # 'gninroM dooG' (문자열 뒤집기)</code></pre>
<p>날짜 문자열 파싱에도 유용하게 사용할 수 있습니다.</p>
<pre><code class="language-python">a = '20190925Tuesday'
year  = a[0:4]   # '2019'
month = a[4:6]   # '09'
day   = a[6:8]   # '25'</code></pre>
<p>오타 수정에도 활용할 수 있습니다.</p>
<pre><code class="language-python">b = 'Pithon'
b[:1] + 'y' + b[2:]   # 'Python'</code></pre>
<hr />
<h3 id="포맷팅-formatting">포맷팅 (Formatting)</h3>
<h4 id="-포맷팅">% 포맷팅</h4>
<pre><code class="language-python">name  = 'Kang'
score = 95

'%s got %d score' % (name, score)   # 'Kang got 95 score'</code></pre>
<table>
<thead>
<tr>
<th>포맷</th>
<th>의미</th>
</tr>
</thead>
<tbody><tr>
<td><code>%d</code></td>
<td>정수</td>
</tr>
<tr>
<td><code>%s</code></td>
<td>문자열</td>
</tr>
<tr>
<td><code>%f</code></td>
<td>실수</td>
</tr>
</tbody></table>
<h4 id="format-함수">format 함수</h4>
<pre><code class="language-python">'I ate {} oranges'.format(3)
'I ate {0} oranges and ate more {1}.'.format(4, 'two')
'I ate {num1} oranges'.format(num1=4)

# 정렬
'I ate {0:&gt;10} oranges'.format('three')  # 오른쪽 정렬
'I ate {0:&lt;10} oranges'.format('three')  # 왼쪽 정렬
'I ate {0:^10} oranges'.format('three')  # 가운데 정렬</code></pre>
<h4 id="f-string-python-36-이상">f-string (Python 3.6 이상)</h4>
<p>가장 직관적인 포맷팅 방식으로, 현재 가장 많이 사용되는 방법입니다.</p>
<pre><code class="language-python">number = 3
f'I ate {number} oranges'</code></pre>
<hr />
<h2 id="표준-입출력-함수">표준 입출력 함수</h2>
<h3 id="print">print</h3>
<pre><code class="language-python">print('hello', 'world!')   # hello world!
print('hello' + 'world!')  # helloworld!</code></pre>
<ul>
<li><code>,</code>로 구분하면 자동으로 공백이 삽입됩니다.</li>
<li><code>+</code>로 연결하면 공백 없이 이어붙입니다.</li>
</ul>
<p>포맷팅을 활용한 출력도 가능합니다.</p>
<pre><code class="language-python">name  = 'Kang'
score = 95
print('%s got %d score' % (name, score))   # Kang got 95 score</code></pre>
<hr />
<h3 id="input">input</h3>
<p><code>input()</code>의 반환값은 항상 <strong>문자열(str)</strong>입니다.<br />숫자 연산이 필요한 경우 반드시 형변환을 해주어야 합니다.</p>
<pre><code class="language-python">y = input('정수값을 입력하세요: ')
y + 10   # TypeError!</code></pre>
<pre><code class="language-python">y = int(input('정수값을 입력하세요: '))
y + 10   # 정상 동작

type(y)  # &lt;class 'int'&gt;</code></pre>
<blockquote>
<p><code>int(input(...))</code>처럼 감싸주면 입력받는 즉시 정수로 변환됩니다.</p>
</blockquote>
<hr />
<h2 id="제어문">제어문</h2>
<h3 id="if-문">if 문</h3>
<p>C언어와의 가장 큰 차이는 <strong>중괄호 <code>{}</code> 대신 들여쓰기(4칸)</strong>로 블록을 구분한다는 점입니다.</p>
<pre><code class="language-c">// C언어
if (x &gt; 0) {
    printf(&quot;양수입니다.&quot;);
}</code></pre>
<pre><code class="language-python"># Python
if x &gt; 0:
    print(&quot;양수입니다.&quot;)</code></pre>
<blockquote>
<p>파이썬에서 들여쓰기는 단순한 코딩 스타일이 아니라 <strong>문법 그 자체</strong>입니다.<br />들여쓰기가 맞지 않으면 즉시 에러가 발생하므로 주의해야 합니다.</p>
</blockquote>
<p>또한 <code>else if</code> 대신 <strong><code>elif</code></strong> 를 사용합니다.</p>
<pre><code class="language-python">score = 75

if score &gt;= 90:
    print(&quot;A&quot;)
elif score &gt;= 80:
    print(&quot;B&quot;)
elif score &gt;= 70:
    print(&quot;C&quot;)
else:
    print(&quot;F&quot;)</code></pre>
<hr />
<h3 id="while-문">while 문</h3>
<p>조건이 참인 동안 반복하는 구조입니다.</p>
<pre><code class="language-python">jajang = 0
while jajang &lt; 10:
    jajang += 1
    print(f'짜장면을 {jajang}그릇 먹었습니다.')

    if jajang == 10:
        print('무료 쿠폰을 받았습니다.')</code></pre>
<p><code>break</code>, <code>continue</code> 등 나머지 구조는 C언어와 거의 동일합니다.</p>
<hr />
<h3 id="for-반복문">for 반복문</h3>
<pre><code class="language-python">for 변수 in 리스트/튜플/문자열:
    수행문1
    수행문2</code></pre>
<p>단순 n회 반복에는 <code>range(n)</code>을 사용합니다.</p>
<pre><code class="language-python">for i in range(5):
    print(i)   # 0, 1, 2, 3, 4</code></pre>
<p>범위를 지정할 경우 <code>range(시작, 끝)</code>으로 작성합니다. 끝 값은 포함되지 않습니다.</p>
<pre><code class="language-python"># 1부터 10까지 합계 구하기
total = 0
for i in range(1, 11):   # 1 이상 11 미만
    total += i
print(total)   # 55</code></pre>