from flask_appbuilder import IndexView, BaseView


class MyIndexView(IndexView):
    index_template = 'my_index.html'
