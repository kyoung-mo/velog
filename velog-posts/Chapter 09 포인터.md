<h3 id="9-1-포인터의-기본-개념">9-1 포인터의 기본 개념</h3>
<h3 id="메모리-주소">메모리 주소</h3>
<ul>
<li>메모리는 데이터를 넣고 꺼내 쓰는 공간</li>
<li>메모리 위치를 식별하는 주소값은 바이트 단위로 구분</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/d6fddb1d-c2f8-4514-8682-198100c60a4f/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/d6c03287-d48c-4707-8e45-67eccee981e7/image.png" /></p>
<h3 id="주소-연산자">주소 연산자: &amp;</h3>
<ul>
<li><p>시작주소를 알면 그 위치부터 변수의 크기만큼 메모리를 사용</p>
</li>
<li><p>주소는 &amp; 연산자를 사용해서 구한다.</p>
</li>
<li><p>ex9-1.c 변수의 메모리 주소확인</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int a;             // int형 변수 선언
      double b;          // double형 변수 선언
      char c;            // char형 변수 선언

      printf(&quot;int형 변수의 주소 : %u\n&quot;, &amp;a);
      printf(&quot;double형 변수의 주소 : %u\n&quot;, &amp;b);
      printf(&quot;char형 변수의 주소 : %u\n**&quot;, &amp;**c);

      return 0;
  }
</code></pre>
<pre><code>  /tmp/tmpawd_5xtv.c: In function ‘main’:
  /tmp/tmpawd_5xtv.c:12:41: warning: format ‘%u’ expects argument of type ‘unsigned int’, but argument 2 has type ‘char *’ [-Wformat=]
       printf(&quot;char형 변수의 주소 : %u\n&quot;, &amp;c);
                                          ~^     ~~
                                          %s

  char형 변수의 주소 : 3201099199
</code></pre><ul>
<li>주소 : 변수가 할당된 메모리 공간의 시작주소</li>
</ul>
</li>
<li><p>실행후 남아 있는 메모리를 활용하므로 주소는 저마다 다르다.</p>
</li>
<li><p>출력후 변환문자가 맞지 않아 경고 메시지가 나오지만 실행은 잘됩니다.</p>
</li>
</ul>
<h3 id="메모리-주소의-출력변환-문자">메모리 주소의 출력변환 문자</h3>
<ul>
<li><p>주소를 출력할 때는 전용 변환문자인 %p를 사용하세요</p>
</li>
<li><p>수정된 프로그램</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      //int a;             // int형 변수 선언
      //double b;          // double형 변수 선언
      //char c;            // char형 변수 선언

      //printf(&quot;int형 변수의 주소 : %p\n&quot;, &amp;a);
      //printf(&quot;double형 변수의 주소 : %p\n&quot;, &amp;b);
      printf(&quot;char형 변수의 주소 : %p\n&quot;, &amp;c);

      return 0;
  }
</code></pre>
<pre><code>  /tmp/tmpy8kyph1l.c: In function ‘main’:
  /tmp/tmpy8kyph1l.c:9:40: warning: format ‘%p’ expects argument of type ‘void *’, but argument 2 has type ‘int *’ [-Wformat=]
       printf(&quot;int형 변수의 주소 : %p\\n&quot;, &amp;a);
                                         ~^     ~~
                                         %ls

  int형 변수의 주소 : 0xbe9ce5bc
  char형 변수의 주소 : 0xbe9ce5bb
</code></pre></li>
</ul>
<h3 id="포인터의-간접-참조-연산자----⇒-포인터-연산자">포인터의 <strong>간접 참조 연산자 : *  ⇒ 포인터 연산자</strong></h3>
<ul>
<li><p>메모리 주소를 활용하기</p>
</li>
<li><p>포인터가 변수의 메모리 주소를 저장하는 변수</p>
</li>
<li><p>선언할때 변수 앞에 * 붙입니다.</p>
</li>
<li><p>ex9-2.c 포인터의 선언과 사용</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int a;        // 일반 변수 선언  age
      int* pa, pb;      // 포인터 선언  ptr

      pa = &amp;a;      // 포인터에 a의 주소 대입

      *pa = 10;     // 포인터로 변수 a에 10 대입

      printf(&quot;포인터로 a 값 출력 : % d\n&quot;, *pa);
      printf(&quot;변수명으로 a 값 출력 : % d\n&quot;, a);    // 변수 a 값 출력

      return 0;
  }
