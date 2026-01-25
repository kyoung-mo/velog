<h3 id="1-버킷-정렬">1. 버킷 정렬</h3>
<ul>
<li>데이터를 여러 개의 버킷에 나누고, 각 버킷을 개별적으로 정렬한 다음 결과를 합치는 방식이다.</li>
<li>주로 데이터가 균등하게 분포해 있을 때 효율적이다.</li>
<li>데이터가 한쪽으로 쏠려 있으면 정렬 성능이 저하된다.</li>
</ul>
<h3 id="2-버킷-정렬-알고리즘">2. 버킷 정렬 알고리즘</h3>
<p>버킷 정렬은 데이터 분할, 정렬, 합치기 과정을 수행합니다.</p>
<ul>
<li>“분할” 과정에서는 비슷한 값끼리 한 버킷에 모은다.</li>
<li>“정렬” 과정에서는 각 버킷을 정렬한다.</li>
<li>“합치기” 과정에서 각 버킷을 순서대로 이어붙인다.</li>
</ul>
<hr />
<h3 id="2-1-분할">2-1) 분할</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8d4a6edc-2304-427d-9374-f9e2a6803cf0/image.png" /></p>
<p>이런 데이터가 존재한다고 가정하였을 때 정렬할 데이터의 개수를 파악하여 버킷을 나눕니다.</p>
<hr />
<h3 id="2-2-정렬">2-2) 정렬</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f75c922a-72da-4715-bfe2-28c972c01a8d/image.png" /></p>
<ul>
<li>버킷을 10개로 나누어 <code>버킷 0</code> 에 한자리 숫자인 7을, <code>버킷 1</code> 은 비워져 있으므로 건너뛰고, 
<code>버킷 2</code> 에는 십의자리 숫자가 2인 항목을 넣습니다. 계속해서 <code>버킷 9</code> 까지 채워나갑니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/834afd04-3103-4b56-b97e-5fc58623d685/image.png" /></p>
<ul>
<li><p><code>버킷 0</code>과 <code>버킷 1</code> 자리는 비어있거나 값이 하나이므로 건너뜁니다.</p>
</li>
<li><p><code>버킷 2</code> 자리에는 index 0~2 이 존재하므로 index 1(그림상 25) 과 index 0, index 2 각각 비교하여 낮은숫자가 낮은 index 가 되도록 삽입 정렬합니다.</p>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5e94aab5-5d08-43fc-b8f8-cd34142a9b3c/image.png" /></p>
<ul>
<li><code>버킷 3</code> 자리에는 index 0~1 이 존재하므로 index 1(그림상 31)과 index 0 을 비교하여 낮은숫자가 낮은 index 가 되도록 삽입 정렬합니다.</li>
</ul>
<p>나머지 버킷 자리는 비어있거나 값이 하나이므로 건너뜁니다.</p>
<hr />
<h3 id="2-3-합치기">2-3) 합치기</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1ef7c451-1611-4a98-a430-dc3e9ae85847/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a1264d83-16c9-4659-8df9-4d71bd242d53/image.png" /></p>
<p>비어있지 않은 버킷들을 차례로 정렬합니다. index 가 1 이상 있는 버킷의 경우 index 0부터 차례로 정렬하여 합칩니다.</p>
<hr />
<h3 id="3-버킷-정렬-시간복잡도">3. 버킷 정렬 시간복잡도</h3>
<p>시간 복잡도: <code>O(n + k)</code> ~ <code>O(n²)</code></p>
<p>n: 정렬할 데이터의 개수
k: 버킷의 개수</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5e4f9768-c641-42fc-811d-7b3207dced3f/image.png" /></p>
<p>버킷 정렬은 데이터를 버킷에 분배(<code>O(n)</code> ) 하고, 각 버킷 내부를 정렬(<code>O(n/k * log(n/k)</code>)한 후 합치는 (<code>O(n)</code>) 과정을 거친다.</p>
<p>데이터가 균등하게 분포 되어있다면 시간 복잡도는 <code>O(n+k)</code>로 매우 빠르나, 모든 데이터가 한 버킷에 몰리면 <code>O(n^2)</code> 으로 느려진다.</p>
<hr />
<h3 id="4-버킷-정렬-예제">4. 버킷 정렬 예제</h3>
<h4 id="4-1-10개-데이터-예제">4-1) 10개 데이터 예제</h4>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;time.h&gt;
// 버킷 개수
#define SIZE 10

