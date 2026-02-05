<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/9be5f16f-4961-47ee-a6b6-d7022df37f23/image.png" /></p>
<hr />
<p>오늘 교육 끝나고 자리를 바꿨는데, 라즈베리파이에 들어가서 실습 코드 한번 더 보고 실행해보려 접속했더니 접속이 안됐다..</p>
<p>다른 사람들은 자리 바꿔도 잘 된다는데 나만 안되서 이게 무슨 일인가 싶었다.</p>
<p>아까 선 배선한다고 플러그 전원 켜져있는 상태에서 라즈베리파이 껐다 켰다 많이 반복했었는데, 그것 때문에 라즈베리파이가 고장났나 싶었다..</p>
<p>일단 ssh 통신이 안되기 때문에 아래 FT232RL칩을 사용해서 SSH 통신을 해줬다.</p>
<ul>
<li><code>GND</code> , <code>TX</code> , <code>RX</code> 배선만 진행하고, MobaXterm으로 Serial 통신을 baudrate=115,200으로 진행하였다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/228f2972-9912-4a01-bd39-c4c2db930a15/image.png" /></p>
<p>다행히 시리얼 통신은 문제 없었고, <code>ping 8.8.8.8</code> 을 통해 인터넷이랑 연결되고있나 확인해봤는데 역시나 안되어있었다. 이후 <code>ip addr show</code> , <code>ifconfig -a</code> 두 명령어를 쳐봤는데</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ba64a9c4-f68c-4ea2-9d9a-bbe8ac941e2c/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b8796924-c73c-4ac8-b771-95b997475d99/image.png" /></p>
<p>여기서 에러가 보이는건 처음이라 내거 아닌 물건 망가뜨렸다는 생각에 진땀이 나기 시작했다..</p>
<h3 id="하드웨어-문제인지-확인">하드웨어 문제인지 확인</h3>
<p>일단 라즈베리파이 자체가 망가진건지 확인해봐야겠다 싶어서 ethtool eth0 명령어로 이더넷 포트 상태를 확인해봤다.</p>
<pre><code class="language-bash">pi@pi-222:~$ ethtool eth0
Settings for eth0:
        Link detected: yes
        Speed: 100Mb/s
        Duplex: Full</code></pre>
<p>링크도 감지되고 속도도 정상이었다. ethtool -S eth0로 패킷 통계도 확인해봤는데 TX 패킷이 400개 넘게 전송되고 있고, 에러 카운터는 모두 0이었다. 이더넷 포트 하드웨어는 정상인 것 같았다. 휴.. 다행이다 싶었다.
문제는 eth0가 UP 상태인데도 IP 주소가 할당되지 않았다는 거였다. DHCP로 IP를 받아야 하는데 받지 못하고 있는 상황이었다.</p>
<h3 id="네트워크-설정-확인">네트워크 설정 확인</h3>
<p>일단 ip route show로 라우팅 테이블을 확인해봤다.</p>
<pre><code class="language-bash">pi@pi-222:~$ ip route show
default via 10.10.16.1 dev eth0 proto static metric 100
10.10.16.0/24 dev eth0 proto kernel scope link src 10.10.16.222 metric 100</code></pre>
<p>게이트웨이는 10.10.16.1로 설정되어 있었다. 그런데 <code>ping 10.10.16.1</code>을 해보니까</p>
<pre><code class="language-bash">pi@pi-222:~$ ping 10.10.16.1
PING 10.10.16.1 (10.10.16.1) 56(84) bytes of data.
From 10.10.16.222 icmp_seq=1 Destination Host Unreachable</code></pre>
<p>게이트웨이로 ping이 안 갔다. 라우팅 설정은 정상인데 게이트웨이가 응답을 안 하는 상황이었다.</p>
<p>혹시 새로 옮긴 자리의 네트워크 설정이 다른 건 아닐까 싶어서, 내 노트북으로 같은 이더넷 포트에 연결해서 <code>ipconfig</code>를 쳐봤다.</p>
<pre><code class="language-plaintext">C:\Users\KCCISTC&gt;ipconfig

이더넷 어댑터 이더넷:
   IPv4 주소 . . . . . . . . . : 10.10.16.172
   서브넷 마스크 . . . . . . . : 255.255.255.0
   기본 게이트웨이 . . . . . . : 10.10.16.254</code></pre>
