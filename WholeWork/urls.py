from api_views import GetAllBills,TestRule,GetSourceData,GetSourceBig
from views import WholeIndexView

def whole_url(app):
    app.add_url_rule('/whole/index','whole_index',WholeIndexView.as_view('whole_index'))


api_root_url = '/whole/api/v1.0/'
def whole_api_url(api):
    api.add_resource(GetAllBills,api_root_url+'get_all_bills')
    api.add_resource(TestRule,api_root_url+'test_rules')
    api.add_resource(GetSourceData,api_root_url+'get_source_data')
    api.add_resource(GetSourceBig,api_root_url+'get_source_big')