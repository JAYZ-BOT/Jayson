
from utils import collect_live_data

if __name__ == "__main__":
    collect_live_data()
import logging

logging.basicConfig(level=logging.INFO)

def on_message(ws, message):
    logging.info(f"Received Data: {message}")  # Log incoming data
    try:
        data = parse_aviator_data(message)  # Your function to extract the multiplier
        logging.info(f"Extracted Multiplier: {data}")  

        if should_predict(data):  # Your logic to decide if a prediction is needed
            logging.info("Triggering Prediction...")  
            prediction = model.predict(data)  # Call your model
            logging.info(f"Model Prediction: {prediction}")  

            send_prediction_to_telegram(prediction)  # Send to Telegram
            logging.info("Prediction sent to Telegram.")
            
    except Exception as e:
        logging.error(f"Error in prediction pipeline: {e}")
