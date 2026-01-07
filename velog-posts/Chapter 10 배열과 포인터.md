<h2 id="10-1-배열과-포인터의-관계">10-1 배열과 포인터의 관계</h2>
<ul>
<li>배열은 자료형이 같은 변수를 메모리에 연속으로 할당합니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/6a275ca6-74c4-485b-b177-31d18f626717/image.png" /></p>
<ul>
<li>따라서 각 배열 요소는 일정한 간격으로 주소를 갖게 됩니다.</li>
<li>첫번째 요소의 주소를 알면 나머지 요소의 주소도 쉽게 알 수 있고, 각 주소의 간접참조연산을 수행하면 모든 배열요소를 사용할 수 있다.</li>
<li>컴파일러는 첫번째 배열 요소의 주소를 쉽게 사용하도록 배열명을 컴파일 과정에서 첫번째 배열 요소의 주소로 변경합니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9447efb9-fbb6-4883-8490-a6e74cdbdbc8/image.png" /></p>
<h3 id="배열명으로-배열-요소-사용하기">배열명으로 배열 요소 사용하기</h3>
<ul>
<li>주소는 정수처럼 보이지만 자료형에 대한 정보를 갖고 있는 특별한 값이다.</li>
<li>따라서 연산을 자유롭게 할 수 없고, 정해진 연산만 가능합니다.</li>
<li>정수덧셈의 경우 4바이트인 int형 변수 a의 주소 100번지에 1을 더한 결과는 101이 아닌 104가 됩니다.</li>
</ul>
<blockquote>
<p>주소 + 정수    ==&gt;   주소 + (정수*주소를 구현 변수의 크기)</p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/38122406-504e-45c5-bbf8-5884bd5da30b/image.png" /></p>
<ul>
<li><p>ex10-1.c 배열명에 정수 연산을 수행하여 배열요소 사용</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      int ary[3];
      int i;

      *(ary + 0) = 10;                   // ary[0] = 10
      *(ary + 1) = *(ary + 0) + 10;      // ary[1] = ary[0] + 10

      printf(&quot;세 번째 배열 요소에 키보드 입력 : &quot;);
      scanf(&quot;%d&quot;, ary + 2);              // &amp;ary[2]

      for (i = 0; i &lt; 3; i++)            // 모든 배열 요소 출력
      {
          printf(&quot;%5d     &quot;, *(ary + i));     // ary[i]
      }

      return 0;
  }
</code></pre>
<pre><code>  세 번째 배열 요소에 키보드 입력 :    10        20     -1390132464
</code></pre></li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/dc30c16e-dcc2-4314-aeb6-573e8b965ae7/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/7bb9f275-bd53-4591-91fe-ad5f38778478/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/e3be1a85-ca5b-449c-98b0-c4fbdc361463/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/1e1c3736-0312-491e-8050-31aeefe81158/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/d6bdc97d-3d75-49e8-90c6-4b2f97b5d764/image.png" /></p>
<h3 id="배열의-할당-영역을-벗어나는-포인터-연산식을-사용할-수-있나요">배열의 할당 영역을 벗어나는 포인터 연산식을 사용할 수 있나요?</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/7bd1fbe7-1d7c-446a-a87c-a19f2b0eebb0/image.png" /></p>
<ul>
<li>사용할 수 있으나 사용하면 안됩니다.</li>
<li>실수가 많으니 주의!</li>
</ul>
<h3 id="배열명-역할을-하는-포인터">배열명 역할을 하는 포인터</h3>
<ul>
<li><p>배열명은 주소이므로 포인터에 저장 할 수 있습니다.</p>
</li>
<li><p>이 경우 포인터로도 연산식이나 대괄호를 써서 배열 요소를 쉽게 사용할 수 있습니다.</p>
</li>
<li><p>ex10-2.c 배열명처럼 사용되는 포인터</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int ary[3];                // 배열 선언
      int* pa = ary;             // 포인터에 배열명 저장
      int i;                     // 반복 제어 변수

      *pa = 10;                  // 첫 번째 배열 요소에 10 대입
      *(pa + 1) = 20;            // 두 번째 배열 요소에 20 대입
      pa[2] = pa[0] + pa[1];     // 대괄호를 써서 pa를 배열명처럼 사용

      for (i = 0; i &lt; 3; i++)
      {
          printf(&quot;%5d&quot;, pa[i]);  // 포인터로 모든 배열 요소 출력
      }

      printf(&quot;\n&quot;);
      for (i = 0; i &lt; 3; i++)
      {
          printf(&quot;%5d&quot;, *(pa+i));
      }
      return 0;
  }
