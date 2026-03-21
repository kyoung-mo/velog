<h2 id="cin이란">cin이란?</h2>
<p><code>cin</code>은 키보드 입력을 받는 <strong>표준 입력 스트림</strong>입니다.</p>
<p>키보드로 입력을 하면 일단 <strong>cin 내부 버퍼</strong>에 데이터가 쌓이고, <code>&gt;&gt;</code> 연산자가 호출될 때 버퍼에서 꺼내서 변수에 저장하는 방식으로 동작하는 것 같습니다.</p>
<pre><code class="language-cpp">cin &gt;&gt; width;</code></pre>
<p>예를 들어 <code>123 엔터</code>를 입력하면 내부적으로 이렇게 동작합니다.</p>
<pre><code>키보드 입력: 123\n
      ↓
cin 내부 버퍼: [ 1 | 2 | 3 | \n ]
      ↓
cin &gt;&gt; width 실행
      ↓
버퍼: [ \n ]  ← \n은 버퍼에 남음
width: 123</code></pre><p>주의할 점은 <code>cin &gt;&gt;</code>은 <code>\n</code>을 변수에 저장하지 않고 버퍼에 남겨둔다는 점입니다. 이후에 <code>getline()</code>과 섞어 쓸 때 문제가 생길 수 있습니다.</p>
<hr />
<h2 id="cin-내부-버퍼의-크기">cin 내부 버퍼의 크기</h2>
<p><code>cin</code> 내부 버퍼는 <strong>힙(Heap)</strong> 영역에 할당됩니다. 힙은 동적 메모리 할당 영역으로, 스택보다 훨씬 큰 가용 메모리를 사용할 수 있습니다.</p>
<table>
<thead>
<tr>
<th>영역</th>
<th>크기</th>
</tr>
</thead>
<tbody><tr>
<td>스택</td>
<td>1~8MB (고정)</td>
</tr>
<tr>
<td>힙</td>
<td>수 GB (가용 RAM 한도)</td>
</tr>
</tbody></table>
<p>따라서 cin 내부 버퍼는 스택보다 훨씬 클 수 있습니다.</p>
<h3 id="예제-코드">예제 코드</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
#include &lt;cstring&gt;
using namespace std;

