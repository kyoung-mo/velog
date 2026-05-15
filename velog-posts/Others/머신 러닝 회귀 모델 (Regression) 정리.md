<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/024982f7-8b15-4cfc-828a-27f6d15100ec/image.png" /></p>
<h2 id="목차">목차</h2>
<ul>
<li><a href="https://api.velog.io/rss/@mommers#%ED%9A%8C%EA%B7%80-%EB%AA%A8%EB%8D%B8%EC%9D%B4%EB%9E%80">회귀 모델이란?</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%8C%80%ED%91%9C-%ED%9A%8C%EA%B7%80-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98">대표 회귀 알고리즘</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%ED%9A%8C%EA%B7%80-%EB%AA%A8%EB%8D%B8-%EC%8B%A4%EC%8A%B5--%EB%B3%B4%ED%97%98%EB%A3%8C-%EC%98%88%EC%B8%A1">회귀 모델 실습 — 보험료 예측</a><ul>
<li><a href="https://api.velog.io/rss/@mommers#%EB%8D%B0%EC%9D%B4%ED%84%B0-%ED%83%90%EC%83%89-eda">데이터 탐색 (EDA)</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%A0%84%EC%B2%98%EB%A6%AC">데이터 전처리</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%ED%8A%B9%EC%84%B1%ED%83%80%EA%B2%9F-%EB%B6%84%EB%A6%AC-%EB%B0%8F-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EB%B6%84%ED%95%A0">특성/타겟 분리 및 데이터 분할</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EB%AA%A8%EB%8D%B8-%ED%95%99%EC%8A%B5-%EB%B0%8F-%ED%8F%89%EA%B0%80">모델 학습 및 평가</a></li>
<li><a href="https://api.velog.io/rss/@mommers#%EC%A4%91%EC%9A%94-%EB%B3%80%EC%88%98-%ED%99%95%EC%9D%B8">중요 변수 확인</a></li>
</ul>
</li>
</ul>
<hr />
<h2 id="회귀-모델이란">회귀 모델이란?</h2>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/b30bfc2b-15e9-459a-9f40-f36582e3220f/image.png" /></p>
<p>회귀(Regression)는 입력 변수(독립변수)와 출력 변수(종속변수) 사이의 관계를 학습하여 <strong>연속적인 수치</strong>를 예측하는 작업입니다.</p>
<ul>
<li><strong>독립변수</strong>: 다른 변수에 영향을 주는 원인에 해당하는 변수</li>
<li><strong>종속변수</strong>: 영향을 받는 변수, 예측하고자 하는 결괏값</li>
</ul>
<p>예를 들어 기온(독립변수)이 올라갈수록 아이스크림 판매량(종속변수)이 늘어나는 관계를 수식으로 표현하고, 새로운 기온 데이터가 들어왔을 때 판매량을 예측하는 것이 회귀 분석입니다.</p>
<blockquote>
<p>회귀의 목표는 예측값과 실제값의 차이(오차)를 최소화하는 최적의 함수를 찾는 것입니다.</p>
</blockquote>
<hr />
<h2 id="대표-회귀-알고리즘">대표 회귀 알고리즘</h2>
<h3 id="선형-회귀-linear-regression">선형 회귀 (Linear Regression)</h3>
<p>독립변수와 종속변수 사이의 <strong>선형 관계</strong>를 학습하는 가장 기본적인 회귀 모델입니다. 직관적이고 해석이 쉬우며 학습 속도가 빠릅니다. 단, 비선형 관계에는 취약하고 과적합이 발생하기 쉽습니다.</p>
<blockquote>
<p>선형 회귀:
  Loss = Σ(실제값 - 예측값)²</p>
</blockquote>
<p>피처가 적고 변수 간 다중공선성 문제가 없을 때 사용하면 좋습니다.</p>
<pre><code class="language-python">from sklearn.linear_model import LinearRegression</code></pre>
<h3 id="릿지-회귀-ridge">릿지 회귀 (Ridge)</h3>
<p>선형 회귀에 <strong>L2 정규화</strong>를 적용한 모델입니다. 회귀 계수에 패널티를 부여해 계수의 크기를 줄임으로써 과적합을 방지합니다. 모든 피처를 사용하되 계수의 크기를 조절합니다.</p>
<blockquote>
<p>릿지 회귀 Loss
  = Σ(실제값 - 예측값)² + α × Σ(계수²)
 = 잔차 제곱합 + L2 패널티 </p>
