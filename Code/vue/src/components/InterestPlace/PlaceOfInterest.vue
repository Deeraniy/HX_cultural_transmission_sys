<template>
  <el-main>
    <div class="hunan-tourist-attractions">
      <div class="map-info-container">
        <!-- 地图区域 -->
        <div class="map-box">
          <div style="width:100%;height:100%;" ref="chartsDOM"></div>
        </div>

        <!-- 地理位置名称显示框 -->
        <div class="location-box">
          <!-- 城市选择下拉框 -->
          <el-select v-model="selectedCity" placeholder="选择城市" @change="onCitySelect" class="city-select">
            <el-option
                v-for="city in cityList"
                :key="city"
                :label="city"
                :value="city">
            </el-option>
          </el-select>
          <div>
            <h3 style="text-align: center;font-family: 'ChillKaiShu',serif;">地理位置</h3>
            <div v-if="selectedCityInfoLocal" class="city-info">
              <div class="image-container">
                <img :src="selectedCityInfoLocal.image" alt="城市图片" class="city-image" />
                <img :src="getImageUrl(selectedCityInfoLocal.wordCloudImage)" alt="词云图片" class="wordcloud-image" />
              </div>
              <div class="description-box">
                <p>{{ selectedCityInfoLocal.description }}</p>
              </div>
            </div>
            <div v-else class="city-name-display" style="display: flex; justify-content: center; align-items: center; height: 100%;">
              <el-text style="color: darkgray;font-family: 'ChillKaiShu',serif;">请点击地图中的城市以显示其名称</el-text>
            </div>
          </div>


        </div>
      </div>
      <div class="attraction-card-box">
        <!-- 动态展示当前选中的城市景点 -->
        <div class="attractions-container">
          <div class="attraction-card" @click="goToPlaceDetail(attraction.name)" v-for="attraction in filteredAttractions" :key="attraction.name" >
            <img :src="attraction.image" :alt="attraction.name" class="attraction-image" />
            <div class="attraction-details">
              <h3>
                {{ attraction.name }}
                <span class="fancy-name">({{ attraction.name }})</span>
              </h3>
              <a :href="attraction.description" target="_blank" rel="noopener noreferrer">{{ attraction.description }}</a>
            </div>
          </div>
        </div>
      </div>

      <!-- 搜索功能 -->
      <div class="search-container">
        <input v-model="searchQuery" type="text" placeholder="搜索湖南名胜古迹" />
        <button @click="searchAttractions">搜索</button>
      </div>
    </div>


  </el-main>
</template>

<script lang="ts" setup>
import {computed, onMounted, ref} from 'vue';
import * as echarts from 'echarts';
import hunanMapData from '@/json/湖南省.json';
import cityInfoDataLocal from '@/assets/cityInfo.json'; // 导入城市信息
//import interestDataLocal from '@/json/interests.json'; // 导入景点信息
import SpotsAPI  from "@/api/spot";
import CityAPI from "@/api/city";
import CloudAPI from "@/api/cloud";
import SentimentAPI from "@/api/sentiment";
import {error} from "echarts/types/src/util/log";
import Sentiment from "@/api/sentiment";
import router from '@/router'
const chartsDOM = ref<HTMLElement | null>(null);
const searchQuery = ref<string>('');
const selectedCity = ref<string>(''); // 保存选中的城市名称
const selectedCityInfo = ref<any | null>(null); // 保存选中城市的详细信息
const selectedCityInfoLocal = ref<any | null>(null);
const selectedCityWordCloudImage = ref<string | null>(null);
const cityList = ref<string[]>([
  '张家界市', '常德市', '岳阳市', '益阳市', '长沙市', '湘潭市', '株洲市',
  '衡阳市', '郴州市', '永州市', '邵阳市', '娄底市', '怀化市', '湘西土家族苗族自治州'
]);
const interestData = ref<any>(null);
const cityInfoData = ref<any>(null);
let myChart: any;

const attractions = ref([]); // 保存当前选中的城市的所有景点

// 从 interest.json 中加载数据并更新 attractions
const loadAttractions = (cityName: string) => {

  // 确保 cityInfoData 和 interestData 已加载且是数组
  if (!cityInfoData.value || !Array.isArray(cityInfoData.value)) {
    console.warn("城市数据未加载或格式错误");
    return;
  }
  if (!interestData.value || !Array.isArray(interestData.value)) {
    console.warn("景点数据未加载或格式错误");
    return;
  }

  console.log(cityInfoData.value);
  console.log("当前城市的名称:", cityName);

  // 找到当前城市的 city_id
  const city = cityInfoData.value.find((c: any) => c.city_name === cityName);
  console.log("当前城市的城市ID:", city);

  if (city) {
    const cityId = city.city_id;

    // 根据 city_id 筛选景点数据
    attractions.value = interestData.value
        .filter((spot: any) => spot.city_id === cityId)
        .map((spot: any) => ({
          name: spot.spot_name,
          image: spot.image_url,
          description: spot.description,
        }));
    console.log("筛选后的景点:", attractions.value);
  } else {
    console.warn("未找到匹配的城市");
    attractions.value = [];
  }
};



