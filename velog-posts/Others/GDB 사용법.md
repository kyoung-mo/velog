<h2 id="1-디버깅-환경">1. 디버깅 환경</h2>
<ul>
<li>OS: Ubuntu (x86_64)</li>
<li>Compiler: gcc</li>
<li>Debugger: GNU gdb 15.x</li>
<li>컴파일 옵션:</li>
</ul>
<pre><code class="language-bash">gcc -g -O0 -o hello_d hello.c</code></pre>
<ul>
<li><code>-g</code>: 디버그 심볼 포함</li>
<li><code>-O0</code>: 최적화 비활성화 (디버깅 정확도 향상)</li>
</ul>
<hr />
<h2 id="2-gdb-실행-및-main-진입">2. GDB 실행 및 main 진입</h2>
<pre><code class="language-gdb">gdb ./hello_d
(gdb) start</code></pre>
<p>출력:</p>
<pre><code class="language-text">Temporary breakpoint 1, main () at hello.c:4
4    int a = 10;</code></pre>
<ul>
<li><code>start</code> 명령은 <code>main()</code> 진입 직후에서 멈춘다.</li>
<li>이 시점에서는 아직 해당 라인의 코드가 <strong>실행되지 않았다</strong>.</li>
</ul>
<hr />
<h2 id="3-지역-변수와-초기화-시점">3. 지역 변수와 초기화 시점</h2>
<h3 id="31-초기화-전-변수-값-쓰레기-값">3.1 초기화 전 변수 값 (쓰레기 값)</h3>
<pre><code class="language-gdb">(gdb) p a
$1 = -8160</code></pre>
<ul>
<li><code>int a = 10;</code> 라인이 <strong>아직 실행되지 않았기 때문</strong></li>
<li>스택 메모리에 할당만 되었고 값은 초기화되지 않음</li>
</ul>
<h3 id="32-next-실행-후">3.2 next 실행 후</h3>
<pre><code class="language-gdb">(gdb) next
(gdb) p a
$2 = 10</code></pre>
<ul>
<li><code>next</code> 실행으로 해당 라인이 수행됨</li>
<li>정상적인 초기값 확인 가능</li>
</ul>
<hr />
<h2 id="4-콤마-연산자-주의-p-b-c">4. 콤마 연산자 주의 (<code>p b, c</code>)</h2>
<pre><code class="language-gdb">(gdb) p b, c
$3 = -8088</code></pre>
<p>이는 다음과 동일한 의미이다:</p>
<pre><code class="language-c">(b, c)</code></pre>
<ul>
<li><code>b</code>는 평가만 되고</li>
<li><strong>출력 결과는 <code>c</code></strong></li>
<li><code>c</code>는 아직 초기화되지 않아 쓰레기 값 출력</li>
</ul>
<p>정확한 확인 방법:</p>
<pre><code class="language-gdb">p b
p c</code></pre>
<hr />
<h2 id="5-char--float-변수도-동일한-원리">5. char / float 변수도 동일한 원리</h2>
<h3 id="char-변수">char 변수</h3>
<pre><code class="language-gdb">(gdb) p d
$4 = 0 '\0'</code></pre>
<pre><code class="language-gdb">(gdb) next
(gdb) p d
$5 = 97 'a'</code></pre>
<h3 id="float-변수">float 변수</h3>
<pre><code class="language-gdb">(gdb) p e
$6 = 4.59e-41   // 초기화 전</code></pre>
<pre><code class="language-gdb">(gdb) next
(gdb) p e
$7 = 3.14159012</code></pre>
<ul>
<li>모든 지역 변수는 <strong>실행되기 전까지는 값이 보장되지 않음</strong></li>
</ul>
<hr />
<h2 id="6-스택-메모리-주소-배치">6. 스택 메모리 주소 배치</h2>
<pre><code class="language-gdb">&amp;a = 0x7fffffffdf30
&amp;b = 0x7fffffffdf34
&amp;c = 0x7fffffffdf38
&amp;d = 0x7fffffffdf2f
&amp;e = 0x7fffffffdf3c</code></pre>
<table>
<thead>
<tr>
<th>변수</th>
<th>타입</th>
<th>크기</th>
<th>주소 예시</th>
</tr>
</thead>
<tbody><tr>
<td>d</td>
<td>char</td>
<td>1B</td>
<td>df2f</td>
</tr>
<tr>
<td>a</td>
<td>int</td>
<td>4B</td>
<td>df30</td>
</tr>
<tr>
<td>b</td>
<td>int</td>
<td>4B</td>
<td>df34</td>
</tr>
<tr>
<td>c</td>
<td>int</td>
<td>4B</td>
<td>df38</td>
</tr>
<tr>
<td>e</td>
<td>float</td>
<td>4B</td>
<td>df3c</td>
</tr>
</tbody></table>
<ul>
<li>스택은 <strong>주소 감소 방향</strong>으로 성장</li>
<li>정렬(alignment) 규칙에 따라 배치됨</li>
</ul>
<hr />
<h2 id="7-libc-관련-경고-메시지">7. libc 관련 경고 메시지</h2>
<pre><code class="language-text">__libc_start_call_main ...
No such file or directory</code></pre>
<ul>
<li>프로그램 종료 이후 libc 내부 코드 진입</li>
<li>glibc 소스가 로컬에 없어서 발생하는 경고</li>
<li><strong>디버깅 대상 아님</strong></li>
<li>무시해도 무방</li>
</ul>
<hr />
<h2 id="8-정리">8. 정리</h2>
<ul>
<li><code>start</code>는 main 진입 시점에서 멈춘다</li>
<li>지역 변수는 <strong>실행 전에는 쓰레기 값</strong></li>
<li><code>next</code>는 한 줄 실행</li>
<li>GDB의 <code>p</code>는 C 문법을 그대로 따른다</li>
<li>스택 주소를 통해 메모리 구조를 직관적으로 확인 가능</li>
</ul>
<hr />