from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
import csv
import pandas as pd
import shutil
 
from datetime import timedelta
 
#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['dcm', 'DCM'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
 


def __del_file(path):
    del_list = os.listdir(path)
    for f in del_list:
        file_path = os.path.join(path, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
        
    os.removedirs(path)
    

@app.route('/', methods=['POST', 'GET'])
def redirect_default():
    print(request.path)
    return redirect(request.url+"index",code=302)


 
# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])  
def upload():
    if request.method == 'POST':
        f=request.files.getlist("file")
        if not request.files["file"]:
            if os.path.exists("osic-pulmonary-fibrosis-progression/test/temp"):
                __del_file("osic-pulmonary-fibrosis-progression/test/temp")
                # os.removedirs("osic-pulmonary-fibrosis-progression/test/temp")
            demo_list=os.listdir("osic-pulmonary-fibrosis-progression/test/demo")

            os.mkdir("osic-pulmonary-fibrosis-progression/test/temp")
            for file_name in demo_list:
                oldname = "osic-pulmonary-fibrosis-progression/test/demo/" + file_name
                newname = "osic-pulmonary-fibrosis-progression/test/temp/" + file_name
                shutil.copyfile(oldname, newname)
                print(file_name+'     Done')
        else:
            if os.path.exists("osic-pulmonary-fibrosis-progression/test/temp"):
                __del_file("osic-pulmonary-fibrosis-progression/test/temp")
                # os.removedirs("osic-pulmonary-fibrosis-progression/test/temp")
            demo_list=os.listdir("osic-pulmonary-fibrosis-progression/test/demo")

            os.mkdir("osic-pulmonary-fibrosis-progression/test/temp")




            if len(f)<5:
                
                return jsonify({"error": 1001, "msg": "We need at lease 5 dcm file"})
            print(f)

            for i in f:
                upload_path = "osic-pulmonary-fibrosis-progression/test/temp/"+i.filename
                i.save(upload_path)
                print(i.filename+'     Done')

                

            


        # f = request.files['file']
 
        age = request.form.get("age")
        gender=request.form.get("gender")
        week=request.form.get("week")
        fvc=request.form.get("fvc")
        smoking_status=request.form.get("smoking_status")
        print(smoking_status)
        f = open('osic-pulmonary-fibrosis-progression/test.csv','w',encoding='utf-8',newline='')
        csv_writer = csv.writer(f)
        csv_writer.writerow(["Patient","Weeks","FVC","Percent","Age","Sex","SmokingStatus"])
        csv_writer.writerow(["temp",week,fvc,"80",age,gender,smoking_status])
        f.close()

        os.system("python run_model.py")
        time.sleep(2)

        df=pd.read_csv("submission.csv")


 
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
        series=[]
        for i in range(25):
            

            P_week="temp_"+str((i-5))
            print(P_week,"temp_"+str(week))
            if P_week=="temp_"+str(week):
                FVC=fvc
                series.append([i+1,series[-1][1]-1.2543])
                continue

            FVC=df.loc[df['Patient_Week'] == P_week,'FVC'].values[0]
            
            series.append([i+1,FVC])
        print(series)


        week_0_fvc=int(df.loc[df['Patient_Week'] == "temp_0",'FVC'].values[0])
        week_100_fvc=int(df.loc[df['Patient_Week'] == "temp_100",'FVC'].values[0])



        diff=week_0_fvc-week_100_fvc
        mess=''
        advice=''
        if diff/week_0_fvc<0.05:
            mess="Your pulmonary fibrosis level: Low"
            advice="please keep on your good habit"
        elif diff/week_0_fvc<0.1:
            mess="Your pulmonary fibrosis level: Medium  "
            advice="When you feel breathless, unwell, go to see a doctor as soon as possible"
        else:
            mess="Your pulmonary fibrosis level: Serious  "
            advice="Please go to the hospital and consult doctor now"
        print(diff,diff/week_0_fvc)
        min_y=int(series[-1][1])*0.99


        return render_template('graph.html',val1=time.time(),series=series,min_y=min_y,gender=gender,smoking_status=smoking_status,age=age,mess=mess,advice=advice)

        # return render_template('index.html',userinput=user_input,val1=time.time())
 
    return render_template('index.html')
 
 
if __name__ == '__main__':
    # app.debug = True
    app.run(host='127.0.0.1', port=8987, debug=True)