onMounted(async () => {
  try {
    const spotsResponse = await SpotsAPI.getSpotsAPI();

    if (typeof spotsResponse === "string") {
      // 替换 "Decimal('4.40')" 为合法的数字 4.40
      const fixedResponse = spotsResponse.replace(/Decimal\('([\d.]+)'\)/g, '$1');

      // 替换单引号为双引号，解析 JSON 对象
      const spotsArray = fixedResponse
          .replace(/'/g, '"')
          .match(/{[^}]+}/g)
          .map((spot) => JSON.parse(spot));

      interestData.value = spotsArray;

      console.log("景点数据（处理后）:", interestData.value);
    } else {
      console.error("景点数据格式错误，期望为字符串形式");
    }
  } catch (error) {
    console.error("加载景点数据时出错:", error);
  }
  try {
    const cityResponse = await CityAPI.getCityAPI();

    if (typeof cityResponse === "string") {
      // 替换单引号为双引号
      const fixedString = cityResponse.replace(/'/g, '"');

      // 添加数组括号并分割字符串
      const cityArray = fixedString
          .match(/{[^}]+}/g) // 匹配所有 JSON 对象
          .map((city) => JSON.parse(city)); // 解析为 JSON 对象

      cityInfoData.value = cityArray;

      console.log("城市数据（处理后）:", cityInfoData.value);
    } else {
      console.error("城市数据格式错误，期望为字符串形式");
    }
  } catch (error) {
    console.error("加载城市数据时出错:", error);
  }
  // SentimentAPI.getSentimentAnalyzeAPI("橘子洲").then(data=>{
  //   console.log("情感分析",data);
  // })
  SentimentAPI.getSentimentResultAPI("橘子洲").then(data=>{
    console.log("情感结果",data);
  })

  myChart = echarts.init(chartsDOM.value as HTMLElement);

  myChart.showLoading();
  echarts.registerMap('HN', hunanMapData);

  const option = {
    series: [
      {
        name: '湖南地图',
        type: 'map',
        map: 'HN',
        label: {
          show: true,
        },
        emphasis: {
          itemStyle: {
            areaColor: '#FFD700' // 高亮颜色
          }
        }
      },
    ],
  };

  myChart.setOption(option);
  myChart.hideLoading();

  // 添加地图点击事件监听
  myChart.on('click', function (params) {
    if (params.name) {
      selectedCity.value = params.name; // 设置选中的城市名称
      highlightCity(); // 调用高亮函数
      updateCityInfo(); // 更新城市信息
      loadAttractions(params.name); // 加载选中城市的景点信息
    }
  });
});

// 当从下拉框选择城市时的处理函数
const onCitySelect = () => {
  highlightCity(); // 高亮显示选择的城市
  updateCityInfo(); // 更新城市信息
  loadAttractions(selectedCity.value); // 加载选中城市的景点信息
};
//const attractionName=ref('')//保存当前点击的景点的名字，并进行跳转，将景点名传给详情页
const goToPlaceDetail = (attractionName) => {
  router.push({ path: '/placeDetail', query: { name: attractionName } });
}
// 更新城市信息
const updateCityInfo = () => {
  console.log('Selected City:', selectedCity.value); // 检查 selectedCity 的值
  console.log('City Info:', cityInfoData[selectedCity.value]); // 检查加载的城市信息
  console.log('Selected City:', selectedCity.value)
  selectedCityInfo.value = cityInfoData[selectedCity.value] || null;
  selectedCityInfoLocal.value=cityInfoDataLocal[selectedCity.value];
  console.log(selectedCityInfo)
  //console.log(selectedCityInfo.value.wordCloudImage)
};

// 清除地图上的所有高亮效果
const clearHighlight = () => {
  myChart.dispatchAction({
    type: 'downplay', // 取消高亮
    seriesIndex: 0,
  });
};

