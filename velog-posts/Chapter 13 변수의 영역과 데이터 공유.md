<h2 id="13-1-변수-사용-영역">13-1 변수 사용 영역</h2>
<h3 id="지역-변수">지역 변수</h3>
<ul>
<li>auto 예약어와 함께 선언할 수 있지만, 생략 가능하다.</li>
<li>지역 변수 = 자동 변수</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4c987c8c-d13e-4036-a148-0605b1c8d594/image.png" /></p>
<ul>
<li><p>ex13-1.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void assign(void);     // 함수 선언

  int main(void)
  {
      auto int a = 0;    // 지역 변수 선언과 초기화, auto는 생략 가능

      assign();          // 함수 호출
      printf(&quot;main 함수 a : %d\n&quot;, a);

      return 0;
  }

  void assign(void)
  {
      int a;             // main 함수에 있는 변수와 같은 이름의 지역 변수, auto 생략

      a = 10;            // assign 함수 안에 선언된 a에 대입
      printf(&quot;assign 함수 a : %d\n&quot;, a);    // assign 함수에 선언된 a 값 출력
  }</code></pre>
<pre><code class="language-c">  assign 함수 a : 10
  main 함수 a : 0</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/7491d47d-b3a3-4ce3-ad05-cae8431b201e/image.png" /></p>
<ul>
<li>지역 변수는 선언된 함수(블록) 안에서만 사용할 수 있다.<ul>
<li>디버깅에 유리하다.</li>
</ul>
</li>
<li>선언된 블록이 끝나면 저장 공간이 메모리에서 사라진다.<ul>
<li>메모리를 효율적으로 사용한다.</li>
</ul>
</li>
</ul>
<ul>
<li>지역 변수는 이름이 같아도 선언된 함수가 다르면 각각 독립된 저장 공간을 갖는다.</li>
<li>함수의 매개변수는 지역변수입니다.</li>
</ul>
<h3 id="블록-안에서-사용하는-지역-변수">블록 안에서 사용하는 지역 변수</h3>
<ul>
<li><p>특정 블록 안에 변수를 선언하면 사용범위가 블록 내부로 제한 됩니다.</p>
</li>
<li><p>ex13-2.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int a = 10, b = 20;

      printf(&quot;교환 전 a와 b의 값 : %d, %d\n&quot;, a, b);
      {                // 블록 시작
          int temp;    // temp 변수 선언

          temp = a;
          a = b;       // a와 b는 5행에 선언된 변수
          b = temp;
      }                // 블록 끝
      printf(&quot;교환 후 a와 b의 값 : %d, %d\n&quot;, a, b);

      return 0;
  }</code></pre>
<pre><code class="language-c">  교환 전 a와 b의 값 : 10, 20
  교환 후 a와 b의 값 : 20, 10</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/1f9b3cf5-a946-42a7-94e5-ee4a32d86bf9/image.png" /></p>
<ul>
<li>사용 가능한 변수가 둘 이상이면 가장 가까운 블록에 선언된 변수를 사용한다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/a7b3f1a0-1dd8-4de7-9b45-7f3fd09880fd/image.png" /></p>
<pre><code>지양하는게 좋다.</code></pre><h3 id="전역-변수">전역 변수</h3>
<ul>
<li><p>함수 밖에서 선언하면 전역변수</p>
</li>
<li><p>프로그램 전체에서 사용가능</p>
</li>
<li><p>ex13-3.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void assign10(void);
  void assign20(void);

  int a;                   // 전역 변수 선언

  int main(void)
  {
      printf(&quot;함수 호출 전 a 값 : % d\n&quot;, a);  // 전역 변수 a 출력

      assign10();
      assign20();

      printf(&quot;함수 호출 후 a 값 : % d\n&quot;, a);  // 전역 변수 a 출력   

      return 0;
  }

  void assign10(void)
  {
      a = 10;              // 전역 변수 a에 10 대입
  }

  void assign20(void)
  {
      int a;               // 전역 변수와 같은 이름의 지역 변수 선언

      a = 20;              // 지역 변수 a에 20 대입
  }</code></pre>
<pre><code class="language-c">  함수 호출 전 a 값 : 0
  함수 호출 후 a 값 : 10</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/f8ea6d15-8105-4706-9ff1-c898b8ac27a4/image.png" /></p>
