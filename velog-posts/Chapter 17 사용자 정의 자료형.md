<h2 id="17-1-구조체">17-1 구조체</h2>
<ul>
<li>배열은 같은 형태의 데이터를 묶어 반복문으로 처리</li>
<li>배열을 사용하려면 데이터의 형태가 같아야 한다.!!</li>
<li>한 학생의 학번, 이름, 학점처럼 다른 자료형을 하나의 배열로 선언해서 처리하는 것은 안되요...</li>
<li>형태별 학번배열, 이름배열, 학점배열 ⇒ 이상하네!!</li>
</ul>
<h3 id="구조체-선언과-멤버-사용">구조체 선언과 멤버 사용</h3>
<ul>
<li><p>구조체는 하나의 자료형으로 변수 선언이 가능하지만 변수 선언 전 필요한 절차가 있다.</p>
</li>
<li><p>구조체 형태를 컴파일러에게 미리 알려주는 구조체선언을 해야한다.</p>
</li>
<li><p>구조체 선언이 끝나면 새로운 자료형이 만들어지며 이후에 구조체의 변수를 사용할 수 있다.</p>
</li>
<li><p>17-1.c : 구조체를 선언하고 사용하는 방법</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  struct student           // 구조체 선언
  {
      int num;             // int형 멤버
      double grade;        // double형 멤버
  };                       // 세미콜론 사용

  int main(void)
  {
      struct student s1;   // struct student형의 변수 선언

      s1.num = 2;          // s1의 num 멤버에 2 저장
      s1.grade = 2.7;      // s1의 grade 멤버에 2.7 저장
      printf(&quot;학번 : %d\n&quot;, s1.num);       // num 멤버 출력
      printf(&quot;학점 : %.1lf\n&quot;, s1.grade);  // grade 멤버 출력

      return 0;
  }</code></pre>
