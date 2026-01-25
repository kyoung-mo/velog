<h2 id="14-1-다차원-배열">14-1 다차원 배열</h2>
<h3 id="2차원-배열-선언과-요소-사용">2차원 배열 선언과 요소 사용</h3>
<ul>
<li>2차원 배열을 사용하는 이유: 배열의 배열이 필요한 경우 ⇒ 행렬</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/bafb79f0-f2fd-49c9-9952-e050637c2dc4/image.png" /></p>
<ul>
<li>table(표)의 형태</li>
<li>int score[행][열];</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/24a234ba-e101-422d-a4f6-2db6e196ef80/image.png" /></p>
<ul>
<li><input disabled="" type="checkbox" /> 배열의 선언</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/97882a11-6a0f-487c-9273-45c71edb7b3c/image.png" /></p>
<ul>
<li><p>ex14-1.c</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      int score[3][4];          // 3명의 네 과목 점수를 저장할 2차원 배열 선언
      int total;                // 총점
      double avg;               // 평균
      int i, j;                 // 반복 제어 변수

      for (i = 0; i &lt; 3; i++)               // 학생 수만큼 반복
      {
          printf(&quot;4과목의 점수 입력 : &quot;);   // 입력 안내 메시지
          for (j = 0; j &lt; 4; j++)           // 과목 수만큼 반복
          {
              scanf(&quot;%d&quot;, &amp;score[i][j]);    // 점수 입력
          }
      }

      for (i = 0; i &lt; 3; i++)               // 학생 수 만큼 반복
      {
          total = 0;                        // 학생이 바뀔 때마다 0으로 초기화
          for (j = 0; j &lt; 4; j++)           // 과목 수 만큼 반복
          {
              total += score[i][j];         // 학생별로 총점 누적
          }
          avg = total / 4.0;                // 평균 계산
          printf(&quot;총점 : %d, 평균 : %.2lf\n&quot;, total, avg);   // 총점, 평균 출력
      }

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/0c6914b2-551a-4302-b12b-9cd0fbf98b42/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/cebae6b8-a9a5-4004-9bd0-3b179de78518/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/d81acfe6-7b63-4ef4-8242-52ca3e28a8ba/image.png" /></p>
<ul>
<li><input disabled="" type="checkbox" /> 메모리에서의 2차원 배열<ul>
<li>행첨자 = 1차원 배열 / 열의 수</li>
<li>열첨자 = 1차원 배열 % 열의 수</li>
<li>일곱번째 공간의 첨자 = score[ (7-1) / 4] [ (7-1) % 4 ] ⇒ score[1][2]</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/446cc2c5-2cc0-436a-8089-dbfc52522d49/image.png" /></p>
<hr />
<h3 id="2차원-배열-초기화">2차원 배열 초기화</h3>
<ul>
<li><p>1차원 배열과 마찬가지로 특정값을 저장할 필요가 있을때 선언과 동시에 초기화를 해줘야한다.</p>
<p>  (배열 요소마다 직접 값을 대입해야하는 번거로움을 방지)</p>
</li>
<li><p>중괄호 쌍 속 또 여러 개의 중괄호 쌍들을 이용해 행 부분을 표현해준다.</p>
<p>  ex) int num[2][2] ={ {1,2}, {3,4} } </p>
<ul>
<li><p>14-2.c(배열요소 전체 초기화)</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int num[3][4] = {       // 2차원 배열의 선언과 초기화
          {1, 2, 3, 4},       // num의 0행 -&gt;중괄호 쌍 하나가 행 하나를 뜻함.
          {5, 6, 7, 8},       // num의 1행
          {9, 10, 11, 12}     // num의 2행
      };
      // int num[3][4] = { {1, 2, 3, 4}, {5, 6, 7, 8}, {9, 10, 11, 12} };와 같은 문장임
    // int num[3][4] = {1, 2, 3, 4, 5, 6, 7, 8, 9 ,10, 11, 12}; 가능
      int i, j;

      for (i = 0; i &lt; 3; i++)  
      {
          for (j = 0; j &lt; 4; j++)
          {
              printf(&quot;%5d&quot;, num[i][j]);   // 배열 요소 출력
          }
          printf(&quot;\n&quot;);       // 한 행(부분배열)을 출력한 후에 줄 바꿈
      }

      return 0;
  }</code></pre>
<pre><code class="language-c">  1    2    3    4
  5    6    7    8
  9   10   11   12</code></pre>
