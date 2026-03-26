<h2 id="static-멤버란">static 멤버란?</h2>
<p>C++에서 <code>static</code>을 붙인 멤버 변수 / 멤버 함수를 <strong>static 멤버</strong>라고 합니다.</p>
<p>static 멤버의 핵심 특징은 <strong>객체 생성 여부와 무관하게 프로그램 시작 시 메모리에 올라간다</strong>는 점입니다.</p>
<hr />
<h2 id="non-static-멤버와의-비교">non-static 멤버와의 비교</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/92da3ed7-a1eb-4b25-b351-f3c90ddced7f/image.png" /></p>
<table>
<thead>
<tr>
<th>구분</th>
<th>static 멤버</th>
<th>non-static 멤버</th>
</tr>
</thead>
<tbody><tr>
<td>생성 시점</td>
<td>프로그램 시작 시</td>
<td>객체 생성 시</td>
</tr>
<tr>
<td>소멸 시점</td>
<td>프로그램 종료 시</td>
<td>객체 소멸 시</td>
</tr>
<tr>
<td>메모리 위치</td>
<td>data 영역</td>
<td>객체 내부 (스택 or 힙)</td>
</tr>
<tr>
<td>공유 여부</td>
<td>모든 객체가 공유</td>
<td>객체마다 별도 존재</td>
</tr>
<tr>
<td>접근 방식</td>
<td><code>클래스명::멤버</code></td>
<td>객체를 통해 접근</td>
</tr>
</tbody></table>
<hr />
<h2 id="static-멤버-변수-선언과-정의">static 멤버 변수 선언과 정의</h2>
<pre><code class="language-cpp">class Person {
public:
    int money;              // non-static 멤버 변수
    static int sharedMoney; // static 멤버 변수 (선언만)
};

// 클래스 외부에서 반드시 정의해야 함 (메모리 할당)
int Person::sharedMoney = 10;</code></pre>
<p>static 멤버 변수는 클래스 내부에 적는 건 <strong>선언</strong>에 불과합니다. 실제 메모리는 <strong>클래스 외부에서 정의</strong>할 때 할당됩니다.</p>
<p>객체가 0개든 100개든 <code>sharedMoney</code>는 data 영역에 딱 하나만 존재합니다.</p>
<hr />
<h2 id="static-멤버-접근-방법">static 멤버 접근 방법</h2>
<h3 id="1-클래스-이름--범위-지정-연산자--기본-방법">1. 클래스 이름 + 범위 지정 연산자 (<code>::</code>), 기본 방법</h3>
<pre><code class="language-cpp">Person::sharedMoney = 200;
Person::addShared(100);</code></pre>
<h3 id="2-객체-이름이나-포인터로도-접근-가능">2. 객체 이름이나 포인터로도 접근 가능</h3>
<pre><code class="language-cpp">Person han;
han.sharedMoney = 200;  // 가능하지만 권장하지 않음

Person* p = &amp;han;
p-&gt;addShared(200);</code></pre>
<p>단, 객체 이름으로 접근하면 마치 그 객체의 멤버인 것처럼 보여서 혼란을 줄 수 있기 때문에, <code>클래스명::</code> 방식을 사용하는 것이 좋습니다.</p>
<h3 id="non-static-멤버는-클래스-이름으로-접근-불가">non-static 멤버는 클래스 이름으로 접근 불가</h3>
<pre><code class="language-cpp">Person::money = 100;      // 컴파일 오류
Person::addMoney(200);    // 컴파일 오류</code></pre>
<p>non-static 멤버는 객체마다 따로 존재하기 때문에 &quot;어떤 객체의 멤버인지&quot;를 특정해야 합니다.</p>
<hr />
<h2 id="static-멤버-함수의-제약">static 멤버 함수의 제약</h2>
<p>static 멤버 함수 안에서 접근 가능한 것은 다음과 같습니다.</p>
<ul>
<li>static 멤버 변수</li>
<li>static 멤버 함수</li>
<li>함수 내 지역 변수</li>
</ul>
<p><strong>non-static 멤버에는 접근할 수 없습니다.</strong></p>
<pre><code class="language-cpp">class PersonError {
    int money;  // non-static
public:
    static int getMoney() { return money; }  // 컴파일 오류!
};</code></pre>
<p>이유는 간단합니다. static 멤버 함수는 객체 없이도 호출될 수 있는데, <code>money</code>는 객체마다 따로 존재하는 변수이기 때문에 <strong>&quot;어떤 객체의 money를 리턴해야 하는지 알 수 없습니다.&quot;</strong></p>
<p>non-static 함수에는 <code>this</code> 포인터가 암묵적으로 전달되어 <code>this-&gt;money</code>로 접근할 수 있지만, static 함수에는 <code>this</code>가 없습니다.</p>
<pre><code class="language-cpp">// non-static 함수 → this가 있어서 OK
int getMoney() { return this-&gt;money; }

