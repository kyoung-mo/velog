<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fb3c48be-878b-4598-bec9-5e11eb8b2217/image.png" /></p>
<hr />
<h3 id="📚-목차">📚 목차</h3>
<ul>
<li><a href="https://api.velog.io/rss/@mommers#1-%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C%EC%9D%B4%EB%9E%80">1. 프로토콜이란?</a></li>
<li><a href="https://api.velog.io/rss/@mommers#2-%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C%EC%97%90-%EC%A0%95%EC%9D%98%EB%90%98%EC%96%B4-%EC%9E%88%EB%8A%94-%EA%B2%83">2. 프로토콜에 정의되어 있는 것</a></li>
<li><a href="https://api.velog.io/rss/@mommers#3-%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C%EC%9D%98-%EA%B3%84%EC%B8%B5-%EA%B5%AC%EC%A1%B0">3. 프로토콜의 계층 구조</a></li>
<li><a href="https://api.velog.io/rss/@mommers#4-%EB%91%90-%EA%B0%80%EC%A7%80-%EA%B3%84%EC%B8%B5-%EA%B5%AC%EC%A1%B0-%EB%AA%A8%EB%8D%B8">4. 두 가지 계층 구조 모델</a></li>
<li><a href="https://api.velog.io/rss/@mommers#5-pdu-protocol-data-unit">5. PDU (Protocol Data Unit)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#6-%ED%91%9C%EC%A4%80%ED%99%94-%EB%8B%A8%EC%B2%B4">6. 표준화 단체</a></li>
<li><a href="https://api.velog.io/rss/@mommers#7-%EC%BA%A1%EC%8A%90%ED%99%94%EC%99%80-%EB%B9%84%EC%BA%A1%EC%8A%90%ED%99%94">7. 캡슐화와 비캡슐화</a></li>
</ul>
<hr />
<h3 id="1-프로토콜이란">1. 프로토콜이란?</h3>
<p><strong>프로토콜(Protocol)</strong> = 네트워크 세계에서 패킷을 처리하기 위한 규칙</p>
<ul>
<li>PC 제조사나 운영체제가 다르고, 유무선에 관계없이 동일하게 패킷 전달 가능</li>
<li>예시: HTTPS는 웹서버와 웹브라우저 사이에서 패킷을 암호화하여 교환할 때 사용하는 프로토콜</li>
</ul>
<hr />
<h3 id="2-프로토콜에-정의되어-있는-것">2. 프로토콜에 정의되어 있는 것</h3>
<h4 id="2-1-물리적-사양">2-1. 물리적 사양</h4>
<ul>
<li>LAN 케이블 소재, 커넥터 형태, 핀 배열 등 네트워크에서 눈에 보이는 모든 것</li>
<li>PC의 <strong>NIC(Network Interface Card)</strong>는 프로토콜에 정의된 내용에 기반하여 케이블이나 전송 매체에 패킷을 보냄</li>
</ul>
<h4 id="2-2-송신-상대-특정">2-2. 송신 상대 특정</h4>
<ul>
<li>송신 상대를 구별하기 위해 주소 할당</li>
<li>예시: <a href="http://www.google.com%EC%97%90%EB%8A%94">www.google.com에는</a> 172.217.175.4라는 숫자 주소가 할당됨</li>
</ul>
<h4 id="2-3-패킷-전송">2-3. 패킷 전송</h4>
<ul>
<li>컴퓨터는 송신 상대 특정 후 데이터를 패킷으로 작게 나누어 네트워크로 보냄</li>
<li>프로토콜에는 헤더의 어디에서 어디까지 어떤 정보를 포함하고 어떤 순서로 교환하는지 등이 정의됨</li>
<li>패킷 교환기(네트워크 기기)는 헤더의 정보를 기반으로 릴레이처럼 패킷을 전송</li>
</ul>
<h4 id="2-4-신뢰성-확립">2-4. 신뢰성 확립</h4>
<ul>
<li>통신 간에 문제가 생겨도 에러를 알리거나 재전송하는 구조 제공</li>
<li>유한한 네트워크 자원이 패킷으로 가득 차서 잠기지 않도록 하는 구조 제공</li>
</ul>
<h4 id="2-5-보안-확보">2-5. 보안 확보</h4>
<ul>
<li>중요한 정보를 안심하고 교환할 수 있도록 올바른 통신 상대인지 인증하고 통신을 암호화하는 구조 제공</li>
<li>예시: 온라인 스토어에서 구입 시 사용자 이름과 비밀번호를 입력하고, 웹브라우저는 접속 대상 서버가 올바른 통신 대상인지 확인하고 정보를 암호화해서 전송</li>
</ul>
<hr />
<h3 id="3-프로토콜의-계층-구조">3. 프로토콜의 계층 구조</h3>
<p>프로토콜로 정의된 다양한 통신 기능은 그 처리에 맞춰 <strong>계층 구조</strong>로 되어 있음</p>
<h4 id="동작-방식">동작 방식:</h4>
<ol>
<li><strong>송신자</strong>: 상위 계층부터 순서대로 데이터를 처리하여 패킷 상태로 전송매체에 보냄</li>
<li><strong>수신자</strong>: 하위 계층에서 순서대로 송신자와 동일한 프로토콜을 따라 데이터를 처리하고 최종적으로 원래 데이터로 복원</li>
</ol>
<hr />
<h3 id="4-두-가지-계층-구조-모델">4. 두 가지 계층 구조 모델</h3>
<p>통신에 필요한 기능을 계층별로 정리한 기초적인 두 가지 모델</p>
<h4 id="4-1-tcpip-참조-모델">4-1. TCP/IP 참조 모델</h4>
<ul>
<li><p>만든 곳의 이름을 따 <strong>DARPA 모델</strong>이라고도 불림</p>
</li>
<li><p>4개 계층 (아래부터):</p>
<ul>
<li><strong>링크 계층</strong> (네트워크 인터페이스 계층): 디지털 데이터를 물리적인 전송 매체로 보내는 변환/변조 및 신뢰성 확보</li>
<li><strong>인터넷 계층</strong>: 수신자 컴퓨터까지의 통신 경로를 확보하는 처리 수행</li>
<li><strong>트랜스포트 계층</strong>: 애플리케이션을 식별하고 그에 따라 통신 제어</li>
<li><strong>애플리케이션 계층</strong>: 사용자에게 애플리케이션 제공</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/48409f10-da59-480b-b68e-ecae4d3b0f90/image.png" /></p>
</li>
</ul>
<h4 id="4-2-osi-참조-모델-open-systems-interconnection">4-2. OSI 참조 모델 (Open Systems Interconnection)</h4>
<ul>
<li>ISO가 책정한 7계층 구조 모델</li>
<li>TCP/IP 참조 모델과 마찬가지로 각 계층의 역할이 나누어져 각각의 처리를 수행</li>
<li>너무 세세하여 원 모델을 그대로 사용하지는 않으나 체계적 논의에 유용</li>
<li>용어: L3 = 네트워크 계층, L4 = 트랜스포트 계층</li>
</ul>
<hr />
<h3 id="5-pdu-protocol-data-unit">5. PDU (Protocol Data Unit)</h3>
<p><strong>PDU</strong> = 각 계층에서 처리하는 한 덩어리의 데이터 단위</p>
<ul>
<li><strong>헤더</strong>: 제어 정보 포함</li>
<li><strong>페이로드(Payload)</strong>: 데이터 자체</li>
</ul>
<h3 id="51-pdu의-명칭">5.1. PDU의 명칭</h3>
<table>
<thead>
<tr>
<th>계층</th>
<th>계층 이름</th>
<th>PDU 이름</th>
</tr>
</thead>
<tbody><tr>
<td>7계층</td>
<td>애플리케이션 계층</td>
<td>메시지</td>
</tr>
<tr>
<td>4계층</td>
<td>트랜스포트 계층</td>
<td>세그먼트(TCP), 데이터그램(UDP)</td>
</tr>
<tr>
<td>3계층</td>
<td>네트워크 계층</td>
<td>패킷</td>
</tr>
<tr>
<td>2계층</td>
<td>데이터링크 계층</td>
<td>프레임</td>
</tr>
<tr>
<td>1계층</td>
<td>물리 계층</td>
<td>비트</td>
</tr>
</tbody></table>
<hr />
<h3 id="6-표준화-단체">6. 표준화 단체</h3>
<h4 id="6-1-ieee-institute-of-electrical-and-electronics-engineers">6-1. IEEE (Institute of Electrical and Electronics Engineers)</h4>
<ul>
<li>전기 기술 및 통신 공학 전문 연구 단체</li>
<li>하드웨어와 관련한 네트워크 기술의 표준화를 IEEE 802에서 연구 논의</li>
<li>예시: IEEE 802.3 (이더넷), IEEE 802.11 (무선 LAN)</li>
</ul>
<h4 id="6-2-ietf-internet-engineering-task-force">6-2. IETF (Internet Engineering Task Force)</h4>
<ul>
<li>인터넷 관련 기술의 표준화를 추진하는 조직</li>
<li>소프트웨어에 가까운 프로토콜을 책정</li>
<li>표준화된 규칙은 <strong>RFC(Request for Comments)</strong>로 문서화되어 공개</li>
</ul>
<hr />
<h3 id="7-캡슐화와-비캡슐화">7. 캡슐화와 비캡슐화</h3>
<h4 id="7-1-캡슐화-encapsulation---송신-단말">7-1. 캡슐화 (Encapsulation) - 송신 단말</h4>
<ol>
<li>애플리케이션 계층에서부터 순서대로 각 계층에서 페이로드에 헤더를 추가</li>
<li>PDU로 만든 후 아래 계층으로 전달</li>
<li>한 단계 아래 계층은 그 <strong>PDU를 페이로드로 인식</strong>하고 해당 계층의 헤더를 새롭게 추가</li>
</ol>
<h4 id="7-2-비캡슐화-decapsulation---수신-단말">7-2. 비캡슐화 (Decapsulation) - 수신 단말</h4>
<ol>
<li>물리 계층에서부터 순서대로 각 계층에서 헤더를 제거</li>
<li>페이로드만을 한 단계 위 계층으로 전달</li>
<li>한 단계 위 계층은 그 <strong>페이로드를 PDU로 인식</strong>하고 해당 계층의 헤더를 제거</li>
</ol>
<h4 id="7-3-계층-간-데이터-전달">7-3. 계층 간 데이터 전달</h4>
<ul>
<li>계층 간 이동 시 <strong>소켓(Socket)</strong>을 통해 데이터를 전달</li>
<li>송신: 서버, 수신: 클라이언트 (예: 크롬 브라우저)</li>
</ul>
<hr />
<p>이어서 <a href="https://velog.io/@mommers/TCPIP-%ED%8F%AC%ED%8A%B8%EC%99%80-%EC%BB%A4%EB%84%A5%EC%85%98-%EC%8B%A4%EC%A0%9C-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%A0%84%EC%86%A1-%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98">TCP/TP 2편</a>에서 정리하겠습니다..</p>