</li>
</ul>
</li>
<li><p>전체 초기화를 해주는 방식 외에 다양한 초기화 방식이 존재한다.</p>
<ul>
<li>일부 초깃값 생략 가능</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/300aa925-929a-42e9-9d0e-8b773c0d4131/image.png" /></p>
<ul>
<li>초깃값을 부족하게 입력하면 각 행의 앞에서부터 차례로 저장, 남는 요소들은 0으로 자동 초기화 된다.</li>
</ul>
<pre><code class="language-c">#include &lt;stdio.h&gt;

int main(void){
    int num[3][4] = { {1}, {5, 6}, {9, 10, 11} };
    // 1행에 index 1~3 , 2행에 index 2~3, 3행에 index 3의 값은 초기화 생략
    int i, j;

    for (i = 0; i &lt; 3; i++){
        for (j = 0; j &lt; 4; j++){
            printf(&quot;%5d&quot;, num[i][j]);   // 배열 요소 출력
        }
        printf(&quot;\n&quot;);       // 한 행(부분배열)을 출력한 후에 줄 바꿈
    }

    return 0;
}</code></pre>
<pre><code class="language-c">        1    0    0    0
        5    6    0    0
        9   10   11    0</code></pre>
<ul>
<li>행의 수 생략 가능</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/0dc371c8-f1ea-4fb3-a921-38ad4e767ecb/image.png" /></p>
<pre><code>    - 행의 수를 생략하고 선언해도 초기화를 통해 그 값을결정할 수 있다.
    - 컴파일러는 중괄호의 개수를 행의 수로 인식해 저장 공간을 할당한다.
    - 한 행의 크기는 열의 수로 결정되기 때문에 열의 개수는 생략할 수 없다.

    ```c
    #include &lt;stdio.h&gt;

    int main(void)
    {
      int num[][4] = { {1}, {5, 6}, {9, 10, 11} };

        int i, j;

        for (i = 0; i &lt; 3; i++)  
        {
            for (j = 0; j &lt; 4; j++)
            {
                printf(&quot;%5d&quot;, num[i][j]);   // 배열 요소 출력
            }
            printf(&quot;\n&quot;);       // 한 행(부분배열)을 출력한 후에 줄 바꿈
        }

        return 0;
    }
    ```

    ```c
    1    0    0    0
    5    6    0    0
    9   10   11    0
    ```

