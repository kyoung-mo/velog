<p>오늘 진도 나갔던 부분인 가상 함수 개념, 오버라이딩, 정적/동적 바인딩 비교, 범위 지정 연산자, 가상 소멸자, 오버로딩/재정의/오버라이딩 비교표, 순수 가상 함수, 추상 클래스에 대해 정리해보겠습니다.</p>
<h2 id="1-가상-함수virtual-function">1. 가상 함수(Virtual Function)</h2>
<p><code>virtual</code> 키워드로 선언된 멤버 함수입니다.</p>
<pre><code class="language-cpp">class Base {
public:
    virtual void f();
};</code></pre>
<h3 id="virtual-키워드의-의미">virtual 키워드의 의미</h3>
<p><code>virtual</code> = <strong>&quot;컴파일러야, 지금 말고 실행할 때 결정해&quot;</strong> 라는 동적 바인딩 지시어입니다.</p>
<ul>
<li>컴파일 시점에 호출할 함수를 결정하지 않습니다.</li>
<li>런타임(실행 시간)에 실제 객체 타입을 보고 호출할 함수를 결정합니다.</li>
</ul>
<hr />
<h2 id="2-함수-오버라이딩function-overriding">2. 함수 오버라이딩(Function Overriding)</h2>
<p>파생 클래스에서 기본 클래스의 <strong>가상 함수와 동일한 이름, 매개변수, 리턴 타입</strong>으로 함수를 재작성하는 것입니다.</p>
<ul>
<li>기본 클래스의 가상 함수의 존재감을 상실시킵니다.</li>
<li>파생 클래스에서 오버라이딩한 함수가 호출되도록 동적 바인딩이 발생합니다.</li>
<li>다형성의 한 종류입니다.</li>
</ul>
<h3 id="오버라이딩-성공-조건">오버라이딩 성공 조건</h3>
<p>이름, 매개변수 타입과 개수, 리턴 타입이 <strong>모두 일치</strong>해야 합니다.</p>
<pre><code class="language-cpp">class Base {
public:
    virtual void f();         // ✅
    virtual void success();   // ✅
    virtual void g(int);      // ✅
};

class Derived : public Base {
public:
    virtual int f();          // ❌ 리턴 타입 다름 → 오버라이딩 실패
    virtual void success();   // ✅ 오버라이딩 성공
    virtual void g(int, double); // ❌ 매개변수 다름 → 오버라이딩 실패
};</code></pre>
<h3 id="virtual-생략-가능">virtual 생략 가능</h3>
<p>기본 클래스에서 <code>virtual</code>로 선언하면 파생 클래스에서 <code>virtual</code>을 생략해도 자동으로 가상 함수가 유지됩니다.</p>
<pre><code class="language-cpp">class Base {
public:
    virtual void f();
};

class Derived : public Base {
public:
    void f();  // virtual 생략해도 가상 함수로 동작
};</code></pre>
<h3 id="오버라이딩의-목적">오버라이딩의 목적</h3>
<p><strong>파생 클래스에서 구현할 함수 인터페이스 제공(파생 클래스의 다형성)</strong></p>
<hr />
<h2 id="3-정적-바인딩-vs-동적-바인딩">3. 정적 바인딩 vs 동적 바인딩</h2>
<p><strong>언제 호출할 함수를 결정하느냐</strong>의 차이입니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c5e10554-ec2c-47ed-b619-9eb30244637a/image.png" /></p>
<pre><code>정적 바인딩 → 컴파일 시점에 포인터 타입 보고 결정
동적 바인딩 → 실행 시점에 실제 객체 타입 보고 결정</code></pre><h3 id="virtual-없을-때-정적-바인딩">virtual 없을 때 (정적 바인딩)</h3>
<pre><code class="language-cpp">class Base {
public:
    void f() { cout &lt;&lt; &quot;Base::f()&quot; &lt;&lt; endl; }
};

class Derived : public Base {
public:
    void f() { cout &lt;&lt; &quot;Derived::f()&quot; &lt;&lt; endl; }
};

int main() {
    Derived d;
    Base* pBase = &amp;d;   // 업캐스팅
    pBase-&gt;f();         // Base::f() 호출 ← 포인터 타입 기준
}</code></pre>
<h3 id="virtual-있을-때-동적-바인딩">virtual 있을 때 (동적 바인딩)</h3>
<pre><code class="language-cpp">class Base {
public:
    virtual void f() { cout &lt;&lt; &quot;Base::f()&quot; &lt;&lt; endl; }
};

class Derived : public Base {
public:
    virtual void f() { cout &lt;&lt; &quot;Derived::f()&quot; &lt;&lt; endl; }
};

