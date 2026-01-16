<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f9d94963-e0a1-4604-9956-ff8df4fe35ad/image.png" /></p>
<hr />
<ul>
<li>1회전:
첫 번째 자료 9를 두 번째 자료부터 마지막 자료까지와 비교하여 가장 작은 값을 첫 번째 위치에 옮겨 놓는다. 이 과정에서 자료를 4번 비교한다.</li>
<li>2회전:
두 번째 자료 6을 세 번째 자료부터 마지막 자료까지와 비교하여 가장 작은 값을 두 번째 위치에 옮겨 놓는다. 이 과정에서 자료를 3번 비교한다.</li>
<li>3회전:
세 번째 자료 7을 네 번째 자료부터 마지막 자료까지와 비교하여 가장 작은 값을 세 번째 위치에 옮겨 놓는다. 이 과정에서 자료를 2번 비교한다.</li>
<li>4회전:
네 번째 자료 9와 마지막에 있는 7을 비교하여 서로 교환한다.</li>
</ul>
<hr />
<pre><code class="language-c">for (j=1; j&lt;5; j++){
    if(a[0] &gt;a[j]){
        temp=a[0];
        a[0]=a[j];
        a[j]=temp;
    }
}</code></pre>
<hr />
<h3 id="선택-정렬-예제-1">선택 정렬 예제 1)</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;

int main(void)
{
    int a[5] = { 3,2,1,6,5 };
    int i,j, temp;
    for (i = 0; i &lt; 4; i++) {
        for (j = i + 1; j &lt; 5; j++) {
            if (a[i] &gt; a[j]) {
                temp = a[i];
                a[i] = a[j];
                a[j] = temp;
            }
        }
    }

    for (i=0;i&lt;5;i++)
    {
        printf(&quot;%5d &quot;, a[i]);
    }
    return 0;
}</code></pre>
<h3 id="선택-정렬-예제-2">선택 정렬 예제 2)</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;

int main(void)
{
    int a[5] = { 3,2,1,6,5 };
    int i,j, temp;
    int min;
    for (i = 0; i &lt; 4; i++) {
        min = i;
        for (j = i + 1; j &lt; 5; j++) {
            if (a[min] &gt; a[j]) {
                min = j;
            }            
        }
        if (min != i){
            temp = a[i];
            a[i] = a[min];
            a[min] = temp;
        }
    }

    for (i=0;i&lt;5;i++)
    {
        printf(&quot;%5d &quot;, a[i]);
    }
    return 0;
}</code></pre>
<h3 id="선택-정렬-예제-3">선택 정렬 예제 3)</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;time.h&gt;

//#define SIZE 1000000
#define SIZE 100000  

int selection_sort(int* arr, int size);

int advanced_selection_sort(int* arr, int size);

// 배열 크기
int* make_dataset(int size);
void print_dataset(int* arr);
int main() {
    int* arr;
    clock_t start, end;      // 시간 측정 변수 선언
    double duration;         // 경과 시간(초)

    start = clock();         // 정렬 시작 직전 시간 저장
    arr=make_dataset(SIZE);
    end = clock();           // 정렬 완료 직후 시간 저장
    duration = (double)(end - start) / CLOCKS_PER_SEC; // 초 단위로 변환
    printf(&quot;make_dataset() 소요 시간: %f초\n&quot;, duration);

    print_dataset(arr);


    start = clock(); 
    selection_sort(arr, SIZE);
    end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf(&quot;selection_sort 소요 시간: %f초\n&quot;, duration);


    start = clock();
    advanced_selection_sort(arr, SIZE);
    end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf(&quot;advanced_selection_sort 소요 시간: %f초\n&quot;, duration);

    print_dataset(arr);

    // 동적 메모리 해제
    free(arr);

    return 0;
}

int selection_sort(int* arr, int size)
{
    int i, j, temp;
    for (i = 0; i &lt; size - 1; i++) {
        for (j = i + 1; j &lt; size; j++) {
            if (arr[i] &gt; arr[j]) {
                temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
    }
    return 0;
}

int advanced_selection_sort(int* arr, int size)
{
    int i,j, temp;
    int min;
    for (i = 0; i &lt; size-1; i++) {
        min = i;
        for (j = i + 1; j &lt; size; j++) {
            if (arr[min] &gt; arr[j]) {
                min = j;
            }            
        }
        if (min != i){
            temp = arr[i];
            arr[i] = arr[min];
            arr[min] = temp;
        }
    }

    //for (i=0;i&lt;size;i++)
    //{
    //    printf(&quot;%7d &quot;, arr[i]);
 //       if(i%10==9) printf(&quot;\n&quot;);
    //}
    return 0;
}

int* make_dataset(int size)
{
    int* arr;
    srand(0); // 난수 시드 초기화

    // 동적 메모리로 정수 배열 할당
    arr = (int*)malloc(sizeof(int) * size);
    if (arr == NULL) {
        printf(&quot;메모리 할당 실패\n&quot;);
        return 1;
    }

    // 난수로 배열 초기화
    for (int i = 0; i &lt; SIZE; i++) {
        //arr[i] = rand() % (SIZE + 1); // rand()=&gt; 32768 16bit까지만 표현
        arr[i] = ((rand() &lt;&lt; 15) | rand()) % (size + 1);
    }

    return arr;
}

void print_dataset(int* arr)
{
    // 앞 10개만 출력
    printf(&quot;1~10 : &quot;);
    for (int i = 0; i &lt; 10; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);

    printf(&quot;%d~%d : &quot;, SIZE - 10, SIZE);
    for (int i = SIZE - 10; i &lt; SIZE; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);
}</code></pre>
<pre><code class="language-c">make_dataset() 소요 시간: 0.039000초
1~10 : 252902 928526 172147 136331 455870 819013 421300 971665 135752 220278
999990~1000000 : 55673 902648 230059 23523 288385 86000 192383 975196 218511 237549
advanced_selection_sort 소요 시간: 552.144000초
selection_sort 소요 시간: 591.209000초
1~10 : 0 3 3 4 5 6 6 8 9 11
999990~1000000 : 999991 999991 999994 999994 999997 999998 999998 999998 999998 1000000</code></pre>
<blockquote>
<ul>
<li>Reference : <a href="https://gmlwjd9405.github.io/2018/05/06/algorithm-selection-sort.html">https://gmlwjd9405.github.io/2018/05/06/algorithm-selection-sort.html</a></li>
</ul>
</blockquote>