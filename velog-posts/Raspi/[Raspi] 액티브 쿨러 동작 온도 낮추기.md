<p>라즈베리파이가 너무 뜨거워서 온도를 확인해봤다.
(rpi-connect &gt; screen sharing 이용)</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/282d2b5f-861d-479d-aab4-38899b532709/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3e55fda3-6280-41d6-b3a8-a6a8508de1be/image.png" /></p>
<p>두 개의 라즈베리 파이 모두 온도가 뜨거웠는데, 왜 쿨러가 동작을 안하지??? 라는 생각에 찾아보게 되었다.</p>
<hr />
<blockquote>
<p>참고) <code>rpi-connect on</code> 명령어 입력, 기기 추가해두면 라즈베리파이에 인터넷과 전원만 연결되어 있다면 외부에서 라즈베리파이에 <a href="https://connect.raspberrypi.com/devices">connect 사이트</a>를 이용해서 원격 접속이 가능하다.</p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/f09a1eb7-9036-4712-9da9-551992e345c5/image.png" /></p>
<ul>
<li>핫스팟 연결된 노트북으로 확인한 화면</li>
</ul>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/a725c89c-d1db-4eab-be76-8e87e28fd0bc/image.png" /></p>
<p><a href="https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#fan-cases">Raspberry pi Documentation</a>에 따르면 Raspberry Pi 5의 온도가 50도 아래일때는 팬이 동작하지 않는다고 한다.</p>
<ul>
<li>50도가 넘었을 때 : 30% speed로 회전</li>
<li>60도가 넘었을 때 : 50% speed로 회전</li>
<li>67.5도가 넘었을 때 : 70% speed로 회전</li>
<li>75도가 넘었을 때 : 1000% speed로 회전</li>
</ul>
<p>팬 설정은 <a href="https://www.raspberrypi.com/documentation/computers/config_txt.html#what-is-config-txt">config.txt</a>에서 변경이 가능하다.</p>
<hr />
<h3 id="configtxt란">config.txt란?</h3>
<p>PC의 BIOS 대신에(?) 라즈베리파이의 디바이스는 <code>config.txt</code> 라고 불리는 configuration file을 사용한다.</p>
<p>GPU는 Arm CPU와 Linux 초기 설정?시 config.txt를 읽는다. 라즈베리파이 OS는 이 파일을 <code>/boot/firmware/</code>에 위치한 boot partition으로 본다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/3eae0a6a-d22f-4ba5-9c20-40070aa9d83d/image.png" /></p>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/945fb3b6-6add-4e25-8269-3586ee4a2364/image.png" /></p>
<p>초기에 UART 통신을 위해 [all]에 <code>enable_uart=1</code> 을 추가한적이 있다.</p>
<p>이건 imager를 통해 OS 구우면서 윈도우 환경에서 수정했었는데, 여기서도 수정이 가능하다.</p>
<hr />
<p>다시 돌아와서, <a href="https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README">raspberrypi_firmware.github</a>를 참고했을때, ReadME.md 파일에서 <code>cool</code> 을 검색하면 아래와 같은 내용들이 나온다.</p>
<pre><code>Name:   &lt;The base DTB&gt;
Info:   Configures the base Raspberry Pi hardware
Load:   &lt;loaded automatically&gt;
Params:

...

        cooling_fan             Enables the Pi 5 cooling fan (enabled
                                automatically by the firmware)

...

        fan_temp0               Temperature threshold (in millicelcius) for
                                1st cooling level (default 50000). Pi5 only.
        fan_temp0_hyst          Temperature hysteresis (in millicelcius) for
                                1st cooling level (default 5000). Pi5 only.
        fan_temp0_speed         Fan PWM setting for 1st cooling level (0-255,
                                default 75). Pi5 only.
        fan_temp1               Temperature threshold (in millicelcius) for
                                2nd cooling level (default 60000). Pi5 only.
        fan_temp1_hyst          Temperature hysteresis (in millicelcius) for
                                2nd cooling level (default 5000). Pi5 only.
        fan_temp1_speed         Fan PWM setting for 2nd cooling level (0-255,
                                default 125). Pi5 only.
        fan_temp2               Temperature threshold (in millicelcius) for
                                3rd cooling level (default 67500). Pi5 only.
        fan_temp2_hyst          Temperature hysteresis (in millicelcius) for
                                3rd cooling level (default 5000). Pi5 only.
        fan_temp2_speed         Fan PWM setting for 3rd cooling level (0-255,
                                default 175). Pi5 only.
        fan_temp3               Temperature threshold (in millicelcius) for
                                4th cooling level (default 75000). Pi5 only.
        fan_temp3_hyst          Temperature hysteresis (in millicelcius) for
                                4th cooling level (default 5000). Pi5 only.
        fan_temp3_speed         Fan PWM setting for 4th cooling level (0-255,
                                default 250). Pi5 only.
