<p>오늘 진도나갔던 상속 개념 및 목적, 접근 지정자(private/protected/public), this 포인터, 생성자 호출 순서, 업캐스팅/다운캐스팅, 다중 상속까지 오늘 나간 내용에 대해 전부 정리해보겠습니다.</p>
<h2 id="1-상속이란">1. 상속이란?</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/80d94db0-051a-4556-850c-d2b4ea364f8c/image.png" /></p>
<p>상속이란 기본 클래스(부모 클래스)의 속성과 기능을 파생 클래스(자식 클래스)에 물려주는 것입니다.</p>
<ul>
<li><strong>기본 클래스(base class)</strong> : 상속해주는 클래스 (부모 클래스)</li>
<li><strong>파생 클래스(derived class)</strong> : 상속받는 클래스 (자식 클래스)</li>
</ul>
<p>기본 클래스에서 파생 클래스로 갈수록 클래스의 개념이 구체화됩니다.</p>
<blockquote>
<p>주의할 점은 상속 관계는 <strong>클래스 사이</strong>에서만 정의되며, 객체 사이에는 상속 관계가 없다는 것입니다.</p>
</blockquote>
<hr />
<h2 id="2-상속의-목적-및-장점">2. 상속의 목적 및 장점</h2>
<ol>
<li><strong>간결한 클래스 작성</strong> : 기본 클래스의 기능을 물려받아 파생 클래스를 간결하게 작성할 수 있습니다.</li>
<li><strong>계층적 분류 및 관리 용이</strong> : 클래스들의 구조적 관계를 파악하기 쉽습니다.</li>
<li><strong>소프트웨어 생산성 향상</strong> : 기존에 작성한 클래스를 재사용하고, 상속받아 새로운 기능을 확장할 수 있습니다.</li>
</ol>
<hr />
<h2 id="3-상속-선언">3. 상속 선언</h2>
<pre><code class="language-cpp">class Student : public Person {
    // Person을 상속받는 Student 선언
};

class StudentWorker : public Student {
    // Student를 상속받는 StudentWorker 선언
    // Student가 물려받은 Person의 멤버도 함께 물려받습니다.
};</code></pre>
<ul>
<li>Student 클래스는 Person 클래스의 멤버를 물려받는다.</li>
<li>StudentWorker 클래스는 Student의 멤버를 물려받는다.
Student가 불려받은 Person의 멤버도 함께 물려 받는다.</li>
</ul>
<hr />
<h2 id="4-파생-클래스의-객체-구성">4. 파생 클래스의 객체 구성</h2>
<p>파생 클래스의 객체는 기본 클래스의 멤버를 포함합니다.</p>
<pre><code class="language-c">// ColorPoint 객체 메모리
┌─────────────────┐
│  int x          │  ← Point(기본 클래스) 영역
│  int y          │
│  set()          │
│  showPoint()    │
├─────────────────┤
│  string color   │  ← ColorPoint(파생 클래스) 영역
│  setColor()     │
│  showColorPoint │
└─────────────────┘
</code></pre>
<hr />
<h2 id="5-접근-지정자-private--protected--public">5. 접근 지정자 (private / protected / public)</h2>
<table>
<thead>
<tr>
<th>접근 지정자</th>
<th>자기 자신</th>
<th>파생 클래스</th>
<th>외부(main 등)</th>
</tr>
</thead>
<tbody><tr>
<td><code>private</code></td>
<td>✅</td>
<td>❌</td>
<td>❌</td>
</tr>
<tr>
<td><code>protected</code></td>
<td>✅</td>
<td>✅</td>
<td>❌</td>
</tr>
<tr>
<td><code>public</code></td>
<td>✅</td>
<td>✅</td>
<td>✅</td>
</tr>
</tbody></table>
<ul>
<li><code>private</code> : 해당 클래스 내부에서만 접근 가능합니다. 파생 클래스에서도 접근할 수 없습니다.</li>
<li><code>protected</code> : 해당 클래스 내부와 파생 클래스에서만 접근 가능합니다. 외부(main 등)에서는 접근할 수 없습니다.</li>
<li><code>public</code> : 어디서든 접근 가능합니다.</li>
</ul>
<h3 id="외부에서-접근하려면-settergetter를-사용합니다">외부에서 접근하려면 setter/getter를 사용합니다.</h3>
<pre><code class="language-cpp">class Point {
private:
    int x, y;
public:
    void set(int x, int y) { this-&gt;x = x; this-&gt;y = y; } // setter
    int getX() { return x; }  // getter
    int getY() { return y; }  // getter
};

