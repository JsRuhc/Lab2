from flask import Blueprint,render_template,request
import json
import os.path
from UseSqlite import  RiskQuery

api_bp= Blueprint('api_bp',__name__)
 
@api_bp.route("/api")
def api():
    rq = RiskQuery('./static/RiskDB.db')
    rq.instructions("SELECT * FROM photo ORDER By time desc")
    rq.do()
    lst = []  # 存储输出的图片信息的数组
    page = ''
    i = 1  # 手动给图片添加ID
    for r in rq.format_results().split('\n\n'):
        photo = r.split(',')
        picture_time = photo[0]  # 获取上传时间
        picture_description = photo[1]  # 获取图片描述
        picture_path = photo[2].strip()  # 获取图片存储路径
        photo_size = str(format((os.path.getsize(picture_path) / 1024), '.2f')) + 'KB'  # 获取图片文件大小
        lst = [{'ID': i, 'upload_date': picture_time, 'description': picture_description, 'photo_size': photo_size}]
        lst2 = json.dumps(lst[0], sort_keys=True, indent=4, separators=(',', ':'))
        page += '</p>%s' % lst2
        i += 1
    return page