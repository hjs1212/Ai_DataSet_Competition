from sqlalchemy import create_engine
import os
from PIL import Image ##Error시 pip install pillow 실행
import pandas as pd #Error시 pip install pandas 실행
import base64
from io import BytesIO

ExImageDir = './../0_DB/Image/Explanation'
ViewImageDir = './../0_DB/Image/View'
GuidImageDir = './../0_DB/Image/Guide'
ImageDir = {1:GuidImageDir,2:ExImageDir,3:GuidImageDir}

host = 'localhost'
user = 'root'
passwd = 'root1!'
db = 'Ai_dataset_competition'

#Image Upload
engine = create_engine("mysql+pymysql://"+user+":"+passwd+"@localhost:3306/"+db+"?charset=utf8", encoding='utf-8', echo=False)
conn = engine.connect()
buffer = BytesIO()
df = pd.DataFrame(columns=['CulturalHeritage_Num','type','Image'])
num = int(input()) # CulturalHeritage_Num
max = 0
for i in range(1,4) :
    dir = ImageDir[i]
    for file in os.listdir(dir) :
        im = Image.open(dir+'/'+file)
        try :
            im.save(buffer,format='jpeg')
        except :
            im = im.convert("RGB")
            im.save(buffer,format='jpeg')
        img_str = base64.b64encode(buffer.getvalue())
        tmp = pd.DataFrame(data=[[num,i,img_str]],columns=['CulturalHeritage_Num','type','Image'])
        df = df.append(tmp)
        df = df.reset_index(drop=True)
df.to_sql(name='imageset',con=conn,if_exists='append',index=False)

#Image Load
'''
img_df = pd.read_sql(sql='select * from imageset where type=1',con=conn)
print(img_df['Image'])
img_df = pd.read_sql(sql='select * from imageset where type=1',con=conn)
img_str = img_df['Image'].values[0]
img = base64.decodestring(img_str)

Image.open(BytesIO(img)).show()
'''
