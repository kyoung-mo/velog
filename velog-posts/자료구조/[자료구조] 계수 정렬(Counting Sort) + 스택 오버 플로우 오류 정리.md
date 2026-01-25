<h3 id="1-계수-정렬">1. 계수 정렬</h3>
<p><img alt="" src="https://miro.medium.com/v2/resize:fit:720/format:webp/1*7QYa43QqcYgfnAAAr3sUWg.gif" /></p>
<ul>
<li>선택, 삽입, 퀵 정렬처럼 데이터를 비교하며 위치를 변경하는 <strong>비교 기반의 정렬 알고리즘이 아니다</strong>.</li>
<li>숫자의 <strong>빈도(count)</strong> 를 세어서 정렬하는 정렬 알고리즘</li>
<li>비교 기반이 아닌 <strong>정수 키 기반 정렬</strong></li>
<li>시간 복잡도: <strong><code>O(n+k)</code></strong> 
(n은 입력 크기, k는 최댓값)</li>
<li>입력 값이 정수이며, <strong>범위</strong>가 작을 때 매우 효율적</li>
</ul>
<h3 id="2-정렬-과정">2. 정렬 과정</h3>
<h5 id="1-가장-작은-데이터부터-가장-큰-데이터까지의-범위가-모두-담길-수-있는-리스트를-생성">1) 가장 작은 데이터부터 가장 큰 데이터까지의 범위가 모두 담길 수 있는 리스트를 생성</h5>
<h5 id="2-데이터를-하나씩-확인하며-데이터의-값을-인덱스로-사용하여-해당-위치의-count-값을-1씩-증가">2) 데이터를 하나씩 확인하며 데이터의 값을 인덱스로 사용하여 해당 위치의 count 값을 1씩 증가</h5>
<pre><code class="language-c">입력 배열:          [4, 2, 2, 8, 3, 3, 1]
Count 배열:      [0, 1, 2, 2, 1, 0, 0, 0, 1]   ← 인덱스가 값
정렬된 결과:      [1, 2, 2, 3, 3, 4, 8]

// 입력 배열의 값을 count 배열에 누적
for (int i = 0; i &lt; SIZE; i++){
     count[data[i]]++;  // 값이 i일 때 count[i]++
}</code></pre>
<h5 id="3-증가된-리스트에서-0인-값을-제외하고-인덱스를-인덱스-값만큼-출력">3) 증가된 리스트에서 0인 값을 제외하고, 인덱스를 인덱스 값만큼 출력</h5>
<pre><code class="language-c">// 원래 배열에 정렬된 값 채우기
int j = 0;
for (int i = 0; i &lt;= max; i++) {
    while (count[i] &gt; 0){
        arr[j++] = i;
        count[i]--;
    }
}</code></pre>
<hr />
<h3 id="3-시간-복잡도">3. 시간 복잡도</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/da02b417-9af8-4178-a790-8ad7e854223e/image.png" /></p>
<p>계수 정렬의 시간 복잡도: O(N + K)</p>
<ul>
<li>N : 정렬할 데이터의 개수</li>
<li>K : 데이터의 최댓값(count 배열의 크기)</li>
</ul>
<p>계수 정렬은 데이터를 한 번 순회하며 카운팅하고(<code>O(N)</code>), count 배열을 순회하며 결과를 생성( <code>O(K)</code> ) 하므로 총 <code>O(N + K)</code> 의 시간 복잡도를 갖는다.</p>
<hr />
<h3 id="4-예제">4. 예제</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

#define SIZE 10  // 배열 크기

