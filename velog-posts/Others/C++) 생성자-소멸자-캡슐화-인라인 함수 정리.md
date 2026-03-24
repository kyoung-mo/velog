<h2 id="1-생성자와-메모리-할당">1. 생성자와 메모리 할당</h2>
<p>생성자가 메모리를 동적으로 할당해주는 것이 <strong>아니다</strong>.  
객체의 메모리는 <strong>어디에 선언했느냐</strong>에 따라 결정된다.</p>
<pre><code class="language-cpp">MyClass obj;              // 스택에 할당
MyClass* obj = new MyClass(); // 힙에 할당 (동적 할당)</code></pre>
<p>생성자의 역할은 메모리를 잡는 것이 아니라, <strong>이미 잡힌 메모리(멤버 변수)를 초기화</strong>하는 것이다.</p>
<hr />
<h2 id="2-소멸자-destructor">2. 소멸자 (Destructor)</h2>
<h3 id="기본-개념">기본 개념</h3>
<ul>
<li>객체가 소멸될 때 자동으로 호출되는 함수</li>
<li><code>~클래스명()</code> 형태로 선언</li>
<li><strong>클래스당 하나만</strong> 존재 (오버로딩 불가)</li>
<li>인자 없음, 반환값 없음</li>
</ul>
<pre><code class="language-cpp">class Circle {
public:
    Circle();       // 생성자 1
    Circle(int r);  // 생성자 2 (오버로딩 가능)
    ~Circle();      // 소멸자는 하나뿐
};</code></pre>
<h3 id="소멸자가-필요한-경우">소멸자가 필요한 경우</h3>
<table>
<thead>
<tr>
<th>상황</th>
<th>소멸자 필요 여부</th>
</tr>
</thead>
<tbody><tr>
<td>멤버가 int, double 등 기본 타입만 있을 때</td>
<td>없어도 됨 (기본 소멸자 자동 생성)</td>
</tr>
<tr>
<td>생성자 안에서 <code>new</code>로 동적 할당했을 때</td>
<td><strong>반드시 필요</strong></td>
</tr>
<tr>
<td>파일 핸들, 소켓 등 외부 자원을 사용할 때</td>
<td><strong>반드시 필요</strong></td>
</tr>
</tbody></table>
<pre><code class="language-cpp">class Buffer {
    int* data;
public:
    Buffer(int n) {
        data = new int[n];  // 힙 동적 할당
    }
    ~Buffer() {
        delete[] data;  // 소멸자에서 해제 안 하면 메모리 누수
    }
};</code></pre>
<h3 id="메모리-구조">메모리 구조</h3>
<pre><code>Buffer buf(5) 생성
│
├─ 스택: buf.data (포인터), buf.size  ← 자동 관리
└─ 힙:  [0][1][2][3][4]              ← new로 잡은 것, 수동 관리 필요

buf 스코프 끝
│
├─ 스택 자동 해제 → buf.data 포인터 변수 사라짐
└─ 소멸자 호출 → delete[] data → 힙도 해제 ✅</code></pre><hr />
<h2 id="3-객체-소멸-순서">3. 객체 소멸 순서</h2>
<h3 id="핵심-규칙-생성의-역순으로-소멸">핵심 규칙: 생성의 역순으로 소멸</h3>
<table>
<thead>
<tr>
<th>구분</th>
<th>생성 시점</th>
<th>소멸 시점</th>
<th>역순 이유</th>
</tr>
</thead>
<tbody><tr>
<td>전역 객체</td>
<td><code>main()</code> 실행 전</td>
<td><code>main()</code> 종료 후</td>
<td>C++ 런타임이 <code>atexit()</code>으로 보장</td>
</tr>
<tr>
<td>지역 객체</td>
<td>선언된 줄 도달 시</td>
<td>해당 <code>{}</code> 스코프 끝</td>
<td>스택 LIFO 구조</td>
</tr>
</tbody></table>
<pre><code class="language-cpp">Circle globalDonut(1000);  // 전역
Circle globalPizza(2000);  // 전역

void f() {
    Circle fDonut(100);
    Circle fPizza(200);
}   // fPizza → fDonut 순으로 소멸

