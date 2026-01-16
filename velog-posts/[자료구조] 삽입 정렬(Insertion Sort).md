<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/209cf4d4-e8e9-496d-ab02-4ee578a0e7d6/image.png" /></p>
<h2 id="삽입-정렬-개념">삽입 정렬 개념</h2>
<p>우리가 카드를 손에 들고 정렬한다고 가정할 때,</p>
<ol>
<li>처음에 한 장을 손에 든다. </li>
<li>그다음 카드를 한 장씩 받아서, 이미 손에 들고 있는 카드들 중에서 알맞은 위치에 끼워 넣는다. </li>
</ol>
<p>위 과정이 삽입 정렬의 과정이다.</p>
<hr />
<h2 id="특징">특징</h2>
<ol>
<li><p>정렬이 거의 되어 있을수록 빠르다.</p>
</li>
<li><p>안정 정렬로, 동일한 값의 순서가 유지된다.</p>
<p> ex) 철수 : 90, 영희 : 75, 민수 : 90, 수지 : 75
 → 영희 : 75, 수지 : 75, 철수 : 90, 민수 : 90
 같은 점수끼리도 순서를 유지한다는 특징 </p>
</li>
</ol>
<hr />
<h2 id="시간-복잡도">시간 복잡도</h2>
<p><strong>최선의 경우 (Best Case) - O(n)</strong></p>
<ul>
<li>배열이 이미 정렬된 상태일 때</li>
<li>한 번의 비교만으로 위치가 결정되므로 반복이 거의 없음</li>
<li>비교만 수행하고, 이동(shift) 없이 지나감</li>
</ul>
<p><strong>평균적인 경우 (Average Case) - O(n²)</strong></p>
<ul>
<li>배열이 무작위로 섞여 있는 상태</li>
<li>앞쪽 정렬된 부분을 탐색하며 삽입 위치를 찾기 때문에</li>
<li>비교 및 이동이 반복적으로 발생</li>
</ul>
<p><strong>최악의 경우 (Worst Case) - O(n²)</strong></p>
<ul>
<li>배열이 내림차순(역순)으로 정렬되어 있을 때</li>
<li>매번 모든 앞쪽 원소와 비교 및 이동이 필요</li>
<li>가장 많은 연산이 발생</li>
</ul>
<p>자료의 양이 적거나, 이미 정렬된 자료라면 매우 효율적인 정렬 방법이다.</p>
<h2 id="공간-복잡도---o1">공간 복잡도 - O(1)</h2>
<ul>
<li>입력 크기와 무관하게 일정한 시간</li>
<li>추가적인 메모리 공간을 거의 사용하지 않는다.</li>
</ul>
<hr />
<h3 id="adt">ADT</h3>
<p>임시변수 temp에 값을 넣음</p>
<table>
<thead>
<tr>
<th>temp</th>
</tr>
</thead>
<tbody><tr>
<td></td>
</tr>
</tbody></table>
<table>
<thead>
<tr>
<th>4</th>
<th>3</th>
<th>5</th>
<th>1</th>
<th>2</th>
</tr>
</thead>
<tbody><tr>
<td>a[0]</td>
<td>a[1]</td>
<td>a[2]</td>
<td>a[3]</td>
<td>a[4]</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody></table>
<hr />
<table>
<thead>
<tr>
<th>패스</th>
<th>꺼내는 인덱스</th>
<th>비교 인덱스</th>
<th>정렬 후 배열 상태</th>
<th>정렬 완료</th>
</tr>
</thead>
<tbody><tr>
<td>1패스</td>
<td>1</td>
<td>0</td>
<td>3 4 5 1 2</td>
<td>a[0], a[1] 정렬됨</td>
</tr>
<tr>
<td>2패스</td>
<td>2</td>
<td>1, 0</td>
<td>3 4 5 1 2</td>
<td>a[2] 정렬됨</td>
</tr>
<tr>
<td>3패스</td>
<td>3</td>
<td>2, 1, 0</td>
<td>1 3 4 5 2</td>
<td>a[3] 정렬됨</td>
</tr>
<tr>
<td>4패스</td>
<td>4</td>
<td>3, 2, 1, 0</td>
<td>1 2 3 4 5</td>
<td>a[4] 정렬됨</td>
</tr>
</tbody></table>
<hr />
<h3 id="삽입-정렬-예제-1">삽입 정렬 예제 1)</h3>
<pre><code class="language-c">/* 예시 부분 삽입 정렬 구현 */
#include &lt;stdio.h&gt;

#define SIZE 5

