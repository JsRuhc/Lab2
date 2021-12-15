.. Mr.Lan Lab2 documentation master file, created by
   sphinx-quickstart on Wed Dec 15 22:35:26 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Mr.Lan Lab2's documentation!
=======================================
.. toctree::
   :maxdepth: 2
   :caption: Contents:


**小组成员**



201932110132邱政淞







**项目GitHub地址**: `BluePrint`_.

.. _BluePrint: https://github.com/ChiefEye-official/Test/



**项目演示视频**: `Bilibili`_.

.. _Bilibili: https://www.bilibili.com/video/BV1A3411t7Ct?spm_id_from=333.999.0.0

作用
=================================================

blueprint把不同功能的module分开。可以让应用模块化，针对大型应用。
蓝图的基本概念：在蓝图被注册到应用之后，所要执行的操作的集合。当分配请求时， Flask 会把蓝图和视图函数关联起来，并生成两个端点之前的 URL 。
比如只有一个run.py。有些功能需要多人分开来写，有些功能会有交错的可能，代码位置也不会在一起，这样可以用蓝图来开关一些模块（功能）和宏定义类似，但不是可插拔的应用而是一套可以注册在应用中的操作，并且可以注册多次。或者简单滴需要降低耦合，提高模块复用率。比如开发环境和应用环境的不同，可以用蓝图来切换环境。
蓝图的缺点是一旦应用被创建后，只有销毁整个应用对象才能注销蓝图。

用法
=================================================

如果使用errorhandler 修饰器，那么只有蓝本中的错误才能触发处理程序。即修饰器由蓝本提供。要想注册程序全局的错误处理程序，必须使用app_errorhandler。

创建 URL用法：
Flask 会为蓝本中的全部端点加上一个命名空间，这样就可以在不
同的蓝本中使用相同的端点名定义视图函数，而不会产生冲突。（跨蓝本）
在单脚本程序中：index() 视图函数的URL 可使用
url_for(‘index’)
在蓝图中：index() 视图函数的URL 可使用
url_for(‘main.index’)
另外，如果在一个蓝图的视图函数或者被渲染的模板中需要链接同一个蓝图中的其他端点，那么使用相对重定向，只使用一个点使用为前缀。简写形式（命名空间是当前请求所在的蓝本）：
url_for(‘.index’)
Methods and materials
=================================================

①Snakefood：从Python代码中生成依赖，过滤，聚类，并从依赖列表中生成图表。使用Snakefood捕获模块级依赖关系。

②Graphviz：开源的图形可视化软件。使用graphviz online渲染依赖关系图。

③Mermaid：基于Javascript的图表和图表工具，使用文本和代码创建图表和可视化，以便动态地创建和修改图表。使用mermaid live editor渲染类/函数级依赖关系图。

代码
=================================================

**UseSqlite.py**
::
      # Reference: Dusty Phillips.  Python 3 Objected-oriented Programming Second Edition. Pages 326-328.
      # Copyright (C) 2019 Hui Lan

      import sqlite3

      class Sqlite3Template:
          def __init__(self, db_fname):
              self.db_fname = db_fname

          def connect(self, db_fname):
              self.conn = sqlite3.connect(self.db_fname)

          def instructions(self, query_statement):
              raise NotImplementedError()

          def operate(self):
              self.results = self.conn.execute(self.query) # self.query is to be given in the child classes
              self.conn.commit()

          def format_results(self):
              raise NotImplementedError()

          def do(self):
              self.connect(self.db_fname)
              self.instructions(self.query)
              self.operate()


      class InsertQuery(Sqlite3Template):
          def instructions(self, query):
              self.query = query


      class RiskQuery(Sqlite3Template):
          def instructions(self, query):
              self.query = query

          def format_results(self):
              output = []
              for row in self.results.fetchall():
                  output.append(', '.join([str(i) for i in row]))
              return '\n\n'.join(output)


      if __name__ == '__main__':

          #iq = InsertQuery('RiskDB.db')
          #iq.instructions("INSERT INTO inspection Values ('FoodSupplies', 'RI2019051301', '2019-05-13', '{}')")
          #iq.do()
          #iq.instructions("INSERT INTO inspection Values ('CarSupplies', 'RI2019051302', '2019-05-13', '{[{\"risk_name\":\"elevator\"}]}')")
          #iq.do()

          rq = RiskQuery('RiskDB.db')
          rq.instructions("SELECT * FROM inspection WHERE inspection_serial_number LIKE 'RI20190513%'")
          rq.do()
          print(rq.format_results())


**upload.py**
::
      from flask import Blueprint

      upload_bp = Blueprint('/upload', __name__)


      @upload_bp.route('/upload')
      def upload():
          return '''<form action="/"method="post"enctype="multipart/form-data">
                  <input type="file"name="file"><input name="description"><input type="submit"value="Upload"></form>'''

