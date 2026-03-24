<p>이전 단원까지는 쉬웠는데 아직도 포인터 개념이 익숙치 않은가봅니다.. 개념 정리하고 예제 반복해보면서 포인터랑 좀 친해지는 과정을 거쳐야겠습니다.</p>
<hr />
<h2 id="1-객체-포인터란">1. 객체 포인터란?</h2>
<p>C++에서 포인터는 특정 변수의 주소를 저장하는 변수입니다. 객체도 마찬가지로 포인터로 가리킬 수 있습니다.</p>
<pre><code class="language-cpp">Circle donut;
Circle* p;
p = &amp;donut;  // donut 객체의 주소를 p에 저장</code></pre>
<hr />
<h2 id="2-포인터로-멤버에-접근하는-방법">2. 포인터로 멤버에 접근하는 방법</h2>
<p>객체 포인터로 멤버 함수에 접근하는 방법은 두 가지입니다.</p>
<pre><code class="language-cpp">// 방법 1: 역참조 후 . 연산자
(*p).getArea();   

// 방법 2: -&gt; 연산자 (위와 완전히 동일)
p-&gt;getArea();     </code></pre>
<p>그렇다면 <code>*p.getArea()</code> 는 왜 안되는가?</p>
<h3 id="pgetarea가-안-되는-이유"><code>*p.getArea()</code>가 안 되는 이유</h3>
<p><code>.</code> 연산자가 <code>*</code> 연산자보다 우선순위가 높기 때문입니다.</p>
<pre><code class="language-cpp">*p.getArea()
// 아래는 컴파일러가 해석하는 방식
*(p.getArea())  // p는 포인터라 .을 쓸 수 없음 → 컴파일 에러</code></pre>
<ol>
<li><code>*p.getArea()</code> &gt; <code>*(p.getArea())</code> </li>
<li><code>(*p).getArea()</code> &gt; <code>(*p).getArea()</code> </li>
<li><code>p-&gt;getArea()</code> &gt; <code>(*p).getArea()</code>와 동일</li>
</ol>
<h3 id="--연산자가-존재하는-이유"><code>-&gt;</code> 연산자가 존재하는 이유</h3>
<p><code>(*p).getArea()</code>처럼 매번 괄호를 쓰는 불편함을 줄이기 위해, <strong>포인터에서 멤버에 바로 접근하는 전용 연산자</strong>로 <code>-&gt;</code> 를 만든 것입니다.</p>
<hr />
<h2 id="3-배열명은-상수-포인터">3. 배열명은 상수 포인터</h2>
<pre><code class="language-cpp">Circle circleArray[3];
Circle* p = circleArray;  // ✅ 배열명을 포인터에 대입 가능
circleArray++;            // ❌ 배열명 자체는 상수라 변경 불가</code></pre>
<p>배열명은 <code>Circle* const</code> 와 같은 개념으로, <strong>항상 첫 번째 원소를 가리키도록 고정된 상수 포인터</strong>입니다.<br />그래서 <code>p++</code> 와 같은 포인터 이동이 필요할 때는 별도의 포인터 변수에 복사해서 사용해야 합니다.</p>
<p>다시 한번.. 배열명은 주소, 주소는 상수, 배열명은 상수.</p>
<h3 id="포인터-산술-연산">포인터 산술 연산</h3>
<pre><code class="language-cpp">p++;  // sizeof(Circle) 만큼 주소 이동</code></pre>
<p><code>p++</code>은 단순히 주소 +1이 아니라, <strong>타입 크기만큼 자동으로 이동</strong>합니다.</p>
<pre><code>[circleArray[0]] [circleArray[1]] [circleArray[2]]
      ↑                ↑                ↑
      p           p++ 후 p         p++ 후 p</code></pre><hr />
<h2 id="4-this-포인터">4. this 포인터</h2>
<h3 id="this가-필요한-이유">this가 필요한 이유</h3>
<pre><code class="language-cpp">Circle c1, c2;
c1.setRadius(10);
c2.setRadius(20);</code></pre>
<p><code>setRadius</code> 함수는 코드에 하나뿐인데, c1을 바꿀 때도 c2를 바꿀 때도 <strong>같은 함수</strong>를 사용합니다.<br />함수 입장에서 &quot;지금 내가 누구의 radius를 바꿔야 하지?&quot;를 알기 위해 <code>this</code>가 필요합니다.</p>
<h3 id="컴파일러가-실제로-하는-일">컴파일러가 실제로 하는 일</h3>
<pre><code class="language-cpp">// 내가 쓴 코드
void setRadius(int r) {
    radius = r;
}

