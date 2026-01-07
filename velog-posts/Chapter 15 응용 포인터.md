<h2 id="15-1-이중-포인터와-배열-포인터">15-1 이중 포인터와 배열 포인터</h2>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/a99fa43c-7865-4cc7-a6dd-12ad70139a01/image.png" /></p>
<ul>
<li>포인터도 메모리에 저장공간을 갖는 하나의 변수</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c582bb5b-a498-4772-bbba-772212650eb2/image.png" /></p>
<ul>
<li><p>주소연산으로 포인터의 주소를 구할 수 있다.</p>
</li>
<li><p>포인터의 주소는 이중 포인터에 저장하며 포인터를 가리킵니다.</p>
</li>
<li><p>포인터주소를 저정한 이중 포인터에 간접 참조연산을 수행하면 가리키는 대상인 포인터를 쓸수 있다.</p>
</li>
<li><p>15-1.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int a = 10;        // int형 변수의 선언과 초기화
      int* pi;        // 포인터 선언
      int** ppi;        // 이중 포인터 선언

      pi = &amp;a;        // int형 변수의 주소를 저장한 포인터
      ppi = &amp;pi;        // 포인터의 주소를 저장한 이중 포인터

      printf(&quot;--------------------------------------------\n&quot;);
      printf(&quot;변수    변숫값     &amp;연산     *연산    **연산\n&quot;);
      printf(&quot;--------------------------------------------\n&quot;);
      printf(&quot;   a%10d%10u\n&quot;, a, &amp;a);
      printf(&quot;  pi%10u%10u%10d\n&quot;, pi, &amp;pi, *pi);
      printf(&quot; ppi%10u%10u%10u%10u\n&quot;, ppi, &amp;ppi, *ppi, **ppi);
      printf(&quot;--------------------------------------------\n&quot;);

      return 0;
  }</code></pre>
<pre><code>  --------------------------------------------
  변수    변숫값     &amp;연산     *연산    **연산
  --------------------------------------------
    a        10  00000100
   pi  00000100  00000200        10
  ppi  00000200  00000300  00000100    10</code></pre><ul>
<li><p>이중 포인터 선언</p>
<ul>
<li><p>별(*) 2개를 붙여서 선언 합니다. 두 별은 각각 다른 의미를 가집니다.</p>
<pre><code class="language-c">  int **ppi</code></pre>
</li>
<li><p>첫번째 별은 ppi가 가리키는 자료형이 포인터임을 뜻함.</p>
</li>
<li><p>두번째 별은 ppi자신이 포인터임을 뜻함.</p>
</li>
</ul>
</li>
<li><p>원칙</p>
<ul>
<li>포인터를 변수명(r-value)으로 쓰면 그안의 값이 됩니다.</li>
<li>포인터에 &amp; 연산을 하면 포인터변수의 주소가 됩니다.</li>
<li>포인터의 *연산은 화살표를 따라갑니다.</li>
</ul>
</li>
<li><p>예제</p>
</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/68a20ba9-fdf3-4d47-8982-e56a172da641/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/6341d4d9-f409-49d0-b95f-d3df9995872c/image.png" /></p>
<ul>
<li>이중 포인터의 형태<ul>
<li>포인터가 가리키는 자료형과 포인터 자체의 형태는 다르다.</li>
<li>이중 포인터도 가리키는 포인터의 형태에 맞춰 선언해야 합니다.</li>
<li>(int *)형 포인터는 (int)형을 가리킨다.</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/d859a417-4dca-4a6c-9259-4729add545b6/image.png" /></p>
<pre><code>- (double **)형 이중 포인터는 (double *)형 포인터를 가리킨다.</code></pre><p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/c38cb008-30e6-415c-a3fd-2c77ae5b6b76/image.png" /></p>
<ul>
<li><p>pi나 ppi는 왜 4바이트인가요?</p>
<ul>
<li>선언할때는 double<em>, double*</em>로 선언하지만 주소를 담는 그릇이므로 4바이트이다.</li>
<li>double은 포인터가 가리키는 자료형에 대한 정보일뿐 포인터 자체를 의미하지 않는다.</li>
</ul>
</li>
<li><p>주소와 포인터의 차이</p>
<ul>
<li><p>포인트는 변수이므로 주소연산자를 사용하여 그 주소를 구할 수 있다.</p>
</li>
<li><p>상수인 주소에는 주소 연산자를 사용할 수 없다.</p>
<pre><code class="language-c">int a;
int *pi = &amp;a;
&amp;pi;   // 포인터에 주소 연산자 사용가능
&amp;(&amp;a); // a의 주소에 다시 주소 연산자 사용할 수 없다. (x)</code></pre>
</li>
</ul>
</li>
<li><p>다중 포인터</p>
<pre><code class="language-c">  double ***ppp;</code></pre>
<ul>
<li>4중 포인터 이상의 포인터도 사용할 수 있으나 프로그램의 가독성을 떨어짐.</li>
<li>이중 이상의 포인터를 다중 포인터라 한다.</li>
</ul>
</li>
</ul>
<h3 id="이중-포인터-활용-1--포인터-값을-바꾸는-함수의-매개변수">이중 포인터 활용 1 : 포인터 값을 바꾸는 함수의 매개변수</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/cec5583a-d29c-46a1-abe6-5d3d2c9d7f85/image.png" /></p>
<ul>
<li><p>15-2.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void swap_ptr(char** ppa, char** ppb);

  int main(void)
  {
      char* pa = &quot;success&quot;;
      char* pb = &quot;failure&quot;;

      printf(&quot;pa -&gt; %s, pb -&gt; %s\n&quot;, pa, pb);   // 바꾸기 전에 문자열 출력
      swap_ptr(&amp;pa, &amp;pb);                       // 함수 호출
      printf(&quot;pa -&gt; %s, pb -&gt; %s\n&quot;, pa, pb);   // 바꾼 후에 문자열 출력

      return 0;
  }

  void swap_ptr(char** ppa, char** ppb)
  {
      char* pt;

      pt = *ppa;
      *ppa = *ppb;
      *ppb = pt;
  }</code></pre>