</code></pre>
<pre><code>     10   20   30
     10   20   30
</code></pre></li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/75ae6538-c136-402c-87b3-f4cea06ee76f/image.png" /></p>
<ul>
<li>정의 할때는 주소를 할당하고, 사용할때는 값을 할당한다.</li>
<li>int *pa=ary;  ⇒ 포인터에 배열명(주소)저장</li>
<li>*pa=10; =&gt; *pa는 pa를 가리키는 것이므로 ary[0]에 10을 저장</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/26d29f7f-af06-44f6-bef1-f1bb22924cdf/image.png" /></p>
<h3 id="배열명과-포인터의-차이">배열명과 포인터의 차이</h3>
<ul>
<li><p>포인터가 배열명처럼 쓰이기는 하지만 서로 다른 점이 더 많습니다.</p>
</li>
<li><p>sizeof 연산자의 결과가 다릅니다.</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;
  int main(void)
  {
      int ary[10];
      int *pa=ary;
      printf(&quot;%5d&quot;,sizeof(ary));  //12byte 배열 전체크기
      printf(&quot;%5d&quot;,sizeof(pa));   // 8byte 포인터 하나의 크기

      return 0;
  }
</code></pre>
<pre><code>     40    8
</code></pre></li>
<li><p>변수와 상수의 차이가 있습니다.</p>
</li>
<li><p>포인터는 그 값을 바꿀수 있지만, 배열명은 상수이므로 그 값을 바꿀 수 없습니다.</p>
</li>
<li><p>포인터는 pa에 1을 더하여 다시 pa에 저장할 수 있으나, 배열명은 ary는 1을 더하는 것은 가능하나, 다시 저장하는 것은 불가능하다.</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;
  int main(void)
  {
      int ary[10];
      int *pa=ary;

      pa=pa+1;
      ary=ary+1;

      return 0;
  }
</code></pre>
<pre><code>  /tmp/tmpbfyv9vke.c: In function 'main':
  /tmp/tmpbfyv9vke.c:8:8: error: assignment to expression with array type
      8 |     ary=ary+1;
        |        ^
  [C kernel] GCC exited with code 1, the executable will not be executed
</code></pre></li>
<li><p>ex10-3.c 포인터를 이용한 배열의 값 출력</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int ary[3] = { 10, 20, 30 };
      int* pa = ary;
      int i;

      printf(&quot;배열의 값 : &quot;);
      for (i = 0; i &lt; 3; i++)
      {
          printf(&quot;%d &quot;, *pa);   // pa가 가리키는 배열 요소 출력
          pa++;                 // 다음 배열 요소를 가리키도록 pa 값 증가
      }

      return 0;
  }
