import pickle

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Using ML in Streamlit
# If the plan is to use a ML model in a Streamlit app, the recommended method is
# to create this model outside of Streamlit first (for example, in a Jupyter notebook or in a standard
# Python file), and then use this model within the app.

penguin_df = sns.load_dataset('penguins')
penguin_df.dropna(inplace=True)
output = penguin_df["species"]
features = penguin_df[
    [
        "island",
        "bill_length_mm",
        "bill_depth_mm",
        "flipper_length_mm",
        "body_mass_g",
        "sex",
    ]
]
features = pd.get_dummies(features)
output, uniques = pd.factorize(output)

x_train, x_test, y_train, y_test = train_test_split(features, output, test_size=0.2)
rfc = RandomForestClassifier(random_state=15, max_depth=5)
rfc.fit(x_train.values, y_train)
y_pred = rfc.predict(x_test.values)
score = accuracy_score(y_pred, y_test)
print("Our accuracy score for this model is {}".format(score))

# We now have a pretty good model for predicting the species of penguins! Our last step in the
# model-generating process is to save the two parts of this model that we need the most – the model
# itself and the uniques variable, which maps the factorized output variable to the species name
# that we recognize.

rf_pickle = open("random_forest_penguin.pickle", "wb")
pickle.dump(rfc, rf_pickle)
rf_pickle.close()
output_pickle = open("output_penguin.pickle", "wb") # mapping between penguin species and the output of our model
pickle.dump(uniques, output_pickle)
output_pickle.close()

# We will add a few lines that will save these objects as pickle files
# (files that turn a Python object into something we can save directly and import easily
# from another Python file such as our Streamlit app). More specifically, the open() function creates
# two pickle files, the pickle.dump() function writes our Python files to said files, and the close()
# function closes the files. The wb in the open() function stands for write bytes, which tells Python
# that we want to write, not read, to this file

# Create figure and axis for feature importance plot
sns.set_style("darkgrid")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=rfc.feature_importances_, y=features.columns, ax=ax)
ax.set_title("Which features are the most important for species prediction?")
ax.set_xlabel("Importance")
ax.set_ylabel("Feature")
plt.tight_layout()
fig.savefig("feature_importance.png")