int main() {
    Point p;
    p.set(3, 4);       // ✅ setter로 간접 접근
    cout &lt;&lt; p.getX();  // ✅ getter로 간접 접근
    // p.x = 5;        // ❌ private이라 직접 접근 불가
}</code></pre>
<h3 id="protected-멤버에-대한-접근">protected 멤버에 대한 접근</h3>
<pre><code class="language-c">#include &lt;iostream&gt;
#include &lt;string&gt;
using namespace std;

class Point {
protected:
    int x, y;
public:
    void set(int x, int y) {
        this-&gt;x = x;
        this-&gt;y = y;
    }
    void showPoint() {
        cout &lt;&lt; &quot;(&quot; &lt;&lt; x &lt;&lt; &quot;,&quot; &lt;&lt; y &lt;&lt; &quot;)&quot; &lt;&lt; endl;
    }
};

class ColorPoint : public Point { // x, y접근 가능
    string color;
public:
    void setColor(string color) {
        this-&gt;color = color;
    }
    void showColorPoint() {
        cout &lt;&lt; color &lt;&lt; &quot;:&quot;;
        showPoint();    // Point 클래스의 showPoint() 호출
    }
    bool equals(ColorPoint p) {
        if (x == p.x &amp;&amp; y == p.y &amp;&amp; color == p.color) return true;
        else return false;
    }
};

void ColorPoint::setColor(string color) {
    this-&gt;color = color;
}


int main() {
    Point p;
    p.set(2, 3);
    p.x = 5;
    p.y = 5;
    p.showPoint();

    ColorPoint cp;
    cp.x = 10;
    cp.y = 10;
    cp.set(3, 4);
    cp.setColor(&quot;Red&quot;);
    cp.showColorPoint();

    ColorPoint cp2;
    cp2.set(3, 4);
    cp2.setColor(&quot;Red&quot;);
    cout &lt;&lt; ((cp.equals(cp2)) ? &quot;true&quot; : &quot;false&quot;);
}</code></pre>
<p> <img alt="" src="https://velog.velcdn.com/images/mommers/post/9ecbee35-a51e-4296-9e54-b667badef16e/image.png" /></p>
<pre><code class="language-c">// main에서 직접 접근 제거
p.set(2, 3);    // ✅ setter로 접근
// p.x = 5;    // ❌ 제거
// p.y = 5;    // ❌ 제거

cp.set(3, 4);   // ✅ setter로 접근
// cp.x = 10;  // ❌ 제거
// cp.y = 10;  // ❌ 제거

// equals 오타 수정
if (x == p.x &amp;&amp; y == p.y &amp;&amp; color == p.color) // ✅ == 로 수정</code></pre>
<h3 id="만약-protected---private로-바꾸면">만약 protected -&gt; private로 바꾸면?</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/37d25d99-42f9-49ca-a131-36173d2812cc/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cb4fe284-66ae-480f-977a-d7d36693aabf/image.png" /></p>
<p>에러가 더 많이 뜨게되며, ColorPoint 멤버 함수에서도 부모 클래스의 x, y에 접근할 수 없다.</p>
<hr />
<h2 id="6-this-포인터">6. this 포인터</h2>
<p><code>this</code>는 <strong>자기 자신 객체의 주소를 가리키는 포인터</strong>입니다.</p>
<pre><code class="language-cpp">this    // 자기 자신의 주소 (포인터)  → Point*
*this   // 자기 자신 객체 자체        → Point</code></pre>
<p><code>this-&gt;</code>는 매개변수 이름이 멤버변수 이름과 같을 때 구분을 위해 사용합니다.</p>
<pre><code class="language-cpp">void set(int x, int y) {
    this-&gt;x = x;  // 매개변수 x와 멤버 x가 이름이 같아서 this-&gt; 필수
    this-&gt;y = y;
}

