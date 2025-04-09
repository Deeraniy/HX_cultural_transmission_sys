<template>
  <div class="huxiang-cuisine">
    <div class="section-header">
      <h2>湖湘美食文化</h2>
      <div class="decorative-line"></div>
    </div>

    <div class="cuisine-content">
      <div class="cuisine-text">
        <p class="cuisine-description">湖湘菜系,是中国"八大菜系"之一,以湖南菜肴为主的菜系。特点是原料广泛,口味多样,尤好辣椒,善用烟熏,风味特殊,浓香郁,菜型花色丰富。湖湘菜可以概括为"一菜一味,百菜百味",各有其独到的风味,菜式博大精深且富有创新精神。</p>

        <div class="cuisine-features">
          <div class="feature-item">
            <div class="feature-icon">🌶️</div>
            <div class="feature-info">
              <h3>重辣</h3>
              <p>湖湘菜以辣著称，无辣不欢。湖南境内遍植辣椒，厨师运用辣椒的手法巧妙多变。</p>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">🔥</div>
            <div class="feature-info">
              <h3>油重</h3>
              <p>湖湘菜讲究"猛火快炒"的烹饪方式和"香、辣、鲜、酥"的口味特点。</p>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">🍲</div>
            <div class="feature-info">
              <h3>色彩丰富</h3>
              <p>重视色彩搭配，菜品色泽鲜艳明快，往往红白分明、色彩斑斓。</p>
            </div>
          </div>
        </div>
      </div>

      <div class="cuisine-images">
        <div class="image-grid">
          <div class="image-item">
            <div class="cuisine-image-placeholder">
              <div class="placeholder-text">剁椒鱼头</div>
            </div>
          </div>
          <div class="image-item">
            <div class="cuisine-image-placeholder">
              <div class="placeholder-text">糖油粑粑</div>
            </div>
          </div>
          <div class="image-item">
            <div class="cuisine-image-placeholder">
              <div class="placeholder-text">臭豆腐</div>
            </div>
          </div>
          <div class="image-item">
            <div class="cuisine-image-placeholder">
              <div class="placeholder-text">口味虾</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="cuisine-footer">
      <div class="btn-wrapper">
        <router-link to="/food" class="explore-btn">
          <span>探索更多湖湘美食</span>
          <span class="arrow">→</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HuXiangCuisine'
}
</script>

<style scoped>
.huxiang-cuisine {
  padding: 40px 20px;
  background-color: #fff8f0;
  font-family: 'HelveticaNeue', '汇文明朝体', sans-serif;
}

.section-header {
  text-align: center;
  margin-bottom: 40px;
  position: relative;
}

.section-header h2 {
  font-size: 32px;
  color: #651e14;
  margin-bottom: 16px;
  font-family: '汇文明朝体', serif;
  font-weight: 600;
}

.decorative-line {
  width: 80px;
  height: 3px;
  background-color: #651e14;
  margin: 0 auto;
  position: relative;
}

.decorative-line:before, .decorative-line:after {
  content: '';
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #651e14;
  top: -2.5px;
}

.decorative-line:before {
  left: -5px;
}

.decorative-line:after {
  right: -5px;
}

.cuisine-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
}

.cuisine-text {
  flex: 1;
  min-width: 300px;
  padding-right: 30px;
}

.cuisine-description {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  margin-bottom: 30px;
  text-align: justify;
}

.cuisine-features {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 24px;
  margin-right: 15px;
  margin-top: 2px;
}

.feature-info h3 {
  font-size: 18px;
  color: #651e14;
  margin-bottom: 5px;
  font-family: '汇文明朝体', serif;
}

.feature-info p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

.cuisine-images {
  flex: 1;
  min-width: 300px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.image-item {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.image-item:hover {
  transform: scale(1.03);
}

.cuisine-image-placeholder {
  width: 100%;
  height: 180px;
  background: linear-gradient(135deg, #f8cda7, #e6a06f);
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-text {
  color: #651e14;
  font-weight: bold;
  font-size: 18px;
  text-align: center;
  font-family: '汇文明朝体', serif;
}

.cuisine-footer {
  margin-top: 50px;
  text-align: center;
}

.btn-wrapper {
  display: inline-block;
  position: relative;
  overflow: hidden;
  border-radius: 30px;
  box-shadow: 0 5px 15px rgba(101, 30, 20, 0.2);
}

.explore-btn {
  display: inline-flex;
  align-items: center;
  padding: 12px 30px;
  background-color: #651e14;
  color: white;
  text-decoration: none;
  border-radius: 30px;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.explore-btn:hover {
  background-color: #7a2f24;
  padding-right: 35px;
}

.arrow {
  opacity: 0;
  margin-left: 5px;
  transform: translateX(-10px);
  transition: all 0.3s ease;
}

.explore-btn:hover .arrow {
  opacity: 1;
  transform: translateX(0);
}

@media (max-width: 768px) {
  .cuisine-content {
    flex-direction: column;
  }
  
  .cuisine-text {
    padding-right: 0;
    margin-bottom: 30px;
  }
  
  .section-header h2 {
    font-size: 28px;
  }
  
  .image-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .cuisine-image-placeholder {
    height: 150px;
  }
}

@media (max-width: 480px) {
  .image-grid {
    grid-template-columns: 1fr;
  }
  
  .cuisine-image-placeholder {
    height: 200px;
  }
  
  .section-header h2 {
    font-size: 24px;
  }
  
  .explore-btn {
    padding: 10px 20px;
    font-size: 14px;
  }
}
</style> 