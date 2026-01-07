<h2 id="81-배열의-선언과-사용">8.1 배열의 선언과 사용</h2>
<blockquote>
<p>int kor, math, eng, social, science;</p>
</blockquote>
<ul>
<li>따로?</li>
<li>반복문 사용이 불가능</li>
<li>메모리에 연속적으로 저장해 놓고 쪼개서 사용하는 방법 =&gt; <strong>배열</strong></li>
</ul>
<h3 id="배열의-선언">배열의 선언</h3>
<ul>
<li>선언을 통해 저장 공간을 확보.</li>
<li>저장공간의 갯수와 관계없이 이름은 하나만 사용.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2bf304a8-23e2-4ff4-aba3-91b377588d66/image.png" /></p>
<pre><code>- ex8-1.c - 나이를 저장할 배열을 선언하고 사용하는 방법

    ```c
    #define _CRT_SECURE_NO_WARNINGS
    #include &lt;stdio.h&gt;

    int main(void)
    {
        int ary[5];                   // int형 요소 5개의 배열 선언
                                      // ary는 array의 축약어
        ary[0] = 10;                  // 첫 번째 배열 요소에 10 대입
        ary[1] = 20;                  // 두 번째 배열 요소에 20 대입
        ary[2] = ary[0] + ary[1];     // 첫 번째와 두 번째 요소를 더해 세 번째 요소에 저장
        scanf(&quot;%d&quot;, &amp;ary[3]);         // 키보드로 입력받아 네 번째 요소에 저장

        printf(&quot;%d\n&quot;, ary[2]);       // 세 번째 배열 요소 출력
        printf(&quot;%d\n&quot;, ary[3]);
        printf(&quot;%d\n&quot;, ary[4]);       // 마지막 배열 요소는 쓰레기 값

        return 0;
    }

    ```

    ```
    30
    30
    30
    0

    ```</code></pre><ul>
<li>배열요소 element : 배열의 나누어진 조각</li>
<li>첨자 index : 배열명에 붙여서 사용, 0부터 시작</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/4c391f85-c685-4bb1-bc1e-ed647a657a23/image.png" /></p>
<h3 id="배열의-사용">배열의 사용</h3>
<ul>
<li>배열을 선언할 때와 배열요소를 사용할 때 대괄호[]안의 숫자는 의미가 다르다.</li>
<li>선언할 때는 배열 요소의 전체 개수를 표시</li>
<li>사용할 때는 각 요소가 배열에서 몇 번째에 있는지..</li>
<li>배열의 첨자 &quot; 0부터 시작, '최대 배열요소개수 -1' 까지만 사용.</li>
</ul>
<h3 id="배열의-첨자가-사용범위를-벗어난다면">배열의 첨자가 사용범위를 벗어난다면?</h3>
<ul>
<li>컴파일러가 경고 메시지로 알림.</li>
<li>어떤 결과가 나올지는 모름</li>
</ul>
<h3 id="배열-초기화">배열 초기화</h3>
<ul>
<li>최초 할당된 저장공간에는 쓰레기 값이 저장되어 있다.</li>
<li>선언과 동시에 초기화 : 중괄호{ } 사용</li>
<li>배열의 초기화는 선언시 최초 한번만 가능합니다.</li>
</ul>
<blockquote>
<p>int ary1[5]={1,2,3,4,5};</p>
</blockquote>
<h3 id="배열과-반복문">배열과 반복문</h3>
<ul>
<li><p>ex8-2.c 배열과 반복문을 사용한 성적 처리 프로그램</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      int score[5];                   // 다섯 과목의 성적을 입력할 int형 배열 선언
      int i;                          // 반복 제어 변수
      int total = 0;                  // 총점을 누적할 변수
      double avg;                     // 평균을 저장할 변수

      for(i = 0; i &lt; 5; i++)          // i가 0부터 4까지 5번 반복
      {
          scanf(&quot;%d&quot;, &amp;score[i]);     // 각 배열 요소에 성적 입력
      }

      for (i = 0; i &lt; 5; i++)
      {
          total += score[i];          // 성적을 누적하여 총점 계산
      }
      avg = total / 5.0;              // 평균 계산  sizeof(score)/sizeof(int)

      for (i = 0; i &lt; 5; i++)
      {
          printf(&quot;%5d&quot;, score[i]);    // 성적 출력
      }
      printf(&quot;\n&quot;);

      printf(&quot;평균 : %.1lf\n&quot;, avg);  // 평균 출력

      return 0;
  }
