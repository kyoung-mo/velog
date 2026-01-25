<h2 id="6-1-while문-for문-do-while문">6-1 while문, for문, do-while문</h2>
<h3 id="while문">while문</h3>
<ul>
<li>조건식을 먼저 검사하고 조건식이 참인 동안 실행문을 반복 합니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3f05e8df-c683-4f0f-9098-e093feb295a1/image.png" /></p>
<pre><code>- ex6-1.c

    ```c
    #include &lt;stdio.h&gt;

    int main(void)
    {
        int a = 1;               // 변수를 선언하고 곱셈을 하기 위해 1로 초기화

        while (a &lt; 10)           // ① a가 10보다 작으므로 조건식은 참
        {

            a = a * 2;           // ② a에 2를 곱해 a에 다시 저장
        }
        printf(&quot;a : %d\n&quot;, a);   // a 값 출력

        return 0;
    }

    ```

    ```
    a : 16

    ```</code></pre><pre><code>/ : slash
\ : back slash

() round parenthsis
{} brace
[] square brackets
&lt;&gt; angle brackets, pointer bracekt
</code></pre><h3 id="for-문">for 문</h3>
<ul>
<li>원하는 횟수만큼 반복할 때 사용</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/4bca840a-216d-402b-9183-1ec52c45ed5e/image.png" /></p>
<ul>
<li><p>ex6-2.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int a = 1;                   // 변수를 선언하고 1로 초기화
      //int i;                       // 반복 횟수를 세기 위한 변수

      for (int i = 0; i &lt; 3; i++)      // ① i는 0으로 초기화된 후에 ② 3보다 작은 동안(i &lt; 3)
      {                            // ③ 하나씩 증가하면서(i++)
          a = a * 2;               // 실행문을 실행
      }
      printf(&quot;a : %d\n&quot;, a);       // for문을 빠져나오면 a 값 출력

      return 0;
  }
</code></pre>
<pre><code>  a : 8
</code></pre></li>
</ul>
<h3 id="for-문-사용-시-주의점">for 문 사용 시 주의점</h3>
<blockquote>
<p>초기식, 조건식, 증감식은 반복 회수를 알기 쉽게 작성합니다.
반복 횟수를 세는 변수를 반복문 안에서 바꾸지 않는 것이 좋습니다.</p>
</blockquote>
<h3 id="do---while문">do - while문</h3>
<ul>
<li>while, for문은 조건식을 먼저 확인</li>
<li>do - while문은 일단 반복할 문장을 수행한 후 조건을 검사합니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/6d276d74-a88b-4e97-b826-d096b8eeac0e/image.png" /></p>
<pre><code>- ex6-3.c

    ```c
    #include &lt;stdio.h&gt;

    int main(void)
    {
        int a = 1;                // 변수를 선언하고 1로 초기화

        do                        // 반복문 시작 위치
        {
            a = a * 2;            // a의 값을 2배로 늘린다.
        } while (a &lt; 10);         // a가 10보다 작으면 9행을 반복
        printf(&quot;a : %d\n&quot;, a);    // 반복이 끝난 후 a 값 출력

        return 0;
    }

    ```

    ```
        a : 16
    ```</code></pre><h3 id="do--while문의-특징">do -while문의 특징</h3>
<ul>
<li>조건식에 관계없이 반복할 문장을 최소 한번은 실행</li>
</ul>
<p>#include &lt;stdio.h&gt;</p>
<p>int main(void)
{
int a = 1;               // 변수를 선언하고 곱셈을 하기 위해 1로 초기화</p>
<pre><code>while (a &lt; 10)           // ① a가 10보다 작으므로 조건식은 참
{

    a = a * 2;           // ② a에 2를 곱해 a에 다시 저장
}
printf(&quot;a : %d\\n&quot;, a);   // a 값 출력

return 0;
</code></pre><p>}</p>
<h2 id="6-2-반복문-활용">6-2 반복문 활용</h2>
<h3 id="중첩-반복문">중첩 반복문</h3>
<ul>
<li><p>반복문안에 실행할 문장으로 반복문이 포함된 경우</p>
</li>
<li><p>ex6-4.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int i, j;                     // 반복 횟수를 세기 위한 제어 변수

      for (i = 0; i &lt; 3; i++)       // i가 0부터 2까지 증가하면서 3번 반복
      {
          for (j = 0; j &lt; 5; j++)   // j가 0부터 4까지 증가하면서 5번 반복
          {
              printf(&quot;*&quot;);          // 별 출력문
          }
          printf(&quot;\n&quot;);             // 별을 5번 출력한 후에 줄을 바꾼다.
      }

      return 0;
  }