</code></pre>
<pre><code>  포인터로 a 값 출력 :  10
  변수명으로 a 값 출력 :  10
</code></pre></li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e0a66e13-783b-4f0c-9ea7-4e2389468ff2/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/47070f58-4371-4f60-8815-fb0f22b73d36/image.png" /></p>
<h3 id="여러가지-포인터-사용해보기">여러가지 포인터 사용해보기</h3>
<ul>
<li><p>ex9-3.c 포인터를 사용한 두 정수의 합과 평균 계산</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int a = 10, b = 15, total;      // 변수 선언과 초기화
      double avg;                     // 평균을 저장할 변수

      int *pa, *pb;                  // 포인터 동시 선언

      int *pt = &amp;total;               // 포인터 선언과 초기화
      double *pg = &amp;avg;              // double형 포인터 선언과 초기화

      pa = &amp;a;                        // 포인터 pa에 변수 a의 주소 대입
      pb = &amp;b;

      *pa=11;
      *pb=16;                       // 포인터 pb에 변수 b의 주소 대입

      *pt = *pa + *pb;                // a 값과 b 값을 더해 total에 저장
      *pg = *pt / 2.0;                // total 값을 2로 나눈 값을 avg에 저장

      printf(&quot;두 정수의 값 : %d, %d\n&quot;, a, b);
      printf(&quot;두 정수의 값 : %d, %d\n&quot;, *pa, *pb);   // a 값과 b 값 출력
      printf(&quot;두 정수의 합 : %d\n&quot;, *pt);            // total 값 출력
      printf(&quot;두 정수의 평균 : %.1lf\n&quot;, *pg);       // avg 값 출력

      return 0;
  }
</code></pre>
<pre><code>  두 정수의 값 : 11, 16
  두 정수의 값 : 11, 16
  두 정수의 합 : 27
  두 정수의 평균 : 13.5</code></pre></li>
<li><p>선언할때 포인터 연산자 *의 위치는 어디에 붙어도 상관없습니다.</p>
</li>
</ul>
<h3 id="const를-사용한-포인터">const를 사용한 포인터</h3>
<ul>
<li><p>const예약어를 포인터로 사용하면 이를 가리키는 변수의 값을 바꿀 수가 없다.</p>
</li>
<li><p>변수에 사용하는 것과는 다른 의미</p>
</li>
<li><ul>
<li>그러나 아래 예제는 const를 붙이나 빼나 결과는 같다</li>
</ul>
</li>
<li><p>9-4.c 포인터에 const사용</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int a = 10, b = 20;
      const int* pa = &amp;a;                // 포인터 pa는 변수 a를 가리킨다.

      printf(&quot;변수 a 값 : %d\n&quot;, *pa);   // 포인터를 간접 참조하여 a 출력
      pa = &amp;b;                           // 포인터가 변수 b를 가리키게 한다.
      printf(&quot;변수 b 값 : %d\n&quot;, *pa);   // 포인터를 간접 참조하여 b 값 출력
      pa = &amp;a;                           // 포인터가 다시 변수 a를 가리킨다.
      a = 30;                            // a를 직접 참조하여 값을 바꾼다.

          //*pa=30
      printf(&quot;변수 a 값 : %d\n&quot;, *pa);   // 포인터로 간접 참조하여 바뀐 값 출력

      return 0;
  }
</code></pre>
<pre><code>  변수 a 값 : 10
  변수 b 값 : 20
  변수 a 값 : 30
