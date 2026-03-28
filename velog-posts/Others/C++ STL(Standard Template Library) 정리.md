<p>저번 글 : <a href="https://velog.io/@mommers/C-%ED%85%9C%ED%94%8C%EB%A6%BFTemplate%EA%B3%BC-%EC%A0%9C%EB%84%A4%EB%A6%AD-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D">C++ 템플릿(Template)과 제네릭 프로그래밍</a></p>
<p>이어서 STL에 대해 정리해보겠습니다. 알고리즘 등 코딩테스트에서 자주 사용되는 부분으로 알고있어서 잘 알아두려 노력중입니다.</p>
<h2 id="목차">목차</h2>
<ol>
<li><a href="https://api.velog.io/rss/@mommers#1-stl%EC%9D%B4%EB%9E%80">STL이란?</a></li>
<li><a href="https://api.velog.io/rss/@mommers#2-stl%EC%9D%98-%EA%B5%AC%EC%84%B1%EC%9A%94%EC%86%8C">STL의 구성요소</a></li>
<li><a href="https://api.velog.io/rss/@mommers#3-vector-%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88">vector 컨테이너</a></li>
<li><a href="https://api.velog.io/rss/@mommers#4-iterator-%EB%B0%98%EB%B3%B5%EC%9E%90">iterator (반복자)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#5-map-%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88">map 컨테이너</a></li>
<li><a href="https://api.velog.io/rss/@mommers#6-stl-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98">STL 알고리즘</a></li>
<li><a href="https://api.velog.io/rss/@mommers#7-%EC%A0%95%EB%A6%AC">정리</a></li>
</ol>
<hr />
<h2 id="1-stl이란">1. STL이란?</h2>
<p><strong>STL(Standard Template Library)</strong> 은 C++ 표준 라이브러리의 일부로, 다양한 제네릭 클래스와 제네릭 함수를 제공합니다. 이전 글에서 살펴본 <strong>템플릿</strong> 개념이 실제로 집대성된 결과물이 바로 STL이라고 볼 수 있습니다.</p>
<p>개발자는 자료구조나 알고리즘을 직접 구현하지 않고, STL이 제공하는 검증된 도구들을 가져다 사용함으로써 생산성을 높일 수 있습니다.</p>
<hr />
<h2 id="2-stl의-구성요소">2. STL의 구성요소</h2>
<p>STL은 크게 세 가지 요소로 구성됩니다.</p>
<h3 id="컨테이너-container">컨테이너 (Container)</h3>
<p>데이터를 담아두는 자료구조를 클래스로 구현한 것입니다.</p>
<table>
<thead>
<tr>
<th>컨테이너</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><code>vector</code></td>
<td>가변 크기의 배열</td>
</tr>
<tr>
<td><code>deque</code></td>
<td>앞뒤 모두 삽입 가능한 큐</td>
</tr>
<tr>
<td><code>list</code></td>
<td>빠른 삽입/삭제가 가능한 리스트</td>
</tr>
<tr>
<td><code>set</code></td>
<td>정렬된 순서로 저장, 중복 없음</td>
</tr>
<tr>
<td><code>map</code></td>
<td>(key, value) 쌍을 저장하는 맵</td>
</tr>
<tr>
<td><code>stack</code></td>
<td>스택 자료구조</td>
</tr>
<tr>
<td><code>queue</code></td>
<td>큐 자료구조</td>
</tr>
</tbody></table>
<h3 id="iterator-반복자">iterator (반복자)</h3>
<p>컨테이너의 원소를 가리키는 포인터로, 원소를 순회할 때 사용합니다.</p>
<table>
<thead>
<tr>
<th>종류</th>
<th>방향</th>
<th>읽기/쓰기</th>
</tr>
</thead>
<tbody><tr>
<td><code>iterator</code></td>
<td>전진</td>
<td>R/W</td>
</tr>
<tr>
<td><code>const_iterator</code></td>
<td>전진</td>
<td>R</td>
</tr>
<tr>
<td><code>reverse_iterator</code></td>
<td>후진</td>
<td>R/W</td>
</tr>
<tr>
<td><code>const_reverse_iterator</code></td>
<td>후진</td>
<td>R</td>
</tr>
</tbody></table>
<h3 id="알고리즘-algorithm">알고리즘 (Algorithm)</h3>
<p>컨테이너 원소에 대한 복사, 검색, 삭제, 정렬 등을 수행하는 <strong>템플릿 함수</strong>들입니다. 컨테이너의 멤버 함수가 아닌 <strong>전역 함수</strong>라는 점이 특징입니다.</p>
<pre><code>copy, merge, random, rotate,
equal, min,  remove, search,
find, move,  replace, sort,
max, partition, reverse, swap</code></pre><h3 id="헤더-파일-및-네임스페이스">헤더 파일 및 네임스페이스</h3>
<pre><code class="language-cpp">#include &lt;vector&gt;      // vector 사용
#include &lt;list&gt;        // list 사용
#include &lt;map&gt;         // map 사용
#include &lt;algorithm&gt;   // 알고리즘 함수 사용 (함수 종류에 관계없이 하나면 됨)

