<p>굉장히 오랜만에 밀린 수업 정리를 시작하네요.. 이때까지 좋은 기회가 생겨서 잘하는 친구 피드백을 받으며 백준 실버를 목표로 알고리즘 문제도 풀고, 수업 진도 따라가고 반복하는 일상을 살았습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5497f156-0d3a-4f84-af68-931016c8caf9/image.png" /></p>
<p>일단 처음에 목표로 하던 실버를 찍었으니 다시 수업 정리를 해보려 합니다!</p>
<p>서울기술교육센터에서 진행하는 과정이라 터틀봇3 버거도 지원 받아서, 이걸 기반으로 ROS 수업을 진행한다고 해요.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d4853ac0-95e5-41ca-b39c-9134ab309f4c/image.png" /></p>
<blockquote>
<p>이번 글에서는 터틀봇3에 들어가는 라즈베리파이4 보드에 대한 기본적인 환경 설정을 하려고합니다.</p>
</blockquote>
<blockquote>
<p>수업을 진행한 교재는 ROS 2로 시작하는 로봇 프로그래밍, 주로 참고한 사이트는 ROBOTIS e-Manual입니다.</p>
</blockquote>
<p>대부분의 ros2 수업 정리는 e-Manual 순서에 맞게 작성중이라 필요하신분은 사이트를 확인하셔도 좋을 것 같습니다.</p>
<p><a href="https://emanual.robotis.com/docs/en/platform/turtlebot3/sbc_setup/#sbc-setup">🔗ROBOTIS-e-Manual : 3. 2. SBC Setup 공식 사이트</a></p>
<h2 id="1-sbc-setup">1. SBC Setup</h2>
<p>라즈베리파이4에 들어갈 microSD card를 준비해줍니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/20bff604-c1c9-4a12-94af-0c3888ab5e71/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5c2e236b-d690-4f1c-94a3-4de6a4397c6b/image.png" /></p>
<p><code>Raspberry Pi Imager</code> 에서 Ubuntu Server 22.04 버전을 받아줍니다.</p>
<p>수업을 진행하며 GUI 환경은 필요하진 않다 싶어서 CLI 환경으로도 충분하다 싶었습니다.</p>
<p>(어차피 가상 환경에서의 Ubuntu를 이용해 Gazebo, Navi 등의 툴을 사용, 실제 터틀봇을 사용할때는 bringup을 해두고 사용)</p>
<hr />
<ol>
<li>라즈베리파이 이미저를 실행</li>
<li>Choose OS</li>
<li>Other general-purpose OS</li>
<li>Ubuntu 선택</li>
<li>Ubuntu Server 22.04.5 LTS (64-bit) 선택</li>
<li>쭉쭉 진행</li>
</ol>
<blockquote>
<p>Server OS를 선택해야합니다.
Desktop OS ✖️</p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6c26b15b-d428-477d-ac67-8b4146045bd0/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/94a5f98d-655d-4f42-ac46-64172d94c79a/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c63724fb-65c8-4f1e-832b-7c8ca621f69e/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/6317c825-1b55-4e05-b3a0-dc2ff9c782b5/image.png" /></p>
<blockquote>
<p>hostname은 추후에 
[ <code>사용자이름</code> @ <code>호스트이름</code> ] 으로 사용됩니다. 한 반에서 호스트이름이 겹치지 않게 제 번호에 맞게 <code>bot05</code> 로 설정, 사용자 이름은 <code>ubuntu</code>로 통일해주었습니다.</p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/395f62ac-e4bf-44eb-932e-4e5288bd1bca/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c290eec6-a57a-4a0a-b8e7-162aa554b086/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/069c2445-2742-4510-b7ca-c6b2a32445ed/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b02cc511-7843-4410-bef3-1970d95036bf/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/bafeb364-3255-404b-b2ce-50b05c69ce65/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/121b099e-a748-4acc-af86-c8de39c51503/image.png" /></p>
<blockquote>
<p>이후 라즈베리파이가 Wifi를 사용할 때, 필요한 고정 IP를 설정해주었습니다.</p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5467dd75-0672-4185-8edb-3ffde203aad5/image.png" /></p>
<pre><code class="language-bash"># This file is generated from information provided by the datasource.  Changes
# to it will not persist across an instance reboot.  To disable cloud-init's
# network configuration capabilities, write a file
# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
# network: {config: disabled}
network:
    version: 2
    renderer: networkd
    ethernets:
        eth0:
            dhcp4: true
            dhcp6: true
            optional: true
    wifis:
        wlan0:
            dhcp4: false
            dhcp6: false
            addresses: [10.10.16.95/24]
            gateway4: 10.10.16.254
            nameservers:
                addresses: [203.248.252.2, 8.8.8.8]
            access-points:
                KCCI603_5G:
                    password: // 비밀번호 설정</code></pre>