int main() {
    char password[11];
    cout &lt;&lt; &quot;프로그램을 종료하려면 암호를 입력하세요.&quot; &lt;&lt; endl;
    while(true) {
        cout &lt;&lt; &quot;암호&gt;&gt;&quot;;
        cin &gt;&gt; password;
        if(strcmp(password, &quot;C++&quot;) == 0) {
            cout &lt;&lt; &quot;프로그램을 정상 종료합니다.&quot; &lt;&lt; endl;
            break;
        }
        else 
            cout &lt;&lt; &quot;암호가 틀립니다~~&quot; &lt;&lt; endl;
    }
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a9100445-1a67-4e64-af9a-ee0380c70061/image.png" /></p>
<hr />
<h2 id="cingetline">cin.getline()</h2>
<p><code>cin &gt;&gt;</code>의 경우 길이 제한 없이 변수에 데이터를 쓰려 하기 때문에 버퍼 오버플로우가 발생할 수 있습니다. 이를 방지하기 위해 <code>cin.getline()</code>을 사용하는 것이 좋습니다.</p>
<pre><code class="language-cpp">cin.getline(address, 100, '\n');
//          buf      size  구분자</code></pre>
<p>동작 순서는 다음과 같습니다.</p>
<pre><code>cin 내부 버퍼: [ h | e | l | l | o | \n ]
                                      ↑
                            \n 발견 → 버퍼에서 제거하고 버림

address:      [ h | e | l | l | o | \0 ]
                                      ↑
                            읽은 문자열 끝에 \0 자동으로 붙여줌</code></pre><ul>
<li>최대 <code>size - 1</code>개의 문자만 읽고 나머지는 버립니다.</li>
<li>구분자(<code>\n</code>)를 만나면 읽기를 멈추고, 해당 문자는 버퍼에서 제거합니다.</li>
<li>문자열 끝에 null terminator(<code>\0</code>)를 자동으로 붙여줍니다.</li>
</ul>
<h3 id="예제-코드-1">예제 코드</h3>
<pre><code class="language-c">#include &lt;iostream&gt;
using namespace std;

int main() {
    cout &lt;&lt; &quot;주소를 입력하세요&gt;&gt;&quot;;

    char address[100]; 
    cin.getline(address, 100, '\n'); // 키보드로부터 주소 읽기

    cout &lt;&lt; &quot;주소는 &quot; &lt;&lt; address &lt;&lt; &quot;입니다\n&quot;; // 주소 출력
}</code></pre>
<p>cin의 내부 버퍼에는 입력한 
<code>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC</code>
값이 힙 영역에 저장됩니다. 데이터가 저장될떄 마지막의 <code>\0</code> 문자를 만나면 자동으로 가 앞의 데이터까지 저장을 합니다.</p>
<p>그리고 <code>getline(address, 100, \n)</code>에서 address 버퍼에 100-1 사이즈만큼 데이터를 가져오고, 데이터 마지막에는 <code>\n</code>을 붙이기 때문에 결과 값으로 아래 내용이 출력됩니다.</p>
<p><code>주소는 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA입니다</code></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b92f2756-b4e6-4844-9711-03facd2ba926/image.png" /></p>
<h3 id="정리--cin---cingetline-비교">정리 : cin &gt;&gt; , cin.getline() 비교</h3>
<table>
<thead>
<tr>
<th></th>
<th><code>cin &gt;&gt;</code></th>
<th><code>cin.getline()</code></th>
</tr>
</thead>
<tbody><tr>
<td><code>\n</code> 처리</td>
<td>버퍼에 남김</td>
<td>버퍼에서 제거하고 버림</td>
</tr>
<tr>
<td>공백 처리</td>
<td>공백 기준으로 끊음</td>
<td>공백도 그냥 읽음</td>
</tr>
<tr>
<td>크기 제한</td>
<td>❌</td>
<td>✅ size-1</td>
</tr>
</tbody></table>
<hr />
<h2 id="cout과--연산자">cout과 &lt;&lt; 연산자</h2>
<p><code>cout</code>은 표준 출력 스트림입니다. <code>&lt;&lt;</code> 뒤에는 다양한 값이 올 수 있습니다.</p>
<pre><code class="language-cpp">cout &lt;&lt; 42;            // 정수 리터럴
cout &lt;&lt; 3.14;          // 실수 리터럴
cout &lt;&lt; &quot;문자열&quot;;       // 문자열
cout &lt;&lt; width;         // 변수
cout &lt;&lt; width * height; // 수식
cout &lt;&lt; sqrt(16);      // 함수 반환값
cout &lt;&lt; (a &gt; b ? &quot;크다&quot; : &quot;작다&quot;); // 조건 연산자</code></pre>
<h3 id="연속-출력-체이닝">연속 출력 (체이닝)</h3>
<pre><code class="language-cpp">cout &lt;&lt; &quot;너비: &quot; &lt;&lt; width &lt;&lt; &quot;, 높이: &quot; &lt;&lt; height;</code></pre>
<p><code>&lt;&lt;</code> 연산자는 실행 후 <strong>cout 자신을 반환</strong>합니다. 덕분에 위처럼 <code>&lt;&lt;</code>를 체인처럼 연결할 수 있는 것 같습니다.</p>
<p>내부적으로는 아래와 동일하게 동작합니다.</p>
<pre><code class="language-cpp">cout &lt;&lt; &quot;너비: &quot;;
cout &lt;&lt; width;
cout &lt;&lt; &quot;, 높이: &quot;;
cout &lt;&lt; height;</code></pre>
<p>왼쪽에서 오른쪽 순서로 하나씩 실행되는 방식입니다.</p>