void grandom(int arr[], int n, int max);
void bucketsort(int arr[], int n, int max);

int main(void) {
    srand(time(NULL));
    int arr[SIZE];

    // 1~100 범위 난수 10개 생성
    grandom(arr, 10, 100);

    // 초기 배열 출력
    printf(&quot;초기 배열: &quot;);
    for (int i = 0; i &lt; 10; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);

    // 버킷 정렬 함수로 데이터 배열과 버킷 갯수 함께 요청
    bucketsort(arr, 10, 100);

    // 정렬된 결과 출력
    printf(&quot;정렬된 결과: &quot;);
    for (int i = 0; i &lt; 10; i++) {
        printf(&quot;%d &quot;, arr[i]);
    }
    printf(&quot;\n&quot;);

    return 0;
}

// 난수 생성 함수
void grandom(int arr[], int n, int max) {
    for (int i = 0; i &lt; n; i++) {
        arr[i] = rand() % max + 1;
    }
}

// 버킷 정렬 함수
void bucketsort(int arr[], int n, int max) {
    int bucketCount = n;//버킷의 개수
    int bucketRange = max / bucketCount;//각 버킷의 범위
    int* buckets[n];
    int count[n] = { 0 };

    // 버킷 메모리 동적 할당
    for (int i = 0; i &lt; bucketCount; i++) {
        buckets[i] = (int*)malloc(n * sizeof(int));
    }

    // 분배
    for (int i = 0; i &lt; n; i++) {
        int index = (arr[i] - 1) / bucketRange;
        buckets[index][count[index]++] = arr[i];
    }

    // 버킷 분배 결과 출력
    printf(&quot;\n--- 버킷 분배 결과 ---\n&quot;);
    for (int i = 0; i &lt; bucketCount; i++) {
        printf(&quot;Bucket[%d]: &quot;, i);
        for (int j = 0; j &lt; count[i]; j++) {
            printf(&quot;%d &quot;, buckets[i][j]);
        }
        printf(&quot;\n&quot;);
    }

    // 정렬 과정 출력
    printf(&quot;\n--- 각 버킷 정렬 과정 ---\n&quot;);
    for (int i = 0; i &lt; bucketCount; i++) {
        for (int j = 1; j &lt; count[i]; j++) {
            int key = buckets[i][j];
            int k = j - 1;
            while (k &gt;= 0 &amp;&amp; buckets[i][k] &gt; key) {
                buckets[i][k + 1] = buckets[i][k];
                k--;
            }
            buckets[i][k + 1] = key;

            // 버킷 i의 현재 상태 출력
            printf(&quot;Bucket[%d] after step %d: &quot;, i, j);
            for (int m = 0; m &lt; count[i]; m++) {
                printf(&quot;%d &quot;, buckets[i][m]);
            }
            printf(&quot;\n&quot;);
        }
    }
    printf(&quot;\n&quot;);

    // 정렬 상태 배열 저장
    int idx = 0;
    for (int i = 0; i &lt; bucketCount; i++) {
        for (int j = 0; j &lt; count[i]; j++) {
            arr[idx++] = buckets[i][j];
        }
    }

    // 메모리 해제
    for (int i = 0; i &lt; bucketCount; i++) {
        free(buckets[i]);
    }
}</code></pre>
<hr />
<h3 id="4-1-실행-결과">4-1) 실행 결과</h3>
<pre><code class="language-c">초기 배열: 1 69 31 31 5 83 37 87 48 47

--- 버킷 분배 결과 ---
Bucket[0]: 1 5
Bucket[1]:
Bucket[2]:
Bucket[3]: 31 31 37
Bucket[4]: 48 47
Bucket[5]:
Bucket[6]: 69
Bucket[7]:
Bucket[8]: 83 87
Bucket[9]:

