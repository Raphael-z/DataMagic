from api_views import GetBBhistory
from views import BBhistoryIndexView,BBTimeView

def single_url(app):
    app.add_url_rule('/single/index','single_index',BBhistoryIndexView.as_view('single_index'))
    app.add_url_rule('/single/bb_time','bb_time_view',BBTimeView.as_view('bb_time_view'))


api_root_url = '/single/api/v1.0/'
def single_api_url(api):
    api.add_resource(GetBBhistory,api_root_url+'get_bb_history')