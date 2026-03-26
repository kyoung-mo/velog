<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/28ae2b8c-b73e-426d-ad43-4bbfe02b493e/image.png" /></p>
<h2 id="프렌드friend란">프렌드(friend)란?</h2>
<p>&quot;내 가족의 일원은 아니지만, 마치 내 가족인 것처럼 동일한 권한을 가진 멤버로 인정받은 사람&quot;이라는 표현이 가장 잘 어울리는 개념입니다.</p>
<p><code>friend</code> 키워드를 사용하면 <strong>외부 함수나 다른 클래스의 멤버 함수</strong>에게 내 클래스의 <code>private</code>, <code>protected</code> 멤버까지 접근할 수 있는 권한을 부여할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fdaf76e0-2dc9-4ef1-a413-20c54f8b4892/image.png" /></p>
<h3 id="프렌드의-특징">프렌드의 특징</h3>
<ul>
<li>클래스의 멤버 함수가 <strong>아닙니다</strong> → 상속되지 않습니다</li>
<li>오직 <strong>함수</strong>만 프렌드가 될 수 있습니다 (프렌드 변수는 없습니다)</li>
<li><code>friend</code> 선언은 <code>public</code>, <code>private</code> 어디에 써도 동일하게 동작합니다<ul>
<li>접근 지정자는 &quot;이 접근이 허용된 범위에서 온 건지&quot; 체크하는 규칙이고, <code>friend</code>는 그 규칙에 대한 <strong>명시적 예외(허가증)</strong> 이기 때문입니다</li>
</ul>
</li>
</ul>
<h3 id="프렌드를-쓰는-이유">프렌드를 쓰는 이유</h3>
<p>클래스 멤버 함수로 선언하기엔 무리가 있지만, 클래스의 <code>private</code> / <code>protected</code> 멤버에 접근해야 하는 특별한 경우에 사용합니다.</p>
<hr />
<h2 id="프렌드-3가지-유형">프렌드 3가지 유형</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/12ed8af6-b0d7-4941-9b86-bbab78733e89/image.png" /></p>
<h3 id="1-전역-함수를-프렌드로-선언">1. 전역 함수를 프렌드로 선언</h3>
<pre><code class="language-cpp">class Rect {
    int width, height;
public:
    Rect(int width, int height) { this-&gt;width = width; this-&gt;height = height; }
    friend bool equals(Rect r, Rect s); // 전역 함수를 프렌드로 선언
};

