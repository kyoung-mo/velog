<p>오늘 수업때 진도 나간 입출력 시스템에 대해 정리해보겠습니다.</p>
<hr />
<h2 id="1-스트림stream이란">1. 스트림(Stream)이란?</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/15162b44-962d-4604-bf7e-ca4d67fa46ff/image.png" /></p>
<p>스트림은 <strong>데이터의 흐름</strong>, 혹은 데이터를 전송하는 소프트웨어 모듈입니다. 흐르는 시냇물처럼 데이터가 한 방향으로 순서대로 흘러가는 개념입니다.</p>
<p>스트림의 양 끝에는 <strong>프로그램</strong>과 <strong>장치(키보드, 모니터, 파일, 네트워크 등)</strong> 가 연결되어 있으며, 입출력의 기본 단위는 <strong>1 Byte</strong>입니다.</p>
<table>
<thead>
<tr>
<th>종류</th>
<th>방향</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td>입력 스트림</td>
<td>장치 → 프로그램</td>
<td>키보드, 파일, 네트워크로부터 데이터를 읽어옴</td>
</tr>
<tr>
<td>출력 스트림</td>
<td>프로그램 → 장치</td>
<td>모니터, 파일, 네트워크로 데이터를 내보냄</td>
</tr>
</tbody></table>
<h3 id="스트림-입출력-vs-저수준-입출력">스트림 입출력 vs 저수준 입출력</h3>
<p>C++은 두 가지 입출력 방식이 존재하지만, <strong>표준은 스트림 입출력만 지원</strong>합니다.</p>
<table>
<thead>
<tr>
<th>방식</th>
<th>특징</th>
<th>사용처</th>
</tr>
</thead>
<tbody><tr>
<td>스트림 입출력</td>
<td>버퍼 경유, <code>&lt;Enter&gt;</code> 키로 확정</td>
<td>C++ 표준, 높은 호환성</td>
</tr>
<tr>
<td>저수준 입출력</td>
<td>키 입력 즉시 전달, 버퍼 없음</td>
<td>게임 등 즉각 반응 필요 시, 컴파일러마다 다름</td>
</tr>
</tbody></table>
<p>저수준 방식은 컴파일러마다 다른 라이브러리를 사용하기 때문에 이식성이 낮습니다. 표준 C++ 프로그래밍에서는 스트림 입출력만 사용한다고 보면 됩니다.</p>
<hr />
<h2 id="2-스트림-버퍼">2. 스트림 버퍼</h2>
<p>C++ 스트림은 <strong>버퍼(buffer)</strong> 를 가지고 있습니다. 데이터를 장치에 바로 전달하지 않고, 일단 버퍼에 모아두었다가 한꺼번에 처리하는 방식입니다.</p>
<h3 id="키-입력-스트림-버퍼">키 입력 스트림 버퍼</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0270c89e-a4b1-4a44-a078-85db71c66536/image.png" /></p>
<ul>
<li>키 입력 도중 <code>&lt;Backspace&gt;</code>를 누르면 버퍼에서 이전 문자를 지울 수 있습니다.</li>
<li><code>&lt;Enter&gt;</code> 키가 입력된 시점부터 프로그램이 버퍼에서 데이터를 읽기 시작합니다.</li>
<li>즉, <code>&lt;Enter&gt;</code> 이전까지는 프로그램이 아무것도 읽지 않습니다.</li>
</ul>
<h3 id="스크린-출력-스트림-버퍼">스크린 출력 스트림 버퍼</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3c42d857-8185-49df-aaf1-0dcd7a767e85/image.png" /></p>
<ul>
<li>프로그램이 출력한 데이터를 바로 화면에 보내지 않고 버퍼에 먼저 쌓습니다.</li>
<li>버퍼가 꽉 차거나, <code>\n</code>을 만나거나, 강제 출력 명령(<code>flush</code>) 시에 화면에 출력됩니다.</li>
<li>출력 장치를 반복적으로 접근하는 비효율을 줄이기 위한 구조입니다.</li>
</ul>
<hr />
<h2 id="3-c-표준-입출력-스트림-객체">3. C++ 표준 입출력 스트림 객체</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d3359b69-3d5d-4045-b78a-b652d0f4811d/image.png" /></p>
<p>C++ 프로그램이 실행되면 자동으로 생성되는 스트림 객체들이 있습니다.</p>
<table>
<thead>
<tr>
<th>객체</th>
<th>타입</th>
<th>연결 장치</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><code>cin</code></td>
<td><code>istream</code></td>
<td>키보드</td>
<td>표준 입력</td>
</tr>
<tr>
<td><code>cout</code></td>
<td><code>ostream</code></td>
<td>모니터</td>
<td>표준 출력, 버퍼 경유</td>
</tr>
<tr>
<td><code>cerr</code></td>
<td><code>ostream</code></td>
<td>모니터</td>
<td>오류 출력, <strong>버퍼 미경유</strong> (즉시 출력)</td>
</tr>
<tr>
<td><code>clog</code></td>
<td><code>ostream</code></td>
<td>모니터</td>
<td>오류 출력, 버퍼 경유</td>
</tr>
</tbody></table>
<p><code>cerr</code>와 <code>clog</code>는 둘 다 오류 메시지 출력 목적이지만, 버퍼를 거치느냐의 차이가 있습니다. 긴급한 오류 메시지는 <code>cerr</code>를 사용하는 것이 적합합니다.</p>
<hr />
<h2 id="4-ostream-멤버-함수">4. ostream 멤버 함수</h2>
<p><code>cout &lt;&lt;</code> 외에도 ostream 클래스가 제공하는 멤버 함수들이 있습니다.</p>
<pre><code class="language-cpp">ostream&amp; put(char ch)       // 문자 하나 출력
ostream&amp; write(char* str, int n)  // str 배열에서 n개 문자 출력
ostream&amp; flush()            // 버퍼 내용 강제 출력</code></pre>
<h3 id="예제--put-write-활용">예제 — put(), write() 활용</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;