</code></pre>
<pre><code>  *****
  *****
  *****
</code></pre></li>
</ul>
<h3 id="중첩-반복문-사용-시-주의점">중첩 반복문 사용 시 주의점</h3>
<ul>
<li>각 반복문이 서로 독립적인 제어 변수를 사용해야 각각 원하는 횟수를 반복할 수 있습니다.</li>
</ul>
<h3 id="중첩반복문으로-구구단-출력하는-프로그램">중첩반복문으로 구구단 출력하는 프로그램</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
int main(void)
{
    int i,j;
    for(i=2; i&lt;=9; i++)
    {
        for(j=1; j&lt;=9; j++)
        {
            printf(&quot;%d * %d = %d\n&quot;, i,j,i*j);
                        //10보다 큰수일 경우 break이용해서 빠져나간다.
        }

    }
}
</code></pre>
<ul>
<li><p>결과</p>
<pre><code>  2 * 1 = 2
  2 * 2 = 4
  2 * 3 = 6
  2 * 4 = 8
  2 * 5 = 10
  2 * 6 = 12
  2 * 7 = 14
  2 * 8 = 16
  2 * 9 = 18
  3 * 1 = 3
  3 * 2 = 6
  3 * 3 = 9
  3 * 4 = 12
  3 * 5 = 15
  3 * 6 = 18
  3 * 7 = 21
  3 * 8 = 24
  3 * 9 = 27
  4 * 1 = 4
  4 * 2 = 8
  4 * 3 = 12
  4 * 4 = 16
  4 * 5 = 20
  4 * 6 = 24
  4 * 7 = 28
  4 * 8 = 32
  4 * 9 = 36
  5 * 1 = 5
  5 * 2 = 10
  5 * 3 = 15
  5 * 4 = 20
  5 * 5 = 25
  5 * 6 = 30
  5 * 7 = 35
  5 * 8 = 40
  5 * 9 = 45
  6 * 1 = 6
  6 * 2 = 12
  6 * 3 = 18
  6 * 4 = 24
  6 * 5 = 30
  6 * 6 = 36
  6 * 7 = 42
  6 * 8 = 48
  6 * 9 = 54
  7 * 1 = 7
  7 * 2 = 14
  7 * 3 = 21
  7 * 4 = 28
  7 * 5 = 35
  7 * 6 = 42
  7 * 7 = 49
  7 * 8 = 56
  7 * 9 = 63
  8 * 1 = 8
  8 * 2 = 16
  8 * 3 = 24
  8 * 4 = 32
  8 * 5 = 40
  8 * 6 = 48
  8 * 7 = 56
  8 * 8 = 64
  8 * 9 = 72
  9 * 1 = 9
  9 * 2 = 18
  9 * 3 = 27
  9 * 4 = 36
  9 * 5 = 45
  9 * 6 = 54
  9 * 7 = 63
  9 * 8 = 72
  9 * 9 = 81
</code></pre></li>
<li><p>구구단 아래와 형식으로 재작성</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;
  int main(void)
  {
  int i, j;
  for (i = 2; i &lt;= 9; i++)
  {
  for (j = 1; j &lt;= 9; j++)
  {
  printf(&quot;%d * %d = %d &quot;, i, j, i * j);
  //10보다 큰수일 경우 break이용해서 빠져나간다.
  }
  printf(&quot;\n&quot;);
  }
  }</code></pre>
<pre><code class="language-c">  2 * 1 = 2 2 * 2 = 4 2 * 3 = 6 2 * 4 = 8 2 * 5 = 10 2 * 6 = 12 2 * 7 = 14 2 * 8 = 16 2 * 9 = 18
  3 * 1 = 3 3 * 2 = 6 3 * 3 = 9 3 * 4 = 12 3 * 5 = 15 3 * 6 = 18 3 * 7 = 21 3 * 8 = 24 3 * 9 = 27break와 continue분기문</code></pre>
<pre><code class="language-c"></code></pre>
</li>
<li><p>반복문 안에서 사용하는 제어문</p>
</li>
</ul>
<h3 id="break문">break문</h3>
<ul>
<li><p>반복문 안에서 반복을 즉시 끝낼 때 사용</p>
</li>
<li><p>모든 반복문은 조건식이 거짓일 때 반복이 끝납니다.</p>
</li>
<li><p>break문은 자신을 포함하는 반복문 하나만 벗어납니다.</p>
</li>
<li><p>반복문이 중첩된 경우 가장 안쪽의 break문으로 모든 반복문을 한번에 벗어날 수 없습니다.</p>
</li>
<li><p>if문 블록에서 사용하면 if문 블록을 포함한 반복문을 벗어납니다.</p>
</li>
<li><p>ex6-5.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int i;                          // 반복 횟수를 세기 위한 제어 변수
      int sum = 0;                    // 1부터 10까지의 합을 누적할 변수

      for (i = 1; i &lt;= 10; i++)       // i는 1부터 10까지 증가하면서 10번 반복
      {
          sum += i;                   // i 값을 sum에 누적
          if (sum &gt; 30) break;        // 누적한 값이 30보다 크면 반복문을 끝낸다.
      }
      printf(&quot;누적한 값 : %d\n&quot;, sum);
      printf(&quot;마지막으로 더한 값 : %d\n&quot;, i);

      return 0;
  }