using namespace std;   // STL은 std 네임스페이스에 선언되어 있음</code></pre>
<hr />
<h2 id="3-vector-컨테이너">3. vector 컨테이너</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6fb0bcb6-e0e1-465a-b7b6-47df4c6f1456/image.png" />
<code>vector</code>는 <strong>가변 길이 배열</strong>을 구현한 제네릭 클래스입니다. 일반 배열과 달리 크기를 미리 정하지 않아도 되며, 원소를 추가할 때마다 내부적으로 크기를 자동으로 늘려줍니다.</p>
<p>인덱스를 통한 임의 접근(<code>v[i]</code>, <code>v.at(i)</code>)이 가능하다는 점도 배열과 유사합니다.</p>
<h3 id="주요-멤버-함수">주요 멤버 함수</h3>
<table>
<thead>
<tr>
<th>멤버 함수</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><code>push_back(val)</code></td>
<td>벡터 끝에 원소 추가</td>
</tr>
<tr>
<td><code>pop_back()</code></td>
<td>벡터 끝 원소 삭제</td>
</tr>
<tr>
<td><code>at(idx)</code></td>
<td><code>idx</code> 번째 원소 반환 (범위 검사 있음)</td>
</tr>
<tr>
<td><code>operator[idx]</code></td>
<td><code>idx</code> 번째 원소 반환 (범위 검사 없음)</td>
</tr>
<tr>
<td><code>size()</code></td>
<td>현재 원소 개수 반환</td>
</tr>
<tr>
<td><code>begin()</code></td>
<td>첫 번째 원소를 가리키는 iterator 반환</td>
</tr>
<tr>
<td><code>end()</code></td>
<td>마지막 원소 다음을 가리키는 iterator 반환</td>
</tr>
</tbody></table>
<h3 id="예제-1--기본-vector-활용">예제 1 — 기본 vector 활용</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
#include &lt;vector&gt;
using namespace std;