</code></pre><ul>
<li><p>fan_temp0에서 threshold 값은 50000 millicelcius로 잡혀있다.</p>
</li>
<li><p>fan_temp0_speed에서는 cooling level이 0~255이고, 기본 값은 75로 동작한다고 한다.
<img alt="" src="https://velog.velcdn.com/images/mommers/post/f533971d-6dc2-47f7-afff-4dbcebd2f084/image.png" />
대충 30에 가까운 값으로, 아까 Document의 설명과 일치</p>
</li>
<li><p>2nd는 60000 millicelcius에서 0~255 중 125로 동작(거의 50%)</p>
</li>
<li><p>3rd는 67500 millicelcius에서 0~255 중 175로 동작(거의 75%)</p>
</li>
<li><p>4th는 75000 millicelcius에서 0~255 중 250으로 동작(거의 100%)</p>
</li>
</ul>
<hr />
<p>config.txt에서 설정하는 법도 나와있다. 약 1525줄에</p>
<pre><code>Name:   gpio-fan
Info:   Configure a GPIO pin to control a cooling fan.
Load:   dtoverlay=gpio-fan,&lt;param&gt;=&lt;val&gt;
Params: gpiopin                 GPIO used to control the fan (default 12)
        temp                    Temperature at which the fan switches on, in
                                millicelcius (default 55000)
        hyst                    Temperature delta (in millicelcius) below
                                temp at which the fan will drop to minrpm
                                (default 10000)</code></pre><p>GPIO핀을 이용하여 colling fan을 control하기 위해서 Params 값과, Load는 어떤 식으로 config.txt에 작성해야 하는지에 대한 내용이다.</p>
<ul>
<li>Load : <code>dtoverlay=gpio-fan,&lt;param&gt;=&lt;val&gt;</code></li>
<li>temp Params에는 default 55000인데, in millicelcius로 잡혀있고, 팬 스위치가 켜지는 시점의 온도를 정할 수 있는 것 같다.</li>
<li>hyst는 동작 시간? 그런 느낌이다.</li>
</ul>
<p>약 4190 줄에도 비슷한 내용이 나와있다.</p>
<pre><code>Name:   pwm-gpio-fan
Info:   Configure a GPIO connected PWM cooling fan controlled by the
        software-based GPIO PWM kernel module
Load:   dtoverlay=pwm-gpio-fan,&lt;param&gt;=&lt;val&gt;
Params: fan_gpio                BCM number of the pin driving the fan,
                                default 18 (GPIO 18)
        fan_temp0               CPU temperature at which fan is started with
                                low speed in millicelsius,
                                default 55000 (55 °C)
        fan_temp1               CPU temperature at which fan is switched
                                to medium speed in millicelsius,
                                default 60000 (60 °C)
        fan_temp2               CPU temperature at which fan is switched
                                to high speed in millicelsius,
                                default 67500 (67.5 °C)
        fan_temp3               CPU temperature at which fan is switched
                                to max speed in millicelsius,
                                default 75000 (75 °C)
        fan_temp0_hyst          Temperature hysteris at which fan is stopped
                                in millicelsius,default 5000 (resulting
                                in 50 °C)
        fan_temp1_hyst          Temperature hysteris at which fan is switched
                                back to low speed in millicelsius,
                                default 5000 (resulting in 55 °C)
        fan_temp2_hyst          Temperature hysteris at which fan is switched
                                back to medium speed in millicelsius,
                                default 5000 (resulting in 62.5 °C)
        fan_temp3_hyst          Temperature hysteris at which fan is switched
                                back to high speed in millicelsius,
                                default 5000 (resulting in 70 °C)
        fan_temp0_speed         Fan speed for low cooling state in range
                                0 to 255, default 114 (45% PWM duty cycle)
        fan_temp1_speed         Fan speed for medium cooling state in range
                                0 to 255, default 152 (60% PWM duty cycle)
        fan_temp2_speed         Fan speed for high cooling state in range
                                0 to 255, default 204 (80% PWM duty cycle)
        fan_temp3_speed         Fan speed for max cooling state in range
                                0 to 255, default 255 (100% PWM duty cycle)</code></pre><p>그냥 gpio-fan이냐 pwm-gpio-fan이냐 차이이다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/fc1d1d76-52c6-411b-95ec-026e0567f42a/image.png" /></p>
<pre><code class="language-bash">dtoverlay=rpi-5-active-cooler
dtparam=fan_temp1=45000,fan_speed1=30
dtparam=fan_temp1=55000,fan_speed1=50
dtparam=fan_temp3=65000,fan_speed3=100 </code></pre>
<p>파일 하단에 이렇게 작성해주고, 저장, <code>sudo reboot</code></p>
<p>이렇게 기본 값을 바꿔줄 수 있다.</p>