int main() {
    Derived d;
    Base* pBase = &amp;d;   // 업캐스팅
    pBase-&gt;f();         // Derived::f() 호출 ← 실제 객체 타입 기준
}</code></pre>
<h3 id="동적-바인딩이-필요한-이유">동적 바인딩이 필요한 이유</h3>
<pre><code class="language-cpp">Base* p;

if (조건) p = new Circle();
else      p = new Rect();

p-&gt;draw();  // 컴파일 시점엔 Circle인지 Rect인지 모름
            // 실행해봐야 알 수 있음 → 동적 바인딩 필요</code></pre>
<p>컴파일 시점에는 <code>p</code>가 어떤 객체를 가리킬지 모를 수 있기 때문에 실행 시간까지 미루는 것입니다.</p>
<hr />
<h2 id="4-오버라이딩의-목적---다형성-실현">4. 오버라이딩의 목적 - 다형성 실현</h2>
<p><code>Shape*</code> 포인터 하나로 여러 파생 클래스의 함수를 호출할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/330e6721-6a5c-4839-8c53-bd35915a6db2/image.png" /></p>
<pre><code class="language-cpp">class Shape {
protected:
    virtual void draw() {}
};

class Circle : public Shape {
protected:
    virtual void draw() { /* Circle을 그린다 */ }
};

class Rect : public Shape {
protected:
    virtual void draw() { /* Rect를 그린다 */ }
};

class Line : public Shape {
protected:
    virtual void draw() { /* Line을 그린다 */ }
};

void paint(Shape* p) {
    p-&gt;draw();  // 실제 객체 타입에 맞는 draw() 자동 호출
}

paint(new Circle());  // Circle::draw() 호출
paint(new Rect());    // Rect::draw() 호출
paint(new Line());    // Line::draw() 호출</code></pre>
<p><code>Circle</code>, <code>Rect</code>, <code>Line</code> Class의 <code>draw()</code> 함수에는 virtual을 생략할 수 있습니다.</p>
<p><code>virtual</code>은 클래스 멤버 함수에 붙이며, <code>p-&gt;draw();</code> 를 호출할 때 <code>draw()</code> 가 virtual이기 때문에 실제 객체 타입을 보고 정합니다.</p>
<p><code>paint(Shape* p)</code> 처럼 기본 클래스 포인터로 받으면 <strong>함수 하나로 모든 파생 클래스 처리</strong>가 가능합니다. <code>virtual</code> 덕분에 실제 객체 타입에 맞는 <code>draw()</code>가 호출됩니다.</p>
<blockquote>
<p>주의: <code>new</code>로 생성하면 반드시 <code>delete</code>로 메모리를 해제해야 합니다. 안 하면 메모리 누수가 발생합니다.</p>
</blockquote>
<hr />
<h2 id="5-오버라이딩과-범위-지정-연산자">5. 오버라이딩과 범위 지정 연산자(::)</h2>
<p><code>클래스명::함수명()</code> 형태로 기본 클래스의 가상 함수를 <strong>정적 바인딩</strong>으로 호출할 수 있습니다.</p>
<pre><code class="language-cpp">class Circle : public Shape {
public:
    virtual void draw() {
        Shape::draw();       // 기본 클래스 draw() 명시적 호출 (정적 바인딩)
        cout &lt;&lt; &quot;Circle&quot; &lt;&lt; endl;
    }
};