</code></pre></li>
</ul>
<h3 id="포인터에-사용된-const의-의미는">포인터에 사용된 const의 의미는?</h3>
<ul>
<li>pa가 가리키는 변수 a는 pa를 간접 참조하여 바꿀 수 없다</li>
<li>const를 사용하는 대표적인 예는 문자열 상수를 인수로 받는 함수.</li>
</ul>
<hr />
<h3 id="9-2-포인터-완전-정복을-위한-포인터-이해하기">9-2 포인터 완전 정복을 위한 포인터 이해하기</h3>
<ul>
<li>언제든지 다른 주소를 저장</li>
<li>포인터끼리 대입</li>
<li>엄격한 기준이 적용.</li>
</ul>
<h3 id="주소와-포인터의-차이">주소와 포인터의 차이</h3>
<ul>
<li>주소는 변수에 할당된 메모리 저장공간의 시작 주소 값 자체.</li>
<li>포인터는 그 값을 저장하는 또 다른 메모리 공간</li>
<li>특정 변수의 주소값은 바뀌지 않지만, 포인터는 다른 주소를 대입하여 그 값을 바꿀 수 있다.</li>
<li>주소도 포인터처럼 간접 참조 연산자를 쓸수 있지만 상수이므로 대입연산자 왼쪽에 올수 없다.</li>
</ul>
<h3 id="주소와-포인터의-크기">주소와 포인터의 크기</h3>
<ul>
<li><p>저장할 주소의 크기에 따라 결정된다.</p>
</li>
<li><p>포인터의 크기는 컴파일러에 따라 다를 수 있다.</p>
</li>
<li><p>ex9-5.c주소와 포인터의 크기</p>
<pre><code class="language-c">
  #include &lt;stdio.h&gt;

  int main(void)
  {
      char ch;
      int in;
      double db;

      char *pc = &amp;ch;
      int *pi = &amp;in;
      double *pd = &amp;db;

      printf(&quot;char형 변수의 주소 크키 : %d\n&quot;, sizeof(&amp;ch));
      printf(&quot;int형 변수의 주소 크기 : %d\n&quot;, sizeof(&amp;in));
      printf(&quot;double형 변수의 주소 크기 : %d\n\n&quot;, sizeof(&amp;db));

      printf(&quot;char *포인터의 크기 : %d\n&quot;, sizeof(pc));
      printf(&quot;int *포인터의 크기 : %d\n&quot;, sizeof(pi));
      printf(&quot;double *포인터의 크기 : %d\n\n&quot;, sizeof(pd));

      printf(&quot;char *포인터가 가리키는 변수의 크기 : %d\n&quot;, sizeof(*pc));
      printf(&quot;int *포인터가 가리키는 변수의 크기 : %d\n&quot;, sizeof(*pi));
      printf(&quot;double *포인터가 가리키는 변수의 크기 : %d\n\n&quot;, sizeof(*pd));

      return 0;

  }</code></pre>
<pre><code class="language-c">  윈도우에서의 결과 (x86에서 컴파일 했기에..)
  ==================
  char형 변수의 주소 크기 : 4
  int형 변수의 주소 크기 : 4
  double형 변수의 주소 크기 : 4
  char * 포인터의 크기 : 4
  int * 포인터의 크기 : 4
  double * 포인터의 크기 : 4
  char * 포인터가 가리키는 변수의 크기 : 1
  int * 포인터가 가리키는 변수의 크기 : 4
  double * 포인터가 가리키는 변수의 크기 : 8
</code></pre>
<pre><code class="language-c">  우분투에서의 결과
  ==================
  int형 변수의 주소 크기 : 8
  double형 변수의 주소 크기 : 8
  char * 포인터의 크기 : 8
  int * 포인터의 크기 : 8
  double * 포인터의 크기 : 8
  char * 포인터가 가리키는 변수의 크기 : 1
  int * 포인터가 가리키는 변수의 크기 : 4
  double * 포인터가 가리키는 변수의 크기 : 8</code></pre>
</li>
</ul>
<h3 id="포인터의-대입-규칙">포인터의 대입 규칙</h3>
<ul>
<li><input disabled="" type="checkbox" /> 포인터는 가리키는 변수의 형태가 같을 때만 대입해야 합니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/41db8cb2-b4cb-456b-a793-0a6c2842e8bf/image.png" /></p>
<ul>
<li><p>ex9-6.c 허용되지 않는 포인터의 대입</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int a = 10;             // 변수 선언과 초기화
      int* p = &amp;a;            // 포인터 선언과 동시에 a를 가리키도록 초기화
      double* pd;             // double형 변수를 가리키는 포인터

      pd = p;                 // 포인터 p 값을 포인터 pd에 대입
      printf(&quot;%lf\n&quot;, *pd);   // pd가 가리키는 변수의 값 출력

      return 0;
  }
</code></pre>
<pre><code>  /tmp/tmpfiqih3qp.c: In function ‘main’:
  /tmp/tmpfiqih3qp.c:9:8: warning: assignment to ‘double *’ from incompatible pointer type ‘int *’ [-Wincompatible-pointer-types]
       pd = p;                 // 포인터 p 값을 포인터 pd에 대입
          ^

  -0.000001