- 1차원 배열의 초기화 방식으로 초기화</code></pre><p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/8a4fb673-17c2-4131-b7e0-3535b58e0eda/image.png" /></p>
<pre><code>    - 2차원 배열은 물리적(메모리에 저장되는 구조상)으로 1차원 배열의 나열로 볼수 있어 행 초기화 괄호를 생략해 1차원 배열을 초기화하는 방식으로 초기화가 가능하다.
    - 배열 요소의 수만큼 초깃값을 나열하고, 열의 수만큼 끊어 행 단위로 차례로 저장된다.

    ```c
    #include &lt;stdio.h&gt;

    int main(void)
    {
      int num[3][4] = {1,2,3,4,5,6,7,8,9,10,11,12};

        int i, j;

        for (i = 0; i &lt; 3; i++)  
        {
            for (j = 0; j &lt; 4; j++)
            {
                printf(&quot;%5d&quot;, num[i][j]);   // 배열 요소 출력
            }
            printf(&quot;\n&quot;);       // 한 행(부분배열)을 출력한 후에 줄 바꿈
        }

        return 0;
    }
    ```

    ```c
    1    2    3    4
    5    6    7    8
    9   10   11   12
    ```

    - 해당 2차원 배열을 참조하기 위해서 포인터 변수를 선언해 사용할 경우 주의할 점이 있다.
        - 컴파일시 컴퓨터는 논리적으로 행 단위로 끊어 인식(전체 요소의 개수가 12개로 같아도 차원에따라 12개의 요소를 가진 1차원 배열 하나 또는  4개의 요소를 가진 1차원 배열 3개의 집합으로 구분) 하기때문에 포인터 변수의 형태를 1차원 배열을 참조할 때와는 다르게 선언해줘야한다.
        - ex ) 1차원 배열 : int *ary ; / 2차원 배열 :  int (*ary)[4];

        ```c
        #include &lt;stdio.h&gt;
        #include &lt;stdlib.h&gt;
        #include &lt;time.h&gt;
        void get2DArray(int arr[][4], int col, int row, int* cp, int size);

        int main(void)
        {
            srand(time(NULL));
            int ary[3][4];
            int compare[12]={1,2,3,4,5,6,7,8,9,10,11,12};
            int i, j, num, size;
            size= sizeof(compare)/sizeof(compare[0]);

            get2DArray(ary, 3, 4, compare, size);

            while(1) //숫자(1~10) 좌표 찾기[숫자 중복 배정]
            {
                scanf(&quot;%d&quot;,  &amp;num);
                printf(&quot;%s &lt;%d의 위치 X표기&gt;\n&quot;, &quot;\033[0m&quot;, num);
                for(i=0; i&lt;3; i++)
                {
                    for(j=0; j&lt;4; j++)
                    {
                        if(ary[i][j]==num)
                        {
                            printf(&quot;%s %5c&quot;, &quot;\033[31m&quot;, 'X');
                        }
                        else
                        {
                            printf(&quot;%s %5d&quot;, &quot;\033[0m&quot;, ary[i][j]);
                        }
                    }
                    printf(&quot;\n&quot;);
                }
            }
            return 0;
        }

        //                          ↓ 배열의 가로 크기 지정
        void get2DArray(int (*arr)[4], int row, int col, int* cp, int size)    // 2차원 배열의 포인터와 가로, 세로 크기를 받음
        {    
            int i, j, k;

            for (i=0; i&lt;row; i++) //여기서 i가 1씩 증가 할때마다 
            {                              //배열 하나의 크기 만큼(16byte) 메모리 주소번지 이동.
                for (j=0; j&lt;col; j++)
                {
                    arr[i][j] = rand()%12+1;
                    for(k=0; k&lt;size; k++)
                    {
                        if(arr[i][j] == cp[k])
                        {
                            cp[k] = 0;
                            ++j;
                            break;
                        }
                    }
                    --j;
                }
            }
            return;
        }
        ```

        ```c
        1210
         &lt;10의 위치 X표기&gt;
             3     5     8     9
            12     7    11     1
             4     2     X     6
        11
         &lt;11의 위치 X표기&gt;
             3     5     8     9
            12     7     X     1
             4     2    10     6
        12
         &lt;12의 위치 X표기&gt;
             3     5     8     9
             X     7    11     1
             4     2    10     6
        ```

    - 초기화시 남는 저장공간은 0으로 자동 초기화</code></pre><p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/42a2ee99-d80c-4a72-8104-ca79e7f8bd39/image.png" /></p>
<pre><code>        - 1차원 배열의 초기화 방식을 사용하는 경우에도 전체 공간의 수보다 적은 값을 나열하면 나머지 공간은 0으로 자동 초기화 된다.

            ```c
            #include &lt;stdio.h&gt;

            int main(void)
            {
              int num[3][4] = {1,2,3,4,5,6};

                int i, j;

                for (i = 0; i &lt; 3; i++)  
                {
                    for (j = 0; j &lt; 4; j++)
                    {
                        printf(&quot;%5d&quot;, num[i][j]);   // 배열 요소 출력
                    }
                    printf(&quot;\n&quot;);       // 한 행(부분배열)을 출력한 후에 줄 바꿈
                }

                return 0;
            }
            ```

            ```c
            1    2    3    4
            5    6    0    0
            0    0    0    0
            ```

    - 행의 수가 생략되고 초깃값이 적은 경우</code></pre><p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/04a09eea-3ce2-483d-abcf-8e043cf50637/image.png" /></p>
<pre><code>        - 1차원 배열의 초기화 방식을 사용하는 경우에 행의 수가 생략되면 열의 수에 맞게 초깃값을 끊어 행의 수를 결정하고 남은 공간은 0으로 자동 초기화 된다.
        - 행의 개수 = sizeof(score) / sizeof(score[0])

        ```c
        #include &lt;stdio.h&gt;

        int main(void)
        {
            int num[][4] = {1,2,3,4,5,6};

            int i, j;
          int countRow = sizeof(num)/sizeof(num[0]); //행의 수 구하기

            for (i = 0; i &lt; countRow; i++)  
            {
                for (j = 0; j &lt; 4; j++)
                {
                    printf(&quot;%5d&quot;, num[i][j]);   // 배열 요소 출력
                }
                printf(&quot;\n&quot;);       // 한 행(부분배열)을 출력한 후에 줄 바꿈
            }

            return 0;
        }
        ```

        ```c
        1    2    3    4
        5    6    0    0
        ```</code></pre><ul>