int main(void)
{
    // 양의 정수(0 제외)만 포함된 배열
    int data[SIZE] = { 5, 3, 1, 2, 3, 1, 7, 4, 5, 2 };

    // 1. 최댓값 찾기
    int max = data[0];
    for (int i = 1; i &lt; SIZE; i++) {
        if (data[i] &gt; max)
            max = data[i];
    }

    // 2. 계수 배열 생성 (크기: max + 1)
    // 0은 사용하지 않으므로 count[0]은 쓰지 않음
    int* count = (int*)malloc((max + 1) * sizeof(int));
    if (count == NULL) {
        printf(&quot;메모리 할당 실패\n&quot;);
        return 1;
    }

    // 3. 계수 배열 초기화 (모든 값을 0으로 설정)
    for (int i = 1; i &lt;= max; i++) {
        count[i] = 0;
    }

    // 4. 입력 배열의 값을 count 배열에 누적
    for (int i = 0; i &lt; SIZE; i++) {
        count[data[i]]++;  // 값이 i일 때 count[i]++
    }

    // 5. 정렬 결과 출력
    printf(&quot;정렬 결과: &quot;);
    for (int i = 1; i &lt;= max; i++) {
        for (int j = 0; j &lt; count[i]; j++) {
            printf(&quot;%d &quot;, i);  // count[i]만큼 i 출력
        }
    }
    printf(&quot;\n&quot;);

    // 6. 메모리 해제
    free(count);

    return 0;
}</code></pre>
<hr />
<ul>
<li>1000000개의 난수 정렬(동적 메모리 할당)</li>
</ul>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;time.h&gt;

#define SIZE 1000000   // 배열 크기

void countingSort(int* arr, int n);

int main() {
    int* arr;

    clock_t start, end;      // 시간 측정 변수 선언
    double duration;         // 경과 시간(초)

    start = clock();
    srand(2); // 난수 시드 초기화

    // 동적 메모리로 정수 배열 할당(4000000byte = 약 4mb)
    arr = (int*)malloc(sizeof(int) * SIZE);
    if (arr == NULL) {
        printf(&quot;메모리 할당 실패\n&quot;);
        return 1;
    }

    // 난수로 배열 초기화
    for (int i = 0; i &lt; SIZE; i++) {
        arr[i] = (((rand() &lt;&lt; 15) | rand()) % SIZE) + 1; // 1 ~ 1000000
    }

    printf(&quot;정렬 전\n\n&quot;);
    end = clock();           // 정렬 완료 직후 시간 저장
    duration = (double)(end - start) / CLOCKS_PER_SEC; // 초 단위로 변환
    printf(&quot;난수 배열 생성: %f초\n&quot;, duration);

    // 앞 10개만 출력
    printf(&quot;1~10번째 배열의 데이터 값 : &quot;);
    for (int i = 0; i &lt; 10; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);

    printf(&quot;%d~%d번째 배열의 데이터 값 : &quot;, SIZE - 9, SIZE);
    for (int i = SIZE - 10; i &lt; SIZE; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n\n\n&quot;);

    printf(&quot;정렬 후\n\n&quot;);
    start = clock();
    // 계수 정렬
    countingSort(arr, SIZE);
    end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf(&quot;counting Sort 소요 시간: %f초\n&quot;, duration);

    // 앞 10개만 출력
    printf(&quot;1~10번째 배열의 데이터 값 : &quot;);
    for (int i = 0; i &lt; 10; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);

    printf(&quot;%d~%d번째 배열의 데이터 값 : &quot;, SIZE - 9, SIZE);
    for (int i = SIZE - 10; i &lt; SIZE; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n\n\n&quot;);

    // 동적 메모리 해제
    free(arr);

    return 0;
}

void countingSort(int* arr, int n) {
    // 1. 배열에서 최댓값 찾기
    int max = arr[0];
    for (int i = 1; i &lt; n; i++) {
        if (arr[i] &gt; max)
            max = arr[i];
    }

    // 2. 계수 배열 만들기 (0~max까지)
    int* count = (int*)calloc(max + 1, sizeof(int));
    if (count == NULL) {
        printf(&quot;메모리 할당 실패\n&quot;);
        return;
    }

    // 3. 각 숫자의 개수 세기
    for (int i = 0; i &lt; n; i++) {
        count[arr[i]]++;
    }

    // 4. 원래 배열에 정렬된 값 채우기
    int j = 0;
    for (int i = 0; i &lt;= max; i++) {
        while (count[i] &gt; 0) {
            arr[j++] = i;
            count[i]--;
        }
    }

    free(count);
}</code></pre>
<p><strong>출력 결과:</strong></p>
<pre><code class="language-c">정렬 전

