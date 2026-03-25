<p>함수 overloading, 디폴트 매개변수에 대한 진도를 복습 겸 정리해보겠습니다.</p>
<h2 id="1-함수-중복이란">1. 함수 중복이란?</h2>
<p><strong>동일한 이름의 함수를 여러 개 선언하는 것</strong>입니다. C에서는 불가능하지만, C++에서는 다형성(polymorphism)의 일환으로 허용됩니다.</p>
<p>함수 중복이 가능한 범위는 다음과 같습니다.</p>
<ul>
<li>보통 함수들 사이</li>
<li>클래스의 멤버 함수들 사이</li>
<li>상속 관계의 기본 클래스와 파생 클래스 멤버 함수들 사이</li>
</ul>
<hr />
<h2 id="2-함수-중복-조건">2. 함수 중복 조건</h2>
<p>함수 중복이 성립하려면 아래 조건을 만족해야 합니다.</p>
<ul>
<li>함수 이름이 동일해야 합니다.</li>
<li>매개변수의 <strong>타입</strong>이 다르거나 <strong>개수</strong>가 달라야 합니다.</li>
<li><strong>리턴 타입은 무관</strong>합니다. (리턴 타입만 다른 경우는 중복 실패)</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f62b8467-8cd2-460e-af65-d18e5ec41c0d/image.png" /></p>
<pre><code class="language-cpp">// 중복 성공 사례 — 매개변수 타입/개수가 다름
int sum(int a, int b, int c) { return a + b + c; }
double sum(double a, double b) { return a + b; }
int sum(int a, int b) { return a + b; }

int main() {
    cout &lt;&lt; sum(2, 5, 33);   // int sum(int, int, int)
    cout &lt;&lt; sum(12.5, 33.6); // double sum(double, double)
    cout &lt;&lt; sum(2, 6);       // int sum(int, int)
}</code></pre>
<pre><code class="language-cpp">// 중복 실패 사례 — 리턴 타입만 다름
int sum(int a, int b) { return a + b; }
double sum(int a, int b) { return (double)(a + b); } // 컴파일 오류</code></pre>
<p>리턴 타입만 다른 경우 컴파일러가 어떤 함수를 호출해야 할지 구분할 수 없어서 오류가 발생합니다.</p>
<hr />
<h2 id="3-함수-중복의-편리함">3. 함수 중복의 편리함</h2>
<p>같은 기능을 하는 함수에 이름을 하나로 통일할 수 있어서, 함수 이름을 따로 외울 필요가 없고 호출 실수를 줄일 수 있습니다.</p>
<pre><code class="language-cpp">// 중복 전
void msg1(){
    cout &lt;&lt; &quot;Hello&quot;;
}
void msg2(){
    cout &lt;&lt; &quot;Hello, &quot; &lt;&lt; name;
}
void msg3(){
    cout &lt;&lt; &quot;Hello, &quot; &lt;&lt; id &lt;&lt; name;
}

// 중복 후
void msg(){
    cout &lt;&lt; &quot;Hello&quot;;
}
void msg(string name){
    cout &lt;&lt; &quot;Hello, &quot; &lt;&lt; name;
}
void msg(int id, string name){
    cout &lt;&lt; &quot;Hello, &quot; &lt;&lt; id &lt;&lt; name;
}</code></pre>
<hr />
<h2 id="4-생성자-함수-중복">4. 생성자 함수 중복</h2>
<p>생성자도 함수이므로 중복이 가능합니다. 객체 생성 시 다양한 형태로 초깃값을 전달하기 위해 사용합니다.</p>
<pre><code class="language-cpp">class Circle {
public:
    Circle() { radius = 1; }         // 매개변수 없음
    Circle(int r) { radius = r; }    // int 매개변수
};

int main() {
    Circle donut;      // Circle() 호출
    Circle pizza(30);  // Circle(int r) 호출
}</code></pre>
<p>소멸자는 매개변수를 가질 수 없기 때문에 중복이 불가능하고, 클래스 안에 오직 하나만 존재할 수 있습니다.</p>
<hr />
<h2 id="5-디폴트-매개변수-default-parameter">5. 디폴트 매개변수 (Default Parameter)</h2>
<p>함수 호출 시 매개변수에 값을 넘기지 않을 경우 자동으로 사용되는 기본값입니다.</p>
<pre><code class="language-cpp">void star(int a = 5) {
    for (int i = 0; i &lt; a; i++) cout &lt;&lt; '*';
    cout &lt;&lt; endl;
}