<li>2차원 배열의 요소는 1차원 배열이며 이를 부분배열이라고도 한다.<ul>
<li>부분배열의 표현 방식<ul>
<li>예를 들어 score[3][4]이라는 2차원 배열의 요소(부분배열)는 score[0], score[1], score[2]로 표현할 수 있다.</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/74a6d0f8-67fd-4b30-b39a-609b4747d101/image.png" /></p>
<pre><code>    ```c
    score[0] : score[0][0]~score[0][4] 
    // 변수명 뒤에 행 index 값만 작성해주면 하나의 1차원 배열로 인식
    score[1] : score[1][0]~score[1][4]
    score[2] : score[2][0]~score[2][4]
    ```</code></pre><h3 id="2차원-char-배열">2차원 char 배열</h3>
<ul>
<li><p>14-3.c</p>
<pre><code class="language-c">  #define _CRT_SECURE_NO_WARNINGS
  #include &lt;stdio.h&gt;

  int main(void)
  {
      char animal[5][20];    // 2차원 char 배열 선언
      int i;                 // 반복 제어 변수
      int count;             // 행의 수를 저장할 변수

      count = sizeof(animal) / sizeof(animal[0]);  // 행의 수 계산
      for (i = 0; i &lt; count; i++)     // 행의 수만큼 반복
      {
          scanf(&quot;%s&quot;, animal[i]);     // 문자열 입력
      }

      for (i = 0; i &lt; count; i++)
      {
          printf(&quot;%s  &quot;, animal[i]);  // 입력된 문자열 출력
      }

      return 0;
  }</code></pre>
<pre><code class="language-c">  char animal[5][20];</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/aaa64e4f-1e1b-4978-b6b6-a3a4959ec9ac/image.png" /></p>
<ul>
<li>각 행은 하나의 1차원 char 배열이며, 부분배열명은 각 행의 배열명 : 각 행이 나타내는 배열의 첫 인덱스의 주소</li>
</ul>
<h3 id="2차원-char-배열-초기화">2차원 char 배열 초기화</h3>
<ul>
<li><p>14-4.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      char animal1[5][10] = {         // 문자 상수로 하나씩 초기화
          {'d', 'o', 'g', '\0'},
          {'t', 'i', 'g', 'e', 'r', '\0'},
          {'r', 'a', 'b', 'b', 'i', 't', '\0'},
          {'h', 'o', 'r', 'c', 'e', '\0'},
          {'c', 'a', 't', '\0'}
      };
      // 문자열 상수로 한 행씩 초기화, 행의 수 생략 가능
      char animal2[][10] = { &quot;dog&quot;, &quot;tiger&quot;, &quot;rabbit&quot;, &quot;horse&quot;, &quot;cat&quot; };  //행의 개수 5개
      int i;

      for (i = 0; i &lt; 5; i++)
      {
          printf(&quot;%s &quot;, animal1[i]);
      }
      printf(&quot;\n&quot;);
      for (i = 0; i &lt; 5; i++)
      {
          printf(&quot;%s &quot;, animal2[i]);
      }

      return 0;