</code></pre>
<pre><code>  1
  2
  3
  4
  5
      1    2    3    4    5
  평균 : 3.0
</code></pre></li>
</ul>
<h3 id="sizeof-연산자를-활용한-배열-처리">sizeof 연산자를 활용한 배열 처리</h3>
<blockquote>
<p>sizeof(배열명) / sizeof (배열요소)</p>
</blockquote>
<ul>
<li><p>ex8-3.c sizeof 연산자를 사용한 배열</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      int score[5];
      int i;
      int total = 0;
      double avg;
      int count;                        // 배열 요소의 개수를 저장할 변수

      count = sizeof(score) / sizeof(score[0]);   // 배열 요소의 개수 계산

      for (i = 0; i &lt; count; i++)       // 11행에서 계산한 count만큼 반복
      {
          scanf(&quot;%d&quot;, &amp;score[i]);
      }

      for (i = 0; i &lt; count; i++)       // 11행에서 계산한 count만큼 반복
      {
          total += score[i];
      }
      avg = total / (double)count;      // 총합을 count로 나누어 평균 계산

      for (i = 0; i &lt; count; i++)       // 11행에서 계산한 count만큼 반복
      {
          printf(&quot;%5d&quot;, score[i]);
      }
      printf(&quot;\\n&quot;);

      printf(&quot;평균 : %.1lf\\n&quot;, avg);

      return 0;
  }
</code></pre>
<pre><code>  1
  2
  3
  4
  5
      1    2    3    4    5
  평균 : 3.0
</code></pre><h2 id="8-2-문자를-저장하는-배열">8-2 문자를 저장하는 배열</h2>
<h3 id="char형-배열의-선언과-초기화">char형 배열의 선언과 초기화</h3>
</li>
<li><p>저장할 문자열의 길이보다 최소한 하나이상 크게 배열을 선언</p>
</li>
<li><p>널문자(null)를 저장할 공간이 있어야 한다.</p>
</li>
<li><p>8-4.c 문자열을 저장하는 char형 배열</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      char str[80] = &quot;applejam&quot;;              // 문자열 초기화

      printf(&quot;최초 문자열 : %s\n&quot;, str);     // 초기화 문자열 출력
      printf(&quot;문자열 입력 : &quot;);
      scanf(&quot;%s&quot;, str);                       // 새로운 문자열 입력
      printf(&quot;입력 후 문자열 : %s\n&quot;, str);   // 입력된 문자열 출력

      return 0;
  }
</code></pre>
<pre><code>  최초 문자열 : applejam
  문자열 입력 : hig
  입력 후 문자열 : hig
</code></pre></li>
</ul>
<h3 id="2가지-초기화-방법">2가지 초기화 방법</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/761e487f-547c-4b62-a618-0f8d0608c9e0/image.png" /></p>
<h3 id="널-문자의-용도">널 문자의 용도</h3>
<ul>
<li>남는 배열 요소에는 자동으로 0으로 채워짐</li>
<li>char형 배열에 저장된 0을 <strong>널문자</strong> null character</li>
<li>아스키 코드 값이 0인 문자는 문자열의 끝을 표시하는 용도로 사용</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/598f760a-463d-46b2-88fe-75176e1b5f4d/image.png" /></p>
<h3 id="char형-배열-선언-시-초기화하지-않은-경우">char형 배열 선언 시 초기화하지 않은 경우</h3>
<ul>
<li>초기화 하지 않고 배열 요소에 문자를 직접 대입하면 문제가 됨.</li>
<li>아래 코드는 무한 실행됨.</li>
<li>마지막 문자 다음에 널문자를 대입해야 무한 실행되지 않는다.</li>
</ul>
<pre><code class="language-c">#define _CRT_SECURE_NO_WARNINGS
#include &lt;stdio.h&gt;