</blockquote>
<p>피처가 많고 과적합이 우려될 때 사용하면 좋습니다.</p>
<pre><code class="language-python">from sklearn.linear_model import Ridge</code></pre>
<h3 id="라쏘-회귀-lasso">라쏘 회귀 (Lasso)</h3>
<p>선형 회귀에 <strong>L1 정규화</strong>를 적용한 모델입니다. 일부 회귀 계수를 완전히 0으로 만들어 불필요한 변수를 자동으로 제거하는 <strong>변수 선택(Feature Selection)</strong> 기능을 가집니다. 단, 스케일에 민감하므로 정규화(Scaling)가 필수입니다.</p>
<blockquote>
<p>$$
최소화=∑(실제값−예측값)^2+λ×(∣a∣+∣b∣+∣c∣+...)
$$</p>
</blockquote>
<p>불필요한 변수를 자동으로 제거하고 싶을 때 사용하면 좋습니다.</p>
<pre><code class="language-python">from sklearn.linear_model import Lasso</code></pre>
<h3 id="랜덤-포레스트-회귀-random-forest-regressor">랜덤 포레스트 회귀 (Random Forest Regressor)</h3>
<p>여러 개의 결정 트리를 학습하고 각 트리의 예측값을 평균내어 최종 예측을 수행하는 앙상블 모델입니다. 높은 예측 정확도와 과적합 방지 효과가 있으며, 피처 중요도(Feature Importance)를 확인할 수 있어 어떤 변수가 예측에 영향을 미치는지 파악할 수 있습니다.</p>
<pre><code class="language-python">from sklearn.ensemble import RandomForestRegressor</code></pre>
<blockquote>
<p><strong>릿지 vs 라쏘</strong>: 릿지는 모든 피처의 계수를 작게 유지하고, 라쏘는 불필요한 피처의 계수를 아예 0으로 만듭니다. 중요한 피처가 소수라고 판단될 때는 라쏘, 모든 피처가 어느 정도 기여한다고 판단될 때는 릿지가 적합합니다.</p>
</blockquote>
<hr />
<h2 id="회귀-모델-실습--보험료-예측">회귀 모델 실습 — 보험료 예측</h2>
<p>고객 정보를 바탕으로 개인 의료 보험료를 예측하는 실습입니다. 여러 회귀 모델을 적용하고 성능을 비교합니다.</p>
<p><strong>사용 데이터</strong>: <code>insurance.csv</code></p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/c5a3202f-84f8-4d79-886c-c51fa0fd4704/image.png" /></p>
<hr />
<h3 id="데이터-탐색-eda">데이터 탐색 (EDA)</h3>
<p><strong>기본 라이브러리 및 데이터 로드</strong></p>
<pre><code class="language-python">import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('insurance.csv')
df.head()</code></pre>
<p><strong>기초 분석</strong></p>
<pre><code class="language-python">df.shape       # 데이터 크기
df.info()      # 컬럼별 정보 및 타입 확인
df.describe()  # 숫자 데이터 기초 통계
df.isnull().sum()  # 결측치 확인</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/1a84c4f2-30b0-427c-85f3-f0a0a4da9423/image.png" /></p>
<p><strong>데이터의 왜도/첨도 확인</strong></p>
<p>타겟 컬럼인 <code>charges</code>의 분포가 정규분포에서 얼마나 치우쳐 있는지 확인합니다.</p>
<pre><code class="language-python">from scipy.stats import kurtosis, skew

