from StateGenerator import StateGenerator
from DFGenerator import FacialDFGenerator

df = FacialDFGenerator.generate_df("../Machine_Learning_Model/images/smile_1.jpg")
sg = StateGenerator("../Machine_Learning_Model/smile_neutral_rf.pkl", "FACE")
print(sg.get_state(df))