난수 배열 생성 소요 시간: 0.038000초
1~10 : 503777 937860 151363 111552 799757 119966 581343 607334 942752 198306
999991~1000000 : 463093 670284 927498 30188 990440 193910 937327 668784 78514 849452

정렬 후

countingSort 소요 시간: 0.013000초
1~10 : 1 2 2 3 4 4 5 5 5 5
999991~1000000 : 999992 999992 999993 999993 999994 999995 999995 999997 999999 1000000</code></pre>
<hr />
<ul>
<li>1000000개의 난수 정렬(정적 메모리 할당) - 스택 오버플로우 발생</li>
</ul>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;time.h&gt;

#define SIZE 1000000   // 배열 크기

void countingSort(int* arr, int n);

int main() {
    int arr[SIZE] = { 0 };   // 정적 메모리로 정수 배열 할당

    clock_t start, end;      // 시간 측정 변수 선언
    double duration;         // 경과 시간(초)

    start = clock();
    srand(2); // 난수 시드 초기화

    if (arr == NULL) {
        printf(&quot;메모리 할당 실패\n&quot;);
        return 1;
    }

    // 난수로 배열 초기화
    for (int i = 0; i &lt; SIZE; i++) {
        arr[i] = (((rand() &lt;&lt; 15) | rand()) % SIZE) + 1; // 1 ~ 1000000
    }

    printf(&quot;정렬 전\n\n&quot;);
    end = clock();           // 정렬 완료 직후 시간 저장
    duration = (double)(end - start) / CLOCKS_PER_SEC; // 초 단위로 변환
    printf(&quot;난수 배열 생성: %f초\n&quot;, duration);

    // 앞 10개만 출력
    printf(&quot;1~10번째 배열의 데이터 값 : &quot;);
    for (int i = 0; i &lt; 10; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);

    printf(&quot;%d~%d번째 배열의 데이터 값 : &quot;, SIZE - 9, SIZE);
    for (int i = SIZE - 10; i &lt; SIZE; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n\n\n&quot;);

    printf(&quot;정렬 후\n\n&quot;);
    start = clock();
    // 계수 정렬
    countingSort(arr, SIZE);
    end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf(&quot;counting Sort 소요 시간: %f초\n&quot;, duration);

    // 앞 10개만 출력
    printf(&quot;1~10번째 배열의 데이터 값 : &quot;);
    for (int i = 0; i &lt; 10; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);

    printf(&quot;%d~%d번째 배열의 데이터 값 : &quot;, SIZE - 9, SIZE);
    for (int i = SIZE - 10; i &lt; SIZE; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n\n\n&quot;);

    return 0;
}

