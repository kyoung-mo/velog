<p>오늘 진도나간 예외 처리(try-throw-catch) 부분에 대해 복습 겸 정리해보겠습니다.</p>
<hr />
<h2 id="1-실행-오류의-종류">1. 실행 오류의 종류</h2>
<p>C++ 프로그램에서 발생하는 오류는 크게 두 가지로 나뉩니다.</p>
<table>
<thead>
<tr>
<th>종류</th>
<th>원인</th>
<th>발생 시점</th>
</tr>
</thead>
<tbody><tr>
<td>컴파일 오류</td>
<td>문법에 맞지 않는 구문</td>
<td>빌드 시</td>
</tr>
<tr>
<td>실행 오류</td>
<td>개발자의 논리 오류, 예외적 입력/상황 미처리</td>
<td>런타임</td>
</tr>
</tbody></table>
<p>실행 오류의 결과는 엉뚱한 값 출력, 잘못된 코드 실행, 또는 프로그램의 비정상 종료로 이어집니다.</p>
<hr />
<h2 id="2-기존-오류-처리-방식의-한계">2. 기존 오류 처리 방식의 한계</h2>
<p>예외 처리 기능이 없던 시절에는 <code>if</code>문과 리턴 값으로 오류를 처리했습니다.</p>
<h3 id="방법-1--특수-리턴-값-사용">방법 1 — 특수 리턴 값 사용</h3>
<pre><code class="language-cpp">int getExp(int base, int exp) {
    if (base &lt;= 0 || exp &lt;= 0)
        return -1;  // 오류를 -1로 표현
    int value = 1;
    for (int n = 0; n &lt; exp; n++)
        value = value * base;
    return value;
}

