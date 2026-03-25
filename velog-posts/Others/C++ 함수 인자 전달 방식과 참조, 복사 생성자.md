<p>함수와 참조, 복사 생성자 등등 오늘 나갔던 수업을 정리해보겠습니다.</p>
<h2 id="1-함수-인자-전달-방식-3가지">1. 함수 인자 전달 방식 3가지</h2>
<p>C++에서 함수에 값을 전달하는 방법은 크게 세 가지입니다.</p>
<h3 id="값에-의한-호출-call-by-value">값에 의한 호출 (Call by Value)</h3>
<p>함수가 호출될 때 매개변수가 스택에 새로 생성되고, 호출한 쪽의 값이 그대로 <strong>복사</strong>됩니다.</p>
<pre><code class="language-cpp">void swap(int a, int b) {
    int tmp = a; a = b; b = tmp;
}
int main() {
    int m = 2, n = 9;
    swap(m, n);
    cout &lt;&lt; m &lt;&lt; ' ' &lt;&lt; n; // 여전히 2 9 → 원본 안 바뀜
}</code></pre>
<p>복사된 공간에서 작업하므로 함수가 끝나면 메모리가 반환됩니다. 원본을 바꿀 수 없다는 단점이 있습니다.</p>
<hr />
<h3 id="주소에-의한-호출-call-by-address">주소에 의한 호출 (Call by Address)</h3>
<p>매개변수를 포인터 타입으로 선언하고, 호출 시 주소값(<code>&amp;</code>)을 넘깁니다.</p>
<pre><code class="language-cpp">void swap(int *a, int *b) {
    int tmp = *a; *a = *b; *b = tmp;
}
int main() {
    int m = 2, n = 9;
    swap(&amp;m, &amp;n);
    cout &lt;&lt; m &lt;&lt; ' ' &lt;&lt; n; // 9 2 → 원본이 바뀜
}</code></pre>
<p>원본 주소를 넘기기 때문에 함수 안에서 원본 값을 변경할 수 있습니다.</p>
<hr />
<h3 id="참조에-의한-호출-call-by-reference">참조에 의한 호출 (Call by Reference)</h3>
<p>매개변수를 참조 타입(<code>&amp;</code>)으로 선언합니다. 포인터처럼 원본을 직접 다루지만, <code>*</code>나 <code>&amp;</code> 연산자 없이 일반 변수처럼 사용할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/139ca1a6-fd6e-44d7-91e8-687758a013aa/image.png" /></p>
<pre><code class="language-cpp">void swap(int &amp;a, int &amp;b) {
    int tmp = a; a = b; b = tmp;
}
int main() {
    int m = 2, n = 9;
    swap(m, n);
    cout &lt;&lt; m &lt;&lt; ' ' &lt;&lt; n; // 9 2 → 원본이 바뀜
}</code></pre>
<p>참조 매개변수는 이름만 생기고 새로운 메모리 공간이 할당되지 않습니다. 실인자 변수의 공간을 그대로 공유하는 방식입니다.</p>
<hr />
<h2 id="2-참조reference란">2. 참조(Reference)란?</h2>
<p>이미 존재하는 변수나 객체에 붙이는 <strong>별명(alias)</strong> 입니다.</p>
<pre><code class="language-cpp">int n = 2;
int &amp;refn = n;  // refn은 n의 별명

refn = 3;       // n = 3 이 됨</code></pre>
<p>참조 변수의 특징은 다음과 같습니다.</p>
<ul>
<li>선언 시 반드시 초기화해야 합니다.</li>
<li>새로운 메모리 공간이 생기지 않습니다 (생성자/소멸자 호출 없음).</li>
<li>포인터(<code>*</code>) 없이 원본을 다룰 수 있습니다.</li>
</ul>
<p>객체에도 동일하게 적용됩니다.</p>
<pre><code class="language-cpp">Circle circle;
Circle &amp;refc = circle;
refc.setRadius(30); // circle.setRadius(30)과 동일</code></pre>
<hr />
<h2 id="3-참조-매개변수-활용--여러-값을-반환하고-싶을-때">3. 참조 매개변수 활용 — 여러 값을 반환하고 싶을 때</h2>
<p>함수의 리턴 값은 하나뿐이지만, 참조 매개변수를 사용하면 여러 값을 호출한 쪽으로 돌려줄 수 있습니다.</p>
<pre><code class="language-cpp">bool average(int a[], int size, int &amp;avg) {
    if (size &lt;= 0) return false;
    int sum = 0;
    for (int i = 0; i &lt; size; i++) sum += a[i];
    avg = sum / size;
    return true;
}</code></pre>
<p><code>avg</code>는 참조 매개변수이므로 함수 안에서 값을 대입하면 호출한 쪽의 변수에 직접 반영됩니다. 리턴 값은 성공/실패 여부를 알리는 데 쓸 수 있습니다.</p>
<hr />
<h2 id="4-참조-리턴">4. 참조 리턴</h2>
<p>C++에서는 함수가 값 대신 <strong>참조를 리턴</strong>할 수 있습니다.</p>
<pre><code class="language-cpp">char c = 'a';

char&amp; find() {
    return c; // c에 대한 참조 리턴
}