</li>
<li><p>이름은 구조체의 성격에 맞는 적절한 이름을 붙인다.</p>
</li>
<li><p>블록 안에는 멤버를 나열한다.</p>
</li>
<li><p>멤버선언은 구조체를 구성하는 자료형 종류와 이름을 컴파일러에 알리는 것이며 실제 저장공간이 할당되는 변수선언과는 다르다.</p>
</li>
<li><p>마지막 블록을 닫은 후에는 반드시 세미콜론을 붙인다.</p>
</li>
<li><p>구조체 선언 위치</p>
<ul>
<li>구조체 선언이 main함수 앞에 있으면 프로그램 전체에서 사용할 수 있고, 
함수 안에서 선언하면 함수 안에서만 사용</li>
</ul>
</li>
<li><p>새로 만든 구조체로 변수를 선언할 때는 struct예약어와 구조체 이름을 함께 하나의 자료형 이름으로 사용합니다.</p>
<pre><code class="language-c">  struct student s1;</code></pre>
</li>
<li><p>구조체 변수를 선언하면 비로서 저장 공간이 할당됩니다.</p>
<p>  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/a42e0d5a-f0f2-4236-a83f-8a9e8e8eabf7/image.png" /></p>
</li>
</ul>
<ul>
<li><p>선언된 구조체 변수는 그 안에 여러개의 멤버를 가지므로 특정 멤버를 골라서 사용해야 하는데 이때 별도의 멤버 접근 연산자 . 가 필요합니다.</p>
<p>  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/b1dcbd47-00c6-4f7e-8dba-1626cf20e036/image.png" /></p>
</li>
</ul>
<ul>
<li>위와 같이 사용하면 s1은 구조체 변수지만 s1.num은 int형 변수가 됩니다.</li>
</ul>
<h3 id="구조체-변수의-크기">구조체 변수의 크기</h3>
<ul>
<li>모든 시스템은 데이터를 빠르게 읽고 쓰기 위해 일정한 크기 단위로 메모리에 접근합니다.</li>
<li>컴파일러는 구조체 멤버의 크기가 다를 때 멤버 사이에 패딩 바이트를 넣어 멤버들을 정렬합니다.<br />이를 바이트 얼라이먼트라고 합니다.  ⇒ 시스템마다 다릅니다.</li>
<li>가장 큰 멤버의 메모리를  할당하는 기준 단위가 됩니다.</li>
<li>구조체는 실행 효율을 위해 패딩 바이트를 넣어 바이트 정렬을 한다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/36df144c-df65-41e1-aac2-2717253543fa/image.png" /></p>
<pre><code>17- 1       구조체</code></pre><ul>
<li><p>다음과 같이 pack(1)로 하면 컴파일러에 패딩 바이트를 넣지 않도록 지시 할 수 있다. 
구조체 선언 전에 적어 주건, include다음에 넣어준다.</p>
<ul>
<li><p>포인터 멤버에 대입 연산으로 문자열을 연결할 수 있다.</p>
<pre><code class="language-c">  yumi.intro=&quot;항상 행복하세요&quot;;</code></pre>
<ul>
<li><p>다만 이 경우 문자열 상수 대신 키보드로 문자열을 입력하면 intro멤버는 포인트이므로 문자열을 처리할 공간이 없습니다. 다음과 같이 저장공간을 확보해야합니다.</p>
<pre><code class="language-c">yumi.intro=(char *)malloc(80)</code></pre>
</li>
<li><p>포인터 멤버는 배열 멤버보다 사용하기 더 번거롭다.</p>
</li>
</ul>
<pre><code class="language-c">#pragma pack(1)</code></pre>
</li>
<li><p>멤버의 순서에 따라 구조체의 크기가 달라질 수 있다.</p>
</li>
</ul>
</li>
<li><p>기본자료형 외에 배열, 포인터, 다른 구조체를 멤버로 사용 가능함.</p>
</li>
</ul>
<h3 id="다양한-구조체-멤버">다양한 구조체 멤버</h3>
<ul>
<li><p>17-2.c : 배열과 포인터로 갖는 구조체 사용</p>
<pre><code class="language-c">   #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;
  #include &lt;stdlib.h&gt;
  #include &lt;string.h&gt;

  struct profile         // 신상명세 구조체 선언
  {
      char name[20];     // 이름을 저장할 배열 멤버
      int age;           // 나이
      double height;     // 키
      char* intro;       // 자기소개를 위한 포인터
  };

  int main(void)
  {
      struct profile yuni;                 // profile 구조체 변수 선언

      strcpy(yuni.name, &quot;서하윤&quot;);         // name 배열 멤버에 이름 복사
      yuni.age = 17;                       // age 멤버에 나이 저장
      yuni.height = 164.5;                 // height 멤버에 키 저장

      yuni.intro = (char*)malloc(80);      // 자기소개를 저장할 공간 동적 할당
      printf(&quot;자기소개 : &quot;);
      gets(yuni.intro);                    // 할당한 공간에 자기소개 입력

      printf(&quot;이름 : %s\n&quot;, yuni.name);    // 각 멤버의 데이터 출력
      printf(&quot;나이 : %d\n&quot;, yuni.age);
      printf(&quot;키 : %.1lf\n&quot;, yuni.height);
      printf(&quot;자기소개 : %s\n&quot;, yuni.intro);
      free(yuni.intro);                    // 동적 할당 영역 반환

      return 0;
  }</code></pre>
