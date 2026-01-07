<h2 id="11-1-아스키-코드-값과-문자-입출력-함수">11-1 아스키 코드 값과 문자 입출력 함수</h2>
<h3 id="아스키-코드">아스키 코드</h3>
<p>128개의 문자에 대해 서로 다른 값을 정해놓은 약속</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2cf211f5-5401-4697-af87-8110e50ecde3/image.png" /></p>
<h3 id="특징">특징</h3>
<ul>
<li><p>알파벳과 숫자는 각각 연속된 아스키 코드 값을 갖는다.</p>
</li>
<li><p>소문자가 대문자보다 아스키 코드 값이 크다.</p>
</li>
<li><p>제어 문자는 백슬래시와 함께 표시하며 출력할 때 그 기능을 수행한다.</p>
</li>
<li><p>11-1.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      char small, cap = 'G';                   // char형 변수 선언과 초기화

      if ((cap &gt;= 'A') &amp;&amp; (cap &lt;= 'Z'))       // 대문자 범위라면
      {
          small = cap + ('a' - 'A');          // 대/소문자의 차이를 더해 소문자로 변환
      }
      printf(&quot;대문자 : %c %c&quot;, cap, '\n');    // '\n'를 %c로 출력하면 줄이 바뀐다.
      printf(&quot;소문자 : %c&quot;, small);

      return 0;
  }</code></pre>
<pre><code class="language-c">  대문자 : G 
  소문자 : g</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/2e60c59d-d59f-436a-a8cb-e3c32ab1bfff/image.png" /></p>
<h3 id="scanf-함수를-사용한-문자-입력">scanf 함수를 사용한 문자 입력</h3>
<ul>
<li><p>11-2.c</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      char ch1, ch2;

      scanf(&quot;%c%c&quot;, &amp;ch1, &amp;ch2);     // 2개의 문자를 연속 입력
      printf(&quot;[%c%c]&quot;, ch1, ch2);    // 입력된 문자 출력

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/af8e29b0-177a-4876-b8e6-355b2d3bca62/image.png" /></p>
<ul>
<li>%c 변환문자는 공백, 탭, 개행문자를 입력한다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/e994d31a-4dca-41c0-9e46-2762de624189/image.png" /></p>
<ul>
<li>공백, 탭, 개행문자를 제외하고 입력할 때는 %c 앞에 공백, 탭, 개행문자 중 하나 이상을 추가한다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/40f0877b-dd88-453f-92c2-dd2d73089b7a/image.png" /></p>
<h3 id="getchar-함수와-putchar-함수">getchar 함수와 putchar 함수</h3>
<p>예제</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;

int main(void)
{
    int ch;                    // 입력 문자를 저장할 변수

    ch = getchar();            // 함수가 반환하는 문자를 바로 저장
    printf(&quot;입력한 문자 : &quot;);
    putchar(ch);               // 입력한 문자 출력
    putchar('\n');             // 개행 문자 출력

    return 0;
}</code></pre>
<pre><code class="language-c">입력한 문자 : a</code></pre>
<h3 id="키워드로-끝내는-핵심-포인트">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>모든 문자 상수는 아스키 코드 값으로 바뀌어 숫자로 저장되고 연산된다.</li>
<li>%c 변환 문자는 화이트 스페이스(공백 문자, 탭 문자, 개행 문자)도 입력하며, %c 앞에 공백을 사용하면 화이트 스페이스를 입력    에서 제외할 수 있다.</li>
<li>getchar, putchar 함수는 문자 전용 입출력 함수이다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/608e87ad-e675-4367-83bd-8e930b165f02/image.png" /></p>
<h2 id="11-2-버퍼를-사용하는-입력-함수">11-2 버퍼를 사용하는 입력 함수</h2>
<h3 id="scanf-함수가-문자를-입력하는-과정">scanf 함수가 문자를 입력하는 과정</h3>
<ul>
<li><p>11-4.c</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      char ch;
      int i;

      for (i = 0; i &lt; 3; i++)        // 3번 반복
      {
          scanf(&quot;%c&quot;, &amp;ch);        // 문자 입력
          printf(&quot;%c&quot;, ch);        // 입력된 문자 출력
      }

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/452d0c92-9916-4bf6-ad55-fe3118b2a472/image.png" /></p>
<h3 id="scanf-함수의-반환값-활용">scanf 함수의 반환값 활용</h3>
<ul>
<li><p>11-5.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int res;
      char ch;

      while(1)
      {
          res=scanf(&quot;%c&quot;, &amp;ch);
          if(res==-1) break;  //윈도우 ctrl+z , 리눅스, 유닉스에서는 ctrl+D
          printf(&quot;%d&quot;, ch);

      }
      return 0;
  }</code></pre>
<ul>
<li><input disabled="" type="checkbox" /> A
6510
B
6610
a
9710</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/0a90016c-e45e-4a1b-af92-d42e27d57bd1/image.png" /></p>
<h3 id="getchar-함수를-사용한-문자열-입력">getchar 함수를 사용한 문자열 입력</h3>
<ul>
<li><p>11-6.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void my_gets(char* str, int size);

  int main(void)
  {
      char str[7];                             // 문자열을 저장할 배열

      my_gets(str, sizeof(str));               // 한 줄의 문자열을 입력하는 함수
      printf(&quot;입력한 문자열 : %s\n&quot;, str);     // 입력한 문자열 출력

      return 0;
  }

  void my_gets(char* str, int size)            // str은 char 배열, size는 배열의 크기
  {
      int ch;                                  // getchar 함수의 반환값을 저장할 변수
      int i = 0;                               // str 배열의 첨자

      ch = getchar();                          // 첫 번째 문자 입력
      while ((ch != '\n') &amp;&amp; (i &lt; size - 1))   // 배열의 크기만큼 입력
      {
          str[i] = ch;             // 입력한 문자를 배열에 저장
          i++;                     // 첨자 증가
          ch = getchar();          // 새로운 문자 입력
      }
      str[i] = '\0';               // 입력된 문자열의 끝에 널 문자를 저장
  }</code></pre>
</li>
</ul>
<h3 id="입력-버퍼-지우기">입력 버퍼 지우기</h3>
<ul>
<li><p>11-7.c</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      int num, grade;           // 학번과 학점을 저장할 변수

      printf(&quot;학번 입력 : &quot;);
      scanf(&quot;%d&quot;, &amp;num);        // 학번 입력
      getchar();                // 버퍼에 남아 있는 개행 문자 제거
      printf(&quot;학점 입력 : &quot;);
      grade = getchar();        // 학점 입력
      printf(&quot;학번 : %d, 학점 : %c&quot;, num, grade);

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/7108f0df-fd04-445c-a1ba-c1b84c256dd9/image.png" /></p>
<ul>
<li>scanf 와 getchar차이 어느것이 좋나?</li>
</ul>
<hr />
<h3 id="키워드로-끝내는-핵심-포인트-1">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>scanf 함수는 입력할 때 가장 먼저 버퍼의 상태를 확인한다.</li>
<li>버퍼에 저장되는 데이터의 끝에는 항상 개행 문자가 있다.</li>
<li>scanf 함수는 Ctrl + Z 를 누르면 EOF(-1)를 반환한다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트-1">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/df7d2e23-a327-4c9b-90eb-a37bf567e5d4/image.png" /></p>