<p><code>/etc/netplan</code> 위치에 위 파일을 추가해줍니다.</p>
<p>부팅 후, 아래 명령어를 통해 ssh를 사용할 수 있게 설정해줍니다.</p>
<pre><code class="language-bash">sudo nano /etc/netplan/50-cloud-init.yaml

sudo nano /etc/apt/apt.conf.d/20auto-upgrades

APT::Periodic::Update-Package-Lists &quot;0&quot;;
APT::Periodic::Unattended-Upgrade &quot;0&quot;;

systemctl mask systemd-networkd-wait-online.service

sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target

sudo reboot

ssh ubuntu@{IP Address of Raspberry PI}</code></pre>
<hr />
<h2 id="2-pc-setupubuntu-2204">2. PC Setup(Ubuntu 22.04)</h2>
<blockquote>
<p><a href="https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/#pc-setup">🔗ROBOTIS e-Manual 3.1. PC Setup</a>
<a href="https://docs.ros.org/en/humble/Installation.html">🔗ROS 2 Documentation : Humble</a></p>
</blockquote>
<p>이번에는 PC(Ubuntu) 설정을 해보겠습니다.
주로 ROS 2 Documentation : humble 링크를 참고하여 진행되었고,</p>
<p>Ubuntu는 윈도우 환경에서 가상환경 <code>Virtual Box</code> 를 이용하여 사용하였습니다.</p>
<p>가상환경에 우분투 까는 과정은 저번에 정리해둔 글이 있어서 링크 남겨두겠습니다.</p>
<blockquote>
<p>🔗 <a href="https://velog.io/@mommers/%EA%B0%80%EC%83%81-%ED%99%98%EA%B2%BD%EC%9D%84-%ED%86%B5%ED%95%9C-Ubuntu-%EA%B0%9C%EB%B0%9C%ED%99%98%EA%B2%BD-%EA%B5%AC%EC%B6%95">가상 환경을 통한 Ubuntu 개발환경 구축(1) - Virtual Box</a></p>
</blockquote>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/25c726d8-6893-4b88-98ea-5a343d8ee42a/image.png" /></p>
<h3 id="1-로케일-설정">1. 로케일 설정</h3>
<p>ROS2 공식 문서에서는 UTF-8 로케일 환경을 권장하고 있습니다.</p>
<p>한글 환경(ko_KR.UTF-8)도 UTF-8이면 설치에 문제는 없으나, 문서 기준대로 진행했습니다.</p>
<pre><code class="language-bash">locale  # UTF-8 확인

sudo apt update &amp;&amp; sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # 설정 확인</code></pre>
<p>설치 후 한글 환경으로 되돌리려면 아래 명령어를 사용하면 됩니다.</p>
<pre><code class="language-bash">sudo update-locale LANG=ko_KR.UTF-8 LANGUAGE=ko:en LC_ALL=ko_KR.UTF-8
source /etc/default/locale</code></pre>
<h3 id="2-소스-등록">2. 소스 등록</h3>
<p>ROS2 apt 저장소를 시스템에 추가했습니다.</p>
<pre><code class="language-bash">sudo apt install software-properties-common
sudo add-apt-repository universe