**show.py**
::
      from flask import Blueprint
      from PIL import Image
      from UseSqlite import RiskQuery

      show_bp = Blueprint('show', __name__)


      def make_html_paragraph(s):  # 将数据库中获取到的图片和信息格式化展现在网页上
          if s.strip() == '':
              return ''
          lst = s.split(',')
          picture_path = lst[2].strip()
          picture_name = lst[3].strip()
          im = Image.open(picture_path)
          im.thumbnail((400, 300))
          im.save('./static/figure/' + picture_name, 'jpeg')
          result = '<p>'
          result += '<i>%s</i><br/>' % (lst[0])
          result += '<i>%s</i><br/>' % (lst[1])
          result += '<a href="%s"><img src="./static/figure/%s"alt="风景图"></a>' % (picture_path, picture_name)
          return result + '</p>'


      def make_html_photo(s):
          if s.strip() == '':
              return ''
          lst = s.split(',')
          picture_path = lst[2].strip()
          picture_name = lst[3].strip()
          im = Image.open(picture_path)
          im.thumbnail((400, 300))
          real_path = '.' + picture_path
          result = '<p>'
          result += '<i>%s</i><br/>' % (lst[0])
          result += '<i>%s</i><br/>' % (lst[1])
          result += '<a href="%s"><img src="../static/figure/%s"alt="风景图"></a>' % (real_path, picture_name)
          return result + '</p>'


      def get_database_photos():  # 从数据库中获取所有图片及其相关信息
          rq = RiskQuery('./static/RiskDB.db')
          rq.instructions("SELECT * FROM photo ORDER By time desc")
          rq.do()
          record = '<p>My past photo</p>'
          for r in rq.format_results().split('\n\n'):  # 将每条图片信息记录按照一定的样式显示在网页上
              record += '%s' % (make_html_paragraph(r))
          return record + '</table>\n'


      def get_description_photos(description):
          rq = RiskQuery('./static/RiskDB.db')
          rq.instructions("SELECT * FROM photo where description = '%s' " % description)
          rq.do()
          record = '<p>search result</p>'
          for r in rq.format_results().split('\n\n'):
              record += '%s' % (make_html_photo(r))
          return record + '</table>\n'


      @show_bp.route('/show')  # 展示所有照片信息页面
      def show():
          return get_database_photos()


**search.py**
::
      from flask import Blueprint, request
      from show import get_description_photos

      search_bp = Blueprint('/search', __name__)


      @search_bp.route('/search', methods=['POST', 'GET'])
      def search():
          return '''<form action="/search/query-string"method="post"enctype="multipart/form-data">
                      <input name="description"><input type="submit"value="search"></form>'''


      @search_bp.route('/search/query-string', methods=['POST', 'GET'])
      def query_string():
          if request.method == 'POST':
              description = request.form['description']
              page = get_description_photos(description)

          return page

**Lab.py**
::
      # -*- coding: utf-8 -*-
      """
      Created on Mon Jun  3 15:42:51 2019

      @author: Administrator
      """

      from flask import Flask, request
      from UseSqlite import InsertQuery
      from datetime import datetime
      from show import get_database_photos
      from upload import upload_bp
      from show import show_bp
      from search import search_bp
      from api_json import api_bp

      app = Flask(__name__)

      # 将蓝图注册到app
      app.register_blueprint(upload_bp)
      app.register_blueprint(show_bp)
      app.register_blueprint(search_bp)
      app.register_blueprint(api_bp)


      @app.route('/', methods=['POST', 'GET'])
      def main():
          if request.method == 'POST':
              uploaded_file = request.files['file']
              time_str = datetime.now().strftime('%Y%m%d%H%M%S')
              new_filename = time_str + '.jpg'
              uploaded_file.save('./static/upload/' + new_filename)
              time_info = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
              description = request.form['description']
              path = './static/upload/' + new_filename
              iq = InsertQuery('./static/RiskDB.db')
              iq.instructions("INSERT INTO photo Values('%s','%s','%s','%s')" % (time_info, description, path, new_filename))
              iq.do()
              return '<p>You have uploaded %s.<br/> <a href="/">Return</a>.' % uploaded_file.filename
          else:
              page = '''
                  <a href='/upload'>upload</a>
                  <a href='/search'>search</a>
                  <a href='/show'>show</a>
                  <a href='/api_json'>api_json</a>
             '''
              page += get_database_photos()
              return page


      if __name__ == '__main__':
          app.run(debug=True)

**api_json.py**
::
      import json
      import os.path

      from flask import Blueprint
      from UseSqlite import RiskQuery

      api_bp = Blueprint('/api_json', __name__)


      @api_bp.route('/api_json', methods=['POST', 'GET'])
      def api_json():
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
              page += '%s' % lst2
              i += 1
          return page



参考资料
=================================================

[1] zoukankan https://stackoverflow.com/questions/7974771/flask-blueprint-template-folder
[2] ITEYE https://www.iteye.com/blog/bcyy-1808978
[3] 百度百科 https://baike.baidu.com/item/Blueprint/3592968?fr=aladdin
