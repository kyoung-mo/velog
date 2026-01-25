<h3 id="fndflexible-numeric-display">FND(Flexible Numeric Display)</h3>
<p>7개의 LED 막대를 조합하여 숫자를 표시하는 표시 장치</p>
<hr />
<h3 id="데이터시트">데이터시트</h3>
<p><a href="https://file.notion.so/f/f/6d8dfb15-0001-489c-860f-715cf05a57d7/ae6a49b6-e262-4ac8-abad-67359cf3f5c3/FND_x1.pdf?table=block&amp;id=2e6c5962-3e61-8175-a9de-eca95f0736e1&amp;spaceId=6d8dfb15-0001-489c-860f-715cf05a57d7&amp;expirationTimestamp=1768608000000&amp;signature=UEB_zt2XHl4vXHvwJDetZgUGuBKfSWWGPXw2Lg0hP1Y&amp;downloadName=FND+x1.pdf">FND x1.pdf</a></p>
<p><a href="https://file.notion.so/f/f/6d8dfb15-0001-489c-860f-715cf05a57d7/d3cb5539-dc02-4a9c-8f9a-a7ee59c54063/FND_x4.pdf?table=block&amp;id=2e6c5962-3e61-810e-bfd1-c36232d01bf3&amp;spaceId=6d8dfb15-0001-489c-860f-715cf05a57d7&amp;expirationTimestamp=1768608000000&amp;signature=mnfkFE45wa5isH_9jZTzH4x0Zqa11Ft72wZMW-N1hd8&amp;downloadName=FND+x4.pdf">FND x4.pdf</a></p>
<hr />
<h3 id="fnd-x1-회로도-연결도">FND x1 회로도, 연결도</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0da0bd94-4f49-45de-8cc4-d9e02e17ca95/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/d7b5745f-7cfd-490d-b516-5a0ae634c9b6/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/7f4cb322-17e6-4f5a-9eac-7899b94bada1/image.png" /></p>
<ul>
<li>현재 사용하는 소자는 Common Cathode</li>
<li>점 (dp)가 오른쪽 아래에 위치하도록 연결</li>
<li>1<del>5번 핀, 6</del>10번 핀이 한 라인에 연결되어 
★ 쇼트되지 않도록 주의 ★</li>
</ul>
<hr />
<h3 id="fnd-x4-회로도-연결도">FND x4 회로도, 연결도</h3>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/227e5c4c-794f-4c1c-8ec9-a006657b8678/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/0ceb5384-f74a-4b04-95b6-18a8f6b8117c/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/901a0246-4703-426f-9801-e170dcd60e38/image.png" /></p>
<ul>
<li>좌측 하단이 1번, 좌측 상단이 12번</li>
<li>★ 쇼트 주의</li>
</ul>
<h3 id="fnd-x1-기본-예제">FND x1 기본 예제</h3>
<pre><code class="language-c">int a = 5;
int b = 6;
int c = A2;
int d = A4;
int e = A5;
int f = 3;
int g = 2;
int p = A1;

//Set DIG1
int d1 = A3;

int val = 0;

#define _0 { HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, LOW}
#define _1 { LOW, HIGH, HIGH, LOW, LOW, LOW, LOW}
#define _2 { HIGH, HIGH, LOW, HIGH, HIGH, LOW, HIGH}
#define _3 { HIGH, HIGH, HIGH, HIGH, LOW, LOW, HIGH}
#define _4 { LOW, HIGH, HIGH, LOW, LOW, HIGH, HIGH}
#define _5 { HIGH, LOW, HIGH, HIGH, LOW, HIGH, HIGH}
#define _6 { HIGH, LOW, HIGH, HIGH, HIGH, HIGH, HIGH}
#define _7 { HIGH, HIGH, HIGH, LOW, LOW, LOW, LOW}
#define _8 { HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH}
#define _9 { HIGH, HIGH, HIGH, HIGH, LOW, HIGH, HIGH}
int num_bit[10][7] = { _0, _1, _2, _3, _4, _5, _6, _7, _8, _9 };

void pickNumber (int n);

void setup()
{
 Serial.begin(9600);

 pinMode(d1, OUTPUT);
 digitalWrite(d1, LOW);

 pinMode(a, OUTPUT);
 pinMode(b, OUTPUT);
 pinMode(c, OUTPUT);
 pinMode(d, OUTPUT);
 pinMode(e, OUTPUT);
 pinMode(f, OUTPUT);
 pinMode(g, OUTPUT);

 pinMode(p, OUTPUT);
}

void loop()
{
 val = (millis() / 1000) % 10;  //

 if (val &gt;= 0)
 {
     pickNumber(val);
 }
} 

void pickNumber(int n) 
{
 digitalWrite(a, num_bit[n][0]);
 digitalWrite(b, num_bit[n][1]);
 digitalWrite(c, num_bit[n][2]);
 digitalWrite(d, num_bit[n][3]);
 digitalWrite(e, num_bit[n][4]);
 digitalWrite(f, num_bit[n][5]);
 digitalWrite(g, num_bit[n][6]);
}