void countingSort(int* arr, int n) {
    // 1. 배열에서 최댓값 찾기
    int max = arr[0];
    for (int i = 1; i &lt; n; i++) {
        if (arr[i] &gt; max)
            max = arr[i];
    }

    // 2. 계수 배열 만들기 (0~max까지)
    int* count = (int*)calloc(max + 1, sizeof(int));
    if (count == NULL) {
        printf(&quot;메모리 할당 실패\n&quot;);
        return;
    }

    // 3. 각 숫자의 개수 세기
    for (int i = 0; i &lt; n; i++) {
        count[arr[i]]++;
    }

    // 4. 원래 배열에 정렬된 값 채우기
    int j = 0;
    for (int i = 0; i &lt;= max; i++) {
        while (count[i] &gt; 0) {
            arr[j++] = i;
            count[i]--;
        }
    }

    free(count);
}</code></pre>
<h4 id="출력-값스택-오버-플로우-발생">&gt; 출력 값(스택 오버 플로우 발생)</h4>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/df33ec37-3ccd-4195-805d-09ed1523bfea/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6a92f445-ffbb-47a8-8b4e-636b7f7075c7/image.png" /></p>
<h4 id="스택-오버플로우란">스택 오버플로우란?</h4>
<ul>
<li>프로그램이 스택에 할당할 수 있는 범위를 넘어서서<strong>다른 메모리 공간을 침범하는 오류</strong></li>
</ul>
<hr />
<h3 id="스택의-메모리-크기는-작은-편-기본-18mb-수준">스택의 메모리 크기는 작은 편 (기본 1~8MB 수준)</h3>
<ul>
<li>스택은 함수 호출, 지역 변수 저장용으로 사용된다.</li>
<li>OS가 스택에 할당하는 메모리는 매우 제한적이다.<ul>
<li>리눅스: 기본 8MB</li>
<li>윈도우: 기본 1MB</li>
</ul>
</li>
<li>즉, <code>int arr[1000000]</code> → 4MB로 선언하면<br />→ 스택에 너무 큰 공간을 요구하게 되어 <strong>오버플로우</strong></li>
</ul>
<hr />
<h3 id="힙은-훨씬-큰-메모리-공간을-가짐">힙은 훨씬 큰 메모리 공간을 가짐</h3>
<ul>
<li><code>malloc</code>/<code>calloc</code> 같은 동적할당은 힙(Heap) 메모리를 사용한다.</li>
<li>힙은 운영체제가 프로세스에 넉넉하게 할당해준다. (보통 수백 MB ~ 수 GB까지 가능)</li>
<li>그래서 같은 배열이라도 <code>malloc</code>을 쓰면 메모리가 넉넉해서 문제가 안 생긴다.</li>
</ul>
<hr />
<h3 id="비교-스택-vs-힙">비교: 스택 vs 힙</h3>
<table>
<thead>
<tr>
<th>항목</th>
<th>스택 (Stack)</th>
<th>힙 (Heap)</th>
</tr>
</thead>
<tbody><tr>
<td>할당 방식</td>
<td>컴파일러가 자동 할당</td>
<td>프로그래머가 직접 할당/해제</td>
</tr>
<tr>
<td>크기 제한</td>
<td>매우 작음 (1~8MB)</td>
<td>큼 (수백 MB 이상 가능)</td>
</tr>
<tr>
<td>속도</td>
<td>매우 빠름</td>
<td>느림 (시스템 호출 포함)</td>
</tr>
<tr>
<td>수명</td>
<td>함수 종료 시 소멸</td>
<td>수동으로 <code>free()</code> 필요</td>
</tr>
<tr>
<td>오버플로우 위험</td>
<td>큰 배열, 재귀 등에서 발생</td>
<td>거의 없음 (메모리 부족 시 에러)</td>
</tr>
</tbody></table>
<hr />
<blockquote>
<p><em>Reference</em> :</p>
<ol>
<li><a href="https://naver.me/FDGDE39a">https://naver.me/FDGDE39a</a></li>
<li><a href="https://naver.me/Grew0i1s">https://naver.me/Grew0i1s</a></li>
<li><a href="https://helloworld-japan.tistory.com/33?utm_source=chatgpt.com">https://helloworld-japan.tistory.com/33?utm_source=chatgpt.com</a></li>
<li><a href="https://velog.io/@dhldksgehl/%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%9D%98-%EA%B5%AC%EC%A1%B0-%EC%8A%A4%ED%83%9D-vs.-%ED%9E%99">https://velog.io/@dhldksgehl/%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%9D%98-%EA%B5%AC%EC%A1%B0-%EC%8A%A4%ED%83%9D-vs.-%ED%9E%99</a></li>
<li><a href="https://velog.io/@limielife/%EB%B0%B1%EC%A4%8010989-%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%B4%88%EA%B3%BC-%EA%B3%B5%EA%B0%84%EB%B3%B5%EC%9E%A1%EB%8F%84">https://velog.io/@limielife/%EB%B0%B1%EC%A4%8010989-%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%B4%88%EA%B3%BC-%EA%B3%B5%EA%B0%84%EB%B3%B5%EC%9E%A1%EB%8F%84</a></li>
</ol>
</blockquote>