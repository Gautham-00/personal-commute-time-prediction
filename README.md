# Personal Commute Time Prediction & Analytics

A Machine Learning project that predicts commute duration based on departure time, traffic conditions, weather, and date using Python and Streamlit.

**Route:** Chethicode → Knovista Technologies, Kadavanthra, Kochi.

## Project Objectives
- Predict commute duration using Machine Learning.
- Analyse travel patterns and trends.
- Compare different departure times.
- Build an interactive analytics dashboard.

## Technologies
Python | Pandas | NumPy | Matplotlib | Scikit-learn | Streamlit | Joblib

## Machine Learning Models
Compared three regression algorithms:
- Ridge Regression
- Random Forest Regressor
- Gradient Boosting Regressor

**Selected Model: Random Forest Regressor**

| Metric | Result |
|---|---:|
| MAE | 3.35 min |
| RMSE | 4.47 min |
| R² Score | 0.774 |

*Note: Results are based on a simulated dataset and do not represent validated real-world prediction accuracy.*

##  Dashboard Features

1. **Commute Prediction** – Predict travel duration and estimated arrival time.
2. **Commute Analytics** – Explore travel trends and visualizations.
3. **Departure Comparison** – Compare different departure times.
4. **Model Details** – View model information and evaluation metrics.

## 📸 Screenshots

<img width="1910" height="963" alt="Screenshot 2026-11-06 160413" src="https://github.com/user-attachments/assets/3bf55e8c-5eda-473d-8b89-cb320791d3dc" />
<img width="412" height="122" alt="Screenshot 2026-11-06 144021" src="https://github.com/user-attachments/assets/29d18d90-6404-4dbf-9d94-fe5928236a4c" />


## ⚙️ Run Locally

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

Open `http://localhost:8501`.

## 📁 Project Structure

```text
├── app.py
├── commute_time_model.joblib
├── Personal_Commute_Time_Prediction_Synthetic_Dataset.xlsx
├── requirements.txt
├── README.md
└── screenshots/
```

## 👨‍💻 Author

**Gautham K Sasidharan**

[GitHub](https://github.com/Gautham-00) | [LinkedIn](https://www.linkedin.com/in/gautham-k-sasidharan-64279b1b4/)