void dpoint() //Light the decimal point
{
 digitalWrite(p, HIGH);
}</code></pre>
<h3 id="fnd-x4-기본-예제">FND x4 기본 예제</h3>
<pre><code class="language-c">int a = 3;
int b = 7;
int c = A2;
int d = A4;
int e = A5;
int f = 4;
int g = A1;
int p = A3;

//Set DIG1, DIG2, DIG3, DIG4
int d1 = 2; //Thousand
int d2 = 5; //Hundred
int d3 = 6; //Ten
int d4 = A0;//One

int val4 = 0;  // DIG1 용 변수
int val3 = 0;  // DIG2 용 변수
int val2 = 0;  // DIG3 용 변수
int val1 = 0;  // DIG4 용 변수

const int DELAY = 1000;  // led display delay
int val = 0;

int digitpin[5] = { -1, d4, d3, d2, d1 };

#define _0 {    HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, LOW}
#define _1 {    LOW, HIGH, HIGH, LOW, LOW, LOW, LOW}
#define _2 {    HIGH, HIGH, LOW, HIGH, HIGH, LOW, HIGH}
#define _3 {    HIGH, HIGH, HIGH, HIGH, LOW, LOW, HIGH}
#define _4 {    LOW, HIGH, HIGH, LOW, LOW, HIGH, HIGH}
#define _5 {    HIGH, LOW, HIGH, HIGH, LOW, HIGH, HIGH}
#define _6 {    HIGH, LOW, HIGH, HIGH, HIGH, HIGH, HIGH}
#define _7 {    HIGH, HIGH, HIGH, LOW, LOW, LOW, LOW}
#define _8 {    HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH}
#define _9 {    HIGH, HIGH, HIGH, HIGH, LOW, HIGH, HIGH}
int num_bit[10][7] = { _0, _1, _2, _3, _4, _5, _6, _7, _8, _9 };

void pickNumber(int n) ;
void pickDigit(int x);
void clearLEDs();
void dpoint() ;

void setup()
{
    Serial.begin(9600);

    pinMode(d1, OUTPUT);
    pinMode(d2, OUTPUT);
    pinMode(d3, OUTPUT);
    pinMode(d4, OUTPUT);

    pinMode(a, OUTPUT);
    pinMode(b, OUTPUT);
    pinMode(c, OUTPUT);
    pinMode(d, OUTPUT);
    pinMode(e, OUTPUT);
    pinMode(f, OUTPUT);
    pinMode(g, OUTPUT);

    pinMode(p, OUTPUT);
}

void loop()
{
    val = millis() / 1000;

    val4 = (val / 1000) % 10;
    val3 = (val / 100) % 10;
    val2 = (val / 10) % 10;
    val1 = val % 10;

    if (val &gt;= 1000)
    {
        clearLEDs();
        pickDigit(4);
        pickNumber(val4);
        delayMicroseconds(DELAY);
    }

    if (val &gt;= 100)
    {
        clearLEDs();
        pickDigit(3);
        pickNumber(val3);
        delayMicroseconds(DELAY);
    }

    if (val &gt;= 10)
    {
        clearLEDs();
        pickDigit(2);
        pickNumber(val2);
        delayMicroseconds(DELAY);
    }

    if (val &gt;= 0)
    {
        clearLEDs();
        pickDigit(1);
        pickNumber(val1);
        delayMicroseconds(DELAY);
    }
}

void pickDigit(int x)
{
    digitalWrite(d1, HIGH);
    digitalWrite(d2, HIGH);
    digitalWrite(d3, HIGH);
    digitalWrite(d4, HIGH);

    digitalWrite(digitpin[x], LOW);
}

void pickNumber(int n) 
{
    digitalWrite(a, num_bit[n][0]);
    digitalWrite(b, num_bit[n][1]);
    digitalWrite(c, num_bit[n][2]);
    digitalWrite(d, num_bit[n][3]);
    digitalWrite(e, num_bit[n][4]);
    digitalWrite(f, num_bit[n][5]);
    digitalWrite(g, num_bit[n][6]);
}

void clearLEDs()
{
    digitalWrite(a, LOW);
    digitalWrite(b, LOW);
    digitalWrite(c, LOW);
    digitalWrite(d, LOW);
    digitalWrite(e, LOW);
    digitalWrite(f, LOW);
    digitalWrite(g, LOW);

    digitalWrite(p, LOW);
}

void dpoint() //Light the decimal point
{
    digitalWrite(p, HIGH);
}</code></pre>
<h3 id="응용-예제">응용 예제</h3>
<p>리모콘으로 누른 버튼의 숫자를 FND에 나타내기</p>
<hr />
<p>리모컨</p>
<pre><code class="language-c"></code></pre>
<hr />