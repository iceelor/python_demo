__author__ = 'www.showbt.com'
# -*- coding:utf-8 -*-

from com.showbt.tool.Spider import Spider
from DataBaseTool import ModelInfo, DataBaseTool, ModelImage
import uuid


def get_data():
    spider = Spider("http://mm.taobao.com/json/request_top_list.htm")
    list_pattern = '<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>'
    # introduce_pattern = '<div class="mm-aixiu-content".*?>(.*?)<!--'
    all_img_pattern = '<div class="mm-aixiu-content".*?>(.*?)<!--'
    img_pattern = '<img.*?src="(.*?)"'

    db = DataBaseTool()
    # db.drop_db()
    db.create_db()
    session = db.get_session()
    try:
        for page in range(10)[1:10]:
            page_str = '?page=' + str(page)
            list_contents = spider.getList(page_str, list_pattern)
            for lc in list_contents:
                is_exist = session.query(ModelInfo).filter(ModelInfo.url == lc[0])
                if is_exist.count() == 0:
                    user_id = str(uuid.uuid1()).replace('-', '')
                    mi = ModelInfo(id=user_id, name=lc[2].decode('gbk'), topPic='https:' + lc[1], url='https:' + lc[0],
                                   age=lc[3],
                                   local=lc[4].decode('gbk'))
                    session.add(mi)
                    detail_url = 'https:' + lc[0]
                    img_content = spider.searchHtml(spider.getHtml(detail_url), all_img_pattern)
                    images = spider.resolveHtml(img_content, img_pattern)
                    for img in images:
                        img = ModelImage(id=str(uuid.uuid1()).replace('-', ''), imgurl='https:' + img, miid=user_id)
                        session.add(img)
                    session.flush()
                    session.commit()
    finally:
        session.flush()
        session.commit()
        db.close_session(session)

def test_save_img():
    img = 'https://img.alicdn.com/imgextra/i2/18820028431303294/T11vS3Fj4cXXXXXXXX_!!53478820-0-tstar.jpg'
    spider = Spider("http://mm.taobao.com/json/request_top_list.htm", '/data/')
    spider.saveImage(img, 'xxx/')

# get_data()
test_save_img()
