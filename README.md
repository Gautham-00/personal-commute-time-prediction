# Personal Commute Intelligence — Streamlit Prototype

Route context: Chethicode → Knovista Technologies, Kadavanthra Junction, Kochi.

## Important data limitation
This project currently uses 100 simulated commute records. Weather and traffic labels are illustrative, not verified historical conditions. The model metrics (MAE 3.35 min, RMSE 4.47 min, R² 0.774) are from a synthetic chronological holdout and must not be presented as real-world commute accuracy.

## Run locally
1. Extract this ZIP.
2. Use Python 3.10 or 3.11.
3. Open a terminal in the extracted folder.
4. Run `pip install -r requirements.txt`
5. Run `streamlit run app.py`

The Excel workbook and model file must stay in the same folder as `app.py`.

## Tabs
- Prediction: estimate duration and arrival time for a selected scenario.
- Commute Analytics: explore simulated trip patterns.
- Departure Comparison: compare 10 departure slots under fixed assumed conditions.
- Model Details: view model and data provenance notes.

## Model compatibility
The saved scikit-learn pipeline was trained with scikit-learn 1.6.1. Keep the pinned version in requirements.txt to avoid pickle compatibility problems.
