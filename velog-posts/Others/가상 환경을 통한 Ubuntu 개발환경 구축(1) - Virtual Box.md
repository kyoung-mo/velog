<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/58763cc9-07c7-44d8-bb21-7c46986f47d4/image.png" /></p>
<p>하나의 PC에는 하나의 운영체제만 사용이 가능하다.
우리는 이번 수업에서 리눅스 환경에서 윈도우 툴을 사용해서 개발을 할 것이기 때문에 <code>Virtual Box</code> 를 사용하여 Ubuntu 가상환경에 윈도우 툴을 이용하여 개발할 수 있다.</p>
<hr />
<p>일단 window ip, ubuntu ip, raspberry pi ip를 20명이 인당 하나씩 설정해줘야 하기 때문에 ip 주소를 다시 할당해주었다.</p>
<p>내 자리는</p>
<ul>
<li>window : 10.10.16.5</li>
<li>ubuntu : 10.10.16.35</li>
<li>raspberrypi : 10.10.16.65</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b108640c-31b9-45df-b54e-59bb398ae273/image.png" /></p>
<hr />
<p>교수님 자리는</p>
<ul>
<li>window : 10.10.16.30</li>
<li>ubuntu : 10.10.16.60</li>
<li>pi : 10.10.16.90</li>
</ul>
<hr />
<p>이렇게 설정되어있다.</p>
<h2 id="virtual-box-설치">Virtual Box 설치</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a4279653-2440-4ee2-9950-ec3190cd34f4/image.png" /></p>
<p>위와 같이 기본 메모리와 프로세서, Hard Disk Size를 윈도우 운영체제의 자원에서 떼준다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/087b15f9-0ae8-48bb-9ab6-277a72419699/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/dbc14635-a667-499f-916a-45981cc9e860/image.png" /></p>
<p>이후 VirtualBox는 생성이 됐고, 실행을 해보면 
아무 운영체제 없이 실행했기 때문에 가상 머신 부팅에 실패한다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1b807733-c1cc-43cf-a269-c43e120ea988/image.png" /></p>
<hr />
<h3 id="운영체제-설치">운영체제 설치</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1f3b73fb-1afd-4ed8-afcd-da8421a2a672/image.png" /></p>
<p><a href="https://releases.ubuntu.com/jammy/">https://releases.ubuntu.com/jammy/</a></p>
<p>위 사이트에서 Desktop image에 있는 <code>64-bit PC (AMD64) desktop image</code> 를 받아준다.</p>
<hr />
<p>이후 VirtualBox를 새로 생성해준다음, </p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d24b6be6-7a4e-4a06-a1a7-ef4ac682d1ef/image.png" /></p>
<p>방금 다운 받은 운영체제를 선택해준다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/8190b2d6-424d-49b9-9882-18a453eb2f3a/image.png" /></p>
<p>Try or Install Ubuntu</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/08a8a46b-f096-4f34-81db-0f36d4de7ae2/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0f993304-aa75-4f28-be34-4aed60a3dbff/image.png" /></p>
<p>우분투 관련 기본 설정을 마무리해주면 윈도우 환경에서 가상환경을 통해 Ubuntu 운영체제를 실행해줄 수 있다.</p>
<p>22.04를 다운받은 후, 최신 버전 업그레이드를 할거냐? 라는 창이 나오는데, 수업 시간에 Ros를 사용할 예정이므로 아니오를 선택해줬다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a0518872-cec2-492c-bce4-65b2462637e5/image.png" /></p>
<p>이후 소프트웨어 업데이터는 설치해줬다.</p>
<hr />
<h2 id="ubuntu-고정-ip-설정">Ubuntu 고정 IP 설정</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fc573958-8d80-412d-b741-d824aa9416a8/image.png" /></p>
<p>케이블 연결을 끊은 후,
설정 - IPv4에서 IPv4 방식을 DHCP가 아닌 수동으로 설정해준 후, 주소, 마스크, 게이트웨이, DNS를 설정해줬다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/50f3c9cf-3d86-48d3-bcf8-ab6c40c449a5/image.png" /></p>
<p>설정 이후 이더넷이 연결 안되는 문제가 있었는데, 가상환경 설정에서 네트워크 &gt; 어탭터 부분에서 Attached to 선택을 기존 NAT -&gt; 어댑터에 브리지 로 설정을 바꿔주니 해결되었다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/358d7781-475d-400e-853b-7f65d039effe/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bdc82ae4-eed5-45d4-8477-d2607c1f9c3b/image.png" /></p>
<p>인터넷이 잘 되는 것을 확인하였다.</p>
<hr />
<p>이후 .. putty 설치 과정 정리</p>
<p><a href="https://velog.io/@mommers/%EA%B0%80%EC%83%81-%ED%99%98%EA%B2%BD%EC%9D%84-%ED%86%B5%ED%95%9C-Ubuntu-%EA%B0%9C%EB%B0%9C%ED%99%98%EA%B2%BD-%EA%B5%AC%EC%B6%952-Putty">[다음 글] 가상 환경을 통한 Ubuntu 개발환경 구축(2) - Putty </a></p>