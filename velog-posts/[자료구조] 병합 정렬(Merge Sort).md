<h1 id="병합-정렬-개념">병합 정렬 개념</h1>
<ul>
<li>배열을 반 씩 나눠서 재귀적으로 호출</li>
<li>다 나눠진 상태에서 합치며 정렬을 반복하는 분할 정복 방식, 안정 정렬</li>
<li>시간 복잡도 : <code>O(NlogN)</code></li>
</ul>
<hr />
<h3 id="0-정렬-전-배열-선언">0. 정렬 전 배열 선언</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/93c977e1-693b-428d-aa49-e8c1684f75a0/image.png" /></p>
<pre><code class="language-c">#define size 8
int* arr;
arr = (int*)malloc(sizeof(int) * size);
 if (arr == NULL)
 {
     printf(&quot;메모리 할당 실패\n&quot;);
     return 1;
 }

 srand(0); 
   for (int i = 0; i &lt; size; i++)
  {
      arr[i] = ((rand() &lt;&lt; 15) | rand()) % (size + 1);
  }
</code></pre>
<h3 id="1-배열을-반씩-나누는-과정-재귀적으로-호출">1. 배열을 반씩 나누는 과정 재귀적으로 호출</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b3e83fa0-9c03-41d8-8de7-9d39ad04237a/image.png" /></p>
<pre><code class="language-c">void mergeSort(int arr[], int left, int right)
{
    if (left &lt; right)// 반을 나눈 오른쪽 같이 왼쪽 시작점과 같아질떄까지 반복
    {
        int mid = (left + right) / 2;  // 중간 지점 계산

        mergeSort(arr, left, mid);      // 왼쪽 절반 정렬
        mergeSort(arr, mid + 1, right); // 오른쪽 절반 정렬

        merge(arr, left, mid, right);   // 정렬된 두 배열 병합
    }
}</code></pre>
<h3 id="2-나눠진-항목들을-정렬하며-합치는-과정을-반복하며-완성">2. 나눠진 항목들을 정렬하며 합치는 과정을 반복하며 완성</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/eb2e884f-39fb-4a8a-aad4-c4603489a5a9/image.png" /></p>
<pre><code class="language-c">// 병합 정렬의 핵심: 두 배열을 합쳐주는 함수
void merge(int arr[], int left, int mid, int right)
{
    int* temp = (int*)malloc((right - left + 1) * sizeof(int));
    int i = left;     // 왼쪽 시작
    int j = mid + 1;  // 오른쪽 시작
    int k = 0;        // temp 인덱스

    // 작은 값부터 temp에 저장
    while (i &lt;= mid &amp;&amp; j &lt;= right)
    {
        if (arr[i] &lt;= arr[j])
            temp[k++] = arr[i++];
        else
            temp[k++] = arr[j++];
    }

    // 왼쪽 배열 남은 값
    while (i &lt;= mid)
        temp[k++] = arr[i++];

    // 오른쪽 배열 남은 값
    while (j &lt;= right)
        temp[k++] = arr[j++];

    // temp를 원래 배열에 복사
    for (i = left, k = 0; i &lt;= right; i++, k++)
        arr[i] = temp[k];

    free(temp);
}</code></pre>
<hr />
<h2 id="병합-정렬-시간복잡도-증명">병합 정렬 시간복잡도 증명</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6340dbcf-ee9d-4c6c-985e-25a87ace00bf/image.png" /></p>
<blockquote>
<p>항상 <code>O(NlogN)</code> 의 시간 복잡도를 가진다.</p>
</blockquote>
<hr />
<h2 id="병합-정렬-코드">병합 정렬 코드</h2>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;time.h&gt;

#define size 1000000

void mergeSort(int arr[], int left, int right);
void merge(int arr[], int left, int mid, int right);
int* make_dataset(int n);
void print_dataset(int* arr);