int main() {
    star();    // a = 5 (디폴트값 사용) → *****
    star(10);  // a = 10 → **********
}</code></pre>
<h3 id="디폴트-매개변수-선언-규칙">디폴트 매개변수 선언 규칙</h3>
<p>디폴트 매개변수는 반드시 <strong>오른쪽(끝 쪽)부터 몰아서</strong> 선언해야 합니다. 중간에 디폴트가 아닌 매개변수가 오면 컴파일 오류가 발생합니다.</p>
<pre><code class="language-cpp">void f(int a, int b = 10, int c = 20); // OK
void f(int a = 1, int b, int c = 20);  // 오류 — 중간에 일반 매개변수가 있음
void f(int a = 1, int b = 2, int c);   // 오류</code></pre>
<p>함수 선언(프로토타입)에 디폴트 값을 명시하면, 함수 정의에서는 다시 쓰지 않아도 됩니다.</p>
<pre><code class="language-cpp">void msg(int id, string text = &quot;&quot;); // 선언부에서만 디폴트값 지정

void msg(int id, string text) {     // 정의부에는 디폴트값 없이 작성
    cout &lt;&lt; id &lt;&lt; ' ' &lt;&lt; text &lt;&lt; endl;
}</code></pre>
<hr />
<h2 id="6-디폴트-매개변수로-함수-중복-간소화">6. 디폴트 매개변수로 함수 중복 간소화</h2>
<p>디폴트 매개변수를 활용하면 여러 개의 중복 함수를 하나로 합칠 수 있습니다.</p>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;
/*
// 중복 함수 2개
void fillLine() {
    for (int i = 0; i &lt; 25; i++) cout &lt;&lt; '*';
    cout &lt;&lt; endl;
}
void fillLine(int n, char c) {
    for (int i = 0; i &lt; n; i++) cout &lt;&lt; c;
    cout &lt;&lt; endl;
}
*/

// 디폴트 매개변수로 하나로 합침
void fillLine(int n = 25, char c = '*') {
    for (int i = 0; i &lt; n; i++) cout &lt;&lt; c;
    cout &lt;&lt; endl;
}

int main() {
    fillLine();
    fillLine(10, '%');
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/66a6bc8c-ebc0-497e-86ee-0bb839cabf97/image.png" /></p>
<p>단, <strong>중복 함수와 디폴트 매개변수를 가진 함수를 함께 사용하면 모호성이 발생</strong>할 수 있으므로 주의가 필요합니다.</p>
<hr />
<h2 id="7-함수-중복의-모호성">7. 함수 중복의 모호성</h2>
<p>컴파일러가 어떤 함수를 호출해야 할지 판단하지 못하는 경우입니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/348e51e2-17b3-4597-9a38-ee48775b4d7c/image.png" /></p>
<h3 id="형-변환으로-인한-모호성">형 변환으로 인한 모호성</h3>
<pre><code class="language-cpp">float square(float a) { return a * a; }
double square(double a) { return a * a; }

square(3.0); // 3.0은 double인데 float으로도 변환 가능 → 모호
square(3);   // int를 float으로도, double로도 변환 가능 → 모호</code></pre>
<h3 id="참조-매개변수로-인한-모호성">참조 매개변수로 인한 모호성</h3>
<pre><code class="language-cpp">int add(int a, int b) { return a + b; }
int add(int a, int&amp; b) { b = b + a; return b; }

int s = 10, t = 20;
add(s, t); // int b 인지 int&amp; b 인지 구분 불가 → 모호</code></pre>
<h3 id="디폴트-매개변수로-인한-모호성">디폴트 매개변수로 인한 모호성</h3>
<pre><code class="language-cpp">void msg(int id) { cout &lt;&lt; id; }
void msg(int id, string s = &quot;&quot;) { cout &lt;&lt; id &lt;&lt; s; }

msg(6); // 두 함수 모두 호출 가능 → 모호</code></pre>
<hr />
<h2 id="정리">정리</h2>
<table>
<thead>
<tr>
<th>개념</th>
<th>핵심 내용</th>
</tr>
</thead>
<tbody><tr>
<td><strong>함수 중복 조건</strong></td>
<td>이름 동일 + 매개변수 타입/개수 다름 (리턴 타입은 무관)</td>
</tr>
<tr>
<td><strong>생성자 중복</strong></td>
<td>가능. 다양한 초기화 방식 제공</td>
</tr>
<tr>
<td><strong>소멸자 중복</strong></td>
<td>불가능. 클래스에 하나만 존재</td>
</tr>
<tr>
<td><strong>디폴트 매개변수</strong></td>
<td>오른쪽부터 몰아서 선언, 선언부에만 디폴트값 명시</td>
</tr>
<tr>
<td><strong>모호성</strong></td>
<td>형 변환 / 참조 매개변수 / 디폴트 매개변수 조합 시 발생 가능</td>
</tr>
</tbody></table>