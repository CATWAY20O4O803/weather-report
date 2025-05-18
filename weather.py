import requests
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 設定字體
# Change the font path to the filename if the font file is in the same directory
# or provide the correct path within the Linux environment
font_path = 'kaiu.ttf'  # Assuming kaiu.ttf is in the same directory as the notebook
try:
    font_properties = font_manager.FontProperties(fname=font_path)
    print(f"字體 {font_path} 載入成功.")
except FileNotFoundError:
    print(f"警告: 未找到字體文件 {font_path}。將使用默認字體。")
    # Fallback to a generic font or let matplotlib use its default
    font_properties = font_manager.FontProperties(family='sans-serif')
except Exception as e:
    print(f"載入字體時發生錯誤: {e}")
    font_properties = font_manager.FontProperties(family='sans-serif')


# 獲取當前天氣
def get_weather(city_name):
    API_KEY = "819766b7bc142b48f08976afb8ba57c1"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
        "lang": "zh_tw"
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        print(f"城市：{city_name}")
        print(f"天氣：{weather}")
        print(f"溫度：{temp}°C")
        print(f"濕度：{humidity}%")
        print(f"風速：{wind_speed} m/s")
        print("")
    else:
        print(f"無法獲取 {city_name} 的天氣資訊，請檢查城市名稱或 API 設置。")

# 獲取未來 5 天天氣預測
def get_5_day_forecast(city_name):
    API_KEY = "819766b7bc142b48f08976afb8ba57c1"
    BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
        "lang": "zh_tw"
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        city = data['city']['name']
        country = data['city']['country']

        print(f"城市：{data['city']['name']}, {data['city']['country']}")
        print("未來 5 天的天氣預測：")

        daily_forecast = {}
        for forecast in data['list']:
            dt_txt = forecast['dt_txt']
            date = dt_txt.split(' ')[0]  # 只取日期部分
            temp = forecast['main']['temp']

            if date not in daily_forecast:
                daily_forecast[date] = {"min": temp, "max": temp}
            else:
                daily_forecast[date]["min"] = min(daily_forecast[date]["min"], temp)
                daily_forecast[date]["max"] = max(daily_forecast[date]["max"], temp)

        dates = []
        min_temps = []
        max_temps = []

        for date, temps in daily_forecast.items():
            dates.append(date)
            min_temps.append(temps["min"])
            max_temps.append(temps["max"])
            print(f"{date}: 最低溫 {temps['min']}°C, 最高溫 {temps['max']}°C")

        return dates, min_temps, max_temps
    else:
        print("獲取天氣預測失敗，請檢查城市名稱或 API 設定。")
        return None, None, None

# 繪製折線圖
def plot_forecast(dates, min_temps, max_temps):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, min_temps, marker="o", label="最低溫", color="blue")
    plt.plot(dates, max_temps, marker="o", label="最高溫", color="red")
    plt.title("未來 5 天天氣預測", fontproperties=font_properties)
    plt.xlabel("日期", fontproperties=font_properties)
    plt.ylabel("溫度 (°C)", fontproperties=font_properties)
    plt.legend(prop=font_properties)
    plt.grid(True)
    plt.show()

# 主程式
if __name__ == "__main__":
    while True:
        city = input("請輸入城市的英文名稱（輸入 'exit' 結束）：")
        if city.lower() == 'exit':
            print("程式結束。")
            break

        # 獲取當前天氣
        get_weather(city)

        # 獲取天氣預測 繪圖
        dates, min_temps, max_temps = get_5_day_forecast(city)
        if dates and min_temps and max_temps:
            plot_forecast(dates, min_temps, max_temps)