int main() {
    Circle circle;
    Shape* pShape = &amp;circle;

    pShape-&gt;draw();         // Circle::draw() 호출 → &quot;--Shape--Circle&quot;
    pShape-&gt;Shape::draw();  // Shape::draw() 직접 호출 → &quot;--Shape--&quot;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/19d6b245-2d86-425a-bf33-3571a6f35462/image.png" /></p>
<p><code>Shape::draw()</code> 처럼 클래스 이름을 명시하면 <code>virtual</code>이 있어도 동적 바인딩을 건너뛰고 해당 클래스의 함수를 바로 호출합니다.</p>
<hr />
<h2 id="6-가상-소멸자virtual-destructor">6. 가상 소멸자(Virtual Destructor)</h2>
<p>소멸자를 <code>virtual</code>로 선언하면 소멸자 호출 시 동적 바인딩이 발생합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2a601e42-2ca8-423c-b144-fcd3ad104e98/image.png" /></p>
<h3 id="virtual-소멸자가-없을-때">virtual 소멸자가 없을 때</h3>
<pre><code class="language-cpp">Base* p = new Derived();
delete p;
// p가 Base* 타입 → ~Base()만 호출
// ~Derived()는 호출 안됨 → 메모리 누수 발생</code></pre>
<h3 id="virtual-소멸자가-있을-때">virtual 소멸자가 있을 때</h3>
<pre><code class="language-cpp">class Base {
public:
    virtual ~Base() { cout &lt;&lt; &quot;~Base()&quot; &lt;&lt; endl; }
};

class Derived : public Base {
public:
    virtual ~Derived() { cout &lt;&lt; &quot;~Derived()&quot; &lt;&lt; endl; }
};

Base* p = new Derived();
delete p;
// ~Derived() 먼저 실행 → ~Base() 실행
// 완전히 정리됨</code></pre>
<p>소멸자 호출 순서는 생성자와 반대입니다.</p>
<pre><code>생성자 : Base → Derived  (부모 먼저)
소멸자 : Derived → Base  (자식 먼저)</code></pre><h3 id="규칙">규칙</h3>
<pre><code>업캐스팅(Base* = new Derived()) 후 delete 할 때
반드시 virtual 소멸자가 필요합니다.</code></pre><h3 id="new-동적-할당">new 동적 할당</h3>
<pre><code class="language-cpp">Base *p = new Derived(); // Derived라는 객체 동적 할당

1. new Derived() -&gt; 힙에 Derived 객체 생성, 그 주소 반환
2. Base* p = -&gt; 반환된 주소를 Base* 포인터에 저장(업캐스팅)</code></pre>
<p>왜 2. 과정이 업케스팅인가?</p>
<p><code>new Derived()</code> 는 </p>
<ul>
<li>Derived 객체를 만들고</li>
<li>Derived* 포인터를 반환</li>
</ul>
<p>그걸 <code>Base*</code>에 저장하면서 업캐스팅이 된다.
기본 클래스 = 파생 클래스 -&gt; 업캐스팅</p>
<h3 id="스택-vs-힙-비교">스택 vs 힙 비교</h3>
<pre><code class="language-cpp">Derived d;          // 스택 - 범위 벗어나면 자동 소멸
Base* p = new Derived();  // 힙 - delete 하기 전까지 살아있음

스택               힙
┌──────────┐      ┌──────────────┐
│  p (주소)│─────→│ Base 영역     │
└──────────┘      │ Derived 영역  │
                  └──────────────┘</code></pre>
<hr />
<h2 id="7-오버로딩--함수-재정의--오버라이딩-비교">7. 오버로딩 / 함수 재정의 / 오버라이딩 비교</h2>
<table>
<thead>
<tr>
<th>비교 요소</th>
<th>오버로딩</th>
<th>함수 재정의 (가상 함수가 아닌 멤버)</th>
<th>오버라이딩</th>
</tr>
</thead>
<tbody><tr>
<td><strong>정의</strong></td>
<td>매개변수 타입이나 개수가 다르지만, 이름이 같은 함수들이 중복 작성되는 것</td>
<td>기본 클래스의 멤버 함수를 파생 클래스에서 이름, 매개변수 타입과 개수, 리턴 타입까지 완벽히 같은 원형으로 재작성하는 것</td>
<td>기본 클래스의 가상 함수를 파생 클래스에서 이름, 매개변수 타입과 개수, 리턴 타입까지 완벽히 같은 원형으로 재작성하는 것</td>
</tr>
<tr>
<td><strong>존재</strong></td>
<td>클래스 멤버들 사이, 외부 함수들 사이, 기본 클래스와 파생 클래스 사이에 존재 가능</td>
<td>상속 관계</td>
<td>상속 관계</td>
</tr>
<tr>
<td><strong>목적</strong></td>
<td>이름이 같은 여러 개의 함수를 중복 작성하여 사용의 편의성 향상</td>
<td>기본 클래스의 멤버 함수와 별도로 파생 클래스에서 필요하여 재작성</td>
<td>기본 클래스에 구현된 가상 함수를 무시하고, 파생 클래스에서 새로운 기능으로 재작성하고자 함</td>
</tr>
<tr>
<td><strong>바인딩</strong></td>
<td>정적 바인딩. 컴파일 시에 중복된 함수들의 호출 구분</td>
<td>정적 바인딩. 컴파일 시에 함수의 호출 구분</td>
<td>동적 바인딩. 실행 시간에 오버라이딩된 함수를 찾아 실행</td>
</tr>
<tr>
<td><strong>객체 지향 특성</strong></td>
<td>컴파일 시간 다형성</td>
<td>컴파일 시간 다형성</td>
<td>실행 시간 다형성</td>
</tr>
</tbody></table>
<hr />
<h2 id="8-순수-가상-함수pure-virtual-function">8. 순수 가상 함수(Pure Virtual Function)</h2>
<p>함수의 코드가 없고 <strong>선언만 있는</strong> 가상 멤버 함수입니다.</p>
<pre><code class="language-cpp">class Shape {
public:
    virtual void draw() = 0;  // 순수 가상 함수 선언
};</code></pre>
<p><code>= 0</code> 은 <strong>&quot;이 함수는 구현 안함, 파생 클래스에서 반드시 구현해라&quot;</strong> 라는 의미입니다.</p>
<hr />
<h2 id="9-추상-클래스abstract-class">9. 추상 클래스(Abstract Class)</h2>
<p><strong>최소한 하나의 순수 가상 함수를 가진 클래스</strong>입니다.</p>
<pre><code class="language-cpp">class Shape {
    Shape* next;
public:
    void paint() { draw(); }
    virtual void draw() = 0;  // 순수 가상 함수
};</code></pre>
<h3 id="추상-클래스의-특징">추상 클래스의 특징</h3>
<p>객체 생성이 불가능합니다.</p>
<pre><code class="language-cpp">Shape shape;          // ❌ 컴파일 오류
Shape* p = new Shape(); // ❌ 컴파일 오류
Shape* p;             // ✅ 포인터 선언만 가능</code></pre>
<h3 id="virtual만-있는-클래스-vs-추상-클래스">virtual만 있는 클래스 vs 추상 클래스</h3>
<blockquote>
<p>📁 예제 코드</p>
<ul>
<li><a href="https://github.com/kyoung-mo/cpp/tree/main/chap9/Shape">Shape (가상 함수)</a></li>
<li><a href="https://github.com/kyoung-mo/cpp/tree/main/chap9/virtual_shape">virtual_shape (추상 클래스)</a></li>
</ul>
</blockquote>
<pre><code class="language-cpp">// virtual만 있는 클래스 → 추상 클래스 아님
class Shape {
public:
    virtual void draw() {
        cout &lt;&lt; &quot;Shape&quot; &lt;&lt; endl;  // 구현이 있음
    }
};
Shape s;  // ✅ 객체 생성 가능

// 추상 클래스
class Shape {
public:
    virtual void draw() = 0;  // = 0 이 붙어야 순수 가상 함수
};
Shape s;  // ❌ 객체 생성 불가</code></pre>
<h3 id="추상-클래스를-쓰는-이유">추상 클래스를 쓰는 이유</h3>
<p>파생 클래스가 특정 함수를 <strong>반드시 구현하도록 강제</strong>하기 위해서입니다.</p>
<pre><code class="language-cpp">class Shape {
public:
    virtual void draw() = 0;  // 반드시 구현하도록 강제
};

class Circle : public Shape {
public:
    void draw() { cout &lt;&lt; &quot;Circle&quot; &lt;&lt; endl; }  // 구현 안하면 컴파일 오류
};</code></pre>
<hr />
<h2 id="10-추상-클래스의-상속과-구현">10. 추상 클래스의 상속과 구현</h2>
<p>추상 클래스를 단순 상속하면 자동으로 추상 클래스가 됩니다.
순수 가상 함수를 모두 오버라이딩하면 일반 클래스가 됩니다.</p>
<pre><code class="language-cpp">class Calculator {
public:
    virtual int add(int a, int b) = 0;
    virtual int subtract(int a, int b) = 0;
    virtual double average(int a[], int size) = 0;
    virtual ~Calculator() {}  // 업캐스팅 후 delete 할 때를 위한 virtual 소멸자
};

class GoodCalc : public Calculator {
public:
    int add(int a, int b) { return a + b; }
    int subtract(int a, int b) { return a - b; }
    double average(int a[], int size) {
        double sum = 0;
        for (int i = 0; i &lt; size; i++) sum += a[i];
        return sum / size;
    }
};

int main() {
    Calculator* c = new GoodCalc();  // 동적 할당 + 업캐스팅
    int a[] = { 1, 2, 3, 4, 5 };

    cout &lt;&lt; c-&gt;add(2, 3) &lt;&lt; endl;       // 5
    cout &lt;&lt; c-&gt;subtract(3, 4) &lt;&lt; endl;  // -1
    cout &lt;&lt; c-&gt;average(a, 5) &lt;&lt; endl;   // 3
    delete c;
}</code></pre>
<blockquote>
<p><code>Calculator*</code> 포인터로 받아서 쓰면 나중에 <code>GoodCalc</code> 대신 다른 구현체(<code>BetterCalc</code>, <code>FastCalc</code> 등)로 교체할 때 포인터 타입을 바꾸지 않아도 되는 장점이 있습니다.</p>
</blockquote>
<hr />
<h2 id="정리">정리</h2>
<pre><code>virtual void f() { }   → 가상 함수        → 구현 있음  → 객체 생성 가능
virtual void f() = 0   → 순수 가상 함수   → 구현 없음  → 객체 생성 불가 (추상 클래스)

정적 바인딩 → 컴파일 시점 결정 (오버로딩, 함수 재정의)
동적 바인딩 → 실행 시점 결정  (오버라이딩 + virtual)

업캐스팅 후 delete 할 때 → 반드시 virtual 소멸자 필요</code></pre>