int main() {
    cout.put('H');
    cout.put('i');
    cout.put(33);    // '!' (아스키 33)
    cout.put('\n');

    cout.put('C').put('+').put('+').put(' ');  // 체이닝 가능

    char str[] = &quot;I love programming&quot;;
    cout.write(str, 6);  // &quot;I love&quot; 출력 (6글자)
}</code></pre>
<p><code>put()</code>은 문자 하나를 출력하며, 반환값이 <code>ostream&amp;</code>이라 연속 호출(체이닝)이 가능합니다. <code>write()</code>는 지정한 바이트 수만큼만 출력합니다.</p>
<hr />
<h2 id="5-istream-멤버-함수">5. istream 멤버 함수</h2>
<h3 id="get--문자-단위-읽기">get() — 문자 단위 읽기</h3>
<pre><code class="language-cpp">int get()              // 문자를 int로 반환. EOF(-1)이면 종료
istream&amp; get(char&amp; ch) // 문자를 ch에 저장. EOF면 failbit 세팅</code></pre>
<pre><code class="language-cpp">// int get() 사용 — 한 줄 읽기
int ch;
while ((ch = cin.get()) != EOF) {
    cout.put(ch);
    if (ch == '\n') break;
}

// get(char&amp;) 사용 — 한 줄 읽기
char ch;
while (true) {
    cin.get(ch);
    if (cin.eof()) break;
    cout.put(ch);
    if (ch == '\n') break;
}</code></pre>
<h3 id="getchar-int--문자열-읽기">get(char*, int) — 문자열 읽기</h3>
<pre><code class="language-cpp">istream&amp; get(char* s, int n)
// 최대 n-1개 문자를 읽어 s에 저장, 끝에 '\0' 삽입
// '\n'을 만나면 읽기 중단하지만 '\n'은 스트림에 남음 ← 주의</code></pre>
<p><code>'\n'</code>이 스트림에 남아있기 때문에, 반복 입력 시 다음 <code>get()</code> 호출이 곧바로 <code>'\n'</code>을 만나 빈 문자열을 반환하는 <strong>무한 루프 문제</strong>가 발생할 수 있습니다. 이를 해결하려면 <code>'\n'</code>을 명시적으로 제거해야 합니다.</p>
<pre><code class="language-cpp">cin.get(cmd, 80);
cin.ignore(1);    // '\n' 제거
// 또는
cin.get();        // '\n' 소비</code></pre>
<h3 id="getline--한-줄-읽기-권장">getline() — 한 줄 읽기 (권장)</h3>
<pre><code class="language-cpp">istream&amp; getline(char* s, int n, char delim='\n')
// get()과 동일하지만 delim 문자를 스트림에서 제거해줌 ← get()과의 핵심 차이</code></pre>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;

