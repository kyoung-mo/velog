<p>지도학습의 모델 중 하나인 분류 모델에 대해 정리해보겠습니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/783f1d15-d5c7-4798-8ef0-f34f55fb05fa/image.png" /></p>
<h2 id="목차">목차</h2>
<ul>
<li><a href="https://api.velog.io/rss/@mommers#%EB%B6%84%EB%A5%98-%EB%AA%A8%EB%8D%B8%EC%9D%B4%EB%9E%80">분류 모델이란?</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%8C%80%ED%91%9C-%EB%B6%84%EB%A5%98-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98">대표 분류 알고리즘</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%B6%84%EB%A5%98-%EB%AA%A8%EB%8D%B8-%EC%8B%A4%EC%8A%B5--%ED%8E%AD%EA%B7%84-%EC%84%B1%EB%B3%84-%EC%98%88%EC%B8%A1">분류 모델 실습 — 펭귄 성별 예측</a></li>
</ul>
<hr />
<h2 id="분류-모델이란">분류 모델이란?</h2>
<p>분류(Classification)는 입력 데이터를 미리 정해진 범주(클래스) 중 하나로 구분하는 작업입니다. 예측 결과가 <strong>이산적인 값(범주)</strong>이라는 점에서 연속적인 수치를 예측하는 회귀와 구분됩니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5f724fdb-fd6a-4490-9f53-402391e9b0a7/image.png" /></p>
<p>결과가 두 가지인 경우를 <strong>이진 분류(Binary Classification)</strong>, 세 가지 이상인 경우를 <strong>다중 분류(Multi-class Classification)</strong> 라고 합니다.</p>
<table>
<thead>
<tr>
<th>구분</th>
<th>예시</th>
</tr>
</thead>
<tbody><tr>
<td>이진 분류</td>
<td>스팸 메일 여부, 불량품 여부, 환자의 질병 유무</td>
</tr>
<tr>
<td>다중 분류</td>
<td>펭귄 종 분류, 손글씨 숫자 인식(0~9), 뉴스 카테고리 분류</td>
</tr>
</tbody></table>
<hr />
<h2 id="대표-분류-알고리즘">대표 분류 알고리즘</h2>
<h3 id="k-최근접-이웃-knn-k-nearest-neighbors">K-최근접 이웃 (KNN, K-Nearest Neighbors)</h3>
<p>예측 대상 데이터와 가장 가까운 K개의 이웃 데이터를 찾아, 그 중 가장 많은 클래스로 분류하는 알고리즘입니다. 거리가 가까울수록 특성이 비슷하다는 가정에 기반합니다.</p>
<p>K 값을 어떻게 설정하느냐에 따라 성능이 크게 달라집니다. K가 너무 작으면 과적합, K가 너무 크면 과소적합이 발생합니다.</p>
<blockquote>
<p>K-NN에서 가장 중요한 것은 <strong>K 수를 적절하게 정하는 것</strong>입니다.</p>
</blockquote>
<pre><code class="language-python">from sklearn.neighbors import KNeighborsClassifier</code></pre>
<h3 id="결정-트리-decision-tree">결정 트리 (Decision Tree)</h3>
<p>데이터를 분할하는 규칙을 트리 형태로 학습하는 알고리즘입니다. 각 분기점에서 조건에 따라 데이터를 나누며, 마지막 리프 노드에서 클래스를 결정합니다. 구조를 시각화할 수 있어 결과 해석이 쉽지만, 과적합이 발생하기 쉽습니다.</p>
<pre><code class="language-python">from sklearn.tree import DecisionTreeClassifier</code></pre>
<h3 id="랜덤-포레스트-random-forest">랜덤 포레스트 (Random Forest)</h3>
<p>여러 개의 결정 트리를 만들어 각각의 예측 결과를 투표(Voting)로 종합하는 앙상블 알고리즘입니다. 단일 트리보다 높은 정확도와 과적합 방지 효과를 가집니다.</p>
<pre><code class="language-python">from sklearn.ensemble import RandomForestClassifier</code></pre>
<hr />
<h2 id="분류-모델-실습--펭귄-성별-예측">분류 모델 실습 — 펭귄 성별 예측</h2>
<p>펭귄의 신체 특성 데이터를 이용해 성별을 분류하는 실습입니다. KNN 알고리즘을 사용합니다.</p>
<p><strong>사용 데이터</strong>: <code>penguins_size.csv</code></p>
<table>
<thead>
<tr>
<th>컬럼명</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td>species</td>
<td>펭귄의 종</td>
</tr>
<tr>
<td>island</td>
<td>데이터 측정 섬</td>
</tr>
<tr>
<td>culmen_length</td>
<td>부리 길이 (mm)</td>
</tr>
<tr>
<td>culmen_depth</td>
<td>부리 깊이 (mm)</td>
</tr>
<tr>
<td>flipper_length</td>
<td>지느러미 길이 (mm)</td>
</tr>
<tr>
<td>body_mass</td>
<td>무게 (g)</td>
</tr>
<tr>
<td>sex</td>
<td>성별 (타겟)</td>
</tr>
</tbody></table>
<hr />
<h3 id="데이터-준비">데이터 준비</h3>
<pre><code class="language-python">import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

df = pd.read_csv('penguins_size.csv')
df.head()</code></pre>
<p>데이터를 불러온 후 <code>info()</code>로 전체 구조와 결측치 여부를 파악합니다.</p>
<pre><code class="language-python">df.info()</code></pre>
<p>타겟 컬럼인 <code>sex</code>의 클래스 분포를 확인합니다. 클래스 불균형이 있으면 평가 지표 선택 시 주의가 필요합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/2be61349-ae24-48b6-9a62-a227da6b2064/image.png" /></p>
<pre><code class="language-python">df['sex'].value_counts()</code></pre>
<hr />
<h3 id="데이터-전처리">데이터 전처리</h3>
<p><strong>결측치 처리</strong></p>
<p>결측치가 있으면 모델 학습 시 오류가 발생하므로 먼저 확인하고 제거합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5d6e1aef-0652-4379-aa20-8f0df6b3ad18/image.png" /></p>
<pre><code class="language-python"># 결측치 확인
df.isnull().sum()