// 컴파일러가 변환한 실제 코드 (개념적으로)
void setRadius(Circle* this, int r) {
    this-&gt;radius = r;
}</code></pre>
<p><code>this</code>는 <strong>&quot;지금 이 함수를 호출한 객체의 주소&quot;</strong>입니다.<br />c1이 호출하면 <code>this = &amp;c1</code>, c2가 호출하면 <code>this = &amp;c2</code>가 됩니다.</p>
<h3 id="이름-충돌-해결">이름 충돌 해결</h3>
<p>멤버 변수와 매개변수 이름이 같을 때 <code>this</code>로 구분할 수 있습니다.</p>
<pre><code class="language-cpp">void setRadius(int radius) {
    this-&gt;radius = radius;
//  ↑ 멤버변수    ↑ 매개변수
}</code></pre>
<h3 id="this-사용-제약">this 사용 제약</h3>
<ul>
<li>멤버 함수가 아닌 일반 함수에서는 사용 불가합니다.</li>
<li><code>static</code> 멤버 함수에서는 사용 불가합니다.<br />→ <code>static</code>은 객체 없이 호출되므로, <code>this</code>가 가리킬 대상 자체가 없기 때문입니다.</li>
</ul>
<hr />
<h2 id="5-동적-메모리-할당---new--delete">5. 동적 메모리 할당 - new / delete</h2>
<h3 id="정적-할당-vs-동적-할당">정적 할당 vs 동적 할당</h3>
<table>
<thead>
<tr>
<th></th>
<th>정적 할당</th>
<th>동적 할당</th>
</tr>
</thead>
<tbody><tr>
<td>시점</td>
<td>컴파일 타임</td>
<td>런타임</td>
</tr>
<tr>
<td>위치</td>
<td>스택</td>
<td>힙</td>
</tr>
<tr>
<td>크기</td>
<td>고정</td>
<td>실행 중 결정 가능</td>
</tr>
<tr>
<td>해제</td>
<td>자동</td>
<td>수동 (delete)</td>
</tr>
</tbody></table>
<h3 id="new와-delete의-동작">new와 delete의 동작</h3>
<pre><code class="language-cpp">Circle* p = new Circle(radius);
// ① 힙에 Circle 크기만큼 메모리 할당
// ② Circle(int r) 생성자 자동 호출

delete p;
// ① ~Circle() 소멸자 자동 호출
// ② 힙 메모리 반환</code></pre>
<p>C의 <code>malloc/free</code>와 달리, <code>new/delete</code>는 <strong>객체의 생명주기(생성자/소멸자)까지 함께 관리</strong>합니다.</p>
<hr />
<h2 id="6-디버거로-직접-확인해보기">6. 디버거로 직접 확인해보기</h2>
<p>아래 코드를 Visual Studio에서 디버깅하며 메모리 상태를 직접 확인해보았습니다.</p>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;