<ul>
<li><input disabled="" type="checkbox" /> 전역 변수와 같은 이름의 지역변수</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/e9ffee21-fa04-419c-b875-25f7bdd14a95/image.png" /></p>
<ul>
<li><input disabled="" type="checkbox" /> 전역변수의 문제점</li>
<li>이름이 바뀌면 사용 함수의 모든 이름을 찾아 바꿔야 한다.</li>
<li>값이 이상하면 접근 가능한 모든 함수를 살펴야 한다. ⇒ 변경 점은 한 곳으로 모은다.</li>
<li>같은 이름의 지역 변수에 의해 사용 범위가 제한 된다</li>
</ul>
<h3 id="정적-지역-변수">정적 지역 변수</h3>
<ul>
<li><p>일반 지역 변수처럼 사용 범위가 블록 내부로 제한되지만 선언된 함수가 반환되더라도 저장 공간을 계속 유지한다.</p>
</li>
<li><p>하나의 함수가 여러 번 호출되는 경우 같은 변수를 공유하는 것이 가능하다.</p>
</li>
<li><p>프로그램이 끝날 때까지 저장 공간을 유지하면서 특정 함수에서만 쓰는 경우 유용하다.</p>
</li>
<li><p>13-4.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void auto_func(void);     // auto_func 함수 선언
  void static_func(void);   // static_func 함수 선언

  int main(void)
  {
      int i;

      printf(&quot;정적 지역 변수(static)를 사용한 함수...\n&quot;);
      for (i = 0; i &lt; 3; i++)
      {
          static_func();
      }
      printf(&quot;일반 지역 변수(auto)를 사용한 함수...\n&quot;);
      for (i = 0; i &lt; 3; i++)
      {
          auto_func();
      }
      return 0;
  }

  void static_func(void)
  {
      static int a;         // 정적 지역 변수 선언

      a++;                  // a 값 1 증가
      printf(&quot;%d\n&quot;, a);    // a 출력
  }
  void auto_func(void)
  {
      auto int a = 0;       // 지역 변수 선언과 초기화

      a++;                  // a 값 1 증가
      printf(&quot;%d\n&quot;, a);    // a 출력
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/af79013e-e942-4c1d-bf8b-bc5107071a2f/image.png" /></p>
<h2 id="static-이-함수-변수-앞에-있을-때"><strong>static 이 함수, 변수 앞에 있을 때</strong></h2>
<h2 id="1-변수-앞에-static">1. 변수 앞에 static</h2>
<ul>
<li><p><strong>함수 내부(static 지역 변수)</strong></p>
<ul>
<li><p>변수가 선언된 함수 안에서만 사용할 수 있습니다.</p>
</li>
<li><p>함수가 끝나도 값이 사라지지 않고, 프로그램이 종료될 때까지 메모리에 남아 있습니다.</p>
</li>
<li><p>함수가 다시 호출되어도 이전 값이 유지됩니다<a href="https://blog-of-gon.tistory.com/103">1</a><a href="https://tgmalacom.tistory.com/27">4</a><a href="https://www.php.cn/ko/faq/683802.html">5</a><a href="https://seok-factory.tistory.com/4">7</a>.</p>
<p>```c
void func() {
  static int count = 0;
  count++;
  printf(&quot;%d\n&quot;, count);
}</p>
</li>
<li><p>// func()를 여러 번 호출하면 count 값이 계속 증가합니다.*</p>
<pre><code></code></pre></li>
</ul>
</li>
<li><p><strong>함수 밖(static 전역 변수)</strong></p>
<ul>
<li><p>전역 변수에 static을 붙이면, 해당 파일 내에서만 접근할 수 있습니다.</p>
</li>
<li><p>다른 파일에서는 이 변수를 사용할 수 없습니다(링크 제한)<a href="https://jeongchul.tistory.com/791">3</a><a href="https://tgmalacom.tistory.com/27">4</a><a href="https://www.php.cn/ko/faq/683802.html">5</a><a href="https://velog.io/@mysprtlty/C%EC%97%90%EC%84%9C-static-%ED%82%A4%EC%9B%8C%EB%93%9C%EB%8A%94-%EB%91%90%EA%B0%80%EC%A7%80-%EC%9A%A9%EB%8F%84%EB%A1%9C-%EC%82%AC%EC%9A%A9%EB%90%9C%EB%8B%A4">8</a>.</p>
<p>```c
static int file_var = 10;</p>
</li>
<li><p>// 이 변수는 선언된 파일 내에서만 접근 가능*</p>
<pre><code>
```c
extern int file_ver;
file_ver=20;</code></pre></li>
</ul>
</li>
</ul>
<h2 id="2-함수-앞에-static">2. 함수 앞에 static</h2>
<ul>
<li><p><strong>static 함수</strong></p>
<ul>
<li><p>함수에 static을 붙이면, 그 함수는 선언된 파일 내에서만 호출할 수 있습니다.</p>
</li>
<li><p>다른 파일에서 extern으로 선언해도 접근할 수 없습니다.</p>
</li>
<li><p>주로 내부적으로만 사용하는 함수(캡슐화)에 사용합니다<a href="https://jeongchul.tistory.com/791">3</a><a href="https://tgmalacom.tistory.com/27">4</a><a href="https://code-giraffe.tistory.com/47">6</a><a href="https://velog.io/@mysprtlty/C%EC%97%90%EC%84%9C-static-%ED%82%A4%EC%9B%8C%EB%93%9C%EB%8A%94-%EB%91%90%EA%B0%80%EC%A7%80-%EC%9A%A9%EB%8F%84%EB%A1%9C-%EC%82%AC%EC%9A%A9%EB%90%9C%EB%8B%A4">8</a>.</p>
<pre><code class="language-c">static void helper() {
  *// 이 함수는 같은 파일 내에서만 호출 가능*
}</code></pre>
</li>
</ul>
</li>
</ul>
<h2 id=""></h2>
<h3 id="레지스터-변수">레지스터 변수</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/664ff5de-291c-4762-894a-d91ebf8639c9/image.png" /></p>
<ul>
<li><p>레지스터 변수는 변수가 CPU 레지스터만 사용하므로 메모리에는 생성되지 않습니다.</p>
</li>
<li><p>따라서 &amp;로 메모리 주소를 구할 수 없습니다.</p>
</li>
<li><p>단, 레지스터 변수에 메모리 주소는 저장할 수 있으므로 역참조 연산자 *를 사용할 수 있습니다.</p>
</li>
<li><p>레지스터 변수는 데이터 처리 속도가 빨라 반복 횟수가 매우 많을 때 유용합니다.</p>
</li>
<li><p>vs2022에서는 동작 안 하는데?</p>
<p>  <strong>register 키워드는 최신 C/C++ 컴파일러(특히 Visual Studio 2022)에서 더 이상 동작하지 않습니다.</strong></p>
<ul>
<li><p><strong><code>register int i = 10;</code></strong>처럼 코드를 작성해도,</p>
<p>  <strong>컴파일러가 register 키워드를 무시하거나 경고/오류를 출력</strong>합니다.</p>
</li>
<li><p>register 키워드는 원래 &quot;이 변수는 CPU 레지스터에 저장해달라&quot;는 <em>컴파일러에 대한 힌트</em>였으나,</p>
<p>  최신 컴파일러들은 자체적으로 최적화를 수행하므로, 이 힌트가 더 이상 필요하지 않습니다.</p>
</li>
<li><p>C++17(그리고 C11 표준 이후)부터는 <strong>register 키워드가 공식적으로 폐지(deprecated)</strong>되었습니다.</p>
<blockquote>
<p>즉, Visual Studio 2022(또는 최신 C/C++ 컴파일러)에서 register 키워드를 '되게' 할 방법은 없습니다.그냥 일반 변수 선언(int i = 10;)으로 사용하면 됩니다.</p>
</blockquote>
</li>
</ul>
</li>
<li><p>13-5.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      register int i;                // 레지스터 변수
      auto int sum = 0;              // auto 지역 변수

      for (i = 1; i &lt;= 10000; i++)   // 반복 과정에서 i를 계속 사용함
      {
          sum += i;                  // i 값을 반복하여 누적
      }

      printf(&quot;%d\n&quot;, sum);

      return 0;
  }</code></pre>
</li>
</ul>
<ul>
<li><input disabled="" type="checkbox" /> 레지스터 변수 사용 시 주의 점</li>
<li>전역 변수는 레지스터 변수로 선언할 수 없다. - 저장 공간을 CPU에서 잠깐 빌리기 때문</li>
<li>레지스터 변수는 주소를 구할 수 없다. - 메모리에 없기 때문</li>
<li>레지스터의 사용 여부는 컴파일러가 활용성을 판단하고 결정한다.</li>
</ul>
<hr />
<h3 id="키워드로-끝내는-핵심-포인트">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>지역 변수의 사용 범위는 블록으로 제한된다.</li>
<li>지역 변수와 전역 변수의 사용 범위가 겹치면 지역 변수를 먼저 사용한다.</li>
<li>지역 변수에 static을 사용해서 정적 지역 변수로 만들면 프로그램의 시작부터 종료까지 저장 공간이 유지된다.</li>
<li>레지스터 변수는 컴파일러가 레지스터에 생성할지 말지를 결정한다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/d22873e4-cc40-443d-a357-f1a11020e6ee/image.png" /></p>
<h2 id="13-2-함수의-데이터-공유-방법">13-2 함수의 데이터 공유 방법</h2>
<h3 id="값을-복사해서-전달하는-방법">값을 복사해서 전달하는 방법</h3>
<ul>
<li><p>13-6.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void add_ten(int a);      // 함수 선언

  int main(void)
  {
      int a = 10;

      add_ten(a);           // a 값을 복사하여 전달
      printf(&quot;a : %d\n&quot;, a);

      return 0;
  }

  void add_ten(int a)       // 7행의 a와 다른 독립적인 저장 공간 할당
  {
      a = a + 10;           // 15행의 매개변수 a에 10을 더한다.
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/12ab9082-edd0-4433-8dbb-f2fa3ee521b8/image.png" /></p>
<pre><code>- 지역변수 및 전역변수

    **지역변수**

    블럭 안에 선언하여, 블럭 안에서만 사용한다.

    블럭이 끝나면 변수도 사라진다.

    선언시의 초기값은 어떤 값일지 모른다.

    **전역변수**

    블럭 밖에 선언하여 전체 함수에서 사용한다.

    프로그램이 종료될 때 사라진다.

    선언시의 초기값은 0이다.</code></pre><h3 id="주소를-전달하는-방법">주소를 전달하는 방법</h3>
<ul>
<li><p>ex13-7.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  void add_ten(int* pa);       // 매개변수로 포인터 pa 선언

  int main(void)
  {
      int a = 10;

      add_ten(&amp;a);             // a의 주소를 인수로 준다.
      printf(&quot;a : %d\n&quot;, a);   // 증가된 a 값 출력

      return 0;
  }

  void add_ten(int* pa)        // 포인터 pa가 a의 주소를 받는다.
  {
      *pa = *pa + 10;          // 포인터 pa가 가리키는 변수의 값 10 증가
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/3e710473-a10a-4b95-b1bb-f235e718c35c/image.png" /></p>
<ul>
<li><p>정적 변수</p>
<p>  <strong>선언은 —&gt;  static 자료형 변수명;</strong></p>
<p>  변수의 선언은 단 한번만 실행된다.</p>
<p>  블럭이 끝나도 사라지지 않는다.</p>
<p>  초기값을 넣어주지 않아도 0으로 초기화된다.</p>
<p>  블럭 밖에서는 이 변수를 사용할 수 없다.</p>
</li>
</ul>
<ul>
<li><input disabled="" type="checkbox" /> 값을 복사하여 전달하는 방식 vs 주소를 전달하는 방식<ul>
<li>값을 복사 ⇒ 원본 데이터를 보존 안정성 담보</li>
<li>주소를 전달 ⇒ 원본데이터 수정에 유용, 사용법 복잡</li>
</ul>
</li>
<li><input disabled="" type="checkbox" /> C언어에서 call by value vs call by reference<ul>
<li>C언에서는 call by reference 개념 없음</li>
</ul>
</li>
</ul>
<h3 id="주소를-반환하는-함수">주소를 반환하는 함수</h3>
<ul>
<li><p>반환 값이 있는 함수는 호출한 함수로 값을 복사해서 반환합니다.</p>
</li>
<li><p>함수 안에서 사용한 지역 변수는 함수가 반환 되면 저장공간이 사라지므로 그 값을 복사하여 반환해야 호출한 함수에서 사용 할 수 있습니다.</p>
</li>
<li><p>ex 13-8.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int* sum(int a, int b);   // int형 변수의 주소를 반환하는 함수 선언

  int main(void)
  {
      int* resp;            // 반환값을 저장할 포인터 resp(result pointer)

      resp = sum(10, 20);   // 반환된 주소는 resp에 저장

      printf(&quot;두 정수의 합 : %d\n&quot;, *resp);   // resp가 가리키는 변숫값 출력

      return 0;
  }

  int* sum(int a, int b)    // int형 변수의 주소를 반환하는 함수
  {
      static int res;       // 정적 지역 변수

      res = a + b;          // 두 정수의 합을 res(result)에 저장

      return &amp;res;          // 정적 지역 변수의 주소 반환
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/57daa755-06ed-4a03-9d28-d9c27947cd80/image.png" /></p>
<ul>
<li><input disabled="" type="checkbox" /> 주소를 반환하는 함수를 만들 때 주의 해야 할 것<ul>
<li>반환 값의 자료형은 반환 값을 저장할 포인터의 자료형과 같아야 합니다.</li>
<li>지역 변수의 주소를 반환해서는 안 됩니다.</li>
</ul>
</li>
</ul>
<hr />
<h3 id="메모리-구조에서-스택-힙-데이타영역-구분하고-예제로-정리하기">메모리 구조에서 스택, 힙, 데이타영역 구분하고 예제로 정리하기</h3>
<ul>
<li>메모리 구조</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/fd54208a-a33e-47ac-b500-7f66280d63a6/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/7e7a153c-008f-44a9-bbf9-809376af513d/image.png" /></p>
<ul>
<li>Code<ul>
<li>코드 자체를 구성하는 메모리 영역.</li>
</ul>
</li>
<li>Data<ul>
<li>전역변수(global), 정적변수(static), 배열(array), 구조체(structure) 등이 저장된다.</li>
</ul>
</li>
<li>Heap<ul>
<li>메모리 주소 값에 의해서만 참조되고 사용되는 영역이다.</li>
<li>이 공간에 메모리 할당하는 것을 동적 할당(Dynamic Memory Allocation)이라고 부른다.</li>
<li>동적 할당 된 메모리들은 프로세스가 종료되면 메모리 리소스가 반납 되기 때문에 그 값이 사라진다. 그러나 프로세스가 종료되기 전까지 동적할당 된 영역은 유지되므로 프로그램이 정해진 힙 영역의 크기를 넘는 메모리 할당을 요구하면 할당되지 않는다.</li>
<li>동적 할당의 장점 : 상황에 따라 메모리 크기를 조절할 수 있기 때문에 경제적이다.</li>
<li>동적 할당의 단점 : 더 이상 사용하지 않을 때 프로그래머가 명시적으로 메모리를 해제하지 않으면 계속 남아있다.</li>
</ul>
</li>
<li>Stack<ul>
<li>지역(local) 변수, 매개변수(parameter), 리턴 값 등 잠시 사용되었다가 사라지는 데이터를 저장하는 영역이다. (정적할당)</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/e95d2428-e0cc-4c04-8859-a4f05d76b3a7/image.png" /></p>
<pre><code>(Last In First Out 방식)

- Heap과 Stack은  Run time시 크기가 결정된다.</code></pre><p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/56239222-3a59-4438-9e66-4f59743d4ba0/image.png" /></p>
<pre><code>- Stack은 지역변수를 사용하고 소멸함, 데이터 용량의 불확실성을 가지기 때문에 밑에서부터 채워올리고, Heap은 위에서부터 채워내려온다.
- Heap Overflow : Heap이 위에서부터 주소를 채워내려오다가 Stack영역을 침범하는것을 말한다.
- Stack Overflow : Stack이 Heap 영역을 침범하는것을 말한다.

([Heap &amp; Stack](https://ghgus0702.tistory.com/11))</code></pre><hr />
<h3 id="키워드로-끝내는-핵심-포인트-1">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>값을 복사해서 전달하면 호출하는 함수의 값은 바뀌지 않는다.</li>
<li>호출하는 함수의 값이 바뀌려면 주소를 인수로 전달해야 한다.</li>
<li>정적 지역 변수나 전역 변수와 같이 함수가 반환 된 후에도 저장 공간이 유지되는 경우만 주소를 반환한다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트-1">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/c51556b1-cc3c-41d4-8722-a4d0dc5278ad/image.png" /></p>