</li>
</ul>
<h3 id="구조체의-멤버로-다른-구조체-사용하기">구조체의 멤버로 다른 구조체 사용하기</h3>
<ul>
<li><p>struct구조체에 신상명세에 대한 부분이 추가된다면 profile구조체를 활용할 수 있다.</p>
</li>
<li><p>17-3.c : 다른 구조체를 멤버로 갖는 구조체 사용</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  struct profile            // 신상명세 구조체 선언
  {
      int age;              // 나이
      double height;        // 키
  };

  struct student
  {
      struct profile pf;    // profile 구조체를 멤버로 사용
      int id;               // 학번을 저장할 멤버
      double grade;         // 학점을 저장할 멤버
  };

  int main(void)
  {
      struct student yuni;      // student 구조체 변수 선언

      yuni.pf.age = 17;         // pf 멤버의 age 멤버에 나이 저장
      yuni.pf.height = 164.5;   // pf 멤버의 height 멤버에 키 저장
      yuni.id = 315;
      yuni.grade = 4.3;

      printf(&quot;나이 : %d\n&quot;, yuni.pf.age);       // pf 멤버의 age 멤버 출력
      printf(&quot;키 : %.1lf\n&quot;, yuni.pf.height);   // pf 멤버의 height 멤버 출력
      printf(&quot;학번 : %d\n&quot;, yuni.id);           // id 멤버 출력
      printf(&quot;학점 : %.1lf\n&quot;, yuni.grade);     // grade 멤버 출력

      return 0;
  }</code></pre>
<p>  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/8d8c0be7-1b87-4b2b-9de4-4c32b1db4b5e/image.png" /></p>
</li>
</ul>
<ul>
<li><p>profile구조체의 멤버를 사용하려면 멤버접근자 .을 2번 사용 해야 합니다.</p>
<pre><code class="language-c">  yumi.pf.age=17;</code></pre>
<p>  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/5bddace4-16d1-4d5b-8762-ac6fbc0becfc/image.png" /></p>
</li>
</ul>
<h3 id="구조체-변수의-초기화와-대입-연산">구조체 변수의 초기화와 대입 연산</h3>
<ul>
<li><p>구조체 변수도 일반 변수와 같이 선언과 동시에 초기화가 가능.</p>
</li>
<li><p>배열의 초기화와 비슷한 방법 사용.</p>
</li>
<li><p>17-4.c : 최고 학점의 학생 데이터 출력</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  struct student       // 학생 구조체 선언
  {
      int id;          // 학번
      char name[20];   // 이름
      double grade;    // 학점
  };

  int main(void)
  {
      struct student s1 = { 315, &quot;홍길동&quot;, 2.4 },   // 구조체 변수 선언과 초기화
                     s2 = { 316, &quot;이순신&quot;, 3.7 },
                     s3 = { 317, &quot;세종대왕&quot;, 4.4 };

      struct student max;                       // 최고 학점을 저장할 구조체 변수

      max = s1;                               // s1을 최고 학점으로 가정
      if (s2.grade &gt; max.grade) max = s2;    // s2가 더 높으면 max에 대입
      if (s3.grade &gt; max.grade) max = s3;    // s3가 더 높으면 max에 대입

      printf(&quot;학번 : %d\n&quot;, max.id);         // 최고 학점 학생의 학번 출력
      printf(&quot;이름 : %s\n&quot;, max.name);       // 최고 학점 학생의 이름 출력
      printf(&quot;학점 : %.1lf\n&quot;, max.grade);   // 최고 학점 학생의 학점 출력

      return 0;
  }</code></pre>
</li>
<li><p>구조체 변수의 대입은 각 멤버들을 자동으로 다른 구조체 변수에 복사합니다.
  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/6d034e1f-5f1d-4f85-b224-7bfca55bc19b/image.png" /></p>
</li>
</ul>
<ul>
<li><p>구조체는 보통 형선언을 먼저 한 후에 구조체 변수 선언과 초기화를 하며, 다음과 같이 3개를 동시에 하는 것도 가능</p>
<pre><code class="language-c">  struct student
  {
      int id;
      char name[20];
      double grade;
  } s1={315,&quot;홍길동&quot;, 2.4};</code></pre>
