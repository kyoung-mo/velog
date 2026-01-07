<h2 id="16-1-동적-할당-함수">16-1 동적 할당 함수</h2>
<h3 id="malloc-free-함수-12">malloc, free 함수 (1/2)</h3>
<p>32비트 Heap영역 주소 &lt; stack영역 주소</p>
<p>64비트에서는 Heap영역 주소 &gt; stack영역 주소</p>
<ul>
<li><p>16-1.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;
  #include &lt;stdlib.h&gt;       // malloc, free 함수 사용을 위한 헤더 파일

  int main(void)
  {
      int* pi;              // 동적 할당 영역을 연결할 포인터 선언
      double* pd;

      pi = (int*)malloc(sizeof(int));               // 메모리 동적 할당 후 포인터 연결
      if (pi == NULL)                               // 동적 할당에 실패하면 NULL 포인터 반환
      {
          printf(&quot;# 메모리가 부족합니다.\n&quot;);    // 예외 상황 메시지 출력
          exit(1);                               // 프로그램 종료
      }
      pd = (double*)malloc(sizeof(double));

      *pi = 10;                                  // 포인터로 동적 할당 영역 사용
      *pd = 3.4;

      printf(&quot;정수형으로 사용 : %d\n&quot;, *pi);     // 동적 할당 영역에 저장된 값 출력
      printf(&quot;실수형으로 사용 : %.1lf\n&quot;, *pd);

      free(pi);                                  // 동적 할당 영역 반환
      free(pd);

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/83d729cb-bcae-429f-9b73-76d644cb771f/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/e2899ea3-b631-41fb-9dfa-3e7b4c52087d/image.png" /></p>
<h3 id="동적-할당-영역을-배열처럼-쓰기">동적 할당 영역을 배열처럼 쓰기</h3>
<ul>
<li><p>16-2.c</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;
  #include &lt;stdlib.h&gt;

  int main(void)
  {
      int* pi;                                  // 동적 할당 영역을 연결할 포인터
      int i, sum = 0;                           // 반복 제어 변수와 누적 변수

      pi = (int*)malloc(5 * sizeof(int));       // 저장 공간 20바이트 할당
      if (pi == NULL)
      {
          printf(&quot;메모리가 부족합니다!\n&quot;);
          exit(1);
      }
      printf(&quot;다섯 명의 나이를 입력하세요 : &quot;);
      for (i = 0; i &lt; 5; i++)                   // i는 0부터 4까지 5번 반복
      {
          scanf(&quot;%d&quot;, &amp;pi[i]);                  // 배열 요소에 입력
          sum += pi[i];                         // 배열 요소의 값 누적
      }
      printf(&quot;다섯 명의 평균 나이 : % .1lf\n&quot;, (sum / 5.0)); // 평균 나이 출력
      free(pi);                                 // 할당한 메모리 영역 반환

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/e63d5615-24cd-428d-a543-4b38be53ffac/image.png" /></p>
<h3 id="기타-동적-할당-함수">기타 동적 할당 함수</h3>
<ul>
<li>calloc 함수는 할당한 공간을 0으로 초기화 한다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/f3bb06e2-19ba-4e84-be5f-aedde8027422/image.png" /></p>
<ul>
<li>realloc 함수는 할당한 공간의 크기를 늘이거나 줄인다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/ee438f22-682a-4075-a4cf-fc81ba6c67bb/image.png" /></p>
<ul>
<li><p>16.3.c</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;
  #include &lt;stdlib.h&gt;

  int main(void)
  {
      int* pi;         // 할당한 저장 공간을 연결할 포인터
      int size = 5;    // 한 번에 할당할 저장 공간의 크기, int형 변수 5개씩
      int count = 0;   // 현재 입력된 양수 개수
      int num;         // 양수를 입력할 변수
      int i;           // 반복 제어 변수

      pi = (int*)calloc(size, sizeof(int));    // 먼저 5개의 저장 공간 할당
      while (1)
      {
          printf(&quot;양수만 입력하세요 = &gt; &quot;);
          scanf(&quot;%d&quot;, &amp;num);                   // 데이터 입력
          if (num &lt;= 0) break;                 // 0또는 음수이면 종료
          if (count == size)                   // 저장 공간을 모두 사용하면
          {
              size += 5;                       // 크기를 늘려서 재할당
              pi = (int*)realloc(pi, size * sizeof(int));
          }
          pi[count++] = num;
      }
      for (i = 0; i &lt; count; i++)
      {
          printf(&quot;%5d&quot;, pi[i]);        // 입력한 데이터 출력
      }
      free(pi);                        // 동적 할당 저장 공간 반납

      return 0;
  }</code></pre>
</li>
<li><p>하나의 프로그램이 사용하는 메모리 영역</p>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/aea08884-a1d6-42e7-acf2-7e8fd07111c7/image.png" /></p>
<ul>
<li>힙 영역은 원하는 크기 만큼 할당하지 못할 수 있다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/9213ee98-3dcf-48a6-96ec-09b0e9a05c8e/image.png" /></p>
<hr />
<h3 id="키워드로-끝내는-핵심-포인트">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>동적 할당한 공간은 변수와 달리 이름이 없으므로 포인터에 주소를 대입하여 사용한다.</li>
<li>동적할당을 요청한 후에는 제대로 할당되었는지 반환값을 확인해야 한다.</li>
<li>사용이 끝난 동적 할당 공간은 재활용을 위해 반환한다.</li>
<li>동적 할당한 저장 공간을 배열처럼 쓸 때는 포인터가 배열명의 역할을 한다.</li>
<li>calloc 함수는 동적 할당한 저장 공간을 0으로 초기화하고, realloc 함수는 크기를 바꿔 재할당한다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/e4fb8ffc-0a51-4d73-b8e0-8c207eb79282/image.png" /></p>
<hr />
<h2 id="16-2-동적-할당-저장-공간의-활용">16-2 동적 할당 저장 공간의 활용</h2>
<ul>
<li>영어 사전의 단어 수 10,000개, 가장 긴 단어의 길이 45자</li>
<li>사전의 모든 단어를 메모리에 저장하고, 정렬/탐색하는 경우 널 문자까지 포함 46만 바이트 필요.</li>
<li>배열은 각 행의 길이가 모두 같아야 하가에...</li>
</ul>
<hr />
<ul>
<li>단어의 평균 길이는 6~7자 정도이며, 이는 메모리 공간 7만 바이트 정도.</li>
<li>대부분의 메모리 공간은 낭비됨.</li>
<li>각 단어의 길이 만큼만 메모리 확보하고 처리하는 방법이 필요함.</li>
</ul>
<h3 id="동적-할당을-사용한-문자열-처리">동적 할당을 사용한 문자열 처리</h3>
<ul>
<li><p>동적할당은 프로그램의 효율을 높이기 위한 하나의 방법.</p>
</li>
<li><p>입력 문자의 길이를 알 수 없는 경우 무조건 가장 큰 문자열을 기준으로 배열을 선언해야 함.</p>
</li>
<li><p>동적 할당을 하면 입력되는 문자열의 길이에 맞게 저장공간을 사용할 수 있다.</p>
</li>
<li><p>16-4 : 3개의 문자열을 저장하기 위한 동적 할당.</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;
  #include &lt;stdlib.h&gt;
  #include &lt;string.h&gt;

  int main(void)
  {
      char temp[80];                // 임시 char 배열
      char* str[3];                 // 동적 할당 영역을 연결할 포인터 배열
      int i;                        // 반복 제어 변수

      for (i = 0; i &lt; 3; i++)
      {
          printf(&quot;문자열을 입력하세요 : &quot;);
          gets(temp);               // 문자열 입력
          str[i] = (char*)malloc(strlen(temp) + 1);   // 문자열 저장 공간 할당
          strcpy(str[i], temp);     // 동적 할당 영역에 문자열 복사
      }

      for (i = 0; i &lt; 3; i++)
      {
          printf(&quot;%s\n&quot;, str[i]);   // 입력된 문자열 출력
      }

      for (i = 0; i &lt; 3; i++)
      {
          free(str[i]);             // 동적 할당 영역 반환
      }

      return 0;
  } </code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/b30b16b9-79fe-4d48-b580-4b67eff2be6b/image.png" /></p>
<pre><code>- 문자열을 입력하기전에 그 길이를 알수 없으므로 충분한 크기(80)의 char배열을 선언하고 문자열을 입력합니다.
- 길이에 맞게 다시 동적으로 할당한 후에 입력한 문자열을 복사</code></pre><ul>
<li><p>gets함수</p>
<ul>
<li>scanf() 함수는 \n(줄바꿈문자)를 가져오지 않고, 마지막에 \0(널문자)를 붙인다.</li>
<li>gets() 함수는 \n(줄바꿈문자)까지 가져오고,    \n을 \0으로 대체 한다.</li>
<li>fgets() 함수는 \n(줄바꿈문자)까지 가져오고, 추가적으로 \0을 붙인다.</li>
</ul>
</li>
<li><p>strlen</p>
<ul>
<li><strong>strlen</strong>은 문자열의 길이를 구하는 <strong>함수</strong>이다. 이 때 null 문자인 '\0'은 포함하지 않는다. strlen 함수는 string.h 헤더에 선언되어있다.</li>
<li><strong>sizeof</strong>는 <strong>연산자</strong>로 피연산자의 메모리 크기를 바이트 단위로 계산한다. 
상수, 변수 뿐만 아니라 자료형 그 자체가 피연산자가 될 수 있다. 
연산자이기 때문에 상수나 변수의 경우 반드시 괄호를 사용해 묶을 필요는 없다. 
size는 컴파일타임 연산자이기 때문에 sizeof와 피연산자는 컴파일 단계에서 결과 값을 가진다.그러므로 동적 할당된 크기는 알 수 없다.</li>
</ul>
</li>
</ul>
<h3 id="동적-할당-영역에-저장한-문자열을-함수로-처리하는-예">동적 할당 영역에 저장한 문자열을 함수로 처리하는 예</h3>
<ul>
<li><p>동적 할당한 저장 공간을 함수로 처리할 때는 할당한 공간의 구조를 잘 살펴야 한다.</p>
</li>
<li><p>16-4의 문자열 출력 부분을 함수로 바꿉니다.</p>
</li>
<li><p>16-5.c : 동적할당 영역의 문자열을 함수로 출력</p>
<ul>
<li><p>함수에서 포인터 배열의 이름을 저장할 포인터 매개변수가 필요합니다.</p>
</li>
<li><p>str은 포인터 배열의 첫번째 요소를 가리키므로 가리키는 것의 형태는 (char *)형입니다.</p>
</li>
<li><p>따라서 str을 저장할 매개변수로 (char*)형을 가리키는 이중 포인터를 선언합니다.</p>
<pre><code class="language-c">#define _CRT_SECURE_NO_WARNINGS
#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;

void print_str(char** ps);     // 동적 할당 영역의 문자열을 출력하는 함수

int main(void)
{
  char temp[80];             // 임시 char 배열
  char* str[21] = { 0 };     // 문자열을 연결할 포인터 배열, 널 포인터로 초기화
  int i = 0;                 // 반복 제어 변수

  while (i &lt; 20)             // 최대 20개까지 입력
  {
      printf(&quot;문자열을 입력하세요 : &quot;);
      gets(temp);                                // 문자열 입력
      if (strcmp(temp, &quot;end&quot;) == 0) break;       // end가 입력되면 반복 종료

      str[i] = (char*)malloc(strlen(temp) + 1);  // 문자열 저장 공간 할당
      strcpy(str[i], temp);                      // 동적 할당 영역에 문자열 복사
      i++;
  }
  print_str(str);                                // 입력한 문자열 출력

  for (i = 0; str[i] != NULL; i++)               // str에 연결된 문자열이 없을 때까지
  {
      free(str[i]);                              // 동적 할당 영역 반환
  }

  return 0;
}

void print_str(char** ps)      // 이중 포인터 선언
{

  //malloc~~~
  while (*ps != NULL)        // 포인터 배열의 값이 널 포인터가 아닌 동안 반복
  {
      printf(&quot;%s\n&quot;, *ps);   // ps가 가리키는 것은 포인터 배열의 요소
      ps++;                  // ps가 다음 배열 요소를 가리킨다.
  }
}</code></pre>
</li>
<li><p>main함수에서 문자열을 직접 출력할 때는 str이 배열명이므로 그 값을 바꿀 수 없습니다.</p>
<ul>
<li>따라서 str[i]와 같이 배열 표현을 사용하거나 *(str+i)와 같이 정수를 더하면서 각 문자열을 출력할 수 밖에 없습니다.</li>
<li>그러나 배열명을 포인터에 저장하면 포인터 자신의 값을 바꿀 수 있으므로 매개변수를 하나씩 증가시키면서 문자열을 출력할 수 있습니다.</li>
</ul>
</li>
<li><p>동적 할당 영역을 마치 행의 길이가 <strong>가변적인 2차원의 char배열</strong>처럼 사용.</p>
<ul>
<li>이 방식은 효과적인 메모리를 사용할 수 있다.</li>
</ul>
</li>
<li><p>주의사항</p>
<ul>
<li>포인터나 포인터 배열을 auto 지역 변수로 선언하면 쓰레기 값이 주소로 존재합니다.</li>
<li>포인터 배열은 선언과 동시에 널 포인터로 초기화하고 참조할 때 널 포인터인지 검사하면 안정적인 프로그램이 가능하다.</li>
<li>포인터 배열의 마지막 요소는 널 포인터가 꼭 들어가야 합니다.</li>
<li></li>
</ul>
</li>
</ul>
</li>
</ul>
<h3 id="main-함수의-명령행-인수-사용">main 함수의 명령행 인수 사용</h3>
<ul>
<li><p>명령행에서 프로그램을 실행시킬 때는 프로그램의 이름 외에도 프로그램에 필요한 정보를 함께 줄수 있는데 이들을 모두 명령행 인수 (Command Line Argument)</p>
</li>
<li><p>명령행 인수를 프로그램의 main함수로 넘기는 방법을 통해 포인터로 동적 할당한 영역을 배열처럼 사용</p>
</li>
<li><p>16.6.c : 명령행 인수를 출력하는 프로그램</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(int argc, char** argv)   // 명령행 인수를 받을 매개변수
  {
      int i;

      for (i = 0; i &lt; argc; i++)    // 인수 개수 만큼 반복
      {
          printf(&quot;%s\n&quot;, argv[i]);  // 인수로 받은 문자열 출력
      }

      return 0;
  }</code></pre>
<ul>
<li>매개변수의 이름은 임의로 작성할 수 있으나 관례적으로 argc, argv로 사용 count, vector
  <img alt="" src="https://velog.velcdn.com/images/kym11290306/post/d6698072-d3b2-450b-aea3-7ed78d4f3880/image.png" /></li>
</ul>
</li>
</ul>
<pre><code>    - 운영체제는 명령행 인수를 가공하여 문자열의 형태로 메모리에 저장하고 포인터 배열로 연결한 후에 포인터 배열의 시작 위치를 실행 프로그램의 main함수에 넘깁니다.

![](https://velog.velcdn.com/images/kym11290306/post/a8866220-a557-4b63-9efe-28ac03235376/image.png)</code></pre><hr />
<h3 id="키워드로-끝내는-핵심-포인트-1">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>입력 문자열의 길이에 딱 맞는 메모리 공간을 확보할 수 있다.</li>
<li>명령행 인수의 구현 방식을 이해할 수 있다.</li>
<li>동적 할당 영역은 복잡할수록 빠짐없이 반환해야 한다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트-1">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/9934d908-3c87-4dd4-aeda-9b9c3daf49fb/image.png" /></p>