find() = 'b'; // c = 'b' 가 됨</code></pre>
<p>참조를 리턴하면 함수 호출 자체가 변수처럼 사용될 수 있습니다.</p>
<h3 id="메서드-체이닝에-활용">메서드 체이닝에 활용</h3>
<pre><code class="language-cpp">Circle&amp; plus(int n) {
    radius += n;
    return *this; // 자기 자신의 참조를 리턴
}

a.plus(1).plus(2).plus(3); // radius에 1, 2, 3이 순차적으로 더해짐</code></pre>
<p>만약 <code>Circle&amp;</code> 대신 <code>Circle</code>(값 리턴)로 선언하면, 매번 복사본이 리턴되기 때문에 원본 객체가 아닌 복사본에 연산이 쌓입니다. 결과적으로 마지막 <code>plus(3)</code>만 원본에 반영되는 것처럼 보이게 됩니다.</p>
<hr />
<h2 id="5-복사-생성자-copy-constructor">5. 복사 생성자 (Copy Constructor)</h2>
<h3 id="복사-생성자란">복사 생성자란?</h3>
<p>객체를 복사해서 새 객체를 만들 때 자동으로 호출되는 생성자입니다.</p>
<pre><code class="language-cpp">Circle::Circle(const Circle&amp; c) {
    // const를 쓰는 이유: 원본 객체 c를 읽기 전용으로만 사용하겠다는 의미입니다.
    this-&gt;radius = c.radius;
}</code></pre>
<p>복사 생성자가 호출되는 상황은 세 가지입니다.</p>
<ol>
<li><code>Circle dest(src);</code> 처럼 객체로 객체를 초기화할 때</li>
<li>함수에 <strong>값으로</strong> 객체를 전달할 때 (<code>call by value</code>)</li>
<li>함수가 객체를 <strong>값으로</strong> 리턴할 때</li>
</ol>
<p>복사 생성자를 직접 정의하지 않으면 컴파일러가 <strong>디폴트 복사 생성자</strong>를 자동 생성합니다. 이때 기존 교재에서 &quot;생성자가 실행되지 않는다&quot;고 표현하는 경우가 있는데, 정확히는 우리가 정의한 생성자가 실행되지 않는 것이고, 컴파일러가 자동 생성한 복사 생성자가 실행되는 것입니다.</p>
<hr />
<h3 id="얕은-복사-vs-깊은-복사">얕은 복사 vs 깊은 복사</h3>
<p>클래스 멤버에 <strong>동적 할당된 포인터</strong>가 있을 때 이 둘의 차이가 발생합니다.</p>
<table>
<thead>
<tr>
<th>구분</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><strong>얕은 복사 (Shallow Copy)</strong></td>
<td>포인터 값(주소)만 복사 → 원본과 사본이 같은 메모리를 공유</td>
</tr>
<tr>
<td><strong>깊은 복사 (Deep Copy)</strong></td>
<td>포인터가 가리키는 메모리까지 별도로 새로 할당하고 내용을 복사</td>
</tr>
</tbody></table>
<pre><code class="language-cpp">// 얕은 복사 (디폴트 복사 생성자 동작)
Person::Person(const Person&amp; p) {
    this-&gt;name = p.name; // 주소만 복사 → 같은 메모리 공유 → 문제 발생
}

// 깊은 복사 (직접 정의)
Person::Person(const Person&amp; p) {
    this-&gt;id = p.id;
    int len = strlen(p.name);
    this-&gt;name = new char[len + 1]; // 새로운 메모리 할당
    strcpy(this-&gt;name, p.name);     // 내용 복사
}</code></pre>
<p>얕은 복사의 문제는 원본과 사본이 같은 메모리를 가리키기 때문에, 한쪽에서 이름을 바꾸면 다른 쪽도 바뀌고, 소멸자가 두 번 호출될 때 같은 메모리를 두 번 해제하려다 프로그램이 비정상 종료될 수 있습니다.</p>
<p>따라서 포인터 멤버가 있는 클래스는 <strong>반드시 깊은 복사 생성자를 직접 정의</strong>해야 합니다.</p>
<hr />
<h2 id="정리">정리</h2>
<table>
<thead>
<tr>
<th>전달 방식</th>
<th>새 공간 생성</th>
<th>원본 수정</th>
<th>생성자/소멸자</th>
</tr>
</thead>
<tbody><tr>
<td>Call by Value</td>
<td>O</td>
<td>X</td>
<td>호출됨 (복사 생성자)</td>
</tr>
<tr>
<td>Call by Address</td>
<td>O (포인터 변수)</td>
<td>O</td>
<td>호출 안 됨</td>
</tr>
<tr>
<td>Call by Reference</td>
<td>X</td>
<td>O</td>
<td>호출 안 됨</td>
</tr>
</tbody></table>
<ul>
<li>참조(<code>&amp;</code>)는 포인터의 장점(원본 접근)과 변수의 장점(간편한 문법)을 함께 가집니다.</li>
<li>복사 생성자는 동적 메모리를 가진 클래스에서 얕은/깊은 복사 차이가 중요합니다.</li>
<li><code>const</code> 참조 매개변수(<code>const Circle&amp; c</code>)는 원본을 읽기 전용으로만 사용하겠다는 의미입니다.</li>
</ul>