</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/1c4e7a35-bcb7-4f1c-8bfd-24619de4a89e/image.png" /></p>
<h3 id="3차원-배열">3차원 배열</h3>
<ul>
<li>2차원 배열의 배열</li>
<li>자료형 배열명[면][행][열]</li>
<li>int score[2][3][4] 는 (int [3][4])의 2개짜리 배열</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/69eb002a-72f7-49e3-85f9-7e84be470dcf/image.png" /></p>
<ul>
<li><p>ex14-5.c</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int score[2][3][4] = {    // 2개 반 세 명의 4과목 점수 저장
          { { 72, 80, 95, 60 }, { 68, 98, 83, 90 }, { 75, 72, 84, 90 } },
          { { 66, 85, 90, 88 }, { 95, 92, 88, 95 }, { 43, 72, 56, 75 } }
      };

      int i, j, k;                           // 반복 제어 변수

      for (i = 0; i &lt; 2; i++)                   // 반 수만큼 반복
      {
          printf(&quot;%d반 점수...\n&quot;, i + 1);   // 반이 바뀔 때마다 출력
          for (j = 0; j &lt; 3; j++)            // 학생 수만큼 반복
          {
              for (k = 0; k &lt; 4; k++)        // 과목 수만큼 반복
              {
                  printf(&quot;%5d&quot;, score[i][j][k]);  // 점수 출력
              }
              printf(&quot;\n&quot;);                  // 한 학생의 점수를 출력하고 줄 바꿈
          }
          printf(&quot;\n&quot;);                      // 한 반의 점수를 출력하고 줄 바꿈
      }

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/b1a6e34b-4812-470b-8ed0-0e9d0a659909/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/3046e474-0b13-40a0-aa16-c0738354f9d6/image.png" /></p>
<ul>
<li>초기값이 채워지는 순서, 방법은 2차원 배열과 같다.</li>
<li>for문 바깥쪽부터 면, 행, 열을 다루는 반복문 사용</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/48f0ba1f-9a9a-4b5e-873f-64982f2d8157/image.png" /></p>
<hr />
<h3 id="키워드로-끝내는-핵심-포인트">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>2차원 배열의 요소는 행 첨자와 열 첨자로 쓰며 0부터 시작한다.</li>
<li>3차원 배열은 2차원 배열에 면을 더해 면, 행, 열로 이뤄진다.</li>
<li>2차원 배열의 초기화는 중괄호 쌍(‘{’와 ‘}’)을 두 번 사용한다.</li>
<li>3차원 배열의 초기화는 중괄호 쌍(‘{’와 ‘}’)을 세 번 사용한다.</li>
<li>2차원 배열은 주로 2중 for문(반복문)으로 처리하며 행의 수와 열의 수만큼 반복한다.</li>
<li>3차원 배열은 주로 3중 for문(반복문)으로 처리하며 면의 수, 행의 수와 열의 수만큼 반복한다.</li>
<li>2차원 char 배열의 초기화는 중괄호 안에 여러 개의 문자열로 초기화할 수 있다.</li>
<li>3차원 char 배열의 초기화도, 중괄호 안에 여러 개의 문자열로 초기화할 수 있다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/a4585498-bde8-4f74-9724-b097d24224a7/image.png" /></p>
<h2 id="14-2-포인터-배열">14-2 포인터 배열</h2>
<h3 id="포인터-배열-선언과-사용">포인터 배열 선언과 사용</h3>
<ul>
<li>포인터는 주소를 저장하는 특별한 용도로 쓰인다.</li>
<li>일반 변수처럼 메모리에 저장 공간을 갖는 변수</li>
<li>같은 포인터를 많이 필요할 때는 배열을 사용해야 한다.</li>
<li>포인터 배열은 같은 자료형의 포인터를 모아 만든 배열이다.</li>
</ul>
<pre><code class="language-c">int *pa;
int *pb;
int *pc;</code></pre>
<pre><code class="language-c">int *pary[3];</code></pre>
<ul>
<li><p>ex14-6.c - 포인터 배열로 여러개의 문자열 출력</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      char* pary[5];           // 포인터 배열 선언. pointer와 array의 약어로 pary
      int i;                   // 반복 제어 변수

      pary[0] = &quot;dog&quot;;         // 배열 요소에 문자열 대입
      pary[1] = &quot;elephant&quot;;
      pary[2] = &quot;horse&quot;;
      pary[3] = &quot;tiger&quot;;
      pary[4] = &quot;lion&quot;;

      for (i = 0; i &lt; 5; i++)  // i는 0부터 4까지 5번 반복
      {
          printf(&quot;%s\n&quot;, pary[i]);  // 배열 요소를 사용하여 모든 문자열 출력
      }

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/1df23f76-0c3b-4cb7-bcfc-c84ed3c194c4/image.png" /></p>
<pre><code>- 포인터 배열의 선언방식은 일반적인 배열 선언 방식과 같다.
- 단 각 배열요소의 자료형이 포인터형이므로 배열명 앞에 별(*)을 붙입니다.</code></pre><p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/9e4256d0-35e5-4632-854e-7062e481992e/image.png" /></p>
<ul>
<li>포인터배열의 각 요소에 문자열 상수를 대입합니다.</li>
<li>문자열 상수는 변경이 불가능한 메모리에 보관되고 포인터 배열에는 그 첫번째 문자의 주소가 저장됩니다.</li>
<li>대입후의 메모리의 상태는 다음과 같고, 메모리의 주소값은 임의로 가정합니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/e77a60a9-0aa3-4ef5-9bc4-10e85e0c12f3/image.png" /></p>
<ul>
<li>포인터 배열은 연속해서 생성되나요?<ul>
<li>포인터 배열은 다른 배열처럼 메모리에 연속해서 위치합니다.</li>
<li>요소에 저장된 주소값은 개별적인 문자열의 주소이므로 연속성을 지니지 않음</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/bb08ec5b-7f73-4cbe-995d-2d95d69ea41d/image.png" /></p>
<ul>
<li>포인터 배열의 초기화<ul>
<li>char포인터 배열의 초기화는 2차원 char배열의 초기화와 같습니다.</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/9e713e2c-266e-4215-a9f4-325686a386d5/image.png" /></p>
<pre><code>- 포인터 배열의 초기화는 문자열의 시작 주소만 배열 요소에 저장
- 2차원 char 배열의 초기화는 문자열 자체를 배열의 공간에 저장</code></pre><h3 id="2차원-배열처럼-활용하는-포인터-배열">2차원 배열처럼 활용하는 포인터 배열</h3>
<ul>
<li><p>포인터 배열은 첨자를 하나 사용하는 1차원 배열입니다.</p>
</li>
<li><p>2차원 배열로 활용하는 방법 ⇒ 1차원 배열을 포인터로 연결하면 2차원 배열처럼 사용할 수 있습니다.</p>
</li>
<li><p>ex14-7.c - 여러개의 1차원 배열을 2차원 배열처럼 사용</p>
<pre><code class="language-c">  #include &lt;stdio.h&gt;

  int main(void)
  {
      int ary1[4] = { 1, 2, 3, 4 };         // 1차원 배열의 선언과 초기화
      int ary2[4] = { 11, 12, 13, 14 };
      int ary3[4] = { 21, 22, 23, 24 };
      int* pary[3] = { ary1, ary2, ary3 };  // 포인터 배열에 각 배열명 초기화
      int i, j;                             // 반복 제어 변수

      for (i = 0; i &lt; 3; i++)               // 3행 반복
      {
          for (j = 0; j &lt; 4; j++)           // 4열 반복
          {
              printf(&quot;%5d&quot;, pary[i][j]);    // 2차원 배열처럼 출력
          }
          printf(&quot;\n&quot;);                     // 한 행을 출력한 후에 줄 바꿈
      }

      return 0;
  }</code></pre>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/4263ed14-95cd-4be4-9064-90d74ee6cc19/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/56fff9b4-cae4-4244-b53c-660048ebb240/image.png" /></p>