sudo apt update &amp;&amp; sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F &quot;tag_name&quot; | awk -F'&quot;' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb &quot;https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release &amp;&amp; echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb&quot;
sudo dpkg -i /tmp/ros2-apt-source.deb</code></pre>
<h3 id="3-ros2-패키지-설치">3. ROS2 패키지 설치</h3>
<pre><code class="language-bash">sudo apt update
sudo apt upgrade</code></pre>
<blockquote>
<p><strong>주의:</strong> Ubuntu 22.04에서는 ROS2 설치 전에 반드시 <code>systemd</code>, <code>udev</code> 관련 패키지를 먼저 업그레이드해야 합니다.</p>
<p>업그레이드 없이 설치하면 핵심 시스템 패키지가 제거될 수 있습니다.</p>
</blockquote>
<p>Desktop 버전(RViz, 데모, 튜토리얼 포함)을 설치했습니다.</p>
<pre><code class="language-bash">sudo apt install ros-humble-desktop</code></pre>
<p>개발 도구도 함께 설치했습니다.</p>
<pre><code class="language-bash">sudo apt install ros-dev-tools</code></pre>
<h3 id="4-환경-설정">4. 환경 설정</h3>
<p>터미널을 열 때마다 ROS2 환경을 자동으로 불러오도록 <code>.bashrc</code>에 추가했습니다.</p>
<pre><code class="language-bash">echo &quot;source /opt/ros/humble/setup.bash&quot; &gt;&gt; ~/.bashrc
source ~/.bashrc</code></pre>
<p>환경 설정이 정상적으로 완료되었는지 아래 명령어로 확인할 수 있습니다.</p>
<pre><code class="language-bash">printenv | grep -i ROS</code></pre>
<p>아래와 같이 <code>ROS_DISTRO</code>, <code>ROS_VERSION</code> 등의 변수가 출력되면 정상입니다.</p>
<pre><code>ROS_VERSION=2
ROS_PYTHON_VERSION=3
ROS_DISTRO=humble</code></pre><h3 id="5-기본-예제-테스트">5. 기본 예제 테스트</h3>
<p>ROS2 설치가 정상적으로 완료되었는지 확인하기 위해 <code>demo_nodes_cpp</code>와 <code>demo_nodes_py</code> 패키지를 이용한 talker-listener 예제를 실행해보았습니다.</p>
<p>터미널을 두 개 열어 각각 아래 명령어를 실행합니다.</p>
<pre><code class="language-bash"># 터미널 1 - talker
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_cpp talker</code></pre>
<pre><code class="language-bash"># 터미널 2 - listener
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c692a929-2c60-4261-8500-7f840f23ef9f/image.png" /></p>
<p>talker가 <code>Hello World: N</code> 메시지를 퍼블리시하고, listener가 이를 정상적으로 수신하는 것을 확인했습니다.</p>
<hr />
<h3 id="6-ros_domain_id-설정">6. ROS_DOMAIN_ID 설정</h3>
<p>예제 테스트 과정에서 문제가 하나 발생했습니다.</p>
<p>수업 환경 특성상 같은 네트워크에 20명이 동시에 실습을 진행하다 보니, <strong>listener가 본인의 talker 메시지뿐만 아니라 같은 반 수강생들의 메시지까지 모두 수신</strong>하는 현상이 나타났습니다.</p>
<p>캡쳐본을 보면 <code>Hello World: 88</code>, <code>Hello World: 95</code> 등 본인이 퍼블리시하지 않은 번호들이 뒤섞여 수신되는 것을 확인할 수 있습니다.</p>
<p>ROS2는 기본적으로 같은 네트워크 내에서 <strong>DDS(Data Distribution Service)</strong> 를 통해 통신하며, <code>ROS_DOMAIN_ID</code>가 동일한 노드끼리는 서로의 토픽을 모두 수신할 수 있습니다. 기본값은 <code>0</code>으로 동일하기 때문에 발생한 문제입니다.</p>
<p>이후 실제 터틀봇을 사용할 때 본인의 터틀봇 신호만 정확히 수신하기 위해 개인별로 <code>ROS_DOMAIN_ID</code>를 설정해주었습니다.</p>
<pre><code class="language-bash">echo &quot;export ROS_DOMAIN_ID=5&quot; &gt;&gt; ~/.bashrc
source ~/.bashrc</code></pre>
<blockquote>
<p><code>ROS_DOMAIN_ID</code>는 0~101 사이의 정수 값을 사용할 수 있습니다. 수업에서는 각자의 번호에 맞게 설정했습니다. (예: 5번 → ID=5)</p>
</blockquote>
<p>설정 후 동일한 talker-listener 예제를 재실행하면, 본인의 메시지만 수신되는 것을 확인할 수 있습니다.</p>
<blockquote>
<p>SBC(라즈베리파이)와 PC 양쪽 모두 동일한 <code>ROS_DOMAIN_ID</code>로 설정해야 통신이 정상적으로 이루어집니다.</p>
</blockquote>
<h3 id="6-1-ros_localhost_only-설정">6-1. ROS_LOCALHOST_ONLY 설정</h3>
<p><code>ROS_DOMAIN_ID</code>와 유사한 목적으로 사용할 수 있는 환경 변수로 <code>ROS_LOCALHOST_ONLY</code>가 있습니다.</p>
<p>이 변수를 <code>1</code>로 설정하면 <strong>ROS2 통신을 localhost로만 제한</strong>할 수 있습니다. 즉, 같은 네트워크에 연결된 다른 컴퓨터에서는 본인의 토픽, 서비스, 액션이 보이지 않게 됩니다.</p>
<pre><code class="language-bash">echo &quot;export ROS_LOCALHOST_ONLY=1&quot; &gt;&gt; ~/.bashrc
source ~/.bashrc</code></pre>
<blockquote>
<p><strong>주의:</strong> <code>ROS_LOCALHOST_ONLY=1</code>을 설정하면 같은 PC 내의 노드끼리만 통신이 가능합니다. 라즈베리파이(SBC)와 PC 간 통신이 필요한 경우에는 이 설정을 사용하지 않아야 합니다. 수업에서는 <code>ROS_DOMAIN_ID</code>만으로 충분했기 때문에 <code>ROS_LOCALHOST_ONLY</code>는 참고 수준으로만 확인했습니다.</p>
</blockquote>