// static 함수 → this가 없어서 오류
static int getMoney() { return money; }</code></pre>
<p>반대로 <strong>non-static 멤버 함수는 static 멤버에 자유롭게 접근 가능</strong>합니다.</p>
<pre><code class="language-cpp">class Person {
public:
    double money;
    static int sharedMoney;

    int total() {
        return money + sharedMoney;  // 정상
    }
};</code></pre>
<hr />
<h2 id="static-활용-예시">static 활용 예시</h2>
<h3 id="1-전역-함수를-클래스로-캡슐화">1. 전역 함수를 클래스로 캡슐화</h3>
<p>전역 함수는 이름 충돌(name collision) 위험이 있습니다. static 멤버 함수를 활용하면 <strong>클래스가 네임스페이스 역할</strong>을 해서 이를 방지할 수 있습니다.</p>
<pre><code class="language-cpp">// 나쁜 예 - 전역 함수
int abs(int a) { return a &gt; 0 ? a : -a; }

// 좋은 예 - static 멤버 함수
class Math {
public:
    static int abs(int a) { return a &gt; 0 ? a : -a; }
    static int max(int a, int b) { return (a &gt; b) ? a : b; }
    static int min(int a, int b) { return (a &gt; b) ? b : a; }
};

int main() {
    cout &lt;&lt; Math::abs(-5) &lt;&lt; endl;   // 5
    cout &lt;&lt; Math::max(10, 8) &lt;&lt; endl; // 10
    cout &lt;&lt; Math::min(-3, -8) &lt;&lt; endl; // -8
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ac5b724a-ee2e-45b1-88bd-28d2cbcb75a8/image.png" /></p>
<blockquote>
<p>메모리 위치는 둘 다 data 영역으로 동일합니다. 차이는 <strong>컴파일러/링커가 보는 심볼 스코프</strong>입니다. 전역 함수는 전역 심볼로 등록되어 이름 충돌 위험이 있지만, static 멤버 함수는 <code>Math::abs</code>로 등록되어 전역 공간에 <code>abs</code>라는 이름이 노출되지 않습니다.</p>
</blockquote>
<h3 id="2-객체-간-공유-변수">2. 객체 간 공유 변수</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;

class Circle {
private:
    static int numOfCircles;
    int radius;
public:
    Circle(int r = 1);
    ~Circle() { numOfCircles--;     cout &lt;&lt; &quot;~Circle 소멸자 호출 : &quot; &lt;&lt; numOfCircles &lt;&lt; endl;
    }
    double getArea() { return 3.14 * radius * radius; }
    static int getNumOfCircles() {
        return numOfCircles;
    }
};
Circle::Circle(int r) {
    radius = r;
    numOfCircles++;
    cout &lt;&lt; &quot;Circle(int r) 호출 : &quot; &lt;&lt; numOfCircles &lt;&lt; endl;
}
int Circle::numOfCircles = 0;

int main() {
    //Circle::numOfCircles = 10;
    Circle* p = new Circle[10]; // numOfCircles = 10
    cout &lt;&lt; &quot;생존하고 있는 원의 개수 = &quot; &lt;&lt; Circle::getNumOfCircles() &lt;&lt; endl;

    delete[] p; // numOfCircles = 0
    cout &lt;&lt; &quot;생존하고 있는 원의 개수 = &quot; &lt;&lt; Circle::getNumOfCircles() &lt;&lt; endl;

    Circle a; // numOfCircles = 1
    cout &lt;&lt; &quot;생존하고 있는 원의 개수 = &quot; &lt;&lt; Circle::getNumOfCircles() &lt;&lt; endl;

    Circle b; // numOfCircles = 2
    cout &lt;&lt; &quot;생존하고 있는 원의 개수 = &quot; &lt;&lt; Circle::getNumOfCircles() &lt;&lt; endl;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5d0ebb45-19f2-4975-a3cf-05e5e3e642c4/image.png" /></p>
<p>생성자에서 <code>++</code>, 소멸자에서 <code>--</code> 하면 현재 살아있는 객체 수를 추적할 수 있습니다. <code>numOfCircles</code>가 static이라 모든 객체가 공유하기 때문에 가능합니다.</p>
<hr />
<h2 id="정리">정리</h2>
<ul>
<li>static 멤버는 <strong>클래스 당 하나</strong>, 모든 객체가 <strong>공유</strong></li>
<li>메모리는 프로그램 시작 시 <strong>data 영역</strong>에 할당, 프로그램 종료 시 해제</li>
<li>static 멤버 변수는 클래스 외부에서 <strong>반드시 정의</strong>해야 함</li>
<li>static 멤버 함수는 <code>this</code>가 없으므로 <strong>non-static 멤버에 접근 불가</strong></li>
<li><code>클래스명::멤버</code> 형식으로 접근하는 것이 의도를 명확히 드러냄</li>
</ul>