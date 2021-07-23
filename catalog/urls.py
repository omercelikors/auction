from django.urls import path
from catalog import views

urlpatterns = [
    path('show/items', views.show_items, name='show_items'),
    path('api/get/items', views.api_get_items, name='api_get_items'),
    path('show/item/detail/<int:item_id>', views.show_item_detail, name='show_item_detail'),
    path('api/get/item', views.api_get_item, name='api_get_item'),
    # path('show/all/apis', views.show_all_apis, name='show_all_apis'),
    # path('show/all/crawler-links', views.show_all_crawler_links, name='show_all_crawler_links'),
    # path('show/all/crg-has-crawlers', views.show_all_crg_has_crawlers, name='show_all_crg_has_crawlers'),
    # path('show/all/crg-has-channels', views.show_all_crg_has_channels, name='show_all_crg_has_channels'),
    # path('show/all/crawler-has-log-files', views.show_all_crawler_has_log_files, name='show_all_crawler_has_log_files'),
    # path('show/all/channels', views.show_all_channels, name='show_all_channels'),
    # path('show/all/settings', views.show_all_settings, name='show_all_settings'),
    # path('show/all/company-report-groups', views.show_all_crgs, name='show_all_crgs'),
    # path('show/all/companies', views.show_all_companies, name='show_all_companies'),

    # path('create/setting', views.create_setting, name='create_setting'),
    # path('update/setting/<int:setting_id>', views.update_setting, name='update_setting'),
    # path('update/crawler-link/<int:crawler_link_id>', views.update_crawler_link, name='update_crawler_link'),
    # path('update/crawler/single-run/<int:crawler_id>', views.update_crawler_single_run, name='update_crawler_single_run'),
    # path('update/api/single-run/<int:api_id>', views.update_api_single_run, name='update_api_single_run'),
    # path('download/log-file/<int:log_file_id>', views.download_log_file, name='download_log_file'),
    # path('assign/link-to-crawler', views.assign_link_to_crawler, name='assign_link_to_crawler'),
]