int main() {
    char line[80];
    int no = 1;
    while (true) {
        cout &lt;&lt; &quot;라인&quot; &lt;&lt; no &lt;&lt; &quot;&gt;&gt; &quot;;
        cin.getline(line, 80);           // '\n' 자동 제거
        if (strcmp(line, &quot;exit&quot;) == 0) break;
        cout &lt;&lt; &quot;echo --&gt; &quot; &lt;&lt; line &lt;&lt; endl;
        no++;
    }
}</code></pre>
<p>반복 입력 시에는 <code>get()</code> 보다 <code>getline()</code>을 사용하는 것이 안전합니다. <code>'\n'</code>을 자동으로 처리해주기 때문입니다.</p>
<h3 id="ignore-gcount">ignore(), gcount()</h3>
<pre><code class="language-cpp">istream&amp; ignore(int n=1, int delim=EOF)
// 스트림에서 n개 문자 제거. delim을 만나면 그 문자까지 제거 후 리턴

int gcount()
// 가장 최근 입력 함수에서 읽은 문자 수 반환 ('\n' 포함)</code></pre>
<pre><code class="language-cpp">cin.ignore(10);       // 10개 문자 버리기
cin.ignore(10, ';');  // ';'를 만날 때까지 최대 10개 버리기

cin.getline(line, 80);
int n = cin.gcount(); // 방금 읽은 문자 수 (줄바꿈 포함)</code></pre>
<hr />
<h2 id="6-포맷-입출력">6. 포맷 입출력</h2>
<p>C++은 <code>printf</code>처럼 출력 형식을 지정할 수 있으며, 방법은 세 가지입니다.</p>
<ul>
<li><strong>포맷 플래그</strong> — <code>setf()</code>, <code>unsetf()</code> 함수로 플래그 직접 세팅</li>
<li><strong>포맷 함수</strong> — <code>width()</code>, <code>fill()</code>, <code>precision()</code> 함수 사용</li>
<li><strong>조작자</strong> — <code>&lt;&lt;</code> 연산자와 함께 사용하는 방식 (가장 편리)</li>
</ul>
<h3 id="포맷-플래그">포맷 플래그</h3>
<p>입출력 스트림에서 입출력을 저장하기 위한 플래그</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/aea9ea95-b1cb-49a2-ac01-970b6616aaab/image.png" /></p>
<pre><code class="language-cpp">cout.unsetf(ios::dec);     // 10진수 해제
cout.setf(ios::hex);       // 16진수 설정
cout &lt;&lt; 30 &lt;&lt; endl;        // 1e 출력

cout.setf(ios::showbase);  // 진수 접두사 표시 (0x, 0 등)
cout &lt;&lt; 30 &lt;&lt; endl;        // 0x1e 출력

cout.setf(ios::uppercase);
cout &lt;&lt; 30 &lt;&lt; endl;        // 0X1E 출력

cout.setf(ios::dec | ios::showpoint);
cout &lt;&lt; 23.5 &lt;&lt; endl;      // 23.5000 출력

cout.setf(ios::scientific);
cout &lt;&lt; 23.5 &lt;&lt; endl;      // 2.35000e+01 출력</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b41f9b83-5575-4073-a5ff-a9472e9a6ca1/image.png" /></p>
<h3 id="포맷-함수">포맷 함수</h3>
<pre><code class="language-cpp">int width(int minWidth)    // 출력 필드의 최소 너비 지정
char fill(char cFill)      // 빈 칸을 채울 문자 지정
int precision(int np)      // 유효 숫자 자릿수 지정 (소수점 제외)</code></pre>
<pre><code class="language-cpp">cout.width(10);
cout &lt;&lt; &quot;Hello&quot; &lt;&lt; endl;   //      Hello (우측 정렬)

cout.fill('^');
cout.width(10);
cout &lt;&lt; &quot;Hello&quot; &lt;&lt; endl;   // ^^^^^Hello