</li>
</ul>
<h3 id="구조체-변수를-함수의-매개변수에-사용하기">구조체 변수를 함수의 매개변수에 사용하기</h3>
<ul>
<li><p>구조체 변수는 대입 연산이 가능하므로 함수의 인수로 주거나 함수에서 여러개의 값을 구조체로 묶어 동시에 반환하는 것도 가능하다.</p>
</li>
<li><p>17-5.c : 구조체를 반환하여 두 변수의 값 교환</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  struct vision       // 로봇의 시력을 저장할 구조체
  {
      double left;    // 왼쪽 눈
      double right;   // 오른쪽 눈
  };

  struct vision exchange(struct vision robot);   // 두 시력을 바꾸는 함수

  int main(void)
  {
      struct vision robot;                       // 구조체 변수 선언

      printf(&quot;시력 입력 : &quot;);
      scanf(&quot;%lf%lf&quot;, &amp;(robot.left), &amp;(robot.right));  // 시력 입력
      robot = exchange(robot);                   // 교환 함수 호출
      printf(&quot;바뀐 시력 : %.1lf %.1lf\n&quot;, robot.left, robot.right);

      return 0;
  }

  struct vision exchange(struct vision robot)    // 구조체를 반환하는 함수
  {
      double temp;                   // 교환을 위한 임시 변수

      temp = robot.left;             // 좌우 시력 교환
      robot.left = robot.right;
      robot.right = temp;

      return robot;                  // 구조체 변수 반환
  }</code></pre>
