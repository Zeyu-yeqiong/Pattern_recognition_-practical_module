# Pulmonary Fibrosis

### Video Introduction

https://drive.google.com/file/d/1fPBAyr71mgXWqtEx4sYrqMCnCx3lXo1F/view?usp=sharing

### Requirements

Please, install the following packages
- tensorflow==2.2.0
- pydicom=2.0.0
- seaborn==0.11.0
- efficientnet==1.1.1
- sklearn
- tensorflow-addons-0.11.2
- plotly-4.11.0




### Model Checkpoint

Download efficientnet B5 net weight from https://drive.google.com/file/d/1cygSFVtJ4kPPn3nZvJsTCsMyMc2np6UM/view?usp=sharing ,
Put it in to Pattern_recognition_-practical_module_group9/weights  folder. 

### Guide
- install all library, note tensorflow need 2.2.0 version
- run run.py in root directory.
- open browser, go to http://127.0.0.1:8987/index.
- input patient's information in text box
- Click choose file button, select some CT scan from "\osic-pulmonary-fibrosis-progression\test\random folder" and upload it (if you don't choose any file, it will use osic-pulmonary-fibrosis-progression\test\demo)
- Waiting for 3 - 15 mins, you can see progress in terminal output
- Dispay output and our suggestion in FE 


### CV Part Training:
For CV part, If you don't want to use our pretrain model, you can train your own model with  training.py
Training dataset download: https://www.kaggle.com/c/osic-pulmonary-fibrosis-progression/data