# 결측치 삭제
df = df.dropna()

# 삭제 후 확인
df.isnull().sum()</code></pre>
<p><strong>레이블 인코딩</strong></p>
<p>머신러닝 모델은 문자열을 직접 처리하지 못하므로 숫자로 변환합니다. <code>sex</code> 컬럼의 <code>MALE</code>을 1, <code>FEMALE</code>을 0으로 변환합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/ad8561a4-e7af-482c-b676-ed91dfd796a6/image.png" /></p>
<pre><code class="language-python">df['sex'] = df['sex'].map({'MALE': 1, 'FEMALE': 0})</code></pre>
<blockquote>
<p>문자형 데이터를 숫자로 변환하는 작업을 <strong>레이블 인코딩(Label Encoding)</strong> 이라고 합니다. 모델이 데이터를 이해할 수 있도록 하는 전처리의 핵심 단계입니다.</p>
</blockquote>
<hr />
<h3 id="특성과-타겟-분리">특성과 타겟 분리</h3>
<p>모델에 입력할 <strong>특성(Feature)</strong>과 예측할 <strong>타겟(Target)</strong>을 분리합니다.</p>
<ul>
<li>특성(X): <code>culmen_length</code>, <code>culmen_depth</code>, <code>flipper_length</code>, <code>body_mass</code></li>
<li>타겟(y): <code>sex</code></li>
</ul>
<pre><code class="language-python">X = df[['culmen_length', 'culmen_depth', 'flipper_length', 'body_mass']]
y = df['sex']</code></pre>
<hr />
<h3 id="학습테스트-데이터-분리">학습/테스트 데이터 분리</h3>
<p>전체 데이터를 학습용과 테스트용으로 분리합니다. 학습 데이터로 모델을 훈련하고, 테스트 데이터로 성능을 평가합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/60d46ecb-5bc9-448f-9e56-01d6cd6fa109/image.png" /></p>
<pre><code class="language-python">X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)</code></pre>
<blockquote>
<p><code>test_size=0.3</code>은 전체 데이터의 30%를 테스트 데이터로 사용한다는 의미입니다. 일반적으로 7:3 또는 8:2 비율을 많이 사용합니다. <code>random_state</code>는 데이터를 나누는 방식을 고정하여 실행할 때마다 동일한 결과를 얻기 위해 설정합니다.</p>
</blockquote>
<hr />
<h3 id="모델-생성-및-학습">모델 생성 및 학습</h3>
<p>필요한 라이브러리를 가져온 뒤, KNN 모델 객체를 생성하고 학습 데이터로 학습합니다.</p>
<pre><code class="language-python">from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report

# 모델 객체 생성
model_knn = KNeighborsClassifier()

# 모델 학습
model_knn.fit(X_train, y_train)</code></pre>
<hr />
<h3 id="모델-예측-및-평가">모델 예측 및 평가</h3>
<p>학습된 모델로 테스트 데이터를 예측하고 성능을 평가합니다.</p>
<p><strong>예측</strong></p>
<pre><code class="language-python">y_pred = model_knn.predict(X_test)</code></pre>
<p><strong>실제값과 예측값 비교</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/e734a73a-5b09-4edf-bf89-79e4c31fcd87/image.png" /></p>
<pre><code class="language-python">df_result = pd.DataFrame({'실제값': y_test.values, '예측값': y_pred})
df_result.head(10)</code></pre>
<p><strong>평가 지표 확인</strong></p>
<pre><code class="language-python">print(&quot;정확도: &quot;, accuracy_score(y_test, y_pred))
print(&quot;정밀도: &quot;, precision_score(y_test, y_pred))
print(&quot;재현율: &quot;, recall_score(y_test, y_pred))
print(&quot;F1-Score: &quot;,f1_score(y_test, y_pred))</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/65cd6a14-2537-455b-950b-adce246cd3f9/image.png" /></p>
<p><strong>혼동 행렬 확인</strong></p>
<pre><code class="language-python">print(confusion_matrix(y_test, y_pred))

# array([[38, 10],
#       [ 7, 45]])</code></pre>
<p><strong>classification_report로 전체 지표 한 번에 확인</strong></p>
<pre><code class="language-python">print(classification_report(y_test, y_pred))</code></pre>
<p><code>classification_report</code>는 정확도, 정밀도, 재현율, F1 Score를 클래스별로 한 번에 출력해 줍니다. 분류 모델 평가 시 가장 유용하게 사용되는 함수입니다.</p>
<hr />
<p>전체 분류 모델 실습의 흐름을 정리하면 다음과 같습니다.</p>
<pre><code>데이터 로드 → 결측치 처리 → 레이블 인코딩 → 특성/타겟 분리
→ 학습/테스트 분리 → 모델 생성 → 학습(fit) → 예측(predict) → 평가</code></pre><blockquote>
<p>평가지표(혼동 행렬, 정확도, 정밀도, 재현율, F1 Score)에 대한 자세한 설명은 이전 글 <a href="https://velog.io/@mommers/%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D-%EB%AA%A8%EB%8D%B8-%ED%8F%89%EA%B0%80%EC%A7%80%ED%91%9C"><strong>[머신러닝 모델 평가지표]</strong></a> 를 참고하시기 바랍니다.</p>
</blockquote>