int main() {
    int* p;
    p = new int;
    if (!p) {
        cout &lt;&lt; &quot;메모리를 할당할 수 없습니다.&quot;;
        return 0;
    }

    *p = 5;
    int n = *p;
    cout &lt;&lt; &quot;*p = &quot; &lt;&lt; *p &lt;&lt; '\n';
    cout &lt;&lt; &quot;n = &quot; &lt;&lt; n &lt;&lt; '\n';

    delete p;
}</code></pre>
<h3 id="p--5-이후---p가-가리키는-힙-주소"><code>*p = 5</code> 이후 - p가 가리키는 힙 주소</h3>
<p>메모리 창에서 <code>p</code>를 검색하면 <code>p</code>가 가리키는 힙 주소로 이동합니다.<br />해당 주소에 <code>05 00 00 00</code> (little-endian으로 5)이 저장된 것을 확인할 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/88400dde-57d6-439f-bc76-5fa9bf0f0d33/image.png" /></p>
<h3 id="p---p-변수-자체의-스택-주소"><code>&amp;p</code> - p 변수 자체의 스택 주소</h3>
<p><code>&amp;p</code>를 검색하면 포인터 변수 <code>p</code>가 저장된 스택 영역으로 이동합니다.<br />여기에는 힙의 주소값 자체가 담겨 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bf6d7373-1e97-44b9-b42b-d917fad5a3f1/image.png" /></p>
<h3 id="n--p---역참조로-값-복사"><code>n = *p</code> - 역참조로 값 복사</h3>
<pre><code class="language-cpp">int n = *p;  // p가 가리키는 값(5)을 n에 복사</code></pre>
<p><code>n</code>은 포인터가 아닌 일반 int 변수이므로, 힙이 아닌 스택에 저장됩니다.<br /><code>*p</code>와 <code>n</code>은 같은 값(5)을 가지지만, 서로 다른 메모리 공간에 존재합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1d2b58ce-8d95-4a0c-b80c-f08083236d71/image.png" /></p>
<h3 id="delete-p-이후---p의-변화-msvc-디버그-모드"><code>delete p</code> 이후 - p의 변화 (MSVC 디버그 모드)</h3>
<p><code>delete p</code> 이후 <code>p</code>를 메모리 창에서 검색하면 전혀 다른 결과가 나옵니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/38ea60b9-c386-4f8e-bba2-2164dee4da0e/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/732343f9-8c64-4538-a22c-dec2360685b5/image.png" /></p>
<p>MSVC 디버그 모드는 <code>delete</code> 후 포인터 변수를 <strong>의도적으로 무효한 주소로 변경</strong>합니다.  </p>
<p><code>??</code>는 해당 주소의 메모리를 읽을 수 없다는 표시입니다.<br />이는 C++ 표준 동작이 아니라, <strong>Dangling Pointer 버그를 즉시 크래시로 잡아내기 위한 MSVC 디버그 빌드의 친절한 기능</strong>입니다.</p>
<blockquote>
<p>릴리즈 빌드나 GCC/Clang에서는 이런 동작을 해주지 않습니다.<br />그래서 <code>delete</code> 후에는 직접 <code>p = nullptr</code>로 명시적으로 무효화하는 습관이 중요합니다.</p>
</blockquote>
<hr />
<h2 id="7-delete를-반드시-해야-하는-이유">7. delete를 반드시 해야 하는 이유</h2>
<h3 id="new는-빈-공간에만-할당한다">new는 빈 공간에만 할당한다</h3>
<pre><code class="language-cpp">Circle* p = new Circle(10);  // 힙의 공간 A 점유
p = new Circle(20);          // 힙의 공간 B 점유 (A는 그대로 잠겨있음)
p = new Circle(30);          // 힙의 공간 C 점유 (A, B 그대로 잠겨있음)</code></pre>
<p><code>new</code>는 매번 <strong>새로운 공간을 따로 할당</strong>하는 것이지, 기존 공간을 덮어쓰는 것이 아닙니다.<br /><code>delete</code> 없이 <code>p</code>를 다른 주소로 바꾸는 순간, <strong>공간 A의 주소를 영영 잃어버리게 됩니다.</strong></p>
<pre><code>힙 메모리
[공간 A: Circle(10)] ← 아무도 가리키지 않음, 해제도 안됨
[공간 B: Circle(20)] ← 아무도 가리키지 않음, 해제도 안됨
[공간 C: Circle(30)] ← p가 가리킴
[      남은 공간    ] ← 점점 줄어듦</code></pre><p>이렇게 접근할 방법을 잃은 메모리가 누적되는 현상을 <strong>메모리 릭(Memory Leak)</strong> 이라고 합니다.</p>
<h3 id="배열은-반드시-delete">배열은 반드시 <code>delete[]</code></h3>
<pre><code class="language-cpp">int* p = new int[n];
delete[] p;   // ✅ 배열 전체 해제
delete p;     // ❌ 첫 번째 원소만 해제, 나머지는 메모리 릭</code></pre>
<p>객체 배열이라면 <code>delete</code>와 <code>delete[]</code>의 차이가 더욱 치명적입니다.</p>
<pre><code class="language-cpp">Circle* arr = new Circle[3];
delete arr;    // ❌ ~Circle() 1번만 호출
delete[] arr;  // ✅ ~Circle() 3번 모두 호출</code></pre>
<hr />
<h2 id="8-raii-패턴---객체가-자원을-스스로-관리">8. RAII 패턴 - 객체가 자원을 스스로 관리</h2>
<pre><code class="language-cpp">class CircleManager {
    Circle* pArray = NULL;
public:
    CircleManager() {
        pArray = new Circle[size];  // 생성자에서 할당
    }
    ~CircleManager() {
        if (pArray != NULL) delete[] pArray;  // 소멸자에서 해제
    }
};</code></pre>
<p><strong>생성자에서 할당, 소멸자에서 해제</strong>가 짝을 이루는 이 패턴을 RAII라고 합니다.<br /><code>delete pMan</code> 하나로 연쇄적으로 정리되는 구조입니다.</p>
<pre><code>delete pMan
  → ~CircleManager() 호출
    → delete[] pArray
      → ~Circle() size번 호출</code></pre>