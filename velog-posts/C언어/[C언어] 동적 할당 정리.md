<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9f4bbadf-6c8e-45b9-828c-ca9190aabbb0/image.png" /></p>
<p><code>malloc()</code> 함수는 사용할 때 마다 계속 개념을 찾아보고 있어서 한번 정리해야겠다 싶었다.</p>
<hr />
<h3 id="동적-할당">동적 할당</h3>
<ul>
<li><p>프로그램 실행 중에 필요한 만큼 메모리 공간을 할당해주는 것을 말한다.</p>
</li>
<li><p>컴파일 타임에 크기가 결정되는 정적할당과 대비되는 개념</p>
</li>
<li><p>힙(Heap) 영역에 메모리를 할당받아 사용</p>
</li>
<li><p>동적 할당할 때는 malloc 함수를, 반환할 때는 free 함수를 사용한다.</p>
</li>
<li><p><code>malloc</code> , <code>free</code> 등의 함수를 사용할 때는 <code>&lt;stdlib.h&gt;</code> 라는 헤더 파일을 추가해줘야 한다.</p>
</li>
</ul>
<hr />
<h3 id="정적-할당-vs-동적-할당">정적 할당 vs 동적 할당</h3>
<pre><code class="language-c">// 정적 할당 : 컴파일 시 크기 고정
int arr[100]; // 항상 100개의 공간 할당

// 동적 할당 : 실행 중 필요한 만큼 할당
int* arr;
arr = (int*)malloc(sizeof(int) * n) // n개 만큼만 할당</code></pre>
<hr />
<h3 id="사용-방법">사용 방법</h3>
<ol>
<li><p>헤더 파일 포함</p>
<pre><code class="language-c">#include &lt;stdlib.h&gt; // malloc, free 사용을 위해 필수</code></pre>
</li>
<li><p>기본 사용 형식</p>
</li>
</ol>
<ul>
<li>단일 변수 할당<pre><code class="language-c">// 1단계 : 포인터 변수 선언
int* a;
</code></pre>
</li>
</ul>
<p>// 2단계 : malloc으로 메모리 할당 + 형변환
a = (int*)malloc(sizeof(int));</p>
<p>// 3단계 : 사용
*a = 10;</p>
<p>// 4단계 : 메모리 해제(필수)</p>
<pre><code>
- 배열 할당
```c
int* arr;
int n=5;

// n개의 int형 공간 할당
arr = (int*)malloc(sizeof(int) * n);

// 배열처럼 사용 가능
for(int i=0;i&lt;n;i++){
    arr[i] = i * 10;
}

// 사용 후 메모리 해제
free(arr);</code></pre><hr />
<h3 id="상세-설명">상세 설명</h3>
<ul>
<li><code>malloc()</code> 함수<pre><code class="language-c">void* malloc(unsigned int size);</code></pre>
기능 : 지정한 크기만큼 힙 영역에 메모리를 할당
매개변수 : <code>size</code> &gt; 할당 받을 바이트 수
반환값 : 성공시 할당된 메모리의 시작주소 반환, 실패시 NULL 반환
주의 : <code>void*</code> 타입으로 반환되므로 형변환 필수</li>
</ul>
<hr />
<ul>
<li><code>sizeof()</code> 함수<pre><code class="language-c">sizeof(자료형) // 해당 자료형의 크기(바이트)를 반환</code></pre>
</li>
</ul>
<p>예시)</p>
<pre><code class="language-c">sizeof(int)        // 4바이트
sizeof(char)    // 1바이트
sizeof(double)    // 8바이트
sizeof(int) * 10    // 40 바이트</code></pre>
<hr />
<ul>
<li><code>free()</code> 함수<pre><code class="language-c">void free(void* p);</code></pre>
기능 : 동적으로 할당받은 메모리를 운영체제에 반환
매개변수 : 할당받은 메모리의 주소를 가진 포인터
중요 : <code>malloc()</code> 으로 할당한 메모리는 반드시 <code>free()</code>로 해제해야 함</li>
</ul>
<hr />
<h3 id="주의-사항">주의 사항</h3>
<ol>
<li><p>메모리 누수(Memory Leak)</p>
<pre><code class="language-c">int*a = (int*)malloc(sizeof(int)*100);
// free(a); 호출하지 않을 시 메모리 누수 발생</code></pre>
</li>
<li><p>NULL 체크</p>
<pre><code class="language-c">int* a = (int*)malloc(sizeof(int) * 1000000000;
</code></pre>
</li>
</ol>
<p>// 할당 실패 가능성을 체크해야 힘
if(a == NULL){
    printf(&quot;메모리 할당 실패&quot;);
    return -1;
}</p>
<pre><code>
3. 이중 해제 방지
```c
int* a = (int*)malloc(sizeof(int));
free(a);
free(a); // 해제된 메모리를 또 해제하면 오류 발생

&gt; 안전한 방법
free(a);
a=NULL;    // 해제 후 NULL로 설정</code></pre><ol start="4">
<li>댕글링 포인터(Dangling Pointer)
```c
int* a = (int*)malloc(sizeof(int));</li>
</ol>
<p>*a = 10;
free(a);
printf(&quot;%d&quot;, *a); // 이미 해제된 메모리에 접근</p>
<pre><code>
---

#### 예제 1) 사용자 입력 크기로 배열 생성

```c
#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

int main(){
    int n;
    printf(&quot;배열 크기 입력: &quot;);
    scanf(&quot;%d&quot;, &amp;n);

    int *arr = (int*)malloc(sizeof(int)*n);

    if(arr == NULL){
        printf(&quot;메모리 할당 실패\n&quot;);
        return -1;
    }

    for(int i=0;i&lt;n;i++){
        arr[i]=i+1;
        printf(&quot;%d &quot;,arr[i]);
    }

    free(arr);

    return 0;
}</code></pre><p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e86233e3-2362-4826-9d23-1aa1a07e080d/image.png" /></p>
<hr />
<h4 id="예제-2-2차원-배열-동적-할당">예제 2) 2차원 배열 동적 할당</h4>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

int main(){
    int row = 3, col = 4;

    int **arr = (int**)malloc(sizeof(int*)*row);

    for(int i=0;i&lt;row;i++){
        arr[i] = (int*)malloc(sizeof(int) * col);
    }

    for(int i = 0;i&lt;row;i++){
        for(int j=0;j&lt;col;j++){
            arr[i][j] = i*col+j;
            printf(&quot;%2d &quot;,arr[i][j]+1);
        }
        printf(&quot;\n&quot;);
    }

    // 메모리 해제는 역순으로 
    for(int i =0;i&lt;row;i++){
        free(arr[i]);
    }
    free(arr);

    return 0;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e0e32d0b-474e-4dc0-b487-2b2f6e3c75a0/image.png" /></p>