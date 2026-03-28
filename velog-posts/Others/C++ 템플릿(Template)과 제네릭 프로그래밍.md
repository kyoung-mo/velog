<p>템플릿 + STL 라이브러리 진도를 나가고 있는데 생소한 개념이라 끊어서 정리하려합니다. 템플릿 먼저 정리해보겠습니다.</p>
<h2 id="목차">목차</h2>
<ol>
<li><a href="https://api.velog.io/rss/@mommers#1-%ED%95%A8%EC%88%98-%EC%A4%91%EB%B3%B5%EC%9D%98-%ED%95%9C%EA%B3%84">함수 중복의 한계</a></li>
<li><a href="https://api.velog.io/rss/@mommers#2-%ED%85%9C%ED%94%8C%EB%A6%BF%EC%9D%B4%EB%9E%80">템플릿이란?</a></li>
<li><a href="https://api.velog.io/rss/@mommers#3-%EC%A0%9C%EB%84%A4%EB%A6%AD-%ED%95%A8%EC%88%98-%EB%A7%8C%EB%93%A4%EA%B8%B0">제네릭 함수 만들기</a></li>
<li><a href="https://api.velog.io/rss/@mommers#4-%EA%B5%AC%EC%B2%B4%ED%99%94specialization">구체화(Specialization)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#5-%EA%B5%AC%EC%B2%B4%ED%99%94-%EC%98%A4%EB%A5%98-%EC%A3%BC%EC%9D%98%EC%82%AC%ED%95%AD">구체화 오류 주의사항</a></li>
<li><a href="https://api.velog.io/rss/@mommers#6-%EB%8B%A4%EC%A4%91-%EC%A0%9C%EB%84%A4%EB%A6%AD-%ED%83%80%EC%9E%85">다중 제네릭 타입</a></li>
<li><a href="https://api.velog.io/rss/@mommers#7-%EC%A0%9C%EB%84%A4%EB%A6%AD-%ED%81%B4%EB%9E%98%EC%8A%A4-%EB%A7%8C%EB%93%A4%EA%B8%B0">제네릭 클래스 만들기</a></li>
<li><a href="https://api.velog.io/rss/@mommers#8-%ED%85%9C%ED%94%8C%EB%A6%BF%EC%9D%98-%EC%9E%A5%EB%8B%A8%EC%A0%90">템플릿의 장단점</a></li>
</ol>
<hr />
<h2 id="1-함수-중복의-한계">1. 함수 중복의 한계</h2>
<p>함수 오버로딩을 통해 같은 이름의 함수를 다양한 타입으로 사용할 수 있었습니다. 하지만 타입만 다르고 내부 로직이 동일한 함수를 매번 새로 작성해야 한다는 <strong>코드 중복 문제</strong>가 존재합니다.</p>
<pre><code class="language-cpp">void myswap(int&amp; a, int&amp; b) {
    int tmp;
    tmp = a; a = b; b = tmp;
}

void myswap(double&amp; a, double&amp; b) {
    double tmp;
    tmp = a; a = b; b = tmp;
}</code></pre>
<p>위 두 함수는 타입만 <code>int</code>와 <code>double</code>로 다를 뿐, 로직이 완전히 동일합니다. 이처럼 타입별로 함수를 일일이 작성하는 것은 비효율적이며, 유지보수 측면에서도 좋지 않습니다.</p>
<hr />
<h2 id="2-템플릿이란">2. 템플릿이란?</h2>
<p>이 문제를 해결하기 위해 C++은 <strong>템플릿(Template)</strong> 을 제공합니다.</p>
<blockquote>
<p>템플릿은 함수나 클래스를 <strong>일반화(Generic)</strong> 하여, 타입에 관계없이 동작하는 코드를 틀처럼 찍어내는 C++ 도구입니다.</p>
</blockquote>
<ul>
<li>타입을 매개변수처럼 받아, 필요한 시점에 컴파일러가 구체적인 타입의 코드를 자동 생성합니다.</li>
<li><code>template</code> 키워드와 <code>class T</code> 또는 <code>typename T</code>를 사용하여 선언합니다.</li>
</ul>
<pre><code class="language-cpp">// 기본 선언 형태
template &lt;class T&gt;
void myswap(T&amp; a, T&amp; b) {
    T tmp;
    tmp = a; a = b; b = tmp;
}