bool equals(Rect r, Rect s) {
    if (r.width == s.width &amp;&amp; r.height == s.height) return true;
    else return false;
}</code></pre>
<p>여기서 주의할 점은 <strong>전방선언(forward declaration)</strong> 입니다.</p>
<p>컴파일러는 코드를 위에서 아래로 읽기 때문에, <code>class Rect</code> 정의 전에 <code>equals</code> 함수를 선언하려면 <code>Rect</code>가 뭔지 미리 알려줘야 합니다.</p>
<pre><code class="language-cpp">class Rect;               // Rect가 나중에 나올 거라고 미리 알림
bool equals(Rect r, Rect s); // 이제 Rect를 타입으로 사용 가능</code></pre>
<h3 id="2-다른-클래스의-멤버-함수를-프렌드로-선언">2. 다른 클래스의 멤버 함수를 프렌드로 선언</h3>
<pre><code class="language-cpp">class Rect {
    int width, height;
public:
    Rect(int width, int height) { this-&gt;width = width; this-&gt;height = height; }
    friend bool RectManager::equals(Rect r, Rect s); // RectManager의 특정 멤버 함수만 프렌드
};</code></pre>
<h3 id="3-다른-클래스-전체를-프렌드로-선언">3. 다른 클래스 전체를 프렌드로 선언</h3>
<pre><code class="language-cpp">class Rect {
    int width, height;
public:
    Rect(int width, int height) { this-&gt;width = width; this-&gt;height = height; }
    friend RectManager; // RectManager의 모든 멤버 함수가 Rect의 프렌드
};</code></pre>
<hr />
<h2 id="연산자-중복operator-overloading이란">연산자 중복(Operator Overloading)이란?</h2>
<p>C++에 본래 있는 연산자(<code>+</code>, <code>==</code>, <code>++</code> 등)에 <strong>사용자 정의 클래스에 맞는 새로운 의미</strong>를 부여하는 것입니다.</p>
<pre><code class="language-cpp">Color a(BLUE), b(RED), c;
c = a + b; // Color 객체끼리 + 연산이 가능하도록 정의</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b679a761-d1d4-48f3-bdd2-04e850ffd0bf/image.png" /></p>
<h3 id="연산자-중복의-특징">연산자 중복의 특징</h3>
<ul>
<li>C++에 <strong>본래 있는 연산자</strong>만 중복 가능합니다 (<code>%%</code>, <code>##</code> 같은 건 불가)</li>
<li>피연산자 타입이나 개수를 바꿀 수 없습니다</li>
<li>연산자의 <strong>우선순위와 결합성</strong>은 바꿀 수 없습니다</li>
</ul>
<hr />
<h2 id="연산자-함수-구현-방법">연산자 함수 구현 방법</h2>
<p>연산자 함수는 두 가지 방법으로 구현할 수 있습니다.</p>
<ol>
<li><strong>클래스의 멤버 함수</strong>로 구현</li>
<li><strong>외부 함수</strong>로 구현하고 클래스에 프렌드로 선언</li>
</ol>
<p>형식은 다음과 같습니다.</p>
<pre><code class="language-cpp">리턴타입 operator연산자(매개변수 리스트);</code></pre>
<hr />
<h2 id="이항-연산자-중복">이항 연산자 중복</h2>
<h3 id="-연산자-멤버-함수로-구현">+ 연산자 (멤버 함수로 구현)</h3>
<pre><code class="language-cpp">class Power {
    int kick, punch;
public:
    Power(int kick = 0, int punch = 0) { this-&gt;kick = kick; this-&gt;punch = punch; }
    Power operator+(Power op2);
};

Power Power::operator+(Power op2) {
    Power tmp;
    tmp.kick = this-&gt;kick + op2.kick;
    tmp.punch = this-&gt;punch + op2.punch;
    return tmp;
}</code></pre>
<p><code>a + b</code>는 내부적으로 <code>a.operator+(b)</code> 로 처리됩니다. 즉 <code>this</code>가 <code>a</code>, <code>op2</code>가 <code>b</code>입니다.</p>
<h3 id="-연산자">== 연산자</h3>
<pre><code class="language-cpp">bool Power::operator==(Power op2) {
    if (kick == op2.kick &amp;&amp; punch == op2.punch) return true;
    else return false;
}</code></pre>
<h3 id="-연산자-1">+= 연산자</h3>
<p><code>c = a += b</code> 처럼 연속 대입이 가능하려면 <strong>자기 자신의 참조(<code>*this</code>)를 리턴</strong>해야 합니다.</p>
<pre><code class="language-cpp">Power&amp; Power::operator+=(Power op2) {
    kick = kick + op2.kick;
    punch = punch + op2.punch;
    return *this; // 변경된 자신을 참조로 리턴
}</code></pre>
<h3 id="b--a--2-처럼-정수와-연산하는-경우">b = a + 2 처럼 정수와 연산하는 경우</h3>
<pre><code class="language-cpp">Power Power::operator+(int op2) {
    Power tmp;
    tmp.kick = kick + op2;
    tmp.punch = punch + op2;
    return tmp;
}</code></pre>
<hr />
<h2 id="단항-연산자-중복">단항 연산자 중복</h2>
<h3 id="전위--연산자">전위 ++ 연산자</h3>
<p><code>++a</code> : 먼저 증가시키고, <strong>증가된 자신을 참조로 리턴</strong>합니다.</p>
<pre><code class="language-cpp">Power&amp; Power::operator++() {
    kick++;
    punch++;
    return *this; // 변경된 객체 자신의 참조 리턴
}</code></pre>
<h3 id="후위--연산자">후위 ++ 연산자</h3>
<p><code>a++</code> : 증가 이전 상태를 저장해두고, 증가시킨 뒤 <strong>이전 상태를 값으로 리턴</strong>합니다.</p>
<p>후위 연산자임을 컴파일러에게 알리기 위해 <strong><code>int x</code> 매개변수를 더미로</strong> 추가합니다 (실제 사용하지 않음).</p>
<pre><code class="language-cpp">Power Power::operator++(int x) {
    Power tmp = *this; // 증가 이전 상태 저장
    kick++;
    punch++;
    return tmp; // 증가 이전 값 리턴
}</code></pre>
<h3 id="-연산자-2">! 연산자</h3>
<pre><code class="language-cpp">bool Power::operator!() {
    if (kick == 0 &amp;&amp; punch == 0) return true;
    else return false;
}</code></pre>
<hr />
<h2 id="프렌드-함수로-연산자-구현">프렌드 함수로 연산자 구현</h2>
<h3 id="왜-프렌드가-필요한가">왜 프렌드가 필요한가?</h3>
<p><code>2 + a</code> 처럼 <strong>정수가 왼쪽 피연산자</strong>인 경우, 멤버 함수로는 구현이 불가능합니다. 멤버 함수는 항상 <code>this</code>(왼쪽 피연산자)가 해당 클래스의 객체여야 하기 때문입니다.</p>
<p>이 경우 <strong>외부 함수로 구현하고 프렌드로 선언</strong>합니다.</p>
<pre><code class="language-cpp">class Power {
    int kick, punch;
public:
    Power(int kick = 0, int punch = 0) { this-&gt;kick = kick; this-&gt;punch = punch; }
    friend Power operator+(int op1, Power op2); // 프렌드 선언
};

Power operator+(int op1, Power op2) {
    Power tmp;
    tmp.kick = op1 + op2.kick;
    tmp.punch = op1 + op2.punch;
    return tmp;
}</code></pre>
<h3 id="프렌드로-전위후위--구현">프렌드로 전위/후위 ++ 구현</h3>
<p>멤버 함수 방식과 달리 <code>this</code> 대신 <strong>참조 매개변수</strong>를 받습니다.</p>
<pre><code class="language-cpp">// 전위
Power&amp; operator++(Power&amp; op) {
    op.kick++;
    op.punch++;
    return op;
}

// 후위 (더미 int로 구분)
Power operator++(Power&amp; op, int x) {
    Power tmp = op;
    op.kick++;
    op.punch++;
    return tmp;
}</code></pre>
<hr />
<h2 id="연속-호출이-가능한--연산자">연속 호출이 가능한 &lt;&lt; 연산자</h2>
<p><code>a &lt;&lt; 3 &lt;&lt; 5 &lt;&lt; 6</code> 처럼 연속 호출을 지원하려면 <strong>자기 자신의 참조를 리턴</strong>해야 합니다.</p>
<pre><code class="language-cpp">Power&amp; Power::operator&lt;&lt;(int n) {
    kick += n;
    punch += n;
    return *this;
}</code></pre>
<p><code>a &lt;&lt; 3 &lt;&lt; 5 &lt;&lt; 6</code>은 <code>((a &lt;&lt; 3) &lt;&lt; 5) &lt;&lt; 6</code>으로 처리되므로, 매번 <code>*this</code>를 리턴해야 다음 <code>&lt;&lt;</code> 연산이 이어집니다.</p>
<hr />
<h2 id="멤버-함수-vs-프렌드-함수-비교">멤버 함수 vs 프렌드 함수 비교</h2>
<table>
<thead>
<tr>
<th>구분</th>
<th>멤버 함수</th>
<th>프렌드 함수</th>
</tr>
</thead>
<tbody><tr>
<td><code>this</code> 존재</td>
<td>O (왼쪽 피연산자)</td>
<td>X</td>
</tr>
<tr>
<td>매개변수 수</td>
<td>이항이면 1개</td>
<td>이항이면 2개</td>
</tr>
<tr>
<td>좌변이 다른 타입일 때</td>
<td>구현 불가 (<code>2 + a</code>)</td>
<td>구현 가능</td>
</tr>
<tr>
<td>캡슐화</td>
<td>더 자연스러움</td>
<td>private 접근 위해 friend 필요</td>
</tr>
</tbody></table>
<hr />
<h2 id="정리">정리</h2>
<ul>
<li><code>friend</code>는 클래스의 <code>private</code> 멤버에 접근할 수 있는 <strong>허가증</strong>을 외부에 부여합니다</li>
<li>프렌드 선언 위치(<code>public</code>/<code>private</code>)는 동작에 <strong>영향 없습니다</strong></li>
<li>연산자 중복은 <code>operator연산자</code> 형식의 함수로 구현합니다</li>
<li>전위/후위 <code>++</code>는 <strong>참조 리턴 여부</strong>와 <strong>더미 int 매개변수</strong>로 구분합니다</li>
<li>연속 대입/호출(<code>c = a += b</code>, <code>a &lt;&lt; 3 &lt;&lt; 5</code>)이 필요하면 <strong><code>*this</code> 참조를 리턴</strong>합니다</li>
<li>좌변이 클래스 객체가 아닌 경우(<code>2 + a</code>)는 <strong>프렌드 외부 함수</strong>로 구현합니다</li>
</ul>