cout.precision(5);
cout &lt;&lt; 11. / 3.;          // 3.6667</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c1577a70-dfab-4431-a9d4-5c9205e4aacb/image.png" /></p>
<p><code>width()</code>는 <strong>다음 출력 하나에만 적용</strong>되고 초기화된다는 점에 주의해야 합니다. <code>fill()</code>과 <code>precision()</code>은 다시 변경하기 전까지 계속 유지됩니다.</p>
<hr />
<h2 id="7-조작자manipulator">7. 조작자(Manipulator)</h2>
<p>조작자는 <code>&lt;&lt;</code> 또는 <code>&gt;&gt;</code> 연산자와 함께 사용하는 <strong>함수</strong>입니다. 포맷 함수보다 코드가 간결해서 실제로는 조작자를 더 많이 사용합니다.</p>
<h3 id="매개변수-없는-조작자">매개변수 없는 조작자</h3>
<p>별도의 헤더 없이 <code>&lt;iostream&gt;</code>에 포함되어 있습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a75f4321-42a7-443a-9478-892a65c0f8ec/image.png" /></p>
<pre><code class="language-cpp">cout &lt;&lt; hex &lt;&lt; showbase &lt;&lt; 30 &lt;&lt; endl;   // 0x1e 출력
cout &lt;&lt; dec &lt;&lt; showpos &lt;&lt; 100 &lt;&lt; endl;   // +100 출력
cout &lt;&lt; boolalpha &lt;&lt; true &lt;&lt; endl;       // true 출력 (기본은 1)</code></pre>
<h3 id="매개변수-있는-조작자">매개변수 있는 조작자</h3>
<p><code>&lt;iomanip&gt;</code> 헤더가 필요합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1038c179-cdd5-43a0-9096-b2d8ec944420/image.png" /></p>
<pre><code class="language-cpp">#include &lt;iomanip&gt;

cout &lt;&lt; setw(10) &lt;&lt; setfill('^') &lt;&lt; &quot;Hello&quot; &lt;&lt; endl;  // ^^^^^Hello
cout &lt;&lt; setprecision(5) &lt;&lt; 11./3. &lt;&lt; endl;             // 3.6667</code></pre>
<h3 id="예제--진수-변환-표-출력">예제 — 진수 변환 표 출력</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
#include &lt;iomanip&gt;
using namespace std;

int main() {
    cout &lt;&lt; showbase;

    cout &lt;&lt; setw(8)  &lt;&lt; &quot;Number&quot;;
    cout &lt;&lt; setw(10) &lt;&lt; &quot;Octal&quot;;
    cout &lt;&lt; setw(10) &lt;&lt; &quot;Hexa&quot; &lt;&lt; endl;

    for (int i = 0; i &lt; 50; i += 5) {
        cout &lt;&lt; setw(8)  &lt;&lt; setfill('.') &lt;&lt; dec &lt;&lt; i;
        cout &lt;&lt; setw(10) &lt;&lt; setfill(' ') &lt;&lt; oct &lt;&lt; i;
        cout &lt;&lt; setw(10) &lt;&lt; setfill(' ') &lt;&lt; hex &lt;&lt; i &lt;&lt; endl;
    }
}</code></pre>
<p><code>setw()</code>는 포맷 함수의 <code>width()</code>와 마찬가지로 <strong>다음 출력 하나에만 적용</strong>되므로, 각 출력마다 반복해서 지정해야 합니다.</p>
<hr />
<h2 id="8-삽입추출-연산자-오버로딩">8. 삽입/추출 연산자 오버로딩</h2>
<p><code>&lt;&lt;</code>와 <code>&gt;&gt;</code>는 원래 C++의 <strong>비트 시프트 연산자</strong>이지만, <code>ostream</code>/<code>istream</code> 클래스에서 오버로딩되어 스트림 입출력에 사용됩니다.</p>
<pre><code class="language-cpp">class ostream {
public:
    ostream&amp; operator&lt;&lt;(int n);
    ostream&amp; operator&lt;&lt;(char c);
    ostream&amp; operator&lt;&lt;(const char* s);
    // ...
};</code></pre>
<p>이 구조 덕분에 사용자 정의 클래스도 <code>&lt;&lt;</code>, <code>&gt;&gt;</code>를 오버로딩하면 <code>cout</code>, <code>cin</code>과 자연스럽게 연동할 수 있습니다.</p>
<h3 id="삽입-연산자--오버로딩">삽입 연산자 <code>&lt;&lt;</code> 오버로딩</h3>
<p><code>private</code> 멤버에 접근해야 하므로 <code>friend</code> 함수로 선언합니다. 반환값을 <code>ostream&amp;</code>로 해야 <code>cout &lt;&lt; a &lt;&lt; b</code>처럼 <strong>체이닝</strong>이 가능합니다.</p>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;

