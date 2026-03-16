<h2 id="c언어에서-메모리-구조를-알아야-하는-이유">C언어에서 메모리 구조를 알아야 하는 이유</h2>
<p>C언어가 다른 언어와 구별되는 가장 큰 특징은 <strong>포인터</strong>이다.</p>
<p>C언어는 메모리 주소에 직접 접근할 수 있는 포인터 개념을 통해 아래와 같은 작업이 가능하다.</p>
<ul>
<li>메모리 주소에 직접 접근</li>
<li><code>malloc</code> / <code>free</code> 로 동적 메모리 할당 및 해제</li>
<li>하드웨어 레지스터 주소에 직접 접근 (임베디드 개발 핵심)</li>
</ul>
<p>다만 직접 메모리 주소에 접근할 수 있다는 것은 장점인 동시에, 잘못 사용하면
메모리 누수·댕글링 포인터·버퍼 오버플로우 같은 오류로 이어지는 단점이 되기도 한다.</p>
<p>C언어와 포인터는 뗄 수 없는 관계이고, 포인터는 메모리 주소를 직접 다루는 개념이기 때문에
<strong>메모리 구조를 필수적으로 알고 있어야 한다.</strong></p>
<hr />
<h2 id="메모리-구조">메모리 구조</h2>
<p>메모리 구조는 크게 4가지 영역으로 나뉜다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6a4ee144-a26b-4ea8-8493-1f8743b3e9e7/image.png" /></p>
<hr />
<h3 id="각-영역의-저장-데이터">각 영역의 저장 데이터</h3>
<p><strong>Code 영역</strong></p>
<ul>
<li>컴파일된 기계어 명령어 (함수, 제어문 등)</li>
</ul>
<p><strong>Data 영역</strong></p>
<ul>
<li>전역 변수</li>
<li><code>static</code> 변수</li>
</ul>
<p><strong>Heap 영역</strong></p>
<ul>
<li>동적 메모리 (<code>malloc</code>, <code>free</code>)</li>
</ul>
<p><strong>Stack 영역</strong></p>
<ul>
<li>지역 변수</li>
<li>함수 호출 정보 (반환 주소, 매개변수)</li>
</ul>
<hr />
<h3 id="data-영역-세부-구조">Data 영역 세부 구조</h3>
<p><code>Data 영역</code> = <code>R/O 영역</code> + <code>R/W 영역</code> + <code>BSS 영역</code></p>
<pre><code class="language-c">int a = 10;             // R/W 영역 - 초기값이 있는 전역/static 변수
int b;                  // BSS 영역 - 초기값이 없는 전역/static 변수
const char* s = &quot;hello&quot; // &quot;hello&quot; 문자열 → R/O 영역 (읽기 전용 상수)</code></pre>
<p><strong>BSS 영역이 존재하는 이유</strong></p>
<p>초기값 없는 정적 변수를 실행 전부터 메모리에 올려두면 낭비가 발생한다.
따라서 컴파일 시점에 BSS 영역에 배치하되, 실행 파일에는 변수 값을 저장하지 않고
<strong>BSS 영역의 크기만 기록</strong>한다.</p>
<p>프로그램 시작 시 startup code가 BSS 영역 전체를 <strong>0으로 초기화</strong>하여 메모리를 할당한다.</p>
<blockquote>
<p><strong>R/O 영역 주의</strong>: 읽기 전용 영역에 쓰기 접근을 시도하면 <code>Segmentation fault</code>가 발생한다.</p>
</blockquote>
<hr />
<h3 id="메모리-주소와-크기">메모리 주소와 크기</h3>
<p>32비트 아키텍처를 기준으로, 주소 버스와 데이터 버스가 각각 32개 존재한다.</p>
<ul>
<li>주소 버스: A0 ~ A31 (32개)</li>
<li>데이터 버스: D0 ~ D31 (32개)</li>
</ul>
<p>$$2^{32} = 2^{10} \times 2^{10} \times 2^{10} \times 2^{2} = 4\text{GB}$$</p>
<ul>
<li>총 약 42억 개의 주소에 접근 가능</li>
<li>메모리 주소는 <strong>상수</strong>이다. STM32 같은 보드는 제조 시 주소가 고정되어 핀에 할당된다.</li>
<li>64비트 아키텍처는 이론상 <strong>16EB(엑사바이트)</strong> 의 주소 공간을 가진다.</li>
</ul>
<hr />
<h3 id="펌웨어와-메모리">펌웨어와 메모리</h3>
<table>
<thead>
<tr>
<th>보드</th>
<th>내부 SRAM</th>
</tr>
</thead>
<tbody><tr>
<td>Arduino</td>
<td>약 32KB</td>
</tr>
<tr>
<td>STM32</td>
<td>약 512KB</td>
</tr>
</tbody></table>
<p>MCU는 <strong>NOR Flash 메모리</strong> 기반으로 바이트 단위 접근이 가능하다.
ROM에서 코드를 읽어 SRAM에 적재한 뒤 실행한다.</p>
<hr />
<h3 id="포인터와-메모리">포인터와 메모리</h3>
<pre><code class="language-c">char  c;   // 1바이트
char* p;   // 4바이트 (32비트 시스템 기준 — 주소 크기)</code></pre>
<ul>
<li>포인터는 <strong>주소값</strong> 이면서 동시에 <strong>타입 크기 정보</strong> 를 가진다.<ul>
<li><code>char*</code> → 1바이트 단위로 읽겠다는 의미</li>
</ul>
</li>
<li><code>arr[3]</code> 에서 배열명 <code>arr</code> 는 <strong>상수 포인터</strong> 이다. (재할당 불가)</li>
</ul>
<hr />
<h3 id="realloc-vs-malloc">realloc vs malloc</h3>
<p><code>malloc</code> 으로 할당한 메모리가 부족해 재할당이 필요할 경우,
새 주소로 이동하면서 <strong>주소의 연속성이 깨질 수 있다.</strong></p>
<p><code>realloc</code> 은 기존 메모리를 여유 공간으로 <strong>복사 + 확장</strong> 하여 반환하므로,
동적 메모리 크기 조절 시 <code>realloc</code> 을 사용한다.</p>
<pre><code class="language-c">ptr = realloc(ptr, new_size);  // 복사 + 확장 후 새 주소 반환</code></pre>