--- 각 버킷 정렬 과정 ---
Bucket[0] after step 1: 1 5
Bucket[3] after step 1: 31 31 37
Bucket[3] after step 2: 31 31 37
Bucket[4] after step 1: 47 48
Bucket[8] after step 1: 83 87

정렬된 결과: 1 5 31 31 37 47 48 69 83 87

C:\studyC\hello_world\x64\Debug\hello_world.exe(프로세스 17556)이(가) 0 코드(0x0)와 함께 종료되었습니다.
이 창을 닫으려면 아무 키나 누르세요...</code></pre>
<hr />
<h3 id="4-2-100만-데이터-고정-10개-버킷-코드-및-결과">4-2) 100만 데이터, 고정 10개 버킷 코드 및 결과</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;time.h&gt;
#define SIZE 1000000   // 배열 크기
void bucketSort(int arr[], int n) {
    clock_t start = clock(), end;
    double elapsed;
    int max = 1000000;
    int bucketRange = 100000;
    int bucketCount = 10;

    int* buckets[10]; //버킷이 10개
    int count[10];    // 각 버킷에 현재 몇 개 들어갔는지

    for (int i = 0; i &lt; bucketCount; i++) {
        buckets[i] = (int*)malloc(n * sizeof(int));
        count[i] = 0;
    } // 버킷 하나당 n개만큼의 공간을 부여 -&gt;메모리 낭비 심함

    for (int i = 0; i &lt; n; i++) //전체 데이터 한번 훑음
    {     // 버킷번호 정해주는 것  index가 버킷 번호
        int index = arr[i] / bucketRange;
         // 9번 버킷범위 밖의 수를 9번버킷에 넣기위해
         if (index == 10) index--; 
        //index번 버킷 안에 실제로 들어있는 값으 개수 세는것
        buckets[index][count[index]++] = arr[i];
    } 
    for (int i = 0; i &lt; bucketCount; i++) {
        printf(&quot;bucket[%d] : &quot;, i);
        for (int j = 0; j &lt; 5; j++) {
            printf(&quot;%d &quot;, buckets[i][j]);
        }
        printf(&quot;\n&quot;);
    }
    end = clock();
    elapsed = (double)(end - start) / CLOCKS_PER_SEC;
    printf(&quot;실행 시간: %.3f초\n&quot;, elapsed);

    printf(&quot;\n&quot;);
   //버킷 내부를 삽입정렬로 정렬
    for (int i = 0; i &lt; bucketCount; i++) {
        for (int j = 1; j &lt; count[i]; j++) {
            int key = buckets[i][j];
            int k = j - 1;

            while (k &gt;= 0 &amp;&amp; buckets[i][k] &gt; key) {
                buckets[i][k + 1] = buckets[i][k];
                k--;
            }
            buckets[i][k + 1] = key;
        }
    }
    // 각 버킷에 들어있는 값들을 순서대로 배열에 합쳐 넣는 과정     
    int idx = 0;
    for (int i = 0; i &lt; bucketCount; i++) {
        for (int j = 0; j &lt; count[i]; j++) {
            arr[idx++] = buckets[i][j];
            //i번에 있는 버킷에 들어있는 j번쨰 값들 arr에 넣기
        }
    }

    for (int i = 0; i &lt; bucketCount; i++) {
        printf(&quot;bucket[%d] : &quot;, i);
        for (int j = 0; j &lt; 5; j++) {
            printf(&quot;%d &quot;, buckets[i][j]);
        }
        printf(&quot;\n&quot;);
    }
    end = clock();
    elapsed = (double)(end - start) / CLOCKS_PER_SEC;
    printf(&quot;실행 시간: %.3f초\n&quot;, elapsed);
    printf(&quot;\n&quot;);
    for (int i = 0; i &lt; bucketCount; i++)
        free(buckets[i]);
}

int rand20() {
    return ((rand() &amp; 0x7FFF) &lt;&lt; 5) | (rand() &amp; 0x1F);
}