int main(void){
    int i, j; // i는 위치 인자, j는 비교 인자
    int arr[SIZE] = {4, 3, 5, 1, 2}; 

    // 정렬 전 배열 출력
    printf(&quot;--- 삽입 정렬 전 출력 ---\n&quot;);
    for (int i = 0; i &lt; SIZE; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }    

    /* 삽입 정렬 알고리즘 */
    // i는 1부터 시작: 첫 번째 카드(arr[0])는 정렬되어 있다고 가정
    // 두 번째 카드부터 시작
    for (i = 1; i &lt; SIZE; i++) { // 두번째요소부터 하나씩 끼울위치 잦기
        int temp = arr[i];       // 현재 삽입할 값을 임시로 저장

        // 앞쪽의 정렬된 부분과 비교하면서 삽입 위치 찾기
        // j = i : 현재 값을 기준으로
        // 왼쪽에 있는 정렬된 부분과 비교를 시작하기 위해 설정

        // 조건 1: j 가 0이 되면 종료되고
        // 그값이 temp보다크면 오른쪽으로 한칸 shift(이동)
        for (j = i; j &gt; 0 &amp;&amp; arr[j - 1] &gt; temp; j--) {
            arr[j] = arr[j - 1];  // 왼쪽이 더 크기 때문에 한 칸씩 오른쪽으로 shift
        }
        // 반복문이 멈춘 지점(j)이 바로 temp가 들어갈 적절한 위치
        arr[j] = temp;  // 빈위치에 temp 삽입
    }

    // 정렬 후 배열 출력
    printf(&quot;\n--- 삽입 정렬 후 출력 ---\n&quot;);
    for (int i = 0; i &lt; SIZE; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }

    return 0;
}</code></pre>
<hr />
<h3 id="삽입-정렬-예제-2">삽입 정렬 예제 2)</h3>
<pre><code class="language-c">**#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt; // malloc, free, rand 함수를 위해 필요
#include &lt;time.h&gt; // 시간 측정 및 난수 시드를 위해 필요

#define SIZE 1000000  //삽입 정렬 시 매우 느림

// 함수 declare
void generate_random_array(int* arr, int size); // 난수 배열 생성 함수
void insertion_sort(int* arr, int size);        // 삽입 정렬 함수
void print_array_edges(int* arr, int size);     // 배열 가장자리(10개) 출력 함수

int main() {
    int* arr;
    clock_t start, end; // C 언어 &lt;time.h&gt;에 정의된 시간 자료형
    double duration;

    // 동적 메모리 할당
    // 스택(Stack)은 작아서 큰 배열은 힙(Heap) 메모리에 할당해야 함
    arr = (int*)malloc(sizeof(int) * SIZE);
    if (arr == NULL) {
        printf(&quot;메모리 할당 실패\n&quot;);
        return 1;
    }

    // 난수 배열 생성
    generate_random_array(arr, SIZE);

    // 정렬 전 배열 앞/뒤 10개 출력
    printf(&quot;--- 정렬 전 배열 ---\n&quot;);
    print_array_edges(arr, SIZE);

    // 삽입 정렬 및 시간 측정
    start = clock();
    insertion_sort(arr, SIZE);
    end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;

    // 정렬 후 배열 앞/뒤 10개 출력
    printf(&quot;--- 정렬 후 배열 ---\n&quot;);
    print_array_edges(arr, SIZE);

    // 실행 시간 출력
    printf(&quot;삽입 정렬 소요 시간: %f초\n&quot;, duration);

    // 메모리 해제 - 빌려온 힙 메모리를 시스템에 반납
    free(arr);

    return 0;
}

// 난수 배열 생성
void generate_random_array(int* arr, int size) {
    srand((unsigned int)time(NULL));  // 현재 시간 기준 시드
    // 실행할 때마다 매번 다른 난수가 나오게 설정
    for (int i = 0; i &lt; size; i++) {
        arr[i] = rand() % (size);  // 0 ~ size 범위 난수
    }
}

// 삽입 정렬
void insertion_sort(int* arr, int size) {
    for (int i = 1; i &lt; size; i++) {
        int temp = arr[i];
        int j = i;
        while (j &gt; 0 &amp;&amp; arr[j - 1] &gt; temp) {
            arr[j] = arr[j - 1];
            j--;
        }
        arr[j] = temp;
    }
}

// 배열 앞 10개, 뒤 10개 출력
void print_array_edges(int* arr, int size) {
    printf(&quot;1~10 : &quot;);
    for (int i = 0; i &lt; 10; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);

    printf(&quot;%d~%d : &quot;, size - 9, size);
    for (int i = size - 10; i &lt; size; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);
}

많은양의 데이터를 정렬하기엔 오랜시간이 걸린다는 단점이있습니다.**</code></pre>
<pre><code class="language-c">-- 정렬 전 배열 ---
1~10 : 10180 8583 16949 22393 3639 12557 13132 27768 16555 18083
999991~1000000 : 27885 7254 3533 28676 17533 14564 7334 11050 7218 21905
--- 정렬 후 배열 ---
1~10 : 0 0 0 0 0 0 0 0 0 0
999991~1000000 : 32767 32767 32767 32767 32767 32767 32767 32767 32767 32767
삽입 정렬 소요 시간: 200.963000초</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/70bc6830-9dba-4c67-baf3-931c898feebe/image.png" /></p>