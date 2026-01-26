<p>힙 정렬이란 힙(Heap) 자료구조를 이용한 정렬 알고리즘으로, 최대 힙 또는 최소 힙을 구성한 뒤, 루트 노드를 반복적으로 추출하여 정렬하는 방식이다.</p>
<p>힙을 알기 위해서는 완전 이진트리와, 이진트리의 개념에 대해 알아야한다.. 천천히 정리해보자.</p>
<hr />
<h3 id="1-이진-트리binary-tree">1. 이진 트리(Binary Tree)</h3>
<p><strong>이진트리(Binary Tree)</strong>는 컴퓨터가 데이터를 표현할 때, 데이터를 두 개씩 이어붙이는 것을 말한다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7bfb89f8-a5f4-4cdc-9c3f-c10de150d974/image.png" /></p>
<ul>
<li><p>각 데이터는 노드라고 말한다. 가장 최상단에 홀로 위치하는 노드를 루트(Root) 노드, 가지의 끝 최 하단에 위치하는 노드들을 리프(Leaf) 노드라고한다.</p>
</li>
<li><p>가지를 뻗어 나가듯 데이터를 뻗어 나간다고해서 트리(Tree)라고 한다.</p>
</li>
</ul>
<hr />
<h3 id="완전-이진-트리complete-binary-tree">완전 이진 트리(Complete Binary Tree)</h3>
<p>완전 이진트리란, 이진 트리의 한 종류이다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e2e9a764-832f-4f42-abd6-6672d001580a/image.png" /></p>
<p>데이터가 루트(Root) 노드를 시작으로 자식 노드가 왼쪽부터 차례대로 들어가는 구조로 되어있다.</p>
<ul>
<li><p>일반 이진트리의 경우 가지가 중간에 비어있을 수 있지만, 완전 이진트리의 경우에는 빈 공간 없이 왼쪽부터 오른쪽 순서대로 빠짐없이 채워나간다.</p>
</li>
<li><p>완전 이진트리는 두가지 조건을 충족한다.</p>
</li>
</ul>
<ol>
<li><p>마지막 레벨(level)을 제외하고 모든 노드가 채워져있어야 한다. 마지막 레벨의 노드는 반드시 다 채워질 필요는 없다.</p>
</li>
<li><p>노드는 왼쪽에서 오른쪽 방향으로 채워져야 한다.</p>
</li>
</ol>
<p>그래서 어느 노드에 오른쪽 자식이 존재한다면 왼쪽 자식도 가지고 있어야 완전이진트리로 볼 수 있다.</p>
<p>완전 이진 트리는 왼쪽 노드부터 채워야 한다는 규칙이 있는 것은 아니지만, 배열로 표현할 때 인덱스 계산의 편의성을 위해 왼쪽부터 채우는 것이 일반적이다. 이는 완전 이진 트리의 특징인 &quot;각 레벨은 왼쪽부터 채워진다&quot;는 점과 관련이 있다. </p>
<hr />
<h3 id="2-힙heap">2. 힙(Heap)</h3>
<p>힙(Heap)은 <code>최댓값</code> 혹은 <code>최솟값</code>을 빠르게 찾아내기 위해 <strong>완전 이진트리</strong>를 기반으로 하는 트리 이다.</p>
<p>완전 이진 트리의 일종으로, 여러 개의 값들 중에서 최댓값/최솟값을 빠르게 찾아내도록 만들어졌다. </p>
<p>이진 탐색 트리와 달리 중복 값이 허용된다.</p>
<pre><code class="language-c">int largest = i;           // 루트 노드
int left = 2 * i + 1;      // 왼쪽 자식
int right = 2 * i + 2;     // 오른쪽 자식

// 왼쪽 자식이 루트보다 크면
if (left &lt; n &amp;&amp; (arr[left] &gt; arr[largest]))
    largest = left;

// 오른쪽 자식이 현재까지 가장 큰 값보다 크면
if (right &lt; n &amp;&amp; (arr[right] &gt; arr[largest]))
    largest = right;