int main() {
    Circle mainDonut;
    Circle mainPizza(30);
    f();
    return 0;
}</code></pre>
<p>실행 결과:</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c62daa73-544e-432b-9363-fc25c073e9c7/image.png" /></p>
<blockquote>
<p>지역 객체는 스택 자체가 LIFO 구조이기 때문에 자연스럽게 역순 소멸된다.<br />전역 객체는 데이터 세그먼트에 저장되므로 스택과 무관하지만, C++ 런타임이 <code>atexit()</code>에 소멸자를 역순 등록해 동일한 규칙을 보장한다.</p>
</blockquote>
<hr />
<h2 id="4-접근-지정자">4. 접근 지정자</h2>
<table>
<thead>
<tr>
<th>지정자</th>
<th>접근 범위</th>
</tr>
</thead>
<tbody><tr>
<td><code>public</code></td>
<td>클래스 외부에서 자유롭게 접근 가능</td>
</tr>
<tr>
<td><code>private</code></td>
<td>클래스 내부(멤버 함수)에서만 접근 가능</td>
</tr>
<tr>
<td><code>protected</code></td>
<td>private + 상속받은 자식 클래스에서도 접근 가능</td>
</tr>
</tbody></table>
<h3 id="캡슐화-데이터는-숨기고-기능만-열어두기">캡슐화: 데이터는 숨기고, 기능만 열어두기</h3>
<p><code>private</code>은 접근을 완전히 막는 것이 아니다.<br /><strong>클래스 외부</strong>에서 직접 접근을 막고, <strong>멤버 함수를 통해서만</strong> 접근하게 강제하는 것이다.</p>
<pre><code class="language-cpp">class Circle {
private:
    int radius;  // 외부에서 직접 접근 불가

public:
    void setRadius(int r) {
        if (r &lt; 0) return;  // 잘못된 값을 여기서 걸러냄
        radius = r;
    }
    double getArea() {
        return 3.14 * radius * radius;  // 멤버 함수 안에서는 자유롭게 사용
    }
};

int main() {
    Circle c;
    c.radius = -10;    // ❌ 컴파일 에러
    c.setRadius(-10);  // ✅ 호출은 되지만 내부에서 무시됨
}</code></pre>
<blockquote>
<p>멤버 변수는 <code>private</code>, 멤버 함수는 <code>public</code>으로 두는 것이 일반적인 캡슐화 패턴이다.</p>
</blockquote>
<hr />
<h2 id="5-인라인-함수-inline">5. 인라인 함수 (inline)</h2>
<h3 id="함수-호출-오버헤드">함수 호출 오버헤드</h3>
<p>함수를 호출하면 리턴 주소 저장, 레지스터 저장, 매개변수 스택 저장 등의 부가 작업이 발생한다.<br />함수 내용이 단순할수록 실행 시간 대비 오버헤드 비율이 커진다.</p>
<h3 id="인라인-함수-동작">인라인 함수 동작</h3>
<pre><code class="language-cpp">inline int add(int a, int b) { return a + b; }

// 작성한 코드
int result = add(3, 5);

// 컴파일 후 실제 동작 (함수 호출 없이 치환)
int result = 3 + 5;</code></pre>
<h3 id="매크로-vs-인라인-함수">매크로 vs 인라인 함수</h3>
<pre><code class="language-cpp">// 매크로 — 텍스트 단순 치환, 위험
#define SQUARE(x) x * x
SQUARE(1 + 2)  // → 1 + 2 * 1 + 2 = 5 (기대값 9인데!)

// 인라인 함수 — 인자 먼저 계산 후 전달, 안전
inline int square(int x) { return x * x; }
square(1 + 2)  // → square(3) → 3 * 3 = 9 ✅</code></pre>
<table>
<thead>
<tr>
<th></th>
<th>매크로</th>
<th>인라인 함수</th>
</tr>
</thead>
<tbody><tr>
<td>동작</td>
<td>텍스트 치환</td>
<td>코드 치환</td>
</tr>
<tr>
<td>타입 체크</td>
<td>❌</td>
<td>✅</td>
</tr>
<tr>
<td>안전성</td>
<td>낮음</td>
<td>높음</td>
</tr>
</tbody></table>
<h3 id="자동-인라인-함수">자동 인라인 함수</h3>
<p>클래스 선언부 <code>{}</code> 안에 본체까지 작성하면 <code>inline</code> 키워드 없이도 자동으로 인라인 처리된다.</p>
<pre><code class="language-cpp">class Circle {
private:
    int radius;
public:
    // 클래스 안에 본체 작성 → 자동 인라인
    double getArea() { return 3.14 * radius * radius; }

    Circle(int r);  // 선언만 → 인라인 아님
};

