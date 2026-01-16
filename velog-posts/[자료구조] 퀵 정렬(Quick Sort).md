<p>피벗 기준 분할 후 재귀적으로 정렬, 평균적으로 매우 빠름(O(NlogN)) .</p>
<h2 id="퀵-정렬">퀵 정렬</h2>
<p>문제를 적은 2개의 문제로 분리하고 각각 해결한 다음, 결과를 결합해 문제를 해결하는 전략</p>
<ul>
<li>리스트의 한 요소를 <strong>피벗(Pivot)</strong>으로 선택하여, 피벗보다 작은 그룹과 피벗보다 큰 그룹으로 분리하는 작업을 반복</li>
<li>시간복잡도 : 평균 O(n log2n) / 최악 O(n^2)</li>
</ul>
<blockquote>
<p>최악의 경우를 방지하기 위한 대안
        1. 피벗을 랜덤하게 선택
        2. 세 요소를 추출하여 중앙값을 피벗으로 사용
        3. 듀얼 피벗 퀵 정렬</p>
</blockquote>
<h2 id="동작-알고리즘">동작 알고리즘</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1adb233f-71fd-48fa-8d8e-01c25fc1d2a8/image.png" /></p>
<h3 id="퀵-정렬-예제-">퀵 정렬 예제 )</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;   
#include &lt;stdlib.h&gt;
#include &lt;time.h&gt;
#include &lt;stdbool.h&gt;

#define LIST_MAX_COUNT 100000000    // 전체 리스트 크기
#define IS_PRINT_LIST_ALL 0        // 리스트 전체 출력 여부
#define ORDER_TYPE 1            // 0 : DESC, 1 : ASC



// 리스트(배열)의 두 요소를 변환하는 함수
void Swap(int* _listNum, int _iLeft, int _iRight)
{
    if (_iLeft == _iRight)
        return;

    int tmp = _listNum[_iLeft];
    _listNum[_iLeft] = _listNum[_iRight];
    _listNum[_iRight] = tmp;
}
// 리스트(배열)를 출력하는 함수
void Print_List(int* _listNum)
{
#if IS_PRINT_LIST_ALL
    for (int i = 0; i &lt; LIST_MAX_COUNT; i++)
        printf(&quot;%8d&quot;, _listNum[i]);
    printf(&quot;\n\n&quot;);
#else
    printf(&quot;%d ~ %d : &quot;, max(0, LIST_MAX_COUNT - 10), LIST_MAX_COUNT - 1);
    for (int i = max(0, LIST_MAX_COUNT - 10); i &lt; LIST_MAX_COUNT; i++)
        printf(&quot;%8d&quot;, _listNum[i]);
    printf(&quot;\n\n&quot;);
#endif
}

void quickSort(int* arr, int L, int R) {

    //피벗 인덱스 구하기
    int pivotIndex = (L + R) / 2;

    //피벗 값 구히가
    int pivot = arr[pivotIndex];

    //종료 조건 넣기
    if (L &gt;= R) return;

    //움직일 두 커서 i, j, 추후 재귀호출 할 때 L, R값을 사용해야 하기 때문
    int i = L;
    int j = R;

    while (i &lt;= j) {

        //i를 움직여 pivot 보다 큰 값을 왼쪽부터 찾기
        while (arr[i] &lt; pivot) {
            i++;
        }

        //j를 움직여 pivot 보다 작은 값을 오른쪽부터 찾기
        while (arr[j] &gt; pivot){
            j--;
        }

        //i가 j보다 크거나 같으면 while문 종료
        if (i &lt;= j) {
            Swap(arr, i++, j--);
        }

    }
    if (L &lt; j) quickSort(arr, L, j);
    if (i &lt; R) quickSort(arr, i, R);
}

void Quick_Sort(int* _listNum, int _iLeft, int _iRight)
{
    // 리스트(배열)의 크기가 2개 미만이면 패스
    int iCnt = _iRight - _iLeft + 1;
    if (iCnt &lt; 2) return;

    // 가장 왼쪽 요소를 피벗으로 사용
    // [3] [1] [4] [1] [5] [9] [2]
    // [P] [L] [ ] [ ] [ ] [ ] [R]
    int iPivot = _iLeft;
    int iL = _iLeft + 1;
    int iR = _iRight;

    // 피벗 기준 작은 값과 큰 값을 찾아 서로 변경
    // iR : 우측에서부터 변경할 값 검색 (오름차순 정렬 시 피벗보다 작은 값)
    // iL : 좌측에서부터 변경할 값 검색 (오름차순 정렬 시 피벗보다 큰 값)
    // 
    // 1 : [3] [1] [4] [1] [5] [9] [2]
    //     [P] [ ] [L] [ ] [ ] [ ] [R]
    // 2 : [3] [1] [2] [1] [5] [9] [4]
    //     [P] [ ] [L] [ ] [ ] [ ] [R]
    bool isSwap = false;
    while (iL &lt; iR)
    {
#if ORDER_TYPE
        while (iL &lt; iR &amp;&amp; _listNum[iR] &gt; _listNum[iPivot])// 왼쪽 인덱스 &lt;  오른쪽 인덱스 // 오른쪽 값 &gt;= 피벗의 값
#else
        while (iL &lt; iR &amp;&amp; _listNum[iR] &lt; _listNum[iPivot])
#endif
            iR--;

#if ORDER_TYPE
        while (iL &lt; iR &amp;&amp; _listNum[iL] &lt;= _listNum[iPivot])// 왼쪽 인덱스 &lt;  오른쪽 인덱스 // 왼쪽 값 &lt;= 피벗의 값
#else
        while (iL &lt; iR &amp;&amp; _listNum[iL] &gt;= _listNum[iPivot])
#endif
            iL++;

        if (iL &lt; iR)
            Swap(_listNum, iL, iR);
    }

    // iL 과 iR 이 만나면
    // 피벗 값을 그 경계로 옮겨 다음과 같은 형태로 변경
    // 전 : [피벗] [피벗보다 작은 그룹] [피벗보다 큰 그룹]
    // 후 : [피벗보다 작은 그룹] [피벗] [피벗보다 큰 그룹]
    //
    // 1 : [3] [1] [2] [1] [5] [9] [4]
    //     [P] [ ] [ ] [LR][ ] [ ] [ ]
    // 2 : [1] [1] [2] [3] [5] [9] [4]
    //     [P] [ ] [ ] [LR][ ] [ ] [R]
#if ORDER_TYPE
    if (_listNum[iPivot] &gt; _listNum[iL])
#else
    if (_listNum[iPivot] &lt; _listNum[iL])
#endif
    {
        Swap(_listNum, iPivot, iL);
        isSwap = true;
    }

    // [피벗보다 작은 그룹]과 [피벗보다 큰 그룹] 도 퀵 정렬
    if (iL &gt; _iLeft)
        Quick_Sort(_listNum, _iLeft, iL - 1);
    if (iL &lt; _iRight)
        Quick_Sort(_listNum, isSwap ? iL + 1 : iL, _iRight);
}