int main() {
    int v = getExp(2, 3);
    if (v != -1)
        cout &lt;&lt; &quot;2의 3승은 &quot; &lt;&lt; v &lt;&lt; &quot;입니다.&quot; &lt;&lt; endl;
    else
        cout &lt;&lt; &quot;오류. 계산할 수 없습니다.&quot; &lt;&lt; endl;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0503d23a-df63-46b9-a5b9-dcf25a440e31/image.png" /></p>
<p>이 방식의 문제는 <strong>-1이 정상적인 계산 결과일 수도 있다</strong>는 점입니다. 오류 값과 정상 값이 혼동될 수 있습니다.</p>
<h3 id="방법-2--bool-리턴--참조-매개변수">방법 2 — bool 리턴 + 참조 매개변수</h3>
<pre><code class="language-cpp">bool getExp(int base, int exp, int&amp; ret) {
    if (base &lt;= 0 || exp &lt;= 0)
        return false;
    int value = 1;
    for (int n = 0; n &lt; exp; n++)
        value = value * base;
    ret = value;
    return true;
}

int main() {
    int v = 0;
    if (getExp(2, 3, v))
        cout &lt;&lt; &quot;2의 3승은 &quot; &lt;&lt; v &lt;&lt; &quot;입니다.&quot; &lt;&lt; endl;
    else
        cout &lt;&lt; &quot;오류. 계산할 수 없습니다.&quot; &lt;&lt; endl;
}</code></pre>
<p>성공/실패를 <code>bool</code>로 분리하고 결과는 참조로 전달하는 방식입니다. 리턴 값 혼동 문제는 해결되지만, 함수를 호출하는 쪽마다 <strong>매번 if문으로 확인</strong>해야 하는 번거로움이 있습니다. C++은 이 문제를 <code>try-throw-catch</code>로 해결합니다.</p>
<hr />
<h2 id="3-예외exception란">3. 예외(Exception)란?</h2>
<p><strong>예외(Exception)</strong> 는 실행 중 프로그램의 오동작이나 결과에 영향을 미치는 <strong>예상치 못한 상황</strong>입니다.</p>
<ul>
<li>예시: <code>getExp(2, -3)</code>처럼 음수 지수가 입력되어 잘못된 결과(1)가 나오는 경우</li>
</ul>
<p><strong>예외 처리기(Exception Handler)</strong> 는 예외 발생을 탐지하고 처리하는 코드로, 잘못된 결과나 비정상 종료를 막는 역할을 합니다.</p>
<h3 id="예외-처리-수준">예외 처리 수준</h3>
<table>
<thead>
<tr>
<th>수준</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td>운영체제 수준</td>
<td>OS가 예외를 탐지하여 응용 프로그램에 알림. OS/컴파일러 의존적</td>
</tr>
<tr>
<td>응용프로그램 수준</td>
<td>잘못된 입력, 없는 파일 접근 등을 프로그램 자체에서 처리. <strong>C++ 예외 처리가 이에 해당</strong></td>
</tr>
</tbody></table>
<hr />
<h2 id="4-try-throw-catch-기본-형식">4. try-throw-catch 기본 형식</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/58a0f5ab-c3b4-48c8-870b-f46d51bf7c0f/image.png" /></p>
<p>C++ 예외 처리는 세 가지 키워드로 구성됩니다.</p>
<table>
<thead>
<tr>
<th>키워드</th>
<th>역할</th>
</tr>
</thead>
<tbody><tr>
<td><code>try { }</code></td>
<td>예외가 발생할 가능성이 있는 코드를 묶음</td>
</tr>
<tr>
<td><code>throw</code></td>
<td>예외 발생을 알림. 반드시 <code>try</code> 블록 안에서 실행되어야 함</td>
</tr>
<tr>
<td><code>catch() { }</code></td>
<td><code>throw</code>로 던져진 예외를 받아 처리</td>
</tr>
</tbody></table>
<pre><code class="language-cpp">try {
    // 예외가 발생할 수 있는 코드
    if (조건)
        throw 예외값;  // 예외 발생 알림
}
catch (처리할_타입 변수) {
    // 예외 처리 코드
}</code></pre>
<h3 id="예제-1--0으로-나누는-예외-처리">예제 1 — 0으로 나누는 예외 처리</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;

int main() {
    int n, sum, average;

    while (true) {
        cout &lt;&lt; &quot;합을 입력하세요 &gt;&gt; &quot;;
        cin &gt;&gt; sum;
        cout &lt;&lt; &quot;인원수를 입력하세요 &gt;&gt; &quot;;
        cin &gt;&gt; n;

        try {
            if (n &lt;= 0)
                throw n;       // int 타입 예외 던지기
            else
                average = sum / n;
        }
        catch (int x) {        // int 타입 예외 수신
            cout &lt;&lt; &quot;예외 발생!! &quot; &lt;&lt; x &lt;&lt; &quot;으로 나눌 수 없음&quot; &lt;&lt; endl &lt;&lt; endl;
            average = 0;
            continue;
        }
        cout &lt;&lt; &quot;평균 = &quot; &lt;&lt; average &lt;&lt; endl &lt;&lt; endl;
    }
}</code></pre>
<p><code>throw n</code>으로 <code>int</code> 타입 값을 던지면, <code>catch(int x)</code>에서 그 값을 받아 처리합니다. <code>throw</code> 이후의 코드는 실행되지 않고 바로 <code>catch</code> 블록으로 점프합니다.</p>
<h3 id="예제-2--예외-처리로-재작성한-지수-계산">예제 2 — 예외 처리로 재작성한 지수 계산</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;

int getExp(int base, int exp) {
    if (base &lt;= 0 || exp &lt;= 0)
        throw &quot;음수 사용 불가&quot;;  // 함수 내에서 throw 가능
    int value = 1;
    for (int n = 0; n &lt; exp; n++)
        value = value * base;
    return value;
}

int main() {
    int v = 0;
    try {
        v = getExp(2, 3);
        cout &lt;&lt; &quot;2의 3승은 &quot; &lt;&lt; v &lt;&lt; &quot;입니다.&quot; &lt;&lt; endl;

        v = getExp(2, -3);  // 여기서 예외 발생 → 아래 줄은 실행 안 됨
        cout &lt;&lt; &quot;2의 -3승은 &quot; &lt;&lt; v &lt;&lt; &quot;입니다.&quot; &lt;&lt; endl;
    }
    catch (const char* s) {
        cout &lt;&lt; s &lt;&lt; endl;
    }
}</code></pre>
<p><code>throw</code>가 함수 내부에서 발생해도, 호출한 쪽의 <code>try-catch</code>가 이를 잡아냅니다. <code>getExp(2, -3)</code> 호출 후 예외가 발생하면 그 아래 줄은 실행되지 않고 바로 <code>catch</code> 블록으로 이동합니다.</p>
<hr />
<h2 id="5-다양한-throw-catch-패턴">5. 다양한 throw-catch 패턴</h2>
<h3 id="다수의-catch-블록">다수의 catch 블록</h3>
<p><code>try</code> 블록 하나에 여러 <code>catch</code> 블록을 연결할 수 있습니다. <code>throw</code>된 타입과 일치하는 <code>catch</code>가 실행됩니다.</p>
<pre><code class="language-cpp">try {
    throw &quot;음수 불가능&quot;;  // const char* 타입
    // 또는
    throw 3;              // int 타입
}
catch (const char* s) {
    cout &lt;&lt; s;
}
catch (int x) {
    cout &lt;&lt; x;
}</code></pre>
<h3 id="함수-내-throw--외부-catch">함수 내 throw + 외부 catch</h3>
<pre><code class="language-cpp">int multiply(int x, int y) {
    if (x &lt; 0 || y &lt; 0)
        throw &quot;음수 불가능&quot;;
    return x * y;
}

int main() {
    try {
        int n = multiply(2, -3);
        cout &lt;&lt; &quot;곱은 &quot; &lt;&lt; n &lt;&lt; endl;
    }
    catch (const char* msg) {
        cout &lt;&lt; &quot;exception happened : &quot; &lt;&lt; msg;
    }
}</code></pre>
<p><code>throw</code>는 함수 내부에서 발생해도 호출 스택을 거슬러 올라가며 맞는 <code>catch</code>를 찾습니다. 이것을 <strong>스택 풀기(stack unwinding)</strong> 라고 합니다.</p>
<h3 id="예제-3--문자열을-정수로-변환">예제 3 — 문자열을 정수로 변환</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
#include &lt;cstring&gt;
using namespace std;

int stringToInt(const char x[]) {
    int sum = 0;
    int len = strlen(x);
    for (int i = 0; i &lt; len; i++) {
        if (x[i] &gt;= '0' &amp;&amp; x[i] &lt;= '9')
            sum = sum * 10 + x[i] - '0';
        else
            throw x;  // 숫자가 아닌 문자 발견 시 예외
    }
    return sum;
}

int main() {
    int n;
    try {
        n = stringToInt(&quot;123&quot;);
        cout &lt;&lt; &quot;\&quot;123\&quot; 은 정수 &quot; &lt;&lt; n &lt;&lt; &quot;로 변환됨&quot; &lt;&lt; endl;
        n = stringToInt(&quot;1A3&quot;);  // 여기서 예외 발생
        cout &lt;&lt; &quot;\&quot;1A3\&quot; 은 정수 &quot; &lt;&lt; n &lt;&lt; &quot;로 변환됨&quot; &lt;&lt; endl;
    }
    catch (const char* s) {
        cout &lt;&lt; s &lt;&lt; &quot; 처리에서 예외 발생!!&quot; &lt;&lt; endl;
    }
}</code></pre>
<hr />
<h2 id="6-예외를-발생시키는-함수-선언">6. 예외를 발생시키는 함수 선언</h2>
<p>함수 원형에 <code>throw(타입, ...)</code> 를 명시하면, 이 함수가 어떤 타입의 예외를 발생시키는지 선언할 수 있습니다.</p>
<pre><code class="language-cpp">int max(int x, int y) throw(int) {
    if (x &lt; 0) throw x;
    else if (y &lt; 0) throw y;
    else if (x &gt; y) return x;
    else return y;
}

double valueAt(double* p, int index) throw(int, char*) {
    if (index &lt; 0)
        throw &quot;index out of bounds exception&quot;;
    else if (p == NULL)
        throw 0;
    else
        return p[index];
}</code></pre>
<h3 id="예제-4--예외-처리를-가진-스택-클래스-파일-분리">예제 4 — 예외 처리를 가진 스택 클래스 (파일 분리)</h3>
<p><strong>MyStack.h</strong></p>
<pre><code class="language-cpp">#ifndef MYSTACK_H
#define MYSTACK_H

class MyStack {
    int data[100];
    int tos;
public:
    MyStack() { tos = -1; }
    void push(int n) throw(char*);
    int  pop()       throw(char*);
};

#endif</code></pre>
<p><strong>MyStack.cpp</strong></p>
<pre><code class="language-cpp">#include &quot;MyStack.h&quot;

void MyStack::push(int n) {
    if (tos == 99)
        throw &quot;Stack Full&quot;;
    tos++;
    data[tos] = n;
}

int MyStack::pop() {
    if (tos == -1)
        throw &quot;Stack Empty&quot;;
    return data[tos--];
}</code></pre>
<p><strong>main.cpp</strong></p>
<pre><code class="language-cpp">#include &lt;iostream&gt;
#include &quot;MyStack.h&quot;
using namespace std;

int main() {
    MyStack intStack;
    try {
        intStack.push(100);
        intStack.push(200);
        cout &lt;&lt; intStack.pop() &lt;&lt; endl;  // 200
        cout &lt;&lt; intStack.pop() &lt;&lt; endl;  // 100
        cout &lt;&lt; intStack.pop() &lt;&lt; endl;  // &quot;Stack Empty&quot; 예외 발생
    }
    catch (const char* s) {
        cout &lt;&lt; &quot;예외 발생 : &quot; &lt;&lt; s &lt;&lt; endl;
    }
}</code></pre>
<p>함수 원형에 <code>throw(char*)</code>를 명시해두면 이 함수를 호출하는 개발자가 <strong>어떤 예외를 처리해야 하는지 즉시 알 수 있어</strong> 가독성과 유지보수성이 높아집니다.</p>
<hr />
<h2 id="7-다중-try-블록과-주의사항">7. 다중 try 블록과 주의사항</h2>
<h3 id="중첩-try-블록">중첩 try 블록</h3>
<p><code>try</code> 블록은 중첩이 가능하며, 안쪽 <code>catch</code>가 처리하지 못한 예외는 바깥쪽 <code>catch</code>로 전달됩니다.</p>
<pre><code class="language-cpp">try {
    throw 3;  // 바깥 catch(int)가 처리
    try {
        throw &quot;abc&quot;;  // 안쪽 catch(const char*)가 처리
    }
    catch (int inner) {
        cout &lt;&lt; inner;
    }
}
catch (const char* s) {
    cout &lt;&lt; s;
}
catch (int outer) {
    cout &lt;&lt; outer;
}</code></pre>
<h3 id="throw-사용-시-주의사항">throw 사용 시 주의사항</h3>
<pre><code class="language-cpp">// ❌ try 블록 밖의 throw → abort() 호출, 강제 종료
throw 3;

// ❌ 매칭되는 catch가 없으면 프로그램 강제 종료
try {
    throw &quot;aa&quot;;
}
catch (double p) { }  // double catch는 char*를 못 잡음

// ✅ catch 블록 내에 try-catch 중첩 가능
try {
    throw 3;
}
catch (int x) {
    try {
        throw &quot;aa&quot;;
    }
    catch (const char* p) {
        cout &lt;&lt; p;
    }
}</code></pre>
<hr />
<h2 id="8-예외-클래스-만들기">8. 예외 클래스 만들기</h2>
<p><code>int</code>나 <code>const char*</code> 같은 기본 타입 대신, <strong>클래스 객체를 예외 값으로 던질 수 있습니다.</strong> 더 많은 예외 정보를 담을 수 있고, 상속을 통해 예외 계층을 구성할 수 있다는 장점이 있습니다.</p>
<h3 id="예제-5--예외-클래스-계층-구조">예제 5 — 예외 클래스 계층 구조</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
#include &lt;string&gt;
using namespace std;

// 기반 예외 클래스
class MyException {
    int lineNo;
    string func, msg;
public:
    MyException(int n, string f, string m)
        : lineNo(n), func(f), msg(m) { }
    void print() {
        cout &lt;&lt; func &lt;&lt; &quot;:&quot; &lt;&lt; lineNo &lt;&lt; &quot; ,&quot; &lt;&lt; msg &lt;&lt; endl;
    }
};

// 파생 예외 클래스 1
class DivideByZeroException : public MyException {
public:
    DivideByZeroException(int lineNo, string func, string msg)
        : MyException(lineNo, func, msg) { }
};

// 파생 예외 클래스 2
class InvalidInputException : public MyException {
public:
    InvalidInputException(int lineNo, string func, string msg)
        : MyException(lineNo, func, msg) { }
};

int main() {
    int x, y;
    try {
        cout &lt;&lt; &quot;두 개의 양의 정수를 입력하세요 &gt;&gt; &quot;;
        cin &gt;&gt; x &gt;&gt; y;
        if (x &lt; 0 || y &lt; 0)
            throw InvalidInputException(32, &quot;main()&quot;, &quot;음수 입력 예외 발생&quot;);
        if (y == 0)
            throw DivideByZeroException(34, &quot;main()&quot;, &quot;0으로 나누는 예외 발생&quot;);
        cout &lt;&lt; (double)x / (double)y;
    }
    catch (DivideByZeroException&amp; e) {
        e.print();
    }
    catch (InvalidInputException&amp; e) {
        e.print();
    }
}</code></pre>
<p><code>catch</code>에서 객체를 <strong>참조(<code>&amp;</code>)</strong> 로 받는 이유는 객체 복사 비용을 줄이고, 파생 클래스 객체가 기반 클래스 참조로 처리될 때 <strong>다형성</strong>이 올바르게 동작하도록 하기 위해서입니다.</p>
<hr />
<h2 id="9-extern-c--c-코드와의-링크">9. extern &quot;C&quot; — C 코드와의 링크</h2>
<h3 id="c-프로그램의-컴파일과-링킹">C 프로그램의 컴파일과 링킹</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6448f143-7c8d-4a24-8bd6-36464167315f/image.png" /></p>
<h3 id="c-소스의-컴파일과-링킹">C++ 소스의 컴파일과 링킹</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4bdddf82-8d72-4d56-98cf-5dd732fe20fb/image.png" /></p>
<h3 id="이름-맹글링name-mangling">이름 맹글링(Name Mangling)</h3>
<p>컴파일러는 컴파일 후 목적 코드의 함수에 고유한 이름을 붙이는데, C와 C++이 이 규칙이 다릅니다.</p>
<table>
<thead>
<tr>
<th>언어</th>
<th><code>int f(int x, int y)</code> 컴파일 후 이름</th>
</tr>
</thead>
<tbody><tr>
<td>C</td>
<td><code>_f</code></td>
</tr>
<tr>
<td>C++</td>
<td><code>?f@@YAHHH@Z</code> (매개변수 타입, 개수, 리턴 타입 인코딩)</td>
</tr>
</tbody></table>
<p>C++이 복잡한 이름 규칙을 사용하는 이유는 <strong>함수 오버로딩</strong> 때문입니다. 매개변수가 다른 동일 이름 함수들을 구별해야 하기 때문입니다.</p>
<h3 id="링크-오류-발생">링크 오류 발생</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/62756b93-d3b0-4ccb-87a6-4a07d256f8f6/image.png" /></p>
<p>C++에서 C로 작성된 함수를 호출하면 링크 오류가 발생합니다.</p>
<pre><code>C++ 컴파일러가 생성한 호출 코드 : ?f@@YAHHH@Z 를 찾음
C 컴파일러가 생성한 목적 코드   : _f 로 저장되어 있음
                                → 이름이 달라 링크 실패</code></pre><h3 id="extern-c-로-해결">extern &quot;C&quot; 로 해결</h3>
<p><img alt="업로드중.." src="blob:https://velog.io/fad6160d-2619-4e0e-84f1-dfa57d5c7c6b" /></p>
<p><code>extern &quot;C&quot;</code> 는 C++ 컴파일러에게 해당 코드를 <strong>C 이름 규칙으로 컴파일</strong>하도록 지시합니다.</p>
<pre><code class="language-cpp">// 함수 하나만 지정
extern &quot;C&quot; int f(int x, int y);

// 여러 함수 지정
extern &quot;C&quot; {
    int f(int x, int y);
    void g();
    char s(int []);
}

// 헤더 파일 전체를 C 방식으로 처리
extern &quot;C&quot; {
    #include &quot;mycfunction.h&quot;
}</code></pre>
<p><code>extern &quot;C&quot;</code>를 사용하면 C++ 파일이 C 목적 코드의 <code>_f</code>를 찾을 수 있게 되어 링크에 성공합니다.</p>
<blockquote>
<p>임베디드 개발에서 C로 작성된 HAL 드라이버나 BSP 라이브러리를 C++ 코드에서 호출할 때 이 선언이 필요할 수 있습니다.</p>
</blockquote>
<hr />
<h2 id="10-정리">10. 정리</h2>
<p>기존 <code>if</code>문 방식과 비교했을 때 <code>try-throw-catch</code>의 핵심 장점은, <strong>오류 처리 코드와 정상 로직 코드를 분리</strong>할 수 있다는 점입니다. </p>
<p>함수 내부에서 예외가 발생하면 호출 스택을 자동으로 거슬러 올라가기 때문에, 호출하는 쪽에서 매번 리턴 값을 확인할 필요 없이 <code>try</code> 블록 하나로 묶어 처리할 수 있습니다.</p>