<ul>
<li><p>각 배열의 요소가 다르면 어떻게 될까?</p>
<ul>
<li><p>세번째 배열만 5개 요소가 있는 경우에</p>
<pre><code class="language-c">int ary3[5] = { 21, 22, 23,24, 25};</code></pre>
<pre><code class="language-c">int ary2[5] = { 11, 12, 13, 14};</code></pre>
<pre><code class="language-c">  1    2    3    4-858993460
 11   12   13   14    0
 21   22   23   24    0</code></pre>
</li>
<li><p>배열 요소의 개수가 달라져도 실행에는 지장이 없다.</p>
</li>
</ul>
</li>
<li><p>포인터 배열을 2차원 배열처럼 사용할 수 있는 이유</p>
<ul>
<li>두 표현식은 같다.</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/0b8abe90-6214-4b7c-ba06-fc5403f2ecab/image.png" /></p>
<pre><code>- 주소 계산과 간접 참조 연산으로 각 위치를 찾아간다.</code></pre><p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/6e4ab71b-881a-4fdf-9f85-2c360dece50d/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/25db1bf6-44a1-4929-9ecb-08c9910e6744/image.png" /></p>
<hr />
<h3 id="키워드로-끝내는-핵심-포인트-1">키워드로 끝내는 핵심 포인트</h3>
<ul>
<li>포인터 배열을 선언하고 사용하는 방법은 일반 배열과 같다.</li>
<li>char 포인터 배열은 여러 개의 문자열을 다루기에 편하다.</li>
<li>포인터 배열을 사용하면 1차원 배열을 모아 2차원 배열처럼 쓸 수 있다.</li>
</ul>
<h3 id="표로-정리하는-핵심-포인트-1">표로 정리하는 핵심 포인트</h3>
<p><img alt="" src="https://velog.velcdn.com/images/kym11290306/post/e5ee6a41-5307-485f-9cb9-08c930678fca/image.png" /></p>