bool equals(ColorPoint p) {
    if (x == p.x ...)  // 매개변수 이름이 p라 x와 안 겹침 → this-&gt; 생략 가능
}</code></pre>
<h3 id="return-this-메서드-체이닝">return *this (메서드 체이닝)</h3>
<pre><code class="language-cpp">Point&amp; setX(int x) {
    this-&gt;x = x;
    return *this;  // 자기 자신 객체를 반환
}

// 체이닝 사용 예시
p.setX(3).setY(4);</code></pre>
<hr />
<h2 id="7-생성자-호출-순서">7. 생성자 호출 순서</h2>
<p>파생 클래스 객체가 생성될 때 <strong>기본 클래스 생성자가 먼저</strong> 호출되고, 그 다음 파생 클래스 생성자가 호출됩니다.</p>
<pre><code>생성자 호출 순서 : A → B → C
소멸자 호출 순서 : C → B → A  (반대 순서)</code></pre><pre><code class="language-cpp">class A {};
class B : public A {};
class C : public B {};

// 생성자 A → 생성자 B → 생성자 C
// 소멸자 C → 소멸자 B → 소멸자 A</code></pre>
<h3 id="기본-생성자-자동-호출">기본 생성자 자동 호출</h3>
<p>명시적으로 지정하지 않으면 컴파일러가 <strong>기본 클래스의 기본 생성자(인자 없는 것)</strong> 를 자동으로 호출합니다.</p>
<pre><code class="language-cpp">class B : public A {
public:
    B() { ... }
    // 컴파일러가 자동으로 아래처럼 변환
    // B() : A() { ... }
};</code></pre>
<h3 id="매개변수-생성자를-호출하고-싶다면-직접-명시해야-합니다">매개변수 생성자를 호출하고 싶다면 직접 명시해야 합니다.</h3>
<pre><code class="language-cpp">class B : public A {
public:
    B() : A(10) { ... }  // A(int x) 명시적 호출
};</code></pre>
<h3 id="기본-클래스에-기본-생성자가-없는-경우">기본 클래스에 기본 생성자가 없는 경우</h3>
<pre><code class="language-cpp">class A {
public:
    A(int x) { ... }  // 기본 생성자 없음
};

class B : public A {
public:
    B() { ... }  // ❌ A() 를 찾는데 없음 → 컴파일 오류
    B() : A(0) { ... }  // ✅ 직접 명시해야 함
};</code></pre>
<p>컴파일러는 인자가 필요한 생성자에 어떤 값을 넣어야 할지 알 수 없기 때문에 자동 호출을 하지 않습니다. 반드시 개발자가 직접 명시해줘야 합니다.</p>
<hr />
<h2 id="8-업캐스팅up-casting">8. 업캐스팅(Up-casting)</h2>
<p><strong>파생 클래스 포인터가 기본 클래스 포인터에 치환되는 것</strong>으로, 자동 형변환이 됩니다.</p>
<pre><code class="language-cpp">cp 객체 메모리
┌─────────────────┐
│  int x          │  ← Point 영역
│  int y          │
│  set()          │
│  showPoint()    │
├─────────────────┤
│  string color   │  ← ColorPoint 영역
│  setColor()     │
│  showColorPoint │
└─────────────────┘

ColorPoint cp;
ColorPoint* pDer  = &amp;cp;   // ColorPoint 포인터 → 전체 접근 가능
Point*      pBase = pDer;  // 업캐스팅 (자동) → Point 영역만 접근 가능</code></pre>
<ul>
<li>같은 주소를 가리키지만, <strong>포인터 타입에 따라 해석 범위가 달라집니다.</strong></li>
<li><code>Point*</code> 타입은 Point 멤버만 접근 가능하고, ColorPoint 멤버는 접근할 수 없습니다.</li>
</ul>
<pre><code class="language-cpp">pDer  →  ┌─────────────────┐
         │  int x          │  ✅
         │  int y          │  ✅
         │  set()          │  ✅
         │  showPoint()    │  ✅
         ├─────────────────┤
         │  string color   │  ✅
         │  setColor()     │  ✅
         │  showColorPoint │  ✅
         └─────────────────┘