</code></pre></li>
</ul>
<h3 id="형변환을-사용한-포인터의-대입은-언제나-가능합니다">형변환을 사용한 포인터의 대입은 언제나 가능합니다.</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a867c01c-5643-4659-95af-a6e084e98c36/image.png" /></p>
<pre><code class="language-c">#include &lt;stdio.h&gt;

int main(void)
{
    double a = 3.4;
    double* pd = &amp;a;
    int *pi;
    pi=(int*)pd;

    //*pi = (int)*pd;  =&gt; 3.5를 3으로 형변환

    printf(&quot;%u\n&quot;, *pi);

    return 0;
}
</code></pre>
<pre><code>858993459
</code></pre><h2 id="포인터를-사용하는-이유">포인터를 사용하는 이유</h2>
<ul>
<li><p>임베디드 프로그래밍을 할 때 메모리에 직접 접근하는 경우</p>
</li>
<li><p>동적 메모리를 사용하는 경우에는 포인터가 필요함.</p>
<ul>
<li>문자열 인 경우/ 배열을 사용하면 / 사용하지 않는  메모리가 생기지만 포인터는 그렇지 않다.</li>
</ul>
</li>
<li><p>ex9-7.c 두 변수의 값을 바꾸며 포인터 이해하기</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void swap(int* pa, int* pb);   // 두 변수의 값을 바꾸는 함수의 선언

  int main(void)
  {
      int a = 10, b = 20;        // 변수 선언과 초기화

      swap(&amp;a, &amp;b);              // a, b의 주소를 인수로 주고 함수 호출
      printf(&quot;a: %d, b : %d\n&quot;, a, b);   // 변수 a, b 출력

      return 0;
  }

  void swap(int* pa, int* pb)    // 매개변수로 포인터 선언
  {
      int temp;                  // 교환을 위한 임시 변수

      temp = *pa;                // temp에 pa가 가리키는 변수의 값 저장
      *pa = *pb;                 // pa가 가리키는 변수에 pb가 가리키는 변수의 값 저장
      *pb = temp;                // pb가 가리키는 변수에 temp 값 저장
  }
</code></pre>
<pre><code>  a: 20, b : 10
</code></pre></li>
<li><p>ex9-8.c 포인터 없이 두 변수의 값을 바꾸는 함수는 불가능한가?</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void swap(void);                   // 두 변수의 값을 바꾸는 함수 선언

  int main(void)
  {
      int a = 10, b = 20;            // 변수 선언과 초기화

      swap();                        // 인수 없이 함수 호출
      printf(&quot;a:%d, b:%d\n&quot;, a, b);  // 변수 a, b 출력

      return 0;
  }

  void swap(void)                    // 인수가 없으므로 매개변수도 없음
  {
      int temp;                      // 교환을 위한 변수

      temp = a;                      // temp에 main 함수의 a 값 저장
      a = b;                         // main 함수의 a에 main 함수의 b 값 저장
      b = temp;                      // main 함수의 b에 temp 값 저장
  }
</code></pre>
<pre><code>  /tmp/tmpcjtbfwrq.c: In function ‘swap’:
  /tmp/tmpcjtbfwrq.c:19:12: error: ‘a’ undeclared (first use in this function)
       temp = a;                      // temp에 main 함수의 a 값 저장
              ^
  /tmp/tmpcjtbfwrq.c:19:12: note: each undeclared identifier is reported only once for each function it appears in
  /tmp/tmpcjtbfwrq.c:20:9: error: ‘b’ undeclared (first use in this function)
       a = b;                         // main 함수의 a에 main 함수의 b 값 저장
           ^
  [C kernel] GCC exited with code 1, the executable will not be executed
</code></pre></li>
<li><p>ex9-9.c 변수의 값을 인수로 주는 경우</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void swap(int x, int y);            // 두 변수의 값을 바꾸는 함수 선언

  int main(void)
  {
      int a = 10, b = 20;             // 변수 선언과 초기화

      swap(a, b);                     // a, b의 값을 복사해서 전달
      printf(&quot;a:%d, b:%d\n&quot;, a, b);   // 변수 a, b 출력

      return 0;
  }

  void swap(int x, int y)             // 인수 a, b의 값을 x, y에 복사해서 저장
  {
      int temp;                       // 교환을 위한 변수

      temp = x;                       // temp에 x 값 저장
      x = y;                          // x에 y 값 저장
      y = temp;                       // y에 temp 값 저장
  }
</code></pre>
<pre><code>  a:10, b:20
</code></pre></li>
</ul>