</code></pre>
<pre><code>  배열의 값 : 10 20 30
</code></pre></li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/82e9dab9-7569-41a4-b290-26bda1622aa6/image.png" /></p>
<ul>
<li><p>포인터 pa로 첫번째 배열요소를 출력하는 여러가지 방법</p>
<ol>
<li><p>pa를 배열명처럼 사용하여 첫번째 배열 요소를 출력하는 방법</p>
<blockquote>
<p>print(&quot;%d&quot;,pa[0]);</p>
</blockquote>
</li>
<li><p>pa[0]를 그대로 포인터 연산식으로 바꾸는 방법</p>
<blockquote>
<p>print(&quot;%d&quot;,*(pa + 0);</p>
</blockquote>
</li>
<li><p>(pa+0)에서 의미 없는 0과 괄호를 제거한 표현 방법</p>
<blockquote>
<p>print(&quot;%d&quot;,*pa);</p>
</blockquote>
</li>
</ol>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/9b0b5d07-fa28-4b73-893c-81eb39d73ca2/image.png" /></p>
<ul>
<li>포인터로 배열의 데이터를 처리할 때  주의점<ol>
<li>포인터의 값이 변할 수 있으므로 유효한 값인지 확인하는 습관이 필요.</li>
</ol>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/86ca3e93-9447-4b23-9671-7297eb6fac19/image.png" /></p>
<pre><code>2. 포인터 증가 연산자와 간접 참조 연산자를 함께 사용할때 전위 표현을 사용하면 안됩니다.</code></pre><p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/2a7faf32-43a7-489c-b3a8-84dc459842bc/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/0a92380f-66a6-4fef-81a6-14decaa5d732/image.png" /></p>
<h3 id="포인터의-뺄셈과-관계연산">포인터의 뺄셈과 관계연산</h3>
<ul>
<li>가리키는 자료형이 같으면 포인터끼리 뺄셈도 가능</li>
</ul>
<blockquote>
<p>포인터 -포인터  ==&gt; 값의차 / 가리키는 자료형의 크기</p>
</blockquote>
<ul>
<li><p>관계연산자로 대소관계도 확인가능</p>
</li>
<li><p>ex10-4.c 포인터의 뺄셈과 관계 연산</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int a=0;
      int ary[5] = { 10, 20, 30, 40, 50 };
      int* pa = ary;                         // 첫 번째 배열 요소 주소
      int* pb = pa + 3;                      // 네 번째 배열 요소 주소

      printf(&quot;pa : %d\n&quot;, *pa);
      printf(&quot;pa : %d\n&quot;, *pb);

      printf(&quot;pa : %u\n&quot;, pa);
      printf(&quot;pb : %u\n&quot;, pb);

      pa++;                                  // pa를 다음 배열 요소로 이동
      printf(&quot;size of %u\n&quot;, sizeof(int));
      printf(&quot;pa : %u\n&quot;, pa);
      printf(&quot;pb : %u\n&quot;, pb);
      printf(&quot;pb - pa : %u\n&quot;, pb - pa);     // 두 포인터의 뺄셈

      printf(&quot;앞에 있는 배열 요소의 값 출력 : &quot;);
      if (pa &lt; pb) printf(&quot;%d\n&quot;, *pa);      // pa가 배열의 앞에 있으면 *pa 출력
      else printf(&quot;%d\n&quot;, *pb);              // pb가 배열의 앞에 있으면 *pb 출력

      return 0;
  }
</code></pre>
<pre><code>  pa : 10
  pa : 40
  pa : 3788207024
  pb : 3788207036
  size of 4
  pa : 3788207028
  pb : 3788207036
  pb - pa : 2
  앞에 있는 배열 요소의 값 출력 : 20