int main()
{
    int* arr;
    arr = (int*)malloc(sizeof(int) * size);
    if (arr == NULL)
    {
        printf(&quot;메모리 할당 실패\n&quot;);
        return 1;
    }
    srand(0); // 난수 시드 초기화

    // 동적 메모리로 정수 배열 할당

    // 난수로 배열 초기화

    for (int i = 0; i &lt; size; i++)
    {
        arr[i] = ((rand() &lt;&lt; 15) | rand()) % (size + 1); // 0 ~ 32767 rand 값은 32767이 최대
    }



    clock_t start, end;      // 시간 측정 변수 선언
    double duration;


    printf(&quot;1~10정렬 전 배열: &quot;);

    for (int i = 0; i &lt; 10; i++)
    {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);

    mergeSort(arr, 0, 9);

    printf(&quot;1~10정렬 후 배열: &quot;);
    for (int i = 0; i &lt; 10; i++)
    {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);
    start = clock();
    mergeSort(arr, 0, 9);
    end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf(&quot;mergeSort 소요 시간: %.15f초\n&quot;, duration);

    printf(&quot;\n&quot;);

    printf(&quot;999990~1000000정렬 전 배열: &quot;);

    for (int i = size - 10; i &lt; size; i++)
    {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);

    mergeSort(arr, size - 10, size - 1);

    printf(&quot;999990~1000000정렬 후 배열: &quot;);
    for (int i = size - 10; i &lt; size; i++)
    {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);
    start = clock();
    mergeSort(arr, size - 10, size - 1);
    end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf(&quot;mergeSort 소요 시간: %.15f초\n&quot;, duration);



    printf(&quot;\n&quot;);


    mergeSort(arr, 0, size - 1);

    printf(&quot;전체 정렬 후 뒤에 10개 배열: &quot;);
    for (int i = size - 10; i &lt; size; i++)
    {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);

    start = clock();
    mergeSort(arr, 0, size - 1);
    end = clock();
    duration = (double)(end - start) / CLOCKS_PER_SEC;
    printf(&quot;mergeSort 소요 시간: %f초\n&quot;, duration);





    return 0;
}







// 분할하고 다시 정렬을 맡는 함수
void mergeSort(int arr[], int left, int right)
{
    if (left &lt; right)// 반을 나눈 오른쪽 같이 왼쪽 시작점과 같아질떄까지 반복
    {
        int mid = (left + right) / 2;  // 중간 지점 계산

        mergeSort(arr, left, mid);      // 왼쪽 절반 정렬
        mergeSort(arr, mid + 1, right); // 오른쪽 절반 정렬

        merge(arr, left, mid, right);   // 정렬된 두 배열 병합
    }
}
// 병합 정렬의 핵심: 두 배열을 합쳐주는 함수
void merge(int arr[], int left, int mid, int right)
{
    int* temp = (int*)malloc((right - left + 1) * sizeof(int));
    int i = left;     // 왼쪽 시작
    int j = mid + 1;  // 오른쪽 시작
    int k = 0;        // temp 인덱스

    // 작은 값부터 temp에 저장
    while (i &lt;= mid &amp;&amp; j &lt;= right)
    {
        if (arr[i] &lt;= arr[j])
            temp[k++] = arr[i++];
        else
            temp[k++] = arr[j++];
    }

    // 왼쪽 배열 남은 값
    while (i &lt;= mid)
    {
        temp[k++] = arr[i++];
    }
    // 오른쪽 배열 남은 값
    while (j &lt;= right)
    {
        temp[k++] = arr[j++];
    }
    // temp를 원래 배열에 복사
    for (i = left, k = 0; i &lt;= right; i++, k++)
    {
        arr[i] = temp[k];
    }
    free(temp);
}


int* make_dataset(int n)
{
    int* arr;
    srand(0); // 난수 시드 초기화

    // 동적 메모리로 정수 배열 할당
    arr = (int*)malloc(sizeof(int) * n);
    if (arr == NULL) 
    {
        printf(&quot;메모리 할당 실패\n&quot;);
        return NULL;
    }

    // 난수로 배열 초기화
    for (int i = 0; i &lt; n; i++) 
    {
        //arr[i] = rand() % (SIZE + 1); // rand()=&gt; 32768 16bit까지만 표현
        arr[i] = ((rand() &lt;&lt; 15) | rand()) % (n + 1);
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

    printf(&quot;%d~%d : &quot;, size - 10, size);
    for (int i = size - 10; i &lt; size; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);
}</code></pre>
<h4 id="데이터-100만개일-때-소요-시간--0305초">데이터 100만개일 때 소요 시간 = 0.305초</h4>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/87b743da-caa9-4149-ac0e-42b5b483347b/image.png" /></p>