// 루트가 가장 크지 않으면 교환
if (largest != i) {
    swap(&amp;arr[i], &amp;arr[largest]);

    // 재귀적으로 힙 구조를 다시 만듦
        heapify(arr, n, largest); // 교환해준 노드가 힙 구조를 깨뜨릴 수 있으므로 다시 heapify 호출, largest가 leaf노드의 index면 함수실행 x
}</code></pre>
<hr />
<h3 id="힙-재구조화heapify">힙 재구조화(heapify)</h3>
<p>힙에서 원소의 삽입이나 삭제가 일어나면 최대 힙의 조건이 깨질 수 있다. 이 경우 다시 최대 힙의 조건을 만족하도록 노드의 위치를 바꾸는 것을 재구조화(heapify)라고 한다.</p>
<hr />
<h3 id="최대-힙-삽입-과정">최대 힙 삽입 과정</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/57f9bc7a-4876-416e-81e5-ca5572f323e2/image.png" /></p>
<p>원소를 가장 말단 노드에 삽입한 다음, 말단 노드부터 부모 노드와 비교하면서 최대 힙 조건을 만족하는지 확인한다.</p>
<p>최악의 경우 가장 말단에 삽입한 원소가 로트 노드까지 올라가게 되고, 이때의 비교 횟수는 트리의 높이만큼이다.</p>
<p>따라서 삽입의 경우 heapify의 시간 복잡도는 <code>O(logN)</code> 이다.</p>
<hr />
<h3 id="최대-힙-삭제-과정">최대 힙 삭제 과정</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2e1c9d73-53ef-4f40-a95f-30ffda1742b9/image.png" /></p>
<p>가장 큰 원소인 루트 노드를 삭제하고 나면, 가장 말단의 원소를 루트로 이동시킨다. 이후 루트 노드부터 자식 노드와 비교하여 최대 힙 조건을 만족하는지 확인한다.</p>
<p>삽입 과정과 유사하게, 최악의 경우 루트 노드에서 말단 노드까지 내려오게 되므로 비교 횟수는 트리 높이만큼이다. 따라서 삭제 과정에서 heapify의 시간 복잡도는 <code>O(logN)</code> 이다.</p>
<hr />
<h3 id="힙-만들기build-heap">힙 만들기(build-heap)</h3>
<p>build-heap은 힙이 아닌 힙으로 만드는 과정을 말한다. 이 때 heapify를 N번 진행하게 되므로 시간 복잡도는 <code>O(NlogN)</code> 이다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e0ce318a-3372-48d9-87f8-1a976fa9d087/image.png" /></p>
<p>가장 말단의 오른쪽에 있는 노드의 부모 노드부터 위에서 아래로 heapify를 진행한다.</p>
<hr />
<h3 id="힙-정렬heap-sort">힙 정렬(heap-sort)</h3>
<p>힙 정렬은 추가적인 배열을 사용하지 않고 시간 복잡도 <code>O(NlogN)</code>에 수행 가능하다. </p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f015d361-74d5-418d-a45e-6c672400aba6/image.png" /></p>
<p>내림차순 정렬 -&gt; 최대 힙 사용 &gt; <code>O(logN)</code>
오름차순 정렬 -&gt; 최소 힙 사용 &gt; <code>O(logN)</code>
 </p>
<h4 id="힙-정렬-과정">힙 정렬 과정</h4>
<ol>
<li>정렬할 N개의 원소로 최대 힙 구성 &gt; <code>O(N)</code><pre><code class="language-c">for (int i = n/2 - 1; i &gt;= 0; i--)
 heapify(arr, n, i);</code></pre>
</li>
<li>최대 힙의 루트 노드(가장 큰 원소)와 마지막 원소 위치 교환 &gt; <code>O(1)</code><pre><code class="language-c">int temp = arr[0];
arr[0] = arr[i];
arr[i] = temp;</code></pre>
</li>
<li>새 루트 노드에 대해 최대 힙 구성 &gt; <code>O(logN)</code></li>
</ol>
<pre><code class="language-c">heapify(arr, i, 0);  // i는 현재 힙 크기

void heapify(int arr[], int n, int i) {
    int largest = i;
    int left = 2*i + 1;
    int right = 2*i + 2;

    // 최대 트리 높이만큼 내려감
    if (left &lt; n &amp;&amp; arr[left] &gt; arr[largest])
        largest = left;
    if (right &lt; n &amp;&amp; arr[right] &gt; arr[largest])
        largest = right;

    if (largest != i) {
        swap(arr[i], arr[largest]);
        heapify(arr, n, largest);  // 재귀 호출
    }
}</code></pre>
<ol start="4">
<li>원소 개수만큼 2와 3을 반복 수행 &gt; <code>O(NlogN)</code></li>
</ol>
<hr />
<h3 id="4-힙-정렬heap-sort-예시-코드">4. 힙 정렬(Heap Sort) 예시 코드</h3>
<h4 id="코드">코드</h4>
<pre><code class="language-c">#define _CRT_SECURE_NO_WARNINGS
#include &lt;string.h&gt;
#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;time.h&gt;

#define SIZE 1000000 // 배열 크기

void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// 힙 구조 만들기 (max heapify)
void heapify(int arr[], int n, int i) {
    int largest = i;           // 루트 노드
    int left = 2 * i + 1;      // 왼쪽 자식
    int right = 2 * i + 2;     // 오른쪽 자식

    // 왼쪽 자식이 루트보다 크면
    if (left &lt; n &amp;&amp; arr[left] &gt; arr[largest])
        largest = left;

    // 오른쪽 자식이 현재까지 가장 큰 값보다 크면
    if (right &lt; n &amp;&amp; arr[right] &gt; arr[largest])
        largest = right;

    // 루트가 가장 크지 않으면 교환
    if (largest != i) {
        swap(&amp;arr[i], &amp;arr[largest]);
        // 재귀적으로 힙 구조를 다시 만듦
        heapify(arr, n, largest);
    }
}