// 제네릭 타입이 여러 개인 경우
template &lt;class T1, class T2, class T3&gt;</code></pre>
<p>여기서 <code>T</code>는 <strong>제네릭 타입(Generic Type)</strong> 이라고 부르며, 실제 타입으로 대체될 자리 표시자 역할을 합니다.</p>
<hr />
<h2 id="3-제네릭-함수-만들기">3. 제네릭 함수 만들기</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/af737066-df62-458b-81fe-0d97d1bf7597/image.png" /></p>
<h3 id="예제-1--myswap-제네릭-함수">예제 1 — <code>myswap()</code> 제네릭 함수</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;

class Circle {
    int radius;
public:
    Circle(int radius = 1) { this-&gt;radius = radius; }
    int getRadius() { return radius; }
};

template &lt;class T&gt;
void myswap(T&amp; a, T&amp; b) {
    T tmp;
    tmp = a; a = b; b = tmp;
}

int main() {
    int a = 4, b = 5;
    myswap(a, b);
    cout &lt;&lt; &quot;a= &quot; &lt;&lt; a &lt;&lt; &quot;, b= &quot; &lt;&lt; b &lt;&lt; endl;

    double c = 0.3, d = 12.5;
    myswap(c, d);
    cout &lt;&lt; &quot;c= &quot; &lt;&lt; c &lt;&lt; &quot;, d= &quot; &lt;&lt; d &lt;&lt; endl;

    Circle donut(5), pizza(20);
    myswap(donut, pizza);
    cout &lt;&lt; &quot;donut 반지름 = &quot; &lt;&lt; donut.getRadius() &lt;&lt; &quot;, &quot;;
    cout &lt;&lt; &quot;pizza 반지름 = &quot; &lt;&lt; pizza.getRadius() &lt;&lt; endl;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/51b69681-7dd6-4e3c-be96-2721927506ec/image.png" /></p>
<p><code>int</code>, <code>double</code>, 사용자 정의 클래스(<code>Circle</code>)까지 하나의 함수로 처리할 수 있었습니다. 컴파일러가 호출 시 타입을 추론하여 알맞은 코드를 자동 생성합니다.</p>
<hr />
<h3 id="예제-2--bigger-더-큰-값-반환">예제 2 — <code>bigger()</code>: 더 큰 값 반환</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;

template &lt;class T&gt;
T bigger(T a, T b) {
    if (a &gt; b) return a;
    else return b;
}

int main() {
    int a = 20, b = 50;
    char c = 'a', d = 'z';
    cout &lt;&lt; &quot;bigger(20,50)의 결과는 &quot; &lt;&lt; bigger(a, b) &lt;&lt; endl;
    cout &lt;&lt; &quot;bigger('a','z')의 결과는 &quot; &lt;&lt; bigger(c, d) &lt;&lt; endl;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ce16d60a-e20f-4dc5-aa10-2aa5c7ccdada/image.png" /></p>
<p><code>&gt;</code> 연산자만 정의되어 있으면 어떤 타입이든 사용 가능합니다. <code>int</code>, <code>char</code> 모두 문제없이 동작합니다.</p>
<hr />
<h3 id="예제-3--add-배열-합계-계산">예제 3 — <code>add()</code>: 배열 합계 계산</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;

template &lt;class T&gt;
T add(T data[], int n) {
    T sum = 0;
    for (int i = 0; i &lt; n; i++) {
        sum += data[i];
    }
    return sum;
}

int main() {
    int x[] = { 1, 2, 3, 4, 5 };
    double d[] = { 1.2, 2.3, 3.4, 4.5, 5.6, 6.7 };

    cout &lt;&lt; &quot;sum of x[] = &quot; &lt;&lt; add(x, 5) &lt;&lt; endl;
    cout &lt;&lt; &quot;sum of d[] = &quot; &lt;&lt; add(d, 6) &lt;&lt; endl;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1516d568-2723-4a34-a3dd-c351aaec33f5/image.png" /></p>
<p>배열의 타입에 관계없이 합계를 구할 수 있었습니다. 배열 원소의 타입이 <code>T</code>로 추론되어 <code>sum</code> 변수도 같은 타입으로 동작합니다.</p>
<hr />
<h2 id="4-구체화specialization">4. 구체화(Specialization)</h2>
<p><strong>구체화</strong>란, 제네릭 타입 <code>T</code>에 실제 타입을 지정하여 컴파일러가 구체적인 함수 코드를 생성하는 과정입니다.</p>
<pre><code class="language-cpp">// 템플릿 정의
template &lt;class T&gt;
void myswap(T&amp; a, T&amp; b) {
    T tmp;
    tmp = a; a = b; b = tmp;
}

int main() {
    int a = 4, b = 5;
    myswap(a, b);  // T = int 로 구체화
}</code></pre>
<p>위 코드를 컴파일하면, 컴파일러는 내부적으로 아래와 같은 코드를 생성합니다.</p>
<pre><code class="language-cpp">// 컴파일러가 자동 생성하는 구체화 코드
void myswap(int&amp; a, int&amp; b) {
    int tmp;
    tmp = a; a = b; b = tmp;
}</code></pre>
<p>즉, 개발자가 직접 작성하지 않아도 컴파일러가 템플릿을 기반으로 필요한 함수를 자동으로 만들어 줍니다.</p>
<hr />
<h2 id="5-구체화-오류-주의사항">5. 구체화 오류 주의사항</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/38779393-d01d-4a62-9b04-6847d0fe338d/image.png" /></p>
<p>같은 템플릿 매개변수 <code>T</code>를 사용하는 인자들은 <strong>반드시 동일한 타입</strong>이어야 합니다.</p>
<pre><code class="language-cpp">template &lt;class T&gt;
void myswap(T&amp; a, T&amp; b);  // a, b 모두 T 타입

int s = 4;
double t = 5.0;
myswap(s, t);  // ❌ 컴파일 오류! int와 double은 서로 다른 타입</code></pre>
<p><code>T</code>가 하나이므로 <code>int</code>와 <code>double</code>을 동시에 받는 구체화가 불가능합니다. 서로 다른 타입을 받으려면 아래처럼 다중 제네릭 타입을 사용해야 합니다.</p>
<hr />
<h2 id="6-다중-제네릭-타입">6. 다중 제네릭 타입</h2>
<h3 id="예제-4--mcopy-다른-타입-배열-간-복사">예제 4 — <code>mcopy()</code>: 다른 타입 배열 간 복사</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;

template&lt;class T1, class T2&gt;
void mcopy(T1 src[], T2 dest[], int n) {
    for (int i = 0; i &lt; n; i++) dest[i] = (T2)src[i];
}

int main() {
    int x[] = { 1, 2, 3, 4, 5 };
    double d[5];
    char c[5] = { 'H', 'e', 'l', 'l', 'o' }, e[5];

    mcopy(x, d, 5);  // int → double
    mcopy(c, e, 5);  // char → char

    for (int i = 0; i &lt; 5; i++) cout &lt;&lt; d[i] &lt;&lt; ' ';
    cout &lt;&lt; endl;
    for (int i = 0; i &lt; 5; i++) cout &lt;&lt; e[i] &lt;&lt; ' ';
    cout &lt;&lt; endl;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8371a42f-2191-4f85-8e53-3000c9477b4b/image.png" /></p>
<p><code>T1</code>, <code>T2</code> 두 개의 제네릭 타입을 사용하여 서로 다른 타입의 배열 간 복사를 구현했습니다. <code>(T2)src[i]</code> 로 명시적 형변환을 수행하고 있습니다.</p>
<hr />
<h2 id="7-제네릭-클래스-만들기">7. 제네릭 클래스 만들기</h2>
<p>함수뿐만 아니라 <strong>클래스도 템플릿화</strong>할 수 있습니다.</p>
<h3 id="선언-형태">선언 형태</h3>
<pre><code class="language-cpp">template &lt;class T&gt;
class MyStack {
    int tos;
    T data[100];
public:
    MyStack();
    void push(T element);
    T pop();
};</code></pre>
<h3 id="멤버-함수-구현-클래스-외부">멤버 함수 구현 (클래스 외부)</h3>
<p>클래스 외부에서 구현할 때는 각 함수마다 <code>template &lt;class T&gt;</code> 를 붙이고, 클래스명에도 <code>&lt;T&gt;</code>를 명시해야 합니다.</p>
<pre><code class="language-cpp">template &lt;class T&gt;
MyStack&lt;T&gt;::MyStack() {
    tos = -1;
}

template &lt;class T&gt;
void MyStack&lt;T&gt;::push(T element) {
    if (tos == 99) { cout &lt;&lt; &quot;stack full&quot;; return; }
    tos++;
    data[tos] = element;
}

template &lt;class T&gt;
T MyStack&lt;T&gt;::pop() {
    if (tos == -1) { cout &lt;&lt; &quot;stack empty&quot;; return 0; }
    return data[tos--];
}</code></pre>
<h3 id="예제-5--제네릭-스택-클래스-전체-코드">예제 5 — 제네릭 스택 클래스 전체 코드</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;

template &lt;class T&gt;
class MyStack {
    int tos;
    T data[100];
public:
    MyStack();
    void push(T element);
    T pop();
};

template &lt;class T&gt;
MyStack&lt;T&gt;::MyStack() { tos = -1; }

template &lt;class T&gt;
void MyStack&lt;T&gt;::push(T element) {
    if (tos == 99) { cout &lt;&lt; &quot;stack full&quot;; return; }
    tos++;
    data[tos] = element;
}

template &lt;class T&gt;
T MyStack&lt;T&gt;::pop() {
    T retData;
    if (tos == -1) { cout &lt;&lt; &quot;stack empty&quot;; return 0; }
    retData = data[tos--];
    return retData;
}

int main() {
    MyStack&lt;int&gt; iStack;
    iStack.push(3);
    cout &lt;&lt; iStack.pop() &lt;&lt; endl;

    MyStack&lt;double&gt; dStack;
    dStack.push(3.5);
    cout &lt;&lt; dStack.pop() &lt;&lt; endl;

    MyStack&lt;char&gt;* p = new MyStack&lt;char&gt;();
    p-&gt;push('a');
    cout &lt;&lt; p-&gt;pop() &lt;&lt; endl;
    delete p;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c6221843-784a-4002-bbb3-9dd447715f95/image.png" /></p>
<h3 id="구체화-및-객체-활용">구체화 및 객체 활용</h3>
<pre><code class="language-cpp">MyStack&lt;int&gt;    iStack;  // int형 스택 생성
MyStack&lt;double&gt; dStack;  // double형 스택 생성

iStack.push(3);
int n = iStack.pop();

dStack.push(3.5);
double d = dStack.pop();</code></pre>
<p><code>&lt;타입&gt;</code> 을 명시하여 원하는 타입의 스택을 생성할 수 있었습니다. 포인터로 동적 할당하는 경우에도 <code>new MyStack&lt;char&gt;()</code> 형태로 사용합니다.</p>
<hr />
<h2 id="8-템플릿의-장단점">8. 템플릿의 장단점</h2>
<table>
<thead>
<tr>
<th>구분</th>
<th>내용</th>
</tr>
</thead>
<tbody><tr>
<td><strong>장점</strong></td>
<td>코드 재사용성 향상, 타입 안전성 보장, 높은 생산성</td>
</tr>
<tr>
<td><strong>단점</strong></td>
<td>컴파일러 간 호환성 문제 가능성(포팅 취약), 컴파일 오류 메시지가 직관적이지 않아 디버깅이 어려울 수 있음</td>
</tr>
</tbody></table>
<hr />
<h2 id="정리">정리</h2>
<table>
<thead>
<tr>
<th>개념</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><code>template &lt;class T&gt;</code></td>
<td>제네릭 타입 T를 사용하는 템플릿 선언</td>
</tr>
<tr>
<td>제네릭 함수</td>
<td>T 타입을 매개변수로 받는 일반화된 함수</td>
</tr>
<tr>
<td>제네릭 클래스</td>
<td>T 타입을 멤버/메서드에 사용하는 일반화된 클래스</td>
</tr>
<tr>
<td>구체화</td>
<td>컴파일러가 T에 실제 타입을 대입하여 코드를 생성하는 과정</td>
</tr>
<tr>
<td>STL</td>
<td>C++ 표준 템플릿 라이브러리, 제네릭 프로그래밍의 집합체</td>
</tr>
</tbody></table>
<p>템플릿은 C++에서 <strong>STL(Standard Template Library)</strong> 의 근간이 되는 개념으로, <code>vector</code>, <code>stack</code>, <code>map</code> 등 표준 컨테이너들이 모두 템플릿으로 구현되어 있습니다. 이번 내용을 잘 이해해두면 STL 사용 시 내부 동작 방식을 이해하는 데 큰 도움이 될 것 같습니다.</p>