int main() {
    int* arr;
    clock_t start = clock(), end;
    double elapsed;
    srand(0); // 난수 시드 초기화

    // 동적 메모리로 정수 배열 할당
    arr = (int*)malloc(sizeof(int) * SIZE);
    if (arr == NULL) {
        printf(&quot;메모리 할당 실패\n&quot;);
        return 1;
    }

    // 난수로 배열 초기화
    for (int i = 0; i &lt; SIZE; i++) {
        arr[i] = rand20() % SIZE + 1;
    }

    bucketSort(arr, SIZE);

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
    end = clock();
    elapsed = (double)(end - start) / CLOCKS_PER_SEC;
    printf(&quot;실행 시간: %.3f초\n&quot;, elapsed);

    // 동적 메모리 해제
    free(arr);

    return 0;
}
</code></pre>
<h3 id="4-2-실행-결과">4-2) 실행 결과</h3>
<pre><code class="language-c">bucket[0] : 1224 36570 95929 78287 26908
bucket[1] : 187301 179141 149888 114088 122343
bucket[2] : 283382 267710 286254 242507 244157
bucket[3] : 334421 311223 398596 390792 392930
bucket[4] : 451134 488327 499840 406404 477527
bucket[5] : 590636 541046 533553 512663 522705
bucket[6] : 679622 657202 671252 692979 692885
bucket[7] : 755562 780418 707673 778801 773357
bucket[8] : 861711 831466 882239 833605 848967
bucket[9] : 924193 945087 903168 923893 999989
실행 시간: 0.003초

bucket[0] : 1 1 1 1 3
bucket[1] : 100001 100002 100005 100005 100006
bucket[2] : 200000 200003 200003 200003 200006
bucket[3] : 300002 300003 300006 300006 300010
bucket[4] : 400002 400002 400003 400003 400004
bucket[5] : 500002 500003 500003 500004 500007
bucket[6] : 600003 600003 600004 600005 600006
bucket[7] : 700001 700002 700005 700006 700007
bucket[8] : 800000 800002 800002 800002 800003
bucket[9] : 900000 900000 900003 900003 900004
실행 시간: 6.925초

1~10 : 1 1 1 1 3 3 3 3 4 4
999990~1000000 : 999991 999992 999993 999993 999994 999995 999996 999996 999998 999998
실행 시간: 6.946초

C:\Project1\x64\Release\c_practice.exe(프로세스 5644)이(가) 0 코드(0x0)와 함께 종료되었습니다.
이 창을 닫으려면 아무 키나 누르세요...</code></pre>
<h3 id="4-3-최적화-버전-및-테스트-코드">4-3) 최적화 버전 및 테스트 코드</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;
#include &lt;time.h&gt;
#include &lt;math.h&gt;

#define N       1000000
#define MAXVAL  1000000

/* ---------- 난수 ---------- */
static int rand20(void) {
    return ((rand() &amp; 0x7FFF) &lt;&lt; 5) | (rand() &amp; 0x1F);
}

/* --------오름차순 qsort비교함수 */
static int cmp_int(const void* a, const void* b) {
    int x = *(const int*)a;
    int y = *(const int*)b;
    return (x &gt; y) - (x &lt; y);
}

static int is_sorted(const int* a, int n) {
    for (int i = 1; i &lt; n; i++)
        if (a[i - 1] &gt; a[i]) return 0;
    return 1;
}

/* ---------- 삽입정렬 ---------- */
static void insertion_sort(int* a, int n) {
    for (int j = 1; j &lt; n; j++) {
        int key = a[j];
        int k = j - 1;
        while (k &gt;= 0 &amp;&amp; a[k] &gt; key) {
            a[k + 1] = a[k];
            k--;
        }
        a[k + 1] = key;
    }
}

/* ---------- Sturges ---------- */
static int sturges_bucket_count(int n) {
    return (int)(1.0 + log2((double)n));
}
/*내부정렬 qsort or 삽입정렬 중 하나 사용한다 */
typedef enum {
    INTERNAL_QSORT,
    INTERNAL_INSERTION
} InternalSort;