class Point {
    int x, y;
public:
    Point(int x=0, int y=0) { this-&gt;x = x; this-&gt;y = y; }
    friend ostream&amp; operator&lt;&lt;(ostream&amp; stream, Point a);
};

ostream&amp; operator&lt;&lt;(ostream&amp; stream, Point a) {
    stream &lt;&lt; &quot;(&quot; &lt;&lt; a.x &lt;&lt; &quot;,&quot; &lt;&lt; a.y &lt;&lt; &quot;)&quot;;
    return stream;  // 체이닝을 위해 stream 반환
}

int main() {
    Point p(3, 4);
    cout &lt;&lt; p &lt;&lt; endl;           // (3,4)

    Point q(1, 100), r(2, 200);
    cout &lt;&lt; q &lt;&lt; r &lt;&lt; endl;      // (1,100)(2,200)
}</code></pre>
<h3 id="추출-연산자--오버로딩">추출 연산자 <code>&gt;&gt;</code> 오버로딩</h3>
<p>입력 대상 객체를 수정해야 하므로 두 번째 매개변수를 <strong>참조(<code>&amp;</code>)</strong> 로 받아야 합니다.</p>
<pre><code class="language-cpp">istream&amp; operator&gt;&gt;(istream&amp; ins, Point&amp; a) {
    cout &lt;&lt; &quot;x 좌표&gt;&gt; &quot;;
    ins &gt;&gt; a.x;
    cout &lt;&lt; &quot;y 좌표&gt;&gt; &quot;;
    ins &gt;&gt; a.y;
    return ins;
}</code></pre>
<pre><code class="language-cpp">// &lt;&lt; 와 &gt;&gt; 를 모두 오버로딩한 Point 클래스 예제
#include &lt;iostream&gt;
using namespace std;

class Point {
    int x, y;
public:
    Point(int x=0, int y=0) { this-&gt;x = x; this-&gt;y = y; }
    friend istream&amp; operator&gt;&gt;(istream&amp; ins, Point&amp; a);
    friend ostream&amp; operator&lt;&lt;(ostream&amp; stream, Point a);
};

istream&amp; operator&gt;&gt;(istream&amp; ins, Point&amp; a) {
    cout &lt;&lt; &quot;x 좌표&gt;&gt; &quot;; ins &gt;&gt; a.x;
    cout &lt;&lt; &quot;y 좌표&gt;&gt; &quot;; ins &gt;&gt; a.y;
    return ins;
}

ostream&amp; operator&lt;&lt;(ostream&amp; stream, Point a) {
    stream &lt;&lt; &quot;(&quot; &lt;&lt; a.x &lt;&lt; &quot;,&quot; &lt;&lt; a.y &lt;&lt; &quot;)&quot;;
    return stream;
}

int main() {
    Point p;
    cin &gt;&gt; p;   // &gt;&gt; 오버로딩 호출
    cout &lt;&lt; p;  // &lt;&lt; 오버로딩 호출
}</code></pre>
<hr />
<h2 id="9-사용자-정의-조작자">9. 사용자 정의 조작자</h2>
<p>개발자가 직접 조작자를 만들 수도 있습니다. 매개변수 없는 조작자의 함수 원형은 아래와 같습니다.</p>
<pre><code class="language-cpp">ostream&amp; 조작자이름(ostream&amp; outs)  // 출력 스트림용
istream&amp; 조작자이름(istream&amp; ins)   // 입력 스트림용</code></pre>
<h3 id="예제--출력-조작자">예제 — 출력 조작자</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
using namespace std;

ostream&amp; fivestar(ostream&amp; outs) {
    return outs &lt;&lt; &quot;*****&quot;;
}

