# 🌫️ AQI Monitoring and Prediction System

## 📌 Overview

This project focuses on building an **IoT-based Air Quality Monitoring and Prediction System** using sensor data and machine learning.
The system collects environmental data, reconstructs inconsistent time-series data into a continuous format, integrates weather information, and predicts future AQI levels.

---

## 🎯 Objectives

* Collect real-time environmental data using IoT sensors
* Handle **inconsistent and missing time-series data**
* Reconstruct a **continuous 24-hour dataset**
* Integrate **weather API data** for better accuracy
* Predict AQI for the next **2–3 hours**
* Generate alerts when AQI is expected to worsen

---

## 🧰 Sensors Used

* **MQ135** → Gas pollutants
* **PMS5007** → PM2.5 and PM10
* **DHT22** → Temperature and Humidity

---

## ⚙️ System Workflow

1. **Data Collection**

   * Sensor readings stored in CSV format
   * Data contains irregular timestamps and missing values

2. **Datetime Processing**

   * Combine date and time into a single timestamp
   * Sort data for time-series operations

3. **Continuous Timeline Creation**

   * Generate full 24-hour time intervals
   * Map existing data onto this timeline

4. **Weather API Integration**

   * Fetch weather data (temperature, humidity, wind, pressure)
   * Align with sensor timestamps

5. **Time-Series Processing**

   * Resampling to fixed intervals
   * Interpolation for small gaps
   * Context-aware imputation for large gaps

6. **Data Smoothing**

   * Apply rolling averages to remove abrupt fluctuations

7. **Feature Engineering**

   * Lag features (previous AQI values)
   * Rolling averages
   * Time-based features (hour, day)
   * Weather interaction features

8. **Model Training**

   * Random Forest
   * XGBoost

9. **AQI Prediction**

   * Predict AQI for next 2–3 hours

10. **Alert System**

* Send SMS alerts using Twilio if AQI exceeds threshold

---

## 🧠 Key Contribution

The major contribution of this project is:

> Transforming inconsistent real-world IoT sensor data into a continuous and realistic time-series dataset using interpolation and context-aware imputation guided by external weather data.

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* OpenWeather API
* Twilio API

---

## 📂 Project Structure

```
aqi-project/
│
├── data/
│   ├── raw_inconsistent.csv
│   ├── step1_datetime_ready.csv
│   ├── step2_timeline.csv
│   ├── step3_api_merged.csv
│   ├── step4_interpolated.csv
│   └── final_dataset.csv
│
├── pipeline.py
├── requirements.txt
├── README.md
```

---

## ▶️ How to Run

1. Clone the repository
2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```
3. Run the pipeline:

   ```
   python pipeline.py
   ```

---

## 📊 Output

* Clean continuous dataset
* AQI predictions
* Alert notifications

---

## 🚀 Future Improvements

* Real-time dashboard visualization
* Deployment using Flask
* Live sensor integration
* Improved deep learning models

---

## 👩‍💻 Author

Siddhi Shandilya
