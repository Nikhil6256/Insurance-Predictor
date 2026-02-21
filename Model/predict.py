import pickle
import pandas as pd
# import the ml model
with open('Model/model.pkl','rb') as f:
    Model = pickle.load(f)

MODEL_VERSION = '1.0.0'
class_labels = Model.classes_.tolist()

def predict_output(user_input: dict):
    df=pd.DataFrame([user_input])
    # input_df=pd.DataFrame(user_input)
    # output = Model.predict(input_df)[0]
    # return output

    predicted_class = str(Model.predict(df)[0])

    # Get probabilities for all classes
    probabilities = Model.predict_proba(df)[0]
    confidence = float(max(probabilities))

    # Create mapping: {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return {
    "predicted_category": predicted_class,
    "confidence": round(confidence, 4),
    "class_probabilities": class_probs
    }