<pre><code class="language-c">  pa -&gt; success, pb -&gt; failure
  pa -&gt; failure, pb -&gt; success</code></pre>
<ul>
<li>위 예제는 문자열을 바꿔 출력하지만 문자열 자체를 바꾸지 않습니다.</li>
<li>문자열을 연결하는 포인터의 값을 바꾸면 연결 상태가 바뀐다.</li>
<li>함수가 호출되어 매개변수가 포인터의 주소를 저장하면 다음과 같다.</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/9f5b8fac-b3dd-479a-9ae8-4ea1f2bd4d6f/image.png" /></p>
<pre><code>- 01   `pt = *ppa`</code></pre><p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/3c77668a-8b50-449a-aec8-de899aada94a/image.png" /></p>
<pre><code>- 02  `*ppa = *ppb`</code></pre><p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/a9f531c2-5a09-46db-8d18-9cc682ea9dfe/image.png" /></p>
<pre><code>- 03 `*ppb = pt;`.</code></pre><p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/9d69f464-14be-4ee3-9217-374d52ae8dee/image.png" /></p>
<h3 id="이중-포인터-활용-2--포인터-배열을-매개변수로-받는-함수">이중 포인터 활용 2 : 포인터 배열을 매개변수로 받는 함수</h3>
<ul>
<li><p>이중 포인터는 포인터 배열을 매개변수로 받는 함수에도 사용된다.</p>
</li>
<li><p>배열명은 첫번째 배열 요소의 주소이므로 int형 배열의 이름은 int형 변수의 주소이다.</p>
</li>
<li><p>15-3.c - 여러개의 문자열을 출력하는 함수, 포인터 배열의 값을 출력하는 함수</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void print_str(char** pps, int cnt);

  int main(void)
  {
      char* ptr_ary[] = {&quot;eagle&quot;, &quot;tiger&quot;, &quot;lion&quot;, &quot;squirrel&quot;};   // 초기화
      int count;                        // 배열 요소 수를 저장할 변수

      count = sizeof(ptr_ary) / sizeof(ptr_ary[0]);  // 배열 요소의 수 계산
      print_str(ptr_ary, count);        // 배열명과 배열 요소 수를 주고 호출

      return 0;
  }

  void print_str(char** pps, int cnt)   // 매개변수로 이중 포인터 사용
  {
      int i;

      for (i = 0; i &lt; cnt; i++)         // 배열 요소 수만큼 반복
      {
          printf(&quot;%s\n&quot;, pps[i]);       // 이중 포인터를 배열명처럼 사용
      }
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/2bfdeb4a-3f45-4eea-ac03-da2fa44a6a52/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/8ec5e584-117c-4b7e-b3fa-5b2218994b9c/image.png" /></p>
<h3 id="배열-요소의-주소와-배열의-주소">배열 요소의 주소와 배열의 주소</h3>
<ul>
<li><p>지금까지는 배열명을 첫번째 요소의 주소로 사용했습니다.</p>
</li>
<li><p>배열 전체를 하나의 변수로 생각하고 그 주소를 구합니다.</p>
</li>
<li><p>15-4.c - 주소로 쓰이는 배열명과 배열의 주소 비교</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int ary[5];

      printf(&quot;  ary의 값 : %u\t&quot;, ary);        // 주소로서의 배열명의 값
      printf(&quot;ary의 주소 : %u\n&quot;, &amp;ary);       // 배열의 주소
      printf(&quot;   ary + 1 : %u\t&quot;, ary + 1);
      printf(&quot;  &amp;ary + 1 : %u\n&quot;, &amp;ary + 1);

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/c1334261-232d-4142-b797-e5c304720f4a/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/3077d1f9-171c-4a8b-a6c0-c912b5a72098/image.png" /></p>
<ul>
<li><p>차이점</p>
<ul>
<li>ary가 주소로 쓰일때와 ary에 주소 연산자를 사용한 &amp;ary의 값은 모두 배열의 시작 위치 입니다.</li>
<li>가리키는 대상이 다르므로 두 주소에 1을 더한 결과값은 다릅니다.</li>
<li>ary자체가 주소로 쓰일 때는 첫번째 요소를 가리키므로 가리키는 대상의 크기는 4가됩니다.</li>
<li>배열의 주소 &amp;ary는 배열 전체를 가리키므로 대상의 크기는 20이 됩니다.</li>
</ul>
</li>
<li><p>배열의 크기와 배열요소의 개수</p>
<ul>
<li>배열의 주소가 가리키는 대상의 크기 = 4바이트 * 배열요소의 수</li>
<li>배열의 크기는 메모리에 할당된 크기(전체바이트)</li>
</ul>
</li>
<li><p>규칙</p>
<ul>
<li><p>배열은 전체가 하나의 논리적인 변수입니다.</p>
<pre><code class="language-c">  sizeof(ary)  //배열 전체의 크기계산

  &amp;ary //배열 전체의 시작주소, 배열 전체를 가리키는 주소</code></pre>
<ul>
<li><p>배열은 논리적인 변수이므로 일반변수처럼 대입연산자 왼쪽에 사용하는 것은 불가능 하다.</p>
<pre><code class="language-c">int ary[5];
ary = 10; //ary배열의 5개 요소중에 어떤 요소에 저장할지 알수 없음 (x)</code></pre>
</li>
</ul>
</li>
<li><p>배열의 주소에 정수를 더하면 배열 전체의 크기를 곱해서 더합니다.</p>
<ul>
<li><p>배열의 정수 연산</p>
<pre><code class="language-c">  ary + 1 //4바이트씩 증가</code></pre>
</li>
<li><p>배열의 주소에 정수 연산</p>
<pre><code class="language-c">  &amp;ary + 1 //배열 전체 크기만큼 증가</code></pre>
</li>
<li><p>1차원 배열에서 배열의 주소를 구하고 정수를 더하는 연산은 가능하지만, 배열의 주소에 정수를 더하면 배열에 할당된 메모리 영역을 벗어나므로 특별한 경우가 아니면 사용하지 말것</p>
</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/a75e4810-06f8-4b0f-bf47-75cb817681df/image.png" /></p>
<h3 id="2차원-배열과-배열-포인터">2차원 배열과 배열 포인터</h3>
<ul>
<li><p>2차원 배열은 1차원 배열로 만든 배열⇒ 논리적인 배열요소가 1차원 배열</p>
</li>
<li><p>2차원 배열의 이름은 1차원 배열의 주소며, 배열을 가리키는 포인터에 저장한다.</p>
</li>
<li><p>15-5.c - 배열포인터로 2차원 배열의 값 출력</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int ary[3][4] = { {1,2,3,4},
                                          {5,6,7,8},
                                          {9,10,11,12} };
      int(*pa)[4];     // int형 변수 4개의 배열을 가리키는 배열 포인터
      int i, j;

      pa = ary;
      for (i = 0; i &lt; 3; i++)
      {
          for (j = 0; j &lt; 4; j++)
          {
              printf(&quot;%5d&quot;, pa[i][j]);  // pa를 2차원 배열처럼 사용
          }
          printf(&quot;\n&quot;);
      }

      return 0;
  }</code></pre>