int cmpfunc(const int* a, const int* b);

int main()
{
#pragma region Init
    // 난수 초기화
    //srand((unsigned int)time(NULL));
    srand(0);

    // 리스트 생성
    int* listNum = NULL;
    listNum = calloc(LIST_MAX_COUNT, sizeof(int));
    if (NULL == listNum)
        return -1;

    clock_t start, end;
#pragma endregion

#pragma region Process Quick_Sort
    // 난수 채우기
    for (int i = 0; i &lt; LIST_MAX_COUNT; i++)
        //listNum[i] = (rand() * rand()) % 999999 + 1;
        listNum[i] = (rand() &lt;&lt; 15 | rand()) % (LIST_MAX_COUNT + 1);

    // 정렬 전 출력
    printf(&quot;정렬 전 데이터 :\n&quot;);
    Print_List(listNum);

    // 정렬
    start = clock();
    Quick_Sort(listNum, 0, LIST_MAX_COUNT - 1);
    end = clock();

    // 정렬 후 출력
    printf(&quot;Quick_Sort 정렬 후 데이터 :\n&quot;);
    Print_List(listNum);

    printf(&quot;수행 시간 : %.3lfs\n&quot;, (double)(end - start) / CLOCKS_PER_SEC);
#pragma endregion

#pragma region Process qsort
    srand(0);

    // 난수 채우기
    for (int i = 0; i &lt; LIST_MAX_COUNT; i++)
        //listNum[i] = (rand() * rand()) % 999999 + 1;
        listNum[i] = (rand() &lt;&lt; 15 | rand()) % (LIST_MAX_COUNT + 1);

    // 정렬 전 출력
    /*printf(&quot;정렬 전 데이터 :\n&quot;);
    Print_List(listNum);*/
    printf(&quot;\n&quot;);

    // 정렬
    start = clock();
    qsort(listNum, LIST_MAX_COUNT, sizeof(int), cmpfunc);
    end = clock();

    // 정렬 후 출력
    printf(&quot;qsort 정렬 후 데이터 :\n&quot;);
    Print_List(listNum);

    printf(&quot;수행 시간 : %.3lfs\n&quot;, (double)(end - start) / CLOCKS_PER_SEC);
#pragma endregion

#pragma region Process Quick_Sort2
    srand(0);

    // 난수 채우기
    for (int i = 0; i &lt; LIST_MAX_COUNT; i++)
        //listNum[i] = (rand() * rand()) % 999999 + 1;
        listNum[i] = (rand() &lt;&lt; 15 | rand()) % (LIST_MAX_COUNT + 1);

    // 정렬 전 출력
    /*printf(&quot;정렬 전 데이터 :\n&quot;);
    Print_List(listNum);*/
    printf(&quot;\n&quot;);

    // 정렬
    start = clock();
    quickSort(listNum, 0, LIST_MAX_COUNT - 1);
    end = clock();

    // 정렬 후 출력
    printf(&quot;Quick_Sort2 정렬 후 데이터 : \n&quot;);
    Print_List(listNum);

    printf(&quot;수행 시간 : %.3lfs\n&quot;, (double)(end - start) / CLOCKS_PER_SEC);
#pragma endregion


#pragma region Release
    if (NULL != listNum) // =&gt; list = NULL 로 실수했을 때 오류발생 안함, 반대로 써서 오류 유도 후 찾기 편하게 하기
    {
        free(listNum);
        listNum = NULL;//free를 하면 NULL로 비워주는게 국룰
    }
#pragma endregion
}

int cmpfunc(const int* a, const int* b)
{
#if ORDER_TYPE
    return (*a - *b);
#else
    return (*b - *a);
#endif
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1e53ac42-f56c-418b-9556-21a0972f02f7/image.png" /></p>
<blockquote>
<p>Reference : <a href="https://prosto.tistory.com/177">https://prosto.tistory.com/177</a></p>
</blockquote>