// 高亮显示选择的城市
const highlightCity = () => {
  if (!selectedCity.value) return;

  clearHighlight(); // 先清除所有高亮

  myChart.dispatchAction({
    type: 'highlight', // 高亮当前选中的城市
    seriesIndex: 0,
    name: selectedCity.value,
  });

  updateCityInfo(); // 更新右侧box中的信息
};
const getImageUrl = (imagePath) => {
  try {
    // 替换路径中的 `@` 为 `/src`
    const adjustedPath = imagePath.replace(/^@/, '/src');
    const url = new URL(adjustedPath, import.meta.url).href;
    console.log(url);
    return url;
  } catch (e) {
    console.error('图片加载失败', e);
    return '';
  }
};
// 判断是否为 URL 的函数
const isUrl = (text: string): boolean => {
  const urlPattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
      '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.?)+[a-z]{2,}|'+ // domain name
      '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
      '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
      '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
      '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
  return !!urlPattern.test(text);
};

// 计算属性用于动态更新过滤后的景点
const filteredAttractions = computed(() => {
  if (!searchQuery.value) return attractions.value;

  return attractions.value.filter(attraction =>
      attraction.name.includes(searchQuery.value) ||
      (attraction.description && attraction.description.includes(searchQuery.value))
  );
});

const searchAttractions = () => {
  console.log("搜索结果：", filteredAttractions.value);
  // 您可以在这里添加额外的逻辑，比如记录搜索日志等
};

</script>

<style scoped lang="scss">
@import '@/assets/font/font.css';
#app {
  height: 100vh;
  margin: 0;
}

.el-main {
  --el-main-padding:0;

}
.hunan-tourist-attractions {

  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}


.hunan-tourist-attractions {
  display: flex;
  flex-direction: column;
  align-items: center;

  min-height: 100vh;
  padding: 10px;

}

.map-info-container {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.map-box {
  width: 500px;
  height: 600px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.location-box {
  width: 650px;
  height: 560px;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  position: relative;
}
.attraction-card-box{
  height: 560px;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width:1210px;
  background-color: #fff;
  position: relative;
  box-sizing: border-box;
  overflow-y: auto; /* 启用垂直滚动 */
}

.centered-text {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
.city-select {
  position: absolute;
  top: 20px;
  left: 20px;
  width: 150px;
}

.city-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}
.city-image,.wordcloud-image {
  width: 300px; /* 设置图片的宽度 */
  height: 200px; /* 设置图片的高度 */
  object-fit: cover; /* 保持图片的比例 */
  border-radius: 8px; /* 图片的圆角 */
  margin-bottom: 15px;
}
.wordcloud-image {
  object-fit: contain; /* 确保图片不裁剪 */
}

/* 滚动文本框样式 */
.description-box {
  max-height: 240px; /* 设置文本框的最大高度 */
  font-family: 'ChillKaiShu',serif;
  overflow-y: auto; /* 启用垂直滚动 */
  padding: 10px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-top: 10px;
  width: 90%;
}

.city-name-display {
  font-size: 18px;
  color: #333;
  margin-top: 100px;
}


.attractions-container {
  display: flex;
  flex-wrap: wrap; /* 允许换行 */
  gap: 15px; /* 卡片之间的间距 */
  justify-content: flex-start; /* 卡片左对齐 */
}

.attraction-card {
  #background-color: #fff8f0;
  background-image: url('@/assets/img_3.jpg');

  margin-right: 22px;
  margin-left: 22px;
  margin-bottom: 15px;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 300px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.fancy-name {
  font-family: 'ZhuanTi', serif; /* 使用纂体字体 */
  font-size: 13px; /* 根据需要调整字体大小 */
  color: #555; /* 设置字体颜色 */
}

.attraction-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.attraction-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
}

.attraction-details {
  margin-top: 10px;
}

.attraction-details a {
  color: #2c3e50; /* 设置链接的颜色 */
  font-family: 'HelveticaNeue',serif;
  font-size: 12px;
  text-decoration: underline; /* 添加下划线让用户知道是链接 */
  cursor: pointer; /* 确保鼠标悬停时显示为指针 */
  pointer-events: auto; /* 确保链接可以点击 */
  word-break: break-all; /* 允许长链接换行 */
}

.attraction-details h3 {
  color: #d32f2f;
  font-family: 'HelveticaNeue',serif;
  font-size: 30px;
  margin: 0;
  font-weight: bold;
}

.attraction-details p {
  font-size: 14px;
  font-family: 'HelveticaNeue',serif;
  color: #555;
  margin-top: 8px;
}

.search-container {
  margin-top: 20px;
  width: 100%;
  max-width: 400px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-container input {
  flex: 1;
  padding: 10px;
  border: 1px solid #d32f2f;
  border-radius: 4px;
  font-size: 14px;
}

.search-container button {
  padding: 10px 20px;
  border: none;
  background-color: #d32f2f;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.search-container button:hover {
  background-color: #b71c1c;
}
</style>