pBase →  ┌─────────────────┐
         │  int x          │  ✅
         │  int y          │  ✅
         │  set()          │  ✅
         │  showPoint()    │  ✅
         ├─────────────────┤
         │  string color   │  ❌ 접근 불가
         │  setColor()     │  ❌ 접근 불가
         │  showColorPoint │  ❌ 접근 불가
         └─────────────────┘

pBase-&gt;showPoint();      // ✅ Point 멤버라 접근 가능
pBase-&gt;showColorPoint(); // ❌ Point에 없는 멤버라 컴파일 오류</code></pre>
<h3 id="업캐스팅을-쓰는-이유">업캐스팅을 쓰는 이유</h3>
<p>다양한 파생 클래스를 기본 클래스 포인터 하나로 묶어서 일괄 처리할 수 있습니다. 이것이 다형성(polymorphism)의 기반이 됩니다.</p>
<pre><code class="language-cpp">Point* arr[4];
arr[0] = &amp;cp1;  // 업캐스팅
arr[1] = &amp;cp2;  // 업캐스팅
arr[2] = &amp;p1;
arr[3] = &amp;p2;

for (int i = 0; i &lt; 4; i++) {
    arr[i]-&gt;showPoint();  // 일괄 처리
}</code></pre>
<hr />
<h2 id="9-다운캐스팅down-casting">9. 다운캐스팅(Down-casting)</h2>
<p><strong>기본 클래스 포인터가 파생 클래스 포인터에 치환되는 것</strong>으로, 강제 형변환이 필요합니다.</p>
<pre><code class="language-cpp">Point*      pBase = &amp;cp;              // 업캐스팅
ColorPoint* pDer  = (ColorPoint*)pBase; // 다운캐스팅 (강제 변환 필수)</code></pre>
<ul>
<li>업캐스팅은 &quot;작게 보는 것&quot; → 안전 → 자동 변환</li>
<li>다운캐스팅은 &quot;크게 보는 것&quot; → 위험할 수 있음 → 개발자가 직접 명시</li>
</ul>
<pre><code>업캐스팅   → ColorPoint 전체 → Point 부분만
다운캐스팅 → Point 부분만   → ColorPoint 전체로 복원</code></pre><h3 id="다운캐스팅이-위험한-경우">다운캐스팅이 위험한 경우</h3>
<pre><code class="language-cpp">Point p;                               // 순수 Point 객체
Point* pBase = &amp;p;
ColorPoint* pDer = (ColorPoint*)pBase; // 컴파일은 되지만
pDer-&gt;setColor(&quot;Red&quot;);                 // ❌ 런타임 오류 (ColorPoint 영역 없음)</code></pre>
<p>다운캐스팅은 <strong>원래 객체가 ColorPoint였을 때만 안전</strong>합니다.</p>
<hr />
<h2 id="10-다중-상속">10. 다중 상속</h2>
<p>여러 기본 클래스를 동시에 상속받는 것입니다.</p>
<pre><code class="language-cpp">class MusicPhone : public MP3, public MobilePhone {
public:
    void dial() {
        play();      // MP3 멤버
        sendCall();  // MobilePhone 멤버
    }
};</code></pre>
<h3 id="다중-상속의-문제점">다중 상속의 문제점</h3>
<p>한 클래스 A를 상속받은 여러 클래스(B, C)를 다시 한 클래스 Z가 다중 상속받을 때, 기본 클래스 A의 멤버가 중복 생성되는 문제가 발생합니다.</p>
<ul>
<li>해결책 : <strong>가상 상속(virtual inheritance)</strong></li>
<li>참고로 자바에서는 다중 상속 대신 <strong>인터페이스</strong>를 제공합니다.</li>
</ul>