<p>  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/95a2554e-3096-4c3e-b1da-e00e6f519d00/image.png" /></p>
</li>
</ul>
<pre><code>- 변수명 앞메 별(*)을 붙여 포인터임을 표시하고 괄호로 묶습니다.
- 괄호가 없으면 포인터 배열이 되므로 주의 합니다.</code></pre><p>  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/4f3c35e0-6cd7-429e-ac52-fd13edc094f2/image.png" /></p>
<pre><code>- 선언된 배열 포인터는 일반 포인터처럼 메모리에 저장공간이 확보되므로 이후로 이름으로 사용합니다.

```c
pa = ary
```

- 포인터 배열명을 저장하면 배열처럼 쓸수 있으므로 배열포인터를 2차원 배열처럼 사용합니다.

```c
printf(&quot;%5d&quot;, pa[i][j]);
```

- 이 예제는 ary를 직접 사용하는 것이 더 간단하므로, 굳이 배열 포인터를 쓸이유는 없으나, 2차원 배열을 출력하는 함수에는 배열 포인터가 필요합니다.</code></pre><ul>
<li><p>15-6.c - 2차원 배열의 값을 출력하는 함수</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void print_ary(int(*)[4]);

  int main(void)
  {
      int ary[3][4] = { {1,2,3,4}, {5,6,7,8}, {9,10,11,12} };

      print_ary(ary);                // 배열명을 인수로 주고 함수 호출

      return 0;
  }

  void print_ary(int(*pa)[4])        // 매개변수는 배열 포인터
  {
      int i, j;

      for (i = 0; i &lt; 3; i++)
      {
          for (j = 0; j &lt; 4; j++)
          {
              printf(&quot;%5d&quot;, pa[i][j]);  // pa를 2차원 배열처럼 사용
          }
          printf(&quot;\n&quot;);
      }
  }</code></pre>