print(df['charges'].describe())
print(&quot;skew: &quot;, skew(df['charges']))      # 왜도
print(&quot;kurtosis: &quot;, kurtosis(df['charges']))  # 첨도</code></pre>
<p>왜도가 1.51로 오른쪽 꼬리가 긴 분포를 보입니다. 즉, 대부분의 보험료는 낮지만, 일부 고객은 매우 높은 보험료를 지불하는 구조입니다.</p>
<blockquote>
<p><strong>왜도(Skewness)</strong>: 분포가 얼마나 한쪽으로 치우쳐 있는지를 나타냅니다.
<strong>첨도(Kurtosis)</strong>: 분포의 꼬리 부분이 정규분포에 비해 얼마나 두꺼운지를 나타냅니다. 정규분포의 첨도는 0입니다.</p>
</blockquote>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/dfd3599b-1928-4bed-b797-3c86b106c4f4/image.png" />
<strong>이상치 탐지</strong></p>
<p>IQR(사분위 범위)을 기준으로 이상치를 식별합니다.</p>
<pre><code class="language-python">def outlier_detect(df):
    for i in df.describe().columns:
        Q1 = df.describe().at['25%', i]
        Q3 = df.describe().at['75%', i]
        IQR = Q3 - Q1
        LTV = Q1 - 1.5 * IQR  # 하한
        UTV = Q3 + 1.5 * IQR  # 상한
        x = np.array(df[i])
        p = [j for j in x if j &lt; LTV or j &gt; UTV]
        print(f'\n Outliers for Column: {i}, count: {len(p)}')

numeric_columns = df.select_dtypes(include=np.number).columns
outlier_detect(df[numeric_columns])</code></pre>
<p><strong>주요 시각화</strong></p>
<pre><code class="language-python"># 보험료 분포 확인
sns.distplot(df['charges'], kde=True, color='c')
plt.title('Distribution of Charges')
plt.show()

# 나이와 보험료의 관계
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
sns.scatterplot(x=df['age'], y=df['charges'], ax=axes[0])
axes[0].set_title('Age vs Charges')
sns.regplot(x=df['age'], y=df['charges'], ax=axes[1])
axes[1].set_title('Regression: Age vs Charges')
plt.show()

# 흡연 여부와 보험료의 관계
sns.swarmplot(x=df['smoker'], y=df['charges'], palette='Set1')
plt.show()</code></pre>
<p>시각화 결과, 흡연 여부가 보험료에 가장 큰 영향을 미치는 것을 확인할 수 있습니다. 흡연자의 보험료가 비흡연자에 비해 현저히 높으며, 보험료를 결정하는 핵심 요인으로 작용합니다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/mommers/post/5c535252-1d4a-430e-9777-6c10ee42f31d/image.png" /></p>
<pre><code class="language-python"># 상관계수 히트맵
plt.figure(figsize=(10, 5))
corr = df.select_dtypes(include=np.number).corr()
sns.heatmap(corr, vmin=-1, vmax=1, center=0, annot=True)
plt.show()</code></pre>
<hr />
<h3 id="데이터-전처리">데이터 전처리</h3>
<p><strong>컬럼명 수정 및 중복값 제거</strong></p>
<pre><code class="language-python"># sex 컬럼명을 gender로 변경
df.rename(columns={'sex': 'gender'}, inplace=True)

# 중복값 제거
df = df.drop_duplicates()</code></pre>
<p><strong>LabelEncoder를 활용한 카테고리 변환</strong></p>
<p>문자형 데이터를 머신러닝 모델이 처리할 수 있는 숫자로 변환합니다. <code>sklearn</code>의 <code>LabelEncoder</code>를 사용하면 여러 컬럼을 일관된 방식으로 변환할 수 있습니다.</p>
<pre><code class="language-python">from sklearn.preprocessing import LabelEncoder

# 카테고리 타입으로 변환
df[['gender', 'smoker', 'region']] = df[['gender', 'smoker', 'region']].astype('category')

# LabelEncoder로 숫자 변환
label = LabelEncoder()

label.fit(df.gender.drop_duplicates())
df.gender = label.transform(df.gender)

label.fit(df.smoker.drop_duplicates())
df.smoker = label.transform(df.smoker)

label.fit(df.region.drop_duplicates())
df.region = label.transform(df.region)</code></pre>
<blockquote>
<p>분류 실습에서는 <code>map()</code>으로 직접 값을 지정했지만, <code>LabelEncoder</code>를 사용하면 클래스가 많거나 값이 미리 정해지지 않은 경우에도 자동으로 숫자를 부여할 수 있습니다.</p>
</blockquote>
<hr />
<h3 id="특성타겟-분리-및-데이터-분할">특성/타겟 분리 및 데이터 분할</h3>
<pre><code class="language-python">from sklearn.model_selection import train_test_split