int main(void)
{
    char str[80];

    str[0]='h';
    str[1]='i';
    printf(&quot;문자열 : %s\n&quot;, str);

    return 0;
}
</code></pre>
<h3 id="char형-배열-선언-시-주의할-점">char형 배열 선언 시 주의할 점</h3>
<blockquote>
<p>배열의 크기는 최대한 넉넉하게 선언
배열 요소의 개수는 최소한 '문자열 길이 +1' 이상</p>
</blockquote>
<h3 id="문자열-대입">문자열 대입</h3>
<ul>
<li><p>문자열의 길이가 다를 수 있으므로 일반 변수처럼 대입연산자를 사용할 수 없다.</p>
</li>
<li><p>strcpy함수를 사용</p>
</li>
<li><p>리눅스에서는 #include &lt;string.h&gt; 안써도 사용 가능함.</p>
</li>
<li><p>8-5.c - 문자열을 대입하는 strcpy함수</p>
<pre><code class="language-c">  //#define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;
  //#include &lt;string.h&gt;            // 문자열 관련 함수 원형을 모아놓은 헤더 파일

  int main(void)
  {
      char str1[80] = &quot;cat&quot;;
      char str2[80];

      strcpy(str1, &quot;tiger&quot;);     // str1 배열에 &quot;tiger&quot; 복사
      strcpy(str2, str1);        // str2 배열에 str1 배열의 문자열 복사
      printf(&quot;%s, %s\n&quot;, str1, str2);

      return 0;
  }
</code></pre>
<pre><code>  tiger, tiger
</code></pre></li>
</ul>
<h3 id="strcpy함수로-문자열-상수를-char형-배열에-대입">strcpy함수로 문자열 상수를 char형 배열에 대입</h3>
<ul>
<li>char형 배열에 저장된 문자열을 다른 char형 배열에 대입</li>
</ul>
<h3 id="배열에-대입-연산자는-왜-사용할-수-없을까">배열에 대입 연산자는 왜 사용할 수 없을까?</h3>
<ul>
<li>대입연산자 왼쪽에 사용한 배열명이 컴파일 과정에서 배열이 할당된 메모리의 주소 값으로 바뀌기 때문입니다.</li>
</ul>
<hr />
<h3 id="문자열-전용-입출력-함수--gets-puts">문자열 전용 입출력 함수 : gets, puts</h3>
<ul>
<li><p>gets함수 : 빈칸을 포함하여 한 줄 전체를 문자열로 입력</p>
</li>
<li><p>puts함수 : 문자열 상수나 char형 배열의 배열명을 주면 문자열을 화면에 출력합니다.</p>
</li>
<li><p><input disabled="" type="checkbox" />  빈칸을 포함한 문자열 입력</p>
</li>
<li><p>8-6.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;
  #include &lt;string.h&gt;

  int main(void) {
      char str[80];
      printf(&quot;문자열 입력 : &quot;);
      gets_s(str,sizeof(str));
      puts(&quot;입력된 문자열 : &quot;);
      puts(str);

      return 0;
  }</code></pre>
</li>
<li><p><input disabled="" type="checkbox" />  빈칸을 포함하여 문자열을 입력하는 gets함수</p>
</li>
<li><p>Enter를 누르기전까지 전체를 하나의 문자열로 배열에 저장합니다.</p>
</li>
<li><p>gets함수는 입력한 배열의 크기를 검사하지 않으므로 배열보다 크기가 긴 문자열을 입력하면 문제생김.</p>
</li>
<li><p>컴파일러에 따라 시스템 안정성때문에 제한하기도 한다.</p>
</li>
<li><p><input disabled="" type="checkbox" />  gets와 짝을 이뤄 문자열을 출력하는 puts함수</p>
</li>
</ul>
<pre><code class="language-c">printf(&quot;문자열 입력 : &quot;);
gets(str); </code></pre>
<h3 id="문자열의-끝에-널-문자가-없다면">문자열의 끝에 널 문자가 없다면?</h3>
<ul>
<li><p>8-7.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      char str[5];

      str[0]='0';
      str[1]='1';
      print(&quot;%s\n&quot;, str);

      return 0;
  }</code></pre>
</li>
<li><p>배열이 초기화되지 않았으므로 배열에는 쓰레기 값이 남아 있다.</p>
</li>
<li><p>배열 0,1에만 직접문자를 넣었으므로 이후 널문자가 없어 쓰레기 값을 출력합니다.</p>
</li>
<li><p>널문자를 만날때까지 계속 출력</p>
</li>
</ul>