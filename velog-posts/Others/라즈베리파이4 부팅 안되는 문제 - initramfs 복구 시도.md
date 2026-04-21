<blockquote>
<p>ROS2 수업 이후 프로젝트를 진행하는 과정에서 팀원의 라즈베리파이4가 갑자기 부팅이 안 되는 문제가 발생했습니다.</p>
</blockquote>
<blockquote>
<p>Serial 통신으로 오류를 직접 해결한 경험이 있어서 이번에도 해결해보고자 했습니다.</p>
</blockquote>
<hr />
<h2 id="증상">증상</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c9685f5d-78fa-4a14-90ef-1882c137160a/image.png" /></p>
<p>위 화면에서 더 이상 부팅 로그가 출력되지 않았습니다. CLI 환경에서 직접 확인하고자 모니터를 라즈베리파이4에 연결하였고, 그 이후로 아래와 같은 현상이 나타났습니다.</p>
<ul>
<li>부팅 시 initramfs 쉘로 떨어짐</li>
<li>정상적인 Ubuntu 부팅이 되지 않음</li>
</ul>
<hr />
<h2 id="원인-분석">원인 분석</h2>
<p>initramfs에서 확인한 결과 아래 메시지가 출력되었습니다.</p>
<pre><code>Superblock needs_recovery flag is clear, but journal has data.</code></pre><p><strong>전원을 갑자기 차단한 것이 원인인 것 같습니다.</strong> journal이 커밋되지 않은 채로 superblock이 클린 상태로 표시된 것입니다.<br />라즈베리파이를 <code>shutdown</code> 명령 없이 전원을 차단하면 이런 문제가 발생할 수 있습니다.</p>
<hr />
<h2 id="복구-시도-과정">복구 시도 과정</h2>
<h3 id="1단계---fsckext4-실행">1단계 - fsck.ext4 실행</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0067cf16-ade5-483f-ae29-4bd38732d725/image.png" /></p>
<pre><code class="language-bash">fsck.ext4 -y /dev/mmcblk0p2</code></pre>
<p><strong>결과:</strong></p>
<pre><code>fsck.ext4: unable to set superblock flags on writable
WARNING: Filesystem still has errors</code></pre><p>superblock 수정 자체가 되지 않았습니다.</p>
<hr />
<h3 id="2단계---백업-superblock으로-복구-시도">2단계 - 백업 superblock으로 복구 시도</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ca5b9313-de4f-4335-ad95-bde6112b01f9/image.png" /></p>
<pre><code class="language-bash">e2fsck -b 32768 -y /dev/mmcblk0p2
e2fsck -b 98304 -y /dev/mmcblk0p2</code></pre>
<p><strong>결과:</strong> 파일시스템 변경 로그(<code>FILE SYSTEM WAS MODIFIED</code>)는 출력됐지만 여전히 <code>WARNING: Filesystem still has errors</code> 메시지가 나왔습니다.</p>
<hr />
<h3 id="3단계---저널-강제-리셋-시도">3단계 - 저널 강제 리셋 시도</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/581259fe-7020-4103-90e8-70ec7e5b9408/image.png" /></p>
<pre><code class="language-bash">tune2fs -O ^has_journal /dev/mmcblk0p2</code></pre>
<p><strong>결과:</strong> <code>tune2fs: not found</code><br />initramfs 환경이라 사용 가능한 툴이 매우 제한적이었습니다.</p>
<hr />
<h3 id="4단계---journal_only-옵션으로-e2fsck">4단계 - journal_only 옵션으로 e2fsck</h3>
<pre><code class="language-bash">e2fsck -f -y -E journal_only /dev/mmcblk0p2</code></pre>
<p><strong>결과:</strong> 마찬가지로 실패했습니다.</p>
<hr />
<h3 id="5단계---dmesg로-하드웨어-오류-확인">5단계 - dmesg로 하드웨어 오류 확인</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/4e457264-1b3c-4ee1-875c-5290b65c12a3/image.png" /></p>
<pre><code class="language-bash">dmesg | grep -i &quot;mmcblk\|error\|i/o&quot;</code></pre>
<p><strong>결과:</strong></p>
<pre><code>mmcblk0: mmc0:aaaa SD32G 29.7 GiB
mmcblk0: p1 p2
mmcblk0: mmc0:aaaa SD32G 29.7 GiB</code></pre><p>I/O 에러가 없었습니다. <strong>SD카드의 물리적 손상은 아닌 것 같습니다.</strong></p>
<hr />
<h3 id="6단계---sd카드-분리-후-windows에서-접근">6단계 - SD카드 분리 후 Windows에서 접근</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/477707af-fb39-42a2-bf1d-0c39efe72abc/image.png" /></p>
<p>SD카드를 분리해 Windows PC에 연결했습니다.<br /><code>system-boot (D:)</code> FAT32 부트 파티션은 정상적으로 접근이 가능했습니다.<br />하지만 중요 파일(<code>/etc/netplan/50-~~.yaml</code>)은 ext4인 <code>writable</code> 파티션에 있어서 Windows에서는 기본적으로 읽을 수 없었습니다.</p>
<hr />
<h3 id="7단계---diskgenius로-ext4-파티션-접근-시도">7단계 - DiskGenius로 ext4 파티션 접근 시도</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/91a4301f-22e7-4a76-bd7c-54d61eb81728/image.png" /></p>
<p>DiskGenius 무료버전으로 ext4 파티션 접근을 시도했습니다.<br />파일 탐색이 가능했고 <strong>Copy to 기능</strong>을 통해 팀원이 백업을 요청한 <code>50-cloud-init</code> 파일을 무사히 백업했습니다.</p>
<hr />
<h2 id="결론">결론</h2>
<table>
<thead>
<tr>
<th>시도</th>
<th>결과</th>
</tr>
</thead>
<tbody><tr>
<td>fsck.ext4 -y</td>
<td>superblock 수정 불가</td>
</tr>
<tr>
<td>e2fsck 백업 superblock</td>
<td>에러 지속</td>
</tr>
<tr>
<td>tune2fs 저널 리셋</td>
<td>툴 없음</td>
</tr>
<tr>
<td>DiskGenius 파일 추출</td>
<td>정상 작동</td>
</tr>
</tbody></table>
<p><strong>최종적으로 SD카드를 재플래싱하는 것으로 결론을 냈습니다.</strong></p>
<hr />
<h2 id="예방-방법">예방 방법</h2>
<p>라즈베리파이는 반드시 정상 종료 명령 이후에 전원을 차단해야 합니다.</p>
<pre><code class="language-bash">sudo shutdown -h now
# 또는
sudo poweroff</code></pre>
<p>갑작스러운 전원 차단은 파일시스템 손상의 주요 원인이 될 수 있습니다.</p>
<hr />
<h2 id="참고-사항">참고 사항</h2>
<ul>
<li>복구에 필요한 툴(<code>tune2fs</code>, <code>debugfs</code>)은 initramfs 환경에 포함되어 있지 않았습니다.</li>
<li>Ubuntu Live USB로 부팅하면 툴이 모두 갖춰져 있어서 복구 가능성이 더 높을 것 같습니다.</li>
<li>ext4 파티션을 Windows에서 읽으려면 <strong>Linux Reader</strong>(DiskInternals)를 사용하는 것을 추천합니다.</li>
</ul>