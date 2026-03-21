<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/48ff2480-f24d-4405-88b6-44ad54be082c/image.png" /></p>
<p>C++에서 추가된 개념을 본격적으로 들어가기 시작했습니다. 학부생때 Java 기초 수업을 들었어서 그런지 어딘가 익숙한거 같기도 하고... 아직 #include &lt;stdio.h&gt;를 자동으로 쓰게 되서 적응 하려면 강의자료 코드 여러번 타이핑 해봐야겠습니다.</p>
<hr />
<h2 id="객체object란">객체(Object)란?</h2>
<p>C++에서 핵심 개념은 <strong>객체</strong>입니다. C언어의 구조체와 비슷한 느낌이라고 볼 수 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/28f5d7bf-ae5a-46e7-bac5-ac5c5dc103ba/image.png" /></p>
<p>객체는 <strong>상태(state)</strong> 와 <strong>행동(behavior)</strong> 으로 구성됩니다.</p>
<ul>
<li><strong>상태</strong> → 변수 값과 비슷한 개념 (멤버 변수)</li>
<li><strong>행동</strong> → 함수와 비슷한 개념 (멤버 함수)</li>
</ul>
<hr />
<h2 id="클래스class란">클래스(Class)란?</h2>
<p>클래스는 객체가 아닙니다. <strong>객체 생성을 위해 정의된 설계도, 틀</strong>이라고 볼 수 있습니다.</p>
<p>클래스 자체는 실체가 아니며, 멤버 변수와 멤버 함수를 선언하는 역할을 합니다.</p>
<pre><code class="language-cpp">class TV {
    bool on;        // 1바이트
    int channel;    // 4바이트   // 멤버 변수
    int volume;     // 4바이트
public:
    void powerOn() { ... }      // 멤버 함수
    void powerOff() { ... }
    void increaseChannel() { ... }
    void decreaseChannel() { ... }
    void increaseVolume() { ... }
    void decreaseVolume() { ... }
};
// 함수 호출 시에는 [객체].[함수] 형태로 호출</code></pre>
<hr />
<h2 id="객체-생성">객체 생성</h2>
<p>객체는 클래스의 모양을 그대로 가지고 탄생합니다. 메모리에 생성되며 <strong>실체(instance)</strong> 라고도 부릅니다.</p>
<p>하나의 클래스 틀에서 여러 개의 객체를 찍어낼 수 있으며, 각 객체는 서로 별도의 공간에 생성됩니다.</p>
<hr />
<h2 id="메모리-구조">메모리 구조</h2>
<p>클래스와 객체는 메모리에서 다음과 같이 저장됩니다.</p>
<table>
<thead>
<tr>
<th>영역</th>
<th>저장 내용</th>
</tr>
</thead>
<tbody><tr>
<td><code>.text</code></td>
<td>클래스 관련 코드 (멤버 함수)</td>
</tr>
<tr>
<td><code>stack</code></td>
<td>각 객체의 멤버 변수 값</td>
</tr>
</tbody></table>
<p>멤버 함수는 코드 영역에 한 번만 올라가고, 멤버 변수는 객체마다 따로 스택에 생성됩니다.</p>
<hr />
<h2 id="클래스-선언부--구현부">클래스 선언부 / 구현부</h2>
<p>클래스 작성은 <strong>선언부</strong>와 <strong>구현부</strong>로 나뉩니다.</p>
<pre><code class="language-cpp">// 선언부
class Circle {
public:
    int radius;
    double getArea();
};

// 구현부
double Circle::getArea() {
    return 3.14 * radius * radius;
}</code></pre>
<p><code>public</code>을 <code>private</code>으로 수정하면 구현부(<code>Circle::getArea()</code>)에서는 문제없이 접근 가능하지만, <code>main()</code> 함수 내에서는 접근이 불가능하여 컴파일 에러가 발생합니다.</p>
<hr />
<h2 id="생성자constructor">생성자(Constructor)</h2>
<p>생성자는 객체가 생성될 때 <strong>초기값을 지정</strong>하기 위해 사용합니다.</p>
<p>생성자의 특징은 다음과 같습니다.</p>
<ul>
<li>리턴 타입이 없습니다.</li>
<li>클래스 이름과 생성자 이름이 동일합니다.</li>
<li><strong>매개변수 없는 생성자(기본 생성자)</strong> → 선언하지 않으면 컴파일러가 자동으로 생성</li>
<li><strong>매개변수를 가진 생성자</strong> → 직접 선언해야 합니다.</li>
</ul>
<pre><code class="language-cpp">Circle::Circle() {
    radius = 1;
    cout &lt;&lt; &quot;반지름 &quot; &lt;&lt; radius &lt;&lt; &quot; 원 생성&quot; &lt;&lt; endl;
}

Circle::Circle(int r) {
    radius = r;
    cout &lt;&lt; &quot;반지름 &quot; &lt;&lt; radius &lt;&lt; &quot; 원 생성&quot; &lt;&lt; endl;
}</code></pre>
<hr />
<h2 id="위임-생성자-delegating-constructor">위임 생성자 (Delegating Constructor)</h2>
<p>코드의 중복을 줄이기 위해 사용하는 생성자입니다. 한 생성자가 다른 생성자를 호출해서 초기화를 위임하는 방식입니다.</p>
<p><strong>위임 생성자 없이 작성한 경우:</strong></p>
<pre><code class="language-cpp">Circle::Circle() {
    radius = 1;
    cout &lt;&lt; &quot;반지름 &quot; &lt;&lt; radius &lt;&lt; &quot; 원 생성&quot; &lt;&lt; endl;
}

Circle::Circle(int r) {
    radius = r;
    cout &lt;&lt; &quot;반지름 &quot; &lt;&lt; radius &lt;&lt; &quot; 원 생성&quot; &lt;&lt; endl;
}</code></pre>
<p><strong>위임 생성자를 사용한 경우:</strong></p>
<pre><code class="language-cpp">Circle::Circle() : Circle(1) { }  // 위임 생성자 → Circle(int r) 호출

Circle::Circle(int r) {            // 타겟 생성자 → 실제 초기화 수행
    radius = r;
    cout &lt;&lt; &quot;반지름 &quot; &lt;&lt; radius &lt;&lt; &quot; 원 생성&quot; &lt;&lt; endl;
}</code></pre>
<ul>
<li><strong>위임 생성자</strong> → 초기화를 다른 생성자에게 맡기는 생성자</li>
<li><strong>타겟 생성자</strong> → 실제 초기화 작업을 수행하는 생성자</li>
</ul>
<p>중복되는 초기화 코드를 타겟 생성자 한 곳에서 관리할 수 있다는 장점이 있습니다.</p>