<p>  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/4e4c4edb-5dd5-4327-9cd3-a6ffb2e5bf01/image.png" /></p>
</li>
</ul>
<pre><code>- print_ary함수를 호출할때 2차원 배열명을 인수로 주면 함수에는 첫번째 부분배열의 주소가 전달됩니다.

```c
print_ary(ary);
```

- 따라서 이 값을 저장하기 위한 매개변수로 배열 포인터를 선언해야 합니다.</code></pre><ul>
<li><p>2차원 배열 요소의 두가지 의미</p>
<ul>
<li><p>개념적으로 2차원 배열의 요소는 1차원 배열이지만 실제 데이터가 저장되는 공간은 1차원 배열의 요소입니다.</p>
</li>
<li><p>2차원 배열에서 배열요소는 논리적으로 1차원의 부분배열을 뜻하고 물리적으로 실제 데이터를 저장하는 부분배열의 요소를 뜻합니다.</p>
<pre><code class="language-c">int ary[3][4];</code></pre>
</li>
<li><p>2차원 배열 ary의 논리적 배열요소의 개수는 3개</p>
</li>
<li><p>2차원 배열 ary의  물리적 배열요소의 개수는 12개</p>
</li>
</ul>
</li>
</ul>
<h3 id="2차원-배열의-요소를-참조하는-원리">2차원 배열의 요소를 참조하는 원리</h3>
<ul>
<li><p>2차원 배열은 1차원 배열과 같이 모든 저장 공간이 메모리에 연속적으로 할당된다.</p>
</li>
<li><p>이 공간을 2차원의 논리적 공간으로 사용할 수 있는 것은 배열명이 1차원 배열의 주소로 1차원 배열 전체를 가리키기 때문이다.</p>
</li>
<li><p>따라서 배열 포인터를 쓰면 1차원의 물리적 공간을 2차원의 논리적 구조로 사용할 수 있다.</p>
</li>
<li><p>2차원 배열 int ary[3][4];가 다음과 같이 초기화되고 메모리에 할당 되었을때 7번째 물리적 요소를 참조하는 과정을 살펴보면...</p>
<p>  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/6b7b1eea-302e-48c9-8330-0ef9f24f6459/image.png" /></p>
</li>
</ul>
<pre><code>```c
ary + 1 ⇒ 100 + (1 * sizeof(ary[0]) =&gt; 100 + (1*16) =&gt; 116
```