<p>게이트웨이가 10.10.16.254였다,, 이전 자리에서는 10.10.16.1이었는데, 새 자리는 10.10.16.254로 바뀐 거였다.</p>
<h3 id="문제-해결">문제 해결</h3>
<p>원인을 찾았으니 이제 라즈베리파이 설정을 고쳐주면 됐다.</p>
<pre><code class="language-bash"># 게이트웨이를 10.10.16.254로 변경
sudo nmcli connection modify &quot;Wired connection 1&quot; ipv4.gateway 10.10.16.254

# 연결 재시작
sudo nmcli connection down &quot;Wired connection 1&quot;
sudo nmcli connection up &quot;Wired connection 1&quot;</code></pre>
<p>그리고 다시 ping을 쳐봤다.</p>
<pre><code class="language-bash">pi@pi-222:~$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=112 time=42.4 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=112 time=41.9 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=112 time=41.6 ms</code></pre>
<p>드디어 됐다! 🎉
SSH 접속도 정상적으로 되는 걸 확인했다.</p>
<h3 id="회고">회고</h3>
<p>처음엔 라즈베리파이가 고장난 줄 알고 엄청 당황했는데, 알고 보니 단순히 네트워크 설정 문제였다. 자리를 옮기면서 네트워크 환경이 바뀌었고, 특히 게이트웨이 주소가 달라진 게 원인이었다.
이번 트러블슈팅을 통해 배운 점:</p>
<ol>
<li>하드웨어 문제인지 먼저 확인하기: ethtool로 물리 계층이 정상인지 확인</li>
<li>네트워크 설정 체계적으로 확인하기: IP → 게이트웨이 → DNS 순서로</li>
<li>주변 환경 변화 고려하기: 자리를 옮기면 네트워크 설정도 바뀔 수 있다.</li>
<li>시리얼 통신의 중요성: SSH가 안 될 때 시리얼 통신으로 접근할 수 있어서 정말 다행이었다.</li>
</ol>
<p>다음부터는 자리 옮길 때 네트워크 설정부터 확인해봐야겠다!</p>
<h3 id="참고-명령어">참고 명령어</h3>
<pre><code class="language-bash"># 네트워크 상태 확인
ip addr show
ip route show
nmcli device status

# 하드웨어 상태 확인
```bash
ethtool eth0
ethtool -S eth0

# 고정 IP 설정 (NetworkManager)
sudo nmcli connection modify &quot;Wired connection 1&quot; ipv4.addresses 10.10.16.222/24
sudo nmcli connection modify &quot;Wired connection 1&quot; ipv4.gateway 10.10.16.254
sudo nmcli connection modify &quot;Wired connection 1&quot; ipv4.dns &quot;8.8.8.8&quot;
sudo nmcli connection modify &quot;Wired connection 1&quot; ipv4.method manual

# 연결 재시작
sudo nmcli connection down &quot;Wired connection 1&quot;
sudo nmcli connection up &quot;Wired connection 1&quot;</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/cf8cdb13-bfe0-4198-a5f1-52da0e090854/image.png" /></p>
<p>이제 하나 더 해야한다 ㅎ</p>
<hr />
<p><code>+ 추가</code> 남은 라즈베리파이 하나가 시리얼 통신이 안되서 이것저것 확인해봤었는데 재부팅하니 해결됐다.</p>
<p>이어서 이것저것 다시 설정 ..</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d4d30dca-f6bf-4f6d-91b7-6f02f2b285e1/image.png" /></p>
<p><code>ping 8.8.8.8</code> 잘 되는 것 확인 완료!</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c1b72d99-840e-474e-8718-4c83f5e95d80/image.png" /></p>
<p><code>rpi-connect</code> 재부팅 시 자동으로 켜지게 하기 위해 위와 같이 설정해주었다.</p>
<pre><code class="language-bash">07:58:17 pi@pi-mo ~ → sudo nano /etc/rc.local

    GNU nano 8.4                      /etc/rc.local
#!/bin/sh -e        # 여기부터 작성, 없으면 새로 만들어짐
#
# rc.local
#

rpi-connect on

exit 0                # 여기까지 작성, 저장

# 권한 부여
07:59:22 pi@pi-mo ~ → sudo chmod +x /etc/rc.local</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/df6ba18e-3e98-492e-aca5-bf9e48acdc92/image.png" /></p>
<p>다시 잘 되는것을 확인하였다!</p>