<p>  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/4e6ed962-2e84-4255-8d0e-c8d7d6e6630c/image.png" /></p>
</li>
</ul>
<ul>
<li><p>바뀐 robot의 값이 반환되면서 main함수의 robot에 복사 되어 결국 main 함수에 있는 robot의 값이 바뀌게 됩니다.</p>
<p>  <img alt="" src="https://s3-us-west-2.amazonaws.com/secure.notion-static.com/4d005ead-8ab0-4141-ba72-187918711e4d/Untitled.png" /></p>
</li>
</ul>
<hr />
<h3 id="키워드로-끝내는-핵심-포인트">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>구조체 변수는 구조체 선언 후에 멤버 접근 연산자 .로 원하는 멤버의 이름을 직접 사용한다.    </li>
<li>구조체는 배열, 포인터, 다른 구조체 등도 멤버로 넣어 확장할 수 있다.</li>
<li>자료형이 같은 구조체 변수는 대입 연산이 가능하며 함수의 매개변수에 쓸 수 있다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/1ecf808a-1c0c-495a-a708-d11b8af8c54f/image.png" /></p>
<hr />
<h2 id="17-2-구조체-활용-공용체-열거형">17-2 구조체 활용, 공용체, 열거형</h2>
<p>구조체는 데이터를 형태가 달라도 하나로 묶을 수 있다.</p>
<p>데이터의 종류가 많을 때는 구조체 변수의 크기가 커지며, 메모리 낭비가 될 수 있다. </p>
<p>이럴 때 공용체(union)를 쓰면 하나의 공간을 여러 멤버가 공유하여 최소한의 메모리만 사용한다. </p>
<h3 id="구조체-포인터와---연산자-arrow-화살표">구조체 포인터와 -&gt; 연산자 (arrow, 화살표)</h3>
<ul>
<li><p>구조체 변수는 그 안에 여러 개의 변수를 멤버로 가질 수 있으나, 그 자신은 단지 하나의 변수이다.</p>
</li>
<li><p>구조체 변수에 주소 연산자를 사용하면 특정 멤버의 주소가 아니라 구조체 변수 전체의 주소를 구합니다.  그 값을 저장할 때는 구조체 포인터를 사용합니다.</p>
</li>
<li><p>17-6.c : 구조체 포인터의 사용</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  struct score        // 구조체 선언
  {
      int kor;        // 국어 점수를 저장할 멤버
      int eng;        // 영어 점수
      int math;        // 수학 점수
  };

  int main(void)
  {
      struct score yuni = { 90, 80, 70 };   // 구조체 변수 선언과 초기화
      struct score* ps = &amp;yuni;             // 구조체 포인터에 주소 저장

      printf(&quot;국어 : %d\n&quot;, (*ps).kor);     // 구조체 포인터로 멤버 접근
      printf(&quot;영어 : %d\n&quot;, ps-&gt;eng);       // -&gt; 연산자 사용
      printf(&quot;수학 : %d\n&quot;, ps-&gt;math);

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/12ed9e20-4c6c-4105-8f26-575f56edf007/image.png" /></p>
<ul>
<li>yuni의 주소로 초기화 ⇒ 구조체 포인터는 가리키는 자료형으로 구조체를 사용하여 선언한다.</li>
<li>yuni는 하나의 변수이므로 주소 연산을 수행하면 구조체 변수 전체의 주소가 구해집니다.</li>
<li>이 값을 구조체 포인터 ps에 저장하면 ps가 구조체 변수 yuni를 가리키게 됩니다.</li>
<li>멤버에 접근하는 . 연산자가 *연산자보다 우선순위가 높다. 따라서 *연산자 먼저 수행할 수 있도록 *연산자에 괄호로 묶습니다.</li>
<li>매번 괄호를 사용하는 것이 번거로우므로 같은 기능으로 → 연산자를 사용합니다.</li>
</ul>
<h2 id="구조체-배열">구조체 배열</h2>
<ul>
<li><p>구조체 변수는 멤버가 여러개지만 구조체 변수 자체는 하나의 변수로 취급</p>
</li>
<li><p>같은 형태의 구조체 변수가 많이 필요하면 배열로 선언 한다.</p>
</li>
<li><p>17-7.c : 구조체 배열을 초기화하고 출력</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  struct address       // 주소록을 만들 구조체 선언
  {
      char name[20];   // 이름을 저장할 멤버
      int age;         // 나이를 저장할 멤버
      char tel[20];    // 전화번호를 저장할 멤버
      char addr[80];   // 주소를 저장할 멤버
  };

  int main(void)
  {
      struct address list[5] = {       // 요소가 5개인 구조체 배열 선언
          {&quot;홍길동&quot;, 23, &quot;111 - 1111&quot;, &quot;울릉도 독도&quot;},
          {&quot;이순신&quot;, 35, &quot;222 - 2222&quot;, &quot;서울 건천동&quot;},
          {&quot;장보고&quot;, 19, &quot;333 - 3333&quot;, &quot;완도 청해진&quot;},
          {&quot;유관순&quot;, 15, &quot;444 - 4444&quot;, &quot;충남 천안&quot;},
          {&quot;안중근&quot;, 45, &quot;555 - 5555&quot;, &quot;황해도 해주&quot;}
      };
      int i;

      for (i = 0; i &lt; 5; i++)          // 배열 요소 수만큼 반복
      {
          printf(&quot;%10s%5d%15s%20s\n&quot;,  // 각 배열 요소의 멤버 출력
              list[i].name, list[i].age, list[i].tel, list[i].addr);
      }

      return 0;
  }</code></pre>
<p>  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/71675aa8-d12e-4217-967f-2b897abe6c25/image.png" /></p>
</li>
</ul>
<pre><code>![](https://velog.velcdn.com/images/kym11290306/post/afc19dd9-9f45-4e6c-aea2-ee7b37dfde57/image.png)</code></pre><h3 id="구조체-배열을-처리하는-함수">구조체 배열을 처리하는 함수</h3>
<ul>
<li><p>구조체 배열은 배열 요소가 구조체 변수일 뿐!!</p>
</li>
<li><p>구조체 배열의 이름은 첫번째 요소의 주소이므로 구조체 변수를 가리킨다.</p>
</li>
<li><p>17-8.c : 함수에서 → 연산자를 사용하여 구조체 배열의 값 출력</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  struct address        // 주소록을 만들 구조체 선언
  {
      char name[20];    // 이름을 저장할 멤버
      int age;          // 나이를 저장할 멤버
      char tel[20];     // 전화번호를 저장할 멤버
      char addr[80];    // 주소를 저장할 멤버
  };

  void print_list(struct address* lp);

  int main(void)
  {
      struct address list[5] = {        // 요소가 5개인 구조체 배열 선언
          {&quot;홍길동&quot;, 23, &quot;111 - 1111&quot;, &quot;울릉도 독도&quot;},
          {&quot;이순신&quot;, 35, &quot;222 - 2222&quot;, &quot;서울 건천동&quot;},
          {&quot;장보고&quot;, 19, &quot;333 - 3333&quot;, &quot;완도 청해진&quot;},
          {&quot;유관순&quot;, 15, &quot;444 - 4444&quot;, &quot;충남 천안&quot;},
          {&quot;안중근&quot;, 45, &quot;555 - 5555&quot;, &quot;황해도 해주&quot;}
      };

      print_list(list);

      return 0;
  }

  void print_list(struct address* lp)   // 매개변수는 구조체 포인터
  {
      int i;                            // 반복 제어 변수

      for (i = 0; i &lt; 5; i++)           // 배열 요소의 개수 만큼 반복
      {
          printf(&quot;%10s%5d%15s%20s\n&quot;,   // 각 배열 요소의 멤버 출력
              (lp + i)-&gt;name, (lp + i)-&gt;age, (lp + i)-&gt;tel, (lp + i)-&gt;addr);
      }
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/ba726c1c-e0c1-4561-9905-ced606ca3329/image.png" /></p>
<ul>
<li><p>배열명은 첫번째 배열요소의 주소이며, 첫번째 배열 요소를 가리킵니다.</p>
</li>
<li><p>세가지 표현은 모두 같은 결과</p>
<ul>
<li><p>배열표현</p>
<pre><code class="language-c">  lp[i].name</code></pre>
</li>
<li><p>포인터표현</p>
<pre><code class="language-c">  *(lp+i).name</code></pre>
</li>
<li><p>→ 연산자 표현</p>
<pre><code class="language-c">  (lp+i)-&gt;name</code></pre>
</li>
</ul>
</li>
</ul>
<h3 id="자기-참조-구조체">자기 참조 구조체</h3>
<ul>
<li><p>개별적으로 할당된 구조체 변수들을 포인터로 연결하면 관련된 데이터를 하나로 묶어 관리할 수 있습니다.  이때 자기 참조 구조체를 사용합니다.</p>
</li>
<li><p>17-9.c : 자기 참조 구조체로 list만들기</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  struct list              // 자기 참조 구조체
  {
      int num;             // 데이터를 저장하는 멤버
      struct list* next;   // 구조체 자신을 가리키는 포인터 멤버
  };

  int main(void)
  {
      struct list a = { 10, 0 }, b = { 20, 0 }, c = { 30, 0 };  // 구조체 변수 초기화
      struct list* head = &amp;a, * current;                        // 헤드 포인터 초기화

      a.next = &amp;b;                        // a의 포인터 멤버가 b를 가리킴
      b.next = &amp;c;                        // b의 포인터 멤버가 c를 가리킴

      printf(&quot;head-&gt;num : %d\n&quot;, head-&gt;num);        // head가 가리키는 a의 num 멤버 사용
      printf(&quot;head-&gt;next-&gt;num : %d\n&quot;, head-&gt;next-&gt;num);    // head로 b의 num 멤버 사용

      printf(&quot;list all : &quot;);
      current = head;                     // 최초 current 포인터가 a를 가리킴
      while (current != NULL)             // 마지막 구조체 변수까지 출력하면 반복 종료
      {
          printf(&quot;%d  &quot;, current-&gt;num);   // current가 가리키는 구조체 변수의 num 출력
          current = current-&gt;next;        // current가 다음 구조체 변수를 가리키도록 함
      }
      printf(&quot;\n&quot;);

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/8f66ad39-2d9d-4061-bee7-2bc1c55ec049/image.png" /></p>
<h3 id="연결리스트">연결리스트</h3>
<ul>
<li><p>구조체 변수를 포인터로 연결한 것을 연결리스트 라고 한다.</p>
</li>
<li><p>연결리스트(링크드 리스트)는 첫번 째 변수의 위치만 알면 나머지 변수는 포인터를 따라가 모두 사용할 수 있으므로 대부분 첫 번째 변수의 위치를 head포인터에 저장해 사용합니다.</p>
<pre><code class="language-c">  struct list *head=&amp;a, *current;</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/2d7c28cc-ef30-4b35-986e-96638e28e2d5/image.png" /></p>
<ul>
<li>head 로 c의 num값 30을 사용하려면 head→next→next→num</li>
<li>head가 길면 head로 모든 값을 찾기 힘들므로 별도의 포인터를 사용합니다.</li>
<li>head포인터의 값은 처음 위치를 찾을 수 있게 바꾸지 않는 게 좋습니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/3e10009e-22f4-45a4-860c-7b72cc1257e8/image.png" /></p>
<h3 id="공용체union">공용체(union)</h3>
<ul>
<li><p>공용체는 선언방식이 구조체와 비슷하지만 공용체는 모든 멤버가 하나의 저장 공간을 같이 사용합니다.</p>
</li>
<li><p>17-10.c : 공용체를 사용한 학번과 학점 데이터 처리</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  union student       // 공용체 선언
  {
      int num;        // 학번을 저장할 멤버
      double grade;   // 학점을 저장할 멤버
  };

  int main(void)
  {
      union student s1 = { 315 };         // 공용체 변수의 선언과 초기화

      printf(&quot;학번 : %d\n&quot;, s1.num);      // 학번 멤버 출력
      s1.grade = 4.4;                     // 학점 멤버에 값 대입
      printf(&quot;학점 : %.1lf\n&quot;, s1.grade);
      printf(&quot;학번 : %d\n&quot;, s1.num);      // 학번 다시 출력

      return 0;
  }</code></pre>
</li>
<li><p>공용체는 예약어 union을 사용, 나머지는 구조체 선언하는 형식과 같다.</p>
</li>
<li><p><strong>공용체 변수의 크기는 멤버 중에서 크기가 가장 큰 멤버로 결정된다.</strong></p>
<pre><code class="language-c">  union student s1={315};</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/a27bb06c-e748-4068-a925-00393ce6b5ce/image.png" /></p>
<pre><code>- 공용체는 저장공간을 공유한다.</code></pre><ul>
<li><p>공용체 변수의 초기화는 중괄호를 사용하여 첫번 째 멤버만 초기화합니다.</p>
<pre><code class="language-c">  union student  sq={315};
  union student  a={.grade=3.4};</code></pre>
</li>
<li><p>공용체 멤버는 언제든지 다른 멤버에 의해 값이 변할 수 있으므로 항상 각 멤버의 값을 확인 해야하는 단점이 있다.  그러나 하나의 메모리를 공유하므로 메모리 절약할 수 있다. 
특히 같은 공간에 저장된 값을 여러가지 형태로 사용이 가능하다.</p>
</li>
</ul>
<h3 id="열거형enum">열거형(enum)</h3>
<ul>
<li><p>구조체와 비슷하게 선언하나, 열거형은 변수에 저장할 수 있는 정수 값을 기호로 정의하여 나열한다.</p>
</li>
<li><p>17-11.c : 열거형을 사용한 프로그램</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  enum season { SPRING, SUMMER, FALL, WINTER };  // 열거형 선언

  int main(void)
  {
      enum season ss;              // 열거형 변수 선언
      char* pc = NULL;             // 문자열을 저장할 포인터

      ss = SPRING;                 // 열거 멤버의 값 대입
      switch (ss)                  // 열거 멤버 판단
      {
          case SPRING:                 // 봄이면
              pc = &quot;inline&quot;; break;    // 인라인 문자열 선택
          case SUMMER:                 // 여름이면
              pc = &quot;swimming&quot;; break;  // 수영 문자열 선택
          case FALL:                   // 가을이면
              pc = &quot;trip&quot;; break;      // 여행 문자열 선택
          case WINTER:                 // 겨울이면
          pc = &quot;skiing&quot;; break;    // 스키 문자열 선택
      }
      printf(&quot;나의 레저 활동 = &gt; %s\n&quot;, pc);     // 선택된 문자열 출력

      return 0;
  }</code></pre>
</li>
<li><p>열거형 선언 : 예약어 enum과 열거형 이름을 짓고 괄호 안에 멤버를 콤마로 나열</p>
<pre><code class="language-c">  enum season {SPRING, SUMMER, FALL, WINTER};</code></pre>
</li>
<li><p>컴파일러는 멤버를 0부터 차례로 하나 씩 큰 정수로 바꾼다.</p>
</li>
<li><p>초기값을 원하는 값으로 다시 설정할 수 있다. - 새로 설정된 멤버 이후의 큰정수로 바뀝니다.</p>
<pre><code class="language-c">  enum season {SPRING=5, SUMMER, FALL=10, WINTER};</code></pre>
</li>
</ul>
<h3 id="typedef를-사용한-형-재정의">typedef를 사용한 형 재정의</h3>
<ul>
<li><p>구조체, 공용체, 열거형의 이름은 항상 struct등의 예약어와 함께 사용 해야 한다.</p>
</li>
<li><p>형 재정의를 통해 자료형을 짧고 쉬운 이름으로 사용할 수 있다.</p>
</li>
<li><p>17-12.c : typedef를 사용한 자료형 재정의</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  struct student
  {
      int num;
      double grade;
  };
  typedef struct student Student;      // Student형으로 재정의
  void print_data(Student* ps);        // 매개변수는 Student형의 포인터

  int main(void)
  {
      Student s1 = { 315, 4.2 };       // Student형의 변수 선언과 초기화

      print_data(&amp;s1);                 // Student형 변수의 주소 전달

      return 0;
  }

  void print_data(Student* ps)
  {
      printf(&quot;학번 : %d\n&quot;, ps-&gt;num);  // Student 포인터로 멤버 접근
      printf(&quot;학점 : %.1lf\n&quot;, ps-&gt;grade);
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/e0abe128-f1d7-485a-8759-5a0cf5521ae9/image.png" /></p>
<ul>
<li><p>일반 변수명과 구분하기위해서 재정의된 자료형의 이름을 대문자로 사용한다.</p>
</li>
<li><p>재정의 하기 전의 자료형을 굳이 사용할 필요가 없다면 다음과 같이 형 선언과 동시에 재정의 하는 방법도 있다.</p>
<pre><code class="language-c">  typedef struct
  {
      int num;
      double grade;
  } Student;</code></pre>
</li>
<li><p>typedef문으로 기본 자료형 재정의 하기</p>
<ul>
<li><p>복잡한 응용 자료형뿐만아니라 필요에 따라 기본 자료형도 재정의 해서 사용가능.</p>
<pre><code class="language-c">typedef unsigned int nbyte;</code></pre>
</li>
</ul>
</li>
</ul>
<hr />
<h3 id="키워드로-끝내는-핵심-포인트-1">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>구조체 변수의 주소를 포인터에 저장하면 포인터로 멤버를 사용할 수 있다.</li>
<li>구조체도 자료형이 같으면 배열을 선언할 수 있다.</li>
<li>자기 참조 구조체는 연결 리스트linked list를 만들 때 사용한다.</li>
<li>공용체 변수의 크기는 멤버의 수에 비례하지 않는다.</li>
<li>열거형의 멤버는 열거형 변수에 저장될 값들을 나열한다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트-1">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/01d867f9-c8cd-4081-a752-b85a9872a322/image.png" /></p>