Circle::Circle(int r) {  // 클래스 밖에서 정의 → 일반 함수
    radius = r;
}</code></pre>
<table>
<thead>
<tr>
<th>방식</th>
<th>인라인 여부</th>
</tr>
</thead>
<tbody><tr>
<td>클래스 안에서 선언 + 본체 작성</td>
<td>자동 인라인</td>
</tr>
<tr>
<td>클래스 밖에서 <code>::</code> 로 정의</td>
<td>일반 함수</td>
</tr>
<tr>
<td>클래스 밖에서 <code>inline</code> 키워드 붙여 정의</td>
<td>명시적 인라인</td>
</tr>
</tbody></table>
<hr />
<h2 id="6-파일-분할-h--cpp">6. 파일 분할 (.h / .cpp)</h2>
<p>규모가 커지면 클래스 선언과 구현을 분리한다.
아래 코드를 분리해보자.</p>
<p><a href="https://github.com/kyoung-mo/cpp/blob/main/chap3/%EC%98%88%EC%A0%9C%203-3/ex3-3-Circle.cpp">ex3-3-Circle.cpp</a></p>
<hr />
<h3 id="파일-구조">파일 구조</h3>
<pre><code>Circle.h    — 클래스 선언 (설계도)
Circle.cpp  — 멤버 함수 구현
main.cpp    — 진입점</code></pre><h3 id="circleh">Circle.h</h3>
<pre><code class="language-cpp">#pragma once
#ifndef __CIRCLE_H__
#define __CIRCLE_H__

class Circle {
public:
    int radius;
    Circle();
    Circle(int r);
    double getArea();
};

#endif</code></pre>
<h3 id="circlecpp">Circle.cpp</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;
#include &quot;Circle.h&quot;

Circle::Circle() {
    radius = 1;
}

Circle::Circle(int r) {
    radius = r;
}

double Circle::getArea() {
    return 3.14 * radius * radius;
}</code></pre>
<h3 id="maincpp">main.cpp</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;
#include &quot;Circle.h&quot;  // .cpp가 아닌 .h를 include

int main() {
    Circle donut;
    Circle pizza(30);
}</code></pre>
<hr />
<h3 id="❌-cpp를-include하면-안-되는-이유">❌ <code>.cpp</code>를 <code>#include</code>하면 안 되는 이유</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/288286d0-2f1a-4bff-9f7d-c2512c478998/image.png" /></p>
<p>실습에서 <code>main.cpp</code> 에 <code>circle.cpp</code> 를 계속 include 하고 있었다. <code>circle.cpp</code>를 작성 했으니 어느 부분에는 포함시켜줘야 작동하지 않을까? 했는데, 아직 컴파일에 대한 개념이 덜 잡혀있었던 것을 확인하였다.</p>
<h3 id="컴파일-및-링크-과정">컴파일 및 링크 과정</h3>
<pre><code>[컴파일 단계]
Circle.cpp  →  Circle.o
main.cpp    →  main.o

[링크 단계]
Circle.o + main.o  →  실행파일</code></pre><blockquote>
<p><code>.h</code> 파일은 독립적으로 컴파일되지 않는다.<br /><code>#include</code> 시점에 해당 <code>.cpp</code> 안으로 텍스트 복붙되어 함께 컴파일된다.<br />따라서 <code>.h</code>에 대응하는 목적파일(.o)은 생성되지 않는다.</p>
</blockquote>
<p>결론적으로, 각각의 <code>.cpp</code> 파일들이 컴파일 되어 목적 파일 <code>.obj</code>가 생성된 후(여기서 헤더 파일은 컴파일 과정에 포함되지 않는다), 각각의 목적 파일이 링킹되어 하나의 실행 파일로 합쳐지는 과정을 거친다. </p>
<p>만약 내가 했던 것 처럼 <code>main.cpp</code>에서 <code>#include &quot;Circle.cpp&quot;</code> 를 하게 되면 Circle 함수에 대한 정의가 중복되는 문제가 생긴다.</p>
<pre><code class="language-cpp">Circle.cpp → Circle.o  (Circle 함수 정의 1번)
main.cpp   → main.o    (Circle 함수 정의 2번 — 복붙됨)

링크 시 → &quot;같은 함수가 두 개!&quot; → 중복 정의 오류</code></pre>