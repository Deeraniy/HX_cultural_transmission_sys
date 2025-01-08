import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import json
from django.http import JsonResponse

def preview(request):
  def generate_predictions_with_curve_fit(data, steps=5, degree=3):
      
      # 将输入数据转换为合适的格式
      data = np.array(data)
      X = np.arange(len(data)).reshape(-1, 1)
      y = data

      # 创建多项式特征和线性回归模型
      poly = PolynomialFeatures(degree=degree)
      X_poly = poly.fit_transform(X)
      model = LinearRegression()
      model.fit(X_poly, y)

      # 生成未来点的多项式特征
      future_X = np.arange(len(data), len(data) + steps).reshape(-1, 1)
      future_X_poly = poly.transform(future_X)
      
      # 预测未来值
      predictions = model.predict(future_X_poly)

      return predictions
  

  
    # 处理结果
  
  # 示例输入数组
  body=json.loads(request.body)
  data=body.get('data')
  steps=body.get('steps',5)
  degree=body.get('degree',4)

  # 预测未来5步的数值，并指定多项式的阶数
  predictions = generate_predictions_with_curve_fit(data, steps, degree)
  results = {'predictions': predictions.tolist()}
  return JsonResponse(results, safe=False)