</code></pre>
<pre><code>  누적한 값 : 36
  마지막으로 더한 값 : 8
</code></pre></li>
</ul>
<h3 id="break로-무한-반복문-빠져나오기">break로 무한 반복문 빠져나오기</h3>
<ul>
<li>반복문의 조건식이 항상 참이면 무한 반복문이 됩니다.</li>
</ul>
<pre><code class="language-c">count=0;
while(1)
{
    printf(&quot;Be happy&quot;);
    count++;
    if(count==5) break;
}

for(;;)
{
    print(&quot;Be happy&quot;);
}
</code></pre>
<h3 id="continue">continue</h3>
<ul>
<li>반복문의 일부를 건너뜁니다.</li>
<li>반복문 안에서 continue를 사용하면 다음 실행 위치가 반복문의 블록 끝이 됩니다.</li>
<li>블록을 탈출하는 것은 아닙니다.</li>
</ul>
<h3 id="while문에서-continue-사용-시-유의점">while문에서 continue 사용 시 유의점</h3>
<ul>
<li>for문과 달리 while문에서 continue를 사용하면 다음 실행 위치가 조건식이 됩니다.</li>
<li>아래 코드는 무한 반복됩니다.</li>
</ul>
<pre><code class="language-c">i=1;
while(i&lt;=100)
{
    if((i%3)==0)
    {
        continue;
    }
    sum+=i;
    i++;
}

#</code></pre>
<ul>
<li><p>별모양으로 삼각형 그리기</p>
<h2 id="1-왼쪽-정렬-직각삼각형"><strong>1. 왼쪽 정렬 직각삼각형</strong></h2>
<pre><code class="language-c">  삼각형의 높이를 입력하세요: 5
  *
  **
  ***
  ****
  *****</code></pre>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int i, j, k;                     // 반복 횟수를 세기 위한 제어 변수

      printf(&quot;삼각형의 높이를 입력하세요: &quot;);
      scanf(&quot;%d&quot;, &amp;k);

      for (i = 0; i &lt; k; i++)       // i가 0부터 입력한 높이까지 증가하면서 3번 반복
      {
          for (j = 0; j &lt;= i; j++)   // j가 0부터 i까지 증가하면서 5번 반복
          {
              printf(&quot;*&quot;);          // 별 출력문
          }
          printf(&quot;\n&quot;);             // 별을 입력한 횟수 번 출력한 후에 줄을 바꾼다.
      }

      return 0;
  }</code></pre>
<p>  <strong>2. 오른쪽 정렬 직각삼각형</strong></p>
<pre><code class="language-c">  삼각형의 높이를 입력하세요: 5
      *
     **
    ***
   ****
  *****</code></pre>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int i, j, k, l;                     

      printf(&quot;삼각형의 높이를 입력하세요: &quot;);
      scanf(&quot;%d&quot;, &amp;k);

      for (i = 0; i &lt; k; i++)       
      {
          for (j = 0; j &lt; k - i; j++)
          {
              printf(&quot; &quot;);
          }
          for (l = 0; l &lt;= i; l ++)   
          {
              printf(&quot;*&quot;);          
          }
          printf(&quot;\n&quot;);             
      }

      return 0;
  }</code></pre>
<p>  <strong>3. 정삼각형(피라미드형)</strong></p>
<pre><code class="language-c">  삼각형의 높이를 입력하세요: 5
      *
     ***
    *****
   *******
  *********</code></pre>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void) {
      int i, j, k, l, m;
      printf(&quot;삼각형의 높이를 입력하세요: &quot;);
      scanf(&quot;%d&quot;, &amp;k);

      for (i = 0; i &lt; k; i++) {
          for (j = 0; j &lt; k - i; j++) {
              printf(&quot; &quot;);
          }
          for (m = 0; m &lt;= i; m++) {
              printf(&quot;*&quot;);
          }
          for (l = 0; l &lt; i; l++) {
              printf(&quot;*&quot;);
          }
          printf(&quot;\n&quot;);
      }

      return 0;
  }</code></pre>
</li>
</ul>