</code></pre></li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/e4a4c52c-04bc-477b-931c-570b8def8571/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/72478f0d-d557-4acc-b3cc-b548c5bb108b/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/c289a253-5df7-47fb-a14a-c980c38bd5f5/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/be28a698-6330-423b-b3b9-b92ee342731e/image.png" /></p>
<h2 id="10-2-배열을-처리하는-함수">10-2 배열을 처리하는 함수</h2>
<ul>
<li>배열명을 꼭 포인터에 넣는 방식으로 배열을 처리할 필요는 없다.</li>
<li>하지만 함수로 배열을 처리하려면 포인터가 필요.</li>
</ul>
<blockquote>
<p>print_ary(ary);</p>
</blockquote>
<blockquote>
<p>void print_aray(int *pa)</p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/1008b9cb-b499-42cd-a8e2-a441bf17845c/image.png" /></p>
</blockquote>
<blockquote>
</blockquote>
<ul>
<li>배열명을 함수의 인수로 준다는 건 결국 int형 변수의 주소를 전달한다는 것입니다.</li>
<li>따라서 매개변수로 받을 때는 int형 변수의 주소를 저장할 포인터를 선언해야 합니다.</li>
</ul>
<h3 id="배열의-값을-출력하는-함수">배열의 값을 출력하는 함수.</h3>
<ul>
<li><p>배열의 값을 확인하기 위해 수시로 출력해야 한다면 그 기능을 함수로 만들어 호출하면 됩니다.</p>
</li>
<li><p>모든 배열요소를 함수의 인수로 줘야 할까?</p>
</li>
<li><p>첫 번째 배열 요소의 주소만 알면 나머지 배열 요소는 포인터 연산으로 모두 사용할 수 있다.</p>
</li>
<li><p>배열명 자체가 주소이므로 그 값을 함수의 인수로 주는 것은 얼마든지 가능합니다.</p>
</li>
<li><p>ex10-5 배열을 처리하는 함수</p>
<pre><code>  10 20 30 40 50
</code></pre><pre><code class="language-c">  #include &lt;stdio.h&gt;

  void print_ary(int* pa);        // 함수 선언

  int main(void)
  {
      int ary[5] = { 10, 20, 30, 40, 50 };

      print_ary(ary);             // 배열명을 주고 함수 호출

      return 0;
  }

  void print_ary(int *pa)         // 매개변수로 포인터 선언
  {
      int i;

      for (i = 0; i &lt; 5; i++)
      {
          printf(&quot;%d &quot;, pa[i]);   // pa로 배열 요소 표현식 사용
                  //pa++;
      }
  }
</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/219b779b-101a-4315-80b0-f556243f079d/image.png" /></p>
<ul>
<li>정수연산 : pa + 1</li>
<li>간접참조연산 : *(pa+1)</li>
<li>배열요소 표현식 : pa[1]</li>
<li>동일한 배열의 데이터를 2개의 함수가 공유합니다.</li>
<li>print_ary함수는 주소를 매개변수로 받아서 main함수에 있는 배열의 값을 출력합니다.</li>
<li>배열에 있는 대량의 데이터를 다른 함수로 복사하지 않고 접근하므로 더 효율적입니다.</li>
</ul>
<h3 id="배열-요소의-개수가-다른-배열도-출력하는-함수">배열 요소의 개수가 다른 배열도 출력하는 함수</h3>
<ul>
<li><p>ex10-6 크기가 다른 배열을 출력하는 함수</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void print_ary(int* pa, int size);   // 함수 선언, 매개변수 2개

  int main(void)
  {
      int ary1[5] = { 10, 20, 30, 40, 50 };           // 배열 요소의 개수가 5개인 배열
      int ary2[7] = { 10, 20, 30, 40, 50, 60, 70 };   // 요소의 개수가 7개인 배열

      print_ary(ary1, 5);              // ary1 배열 출력, 배열 요소의 개수 전달
      printf(&quot;\n&quot;);
      print_ary(ary2, 7);              // ary2 배열 출력, 배열 요소의 개수 전달

      return 0;
  }

  void print_ary(int* pa, int size)    // 배열명과 배열 요소의 개수를 받는 매개변수 선언
  {
      int i;

      for (i = 0; i &lt; size; i++)       // size의 값에 따라 반복 횟수 결정
      {
          printf(&quot;%d &quot;, pa[i]);
      }
  }
</code></pre>
<pre><code>  10 20 30 40 50
  10 20 30 40 50 60 70
