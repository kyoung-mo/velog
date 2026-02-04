<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f773f493-74e7-426a-8674-70e51f498747/image.png" /></p>
<p><a href="https://blog.desdelinux.net/ko/lnav-%EC%8B%9C%EC%8A%A4%ED%85%9C-%EB%A1%9C%EA%B7%B8%EB%A5%BC%EB%B3%B4%EA%B8%B0%EC%9C%84%ED%95%9C-%ED%9B%8C%EB%A5%AD%ED%95%9C-%EB%8F%84%EA%B5%AC/"><del>썸넬</del></a></p>
<hr />
<h3 id="로그-분석-journalctl-dmesg">로그 분석 (journalctl, dmesg)</h3>
<p>-
시스템 에러 추적. 커널 메시지.</p>
<ul>
<li><code>journalctl -xe</code>로 방금 발생한 에러 로그 상세 확인.</li>
<li><code>journalctl -u ssh</code>로 SSH 서비스 로그만 필터링.</li>
<li><code>dmesg | grep usb</code>로 USB 장치 연결 기록 확인.</li>
</ul>
<hr />
<h3 id="journalctl--vs-dmesg">journalctl  vs dmesg</h3>
<hr />
<p><code>dmesg</code>는 '커널(하드웨어)이 토하는 로그'만 보는 것, <code>journalctl</code>은 '시스템의 모든 역사(S/W 포함)'를 검색하는 도구.</p>
<p>최신 리눅스(Systemd 기반)에서는 <code>journalctl</code>이 <code>dmesg</code>의 내용을 포함하고 있으므로, <code>journalctl</code> 하나만 잘 써도 됩니다.</p>
<h3 id="1-dmesg-diagnostic-message">1. dmesg (Diagnostic Message)</h3>
<ul>
<li>출처: 커널 링 버퍼 (Kernel Ring Buffer). 메모리 공간에 있는 데이터를 긁어옵니다.</li>
<li>내용: 부팅 과정, 하드웨어 인식(USB, LAN), 드라이버 로딩, 커널 패닉 등.</li>
<li>특징:<ul>
<li>휘발성: 재부팅하면 내용이 초기화됩니다 (링 버퍼 특성).</li>
<li>빠름: 단순히 메모리를 읽어서 출력하므로 매우 빠르고 단순합니다.</li>
<li>주 용도: &quot;방금 꽂은 USB가 인식됐나?&quot;, &quot;드라이버가 왜 죽었지?&quot; 확인할 때.</li>
</ul>
</li>
</ul>
<h3 id="2-journalctl-journal-control">2. journalctl (Journal Control)</h3>
<ul>
<li>출처: Systemd Journal. 디스크에 저장된 바이너리 로그 데이터베이스.</li>
<li>내용: <code>dmesg</code> 내용 + 모든 서비스 로그(웹서버, SSH) + 사용자 앱 로그.</li>
<li>특징:<ul>
<li>영구성: 재부팅 후에도 과거 로그를 뒤져볼 수 있습니다 (<code>b</code> 옵션).</li>
<li>검색: 시간별, 서비스별, 중요도별 필터링이 강력합니다.</li>
<li>주 용도: &quot;어제 밤에 웹서버가 왜 죽었지?&quot;, &quot;부팅부터 지금까지 전체 흐름을 보자.&quot;</li>
</ul>
</li>
</ul>
<h3 id="3-비교표">3. 비교표</h3>
<table>
<thead>
<tr>
<th>비교 항목</th>
<th>dmesg</th>
<th>journalctl</th>
</tr>
</thead>
<tbody><tr>
<td>영역</td>
<td>커널 &amp; 하드웨어 Only</td>
<td>시스템 전체 (커널 + 유저 공간)</td>
</tr>
<tr>
<td>저장소</td>
<td>RAM (Ring Buffer)</td>
<td>Disk (<code>/var/log/journal</code>)</td>
</tr>
<tr>
<td>재부팅 후</td>
<td>사라짐 (초기화)</td>
<td>남아있음 (설정 시)</td>
</tr>
<tr>
<td>필터링</td>
<td>거의 없음 (<code>grep</code> 써야 함)</td>
<td>매우 강력함 (옵션 내장)</td>
</tr>
</tbody></table>
<h3 id="4-dmesg-대신-joutnalctl-사용-가능">4. dmesg 대신 joutnalctl 사용 가능</h3>
<p><code>dmesg</code> 기능을 <code>journalctl</code>로 대체하는 방법입니다.</p>
<p>A. 커널 로그만 보고 싶을 때 (<code>dmesg</code>와 동일)</p>
<pre><code class="language-bash">journalctl -k
# -k: Kernel messages only</code></pre>
<p>B. 실시간으로 로그 따라가기 (<code>tail -f</code> 효과)</p>
<pre><code class="language-bash"># dmesg -w 와 비슷하지만 더 강력함
journalctl -f</code></pre>
<p>C. 이번 부팅 로그만 보기 (재부팅 직후)</p>
<pre><code class="language-bash">journalctl -b</code></pre>
<p>D. 빨간색 에러만 골라 보기</p>
<pre><code class="language-bash">journalctl -p err
# -p: Priority (err, warning, info...)</code></pre>
<hr />
<p>결론적으로, <code>dmesg</code>를 사용해도 괜찮으나, 과거 내역을 보거나 특정 서비스와 연관성을 찾기 위해서는 <code>journalctl</code> 를 사용하면 좋습니다.</p>