/* ---------- 버킷정렬  ---------- */
static void bucket_sort(
    int* a, int n, int maxval,
    int bucketCount, InternalSort mode)
{    //각 버킷에 몇개 들어갈지
    int* count = calloc(bucketCount, sizeof(int));
    //초기값 0으로 채움 ,
    int* pos = calloc(bucketCount, sizeof(int));
    //각 버킷
    int** buckets = calloc(bucketCount, sizeof(int*));

    if (!count || !pos || !buckets) exit(1);

    /* 1-pass : count */
    for (int i = 0; i &lt; n; i++) {
        int num = a[i];
        int idx = (int)((long long)num * bucketCount / (maxval + 1));
        if (idx &gt;= bucketCount) idx = bucketCount - 1;
        count[idx]++;
    }

    /* exact alloc 각 버킷에 들어온개수만큼 할당*/
    for (int i = 0; i &lt; bucketCount; i++)
        if (count[i] &gt; 0)
            buckets[i] = malloc(sizeof(int) * count[i]);

    /* 2-pass : fill */
    for (int i = 0; i &lt; n; i++) {
        int num = a[i];
        int idx = (int)((long long)num * bucketCount / (maxval + 1));
        if (idx &gt;= bucketCount) idx = bucketCount - 1;
        buckets[idx][pos[idx]++] = num;
        //pos는 지금까지 몇개 넣었는지 뜻한다 버킷안에서 번호/
    }

    /* i*/internal sort */
    for (int i = 0; i &lt; bucketCount; i++) {
        int m = count[i];
        if (m &lt;= 1) continue;
        if (mode == INTERNAL_QSORT)
            qsort(buckets[i], m, sizeof(int), cmp_int);
        else
            insertion_sort(buckets[i], m);
    }

    /* gather */
    int k = 0;
    for (int i = 0; i &lt; bucketCount; i++) {
        for (int j = 0; j &lt; count[i]; j++)
            a[k++] = buckets[i][j];
        free(buckets[i]);
    }

    free(buckets);
    free(count);
    free(pos);
}

/* 내부정렬 퀵소트 vs 내부정렬 비교 */
static void run_case(
    const char* label,
    int* base, int* work,
    int bucketCount, InternalSort mode)
{
    memcpy(work, base, sizeof(int) * N);

    clock_t st = clock();
    bucket_sort(work, N, MAXVAL, bucketCount, mode);
    clock_t ed = clock();

    printf(&quot;%-20s | buckets=%6d | %-9s | %.3f sec | %s\n&quot;,
        label,
        bucketCount,
        (mode == INTERNAL_QSORT ? &quot;qsort&quot; : &quot;insertion&quot;),
        (double)(ed - st) / CLOCKS_PER_SEC,
        is_sorted(work, N) ? &quot;YES&quot; : &quot;NO&quot;);
}

/* ---------- main ---------- */
int main(void)
{
    srand(0);

    int* base = malloc(sizeof(int) * N);
    int* work = malloc(sizeof(int) * N);

    for (int i = 0; i &lt; N; i++)
        base[i] = rand20() % MAXVAL + 1;

    int b_sturges = sturges_bucket_count(N);
    int bucket_list[4] = { 10, b_sturges, 500, 10000 };
    const char* names[4] = {
        &quot;Bucket(10)&quot;, &quot;Bucket(Sturges)&quot;,
        &quot;Bucket(500)&quot;, &quot;Bucket(10000)&quot; };
    printf(&quot;N=%d, MAXVAL=%d, Sturges=%d\n&quot;, N, MAXVAL, b_sturges);
    printf(&quot;Sturges bucket count = %d\n\n&quot;, b_sturges);
    ;

    printf(&quot;N=%d, MAXVAL=%d\n\n&quot;, N, MAXVAL);

    printf(&quot;=== Bucket + QuickSort ===\n&quot;);
    for (int i = 0; i &lt; 4; i++)
        run_case(names[i], base, work, bucket_list[i], INTERNAL_QSORT);

    printf(&quot;\n=== Bucket + InsertionSort ===\n&quot;);
    for (int i = 0; i &lt; 4; i++)
        run_case(names[i], base, work, bucket_list[i], INTERNAL_INSERTION);

    free(base);
    free(work);
    return 0;
}
</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6109ac84-8a17-4f69-89a3-deab330800ff/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/abf8a0c9-9bc3-421e-895e-48336bdcd10a/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7e515976-a627-47e7-90ad-3361acf01a67/image.png" /></p>