<p>간단하게 복습 내용만 정리 하겠습니당</p>
<hr />
<h2 id="1---bash-명령어">1. <code>$?</code> : bash 명령어</h2>
<ul>
<li>명령어의 종료 상태를 나타내는 셸 변수</li>
<li>성공적으로 종료 시 0 반환</li>
<li>터미널에서 <code>echo $?</code> 입력 시 확인 가능하다.</li>
</ul>
<hr />
<h2 id="2-fgets-vs-gets">2. fgets vs gets</h2>
<p><strong>1.fgets</strong></p>
<pre><code class="language-c">char* fgets(char* buf, int n, FILE* stream);</code></pre>
<p><code>h</code> <code>e</code> <code>l</code> <code>l</code> <code>o</code> <code>↵(\n)</code> <code>\0</code> 에서 <code>\0</code> 까지 읽음.
따라서 <code>↵</code> 문자가 포함되어서 들어간다.</p>
<p>따라서 순수하게 문자열만 보내고싶다! 하면
5번 index에 <code>\0(NULL 문자)</code> 넣어주면 된다.</p>
<pre><code class="language-c">buf[strlen(buf) - 1] = '\0';    // \n 을 \0 으로 덮어씀</code></pre>
<ul>
<li><strong>참고) ASCII에서 0 =&gt; <code>\0</code> 널문자</strong></li>
</ul>
<p><strong>2. gets</strong></p>
<pre><code class="language-c">char* gets(char* buf);</code></pre>
<p><code>gets</code>는 버퍼 크기 제한이 없어서 보한 취약점(버퍼 오버 플로우) 때문에 C11에서 표준에서 제거되어, 주로  fgets를 사용한다.</p>
<hr />
<h2 id="3strlen-vs-sizeof">3.strlen vs sizeof</h2>
<p><strong>strlen</strong> : NULL(<code>\0</code>) 포함
<strong>sizeof</strong> : NULL(<code>\0</code>) 제외</p>
<pre><code class="language-c">char buf[] = &quot;hello&quot;;

sizeof(buf)   // 6  → \0 포함
strlen(buf)   // 5  → \0 제외, 순수 문자 개수</code></pre>
<hr />
<h2 id="4-argc--argv">4. argc / argv</h2>
<pre><code class="language-c">int main(int argc, char* argv[]);
int main(int argc, char** argv); // 같은 표현</code></pre>
<p><strong>간단 정리</strong></p>
<table>
<thead>
<tr>
<th>매개변수</th>
<th>의미</th>
</tr>
</thead>
<tbody><tr>
<td><code>argc</code></td>
<td>전달된 인자의 개수(argument count)</td>
</tr>
<tr>
<td><code>argv</code></td>
<td>전달된 인자의 문자열 배열(argument vector)</td>
</tr>
</tbody></table>
<p>예를 들어 아래와 같은 인자를 받아 실행해야 하는 프로그램이 있다고 합시다.</p>
<ul>
<li><code>./file_client</code> <code>127.0.0.1</code> <code>5000</code> <code>file_client.c</code></li>
</ul>
<p>여기서 파일을 실행시키기 위해 필요한 인자의 개수는 <code>./file_client</code> <code>127.0.0.1</code> <code>5000</code> <code>file_client.c</code> 이렇게 4개이므로, <code>argc = 4</code></p>
<p><code>argv[0]</code> : <code>./file_client</code> 를 가리키는 시작 주소
<code>argv[1]</code> : <code>127.0.0.1</code> 를 가리키는 시작 주소
<code>argv[2]</code> : <code>5000</code> 를 가리키는 시작 주소
<code>argv[3]</code> : <code>file_client.c</code> 를 가리키는 시작 주소</p>
<hr />
<p>추가로, <code>atoi()</code> 개념 정리</p>
<pre><code class="language-c">atoi(argv[2]) // &quot;5000&quot; &gt; 5000 (문자열 -&gt; 정수) </code></pre>