// Heap Sort 함수
void heapSort(int arr[], int n) {
    // Step 1: 배열을 max heap으로 만든다
    for (int i = n / 2 - 1; i &gt;= 0; i--)
        heapify(arr, n, i);

    // Step 2: 정렬 (하나씩 꺼내서 맨 뒤로 보냄)
    for (int i = n - 1; i &gt; 0; i--) {
        swap(&amp;arr[0], &amp;arr[i]);      // 최대값(루트)을 끝으로 이동
        heapify(arr, i, 0);          // 나머지에 대해 다시 heapify
    }
}

// 출력 함수
void printArray(int arr[], int n) {
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
}

// main 함수
int main() {
    int* arr;
    int n = SIZE;

    srand(0); // 난수 시드 초기화

    // 동적 메모리로 정수 배열 할당
    arr = (int*)malloc(sizeof(int) * SIZE);
    if (arr == NULL) {
        printf(&quot;메모리 할당 실패\n&quot;);
        return 1;
    }

    // 난수로 배열 초기화
    for (int i = 0; i &lt; SIZE; i++) {
        arr[i] = rand() % SIZE + 1; // 1 ~ 1000000
    }
    printf(&quot;정렬 전 배열 :\n&quot;);
    printArray(arr, n);

    clock_t start = clock(); // 시간 측정 시작
    heapSort(arr, n);
    clock_t end = clock(); // 시간 측정 종료

    printf(&quot;\n정렬 후 배열 :\n&quot;);
    printArray(arr, n);
    printf(&quot;소요 시간 : %.2f초\n&quot;, (double)(end - start) / CLOCKS_PER_SEC);

    // 동적 메모리 해제
    free(arr);

    return 0;
}</code></pre>
<p><code>1000000개의 데이터를 정렬하는데 걸리는 시간은 약 0.24초</code></p>
<h4 id="삽입-삭제">삽입 삭제</h4>
<pre><code class="language-c">#define _CRT_SECURE_NO_WARNINGS
#include &lt;stdio.h&gt;
#include &lt;string.h&gt;
#include &lt;stdlib.h&gt;
#define SIZE 1000001

typedef struct {
    int *data;
    int len;
} heap;

void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

void push_heap(heap* h, int n) {
    h-&gt;data[++h-&gt;len] = n;
    int i = h-&gt;len;
    while (i &gt; 1 &amp;&amp; h-&gt;data[i] &gt; h-&gt;data[i/2]) {
        swap(&amp;h-&gt;data[i], &amp;h-&gt;data[i / 2]);
        i /= 2;
    }
}

int pop_heap(heap* h) {
    if (h-&gt;len == 0)
        return -1;

    int r = h-&gt;data[1];
    swap(&amp;h-&gt;data[1], &amp;h-&gt;data[h-&gt;len]);
    h-&gt;data[h-&gt;len] = 0;
    h-&gt;len--;

    int p = 1;
    int c;
    while (1) {
        c = p * 2;
        if (c + 1 &lt;= h-&gt;len &amp;&amp; h-&gt;data[c] &lt; h-&gt;data[c + 1])
            c++;
        if (c &gt; h-&gt;len || h-&gt;data[p] &gt;= h-&gt;data[c])
            break;
        swap(&amp;h-&gt;data[p], &amp;h-&gt;data[c]);
        p = c;
    }
    return r;
}

int main() {
    heap h;
    h.len = 0;
    h.data = (int*)malloc(SIZE * sizeof(int));
    if (h.data == NULL) {
        printf(&quot;메모리 할당 실패.&quot;);
        return 2;
    }

    FILE* fp = fopen(&quot;data.txt&quot;, &quot;r&quot;);
    if (fp == NULL) {
        printf(&quot;파일을 읽을 수 없음.&quot;);
        free(h.data);
        return 1;
    }

    int num;
    while (fscanf(fp, &quot;%d&quot;, &amp;num) == 1)
        push_heap(&amp;h, num);

    FILE* fout = fopen(&quot;output.txt&quot;, &quot;w&quot;);
    if (fout == NULL) {
        printf(&quot;파일을 읽을 수 없음.&quot;);
        free(h.data);
        return 1;
    }

    while(h.len &gt; 0) {
        fprintf(fout, &quot;%d &quot;, pop_heap(&amp;h));
    }

    fclose(fp);
    fclose(fout);
    free(h.data);

    return 0;
}</code></pre>
<hr />
<blockquote>
<p><em>Reference</em> : <a href="https://mjmjmj98.tistory.com/154">https://mjmjmj98.tistory.com/154</a> [👾:티스토리]</p>
</blockquote>