int main() {
    vector&lt;int&gt; v;

    v.push_back(1);
    v.push_back(2);
    v.push_back(3);

    for (int i = 0; i &lt; v.size(); i++) cout &lt;&lt; v[i] &lt;&lt; &quot; &quot;;
    cout &lt;&lt; endl;

    v[0] = 10;        // 인덱스 연산자로 수정
    int n = v[2];     // 값 읽기
    v.at(2) = 5;      // at()으로 수정

    for (int i = 0; i &lt; v.size(); i++) cout &lt;&lt; v[i] &lt;&lt; &quot; &quot;;
    cout &lt;&lt; endl;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b5b4bfc7-3a7b-4813-ac3d-2f23d7e478fe/image.png" /></p>
<p><code>[]</code> 연산자와 <code>at()</code> 멤버 함수 모두 원소 접근 및 수정에 사용할 수 있습니다. 차이점은 <code>at()</code>은 인덱스 범위를 검사하여 예외를 던지지만, <code>[]</code>는 범위 검사를 하지 않습니다.</p>
<hr />
<h3 id="예제-2--문자열-벡터-활용">예제 2 — 문자열 벡터 활용</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;vector&gt;
using namespace std;

int main() {
    vector&lt;string&gt; sv;
    string name;

    cout &lt;&lt; &quot;이름을 5개 입력 : &quot; &lt;&lt; endl;
    for (int i = 0; i &lt; 5; i++) {
        cout &lt;&lt; i + 1 &lt;&lt; &quot; &gt;&gt; &quot;;
        getline(cin, name);
        sv.push_back(name);
    }

    name = sv.at(0);
    for (int i = 1; i &lt; sv.size(); i++) {
        if (name &lt; sv[i]) name = sv[i];
    }
    cout &lt;&lt; &quot;사전에서 가장 뒤에 나오는 이름은 &quot; &lt;&lt; name &lt;&lt; endl;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5f29b95b-bccb-4380-8a1e-d58ae30d25c4/image.png" /></p>
<p><code>vector&lt;string&gt;</code> 처럼 문자열도 제네릭 타입으로 지정하여 저장할 수 있습니다. <code>string</code> 타입은 <code>&lt;</code> 연산자로 사전 순 비교가 가능하기 때문에 위와 같은 방식으로 최댓값을 찾을 수 있었습니다.</p>
<hr />
<h2 id="4-iterator-반복자">4. iterator (반복자)</h2>
<p>iterator는 <strong>컨테이너의 원소를 가리키는 포인터</strong>입니다. 포인터처럼 <code>*</code>로 역참조하고, <code>++</code>로 다음 원소로 이동합니다.</p>
<h3 id="iterator-변수-선언">iterator 변수 선언</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f8d114e5-1558-4f67-bdb5-414157919821/image.png" /></p>
<pre><code class="language-cpp">vector&lt;int&gt;::iterator it;  // int형 벡터의 원소를 가리키는 iterator 선언</code></pre>
<h3 id="벡터-순회-패턴">벡터 순회 패턴</h3>
<pre><code class="language-cpp">for (it = v.begin(); it != v.end(); it++) {
    cout &lt;&lt; *it &lt;&lt; ' ';
}</code></pre>
<p><code>v.begin()</code>은 첫 번째 원소를, <code>v.end()</code>는 마지막 원소의 <strong>다음</strong>을 가리킵니다. 따라서 <code>it != v.end()</code> 조건으로 순회를 제어합니다.</p>
<h3 id="예제-3--iterator로-모든-원소에-2-곱하기">예제 3 — iterator로 모든 원소에 2 곱하기</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
#include &lt;vector&gt;
using namespace std;

int main() {
    vector&lt;int&gt; v;
    v.push_back(1);
    v.push_back(2);
    v.push_back(3);

    vector&lt;int&gt;::iterator it;

    for (it = v.begin(); it != v.end(); it++) {
        int n = *it;
        n = n * 2;
        *it = n;  // 역참조로 원소 값 수정
    }

    for (it = v.begin(); it != v.end(); it++) {
        cout &lt;&lt; *it &lt;&lt; ' ';
    }
    cout &lt;&lt; endl;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/995f1801-f56f-4871-8782-2e877638f76a/image.png" /></p>
<p><code>*it</code>로 원소의 값을 읽을 수도 있고, <code>*it = 값</code> 형태로 수정도 가능합니다. 포인터 문법과 동일하게 동작한다는 점이 직관적입니다.</p>
<hr />
<h2 id="5-map-컨테이너">5. map 컨테이너</h2>
<p><code>map</code>은 <strong>(key, value) 쌍</strong>을 원소로 저장하는 컨테이너입니다. 동일한 키를 가진 원소는 중복 저장되지 않으며, 키를 기준으로 자동 정렬됩니다.</p>
<p>사전, 캐시, 설정 파일 파싱 등 다양한 상황에서 활용됩니다.</p>
<h3 id="주요-멤버-함수-1">주요 멤버 함수</h3>
<table>
<thead>
<tr>
<th>멤버 함수</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><code>insert(make_pair(key, val))</code></td>
<td>(key, value) 쌍 삽입</td>
</tr>
<tr>
<td><code>operator[key]</code></td>
<td>key에 해당하는 value 접근 및 수정</td>
</tr>
<tr>
<td><code>at(key)</code></td>
<td>key에 해당하는 value 반환</td>
</tr>
<tr>
<td><code>find(key)</code></td>
<td>key를 가진 원소의 iterator 반환. 없으면 <code>end()</code> 반환</td>
</tr>
<tr>
<td><code>erase(key)</code></td>
<td>key에 해당하는 원소 삭제. 삭제된 개수 반환</td>
</tr>
<tr>
<td><code>size()</code></td>
<td>저장된 원소 개수 반환</td>
</tr>
<tr>
<td><code>begin()</code> / <code>end()</code></td>
<td>순회용 iterator 반환</td>
</tr>
</tbody></table>
<h2 id="map-활용---영한-사전-사례">map 활용 - 영한 사전 사례</h2>
<p>map 컨테이너 생성 및 원소 삽입</p>
<pre><code class="language-cpp">map &lt;string, string&gt; dic; 
// 키는 영어 단어, 값은 한글 단어</code></pre>
<p>map 컨테이너 생성 및 원소 삽입</p>
<pre><code class="language-cpp">dic.insert(make_pair(&quot;love&quot;, &quot;사랑&quot;)); // (&quot;love&quot;, &quot;사랑&quot;) 저장
dic[&quot;love&quot;] = &quot;사랑&quot;; // (&quot;love&quot;, &quot;사랑&quot;) 저장</code></pre>
<p>키로 값 검색 : [] 연산자나 at() 멤버 함수 활용</p>
<pre><code class="language-cpp">string kor = dic[&quot;love&quot;]; // kor은 사랑
string kore = dic.at(&quot;love&quot;); // kor은 사랑</code></pre>
<p>키 원소가 맵에 있는지 검사</p>
<pre><code class="language-cpp">if(dic.find(eng) == dic.end())
// eng의 키를 찾을 수 없다면 조건문은 true</code></pre>
<p>원소 삭제 - 반드시 키를 이용하여 삭제</p>
<pre><code class="language-cpp">dic.erase(&quot;love&quot;);
// 키가 &quot;love&quot;인 원소 삭제. 삭제된 원소 개수 1 리턴.
// 키가 &quot;love&quot;인 원소가 없으면 0 리턴</code></pre>
<h3 id="예제-4--영한-사전-만들기">예제 4 — 영한 사전 만들기</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;map&gt;
using namespace std;

int main() {
    map&lt;string, string&gt; dic;

    dic.insert(make_pair(&quot;love&quot;, &quot;사랑&quot;));
    dic.insert(make_pair(&quot;apple&quot;, &quot;사과&quot;));
    dic[&quot;cherry&quot;] = &quot;체리&quot;;  // [] 연산자로도 삽입 가능

    cout &lt;&lt; &quot;저장된 단어 개수 &quot; &lt;&lt; dic.size() &lt;&lt; endl;

    string eng;
    while (true) {
        cout &lt;&lt; &quot;찾고 싶은 단어 &gt;&gt; &quot;;
        getline(cin, eng);
        if (eng == &quot;exit&quot;) break;
        if (dic.find(eng) == dic.end()) cout &lt;&lt; &quot;없음&quot; &lt;&lt; endl;
        else cout &lt;&lt; dic[eng] &lt;&lt; endl;
    }
    cout &lt;&lt; &quot;종료합니다..&quot; &lt;&lt; endl;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/dd03564a-e1b7-4a01-81bd-cf4ee9b60fe9/image.png" /></p>
<p><code>find(key)</code>의 반환값이 <code>end()</code>와 같다면 키가 존재하지 않는다는 의미입니다. 이 패턴은 map을 사용할 때 매우 자주 등장하는 관용 표현입니다.</p>
<hr />
<h3 id="예제-5--상품-재고-관리-map--사용자-클래스">예제 5 — 상품 재고 관리 (map + 사용자 클래스)</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;map&gt;
using namespace std;

class Item {
public:
    int price;
    int count;
    Item(int price = 0, int count = 0) {
        this-&gt;price = price;
        this-&gt;count = count;
    }
};

int main() {
    map&lt;string, Item&gt; stock;
    string name;
    int price = 0, count = 0, removedCount = 0;

    while (true) {
        cout &lt;&lt; &quot;상품 입고:1, 검색:2, 삭제:3, 종료:4 &gt;&gt; &quot;;
        int menu;
        cin &gt;&gt; menu;
        switch (menu) {
        case 1:
            cout &lt;&lt; &quot;상품명, 가격, 개수 입력&gt;&gt; &quot;;
            cin &gt;&gt; name &gt;&gt; price &gt;&gt; count;
            stock.insert(make_pair(name, Item(price, count)));
            break;
        case 2:
            cout &lt;&lt; &quot;상품명 입력&gt;&gt; &quot;;
            cin &gt;&gt; name;
            if (stock.find(name) == stock.end())
                cout &lt;&lt; name &lt;&lt; &quot; 없음&quot; &lt;&lt; endl;
            else {
                Item item = stock[name];
                cout &lt;&lt; &quot;가격 &quot; &lt;&lt; item.price &lt;&lt; &quot;, 재고 &quot; &lt;&lt; item.count &lt;&lt; &quot;개&quot; &lt;&lt; endl;
            }
            break;
        case 3:
            cout &lt;&lt; &quot;상품명 입력&gt;&gt; &quot;;
            cin &gt;&gt; name;
            removedCount = stock.erase(name);
            if (removedCount == 0) cout &lt;&lt; name &lt;&lt; &quot; 없음&quot; &lt;&lt; endl;
            else cout &lt;&lt; name &lt;&lt; &quot; 삭제 완료&quot; &lt;&lt; endl;
            break;
        case 4:
            cout &lt;&lt; &quot;종료합니다..&quot; &lt;&lt; endl;
            return 0;
        }
    }
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ae40b210-c13b-43f5-bea9-f2af789809f5/image.png" /></p>
<p>value 타입으로 기본 타입 뿐만 아니라 사용자 정의 클래스도 사용할 수 있습니다. map은 내부적으로 키를 기준으로 정렬된 상태를 유지하기 때문에, 원소 삽입 순서와 관계없이 항상 키 순서로 저장됩니다.</p>
<hr />
<h3 id="예제-6--iterator로-map의-모든-원소-출력">예제 6 — iterator로 map의 모든 원소 출력</h3>
<p>map의 원소는 <code>it-&gt;first</code>(키), <code>it-&gt;second</code>(값) 형태로 접근합니다.</p>
<pre><code class="language-cpp">#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;map&gt;
using namespace std;

void printMap(map&lt;string, int&gt;&amp; m) {
    map&lt;string, int&gt;::iterator it;
    for (it = m.begin(); it != m.end(); it++) {
        string menu = it-&gt;first;
        int price = it-&gt;second;
        cout &lt;&lt; menu &lt;&lt; &quot;: &quot; &lt;&lt; price &lt;&lt; &quot;원&quot; &lt;&lt; endl;
    }
}

int main() {
    map&lt;string, int&gt; priceMap;
    priceMap[&quot;붕어빵&quot;] = 2000;
    priceMap[&quot;잉어빵&quot;] = 2500;
    priceMap.insert(make_pair(&quot;국화빵&quot;, 3000));
    printMap(priceMap);
    cout &lt;&lt; endl;

    priceMap.erase(&quot;붕어빵&quot;);
    printMap(priceMap);
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/327cf85a-e77b-4309-831c-917878348bfb/image.png" /></p>
<p>vector와 마찬가지로 <code>begin()</code>에서 <code>end()</code>까지 iterator로 순회할 수 있습니다. pair 구조체의 <code>first</code>, <code>second</code> 멤버로 키와 값에 각각 접근하는 방식이 map 순회의 핵심 패턴입니다.</p>
<hr />
<h2 id="6-stl-알고리즘">6. STL 알고리즘</h2>
<p>알고리즘 함수는 <code>&lt;algorithm&gt;</code> 헤더를 포함하면 사용할 수 있으며, 컨테이너의 멤버가 아닌 <strong>전역 템플릿 함수</strong>입니다. iterator와 함께 동작하며, 어떤 컨테이너든 동일한 인터페이스로 사용할 수 있습니다.</p>
<h3 id="sort-함수">sort() 함수</h3>
<p>가장 자주 사용하는 알고리즘 중 하나로, 정렬 범위를 iterator로 지정합니다.</p>
<pre><code class="language-cpp">sort(v.begin(), v.end());          // 벡터 전체 정렬
sort(v.begin(), v.begin() + 3);    // 처음 3개 원소만 정렬
sort(v.begin() + 2, v.begin() + 5); // 3번째~5번째 원소 정렬</code></pre>
<h3 id="예제-7--sort로-벡터-정렬">예제 7 — sort()로 벡터 정렬</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
#include &lt;vector&gt;
#include &lt;algorithm&gt;
using namespace std;

int main() {
    vector&lt;int&gt; v;

    cout &lt;&lt; &quot;5개의 정수를 입력하세요 &gt;&gt; &quot;;
    for (int i = 0; i &lt; 5; i++) {
        int n;
        cin &gt;&gt; n;
        v.push_back(n);
    }

    sort(v.begin(), v.end());  // 오름차순 정렬

    vector&lt;int&gt;::iterator it;
    for (it = v.begin(); it != v.end(); it++) {
        cout &lt;&lt; *it &lt;&lt; ' ';
    }
    cout &lt;&lt; endl;
}</code></pre>
<p><img alt="업로드중.." src="blob:https://velog.io/267cbcf8-7621-4f86-aadb-2cc69fbdb566" /></p>
<p><code>sort()</code>는 기본적으로 오름차순 정렬을 수행합니다. 세 번째 인자로 비교 함수(또는 람다)를 전달하면 내림차순이나 사용자 정의 정렬 기준도 적용할 수 있습니다.</p>
<hr />
<h2 id="7-정리">7. 정리</h2>
<table>
<thead>
<tr>
<th>구성요소</th>
<th>역할</th>
<th>대표 헤더</th>
</tr>
</thead>
<tbody><tr>
<td>컨테이너</td>
<td>데이터 저장 자료구조</td>
<td><code>&lt;vector&gt;</code>, <code>&lt;map&gt;</code>, <code>&lt;list&gt;</code> 등</td>
</tr>
<tr>
<td>iterator</td>
<td>컨테이너 원소 순회용 포인터</td>
<td>각 컨테이너 헤더에 포함</td>
</tr>
<tr>
<td>알고리즘</td>
<td>정렬, 검색, 복사 등 범용 함수</td>
<td><code>&lt;algorithm&gt;</code></td>
</tr>
</tbody></table>
<table>
<thead>
<tr>
<th>패턴</th>
<th>코드</th>
</tr>
</thead>
<tbody><tr>
<td>벡터 순회</td>
<td><code>for (it = v.begin(); it != v.end(); it++)</code></td>
</tr>
<tr>
<td>map 검색</td>
<td><code>if (m.find(key) == m.end())</code> → 없음</td>
</tr>
<tr>
<td>map 원소 접근</td>
<td><code>it-&gt;first</code> (키), <code>it-&gt;second</code> (값)</td>
</tr>
<tr>
<td>sort</td>
<td><code>sort(v.begin(), v.end())</code></td>
</tr>
</tbody></table>
<p>STL은 C++을 실제 프로젝트에서 사용할 때 반드시 익혀야 하는 핵심 라이브러리입니다. 자료구조를 직접 구현하지 않아도 검증된 컨테이너를 바로 활용할 수 있다는 점에서 생산성 면에서 큰 이점이 있습니다. 특히 임베디드 환경을 제외한 일반 C++ 애플리케이션에서는 거의 필수적으로 등장하는 개념이므로 확실하게 이해해두는 것이 좋을 것 같습니다.</p>