X = df.drop(['charges'], axis=1)
y = df['charges']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)</code></pre>
<hr />
<h3 id="모델-학습-및-평가">모델 학습 및 평가</h3>
<p><strong>선형 회귀 (Linear Regression)</strong></p>
<pre><code class="language-python">from sklearn.linear_model import LinearRegression
from sklearn import metrics

model_lr = LinearRegression()
model_lr.fit(x_train, y_train)

x_train_pred = model_lr.predict(x_train)
x_test_pred = model_lr.predict(x_test)

print('MSE train: %.3f, MSE test: %.3f' % (
    metrics.mean_squared_error(x_train_pred, y_train),
    metrics.mean_squared_error(x_test_pred, y_test)
))
print('R2 train: %.3f, R2 test: %.3f' % (
    metrics.r2_score(y_train, x_train_pred),
    metrics.r2_score(y_test, x_test_pred)
))</code></pre>
<p><strong>릿지 회귀 (Ridge)</strong></p>
<pre><code class="language-python">from sklearn.linear_model import Ridge

model_ridge = Ridge(alpha=0.5)
model_ridge.fit(x_train, y_train)
print(model_ridge.score(x_test, y_test))</code></pre>
<p><strong>라쏘 회귀 (Lasso)</strong></p>
<p>라쏘는 스케일에 민감하므로 <code>StandardScaler</code>로 정규화를 먼저 적용합니다.</p>
<pre><code class="language-python">from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

model_lasso = Lasso(alpha=0.2)
model_lasso.fit(x_train_scaled, y_train)
print(model_lasso.score(x_test_scaled, y_test))</code></pre>
<blockquote>
<p><code>fit_transform()</code>은 학습 데이터에만 사용하고, 테스트 데이터에는 <code>transform()</code>만 사용합니다. 테스트 데이터에 <code>fit_transform()</code>을 사용하면 데이터 누수(Data Leakage)가 발생합니다.</p>
</blockquote>
<p><strong>랜덤 포레스트 회귀 (Random Forest Regressor)</strong></p>
<pre><code class="language-python">from sklearn.ensemble import RandomForestRegressor

model_rfr = RandomForestRegressor(n_estimators=100, criterion='squared_error', random_state=1, n_jobs=-1)
model_rfr.fit(x_train, y_train)

x_train_pred = model_rfr.predict(x_train)
x_test_pred = model_rfr.predict(x_test)

print('MSE train: %.3f, MSE test: %.3f' % (
    metrics.mean_squared_error(x_train_pred, y_train),
    metrics.mean_squared_error(x_test_pred, y_test)
))
print('R2 train: %.3f, R2 test: %.3f' % (
    metrics.r2_score(y_train, x_train_pred),
    metrics.r2_score(y_test, x_test_pred)
))</code></pre>
<p><strong>예측값 vs 실제값 시각화</strong></p>
<pre><code class="language-python">plt.figure(figsize=(8, 6))
plt.scatter(x_train_pred, y_train - x_train_pred, c='grey', label='Train data', alpha=0.5)
plt.scatter(x_test_pred, y_test - x_test_pred, c='blue', label='Test data')
plt.axhline(y=0, color='r', linestyle='-')
plt.xlabel('Predicted values')
plt.ylabel('Residuals')
plt.title('Predicted vs Actual Values')
plt.legend()
plt.show()</code></pre>
<hr />
<hr />
<p>전체 회귀 모델 실습의 흐름을 정리하면 다음과 같습니다.</p>
<pre><code>데이터 로드 → EDA (왜도/첨도/이상치/시각화) → 전처리 (LabelEncoder)
→ 특성/타겟 분리 → 학습/테스트 분리 → 모델 학습 → 평가 (MSE, R2) → 피처 중요도 확인</code></pre><blockquote>
<p>평가지표(MAE, MSE)에 대한 자세한 설명은 이전 글 <strong>[머신러닝 모델 평가지표]</strong> 를 참고하시기 바랍니다.</p>
</blockquote>