</code></pre></li>
<li><p>배열요소의 개수를 sizeof연산자로 구해서 함수호출</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void print_ary(int* pa, int size);   // 함수 선언, 매개변수 2개

  int main(void)
  {
      int ary1[5] = { 10, 20, 30, 40, 50 };           // 배열 요소의 개수가 5개인 배열
      int ary2[7] = { 10, 20, 30, 40, 50, 60, 70 };   // 요소의 개수가 7개인 배열

      print_ary(ary1, sizeof(ary1)/sizeof(ary1[0]));              // ary1 배열 출력, 배열 요소의 개수 전달
      printf(&quot;\\n&quot;);
      print_ary(ary2, sizeof(ary2)/sizeof(ary2[0]));              // ary2 배열 출력, 배열 요소의 개수 전달

      return 0;
  }

  void print_ary(int* pa, int size)    // 배열명과 배열 요소의 개수를 받는 매개변수 선언
  {
      int i;

      for (i = 0; i &lt; size; i++)       // size의 값에 따라 반복 횟수 결정
      {
          printf(&quot;%d &quot;, pa[i]);
      }
  }
</code></pre>
<pre><code>  10 20 30 40 50
  10 20 30 40 50 60 70
</code></pre></li>
</ul>
<h3 id="배열에-값을-입력하는-함수">배열에 값을 입력하는 함수</h3>
<ul>
<li><p>배열에 값을 입력하는 함수도 배열의 값을 출력하는 함수와 구현 방법은 같습니다.</p>
</li>
<li><p>다만 입력함수는 데이터를 저장할 배열의 위치가 필요하므로 함수안에서 포인터를 직접 사용합니다.</p>
</li>
<li><p>예제로 실수배열에 값을 입력하는 함수와 최대값을 찾는 함수를 만들어 봅시다.</p>
</li>
<li><p>ex10-7 배열에 값을 입력하는 함수</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  void input_ary(double* pa, int size);
  double find_max(double* pa, int size);

  int main(void)
  {
      double ary[5];
      double max;                               // 최댓값을 저장할 변수
      int size = sizeof(ary) / sizeof(ary[0]);  // 배열 요소의 개수 계산

      input_ary(ary, size);                     // 배열에 값 입력
      max = find_max(ary, size);                // 배열의 최댓값 반환
      printf(&quot;배열의 최댓값 : %.1lf\n&quot;, max);

      return 0;
  }

  void input_ary(double* pa, int size)          // double 포인터를 매개변수로 선언
  {
      int i;

      printf(&quot;%d개의 실수값 입력 : &quot;, size);
      for (i = 0; i &lt; size; i++)                // size의 값에 따라 반복 횟수 결정
      {
          scanf(&quot;%lf&quot;, pa + i);                 // &amp;pa[i]도 가능, 입력할 배열 요소의 주소를 전달
          pa[i]=i+1;
      }
  }

  double find_max(double* pa, int size)
  {
      double max;
      int i;

      max = pa[0];                              // 첫 번째 배열 요소의 값을 최댓값으로 설정
      for (i = 1; i &lt; size; i++)                // 두 번째 배열 요소부터 max와 비교
      {
          if (pa[i] &gt; max) max = pa[i];         // 새로운 배열 요소의 값이 max보다 크면 대입
      }

      return max;                               // 최댓값 반환
  }
</code></pre>
<pre><code>  5개의 실수값 입력 : 배열의 최댓값 : 5.0
</code></pre></li>
</ul>
<h3 id="함수의-매개변수-자리에-배열을-선언하는-경우">함수의 매개변수 자리에 배열을 선언하는 경우</h3>
<ul>
<li>함수의 매개변수 자리에 배열을 선언하면 배열의 저장공간이 할당되지않으며,</li>
<li>배열명은 컴파일과정에서 첫번째 배열요소를 가리키는 포인터로 바뀝니다.</li>
<li>매개변수 자리에 선언된 배열은 포인터로 바뀌므로 함수안에서 sizeof연산자로 배열의 크기를 알수 없습니다.</li>
<li>따라서 배열 요소와 개수와 무관하게 배열을 처리하는 함수를 만들려면 반드시 배열 요소의 개수를 따로 받아야 합니다.</li>
</ul>