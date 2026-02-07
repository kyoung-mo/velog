<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8e123a76-8c9b-4be4-85e1-72ffd7072b6f/image.png" /></p>
<p>썸네일 출처: <a href="https://bezzang2.tistory.com/127">https://bezzang2.tistory.com/127</a>
<a href="https://velog.io/@mommers/TCPIP-%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C-%EC%A0%95%EB%A6%AC">TCP IP 1편</a> 이어서 2편에 대해 정리해보겠습니다.</p>
<hr />
<h2 id="📚-목차">📚 목차</h2>
<ul>
<li><a href="https://api.velog.io/rss/@mommers#8-%ED%8F%AC%ED%8A%B8-port">8. 포트 (Port)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#9-%EC%BB%A4%EB%84%A5%EC%85%98-%ED%83%80%EC%9E%85%EA%B3%BC-%EC%BB%A4%EB%84%A5%EC%85%98%EB%A6%AC%EC%8A%A4-%ED%83%80%EC%9E%85">9. 커넥션 타입과 커넥션리스 타입</a></li>
<li><a href="https://api.velog.io/rss/@mommers#10-%EB%8C%80%ED%91%9C-%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C">10. 대표 프로토콜</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%B4%9D-%EC%A0%95%EB%A6%AC">총 정리</a></li>
</ul>
<hr />
<h3 id="8-포트-port">8. 포트 (Port)</h3>
<h4 id="8-1-포트란">8-1. 포트란?</h4>
<ul>
<li>트랜스포트(전송) 계층에서 사용</li>
<li>프로세스를 식별하기 위한 번호</li>
<li>HTTP, CHAT 등 모두 프로세스로 취급</li>
</ul>
<h4 id="8-2-포트-번호">8-2. 포트 번호:</h4>
<ul>
<li>범위: 0 ~ 65535 (2^16 = 65,536개)</li>
<li><strong>1~1023</strong>: Well-Known Port (잘 알려진 포트)<ul>
<li>예: HTTP(80), HTTPS(443), SSH(22)</li>
</ul>
</li>
</ul>
<h4 id="8-3-바인딩-binding">8-3. 바인딩 (Binding)</h4>
<ul>
<li>프로세스에게 포트 번호를 지정해주는 것</li>
</ul>
<hr />
<h3 id="9-커넥션-타입과-커넥션리스-타입">9. 커넥션 타입과 커넥션리스 타입</h3>
<p>각 계층의 프로토콜은 <strong>커넥션 타입(연결형)</strong> 또는 <strong>커넥션리스 타입(비연결형)</strong> 데이터 전송 서비스를 상위 계층에 제공</p>
<h4 id="9-1-커넥션-connection">9-1. 커넥션 (Connection)</h4>
<ul>
<li>통신 단말 사이에 확립된 논리적 통신로 (예: 파이프)</li>
</ul>
<h4 id="9-2-커넥션-타입-연결형">9-2. 커넥션 타입 (연결형)</h4>
<ul>
<li>확실하게 정해진 순서를 따름</li>
<li>전송에 다소 시간이 걸리지만 데이터를 확실히 전송 가능</li>
<li>예시: TCP</li>
</ul>
<p><strong>동작 순서:</strong></p>
<ol>
<li>커넥션 확립</li>
<li>데이터 전송</li>
<li>커넥션 종료</li>
</ol>
<h4 id="9-3-커넥션리스-타입-비연결형">9-3. 커넥션리스 타입 (비연결형)</h4>
<ul>
<li>커넥션 확립 없이 곧바로 데이터를 보냄</li>
<li>빠르지만 신뢰성이 낮음</li>
<li>예시: UDP</li>
</ul>
<hr />
<h3 id="10-대표-프로토콜">10. 대표 프로토콜</h3>
<p>네트워크에서 이용되는 주요 프로토콜 (실제로 자주 사용되는 것들)</p>
<h4 id="10-1-계층별-프로토콜">10-1. 계층별 프로토콜:</h4>
<table>
<thead>
<tr>
<th>계층</th>
<th>환경/용도</th>
<th>프로토콜</th>
</tr>
</thead>
<tbody><tr>
<td><strong>물리/데이터링크</strong></td>
<td>유선</td>
<td>이더넷 (IEEE 802.3)</td>
</tr>
<tr>
<td></td>
<td>무선</td>
<td>IEEE 802.11 (Wi-Fi)</td>
</tr>
<tr>
<td><strong>네트워크</strong></td>
<td>-</td>
<td>IP (Internet Protocol)</td>
</tr>
<tr>
<td><strong>트랜스포트</strong></td>
<td>신뢰성 필요</td>
<td>TCP</td>
</tr>
<tr>
<td></td>
<td>실시간성 필요</td>
<td>UDP</td>
</tr>
<tr>
<td><strong>애플리케이션</strong></td>
<td>-</td>
<td>HTTP, HTTPS, QUIC, DNS</td>
</tr>
</tbody></table>
<h4 id="10-2-통신-과정">10-2. 통신 과정:</h4>
<ul>
<li>NIC 장치 드라이버, 운영체제, 애플리케이션이 각 계층에서 이용하는 프로토콜을 선택</li>
<li>송신 단말: 캡슐화</li>
<li>수신 단말: 비캡슐화</li>
</ul>
<hr />
<h3 id="총-정리">총 정리</h3>
<ul>
<li><strong>프로토콜</strong> = 네트워크 통신을 위한 규칙</li>
<li><strong>계층 구조</strong> = 역할별로 나누어 처리 (TCP/IP 4계층, OSI 7계층)</li>
<li><strong>캡슐화/비캡슐화</strong> = 송신 시 헤더 추가, 수신 시 헤더 제거</li>
<li><strong>대표 프로토콜</strong> = 이더넷, IP, TCP/UDP, HTTP/HTTPS</li>
</ul>