```c
&amp;ary        // 2차원 배열 전체 주소
ary         // 첫번째 부분배열의 주소
&amp;ary[0]     // 첫번째 부분배열의 주소
ary[0]      // 첫번째 부분배열의 첫번째 배열 요소의 주소
&amp;ary[0][0]  // 첫번째 부분배열의 첫번째 배열 요소의 주소

    printf(&quot;%p-&gt;%p\n&quot;, &amp;ary, &amp;ary+1);
    printf(&quot;%p-&gt;%p\n&quot;, ary, ary+1);
    printf(&quot;%p-&gt;%p\n&quot;, &amp;ary[0], &amp;ary[0]+1);
    printf(&quot;%p-&gt;%p\n&quot;, ary[0], ary[0]+1);
    printf(&quot;%p-&gt;%p\n&quot;, &amp;ary[0][0], &amp;ary[0][0] + 1 );

0000002D8592F8E8-&gt;0000002D8592F918
0000002D8592F8E8-&gt;0000002D8592F8F8
0000002D8592F8E8-&gt;0000002D8592F8F8
0000002D8592F8E8-&gt;0000002D8592F8EC
0000002D8592F8E8-&gt;0000002D8592F8EC
```

```c
sizeof(ary)       //배열 전체의 크기 48바이트
sizeof(&amp;ary[0])       // 주소의 크기 4바이트
sizeof(ary[0])       // 부분배열 전체의 크기 16바이트
sizeof(&amp;ary[0][0])       //주소의 크기 4바이트
```</code></pre><h3 id="키워드로-끝내는-핵심-포인트">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>포인터도 하나의 변수이므로 그 주소가 있다.</li>
<li>이중 포인터에 참조연산자를 사용하면 단일 포인터가 된다.</li>
<li>2차원 배열의 배열명은 첫 번째 부분배열의 주소가 된다.</li>
<li>배열 포인터에 참조연산자를 사용하면 가리키는 배열이 된다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/b94ae46f-81e1-4a7c-b412-25199212962d/image.png" /></p>
<hr />
<h2 id="15-2-함수-포인터와-void-포인터">15-2 함수 포인터와 void 포인터</h2>
<h3 id="함수-포인터의-개념">함수 포인터의 개념</h3>
<ul>
<li><p>함수명은 함수 정의가 있는 메모리의 시작 위치 ⇒ 주소</p>
</li>
<li><p>함수명이 주소이므로 포인터에 저장 후 다양한 방식으로 호출 가능.</p>
</li>
<li><p>ex15-7.c - 함수 포인터를 사용한 함수 호출</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int sum(int, int);         // 함수 선언

  int main(void)
  {
      int (*fp)(int, int);   // 함수 포인터 선언
      int res;               // 반환값 저장할 변수

      fp = sum;              // 함수명을 함수 포인터에 저장
      res = fp(10, 20);      // 함수 포인터로 함수 호출
      printf(&quot;result : %d\n&quot;, res);   // 반환값 출력

      return 0;
  }

  int sum(int a, int b)      // 함수 정의
  {
      return (a + b);
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/32a3e353-802f-4793-b195-7703d0c8addb/image.png" /></p>
<ul>
<li>함수명이 주소라는 증거 ⇒ 간접 참조연산자를 사용하면 가리키는 함수의 기능을 사용할 수 있다.9</li>
</ul>
<h3 id="함수의-형태">함수의 형태</h3>
<h2 id="함수-포인터의-활용">함수 포인터의 활용</h2>
<ul>
<li><p>15-8.c</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  void func(int (*fp)(int, int));      // 함수 포인터를 매개변수로 갖는 함수
  int sum(int a, int b);               // 두 정수를 더하는 함수
  int mul(int a, int b);               // 두 정수를 곱하는 함수
  int max(int a, int b);               // 두 정수 중에 큰 값을 구하는 함수

  int main(void)
  {
      int sel;                         // 선택된 메뉴 번호를 저장할 변수

      printf(&quot;01 두 정수의 합\n&quot;);     // 메뉴 출력
      printf(&quot;02 두 정수의 곱\n&quot;);
      printf(&quot;03 두 정수 중에서 큰 값 계산\n&quot;);
      printf(&quot;원하는 연산을 선택하세요 : &quot;);
      scanf(&quot;%d&quot;, &amp;sel);               // 메뉴 번호 입력

      switch (sel)
      {
          case 1: func(sum); break;        // 1이면 func에 덧셈 기능 추가
          case 2: func(mul); break;        // 2이면 func에 곱셈 기능 추가
          case 3: func(max); break;        // 3이면 func에 큰 값 구하는 기능 추가
      }

      return 0;
  }

  void func(int (*fp)(int, int))
  {
      int a, b;                        // 두 정수를 저장할 변수
      int res;                         // 함수의 반환값을 저장할 변수

      printf(&quot;두 정수의 값을 입력하세요 : &quot;);
      scanf(&quot;%d%d&quot;, &amp;a, &amp;b);           // 두 정수 입력
      res = fp(a, b);                  // 함수 포인터로 가리키는 함수를 호출
      printf(&quot;결과값은 : %d\n&quot;, res);  // 반환값 출력
  }

  int sum(int a, int b)        // 덧셈 함수
  {
      return (a + b);
  }

  int mul(int a, int b)        // 곱셈 함수
  {
      return (a * b);
  }

  int max(int a, int b)        // 큰 값을 구하는 함수
  {
      if (a &gt; b) return a;
      else return b;
      }                      </code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/967b0088-8555-48ea-91e7-d7cd1de79a5f/image.png" /></p>
<ul>
<li><p>15-8-simple.c</p>
<pre><code class="language-c">
  #include &lt;stdio.h&gt;

  int sum(int a, int b);               // 두 정수를 더하는 함수
  int mul(int a, int b);               // 두 정수를 곱하는 함수
  int max(int a, int b);               // 두 정수 중에 큰 값을 구하는 함수

  int main(void)
  {
      int a, b;

      int (*fp)(int a, int b);
      scanf(&quot;%d %d&quot;,&amp;a, &amp;b );               // 메뉴 번호 입력

      fp = sum;
      int result = fp(a, b);
      printf(&quot;01 두 정수의 합: %d \n&quot;,result );   

      fp = mul;
      result = fp(a, b);
      printf(&quot;02 두 정수의 곱 : %d\n&quot;, result);

      fp = max;
      result = fp(a, b);
      printf(&quot;03 두 정수 중에서 큰 값 계산: %d\n&quot;, result);

      printf(&quot;원하는 연산을 선택하세요 : &quot;);

      return 0;
  }

  int sum(int a, int b)        // 덧셈 함수
  {
      return (a + b);
  }

  int mul(int a, int b)        // 곱셈 함수
  {
      return (a * b);
  }

  int max(int a, int b)        // 큰 값을 구하는 함수
  {
      if (a &gt; b) return a;
      else return b;
  }</code></pre>
</li>
</ul>
<h3 id="void-포인터">void 포인터</h3>
<ul>
<li><p>15-9.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int a = 10;                           // int형 변수
      double b = 3.5;                       // double형 변수
      void* vp;                             // void 포인터

      vp = &amp;a;                              // int형 변수의 주소 저장
      printf(&quot;a : %d\n&quot;, *(int*)vp);

      vp = &amp;b;                              // double형 변수의 주소 저장
      printf(&quot;b : %.1lf\n&quot;, *(double*)vp);
  //printf(&quot;b : %.1lf\n&quot;, *vp);           // 잘못된 표현(data type을 변경해야 한다!)
      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/fae7405a-ed7d-4c88-9dc1-feb409c5a881/image.png" /></p>
<hr />
<h3 id="키워드로-끝내는-핵심-포인트-1">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>함수명의 의미부터 보자면 함수명은 함수 정의가 있는 메모리의 시작 주소다.</li>
<li>함수 포인터에 함수명을 대입하면 함수처럼 호출할 수 있다.</li>
<li>void 포인터에는 임의의 주소를 저장할 수 있다.</li>
<li>void 포인터는 간접 참조 연산과 주소에 대한 정수 연산이 불가능하다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트-1">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/642379ba-9c46-4482-b240-a171c90c5a1e/image.png" /></p>