<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/78bc8061-5dea-4478-a699-d436a031c25d/image.png" /></p>
<h3 id="1-동시성concurrency-vs-병렬성parallelism">1. 동시성(Concurrency) vs 병렬성(Parallelism)</h3>
<ul>
<li>동시성 : 여러 작업을 논리적으로 동시에 처리하는것 처럼 보이게 하는 것</li>
<li>병렬성 : 여러 작업을 물리적으로 동시에 실행하는 것</li>
</ul>
<hr />
<h3 id="2-상세-비교">2. 상세 비교</h3>
<h4 id="동시성-concurrency---가짜-동시">동시성 (Concurrency) - &quot;가짜 동시&quot;</h4>
<ul>
<li>논리적으로 동시에 실행되는 것처럼 보이게 만드는 것.</li>
<li>실제로는 CPU 코어 1개가 아주 빠른 속도로 작업 A와 작업 B를 번갈아 가며(Context Switching) 처리합니다.</li>
<li>유휴 시간(I/O 대기 등)을 줄여서 효율성을 극대화하는 것.</li>
</ul>
<p>비유하자면, 커피숍 직원 1명이 주문도 받고, 커피도 내리고, 청소도 하는 것. (손님 눈에는 다 동시에 하는 것처럼 보임).</p>
<h4 id="병렬성-parallelism---진짜-동시">병렬성 (Parallelism) - &quot;진짜 동시&quot;</h4>
<ul>
<li>물리적으로 정확히 같은 시간에 여러 작업이 실행되는 것</li>
<li>멀티 코어(Multi-core)가 필수입니다. 코어 1은 작업 A를, 코어 2는 작업 B를 잡고 달립니다.</li>
<li>작업을 쪼개서 처리 속도를 높이는 것.</li>
</ul>
<p>비유하자면, 커피숍 직원 2명이 있어서, 한 명은 주문만 받고 다른 한 명은 커피만 내리는 것.</p>
<hr />
<h3 id="3-한눈에-보는-비교표">3. 한눈에 보는 비교표</h3>
<table>
<thead>
<tr>
<th>구분</th>
<th>동시성 (Concurrency)</th>
<th>병렬성 (Parallelism)</th>
</tr>
</thead>
<tbody><tr>
<td>핵심</td>
<td>구성 (Structure)</td>
<td>실행 (Execution)</td>
</tr>
<tr>
<td>CPU 환경</td>
<td>싱글 코어에서도 가능</td>
<td>멀티 코어 필수</td>
</tr>
<tr>
<td>동작</td>
<td>시분할 (Time-slicing), 인터리빙</td>
<td>물리적 동시 실행</td>
</tr>
<tr>
<td>느낌</td>
<td>동시에 하는 척 함</td>
<td>진짜 동시에 함</td>
</tr>
<tr>
<td>목적</td>
<td>자원 효율화, 응답성 향상</td>
<td>대용량 데이터 빠른 처리</td>
</tr>
</tbody></table>
<hr />
<h3 id="4-관계-정리-다이어그램">4. 관계 정리 (다이어그램)</h3>
<p>소프트웨어 시스템에서 두 개념은 상호 배타적이지 않습니다.</p>
<ol>
<li>동시성 O, 병렬성 X: 싱글 코어에서 멀티스레딩 </li>
<li>동시성 O, 병렬성 O: 멀티 코어에서 멀티스레딩 </li>
<li>동시성 X, 병렬성 O:  단순히 데이터를 쪼개서 GPU 등에서 연산만 수행할 때 (Bit-level Parallelism)</li>
</ol>