ostream&amp; rightarrow(ostream&amp; outs) {
    return outs &lt;&lt; &quot;----&gt;&quot;;
}

int main() {
    cout &lt;&lt; &quot;C&quot; &lt;&lt; rightarrow &lt;&lt; &quot;C++&quot; &lt;&lt; rightarrow &lt;&lt; &quot;Java&quot; &lt;&lt; endl;
    cout &lt;&lt; &quot;Visual&quot; &lt;&lt; fivestar &lt;&lt; &quot;C++&quot; &lt;&lt; endl;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/689cf3c3-4078-4b0a-baa5-44bd8a32331f/image.png" /></p>
<h3 id="예제--입력-조작자">예제 — 입력 조작자</h3>
<pre><code class="language-cpp">#include &lt;iostream&gt;
#include &lt;string&gt;
using namespace std;

istream&amp; question(istream&amp; ins) {
    cout &lt;&lt; &quot;거울아 거울아 누가 제일 이쁘니? &quot;;
    return ins;
}

int main() {
    string answer;
    cin &gt;&gt; question &gt;&gt; answer;
    cout &lt;&lt; &quot;세상에서 제일 이쁜 사람은 &quot; &lt;&lt; answer &lt;&lt; &quot;입니다.&quot; &lt;&lt; endl;
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/564c37b2-ac62-45f0-a025-0b3fc1647647/image.png" /></p>
<p>조작자 함수가 <code>ostream&amp;</code> 또는 <code>istream&amp;</code>을 받고 같은 타입을 반환하기 때문에, <code>&lt;&lt;</code> / <code>&gt;&gt;</code> 연산자 체인 중간에 자연스럽게 끼워 넣을 수 있습니다.</p>
<hr />
<h2 id="10-정리">10. 정리</h2>
<table>
<thead>
<tr>
<th>분류</th>
<th>함수/기능</th>
<th>핵심 내용</th>
</tr>
</thead>
<tbody><tr>
<td>ostream</td>
<td><code>put()</code>, <code>write()</code>, <code>flush()</code></td>
<td>문자/문자열 단위 출력, 강제 플러시</td>
</tr>
<tr>
<td>istream</td>
<td><code>get()</code>, <code>getline()</code></td>
<td><code>get()</code>은 <code>\n</code> 스트림에 남김, <code>getline()</code>은 제거</td>
</tr>
<tr>
<td>istream</td>
<td><code>ignore()</code>, <code>gcount()</code></td>
<td>버퍼 문자 제거, 읽은 문자 수 확인</td>
</tr>
<tr>
<td>포맷 플래그</td>
<td><code>setf()</code>, <code>unsetf()</code></td>
<td><code>ios::hex</code>, <code>ios::showbase</code> 등</td>
</tr>
<tr>
<td>포맷 함수</td>
<td><code>width()</code>, <code>fill()</code>, <code>precision()</code></td>
<td><code>width()</code>는 한 번만 적용됨 주의</td>
</tr>
<tr>
<td>조작자</td>
<td><code>hex</code>, <code>setw()</code>, <code>setfill()</code> 등</td>
<td><code>&lt;iomanip&gt;</code> 필요, 가장 간결한 방식</td>
</tr>
<tr>
<td><code>&lt;&lt;</code> 오버로딩</td>
<td><code>friend ostream&amp; operator&lt;&lt;</code></td>
<td>반환값 <code>ostream&amp;</code>로 체이닝 지원</td>
</tr>
<tr>
<td><code>&gt;&gt;</code> 오버로딩</td>
<td><code>friend istream&amp; operator&gt;&gt;</code></td>
<td>두 번째 인자 반드시 참조(<code>&amp;</code>)</td>
</tr>
<tr>
<td>사용자 조작자</td>
<td><code>ostream&amp; func(ostream&amp;)</code></td>
<td><code>&lt;&lt;</code> 체인 중간에 삽입 가능</td>
</tr>
</tbody></table>
<p><code>get()</code>과 <code>getline()</code>의 <code>'\n'</code> 처리 차이, <code>width()</code>가 한 번만 적용된다는 점, 연산자 오버로딩 시 <code>friend</code>와 참조 반환이 필요한 이유를 중심으로 이해해두면 좋을 것 같습니다.</p>